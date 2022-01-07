* MOS Sizing

* Includes
* .include ./45nm_NMOS_bulk92148.pm
.include ./45nm_LP.pm

* Options
.save v(g)
.save v(d)
.save v(target_vd)
.save @mn0[id]
.save @mn0[igd]
.save @mn0[igb]
.save @mn0[igs]
.save @mn0[gm]
.save @mn0[gds]

* Netlist
idd 0 d dc 1.500000e-04
e0 g 0 target_vd d 10000
vsweep target_vd 0 dc 0.5
mn0 d g 0 0 nmos w=1.140630e-05 l=1.000000e-06

* Control
.control
dc vsweep 0.1 2 0.001
let id = @mn0[id]
let gm = @mn0[gm]
* print @mn0[id]
* show mn0
* display
write biasing.dat id gm v(g) v(d) v(target_vd)
.endc

* End of file
.end

* vim:ft=spice
