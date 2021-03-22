# smart_room
raspberry pi4  python sensor snowboy 利用树莓派实现简单的智能家居

项目功能：
1.利用传感器收集温湿度、二氧化碳浓度信息并写入sqlite3
2.从数据库读取相关传感器信息并显示在0.96寸OLED屏幕上
3.提供语音播报与识别功能，实现查询天气、环境数据语音播报
4.环境温度异常时语音播报


项目所用材料：
raspberry pi4 一台，DHT11温湿度传感器，ccs811二氧化碳传感器、0.96寸OLED显示屏，usb免驱动声卡，jetson Nano扬声器一个，面包板一块


技术路径：
1.python作为主要开发语言
2.GPIO、sumbus库
3.语音唤醒使用snowboy
4.语音识别与语音合成采用百度API
5.一系列adafruit库


