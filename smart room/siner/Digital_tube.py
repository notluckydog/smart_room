import sys
import time
import datetime
import RPi.GPIO as GPIO
import tm1637


#CLK -> GPIO23 (Pin 16)
#Di0 -> GPIO24 (Pin 18)

class Digital():
   def __init__(self,pin1,pin2):
      self.pin1 = pin1
      self.pin2 = pin2
      self.status = 0   #传感器状态图标，为0时表示不在线

   def start(self):
      Display = tm1637.TM1637(self.pin1,self.pin2,tm1637.BRIGHT_TYPICAL)
      Display.Clear()
      Display.SetBrightnes(1)

      while (True):
         now = datetime.datetime.now()
         hour = now.hour
         minute = now.minute
         second = now.second
         currenttime = [int(hour / 10), hour % 10, int(minute / 10), minute % 10]

         Display.Show(currenttime)
         Display.ShowDoublepoint(second % 2)

         time.sleep(1)

if __name__ =='__main__':
   a = Digital(17,18)
   a.start()