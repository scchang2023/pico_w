# RTC(Real Time Clock) 實時時鐘

`from machine import RTC`

- 取得目前日期時間：

```python
rtc = RTC()
print(rtc.datetime())
# (2024, 2, 2, 4, 17, 19, 17, 0)
```

- 設定日期時間：
  - RTC的時間是取得電腦的時間(當電腦連線時是正常的現在日期和時間)
  - 當單獨運作時(無連接電腦,所以要透過RTC sensor,或wifi取得目前的時間)

```python
rtc.datetime((2017,8,23,2,12,48,0,0))
print(rtc.datetime())
# (2017, 8, 23, 2, 12, 48, 1, 0)
```

[RTC.py](./RTC.py)