from CarLibrary.classCar import Smart
from time import sleep

MINIMUM_SPEED = 5
MENU_QUANTITY = 3
port = "/dev/rfcomm99"
#port = "/dev/pts/2"
coche = Smart(rs=25, en=24, d4=23, d5=18, d6=15, d7=14, e1=20, e2=16, eb=21, port=port, debug=False)
while True:
        try:
            coche.getOBDData()
            coche.turboCare(MINIMUM_SPEED)
            if not coche.getStopped():
                menu = coche.checkRotatory(MENU_QUANTITY)
                if menu == 0:
                    coche.rpmScreen()
                elif menu == 1:
                    coche.rpmCoolScreen()
                elif menu == 2:
                    coche.timeScreen()
            sleep(.5)
        except Exception as e:
            print(e)
            print("Reinicio SMART")
            coche.sos()
            sleep(2)