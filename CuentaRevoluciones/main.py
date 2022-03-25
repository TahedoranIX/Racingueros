from CarLibrary.classCar import Smart
from time import sleep

MINIMUM_SPEED = 5
# port = "/dev/rfcomm99"
port = "/dev/pts/2"
coche = Smart(rs=0, en=5, d4=26, d5=19, d6=13, d7=6, e1=None, e2=None, port=port, debug=False)
while True:
        try:
            coche.getOBDData()
            coche.turboCare(MINIMUM_SPEED)
            if not coche.getStopped():
                menu = coche.checkRotatory()
                if menu == 0:
                    coche.rpmScreen()
                elif menu == 1:
                    coche.rpmCoolScreen()
                elif menu == 2:
                    pass
                elif menu == 3:
                    pass
            sleep(.5)
        except:
            print("Reinicio SMART")
            coche.sos()
            sleep(2)