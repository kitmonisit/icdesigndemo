* MOS Sizing

* Includes
* .include ./45nm_NMOS_bulk92148.pm
.include ./45nm_LP.pm

* Options
.save @mn0[id]
.save @mn0[igd]
.save @mn0[igb]
.save @mn0[igs]
.save @mn0[gm]
.save @mn0[gds]

* Netlist
vsweep d 0 dc 1
mn0 d d 0 0 nmos w=1.140630e-05 l=1.000000e-06

* Control
.control
dc vsweep 1e-3 2 0.001
let id = @mn0[id]
let gm = @mn0[gm]
* print @mn0[id]
* show mn0
* display
write sizing.dat id gm
.endc

* End of file
.end

* vim:ft=spice
