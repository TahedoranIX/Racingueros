import time as t
from OBDLibrary import obd
from LCDLibrary.lcdLibrary import LCD
from RotaryLibrary.encoder import Encoder
from os.path import exists

#Densidad de la gasolina g/L
DENSIDAD_G = 720
#Valor ideal de la mezcla estequiometrica
ESTEQUIOMETRICA = 14.7
#Nombre del archivo donde guardar la media de consumo
FILENAME = './mpg.dat'
#Min Throttle position
THROTTLE = 6


class Smart:
    def __init__(self, rs, en, d4, d5, d6, d7, port, e1, e2, eb, minimumSpeed, maxRev=5500, minRev=1200, debug=False):
        """
        Args:
            rs: Register Select pin
            en: Enable pin
            d4: Data 4 pin
            d5: Data 5 pin
            d6: Data 6 pin
            d7: Data 7 pin
            port: obd port in raspberry
            e1: OutA pin. util Menus
            e2: OutB pin. util Menus
            eb: Button pin. util StartClock
            minimumSpeed: Minimum Speed considered of vehicle
            maxRev: MaxRev of car. util RpmScreen
            minRev: MinRev of car. util RpmScreen
            debug: True/false
        """

        #Puerto conectado OBD.
        self.__port = port
        #Flag de debug.
        self.__debug = debug
        if self.__debug:
            obd.logger.setLevel(obd.logging.DEBUG)
            print("Starting ConnOBD")

        # 1º Stage - Declarations
            #./LCDLibrary/lcdlibrary.py
        self.__lcd = LCD(rs=rs, en=en, d4=d4, d5=d5, d6=d6, d7=d7)
            #./OBDLibrary/obd.py
        self.__obd = self.__connection()
            #./RotaryLibrary/encoder.py
        self.__encoder = Encoder(e1, e2, eb)

        if self.__debug:
            print("rotatorio: ", self.__encoder.getValue())

        # TURBOCARE
            #Comprueba si coche parado.
        self.__stopped = False
            #Tiempo de espera
        self.__finalTime = None
            #Velocidad minima para considerar en movimiento.
        self.__minimumSpeed = minimumSpeed

        # RPMSCREEN
            #Segmentos para mostrar en modo racing.
        self.__rpmSegments = int((maxRev - minRev) / 16)
            #Rev minimas para modo racing.
        self.__minRev = minRev

        # TIMESCREEN. DESHABILITADO, DEMASIADOS MENUS.
        #Tiempo inicial al que sumar segundos.
        #self.__initialTime = None
        #Tiempo final de cronometro: h, m, s
        #self.__lastTime = [0, 0, 0]

        # OBD DATA
            #Velocidad coche
        self.__speed = None
            #Rev de motor
        self.__rpm = None
            #Coolant temp.
        self.__cool = None
            #Acelerador posicion
        self.__throttle = 0
            #Load mpg, muestras data from file
        self.__getDataFromFile()
            #instant mpg
        self.__instMPG = None
            #maf sensor data
        self.__LPerS = None

        # FUELSCREEN
        self.__fuelIterations = 0

        # SAVE FILE
            #flag de guardado en archivo
        self.__guardado = False

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

    def startTurboCare(self, actualTime):
        """ Función auxiliar utilizada para turboCare.
            Set tiempos de inicio para el temporizador.
        """
        # Si nos acabamos de parar, set finalTime.
        if self.__speed <= self.__minimumSpeed and not self.getStopped():
            self.__stopped = True
            self.__finalTime = actualTime + 60

            if self.__debug:
                print("Start timer turbocare")
        #Si ya estabamos parados.
        elif self.__speed > self.__minimumSpeed and self.getStopped():
            self.__stopped = False

            if self.__debug:
                print("Velocidad no suficiente turbocare")

    def turboCare(self, actualTime):
        """
        Menu
            COOLANT TEMPERATURE
            CONTADOR
        """
        # Si estamos parados, printamos el tiempo que queda y temp refrigerante
        if self.__stopped:
            time = self.__finalTime - actualTime
            self.__lcd.clearDisplay()
            self.__lcd.writeMessage('Temp: ' + self.__cool + ' C')
            #Si el tiempo ya se ha cumplido, mostrar engine off.
            if time <= 0:
                self.__lcd.writeMessage('\nEngine OFF')
            #Si no, mostrar el temporizador.
            else:
                self.__lcd.writeMessage('\nTime: 00:' + str('{:0>2}'.format(int(time))))
        # Si se activa el menu pero no estamos parados
        else:
            self.__lcd.clearDisplay()
            self.__lcd.writeMessage('Temp: ' + self.__cool + ' C' + '\nEn marcha')

    def getStopped(self):
        return self.__stopped

    def getRotatory(self, menu):
        """
        Comprueba el giro del encoder.
        Args:
            menu: Cantidad de items en menu

        Returns:
            Menu number
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
        if self.__debug:
            print("pulsacion rot: ", self.__encoder.getButtonValue())
        return self.__encoder.getButtonValue()

    def __getDataFromFile(self):
        """
        Carga datos del archivo.
        Format:
            mpg
            muestras
        EOF
        """
        if exists(FILENAME):
            f = open(FILENAME, 'r')
            self.__mpg = float(f.readline())
            self.__muestras = float(f.readline())

        else:
            self.__muestras = 0
            self.__mpg = 0
            f = open(FILENAME, 'x')
            f.write('0\n0')
        f.close()

    def __saveDataToFile(self):
        """
        Guarda en archivo el mpg medio.
        Format:
            mpg
            muestras
        EOF
        """
        f = open(FILENAME, 'w')
        f.write(str(self.__mpg))
        f.write('\n')
        f.write(str(self.__muestras))
        self.__iterations = 0
        self.__guardado = True
        f.close()

    def getOBDData(self):
        """
        Get OBD data
        Returns:
            Speed, RPM, Coolant, MPG
        """

        self.__speed = int(self.__obd.query(obd.commands.SPEED).value.magnitude)
        self.__rpm = str(self.__obd.query(obd.commands.RPM).value.magnitude)
        self.__cool = str(self.__obd.query(obd.commands.COOLANT_TEMP).value.magnitude)

        self.__throttle = int(self.__obd.query(obd.commands.THROTTLE_POS).value.magnitude)
        #Estoy acelerando?
        if self.__throttle > THROTTLE:
            #Si voy a velocidad mayor que parada, cuenta consumo.
            if self.__speed > self.__minimumSpeed:
                #Si mpg guardado en archivo, marca flag.
                if self.__guardado:
                    self.__guardado = False
                self.__LPerS = float(self.__obd.query(obd.commands.MAF).value.magnitude) / (ESTEQUIOMETRICA * DENSIDAD_G)
                self.__instMPG = round(self.__LPerS * (360000 / (self.__speed + 0.0000001)), 1)
                self.__mpg = round(((self.__mpg * self.__muestras + self.__instMPG) / (self.__muestras + 1)), 1)
                self.__muestras += 1
            #Si voy a velocidad menor que parada, consumo infinito.
            else:
                self.__instMPG = '---'
        else:
            self.__instMPG = '0'
        if self.__speed < self.__minimumSpeed and not self.__guardado:
            self.__saveDataToFile()

        if self.__debug:
            print("velocidad " + str(self.__speed))
            print("rpm " + self.__rpm)
            print("coolant " + self.__cool)
            print("mezcla " + str(self.__LPerS))
            print("air flow " + str(self.__obd.query(obd.commands.MAF).value.magnitude))
            print("inst mpg " + str(self.__instMPG))
            print("media mpg " + str(self.__mpg))

    def fuelScreen(self):
        """
        Menu
            Instant MPG  Average MPG
            RPM
        """
        if self.getButtonRotatory():
            self.__fuelIterations += 1
        if self.__fuelIterations == 6:
            self.__fuelIterations = 0
            self.__mpg = 0
            self.__muestras = 0
            self.__saveDataToFile()

        self.__lcd.clearDisplay()
        self.__lcd.writeMessage('Fuel: ' + str(self.__instMPG) + ' ' + str(self.__mpg))
        self.__lcd.writeMessage('\nRPM: ' + self.__rpm)

    def rpmCoolScreen(self):
        """
        Menu
            COOLANT TEMPERATURE
            RPM
        """
        self.__lcd.clearDisplay()
        self.__lcd.writeMessage('Temp: ' + self.__cool + ' C')
        self.__lcd.writeMessage('\nRPM: ' + self.__rpm)

    def rpmScreen(self):
        """
        Menu
            SEGMENTOS LED
            RPM
        """
        self.__lcd.clearDisplay()
        actualRpm = int((float(self.__rpm) - self.__minRev) / self.__rpmSegments)
        if self.__debug:
            print(actualRpm)
            print(self.__rpmSegments)
        while actualRpm > 0:
            self.__lcd.writeRAM([1, 1, 1, 1, 1, 1, 1, 1])
            actualRpm = actualRpm - 1
        self.__lcd.writeMessage('\nRPM: ' + self.__rpm)

    """def timeScreen(self, actualTime):
        
        :param actualTime: Actual time given by main loop
        Menu
            TEMPORIZADOR
            RPM
        
        # Si se ha presionado el botón
        if self.getButtonRotatory() and self.__initialTime is not None:
            self.__initialTime = None
            h, m, s = self.__timeConvert(self.__lastTime)
            self.__lastTime = []
            self.__lastTime[:3] = h, m, s

        elif self.getButtonRotatory() or self.__initialTime is not None:
            # Empezamos el contador
            if self.__initialTime is None:
                self.__initialTime = t.time()
                self.__lastTime = None
            # Tiempo desde que empezó el contador en seg.
            self.__lastTime = actualTime - self.__initialTime
            # Conversion a horas, minutos, segundos
            h, m, s = self.__timeConvert(self.__lastTime)
            # Printamos el contador.
            self.__lcd.clearDisplay()
            self.__lcd.writeMessage("{:0>2}:{:0>2}:{:0>2}".format(h, m, s) + '\nRPM: ' + self.__rpm)

        # si el boton no esta presionado y habia valor, guardamos last time para que se quede marcado.
        else:
            self.__lcd.clearDisplay()
            self.__lcd.writeMessage("{:0>2}:{:0>2}:{:0>2}".format(self.__lastTime[0], self.__lastTime[1],
                                                                  self.__lastTime[2]) + '\nRPM: ' + self.__rpm)
"""

    def __timeConvert(self, sec):
        mins = sec // 60
        sec = sec % 60
        hours = mins // 60
        mins = mins % 60
        return int(hours), int(mins), int(sec)