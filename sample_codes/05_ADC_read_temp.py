# from machine import ADC

# 使用GPIO連線, GPIO26
# adc = machine.ADC(26) # Connect to GP26, which is channel 0

# 使用channel連線, channel 4
# adc = machine.ADC(4) # Connect to the internal temperature sensor

# 讀取系統溫度範例
import machine
import utime

sensor_temp = machine.ADC(4)
conversion_factor = 3.3 / (65535)

while True:
    reading = sensor_temp.read_u16() * conversion_factor
    
    # The temperature sensor measures the Vbe voltage of a biased bipolar diode, connected to the fifth ADC channel
    # Typically, Vbe = 0.706V at 27 degrees C, with a slope of -1.721mV (0.001721) per degree. 
    temperature = 27 - (reading - 0.706)/0.001721
    print(temperature)
    utime.sleep(2)
