from CarLibrary.classCar import Smart
from time import sleep

MINIMUM_SPEED = 5
port = "/dev/rfcomm99"
# port = "/dev/pts/2"
coche = Smart(rs=0, en=5, d4=26, d5=19, d6=13, d7=6, port=port)
while True:
    try:
        coche.turboCare(MINIMUM_SPEED)
        if not coche.getStopped():
            menu = coche.checkRotatory()
            if menu == 0:
                coche.rpmCoolScreen()
            elif menu == 1:
                pass
            elif menu == 2:
                pass
            elif menu == 3:
                pass
        sleep(.5)
    except:
        del coche
        sleep(2)
        coche = Smart(rs=0, en=5, d4=26, d5=19, d6=13, d7=6, port=port)
