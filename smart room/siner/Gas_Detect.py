import RPi.GPIO as GPIO

class Gas_Detect():
    def _init_(self,DO, Buzz):
        GPIO.setmode(GPIO.BCM)
        self.DO = DO
        self.Buzz = Buzz
        self.Gas_Status = 'safe'
        self.state = 0

    def start(self):
        ADC.setup(0x48)

        GPIO.setup(self.DO, GPIO.IN)
        GPIO.setup(self.Buzz, GPIO.OUT)
        GPIO.output(self.Buzz, 0)
        self.state = 1

    def get_data(self):
        pass

    def get_state(self):
        return self.state

    def close(self):
        GPIO.output(self.Buzz, 0)
        GPIO.cleanup()
