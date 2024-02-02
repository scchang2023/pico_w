from machine import WDT

wdt = WDT(timeout=2000)
wdt.feed()