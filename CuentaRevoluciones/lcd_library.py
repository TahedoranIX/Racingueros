import RPi.GPIO as GPIO
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
class LCD:
    def __init__(self, d4, d5, d6, d7, en, rs):
        #DEFINICIÓN DE PINES
        GPIO.setmode(GPIO.BCM)
        self.datas = [d4,d5,d6,d7]
        GPIO.setup(d4, GPIO.OUT)
        GPIO.setup(d5, GPIO.OUT)
        GPIO.setup(d6, GPIO.OUT)
        GPIO.setup(d7, GPIO.OUT)
        GPIO.setup(en, GPIO.OUT)
        GPIO.setup(rs, GPIO.OUT)
        print("entradas definidas")
        #init LCD
        GPIO.output(rs, False)
        GPIO.output(self.datas, (0,0,0,0))
        func = GPIO.output(d4, not GPIO.input(d4))
        print("init")




    def sendMessage(self):
        pass

prueba = LCD(26,19,13,6,5,0)
