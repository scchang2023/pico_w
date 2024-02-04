
# Timer 計時器

`from machine import Timer`
- 執行一次

```python
timer = Timer(period=5000, mode=Timer.ONE_SHOT, callback=lambda t:print(1))
```

- 持續執行

```python
timer = Timer(period=1000, mode=Timer.PERIODIC, callback=lambda t:print(2))
```

- 執行10次,然後停止執行

```python
def run10(t):
    global i
    if i>=10:
        timer.deinit()
        return
    print(i)
    i += 1

i=0
timer = Timer(period=1000, mode=Timer.PERIODIC, callback=lambda t:run10(t))
```
[timer.py](./timer.py)