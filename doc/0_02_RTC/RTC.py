from machine import RTC

# 取得目前日期時間
rtc = RTC()
# print(rtc.datetime()) # # (2024, 2, 2, 4, 17, 19, 17, 0)

# 設定日期時間
rtc.datetime((2017,8,23,2,12,48,0,0))
print(rtc.datetime()) # (2017, 8, 23, 2, 12, 48, 1, 0)
