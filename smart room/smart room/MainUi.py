import wx
import time
from uilt.weather import weatherforlifestyle
from wx.lib.ticker import Ticker
from wx import NewId
import os

from .siner.Active_Buzzer import Active_Buzzer
from .siner.Body_Detect import Body_Detect
from .siner.Temperature import Temperature
from .siner.CO2_Detect import CO2_Detect
from .siner.sound_noise import Sound_Noise
from .siner.screen import Screen
from .siner.Gas_Detect import Gas_Detect
from .siner.RGB_LED import RGB_LED

from .siner.Fire_detect import Fire

ID_00 = NewId()
ID_01 = NewId()
ID_02 = NewId()
ID_03 = NewId()
ID_04 = NewId()
ID_05 = NewId()
ID_06 = NewId()
ID_07 = NewId()
ID_08 = NewId()
ID_09 = NewId()
ID_10 = NewId()
ID_11 = NewId()
class Room(wx.Frame):
    def __init__(self,parent):
        super().__init__(parent)
        self.setupIcon()
        self.initUi()
        self.Center()

    def setupIcon(self):
        ## 图标的实现
        path2 = os.path.abspath('..') + '\\asset'
        self.file = path2 +"/image/"+ "house "+".png"

        icon = wx.Icon(self.file, type=wx.BITMAP_TYPE_PNG)
        self.SetIcon(icon)

    def initUi(self):
        self.SetBackgroundColour('white')
        #用来展示天气信息
        weatherbox = wx.BoxSizer(wx.VERTICAL)

        canshu = weatherforlifestyle()

        icon = canshu[0]
        text = canshu[1]
        temp = canshu[2]
        path2 = os.path.abspath('..')+'\\asset\\image'
        file = path2 +"/color-64/" + str(icon) + ".png"
        print(file)

        weather_image = wx.StaticBitmap(self,
                                        wx.ID_ANY, wx.Bitmap(file, wx.BITMAP_TYPE_ANY))
        weatherbox.Add(weather_image, flag=wx.ALIGN_CENTER, border=8)

        '''weather_text = wx.StaticText(self, label=str(text))
        Box1.Add(weather_text, flag=wx.RIGHT | wx.ALIGN_CENTER, border=8)'''

        weather_temp = wx.StaticText(self, label=str(text) + '   ' + str(temp) + "℃")
        weatherbox.Add(weather_temp, flag=wx.RIGHT | wx.ALIGN_CENTER)

        t = time.localtime(time.time())
        st = time.strftime('%Y-%m-%d ', t)
        str2 = wx.StaticText(self, label=st)
        weatherbox.Add(str2)
        #用来展示警示信息
        #烟雾浓度过高、雨滴传感器下雨信息、火焰信息、声音太吵了的信息
        waringbox  = wx.BoxSizer(wx.VERTICAL)
        self.ticker = Ticker(self,size = (200,80))
        text_message = ' 岁月静好、就当无事发生'
        self.ticker.SetText(text_message)
        waringbox.Add(self.ticker,flag = wx.ALIGN_CENTER,border =10)

        #用来展示传感器在线信息
        sensorBox = wx.FlexGridSizer(10,2,5,5)
        self.bt_fire = wx.ToggleButton(self,size = (100,20),id = ID_00,label = u'火焰传感器')
        self.bt_fire.Bind(wx.EVT_BUTTON,self.Siner_Set)
        self.t_fire = wx.StaticText(self,-1,label = '离线')
        self.bt_gas = wx.ToggleButton(self,size = (100,20), id=ID_01, label=u'烟雾传感器')
        self.bt_gas.Bind(wx.EVT_BUTTON, self.Siner_Set)
        self.t_gas = wx.StaticText(self, -1, label='离线')
        self.bt_temp = wx.ToggleButton(self,size = (100,20), id=ID_02, label=u'温湿度传感器')
        self.bt_temp.Bind(wx.EVT_BUTTON, self.Siner_Set)
        self.t_temp = wx.StaticText(self, -1, label='离线')

        self.bt_rain = wx.ToggleButton(self, size = (100,20),id=ID_03, label=u'雨滴传感器')
        self.bt_rain.Bind(wx.EVT_BUTTON, self.Siner_Set)
        self.t_rain = wx.StaticText(self, -1, label='离线')

        self.bt_dusty = wx.ToggleButton(self,size = (100,20), id=ID_04, label=u'土壤湿度传感器')
        self.bt_dusty.Bind(wx.EVT_BUTTON, self.Siner_Set)
        self.t_dusty = wx.StaticText(self, -1, label='离线')

        self.bt_sound = wx.ToggleButton(self,size = (100,20), id=ID_05, label=u'声音传感器')
        self.bt_sound.Bind(wx.EVT_BUTTON, self.Siner_Set)
        self.t_sound = wx.StaticText(self, -1, label='离线')
        self.bt_LED = wx.ToggleButton(self, size = (100,20),id=ID_06, label=u'LED灯')
        self.bt_LED.Bind(wx.EVT_BUTTON, self.Siner_Set)
        self.t_LED = wx.StaticText(self, -1, label='离线')
        self.bt_buzzer = wx.ToggleButton(self, size = (100,20),id=ID_07, label=u'蜂鸣器')
        self.bt_buzzer.Bind(wx.EVT_BUTTON, self.Siner_Set)
        self.t_buzzer = wx.StaticText(self, -1, label='离线')
        self.bt_resetwarn = wx.ToggleButton(self, size = (100,20),id=ID_08, label=u'警报复位按钮')
        self.bt_resetwarn.Bind(wx.EVT_BUTTON, self.Siner_Set)
        self.t_resetwarn = wx.StaticText(self, -1, label='离线')
        self.bt_screen = wx.ToggleButton(self,size = (100,20),id = ID_09,label = u'屏幕')
        self.bt_screen.Bind(wx.EVT_BUTTON, self.Siner_Set)
        self.t_screen = wx.StaticText(self, -1, label='离线')
        self.bt_motor = wx.ToggleButton(self, size = (100,20),id=ID_10, label=u'马达')
        self.bt_motor.Bind(wx.EVT_BUTTON, self.Siner_Set)
        self.t_motor = wx.StaticText(self, -1, label='离线')
        self.bt_CO2 = wx.ToggleButton(self,size = (100,20),id = ID_11,label = 'CO2传感器')
        self.bt_CO2.Bind(wx.EVT_BUTTON, self.Siner_Set)
        self.t_CO2 = wx.StaticText(self,-1,label = '离线')

        sensorBox.AddMany([(self.bt_fire),(self.t_fire,-1,wx.EXPAND),(self.bt_gas),(self.t_gas,-1,wx.EXPAND),
                          (self.bt_temp),(self.t_temp,-1,wx.EXPAND),(self.bt_sound),(self.t_sound,-1,wx.EXPAND),
                          (self.bt_LED),(self.t_LED,-1,wx.EXPAND),(self.bt_buzzer),(self.t_buzzer,-1,wx.EXPAND),
                          (self.bt_resetwarn),(self.t_resetwarn,-1,wx.EXPAND),(self.bt_screen),(self.t_screen,-1,wx.EXPAND),
                          (self.bt_motor),(self.t_motor,-1,wx.EXPAND),(self.bt_CO2),(self.t_CO2,-1,wx.EXPAND)])
        #(self.bt_rain),(self.t_rain,-1,wx.EXPAND),(self.bt_dusty),(self.t_dusty,-1,wx.EXPAND)
        #用来展示温湿度等相关信息
        #温度，湿度，二氧化碳浓度,

        self.t_mes_humidty = wx.StaticText(self,-1,label = u'湿度')
        self.t_mes_humidty1 = wx.StaticText(self,-1,label = u'0%')
        font = wx.Font(14,wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        font1 = wx.Font(24, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        self.t_mes_humidty.SetFont(font)
        self.t_mes_humidty1.SetFont(font1)

        self.t_mes_tem = wx.StaticText(self,-1,label = u'温度')
        self.t_mes_tem1 = wx.StaticText(self,-1,label = u'0°')
        self.t_mes_tem.SetFont(font)
        self.t_mes_tem1.SetFont(font1)

        self.t_mes_CO2 = wx.StaticText(self,-1,label = u'CO2浓度')
        self.t_mes_CO21 = wx.StaticText(self,-1,label = u'0')
        self.t_mes_CO2.SetFont(font)
        self.t_mes_CO21.SetFont(font1)

        showbox= wx.FlexGridSizer(3,2,5,5)
        showbox.AddMany([(self.t_mes_humidty),(self.t_mes_humidty1,-1,wx.EXPAND),
                        (self.t_mes_tem),(self.t_mes_tem1,-1,wx.EXPAND),
                        (self.t_mes_CO2),(self.t_mes_CO21,-1,wx.EXPAND)])

        box1 = wx.BoxSizer(wx.HORIZONTAL)
        box1.AddSpacer(50)
        box1.Add(weatherbox)
        box1.AddSpacer(50)
        box1.Add(waringbox)

        box2=wx.BoxSizer(wx.HORIZONTAL)
        box2.Add(showbox,flag = wx.LEFT|wx.RIGHT,border = 50)
        box2.Add(sensorBox)

        box = wx.BoxSizer(wx.VERTICAL)
        box.Add(box1,flag = wx.TOP|wx.BOTTOM,border = 20)
        box.Add(box2)

        '''box = wx.GridSizer(2,2,5,5)
        box.Add(weatherbox,pos = (0,0),flag = wx.ALL,border = 10)
        box.Add(waringbox, pos=(0, 1), flag=wx.ALL, border=10)
        box.Add(showbox, pos=(1, 0), flag=wx.ALL, border=10)
        box.Add(sensorBox, pos=(1, 1), flag=wx.ALL, border=10)'''

        self.SetSizer(box)

    def Siner_Set(self,e):
        if e.GetId()== ID_01:
            self.bt_fire.SetToggle(True)
            fire = Fire.close()
        pass


def main():
    app = wx.App()
    main_frame = Room(None)
    main_frame.Show()
    app.MainLoop()


if __name__ == '__main__':
    main()
