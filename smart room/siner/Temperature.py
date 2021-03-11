import RPi.GPIO as GPIO
import numpy as np
import time

class Temperature():
    def __init__(self,pin,mode):
        self.mode = mode
        self.pin = pin

        if self.mode == 'BCM':
            GPIO.setmode(GPIO.BCM)
        else:
            GPIO.setmode(GPIO.BOARD)

        self.temperature = 0
        self.humidy = 0
        self.state = 0  #状态标志位

        self.data_state = False

    def start(self):
        GPIO.setup(self.pin,GPIO.OUT)
        GPIO.output(self.pin,GPIO.LOW)

    def get_data(self):
        #由于物理硬件的限制，至少需要18ms以上的时间才能够提示传感器开始工作
        #保持低电平20ms
        time.sleep(0.02)
        #输出高电平
        GPIO.output(self.pin, GPIO.HIGH)
        # 发送完开始信号之后将输出模式转换为输入模式，不然信号线上的电平始终被拉高
        GPIO.oupput(self.pin,GPIO.IN)

        while GPIO.input(self.pin) == GPIO.LOW:
            continue     #传感器发出应答信号，输出80ms的低电平

        while GPIO.input(self.pin) == GPIO.HIGH:
            continue     #输出80ms的高电平通知外设设备准备接受数据

        #开始接受数据
        #该传感器每次发送40位数据，前16位位湿度相关，中间16位位温度相关，最后8位用来校验
        j = 0   #计数器,该传感器每次发送40位数据
        data = []  #受到的二进制数据
        kk = []    #存放每次高电平结束后k值的列表

        while j< 40:
            k = 0
            while GPIO.input(self.pin) == GPIO.LOW:
                #先50ms的低电平
                continue

            while GPIO.input(self.pin)==GPIO.HIGH:
                #接着是26-28ms的高电平，或者是70ms的g高电平
                k+=1
                if k>100:
                    break
            kk.append()
            if k<8:   #当26-28ms时高电平通常k=6|k=6
                data.append(0)     #在数据列表后面添加一位新的二进制数据0
            else:      ##70 微秒时高电平时通常k等于17或18
                data.append(1) ##在数据列表后面添加一位新的二进制数据“1”

            m = np.logspace(7, 0, 8, base=2, dtype=int)  # logspace()函数用于创建一个于等比数列的数组
            # 即[128 64 32 16 8 4 2 1]，8位二进制数各位的权值
            data_array = np.array(data)  # 将data列表转换为数组

            # dot()函数对于两个一维的数组，计算的是这两个数组对应下标元素的乘积和(数学上称之为内积)
            self.humidity = m.dot(data_array[0:8])  # 用前8位二进制数据计算湿度的十进制值
            humidity_point = m.dot(data_array[8:16])
            self.temperature = m.dot(data_array[16:24])
            temperature_point = m.dot(data_array[24:32])
            check = m.dot(data_array[32:40])



            tmp = self.humidity + humidity_point + self.temperature + temperature_point
            # 十进制的数据相加

            if check == tmp:  # 数据校验，相等则输出
                self.data_state = True

            else:  # 错误输出错误信息
                self.data_state = False


    def get_temperature(self):
        self.get_data()
        if self.data_state:
            return self.temperature
        else:
            return 'no'

    def get_humidy(self):
        self.get_data()
        if self.data_state:
            return self.humidy
        else:
            return 'no'

    def get_state(self):
        return self.state

    def close(self):
        GPIO.cleanup()