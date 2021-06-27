# smart_room
raspberry pi4  python sensor 

功能：
1. 利用传感器收集环境中CO2，TVOC，温度、湿度的信息，保存至数据库中
2. 获取天气信息，与环境信息一起显示在oled屏幕上
3. 数码管显示当前时间
4. 早上自动播放音乐作为闹钟
5. 早上播放当天的天气等相关信息

所用材料：
1. 树莓派4B 4G
2.tm1637的数码管
3.SSD1306的0.96寸OLED
4.ccs811的二氧化碳传感器
5.DHT11的温湿度传感器
6. jetson Nano USB转音频模块

实现过程：
1. 部分传感器库来自于Adafruit
2. 天气信息来自于和风天气
3. 语音合成使用百度语音
4. 数据库使用sqlite3
5. 定时功能采用Apscheduler库实现
6.语音播放使用的是pygame
 
 整体截图如下：
 ![输入图片描述](README_md_files%5C6882fa11974b60e3199d01ccec9a139.jpg?v=1&type=image)
![输入图片描述](README_md_files%5Cbab3a1c0d996257bc49144228fa8c35.jpg?v=1&type=image)

![输入图片描述](README_md_files%5C75c94d4dcc36f3b837ed9a5709fe0ad.jpg?v=1&type=image)

![输入图片描述](README_md_files%5Ca016d95e33fe78ef255b3ef7fae2c32.jpg?v=1&type=image)


