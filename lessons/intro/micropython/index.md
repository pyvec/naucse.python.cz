# MicroPython (na ESP8266/NodeMCU)

(Tato lekce bohužel, na rozdíl od předchozích, nejde jen tak vyzkoušet z domu – je potřeba speciální hardware.)

Dnes si ukážeme, jak lze Python použít na malých/vestavěných zařízeních.

Před sebou byste měli mít:

* vývojovou desku *NodeMCU*,
* modrou LED,
* pásek s RGB LED moduly,
* několik drátků,
* malé nepájivé pole.

Přichystejte si MicroUSB kabel. Pokud nemáte vlastní, několik jich můžeme zapůjčit.

Obsah lekce vychází z tutoriálů pro PyLadies ([a](https://naucse.python.cz/2019/brno-podzim-pondeli/sessions/micropython/), [b](https://github.com/stlk/micropython/tree/master/workshop)), na které se můžete podívat, pokud tu bude něco vysvětleno příliš rychle.


## Popis desky

V posledních letech se dá za relativně málo peněz pořídit počítač dost „velký” na to, aby se na něm dal spustit MicroPython – speciální implementace Pythonu pro prostředí s omezenou pamětí.
NodeMCU, které budeme používat my, obsahuje čip ESP8266, čip navržený jako ovladač WiFi k vestavěným systémům (např. k Arduinu).
Kromě samotného čipu a flash paměti, které se skrývají v oplechované krabičce, je na desce převodník napětí z 5 V (USB) na 3,3 V a datový převodník z USB na sériový protokol a jednotlivé piny procesoru jsou vyvedeny na „nožičky” desky.

V paměti je už nahraný firmware MicroPython; pojďme se k němu připojit.


## Drivery a připojení

Postup připojení je jiný pro každý systém:
* Linux: Driver už je nainstalovaný; nainstalujte `picocom`, přidejte se do skupiny jako `dialout` (Fedora, nové Ubuntu) nebo `uucp` (Arch, některý Debian) (správnou skupinu zjistíte pomocí `ls -l /dev/ttyUSB0`) a zadejte `picocom -b 115200 --flow n /dev/ttyUSB0`.
* Windows: Připojte se pomocí [PuTTY](http://www.chiark.greenend.org.uk/~sgtatham/putty/download.html) (`putty.exe`). Nastavení:
  * Session:Connection Type: Serial
  * Serial/Serial line: COM port (najdeš ve správci zařízení)
  * Serial/Speed: 115200
  * Serial/Flow Control: None
* Mac: `screen /dev/tty.wchusbserial1420 115200`

Kdyby byly pro Windows či Mac potřeba ovladače, dají se najít na [stránkách výrobce](https://www.silabs.com/products/development-tools/software/usb-to-uart-bridge-vcp-drivers).

Po připojení stiskněte tlačítko RST na desce. Měla by se objevit hlavička a nakonec známý pythonní prompt `>>>`.


## MicroPython

Implementace MicroPython se chová téměř stejně jako CPython. Vyzkoušejte si ale některé rozdíly (porovnejte výstup MicroPythonu a Pythonu 3 na počítači):

``` python
>>> print
>>> import math
>>> math.pi
>>> import random
>>> random.randrange()
```

Hlavní omezení MicroPythonu je to, že chybí většina standardní knihovny.
Některé části (např `math`) jsou k dispozici, spousta ne.
Několik funkcí je na nestandardních místech se změněným rozhraním, např. generátor náhodných čísel:

```python
>>> from os import urandom
>>> urandom(1)[0]
61
```


## Vstup a výstup

Co má MicroPython navíc je přístup k hardwaru.
Zkusme zjistit hodnotu pinu 0, který je na NodeMCU normálně HIGH (3,3 V) a je spojen se zemí přes tlačítko FLASH.

```python
from machine import Pin
pin = Pin(0, Pin.IN)
print(pin.value())
```

API MicroPythonu často používá metody tam, kde bychom čekali atributy, proto ne `pin.value` ale `pin.value()`.

Konstanta `Pin.IN` konfiguruje daný pin pro čtení.
Zkusme si i zápis: zapojte stranu desky s piny D0-D8 do nepájivého pole a mezi piny `D5` a `G` zapojte diodu.
Následující kód diodu rozsvítí:

```python
from machine import Pin
pin = Pin(14, Pin.OUT)
pin.value(1)
```

Pro zhasnutí zadejte `pin.value(0)`. (Opět jde o volání metody, není to `pin.value = 0`.)

`Pin(14)` odpovídá pinu označenému `D5` – číslování, které používá procesor (a MicroPython), se bohužel liší od toho, které používá deska.
Odpovídající si označení lze zjistit z [taháku](https://pyvec.github.io/cheatsheets/micropython/nodemcu-cs.pdf).

Zkuste zajistit, aby dioda svítila, právě pokud je stisknuté tlačítko FLASH.


## Ovládání konzole

Pravděpodobně jste si všimli, že konzole MicroPythonu automaticky odsazuje.
To je pro malé programy pohodlné, ale umí to i znepříjemnit život – hlavně když chceme kód do konzole vložit.

Proto má konzole MicroPythonu speciální vkládací mód, který automatické odsazování vypíná.
Aktivuje se pomocí <kbd>Ctrl+E</kbd> a ukončuje se pomocí <kbd>Ctrl+D</kbd>.

Existuje ale i nástroj jménem `ampy`, který umožňuje pustit předpřipravený skript.
Instaluje se jako `adafruit-ampy`:

```console
$ python -m pip install adafruit-ampy
```

Po nainstalování vypněte existující připojení k desce (picocom/screen/PuTTY),
napište skript a spusťte ho pomocí příkazu `run`:

```console
$ ampy -p PORT run script.py
```

Kde `PORT` je stejný port jako výše – např. `/dev/ttyUSB0` na Linuxu, `COM3` na Windows.
Pro více informací můžete nepřekvapivě použít příkaz `ampy --help`.

Od teď doporučuji psát kód vedle do editoru a spouštět jej pomocí `ampy run`.

Zkuste pomocí funkce `time.sleep` (která v MicroPythonu k dispozici je) diodou blikat v pravidelných intervalech.


## Blikání

Na pravidelné blikání, technicky řečeno *pulzně-šířkovou modulaci* (angl. *Pulse Width Modulation*)
má MicroPython třídu `PWM`, které se dá nastavit frekvence (`freq`) v Hz a střída (`duty`) od 0 do 1024:

```python
from machine import Pin, PWM
from time import sleep

led_pin = Pin(14, Pin.OUT)
pwm = PWM(led_pin, freq=50, duty=512)
```

Výsledný signál – čtvercová vlna – lze použít pro ovládání
LED (střída určuje intenzitu světla), bzučáků (frekvence určuje výšku tónu),
servomotorků (délka signálu určuje úhel otočení), atd.


## LED pásek WS2812

Na destičku se dá připojit spousta různých komponent. Jen je vždy potřeba ověřit v [dokumentaci], že existuje knihovna pro daný protokol na MicroPython *pro ESP8266*.
Časté protokoly jsou [I2C], [OneWire], či [SPI].

My připojíme pásek s moduly WS2812.
Každý modul obsahuje tři LED a čip, který umožňuje celý pásek ovládat jedním datovým pinem.
Používá vlastní protokol, který je v MicroPythonu pro ESP8266 implementován pod jménem `NeoPixel`.

[dokumentaci]:http://docs.micropython.org/en/latest/esp8266/
[I2C]: http://docs.micropython.org/en/latest/esp8266/library/machine.I2C.html#machine-i2c
[OneWire]: http://docs.micropython.org/en/latest/esp8266/esp8266/quickref.html#onewire-driver
[SPI]: http://docs.micropython.org/en/latest/esp8266/esp8266/quickref.html#software-spi-bus

Zapojení:

  * `GND` - `G`
  * `DI` (data in) - `D4`
  * `+5V` - `VU`

Kód:

```python
from machine import Pin
from neopixel import NeoPixel

NUM_LEDS = 8
pin = Pin(2, Pin.OUT)
np = NeoPixel(pin, NUM_LEDS)
np[0] = (255, 255, 255)
np.write()
```

Co znamenají čísla 0 a 255 na posledním řádku, jistě zjistíte experimentálně.


## Flashování

Na našich destičkách je MicroPython už nahraný, ale kdybyste si koupili vlastní NodeMCU nebo chtěli firmware aktualizovat, budete ho potřebovat umět nahrát.

K tomu je potřeba nástroj `esptool`, který se dá nainstalovat pomocí:

```console
$ python -m pip install esptool
```

Po instalaci esptool si stáhněte nejnovější stabilní firmware pro ESP8266 z [micropython.org/download](http://micropython.org/download#esp8266) a zadejte:

```console
$ esptool.py --port /dev/ttyUSB0 --baud 460800 write_flash 0 esp8266-20161110-v1.8.6.bin
```

Hodnotu pro `--port` opět doplňte podle svého systému – např. `/dev/tty.wchusbserial1420` na Macu, `COM3` na Windows.

> [note]
> Destiček s čipem ESP8266 se vyrábí celá řada různých typů a některé mohou
> potřebovat odlišné nastavení při flashování.
> Popis všech možností nastavení je k nalezení v [dokumentaci k esptool](https://github.com/espressif/esptool#usage).

Je-li na desce nahraný MicroPython, tento příkaz by měl fungovat. U jiného firmware, (případně u poškozeného MicroPythonu), je potřeba při zapojování destičky do USB držet tlačítko FLASH.

## Souborový systém

MicroPython pro ESP8266 obsahuje souborový systém nad flash pamětí,
se kterým pracují standardní pythonní funkce jako `open` a `os.listdir`.
Nahrajete-li soubor s příponou `.py`, lze jej pak v kódu importovat.

Existuje-li soubor `main.py`, naimportuje se automaticky po zapnutí (či resetu)
zařízení.
Není ho pak potřeba připojovat k počítači – stačí powerbanka nebo 3,3V zdroj.

Pro nahrání souborů do zařízení můžete použít příkaz `ampy put`:

```console
$ ampy -p PORT put main.py
```


## WebREPL

ESP8266 byl původně navržen i jako čip pro WiFi a i s MicroPythonem se umí připojit k síti.
Dokonce se přes WiFi dá i ovládat.

Otevřete si stránku [micropython.org/webrepl](http://micropython.org/webrepl/), přes kterou budete po připojení s destičkou komunikovat.

Poté se buď připojte k existující WiFi síti (Eduroam fungovat nebude) nebo použijte destičku jako samostatný *access point*:

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
```

Nastavení WebREPL spusťte z interaktivní konzole:


```pycon
>>> import webrepl_setup
```

S počítačem se připojte na stejnou síť a na stránce webrepl otevřené výše se připojte k IP vypsané z `ifconfig()`.
Měli byste dostat konzoli, jako přes USB.
Pomocí WebREPL lze nejen zadávat interaktivní příkazy, ale i nahrávat soubory.


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
