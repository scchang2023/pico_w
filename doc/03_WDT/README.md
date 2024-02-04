# WTD(Watch Dog Timer) 重新啟動

```python
from machine import WDT

wdt = WDT(timeout=2000)
wdt.feed()
```
