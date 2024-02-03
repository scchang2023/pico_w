import network
import time

# 檢查是否可以連線,顯示連線資訊

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect('linkou_203_1F-5G','56665666')

while not wlan.isconnected() and wlan.status() >= 0:
    print("Waiting to connect:")
    time.sleep(1)
    
print(wlan.ifconfig())
