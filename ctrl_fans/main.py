from machine import I2C, Pin, ADC
import time
import sys
sys.path.append("/lib")
from dht import DHT11
from lcd_api import LcdApi
from pico_i2c_lcd import I2cLcd

TEMP_SETTING_MIN = 10
TEMP_SETTING_MAX = 50
TEMP_SETTING_HYSTERESIS = 2
TEMP_SETTING_MODE_OFF = 0
TEMP_SETTING_MODE_ON = 1
TEMP_SETTING_MODE_AUTO = 2
    
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

def lcd_display_cur_mode(lcd, mode):
    if mode == 0:
        str1 = "OFF "
    elif mode == 1:
        str1 = "ON  "
    else:
        str1 = "AUTO"
    lcd.move_to(8,1)
    lcd.putstr(str1)

def build_in_led_init():
    build_in_led=machine.Pin("LED", machine.Pin.OUT)
    build_in_led.off()
    return build_in_led

def fans_init():
    fans=machine.Pin(15, machine.Pin.OUT)
    fans.off()
    return fans

def fans_auto_turn_on(fans, temp, ts, mode):
    if mode == TEMP_SETTING_MODE_OFF:
        fans.off()
    elif mode == TEMP_SETTING_MODE_ON:
        fans.on()
    else:
        if fans.value() == 0:
            if temp >= ts:
                fans.on()
        else:
            if temp < ts-TEMP_SETTING_HYSTERESIS:
                fans.off()

def temp_setting_pin_init():
    pot = ADC(Pin(26))
    return pot

def temp_setting_read(pot):
    value = pot.read_u16()
    ts = TEMP_SETTING_MIN + int((TEMP_SETTING_MAX-TEMP_SETTING_MIN) * value / 65535)
    if ts <= TEMP_SETTING_MIN:
        mode = 0
    elif ts >= TEMP_SETTING_MAX:
        mode = 1
    else:
        mode = 2 
    print("ADC:", value, "ts:", ts, "mode:", mode)
    return ts, mode

def main():
    sensor = dht11_init()
    lcd = lcd_init()
    build_in_led = build_in_led_init()
    fans = fans_init()
    pot =  temp_setting_pin_init()
    build_in_led.off()
    time.sleep(1)
    while True:
        try:
            cur_temp, cur_humi = dht11_get_temp_humi(sensor)
            lcd_display_cur_temp_humi(lcd, cur_temp, cur_humi)
            cur_ts, cur_mode = temp_setting_read(pot)
            lcd_display_cur_ts(lcd, cur_ts)
            lcd_display_cur_mode(lcd, cur_mode)
            print(f"CT:{cur_temp}, CH:{cur_humi}, TS:{cur_ts}")
            fans_auto_turn_on(fans, cur_temp, cur_ts, cur_mode)
        except:
            print("Exception!!!")
        time.sleep(0.2)

if __name__ == "__main__":
    main()