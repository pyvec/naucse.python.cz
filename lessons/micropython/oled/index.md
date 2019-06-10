# OLED displej

Nejzákladnější informace pro modul s OLED displejem.


## Zapojení

* `GND` modulu na `GND` destičky
* `VDD` modulu na `3V3` destičky
* `SCK` modulu na `D4` destičky
* `SDA` modulu na `D3` destičky


## Kód

```
# Importy
from machine import Pin, I2C
from ssd1306 import SSD1306_I2C

# Komunikační protokol I2C a display SSD1306, 128x 64 bodů
i2c = I2C(scl=Pin(2, Pin.OUT), sda=Pin(0, Pin.OUT))
oled = SSD1306_I2C(width=128, height=64, i2c=i2c, addr=0x3c)

# Různé kreslící příkazy (se objeví až po zavolání show())
oled.line(0, 0, 64, 64, 1)
oled.text("Hello World", 0, 0, 1)
oled.rect(110, 2, 10, 5, 1)
oled.fill_rect(100, 20, 10, 5, 1)
oled.show()
```
