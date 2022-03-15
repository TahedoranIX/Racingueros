import time as t
from OBDLibrary.PosibleNueva.obd import obd
from Adafruit_CharLCD import Adafruit_CharLCD

#CONSTANTS
BAD_OBD = 2
OBD_OK = 1
VAR = 2

#DEBUG
#obd.logger.setLevel(obd.logging.DEBUG)

#port assigned obd
ports = "/dev/rfcomm99"
#ports = "/dev/pts/1"

#Init lcd screen
lcd = Adafruit_CharLCD(rs=25,en=24,d4=23,d5=18,d6=15,d7=14,cols=16,lines=2)

#CONNECT TO OBD
def connection(ports):
    try:
        lcd.clear()
        lcd.message("Conectando...")
        c = obd.OBD(ports, fast=False, timeout=30)
        if not c.is_connected():
            return obd.OBDstatus.NOT_CONNECTED,BAD_OBD
        lcd.clear()
        lcd.message("Conectado")
        return c,OBD_OK
    except:
        lcd.clear()
        lcd.message("No Conectado")
        return obd.OBDStatus.NOT_CONNECTED,BAD_OBD

#BASIC STAGE OF CONNECTION
def fStage():
    #if obd not connected, keep trying until it is
    c, var = connection(ports)
    while var == BAD_OBD:
        c, var = connection(ports)
        #lcd.message('\nReloj: '+t.strftime("%H:%M",t.localtime()))
    return c


######################
###PROGRAM
######################

lcd.clear()
lcd.message("Arrancando...")
#first conn
c = fStage()
arrancada = False

#while it is connected
while True:
    try:
        t1 = t.time()
        #EXTRACT VALUES FROM CONNECTION
        speed = int(c.query(obd.commands.SPEED).value.magnitude)
        rpm = str(c.query(obd.commands.RPM).value.magnitude)
        cool = str(c.query(obd.commands.COOLANT_TEMP).value.magnitude)
        #PRINT THEM
        lcd.clear()
        lcd.message('RPM: '+ rpm)
        if speed <= 5:
            if arrancada == False:
                tStart = t.time()
                tFinal = int(tStart) + 60
                arrancada = True
            else:
                if int(t1) >= int(tStart) + 10:
                    tiempo = tFinal - int(t1)
                    if tiempo <= 0:
                        lcd.message('\nEngine OFF')
                    else:
                        lcd.message('\nTiempo: 00:' + str('{:0>2}'.format(tiempo)))
                else:
                    lcd.message('\nTemp: ' + cool + ' C')
        else:
            arrancada = False
            lcd.message('\nTemp: ' + cool + ' C')
        #LITTLE DELAY
        t.sleep(.5)
    except:
        c.close()
        lcd.clear()
        lcd.message('Lost\nConnection')
        c = fStage()
