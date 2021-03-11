import RPi.GPIO as GPIO
import time

class RGB_LED():
    def __init__(self,R,G,B,Color):

        self.R_pin = R
        self.G_pin = G
        self.B_pin = B
        self.status = 0  #设备默认不在线
        self.Color = Color
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)

    def start(self):

        GPIO.setup(self.R_pin,GPIO.OUT)      #设置引脚模式为输出
        GPIO.output(self.R_pin,GPIO.HIGH)

        GPIO.setup(self.G_pin, GPIO.OUT)  # 设置引脚模式为输出
        GPIO.output(self.G_pin, GPIO.HIGH)

        GPIO.setup(self.B_pin, GPIO.OUT)  # 设置引脚模式为输出
        GPIO.output(self.B_pin, GPIO.HIGH)

        self.p_R = GPIO.PWM(self.R_pin,2000)
        self.p_G = GPIO.PWM(self.G_pin, 1999)
        self.p_B = GPIO.PWM(self.B_pin, 5000)

        self.status=1

        self.p_R.start(100)
        self.p_G.start(100)
        self.p_B.start(100)

        self.loop()

    def setColor(self):
        pass


    def close(self):
        self.p_R.stop()
        self.p_B.stop()
        self.p_G.stop()

        #关闭所有灯
        GPIO.output(self.R_pin, GPIO.HIGH)
        GPIO.output(self.G_pin, GPIO.HIGH)
        GPIO.output(self.B_pin, GPIO.HIGH)

        self.status = 0

        GPIO.cleanup()

    def map(self,x, in_min, in_max, out_min, out_max):
        return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


    def loop(self):
        while True:
            for col in self.Color:
                R_val = (col & 0xff0000) >> 16
                G_val = (col & 0x00ff00) >> 8
                B_val = (col & 0x0000ff) >> 0

                R_val = self.map(R_val, 0, 255, 0, 100)
                G_val = self.map(G_val, 0, 255, 0, 100)
                B_val = self.map(B_val, 0, 255, 0, 100)

                self.p_R.ChangeDutyCycle(100 - R_val)  # Change duty cycle
                self.p_G.ChangeDutyCycle(100 - G_val)
                self.p_B.ChangeDutyCycle(100 - B_val)

                time.sleep(1)


def main():
    colors = [0xFF0000, 0x00FF00, 0x0000FF, 0xFFFF00, 0xFF00FF, 0x00FFFF]
    R = 11
    G = 12
    B =13
    a=RGB_LED(R,G,B,colors)
    GPIO.cleanup()
    a.start()