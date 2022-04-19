import time as t
from OBDLibrary import obd
from LCDLibrary.lcdLibrary import LCD
from RotaryLibrary.encoder import Encoder

class Smart:
    def __init__(self, rs, en, d4, d5, d6, d7, port, e1, e2, eb, maxRev=5500, debug=False):
        """
        Args:
            rs: Register Select pin
            en: Enable pin
            d4: Data 4 pin
            d5: Data 5 pin
            d6: Data 6 pin
            d7: Data 7 pin
            port: obd port in raspberry
            e1: OutA pin
            e2: OutB pin
            eb: Button pin
            maxRev: MaxRev of car
            debug: True/false
        """
        self.__lcd = LCD(rs=rs, en=en, d4=d4, d5=d5, d6=d6, d7=d7)
        self.__port = port
        self.__debug = debug
        if self.__debug:
            obd.logger.setLevel(obd.logging.DEBUG)
            print("Starting ConnOBD")

        # 1º Stage - Declarations
        self.__obd = self.__connection()
        self.__encoder = Encoder(e1, e2, eb)

        if self.__debug:
            print("rotatorio: ", self.__encoder.getValue())

        #TURBOCARE
        self.__stopped = False
        self.__finalTime = None

        #RPMSCREEN
        self.__rpmSegments = int(maxRev/16)

        #TIMESCREEN
        self.__initialTime = None
        self.__lastTime = [0,0,0]

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


    def startTurboCare(self, minimumSpeed, actualTime):
        # Estamos por debajo de la velocidad minima?
        # Si nos acabamos de parar, set finalTime
        if self.__speed <= minimumSpeed and not self.__stopped:
            self.__stopped = True
            self.__finalTime = actualTime + 60

            if self.__debug:
                print("Start timer turbocare")

        elif self.__speed > minimumSpeed and self.__stopped:
            self.__stopped = False

            if self.__debug:
                print("Velocidad no suficiente turbocare")


    def turboCare(self, actualTime):
        #Si estamos parados, printamos el tiempo que queda y temp refrigerante
        if self.__stopped:
            time = self.__finalTime - actualTime
            self.__lcd.clearDisplay()
            self.__lcd.writeMessage('Temp: ' + self.__cool + ' C')
            if time <= 0:
                self.__lcd.writeMessage('\nEngine OFF')
            else:
                self.__lcd.writeMessage('\nTime: 00:' + str('{:0>2}'.format(int(time))))
        #Si se activa el menu pero no estamos parados
        else:
            self.__lcd.clearDisplay()
            self.__lcd.writeMessage('Temp: ' + self.__cool + ' C' + '\nEn marcha')


    def getStopped(self):
        return self.__stopped


    def getRotatory(self, menu):
        """
        Check Rotatory state for changing screen

        :returns: Screen number
        """
        valor = self.__encoder.getValue()
        if valor > (menu - 1):
            self.__encoder.value = 0
            valor = 0
        elif valor < 0:
            valor = (menu - 1)
            self.__encoder.value = (menu - 1)
        if self.__debug:
            print("rotatory: ", valor)
        return valor

    def getButtonRotatory(self):
        return self.__encoder.getButtonValue()


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
        """
        Rpm with coolant temp screen
        """
        self.__lcd.clearDisplay()
        self.__lcd.writeMessage('Temp: ' + self.__cool + ' C')
        self.__lcd.writeMessage('\nRPM: ' + self.__rpm)


    def rpmScreen(self):
        """
        Rpm with revcounter
        """
        self.__lcd.clearDisplay()
        actualRpm = int(float(self.__rpm) / self.__rpmSegments)
        while actualRpm > 0:
            self.__lcd.writeRAM([1,1,1,1,1,1,1,1])
            actualRpm = actualRpm - 1
        self.__lcd.writeMessage('\nRPM: ' + self.__rpm)

    def timeScreen(self, actualTime):
        """
        StopWatch screen
        :param actualTime: Actual time given by main loop
        """
        #Si se ha presionado el botón
        if self.getButtonRotatory():
            #Empezamos el contador
            if self.__initialTime == None:
                self.__initialTime = t.time()
                self.__lastTime = None
            else:
                #Tiempo desde que empezó el contador en seg.
                self.__lastTime = actualTime - self.__initialTime
                #Conversion a horas, minutos, segundos
                h, m, s = self.__timeConvert(self.__lastTime)
                #Printamos el contador.
                self.__lcd.clearDisplay()
                self.__lcd.writeMessage("{:0>2}:{:0>2}:{:0>2}".format(h, m, s) + '\nRPM: ' + self.__rpm)

        #si el boton no esta presionado y habia valor, guardamos last time para que se quede marcado.
        elif self.__initialTime != None:
            self.__initialTime = None
            h, m, s = self.__timeConvert(self.__lastTime)
            self.__lastTime = []
            self.__lastTime[:3] = h, m, s
        else:
            self.__lcd.clearDisplay()
            self.__lcd.writeMessage("{:0>2}:{:0>2}:{:0>2}".format(self.__lastTime[0], self.__lastTime[1], self.__lastTime[2]) + '\nRPM: ' + self.__rpm)

    def __timeConvert(self, sec):
        mins = sec // 60
        sec = sec % 60
        hours = mins // 60
        mins = mins % 60
        return int(hours), int(mins), int(sec)







