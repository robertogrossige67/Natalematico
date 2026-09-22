from machine import Pin
from time import sleep

r1 = Pin(32, Pin.OUT)
r2 = Pin(33, Pin.OUT)
r3 = Pin(25, Pin.OUT)
r4 = Pin(26, Pin.OUT)

r1.off()
r2.off()
r3.off()
r4.off()

r1.on()
sleep(1)
r1.off()

r2.on()
sleep(1)
r2.off()

r3.on()
sleep(1)
r3.off()

r4.on()
sleep(1)
r4.off()