import RPi.GPIO as GPIO
import time

class Sound_Noise():
    def __init__(self, pin):
        GPIO.setmode(GPIO.BCM)
        self.pin = pin
        GPIO.setup(self.pin, GPIO.IN)
        GPIO.input(self.pin)
        self.vioce = 0
        self.state = 0

    def start(self):
        GPIO.setup(self.pin, GPIO.IN)
        GPIO.input(self.pin)
        self.state = 1


    def Get_Vioce(self):
        A = AD_Change(0x48)
        vioceValue = A.read(0)
        self.vioce = vioceValue
        time.sleep(0.2)
        return self.vioce

    def close(self):
        self.state=0
        GPIO.cleanup()