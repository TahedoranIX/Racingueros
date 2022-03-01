import time as t
import obd
from Adafruit_CharLCD import Adafruit_CharLCD

#CONSTANTS
t.sleep(1)
BAD_OBD = 2
OBD_OK = 1
VAR = 2

#DEBUG
#obd.logger.setLevel(obd.logging.DEBUG)

#port assigned obd
#rc.local: rfcomm bind rfcomm99 00:1D:A5:68:98:8B
ports = "/dev/rfcomm99"
#ports = "/dev/pts/1"

#Init lcd screen
lcd = Adafruit_CharLCD(rs=25,en=24,d4=23,d5=18,d6=15,d7=14,cols=16,lines=2)
lcd.clear()
#CONNECT TO OBD
def connection(ports):
	try:
		c = obd.OBD(ports)
		if c.status() != obd.OBDStatus.CAR_CONNECTED:
			return obd.OBDstatus.NOT_CONNECTED,BAD_OBD
		return c,OBD_OK
	except:
		lcd.clear()
		lcd.message("Er OBD")
		return obd.OBDStatus.NOT_CONNECTED,BAD_OBD

#BASIC STAGE OF CONNECTION
def fStage():
    #if obd not connected, keep trying until it is
    c,var = connection(ports)
    while var == BAD_OBD:
        t.sleep(10)
        c,var = connection(ports)
        lcd.message('\nReloj: '+t.strftime("%H:%M",t.localtime()))
    return c

######################
###PROGRAM
######################
#first conn
c = fStage()

#while it is connected
while c.is_connected():
	#EXTRACT RPM FROM CONNECTION
	s = str(c.query(obd.commands.RPM))
	for i in range(10):
		#FIND A SPACE TO ONLY SHOW THE NUMBER
		if ' ' == s[i]:
			lcd.clear()
			lcd.message('RPM: '+s[:i])
			lcd.message('\nReloj: '+t.strftime("%H:%M",t.localtime()))
			#l.message(str(c.query(obd.commands.COOLANT_TEMP)))
			#LITTLE DELAY
			t.sleep(.5)
		if not c.is_connected():
			c.close()
			lcd.clear()
			lcd.message('Lost Conn')
			lcd.message('\nReloj: '+t.strftime("%H:%M",t.localtime()))
			c = fStage()
			break
