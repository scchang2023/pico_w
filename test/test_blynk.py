from machine import Pin, I2C
import network
import time
import sys
sys.path.append('/lib')
from blynklib import Blynk

# ssid = "linkou_203_1F"
ssid = "linkou203-4F"
password = "56665666"
blynk_token = "BBITOQPAWXszFKZzMp6YKlQ-88vRqAl0"

i2c=I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)

def connect_to_internet(ssid, password):
    # Pass in string arguments for ssid and password

    # Just making our internet connection
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)

    # Wait for connect or fail
    max_wait = 10
    while max_wait > 0:
        if wlan.status() < 0 or wlan.status() >= 3:
            break
        max_wait -= 1
        print('waiting for connection...')
        time.sleep(1)
    # Handle connection error
    if wlan.status() != 3:
        print(wlan.status())
        raise RuntimeError('network connection failed')
    else:
        print('connected')
        print(wlan.status())
        status = wlan.ifconfig()

connect_to_internet(ssid, password)
BLYNK = Blynk(blynk_token)

while True:
    # bme = bme280.BME280(i2c=i2c)
    # temperature, pressure, humidity = bme.read_compensated_data()
    # Print sensor data to console
    # print('Temperature: {:.1f} C'.format(temperature/100))
    # print('Humidity: {:.1f} %'.format(humidity/1024))
    # print('Pressure: {:.1f} hPa'.format(pressure/25600))
    BLYNK.virtual_write(0, 25)
    BLYNK.virtual_write(1, 65)
    BLYNK.run()
    time.sleep(1)