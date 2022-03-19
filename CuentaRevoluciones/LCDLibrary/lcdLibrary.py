import RPi.GPIO as GPIO
from time import sleep
'''
GPIO.setmode(GPIO.BOARD)
GPIO.setup(7, GPIO.OUT)

GPIO.output(7, True)

p = GPIO.PWM(11, 50)
p.start(6)
p.ChangeDutyCycle(4)
p.ChangeFrequency(60)
p.stop()
'''

LOW_TIME = 0.000040
HIGH_TIME = 0.00153
GPIO.setwarnings(False)

class LCD:
    def __init__(self, d4, d5, d6, d7, en, rs):
        '''Pin set and LCD init'''

        #######################
        # pin assignment
        #######################
        GPIO.setmode(GPIO.BCM)
        self.__datas = [d7,d6,d5,d4]
        self.__en = en
        self.__rs = rs
        for pin in (rs, en, d4, d5, d6, d7):
            GPIO.setup(pin, GPIO.OUT)
         
        #######################
        # begin INIT
        #######################
        GPIO.output(en, 0)
        
        #function set1
        GPIO.output(rs, 0)
        GPIO.output(self.__datas, (0,0,1,1))
        self.__enviar()
        sleep(LOW_TIME)
        #function set2
        self.__functionSet()
        #function set3
        self.__functionSet()
        #display on
        self.display()
        #clear
        self.clearDisplay()
        #entry mode
        self.__entryMode()

        #######################
        # end INIT
        #######################
        
    def __enviar(self):
        ''' Trigger PIN ENABLE'''
        GPIO.output(self.__en, 1)
        GPIO.output(self.__en, 0)

    def __sendCommand(self, rs, data, time):
        ''' SendCommand to LCD

            :arg rs: Pin RS (instruction/data register)
            :arg data: 8bit list data.
            :arg time: HIGH_TIME/LOW_TIME
        '''
        GPIO.output(self.__rs, rs)
        GPIO.output(self.__datas, data[:4])
        self.__enviar()
        GPIO.output(self.__datas, data[4:])
        self.__enviar()
        sleep(time)

    def __functionSet(self):
        ''' Set bit mode LCD, only used in init'''
        self.__sendCommand(rs=0, data=[0,0,1,0,1,0,0,0], time=LOW_TIME)

    def __setCGRAM(self, address):
        ''' Set CGRAM address to AC (custom chars)

            :args address: 6bit Address(5-0)
        '''
        self.__sendCommand(rs=0, data=[0,1,address[0],address[1],address[2],address[3],address[4],address[5]], time=LOW_TIME)

    def __setDDRAM(self, address):
        ''' Set DDRAM addresss to AC ('\ n' for example)

            :args address: 7bit Address(6-0)
        '''
        self.__sendCommand(rs=0, data=[1,address[0],address[1],address[2],address[3],address[4],address[5],address[6]], time=LOW_TIME)

    def __writeRAM(self, data):
        '''  Write data in RAM, show chars.

        :args data: 8bit data package.
        '''
        self.__sendCommand(rs=1, data=data, time=LOW_TIME)

    def __entryMode(self,cursor=1,display=0):
        ''' Set moving direction of cursor and display.

            :arg cursor: set orientation of cursor
            :arg display: shift entire display
        '''
        self.__sendCommand(rs=0, data=[0,0,0,0,0,1,cursor,display], time=LOW_TIME)

    def clearDisplay(self):
        ''' Clear all display data'''
        self.__sendCommand(rs=0, data=[0,0,0,0,0,0,0,1], time=HIGH_TIME)
        
    def home(self):
        ''' Return cursor to home'''
        self.__sendCommand(rs=0, data=[0,0,0,0,0,0,1,0], time=HIGH_TIME)

    def display(self, display=1, cursor=0, blink=0):

        '''View options

            :arg display: Show messages in display
            :arg cursor: Show cursor
            :arg blink: Show blinking cursor
        '''
        self.__sendCommand(rs=0, data=[0,0,0,0,1,display,cursor,blink], time=LOW_TIME)

    def moveCursor(self, cursor=0, direction=1, times=1):
        '''
        View options

            :arg cursor: Shift cursor(0) display(1)
            :arg direction: Direction right(1) left(0)
            :arg times: Times to move
        '''
        for i in range(times):
            self.__sendCommand(rs=0, data=[0,0,0,1,cursor,direction,0,0], time=LOW_TIME)
    
    def textLeftRight(self):
        ''' Writes to the right (Normal)'''

        self.__sendCommand(rs=0, data=[0,0,0,0,0,1,1,0], time=LOW_TIME)
        
    def textRightLeft(self):
        ''' Writes to the left ¿?'''
        self.__sendCommand(rs=0, data=[0,0,0,0,0,1,0,0], time=LOW_TIME)

    def writeMessage(self, message):
        '''Write message in display '''
        for char in message:
            if char == '\n':
                self.__setDDRAM([1,0,0,0,0,0,0])
            else:
                dataMessage = []
                letra = bin(ord(char))[2:].zfill(8)
                for binario in letra:
                    dataMessage.append(int(binario))
                self.__writeRAM(dataMessage)
        

h = LCD(d4=26,d5=19,d6=13,d7=6,en=5,rs=0)
h.writeMessage("hola que tal\nyo bien")
h.writeMessage("perro")
h.home()
h.clearDisplay()
GPIO.cleanup()
