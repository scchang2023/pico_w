import machine # 導入Pi Pico硬體參數設定類別
import utime   # 導入時間相關類別
led_onboard = machine.Pin(25, machine.Pin.OUT) #設定GP25為輸出腳
while True: # 若真則循環
    led_onboard.value(1) # 點亮LED
    utime.sleep(0.5)     # 延時0.5秒
    led_onboard.value(0) # 熄滅LED
    utime.sleep(0.5)     # 延時0.5秒