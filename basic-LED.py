from machine import Pin
import time

led = Pin(4, Pin.OUT) #กำหนดให้ pin 4 เป็น output

while True:
    led.value(1)  #เปิด LED
    print("LED ON") # แสดงข้อความใน Console
    time.sleep(1)   # หน่วงเวลา 1 วินาที

    led.value(0)    # ปิด LED
    print("LED OFF")
    time.sleep(1)   # หน่วงเวลา 1 วินาที
