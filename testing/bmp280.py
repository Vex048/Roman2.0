import board
import time
#from bmp280 import BMP280
import adafruit_bmp280
#try:
 #from smbus2 import SMBus
#except:
 #from smbus import SMBus
i2c=board.I2C()
bmp280=adafruit_bmp280.Adafruit_BMP280_I2C(i2c,address=0x76)

#bus = SMBus(1)
#bmp280 = BMP280(i2c_dev=bus)
bmp280.sea_level_pressure = 1013.25
while True:
 temperature = bmp280.temperature
 pressure = bmp280.pressure
 print("Temp: ",temperature)
 print("Pressure: ", pressure)
 time.sleep(2)
