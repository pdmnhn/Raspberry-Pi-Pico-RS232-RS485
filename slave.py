from machine import UART, Pin
from time import sleep_ms

uart = UART(0, baudrate=9600, tx=Pin(16), rx=Pin(17))
commands = [0x38,0x0E,0x01,0x06,0x80]
str1 = "Photoresistor"

RS = Pin(0, Pin.OUT)
RW = Pin(1, Pin.OUT)
EN = Pin(2, Pin.OUT)

DE_RE = Pin(3, Pin.OUT)

data_pins = [Pin(6, Pin.OUT), Pin(7, Pin.OUT), Pin(8, Pin.OUT), Pin(9, Pin.OUT), Pin(10, Pin.OUT), Pin(11, Pin.OUT), Pin(12, Pin.OUT), Pin(13, Pin.OUT)]

DE_RE.value(0)

def send_cmd(cmd):
    byte = list(map(int, reversed(bin(cmd)[2:])))
    byte = byte + (8 - len(byte)) * [0]
    for i in range(8):
        data_pins[i].value(byte[i])
    RS.value(0)
    RW.value(0)
    EN.value(1)
    sleep_ms(1)
    EN.value(0)

def send_data(data):
    byte = list(map(int, reversed((bin(ord(data)))[2:])))
    byte = byte + (8 - len(byte)) * [0]
    for i in range(8):
        data_pins[i].value(byte[i])
    RS.value(1)
    RW.value(0)
    EN.value(1)
    sleep_ms(1)
    EN.value(0)

for i in commands:
    send_cmd(i)
    sleep_ms(2)

for i in str1:
    send_data(i)
    sleep_ms(2)
    
while True:
    if uart.any() > 0:
        data = uart.readline()
    else:
        continue
    
    send_cmd(0xC0)
    data_str = data.decode('utf-8')
    
    for i in data_str[:-1]:
        send_data(i)
        sleep_ms(2)
    
    sleep_ms(2500)

