import math
import time

import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306

from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from uilt.weather import weatherforlifestyle

class Screen():
    def __int__(self):
        # Raspberry Pi pin configuration:
        self.RST = None
        # Note the following are only used with SPI:
        self.DC = 23
        self.SPI_PORT = 0
        self.SPI_DEVICE = 0
        #显示天气信息  天气图标、天气文字、温度
        #初始化时获取一次
        self.icon, self.text, self.tem = weatherforlifestyle()
        self.status = 0

    def start(self,temptrue_text,humity_text,CO2_text):
        # 128x64 display with hardware I2C:
        disp = Adafruit_SSD1306.SSD1306_128_64(rst=self.RST)
        # Initialize library.
        disp.begin()
        self.status =1

        # Get display width and height.
        width = disp.width
        height = disp.height

        # Clear display.
        disp.clear()
        disp.display()


        #显示室内温湿度，二氧化碳浓度
        humity = humity_text
        temptrue = temptrue_text

        image1 = Image.new('1',(128,64))
        draw1 = ImageDraw.Draw(image1)
        font1 = ImageFont.load_default()
        #font2 = ImageFont.truetype('04B_30__.TTF',15)
        draw1.text((0,0),temptrue_text,font =font1,fill =1)
        draw1.text((0,15),humity_text,font = font1,fill = 1)
        draw1.text((0,30),CO2_text,font = font1)
        draw1.text((0,30),'天气状况'+self.text,font = font1,fill =1)
        draw1.text((0,45),'温度'+self.tem,font = font1,fill =1)


    def close(self):
        GPIO.cleanup()



