from machine import Pin, ADC, UART
from time import sleep_ms

uart = UART(0, baudrate=9600, tx=Pin(0), rx=Pin(1))
adc = ADC(2)
conversion_factor = 3.3 / 65535
DE_RE = Pin(2, Pin.OUT)

DE_RE.value(1)
while True:
    reading = adc.read_u16() * conversion_factor
    data = "{:.2f}".format(reading) + ' V\n'
    print(data)
    uart.write(bytes(data, 'utf-8'))
    sleep_ms(2500)