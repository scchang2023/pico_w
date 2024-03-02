from machine import I2C,Pin
import utime
import network
import sys
sys.path.append("/lib")
from blynklib import Blynk
from dht import DHT11
from lcd_api import LcdApi
from pico_i2c_lcd import I2cLcd

def connect_to_internet(ssid, password):
    # Pass in string arguments for ssid and password
    # Just making our internet connection
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    # Wait for connect or fail
    max_wait = 10
    while max_wait > 0:
        print(wlan.status(), max_wait)
        if wlan.status() < 0 or wlan.status() >= 3:
            break
        max_wait -= 1
        print('waiting for connection...')
        utime.sleep(1)
    # Handle connection error
    if wlan.status() != 3:
        print(wlan.status())
        # raise RuntimeError('network connection failed')
        print('network connection failed')
    else:
        print('connected')
        print(wlan.status())
        status = wlan.ifconfig()
    return wlan.status()

# ssid = "linkou_203_1F"
# ssid = "linkou203-4F"
ssid = "scchang_iphone"
# password = "56665666"
password = "0928136004"
blynk_token = "BBITOQPAWXszFKZzMp6YKlQ-88vRqAl0"

sensor = DHT11(Pin(22, Pin.OUT, Pin.PULL_DOWN))

I2C_ADDR     = 39
I2C_NUM_ROWS = 2
I2C_NUM_COLS = 16
i2c = I2C(0, sda=machine.Pin(0), scl=machine.Pin(1), freq=400000)
lcd = I2cLcd(i2c, I2C_ADDR, I2C_NUM_ROWS, I2C_NUM_COLS)

led=machine.Pin(15, machine.Pin.OUT)
build_in_led=machine.Pin("LED", machine.Pin.OUT)
led.off()
build_in_led.off()

wlan_status = connect_to_internet(ssid, password)
if wlan_status == 3:
    BLYNK = Blynk(blynk_token)
    build_in_led.on()
    # Register virtual pin handler
    @BLYNK.on("V2") #virtual pin V0
    def v0_write_handler(value): #read the value
        if int(value[0]) == 1:
            led.value(1) #turn the led on        
        else:
            led.value(0) #turn the led off
else:
    build_in_led.off()

while True:
    try:
        sensor.measure()
        temp = sensor.temperature()
        humidity = sensor.humidity()
        print(temp, humidity)
        str1 = f"temp:{temp} *C"
        lcd.move_to(0,0)
        lcd.putstr(str1)
        lcd.move_to(0,1)
        str1 = f"hum:{humidity} %"
        lcd.putstr(str1)
        if wlan_status == 3:
            BLYNK.virtual_write(0, temp)
            BLYNK.virtual_write(1, humidity)
            BLYNK.run()
    except:
        print("Checksum from the sensor was invalid")
    utime.sleep(1)