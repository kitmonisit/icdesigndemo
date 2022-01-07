import pexpect
import numpy as np
from pexpect import replwrap
from functools import partial
from scipy.optimize import minimize
from scipy.interpolate import interp1d
from pathlib import Path
from . import spice3read as sr
import pandas as pd


def write_sizing_script(width, length):
    with open("sizing.template", "r") as fdr, open("sizing.sp", "w") as fdw:
        template = fdr.read()
        fdw.write(template.format(**locals()))


def get_width(starting_width, length, target_vstar, target_gm, tol=1e-4):
    ngspice = replwrap.REPLWrapper(
        cmd_or_spawn="ngspice",
        orig_prompt="->",
        prompt_change=None,
    )

    for p in Path(".").glob("sizing_*.dat"):
        p.unlink()
    width = starting_width
    iteration = 0

    target_idd = target_gm * target_vstar / 2

    while True:
        write_sizing_script(width, length)
        ngspice.run_command("source sizing.sp")

        data = sr.read(f"sizing.dat")
        idd = data["i(id)"][0]
        gm = data["gm"][0]
        gmoverid = gm / idd
        vstar = 2 * idd / gm

        interpolator = interp1d(x=vstar, y=idd)
        idd_at_target_vstar = interpolator(target_vstar)

        ratio = target_idd / idd_at_target_vstar

        if abs(ratio - 1) < tol:
            try:
                ngspice.run_command("exit")
            except pexpect.EOF:
                pass
            return {
                "RESULT_SWEEP": pd.DataFrame(
                    data={
                        "vstar": vstar,
                        "gmoverid": gmoverid,
                        "id": idd,
                        "id_unit": idd / (width / length),
                    }
                ),
                "RESULT_SWEEP_XY": {
                    "TARGET_VSTAR": target_vstar,
                    "TARGET_GMOVERID": 2 / target_vstar,
                    "TARGET_ID": target_idd,
                    "TARGET_ID_UNIT": target_idd / (width / length),
                },
                "RESULT_SIZE": {
                    "WIDTH": width,
                    "LENGTH": length,
                },
            }

        width = width * ratio
        iteration += 1


def write_biasing_script(idd, width, length):
    with open("biasing.template", "r") as fdr, open("biasing.sp", "w") as fdw:
        template = fdr.read()
        fdw.write(template.format(**locals()))


def get_vg(idd, width, length, target_vd):
    ngspice = replwrap.REPLWrapper(
        cmd_or_spawn="ngspice",
        orig_prompt="->",
        prompt_change=None,
    )

    for p in Path(".").glob("biasing.dat"):
        p.unlink()
    write_biasing_script(idd, width, length)
    ngspice.run_command("source biasing.sp")
    try:
        ngspice.run_command("exit")
    except pexpect.EOF:
        pass

    data = sr.read("biasing.dat")
    vg = data["v(g)"][0]
    vd = data["v(d)"][0]
    gm = data["gm"][0]
    idd = data["i(id)"][0]

    interpolator = interp1d(x=vd, y=vg)

    return {
        "RESULT_SWEEP": pd.DataFrame(
            data={
                "vd": vd,
                "vg": vg,
            }
        ),
        "RESULT_SWEEP_XY": {
            "TARGET_VD": target_vd,
            "TARGET_VG": interpolator(np.array(target_vd, ndmin=1))[0],
        },
    }


def write_char_script(width, length, vg):
    with open("char.template", "r") as fdr, open("char.sp", "w") as fdw:
        template = fdr.read()
        fdw.write(template.format(**locals()))


def get_char(width, length, vg, target_vd, target_gm):
    ngspice = replwrap.REPLWrapper(
        cmd_or_spawn="ngspice",
        orig_prompt="->",
        prompt_change=None,
    )

    for p in Path(".").glob("char.dat"):
        p.unlink()
    write_char_script(width, length, vg)
    ngspice.run_command("source char.sp")
    try:
        ngspice.run_command("exit")
    except pexpect.EOF:
        pass

    data = sr.read("char.dat")
    vg = data["v(g)"][0]
    vd = data["v(d)"][0]
    gm = data["gm"][0]
    ro = data["ro"][0]
    cgg = data["cgg"][0]
    vth = data["v(vth)"][0]
    idd = data["i(id)"][0]

    interpolator = interp1d(x=vd, y=idd)

    return {
        "RESULT_SWEEP": pd.DataFrame(
            data={
                "vg": vg,
                "vd": vd,
                "id": idd,
                "gm": gm,
                "cgg": cgg,
                "vth": vth,
                "ro": ro,
            }
        ),
        "RESULT_SWEEP_XY": {
            "TARGET_VD": target_vd,
            "TARGET_ID": interpolator(np.array(target_vd, ndmin=1))[0],
            "TARGET_GM": interp1d(x=vd, y=gm)(np.array(target_vd, ndmin=1))[0],
            "TARGET_RO": interp1d(x=vd, y=ro)(np.array(target_vd, ndmin=1))[0],
            "TARGET_VTH": interp1d(x=vd, y=vth)(np.array(target_vd, ndmin=1))[0],
        },
    }
