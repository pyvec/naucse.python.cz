# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
import gc
#import webrepl
#webrepl.start()
gc.collect()


from machine import Pin, PWM
from neopixel import NeoPixel
from time import sleep

flash = Pin(0, Pin.IN)                  # D3/FLASH
led = Pin(5, Pin.OUT)                   # D1
btn = Pin(14, Pin.IN)                   # D5
strip = NeoPixel(Pin(12, Pin.OUT), 8)   # D6
servo = PWM(Pin(15, Pin.OUT), freq=50)  # D8

Pin(2, Pin.OUT).value(1)    # D4/TXD1
Pin(4, Pin.OUT).value(0)    # D2
led.value(0)

BLACK = OFF = 0, 0, 0
WHITE = 10, 10, 10
RED = 10, 0, 0
ORANGE = 10, 5, 0
YELLOW = 10, 10, 0
GREEN = 0, 10, 0
CYAN = 0, 10, 10
BLUE = 0, 0, 10
VIOLET = PURPLE = PINK = 10, 0, 10
GRAY = 5, 5, 5


if btn.value() == 0:
    # Self-test
    colors = [RED, GREEN, BLUE, ORANGE, YELLOW, CYAN, PINK, GRAY]
    led.value(1)
    servo.duty(120)
    for i, color in enumerate(colors):
        strip[i] = color
    strip.write()
    sleep(0.5)
    servo.duty(40)
    for i in range(8):
        led.value(0)
        sleep(0.1)
        led.value(1)
        sleep(0.1)
        colors = colors[1:] + [colors[0]]
        for i, color in enumerate(colors):
            strip[i] = color
        strip.write()
    led.value(0)

for i in range(8):
    strip[i] = 0, 0, 0
strip.write()
