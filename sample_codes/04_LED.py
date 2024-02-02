from machine import Pin, Timer

# 使用REPL操控
# led = Pin("LED", Pin.OUT)
# led.value(1)
# led.value(0)

# blink
led = Pin("LED", Pin.OUT)
tim = Timer()
def tick(timer):
    global led
    led.toggle()

tim.init(freq=2.5, mode=Timer.PERIODIC, callback=tick)