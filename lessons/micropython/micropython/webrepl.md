## WebREPL

ESP8266 byl původně navržen i jako čip pro WiFi a i s MicroPythonem se umí připojit k síti.
Dokonce se přes WiFi dá i ovládat.

Otevři si stránku [micropython.org/webrepl](http://micropython.org/webrepl/),
přes kterou budeš po připojení s destičkou komunikovat.

Poté se buď připoj k existující WiFi síti (Eduroam fungovat nebude) nebo
použij destičku jako samostatný *access point*:

```python

# Existující síť:

ESSID = ...
PASSWORD = ...

import network
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
if not wlan.isconnected():
    print('connecting to network...')
    wlan.connect(ESSID, PASSWORD)
    while not wlan.isconnected():
        pass
print('network config:', wlan.ifconfig())

# AP:

ESSID = ...
PASSWORD = ...
CHANNEL = 3

import network
ap_if = network.WLAN(network.AP_IF)
ap_if.active(True)
ap_if.config(essid=ESSID, password=PASSWORD, authmode=network.AUTH_WEP, channel=CHANNEL)
print('network config:', ap_if.ifconfig())

# Nastavení WebREPL:

import webrepl_setup
```

S počítačem se připoj na stejnou síť a na stránce webrepl otevřené výše
se připoj k IP vypsané z `ifconfig()`. Měl{{a}} bys dostat konzoli, jako přes
USB. Pomocí WebREPL lze nejen zadávat interaktivní příkazy, ale i nahrávat
soubory.
