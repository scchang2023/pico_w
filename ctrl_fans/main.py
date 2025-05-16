from machine import I2C,Pin
import utime
import network
import sys
sys.path.append("/lib")
from blynklib import Blynk
from dht import DHT11
from lcd_api import LcdApi
from pico_i2c_lcd import I2cLcd

# ssid = "linkou_203_1F"
# ssid = "linkou203-4F"
ssid = "scchang_iphone"
# password = "56665666"
password = "0928136004"
blynk_token = "BBITOQPAWXszFKZzMp6YKlQ-88vRqAl0"
temp_setting = 30

def wifi_connect(ssid, password):
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
        print('wait for connecting.')
        utime.sleep(1)
    print(wlan.status())
    if wlan.status() != 3:
        # raise RuntimeError('network connection failed')
        print('failed to connect wifi.')
    else:
        print('connected')
        status = wlan.ifconfig()
    
    return wlan.status()
    
def dht11_init():
    sensor = DHT11(Pin(22, Pin.OUT, Pin.PULL_DOWN))
    return sensor

def dht11_get_temp_humi(sensor):
    sensor.measure()
    temp = sensor.temperature()
    humi = sensor.humidity()
    return temp, humi

def lcd_init():
    I2C_ADDR     = 39
    I2C_NUM_ROWS = 2
    I2C_NUM_COLS = 16
    i2c = I2C(0, sda=machine.Pin(0), scl=machine.Pin(1), freq=400000)
    lcd = I2cLcd(i2c, I2C_ADDR, I2C_NUM_ROWS, I2C_NUM_COLS)
    return lcd

def lcd_display_cur_temp_humi(lcd, temp, humi):
    str1 = f"CT:{temp}"
    lcd.move_to(0,0)
    lcd.putstr(str1)
    lcd.move_to(8,0)
    str1 = f"CH:{humi}"
    lcd.putstr(str1)

def lcd_display_temp_setting(lcd, temp_setting):
    str1 = f"TS:{temp_setting}"
    lcd.move_to(0,1)
    lcd.putstr(str1)

def build_led_init():
    # led=machine.Pin(15, machine.Pin.OUT)
    build_in_led=machine.Pin("LED", machine.Pin.OUT)
    # led.off()
    build_in_led.off()
    return build_in_led

def fans_init():
    fans=machine.Pin(15, machine.Pin.OUT)
    fans.off()
    return fans

def auto_turnon_fans(fans, cur_temp, temp_setting):
    if cur_temp >= temp_setting:
        fans.on()
    else:
        fans.off()

def main():
    sensor = dht11_init()
    lcd = lcd_init()
    build_in_led = build_led_init()
    fans = fans_init()
    # wlan_status = wifi_connect(ssid, password)
    wlan_status = 0

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

    utime.sleep(1)
    while True:
        try:
            cur_temp, cur_humi = dht11_get_temp_humi(sensor)
            print(f"CT:{cur_temp}, CH:{cur_humi}, TS:{temp_setting}")
            lcd_display_cur_temp_humi(lcd, cur_temp, cur_humi)
            lcd_display_temp_setting(lcd, temp_setting)
            auto_turnon_fans(fans, cur_temp, temp_setting)
            if wlan_status == 3:
                BLYNK.virtual_write(0, temp)
                BLYNK.virtual_write(1, humi)
                BLYNK.run()
        except:
            print("The checksum of dht11 was invalid")
        utime.sleep(1)

if __name__ == "__main__":
    main()