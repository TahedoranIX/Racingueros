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

class LCD:
    def __init__(self, d4, d5, d6, d7, en, rs):
        #DEFINICIÓN DE PINES
        GPIO.setmode(GPIO.BCM)
        self.datas = [d7,d6,d5,d4]
        self.en = en
        self.rs = rs
        for pin in (rs, en, d4, d5, d6, d7):
            GPIO.setup(pin, GPIO.OUT)
         
        '''BEGIN INIT''' 
        GPIO.output(en, 0)
        
        #function set1
        GPIO.output(rs, 0)
        GPIO.output(self.datas, (0,0,1,1))
        self.enviar()
        sleep(LOW_TIME)
        
        #function set2
        self.functionSet()
        #function set3
        self.functionSet()
        #display on
        self.display(1,1,1)
        #clear
        self.clearDisplay()
        
        #entry mode
        GPIO.output(rs, 0)
        GPIO.output(self.datas, (0,0,0,0))
        GPIO.output(en, 1)
        GPIO.output(en, 0)
        GPIO.output(self.datas, (0,1,1,0))
        GPIO.output(en, 1)
        GPIO.output(en, 0)
        sleep(LOW_TIME)
        
        '''END INIT'''
        
    def enviar(self):
        GPIO.output(self.en, 1)
        GPIO.output(self.en, 0)
        
    def functionSet(self):
        GPIO.output(self.rs, 0)
        GPIO.output(self.datas, (0,0,1,0))
        self.enviar()
        GPIO.output(self.datas, (1,0,0,0))
        self.enviar()
        sleep(LOW_TIME)
                
    def clearDisplay(self):
        GPIO.output(self.rs, 0)
        GPIO.output(self.datas, (0,0,0,0))
        self.enviar()
        GPIO.output(self.datas, (0,0,0,1))
        self.enviar()
        sleep(0.002)
        
    def home(self):
        GPIO.output(self.rs, 0)
        GPIO.output(self.datas, (0,0,0,0))
        GPIO.output(en, 1)
        GPIO.output(en, 0)
        GPIO.output(self.datas, (0,0,1,0))
        GPIO.output(en, 1)
        GPIO.output(en, 0)
        sleep(HIGH_TIME)
    
    def textLeftRight(self):
        GPIO.output(self.rs, 0)
        GPIO.output(self.datas, (0,0,0,0))
        GPIO.output(en, 1)
        GPIO.output(en, 0)
        GPIO.output(self.datas, (0,1,1,0))
        GPIO.output(en, 1)
        GPIO.output(en, 0)
        sleep(LOW_TIME)
        
    def textRightLeft(self):
        GPIO.output(self.rs, 0)
        GPIO.output(self.datas, (0,0,0,0))
        GPIO.output(en, 1)
        GPIO.output(en, 0)
        GPIO.output(self.datas, (0,1,0,0))
        GPIO.output(en, 1)
        GPIO.output(en, 0)
        sleep(LOW_TIME)
    
    def display(self, display, cursor, blink):
        GPIO.output(self.rs, 0)
        GPIO.output(self.datas, (0,0,0,0))
        self.enviar()
        GPIO.output(self.datas, (1,display,cursor,blink))
        self.enviar()
        sleep(LOW_TIME)
        
    def moveCursor(self,direction):
        pass
    
    def writeMessage(self, message):
        for char in message:
            highPos = []
            lowPos = []
            letra = bin(ord(char))[2:].zfill(8)
            for binario in letra[:4]:
                highPos.append(int(binario))
            for binario in letra[4:]:
                lowPos.append(int(binario))
                
            GPIO.output(self.rs, 1)
            GPIO.output(self.datas, highPos)
            self.enviar()
            GPIO.output(self.datas, lowPos)
            self.enviar()
            sleep(LOW_TIME)
        

prueba = LCD(d4=26,d5=19,d6=13,d7=6,en=5,rs=0)
prueba.writeMessage("hola que tal")
GPIO.cleanup()
