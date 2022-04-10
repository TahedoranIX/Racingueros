# Sample code to demonstrate Encoder class.  Prints the value every 5 seconds, and also whenever it changes.

import time
import RPi.GPIO as GPIO
from encoder import Encoder

def valueChanged(value, direction, valueButton):
    print("* New value: {}, Direction: {}, Button: {}".format(value, direction, valueButton))

GPIO.setmode(GPIO.BCM)

e1 = Encoder(16, 20, 21)
#GPIO.setup(20, GPIO.IN, pull_up_down=GPIO.PUD_UP)
#GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

try:
    while True:
        time.sleep(2)
        #print(GPIO.input(21))
        print("Value is {}".format(e1.getValue()))
except Exception:
    pass

GPIO.cleanup()