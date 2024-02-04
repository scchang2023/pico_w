from machine import ADC,Timer
import time
# Typically, Vbe = 0.706V at 27 degrees C, with a slope of -1.721mV (0.001721) per degree.

def alert():
    print('要爆炸了!')
    
def callback1(t:Timer):
    global start
    sensor = ADC(4)    
    vol = sensor.read_u16() * (3.3/65535)
    temperature = 27 - (vol-0.706) / 0.001721
    print(f'溫度:{temperature}')    
    delta = time.ticks_diff(time.ticks_ms(), start)
    print(delta)
    #溫度超過24度,並且發送alert()的時間已經大於60秒
    if temperature >= 24 and delta >= 60 * 1000:        
        alert()
        start = time.ticks_ms()#重新設定計時的時間
        

start = time.ticks_ms() - 60 * 1000 #應用程式啟動時,計時時間,先減60秒
    
time1 = Timer()
time1.init(period=1000,callback=callback1)
