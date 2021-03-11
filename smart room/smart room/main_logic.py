from apscheduler.schedulers.blocking import BlockingScheduler

import time
from .siner.Active_Buzzer import Active_Buzzer
from .siner.Body_Detect import Body_Detect
from .siner.Temperature import Temperature
from .siner.CO2_Detect import CO2_Detect
from .siner.sound_noise import Sound_Noise
from .siner.screen import Screen
from .siner.Gas_Detect import Gas_Detect
from .siner.RGB_LED import RGB_LED
from .siner.Fire_detect import Fire

from uilt.weather import weatherforlifestyle



def start_siner():
    #初始化各个传感器
    active_buzzer=Active_Buzzer(11,0.5)
    body_detect = Body_Detect(12,1)
    body_detect.start()
    temperature_dectct = Temperature(13,1)
    temperature_dectct.start()
    co2_detect = CO2_Detect(14,1)
    co2_detect.start()
    sound_detect = Sound_Noise(15,1)
    sound_detect.start()
    screen_led = Screen(16,1)
    gas_detect = Gas_Detect(17,1)
    gas_detect.start()
    rgb_led = RGB_LED(18,1)
    rgb_led.start()
    fire_detect = Fire(19,1)
    fire_detect.start()





def get_siner_status():
    #获取传感器状态
    pass

def get_siner_data():
    #获取传感器数据
    temperature_data = Temperature.get_temperature()
    body_data = Body_Detect.get_data()
    sound_data = Sound_Noise.get_data()
    fire_data = Fire.get_data()
    gas_data = Gas_Detect.get_data()
    CO2_data = CO2_Detect.get_data()
    humdity = Temperature.get_humidy()

    return temperature_data,body_data,sound_data,fire_data,gas_data,CO2_data,humdity


def get_warn():
    #用来判断环境数据是否超标
    temperature_data, body_data, sound_data, fire_data, gas_data, CO2_data, humdity =get_siner_data()
    if temperature_data >= 30:
        print('hot')

    if sound_data >= 20:
        print('noise')

    if fire_data >= 20:
        print('fire')

    if humdity >= 20:
        print('humdity')

    if gas_data >= 20:
        print('gas')

    if CO2_data >=20:
        print('Co2')

def screen_display():
    #用来刷新屏幕状态
    pass

def play_weather():
    #获取天气信息，并进行语音播报
    icon ,text,tem = weatherforlifestyle()


    pass

def voice_detect():
    #用来检测语音输入
    #唤醒词：你好贾维斯
    #根据不同语音指令完成不同的内容
    #天气怎么样？明天天气怎么样？ 播放音乐 ？ 室内指标？
    pass

def main():
    start_siner()
    get_siner_status()

    get_data = BlockingScheduler()
    get_data.add_job(get_siner_data(),'interval',seconds=10,id='get_data')

    warn = BlockingScheduler()
    warn.add_job(get_warn(),'interval',seconds = 10,id='warn')

    voice = BlockingScheduler()
    voice.add_job(voice_detect(),'interval',seconds = 5,id='voice')



