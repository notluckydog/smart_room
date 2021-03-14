#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#



import math
import time

import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306
import RPi.GPIO as GPIO

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
        '''weather_mes = weatherforlifestyle()
        self.icon=weather_mes[0]
        self.text1 = weather_mes[1]
        self.tem1 = weather_mes[2]
        self.icon, self.text1, self.tem1 = weatherforlifestyle()'''
        self.status = 0

    def start(self,temptrue_text,humity_text,CO2_text,weather1,weather_tem1):
        # 128x64 display with hardware I2C:
        disp = Adafruit_SSD1306.SSD1306_128_64(rst=None)
        # Initialize library.
        disp.begin()
        self.status =1

        # Get display width and height.
        width = disp.width
        height = disp.height

        # Clear display.
        disp.clear()
        disp.display()
        #print('1')
        #显示室内温湿度，二氧化碳浓度
        humity = humity_text
        temptrue = temptrue_text
        CO2 = CO2_text
        '''print('humity'+str(type(humity)))
        print('temptrue'+str(type(temptrue)))
        print('CO2'+str(type(CO2)))'''
        #print(self.text1,self.tem1)
        padding = 2
        shape_width = 20
        top = padding
        bottom = height - padding
        x = padding
        '''weather_mes = weatherforlifestyle()
        self.icon = weather_mes[0]
        self.text1 = weather_mes[1]
        self.tem1 = weather_mes[2]
        print(weather_mes)'''
        #print(type(self.tem1),type(self.text1))
        # self.icon, self.text1, self.tem1 = weatherforlifestyle()

        image1 = Image.new('1',(128,64))
        draw1 = ImageDraw.Draw(image1)
        font1 = ImageFont.load_default()
        #font2 = ImageFont.truetype('04B_30__.TTF',15)
        draw1.text((x,top),'temptrue: '+temptrue+'C',font =font1,fill =255)
        draw1.text((x,top+8),'humity: '+humity+'%',font = font1,fill = 255)
        draw1.text((x,top+16),'CO2:'+CO2+'ppm',font = font1,fill = 255)
        draw1.text((x,top+25),'weather: '+weather1,font = font1,fill =255)
        draw1.text((x,top+35),'outside_temptrue: '+weather_tem1+'C',font = font1,fill =255)
        disp.image(image1)
        disp.display()
        #print('2')


    def get_status(self):
        return self.status
    def close(self):
        GPIO.cleanup()



if __name__=='__main__':
    a = Screen()
    '''weather_mes = weatherforlifestyle()
    icon = weather_mes[0]
    text1 = weather_mes[1]
    tem1 = weather_mes[2]'''
    a.start('25','30','100','lcear','22')
    print(a.get_status())