import RPi.GPIO as GPIO
import time

class Active_Buzzer():
	def __init__(self,BuzzerPin,time):
		#BuzzerPin 引脚号
		#time 响铃时间
		self.BuzzerPin = BuzzerPin
		self.time_x = time
		#0表示不在线 1表示在线
		self.status = 1
		GPIO.setwarnings(False)
		GPIO.setmode(GPIO.BOARD)


	def start(self):
		GPIO.setup(self.BuzzerPin,GPIO.OUT)
		GPIO.output(self.BuzzerPin,GPIO.HIGH)
		self.status = 1
		self.loop()


	def loop(self):
		while True:
			GPIO.output(self.BuzzerPin,GPIO.LOW)
			time.sleep(self.time_x)
			GPIO.output(self.BuzzerPin,GPIO.HIGH)
			time.sleep(self.time_x)

	def get_state(self):
		return self.status

	def close(self):
		self.status=0
		GPIO.output(self.BuzzerPin,GPIO.HIGH)
		GPIO.cleanup()


if __name__ == '__main__':
	a = Active_Buzzer(29,0.5)
	GPIO.cleanup()
	a.start()
	a.close()
