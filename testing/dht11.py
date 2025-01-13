import time
import adafruit_dht
import board
print("JD")
dht_device=adafruit_dht.DHT11(board.D4, use_pulseio=False)
while True:
	 temperature_c = dht_device.temperature
	 temperature_f = temperature_c *(9/5)+32
	 humidity=dht_device.humidity
	 print(temperature_c,humidity)
