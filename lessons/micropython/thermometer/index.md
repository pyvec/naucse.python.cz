## Teploměr

Poslední součástkou, kterou si dnes ukážeme, bude jednoduchý teploměr DS18B20.
Tento teploměr se vyrábí v několika provedeních a je velmi populární především
pro jednoduchost použití a velmi nízkou cenu.

Stejně jako si MicroPython pomocí speciálního „jazyka” rozumí s LED páskem, ovládá
i „jazyk” pro komunikaci s teploměrem a řadou dalších zařízení. 1-wire sběrnice
má navíc tu výhodu, že se na jednu nožičku naší destičky dá připojit hned
několik teploměrů a číst teploty z každého z nich.

Otoč teploměr tak, aby jeho „břicho” směřovalo směrem od tebe a takto jej zapoj
do nevyužité části nepájivého pole. Následně propoj nožičky teploměru
s destičkou takto:

* Levou nožičku propoj s `G`
* Prostřední nožičku propoj s `D2`
* Pravou nožičku propoj s `3V`

> [note]
> Po zapojení drž teploměr na chvíli mezi prsty. Pokud je zapojený špatně začne
> se velmi rychle zahřívat a v takovém případě jej okamžitě odpoj.

Pokud je vše zapojeno správně, můžeme přistoupit k měření teploty.

```python
from time import sleep
from machine import Pin
import onewire
from ds18x20 import DS18X20


pin = Pin(4, Pin.IN)
ow = DS18X20(onewire.OneWire(pin))

sensory = ow.scan()
ow.convert_temp()
sleep(1)
teplota = ow.read_temp(sensory[0])
print("Teplota je", teplota)
```

Nejdříve si opět připravíme nožičku (pin) pro komunikaci a následně si na ní
připravíme komunikační protokol OneWire. Prvním krokem k teplotě je nalezení
všech dostupných teploměrů na dané sběrnici, což nám zajistí metoda `ow.scan()`,
která nám vrátí seznam identifikátorů nalezených teploměrů.
Metoda `ow.convert_temp()` pak pošle všem teploměrům příkaz, aby změřily
teplotu. Po tomhle rozkazu musíme alespoň vteřinu počkat a následně můžeme
teplotu z našeho čidla přečíst.
