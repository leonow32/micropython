from machine import Pin, ADC
V = ADC(Pin(33), atten=ADC.ATTN_11DB)
Vvalue = (V.read_uv() / 1000000) * 2
print("Battery Voltage = " + str(Vvalue) + " V")
