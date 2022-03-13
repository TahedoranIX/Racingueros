import time as t
import obd
from Adafruit_CharLCD import Adafruit_CharLCD
from Rotaries.encoder import Encoder


#CONSTANTS
BAD_OBD = 2
OBD_OK = 1
VAR = 2

#DEBUG
obd.logger.setLevel(obd.logging.DEBUG)

#port assigned obd
ports = "/dev/rfcomm99"
ports = "/dev/pts/2"

#Init lcd screen
lcd = Adafruit_CharLCD(rs=25,en=24,d4=23,d5=18,d6=15,d7=14,cols=16,lines=2)


def connection(ports):
    """Conexión a OBD"""
    try:
        lcd.clear()
        lcd.message("Conectando...")
        c = obd.OBD(ports, fast=False, timeout=30)
        while not c.is_connected():
            c = obd.OBD(ports, fast=False, timeout=30)
        return c
    except:
        lcd.clear()
        lcd.message("No Conectado")
        c = connection(ports)
        return c

def menu():
    pass


def encoder(value):
    """Función que detecta al encoder funcionando"""
    pass

######################
###PROGRAM
######################

lcd.clear()
#first conn
c = connection(ports)
#definicion del encoder
e = Encoder(leftPin=10, rightPin=11, callback=encoder)

#while it is connected
while True:
	while c.is_connected():
		#EXTRACT RPM FROM CONNECTION
		lcd.clear()
		lcd.message('RPM: '+ c.query(obd.commands.RPM).value.magnitude)
		lcd.message('\nTemp: ' + c.query(obd.commands.COOLANT_TEMP).value.magnitude + ' ºC')
		#LITTLE DELAY
		t.sleep(.5)

    #program recovery
	c.close()
	lcd.clear()
	lcd.message('Lost\nConnection')
	c = connection(ports)

