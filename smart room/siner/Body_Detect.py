import RPi.GPIO as GPIO

import time

class Body_Detect():
    def __init__(self,pin,mode):
        self.Pin = pin
        self.mode = mode
        self.status = 0  #传感器是否在线标志，0表示不在线
        self.state = 0   #若有人，则输出高电平，默认无人
        if self.mode == 'BCM':
            GPIO.setmode(GPIO.BCM)
        else:
            GPIO.setmode(GPIO.BOARD)

    def start(self):
        GPIO.setup(self.Pin,GPIO.IN)
        self.status=1

    def get_state(self):
        if GPIO.input(self.Pin)== True:
            self.state = 1     #有人出现
            return self.state
            #return 'somebody'

        else:
            #return 'nobody'
            self.state = 0
            return self.state

    def close(self):
        self.status=0
        GPIO.cleanup()


if __name__ == '__main__':
    a=Body_Detect(pin = 20,mode='BCM')

    try:
        a.start()
    except:
        print('串口打开失败')

    while True:
        k=0

        print(a.get_state())
        time.sleep(0.5)
        k+=1
        if k>=300:
            a.close()
            break