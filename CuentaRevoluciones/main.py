from CarLibrary.classCar import Smart
import time as t

MINIMUM_SPEED = 5
MENU_QUANTITY = 4
#port = "/dev/rfcomm99"
port = "/dev/pts/2"
coche = Smart(rs=25, en=24, d4=23, d5=18, d6=15, d7=14, e1=20, e2=16, eb=21, port=port, debug=True)
while True:
        try:
            #Tiempo actual.
            actualTime = t.time()
            #Obtencion datos.
            coche.getOBDData()
            #Set Tiempo de parada
            coche.startTurboCare(MINIMUM_SPEED, actualTime)

            ############
            ###MENU
            ############
            menu = coche.getRotatory(MENU_QUANTITY)
            if menu == 0:
                coche.rpmCoolScreen()
            elif menu == 1:
                coche.rpmScreen()
            elif menu == 2:
                coche.turboCare(actualTime)
            elif menu == 3:
                coche.timeScreen(actualTime)

            #Default screen

            t.sleep(.5)

        except Exception as e:
            print(e)
            print("Reinicio SMART")
            coche.sos()
            t.sleep(2)
