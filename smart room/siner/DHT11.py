import Adafruit_DHT

class DHT11():
    def __int__(self,pin):
        self.pin=pin
        self.status = 0

    def start(self):
        self.sensor = Adafruit_DHT.DHT11
        self.status = 1

    def get_data(self):
        humidity, temperature = Adafruit_DHT.read_retry(self.sensor, self.pin)
        # Reading the DHT11 is very sensitive to timings and occasionally
        # the Pi might fail to get a valid reading. So check if readings are valid.
        if humidity is not None and temperature is not None:
            humidity_text = 'Humidity:{0:0.1f}*C'.format(humidity)
            temperature_text = 'Temp:{0:0.1f}*C'.format(temperature)

        else:
            humidity_text = '读取失败'
            temperature_text = '读取失败'

        return temperature_text,humidity_text

    def get_status(self):
        return self.status

    def close(self):
        GPIO.cleanup()