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

Obsah lekce vychází z tutoriálů pro PyLadies ([a](http://pyladies.cz/v1/s016-micropython/index.html), [b](https://github.com/stlk/micropython/tree/master/workshop)), na které se můžete podívat pokud tu bude něco vysvětleno příliš rychle.


## Popis desky

V posledních letech se dá za relativně málo peněz pořídit počítač dost „velký” na to, aby se na něm dal spustit MicroPython – speciální implementace Pythonu pro prostředí s omezenou pamětí.
NodeMCU, které budeme používat my, obsahuje čip ESP8266, čip navržený jako ovladač WiFi k vestavěným systémům (např. k Arduinu).
Kromě samotného čipu a flash paměti, které se skrývají v oplechované krabičce, je na desce převodník napětí z 5 V (USB) na 3,3 V a datový převodník z USB na sériový protokol, a jednotlivé piny procesoru jsou vyvedeny na „nožičky” desky.

V paměti je už nahraný firmware MicroPython; pojďme se k němu připojit.


## Drivery a připojení

Postup připojení je jiný pro každý systém:
* Linux: Driver už je nainstalovaný; nainstalujte `picocom`, přidejte se do skupiny jako `dialout` (Fedora) nebo `uucp` (Debian) a zadej `picocom -b 115200 --flow n /dev/ttyUSB0`
* Windows: Připojte se pomocí [PuTTY](http://www.chiark.greenend.org.uk/~sgtatham/putty/download.html) (`putty.exe`). Nastavení:
  * Session:Connection Type: Serial
  * Serial/Serial line: COM port (najdeš ve správci zařízení)
  * Serial/Speed: 115200
  * Serial/Flow Control: None
* Mac: `screen /dev/tty.wchusbserial1420 115200`

Kdyby byly pro Windows či Mac potřeba ovladače, dají se najít na [iotta.cz/ovladace-pro-ch340g](https://iotta.cz/ovladace-pro-ch340g/)

Po připojení stiskněte tlačítko RST na desce. Měla by se objevit hlavička a nakonec známý pythonní prompt `>>>`.


## MicroPython

Implementace MicroPython se chová téměř stejně jako CPython. Vyzkoušejte si ale některé rozdíly (porovnejte výstup MicroPythonu a Pythonu 3 na počítači):

``` python
>>> print
>>> import math
>>> math.pi
>>> import random
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
Zkusme zjistit hodnotu pinu 0, který je na NodeMCU normálně HIGH (3,3 V) spojen se zemí přes tlačítko FLASH.

```python
from machine import Pin
pin = Pin(0, Pin.IN)
print(pin.value())
```

API MicroPythonu často používá metody tam, kde bychom čekali atributy, proto ne `pin.value` ale `pin.value()`.

Konstanta `Pin.IN` konfiguruje daný pin pro čtení.
Zkusme si i zápis: zapojte stranu desky s piny D0-D8 do nepájivého pole, a mezi piny `D5` a `G` zapojte diodu.
Následující kód diodu rozsvítí:

```python
from machine import Pin
pin = Pin(14, Pin.OUT)
pin.value(1)
```

Pro zhasnutí zadejte `pin.value(0)`. (Opět jde o volání metody, není to `pin.value = 0`.)

`Pin(14)` odpovídá pinu označenému `D5` – číslování, které používá procesor (a MicroPython), ze bohužel liší od toho, které používá deska.
Odpovídající si označení lze zjistit z [taháku](https://github.com/pyvec/cheatsheets/raw/master/micropython/nodemcu-cs.pdf).

Zkuste zajistit, aby dioda svítila, právě pokud je stisknuté tlačítko FLASH.


## Ovládání konzole

Pravděpodobně jste si všimli, že konzole MicroPythonu automaticky odsazuje.
To je pro malé programy pohodlné, ale umí to i znepříjemnit život – hlavně když chceme kód do konzole vložit.
Proto má konzole MicroPythonu speciální vkládací mód, který automatické odsazování vypíná.
Aktivuje se pomocí <kbd>Ctrl+E</kbd> a ukončuje se pomocí <kbd>Ctrl+D</kbd>.

Od teď doporučuji psát kód vedle do editoru a vždy jej do konzole zkopírovat.

Zkuste pomocí funkce `time.sleep` (která v MicroPythonu k dispozici je) diodou blikat v pravidelných intervalech.


## Blikání

Na pravidelné blikání má MicroPython třídu `PWM`, které se dá nastavit frekvence (`freq`) v Hz a střída (`duty`) od 0 do 1024:

```python
from machine import Pin, PWM
from time import sleep

led_pin = Pin(14, Pin.OUT)
pwm = PWM(led_pin, freq=50, duty=512)
```


## LED pásek WS2812

Na destičku se dá připojit spousta různých komponent. Jen je vždy potřeba ověřit v [dokumentaci], že existuje knihovna pro daný protokol na MicroPython *pro ESP8266*.
My připojíme pásek s moduly WS2812. Každý modul obsahuje tři LED a čip, který umožňuje celý pásek ovládat jedním datovým pinem.

[dokumnetaci]:http://docs.micropython.org/en/latest/esp8266/

Zapojení:
    
  * `GND` - `G`
  * `DI` (data in) - `D4`
  * `+5V` - `VU`

Kód:

```python
from machine import Pin
from neopixel import NeoPixel

POCET_LED = 8
pin = Pin(2, Pin.OUT)
np = NeoPixel(pin, POCET_LED)
np[0] = (255, 255, 255)
np.write()
```

Co znamenají čísla 0 a 255 na posledním řádku, jistě zjistíte experimentálně.


## Flashování

Na našich destičkách je MicroPython už nahraný, ale kdybyste si koupili vlastní NodeMCU, nebo chtěli firmware aktualizovat, budete ho potřebovat umět nahrát.

K tomu je potřeba nástroj `esptool`, který se, až vyjde verze 1.3, bude dát nainstalovat pomocí:

    python -m pip install esptool

Pokud tento příkaz ještě nefunguje, je potřeba použít vývojovou verzi přímo z GitHubu:

    python -m pip install git+https://github.com/espressif/esptool

Po instalaci esptool si stáhněte nejnovější stabilní firmware pro ESP8266 z [micropython.org/download](http://micropython.org/download#esp8266), a zadejte:

    esptool.py --port /dev/ttyUSB0 --baud 460800 write_flash 0 ~/dev/esptool/esp8266-20161110-v1.8.6.bin

Hodnotu pro `--port` doplňte podle svého systému – např. `/dev/tty.wchusbserial1420` na Macu, `COM3` na Windows.

Je-li na desce nahraný MicroPython, tento příkaz by měl fungovat. U jiného firmware, (případně u poškozeného MicroPythonu), je potřeba při zapojování destičky do USB držet tlačítko FLASH.


## WebREPL

ESP8266 byl původně navržen i jako čip pro WiFi, a i s MicroPythonem se umí připojit k síti.
Dokonce se přes WiFi dá i ovládat.

Otevřete si stránku [micropython.org/webrepl](http://micropython.org/webrepl/), přes kterou budete po připojení s destičkou komunikovat.

Poté se buď připojte k existující WiFi síti (Eduroam fungovat nebude), nebo použijte destičku jako samostatný *access point*:

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

ap_if = network.WLAN(network.AP_IF)
ap_if.active(True)
ap_if.config(essid=ESSID, password=PASSWORD, authmode=network.AUTH_WEP, channel=CHANNEL)
print('network config:', ap_if.ifconfig())

# Nastavení WebREPL:

import webrepl_setup
```

S počítačem se připojte na stejnou síť, a na stránce webrepl otevřené výše se připojte k IP vypsané z `ifconfig()`.
Měli byste dostat konzoli, jako přes USB.


## Webová komunikace

XXX: stahování přes HTTP; #cheerlights


## Souborový systém

XXX: main.py

