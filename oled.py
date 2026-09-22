# oled.py
from machine import Pin, I2C
import ssd1306

I2C_SDA = 0
I2C_SCL = 4

WIDTH  = 128
HEIGHT = 64
FONT_W = 8
FONT_H = 8

LINE_H = FONT_H
MAX_LINES = HEIGHT // LINE_H

_oled = None
_lines = []

def init():
    global _oled, _lines

    i2c = I2C(0, sda=Pin(I2C_SDA), scl=Pin(I2C_SCL), freq=400_000)
    _oled = ssd1306.SSD1306_I2C(WIDTH, HEIGHT, i2c)

    _lines = []
    _oled.fill(0)
    _oled.show()

def repl(msg):
    global _lines

    if _oled is None:
        return

    msg = str(msg)

    MAX_CHARS = WIDTH // FONT_W

    while len(msg) > MAX_CHARS:
        _lines.append(msg[:MAX_CHARS])
        msg = msg[MAX_CHARS:]
    _lines.append(msg)

    _lines = _lines[-MAX_LINES:]

    _oled.fill(0)
    for i, line in enumerate(_lines):
        _oled.text(line, 0, i * LINE_H)
    _oled.show()