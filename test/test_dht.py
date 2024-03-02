from machine import Pin
import utime
from dht import DHT11

sensor = DHT11(Pin(22, Pin.OUT, Pin.PULL_DOWN))

while True:
    sensor.measure()
    temp = sensor.temperature()
    humidity = sensor.humidity()
    print(temp, humidity)
    utime.sleep(2)
