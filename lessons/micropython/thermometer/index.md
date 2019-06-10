# Teploměr

Poslední součástkou, kterou si dnes ukážeme, bude jednoduchý teploměr DS18B20.
Tento teploměr se vyrábí v několika provedeních a je velmi populární především
pro jednoduchost použití a velmi nízkou cenu.

Stejně jako si MicroPython pomocí speciálního „jazyka” rozumí s LED páskem,
ovládá i „jazyk” pro komunikaci s teploměrem a řadou dalších zařízení.
Tento „jazyk“, protokol sběrnice OneWire, má navíc tu výhodu, že se na jednu
nožičku destičky dá připojit hned několik teploměrů a číst teploty
z každého z nich.


## Zapojení

> [warning]
> Po zapojení drž teploměr na chvíli mezi prsty.
> Pokud je zapojený špatně, začne se velmi rychle zahřívat.
> V takovém případě jej okamžitě odpoj.

Otoč teploměr tak, aby jeho „břicho” směřovalo směrem od tebe.
Následně propoj nožičky teploměru s destičkou takto:

* Levou nožičku propoj s `GND`
* Prostřední nožičku propoj s `D4`
* Pravou nožičku propoj s `3V3`

# Měření

Pokud je vše zapojeno správně, přistup k měření teploty.

```python
from time import sleep
from machine import Pin
import onewire
from ds18x20 import DS18X20


pin = Pin(2, Pin.IN)  # D4
ow = DS18X20(onewire.OneWire(pin))
sensory = ow.scan()

ow.convert_temp()
sleep(1)
teplota = ow.read_temp(sensory[0])
print("Teplota je", teplota)
```

Tento kód nejdříve opět připraví nožičku (pin) pro komunikaci a následně na ní
připraví komunikační protokol OneWire a teploměr DS18X20.
Prvním krokem k teplotě je nalezení všech dostupných teploměrů na dané
sběrnici, což nám zajistí metoda `ow.scan()`,
která nám vrátí seznam identifikátorů nalezených teploměrů.

Metoda `ow.convert_temp()` pak pošle všem teploměrům příkaz, aby změřily
teplotu.
Po tomhle rozkazu musíš alespoň vteřinu počkat a následně můžeš
teplotu z čidla přečíst.

Zkus teploměr na chvíli chytit mezi prsty, zahřát ho tak, a změřit teplotu
znovu.
