import RPi.GPIO as GPIO
import time
import math

'''DO = 17 
GPIO.setmode(GPIO.BCM)   '''

class Fire():
	def __init__(self,pin,mode):
		self.Pin = pin
		self.mode = mode
		self.state = 0
		if self.mode == 'BCM':
			GPIO.setmode(GPIO.BCM)
		else :
			GPIO.setmode(GPIO.BOARD)

	def start(self):
		GPIO.setup(self.Pin,GPIO.IN)

	def get_state(self):
		if GPIO.input(self.Pin) == 0:
			return 'fire'

		else:
			return 'no fire'

	def close(self):
		GPIO.cleanup()

if __name__ == '__main__':
	a = Fire(pin = 21,mode = 'BCM')
	a.start()

	while True:
		k=0
		print(a.get_state())
		k+=1
		time.sleep(0.5)

		if k>=100:
			a.close()
			break