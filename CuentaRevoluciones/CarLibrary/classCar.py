import time as t
from OBDLibrary import obd
from LCDLibrary.lcdLibrary import LCD
from RotaryLibrary.encoder import Encoder

MENU_QUANTITY = 3

class Smart:
    def __init__(self, rs, en, d4, d5, d6, d7, port, e1, e2, maxRev=5500, debug=False):

        self.__lcd = LCD(rs=rs, en=en, d4=d4, d5=d5, d6=d6, d7=d7)
        self.__port = port
        self.__debug = debug
        if self.__debug:
            obd.logger.setLevel(obd.logging.DEBUG)
            print("Starting ConnOBD")

        # 1º Stage - Declarations
        self.__obd = self.__connection()
        self.__encoder = Encoder(e1, e2)
        self.__encoderLast = self.__encoder.getValue()
        if self.__debug:
            print("rotatorio: ", self.__encoderLast)
        self.__stopped = False
        self.__finalTime = None
        self.__rpmSegments = int(maxRev/16)

        # OBD DATA
        self.__speed = None
        self.__rpm = None
        self.__cool = None

    def __del__(self):
        if self.__debug:
            print("Destructor Smart")
        del self.__lcd
        self.__obd.close()

    def __connection(self):
        try:
            if self.__debug:
                print("try conn")
            self.__lcd.clearDisplay()
            self.__lcd.writeMessage("Connecting...")
            connection = obd.OBD(self.__port, fast=False, timeout=30)
            while not connection.is_connected():
                if self.__debug:
                    print("while not connection")
                self.__lcd.clearDisplay()
                self.__lcd.writeMessage("Not Connected")
                t.sleep(2)
                self.__lcd.clearDisplay()
                self.__lcd.writeMessage("Connecting...")
                connection = obd.OBD(self.__port, fast=False, timeout=30)
            return connection
        except:
            if self.__debug:
                print("except conn")
            self.__lcd.clearDisplay()
            self.__lcd.writeMessage("Problems OBD")
            t.sleep(2)
            return self.__connection()

    def sos(self):
        self.__lcd.clearDisplay()
        self.__lcd.writeMessage('Connection\nLost')
        self.__obd.close()
        self.__obd = self.__connection()

    def turboCare(self, minimumSpeed):
        if self.__speed <= minimumSpeed:
            if not self.__stopped:
                self.__finalTime = int(t.time()) + 60
                self.__stopped = True
                if self.__debug:
                    print("Start timer turbocare")
            else:
                time = self.__finalTime - int(t.time())
                self.__lcd.clearDisplay()
                self.__lcd.writeMessage('Temp: ' + self.__cool + ' C')
                if time <= 0:
                    self.__lcd.writeMessage('\nEngine OFF')
                else:
                    self.__lcd.writeMessage('\nTime: 00:' + str('{:0>2}'.format(time)))
        elif self.__stopped:
            if self.__debug:
                print("Velocidad no suficiente turbocare")
            self.__stopped = False

    def getStopped(self):
        return self.__stopped

    def getOBDData(self):
        """
        Get OBD data

        :returns: Speed, RPM, Coolant
        """
        self.__speed = int(self.__obd.query(obd.commands.SPEED).value.magnitude)
        self.__rpm = str(self.__obd.query(obd.commands.RPM).value.magnitude)
        self.__cool = str(self.__obd.query(obd.commands.COOLANT_TEMP).value.magnitude)
        if self.__debug:
            print("velocidad " + str(self.__speed))
            print("rpm " + self.__rpm)
            print("coolant " + self.__cool)

    def rpmCoolScreen(self):
        self.__lcd.clearDisplay()
        self.__lcd.writeMessage('Temp: ' + self.__cool + ' C')
        self.__lcd.writeMessage('\nRPM: ' + self.__rpm)

    def rpmScreen(self):
        self.__lcd.clearDisplay()
        actualRpm = int(float(self.__rpm) / self.__rpmSegments)
        while actualRpm > 0:
            self.__lcd.writeRAM([1,1,1,1,1,1,1,1])
            actualRpm = actualRpm - 1
        self.__lcd.writeMessage('\nRPM: ' + self.__rpm)

    def checkRotatory(self):
        """
        Check Rotatory state for changing screen

        :returns: Screen number
        """
        valor = abs(self.__encoder.getValue())
        if valor > MENU_QUANTITY:
            self.__encoder.value = 0
        if self.__debug:
            print("rotatory: ", valor)
        return valor

