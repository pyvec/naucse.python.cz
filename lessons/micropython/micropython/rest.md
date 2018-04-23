
## WiFi

Jak jsme zmínili na začátku, byl čip ESP8266 primárně určen pro práci s WiFi
a tato schopnost mu zůstala. Umí se buď připojit k existující síti, nebo
ze sebe udělat hotspot a vytvořit si tak vlastní WiFi síť. Obě tyto možnosti
nám umožní spojit se s destičkou bezdrátově a pracovat s ní skrze
webový prohlížeč pomocí tzv. WebREPL, nebo použít připojení k síti k odesílání
dat z destičky pro další zpracování.

Používání WiFi je ovšem mimo možnosti tohoto workshopu. Vše potřebné k jejímu
zprovoznění je k dispozici [v této části dokumentace](https://docs.micropython.org/en/latest/esp8266/esp8266/tutorial/repl.html#webrepl-a-prompt-over-wifi).








## WebREPL

ESP8266 byl původně navržen i jako čip pro WiFi a i s MicroPythonem se umí připojit k síti.
Dokonce se přes WiFi dá i ovládat.

Otevřete si stránku [micropython.org/webrepl](http://micropython.org/webrepl/),
přes kterou budete po připojení s destičkou komunikovat.

Poté se buď připojte k existující WiFi síti (Eduroam fungovat nebude) nebo
použijte destičku jako samostatný *access point*:

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

S počítačem se připojte na stejnou síť a na stránce webrepl otevřené výše
se připojte k IP vypsané z `ifconfig()`. Měli byste dostat konzoli, jako přes
USB. Pomocí WebREPL lze nejen zadávat interaktivní příkazy, ale i nahrávat
soubory.


## Komunikace

Pro komunikaci po síti můžete použít nízkoúrovňovou knihovnu `socket`,
nebo protokol pro „internet of things“ (jako MQTT), ale
MicroPython pro ESP8266 má zabudouvanou i knihovnu pro HTTP:
ořezanou verzi známých Requests.
Následující kód stáhne data ze stránky
[api.thingspeak.com/channels/1417/field/2/last.txt](http://api.thingspeak.com/channels/1417/field/2/last.txt),
kde se objevuje poslední barva tweetnutá s hashtagem `#cheerlights`.

Výslednou hodnotu lze použít jako barvu modul v LED pásku.

```python
import urequests

url = 'http://api.thingspeak.com/channels/1417/field/2/last.txt'

def download_color():
    response = urequests.get(url)
    text = response.text

    if text and text[0] == '#':
        color = text[1:7]

        red = int(color[0:2], 16)
        green = int(color[2:4], 16)
        blue = int(color[4:6], 16)

        return red, green, blue
    return 0, 0, 0
```

Opravdové projekty používají lehčí protokoly než HTTP, například MQTT.
