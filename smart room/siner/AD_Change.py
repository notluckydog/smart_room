import smbus
import time

class AD_Change():
    def __init__(self,addr):
        self.bus = smbus.SMBus(1)
        self.addr = addr


    def read(self,chn):

        if chn == 0:
            self.bus.write_byte(self.addr,0x40)

        if chn == 1:
            self.bus.write_byte(self.addr, 0x41)

        if chn == 2:
            self.bus.write_byte(self.addr, 0x42)

        if chn == 3:
            self.bus.write_byte(self.addr, 0x43)

        #self.bus.read_byte(self.addr)
        return self.bus.read_byte(self.addr)

    def write(self,temp):
        val = int(temp)

        self.bus.write_byte_data(self.addr,0x40,val)




