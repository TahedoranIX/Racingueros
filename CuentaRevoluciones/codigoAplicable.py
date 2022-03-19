import time as t
from OBDLibrary.PosibleNueva.obd import obd
from LCDLibrary.lcdLibrary import LCD

#CONSTANTS
BAD_OBD = 2
OBD_OK = 1
VAR = 2

#DEBUG
#obd.logger.setLevel(obd.logging.DEBUG)

#port assigned obd
#ports = "/dev/rfcomm99"
ports = "/dev/pts/2"


#CONNECT TO OBD
def connection(ports):
    try:
        lcd.clearDisplay()
        lcd.writeMessage("Connecting...")
        c = obd.OBD(ports, fast=False, timeout=30)
        if not c.is_connected():
            lcd.clearDisplay()
            lcd.writeMessage("Not Connected")
            t.sleep(2)
            return connection(ports)
        return c
    except:
        lcd.clearDisplay()
        lcd.writeMessage("Not Connected")
        t.sleep(2)
        return connection(ports)


######################
###PROGRAM
######################
#Init lcd screen
lcd = LCD(rs=0, en=5, d4=26, d5=19, d6=13, d7=6)
lcd.clearDisplay()
#first conn
c = connection(ports)

arrancada = False
tFinal = 0

def parado(arrancada, t1, tFinal):
    if arrancada == False:
        tFinal = int(t1) + 60
        return True, tFinal
    else:
        tiempo = tFinal - int(t1)
        if tiempo <= 0:
            lcd.writeMessage('\nEngine OFF')
        else:
            lcd.writeMessage('\nTime: 00:' + str('{:0>2}'.format(tiempo)))
        return True, tFinal

#while it is connected
while True:
    try:
        t1 = t.time()
        #EXTRACT VALUES FROM CONNECTION
        speed = int(c.query(obd.commands.SPEED).value.magnitude)
        rpm = str(c.query(obd.commands.RPM).value.magnitude)
        cool = str(c.query(obd.commands.COOLANT_TEMP).value.magnitude)

        #PRINT THEM
        lcd.clearDisplay()
        lcd.writeMessage('Temp: ' + cool + ' C')

        if speed <= 5:
            arrancada, tFinal = parado(arrancada, t1, tFinal)
        else:
            arrancada = False
            lcd.writeMessage('\nRPM: ' + rpm)
        #LITTLE DELAY
        t.sleep(.5)
    except:
        c.close()
        lcd.clearDisplay()
        lcd.writeMessage('Lost\nConnection')
        t.sleep(2)
        c = connection(ports)
