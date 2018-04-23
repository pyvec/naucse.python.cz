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
