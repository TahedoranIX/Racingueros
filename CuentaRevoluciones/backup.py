import time as t
from nuevoOBD import obd
from Adafruit_CharLCD import Adafruit_CharLCD

#DEBUG
#obd.logger.setLevel(obd.logging.DEBUG)

#port assigned obd
#ports = "/dev/rfcomm99"
ports = "/dev/pts/2"


#CONNECT TO OBD
def connection(ports):
    try:
        lcd.clear()
        lcd.message("Connecting...")
        c = obd.OBD(ports, fast=False, timeout=30)
        if not c.is_connected():
            lcd.clear()
            lcd.message("Not Connected")
            t.sleep(2)
            return connection(ports)
        return c
    except:
        lcd.clear()
        lcd.message("Not Connected")
        t.sleep(2)
        return connection(ports)


######################
###PROGRAM
######################
#Init lcd screen
lcd = Adafruit_CharLCD(rs=25,en=24,d4=23,d5=18,d6=15,d7=14,cols=16,lines=2)
lcd.clear()
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
            lcd.message('\nEngine OFF')
        else:
            lcd.message('\nTime: 00:' + str('{:0>2}'.format(tiempo)))
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
        lcd.clear()
        lcd.message('Temp: ' + cool + ' C')

        if speed <= 5:
            arrancada, tFinal = parado(arrancada, t1, tFinal)
        else:
            arrancada = False
            lcd.message('\nRPM: ' + rpm)
        #LITTLE DELAY
        t.sleep(.5)
    except:
        c.close()
        lcd.clear()
        lcd.message('Lost\nConnection')
        t.sleep(2)
        c = connection(ports)
