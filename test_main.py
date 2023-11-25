from machine import I2C,Pin
import utime
from dht import DHT11, InvalidChecksum
from lcd_api import LcdApi
from pico_i2c_lcd import I2cLcd

sensor = DHT11(Pin(22, Pin.OUT, Pin.PULL_DOWN))
I2C_ADDR     = 39
I2C_NUM_ROWS = 2
I2C_NUM_COLS = 16

i2c = I2C(0, sda=machine.Pin(0), scl=machine.Pin(1), freq=400000)
lcd = I2cLcd(i2c, I2C_ADDR, I2C_NUM_ROWS, I2C_NUM_COLS)

while True:
    try:
        temp = sensor.temperature
        humidity = sensor.humidity
        print(temp, humidity)
        str1 = f"temp:{temp} C"
        lcd.move_to(0,0)
        lcd.putstr(str1)
        lcd.move_to(0,1)
        str1 = f"hum:{humidity} %"
        lcd.putstr(str1)        
    except:
        print("Checksum from the sensor was invalid")
    utime.sleep(2)