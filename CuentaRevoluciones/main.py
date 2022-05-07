from CarLibrary.classCar import Smart
import time as t

MINIMUM_SPEED = 5
MENU_QUANTITY = 4
#port = "/dev/rfcomm99" # Puerto que asignado al OBD
port = "/dev/pts/2" # Puerto del OBD virtual
coche = Smart(rs=25, en=24, d4=23, d5=18, d6=15, d7=14, e1=20, e2=16, eb=21, port=port, minimumSpeed=MINIMUM_SPEED, debug=False)
#coche = Smart(rs=0, en=5, d4=26, d5=19, d6=13, d7=6, e1=20, e2=16, eb=21, port=port, minimumSpeed=MINIMUM_SPEED, debug=False) # Configuración para otra raspberry.
while True:
        try:
            #Tiempo actual.
            actualTime = t.time()
            #Obtencion datos.
            coche.getOBDData()
            #Set Tiempo de parada
            coche.startTurboCare(actualTime)

            ############
            ###MENU
            ############
            menu = coche.getRotatory(MENU_QUANTITY)
            if menu == 0:
                coche.rpmCoolScreen()
            elif menu == 1:
                coche.fuelScreen()
            elif menu == 2:
                coche.rpmScreen()
            elif menu == 3:
                coche.turboCare(actualTime)

            t.sleep(.5)

        except Exception as e:
            print(e)
            print("Reinicio SMART")
            coche.sos()
            t.sleep(2)
