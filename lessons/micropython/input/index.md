## Vstup

MicroPython na malé destičce obsahuje některé
moduly, které jinde nenajdeš. Ten hlavní se jmenuje
`machine` a zpřístupňuje základní funkce zařízení. Zkus si:

```python
from machine import Pin
pin = Pin(0, Pin.IN)
print(pin.value())
```

Zmáčkni a drž tlačítko `FLASH` vedle USB konektoru.
Přitom pusť `print(pin.value())` znovu.
Jak se hodnota změní?

Jak tomuhle kódu rozumět?
Třída `Pin` ti umožňuje ovládat jednotlivé
„nožičky”, kterými zařízení komunikuje s vnějším
světem: buď na nich nastavovat napětí, nebo zkoumat
jestli na nich nějaké napětí je.

`Pin(0, Pin.IN)` vytvoří objekt třídy Pin,
který bude načítat data z „nožičky” číslo 0.
(`IN` znamená načítání – informace jdou *do* procesoru).
Funkce `pin.value()` změří napětí na dané
„nožičce” a vrátí buď 1 nebo 0 podle toho, jestli nějaké naměřila.

No a „nožička” číslo 0 je připojená k tlačítku `FLASH`,
kterým se tak dá ono napětí ovládat.
Informace o tom, která nožička je kam připojená,
máš na [taháku](https://pyvec.github.io/cheatsheets/micropython/nodemcu-cs.pdf) –
můžeš si zkontrolovat, že Pin(0) u sebe má poznámku FLASH.
