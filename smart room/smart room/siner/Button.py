import RPi.GPIO as GPIO
import time

class Button():
	def __init__(self,KeyPin):
		self.KeyPin = KeyPin
		self.KeyState = 0


		GPIO.setwarnings(False)
		GPIO.setmode(GPIO.BOARD)

	def start(self):

		GPIO.setup(self.KeyPin,GPIO.IN)
		while True:
			if GPIO.input(self.KeyPin)==1:#松开时为高电平
				time.sleep(0.02)    #绕过抖动区间

				if GPIO.input(self.KeyPin)==1:
					while(GPIO.input(self.KeyPin)==1):
                        #等待松手
                        self.KeyState = 1


                    #print('key precess')
					if self.KeyState==0:
						self.KeyState = 0
					else:
						self.KeyState=0

	def get_state(self):
		return self.KeyState

def main():
	a = X_Button(15)
	print(a.get_state())

	a.start()
	print(a.get_state())


if __name__ =='__main_':
	main()