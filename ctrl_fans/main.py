from machine import I2C, Pin, ADC
import utime
import sys
sys.path.append("/lib")
from dht import DHT11
from lcd_api import LcdApi
from pico_i2c_lcd import I2cLcd

TEMP_SETTING_DEFAULT = 25
    
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

def lcd_display_cur_ts(lcd, ts):
    str1 = f"TS:{ts}"
    lcd.move_to(0,1)
    lcd.putstr(str1)

def build_in_led_init():
    # led=machine.Pin(15, machine.Pin.OUT)
    build_in_led=machine.Pin("LED", machine.Pin.OUT)
    # led.off()
    build_in_led.off()
    return build_in_led

def fans_init():
    fans=machine.Pin(15, machine.Pin.OUT)
    fans.off()
    return fans

def fans_auto_turn_on(fans, cur_temp, cur_ts):
    if cur_temp >= cur_ts:
        fans.on()
    else:
        fans.off()

def temp_setting_pin_init():
    pot = ADC(Pin(26))
    return pot

def temp_setting_pin_read(pot):
    value = pot.read_u16()  # 回傳值範圍為 0 ~ 65535（16位）
    voltage = 3.3 * value / 65535  # 轉換為電壓值
    print("ADC值:", value, "電壓: {:.2f}V".format(voltage))    

def main():
    sensor = dht11_init()
    lcd = lcd_init()
    build_in_led = build_in_led_init()
    fans = fans_init()
    pot =  temp_setting_pin_init()
    build_in_led.off()
    utime.sleep(1)
    while True:
        try:
            cur_temp, cur_humi = dht11_get_temp_humi(sensor)
            print(f"CT:{cur_temp}, CH:{cur_humi}, TS:{TEMP_SETTING_DEFAULT}")
            lcd_display_cur_temp_humi(lcd, cur_temp, cur_humi)
            lcd_display_cur_ts(lcd, TEMP_SETTING_DEFAULT)
            temp_setting_pin_read(pot)
            fans_auto_turn_on(fans, cur_temp, TEMP_SETTING_DEFAULT)
        except:
            print("The checksum of dht11 was invalid")
        utime.sleep(1)

if __name__ == "__main__":
    main()