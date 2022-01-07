* MOS Sizing

* Includes
*******************************************************************
* Model name       : 1N6640U
* Description      : Aerospace 0.3 A - 75 V switching diode
* Package type     : LCC2D
*******************************************************************
.MODEL 1N6640U D IS=15.471E-9 N=2.0208 RS=.47849 IKF=38.722E-3 CJO=1.5914E-12 M=.11684
+ VJ=.3905 ISR=10.010E-21 NR=4.9950 TT=0 FC=0.5 XTI=3 EG=1.11

* Options
.save @vsweep[i]

* Netlist
d0 anode cathode 1N6640U
r0 cathode 0 52k
vsweep anode 0 dc 0.5

* Control
.control
dc vsweep 1 2 0.2
* print @mn0[id]
* show mn0
* display
write diode.dat @vsweep[i]
.endc

* End of file
.end

* vim:ft=spice
