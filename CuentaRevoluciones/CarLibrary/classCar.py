import time as t
from OBDLibrary.obd import obd
from LCDLibrary.lcdLibrary import LCD


class Smart:
    def __init__(self, rs, en, d4, d5, d6, d7, port, debug=False):

        self.__lcd = LCD(rs=rs, en=en, d4=d4, d5=d5, d6=d6, d7=d7)
        self.__port = port
        self.__debug = debug
        if self.__debug:
            obd.logger.setLevel(obd.logging.DEBUG)
            print("Starting ConnOBD")

        # 1º Stage - Declarations
        self.__obd = self.__connection()
        self.__stopped = False
        self.__finalTime = None

        # OBD DATA
        self.__speed = None
        self.__rpm = None
        self.__cool = None

    def __del__(self):
        if self.__debug:
            print("Destructor Smart")
        self.__lcd.clearDisplay()
        self.__lcd.writeMessage('Lost\nConnection')
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
                connection = obd.OBD(self.__port, fast=False, timeout=30)
            return connection
        except:
            if self.__debug:
                print("except conn")
            self.__lcd.clearDisplay()
            self.__lcd.writeMessage("Problems")
            t.sleep(2)
            return self.__connection()

    def turboCare(self, minimumSpeed):
        if self.__speed <= minimumSpeed:
            if not self.__stopped:
                self.__finalTime = int(t.time()) + 60
                self.__stopped = True
                self.rpmCoolScreen()
            else:
                time = self.__finalTime - int(t.time())
                self.__lcd.writeMessage('Temp: ' + self.__cool + ' C')
                if time <= 0:
                    self.__lcd.writeMessage('\nEngine OFF')
                else:
                    self.__lcd.writeMessage('\nTime: 00:' + str('{:0>2}'.format(time)))
        elif self.__stopped:
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

        return self.__speed, self.__rpm, self.__cool

    def rpmCoolScreen(self):
        self.__lcd.clearDisplay()
        self.__lcd.writeMessage('Temp: ' + self.__cool + ' C')
        self.__lcd.writeMessage('\nRPM: ' + self.__rpm)

    def connectionLost(self):
        self.__lcd.clearDisplay()
        self.__lcd.writeMessage('Connection\nLost')

    def checkRotatory(self):
        """
        Check Rotatory state for changing screen

        :returns: Screen number
        """
        return 0
