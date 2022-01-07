import pandas as pd
import sympy as sp
import numpy as np


class Amplifier:
    def __init__(self, G):
        self.G = G
        self.stimulus_vector = sp.Matrix([0, 0, 0, 1])
        self.response_vector = self.G.inv() * self.stimulus_vector

        self.G = self.G.subs(
            {
                sp.symbols("g_{o1}"): 1 / sp.symbols("r_{o1}"),
                sp.symbols("Y_L"): 1 / sp.symbols("R_L")
                + sp.symbols("s") * sp.symbols("C_L"),
            }
        )

        self.gm1 = 10e-3
        self.gm2 = 10e-3
        self.ro1 = 500e3
        self.RL = 2e3
        self.CL = 15e-12
        self.CM = 5e-12

    def __repr__(self):
        display(self.G)
        out = (
            f"gm1 = {self.gm1:.3e}",
            f"gm2 = {self.gm1:.3e}",
            f"ro1 = {self.ro1:.3e}",
            f"RL = {self.RL:.3e}",
            f"CL = {self.CL:.3e}",
            f"CM = {self.CM:.3e}",
        )
        return "\n".join(out)

    def voltage_gain(
        self,
        *,
        gm1=10e-3,
        gm2=10e-3,
        ro1=500e3,
        RL=2e3,
        CL=15e-12,
        CM=5e-12,
    ):
        """
        Returns a voltage gain function that accepts a 1-D array of
        frequencies in Hz.
        """
        sp_gm1, sp_gm2 = sp.symbols("g_{m1} g_{m2}")
        sp_go1 = sp.symbols("g_{o1}")
        sp_CM = sp.symbols("C_M")
        sp_RL = sp.symbols("R_L")
        sp_CL = sp.symbols("C_L")
        sp_YL = sp.symbols("Y_L")
        sp_s = sp.symbols("s")
        sp_f = sp.symbols("f")

        self.gm1 = gm1
        self.gm2 = gm2
        self.ro1 = ro1
        self.RL = RL
        self.CL = CL
        self.CM = CM

        gain = self.response_vector[2]
        gain = gain.subs(
            {
                sp_gm1: gm1,
                sp_gm2: gm2,
                sp_CM: CM,
                sp_go1: 1 / ro1,
                sp_YL: 1 / RL + sp_s * CL,
                sp_RL: RL,
                sp_CL: CL,
            }
        )
        gain = gain.subs(
            {
                sp_s: 2 * sp.pi * sp_f * 1j,
            }
        )

        # num, den = gain.as_numer_denom()
        # self.UGF = np.float(abs(sp.solve(num - den)[1]))
        return sp.lambdify(sp_f, gain)


import ipywidgets as widgets

import bokeh.io as bkio
import bokeh.models as bkm
import bokeh.layouts as bkl
import bokeh.plotting as bkp

def create_slider(value, min, max, step, readout_format=".3f"):
    return widgets.FloatSlider(
        value=value, min=min, max=max, step=step, readout_format=readout_format
    )


def run_interactive(amp_exact, amp_approx):
    bkio.output_notebook()

    freq = np.logspace(-3, 12, 1000)

    fn_exact = amp_exact.voltage_gain()
    fn_approx = amp_approx.voltage_gain()

    mag_exact = 20 * np.log10(np.abs(fn_exact(freq)))
    pha_exact = np.angle(fn_exact(freq), deg=True)

    mag_approx = 20 * np.log10(np.abs(fn_approx(freq)))
    pha_approx = np.angle(fn_approx(freq), deg=True)

    f1 = bkp.figure(
        width=600,
        height=200,
        x_axis_type="log",
    )
    f1.y_range = bkm.Range1d(-50, 150)

    f2 = bkp.figure(
        width=600,
        height=200,
        x_axis_type="log",
    )
    f2.y_range = bkm.Range1d(-90, 180)

    mag_exact_line = f1.line(freq, mag_exact, color="#8888cc")
    pha_exact_line = f2.line(freq, pha_exact, color="#8888cc")
    mag_approx_line = f1.line(freq, mag_approx, color="#cc8888")
    pha_approx_line = f2.line(freq, pha_approx, color="#cc8888")

    # UGF_line = bkm.Span(location=amp_exact.UGF, dimension='height')
    # f1.renderers.extend([UGF_line])
    # f2.renderers.extend([UGF_line])

    output = bkl.column(f1, f2)

    def update(
        gm1=10e-3,
        gm2=10e-3,
        ro1=500e3,
        RL=2e3,
        CL=15e-12,
        CM=5e-12,
    ):
        fn_exact = amp_exact.voltage_gain(
            gm1=gm1,
            gm2=gm2,
            ro1=ro1,
            RL=RL,
            CL=CL,
            CM=CM,
        )
        mag_exact_line.data_source.data["y"] = 20 * np.log10(np.abs(fn_exact(freq)))
        pha_exact_line.data_source.data["y"] = np.angle(fn_exact(freq), deg=True)

        fn_approx = amp_approx.voltage_gain(
            gm1=gm1,
            gm2=gm2,
            ro1=ro1,
            RL=RL,
            CL=CL,
            CM=CM,
        )
        mag_approx_line.data_source.data["y"] = 20 * np.log10(np.abs(fn_approx(freq)))
        pha_approx_line.data_source.data["y"] = np.angle(fn_approx(freq), deg=True)
        # UGF_line.location = amp_exact.UGF
        bkio.push_notebook()

    bkio.show(output, notebook_handle=True)

    widgets.interact(
        update,
        gm1=create_slider(10e-3, 1e-3, 500e-3, 1e-3),
        gm2=create_slider(10e-3, 1e-3, 500e-3, 1e-3),
        ro1=widgets.FloatLogSlider(value=500e3, base=10, min=3, max=9, step=0.01, readout_format=".2e"),
        RL=widgets.FloatLogSlider(value=2e3, base=10, min=1, max=6, step=0.01, readout_format=".2e"),
        CL=widgets.FloatLogSlider(value=15e-12, base=10, min=-15, max=-9, step=0.01, readout_format=".2e"),
        CM=widgets.FloatLogSlider(value=5e-12, base=10, min=-24, max=-9, step=0.01, readout_format=".2e"),
    )
