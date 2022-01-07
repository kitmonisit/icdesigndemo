* MOS Sizing

* Includes
* .include ./45nm_NMOS_bulk92148.pm
.include ./45nm_LP.pm

* Options
.save v(g)
.save v(d)
.save @mn0[id]
.save @mn0[igd]
.save @mn0[igb]
.save @mn0[igs]
.save @mn0[gm]
.save @mn0[gds]
.save @mn0[cgg]
.save @mn0[vth]

* Netlist
mn0 d g 0 0 nmos w=1.140630e-05 l=1.000000e-06
vsweep d 0 dc 0.5
vg g 0 dc 8.697069e-01

* Control
.control
dc vsweep 1e-3 2 0.001
let id = @mn0[id]
let gm = @mn0[gm]
let ro = 1 / @mn0[gds]
let cgg = @mn0[cgg]
let vth = @mn0[vth]
* print @mn0[id]
* show mn0
* display
write char.dat id gm ro cgg vth v(g) v(d)
.endc

* End of file
.end

* vim:ft=spice
