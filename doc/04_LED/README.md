# build-in LED 內建LED

- 使用字串"LED"或"WL_GPIO0"

- `from machine import Pin`

- 使用REPL操控

    ```python
    led = Pin("LED", Pin.OUT)
    led.value(1)
    led.value(0)
    ```

- blink

    ```python
    from machine import Pin, Timer

    led = Pin("LED", Pin.OUT)
    tim = Timer()
    def tick(timer):
        global led
        led.toggle()

    tim.init(freq=2.5, mode=Timer.PERIODIC, callback=tick)
    ```
