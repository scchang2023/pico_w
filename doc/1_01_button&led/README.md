# Button & LED

- button 使用 GPIO14， led 使用 GPIO15 來做測試，線路圖如下：
  ![線路圖](./button_led.png)

- 此測試程式，每按一次按鈕，LED則會反向一次

  ```python
  from machine import Pin
  import time

  led = Pin(15, Pin.OUT)
  button = Pin(14, Pin.IN, Pin.PULL_DOWN)

  while True:
      if button.value():
        led.toggle()
        time.sleep(0.5)

  ```
