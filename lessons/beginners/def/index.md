# Funkce
[Dříve]({{ lesson_url('beginners/functions') }}) jsme
volal{{gnd('i', 'y', both='i')}} funkce, které napsal někdo jiný:

```python
print('Ahoj světe!')
```

Dnes si ukážeme, jak psát funkce vlastní.

Není to tak složité:

```python
def obvod_obdelnika(sirka, vyska):
    "Vrátí obvod obdélníka daných rozměrů"
    return 2 * (sirka + vyska)

print(obvod_obdelnika(4, 2))
```

Jak to funguje?


Funkce se *definuje* příkazem `def`, za nějž napíšeš jméno funkce,
pak do závorky seznam *argumentů*, které funkce bere, a pak dvojtečku.

Potom následuje odsazené *tělo funkce* – příkazy, které funkce provádí.
Tělo může začít *dokumentačním řetězcem*, který popisuje, co funkce dělá.

Příkazem `return` pak můžeš z funkce
vrátit nějakou hodnotu.

Tělo funkce může mít více příkazů, včetně podmínek, cyklů a podobně:

```python
def napis_hlasku(nazev, skore):
    "Popíše skóre. Název má být přivlastňovací přídavné jméno."

    print(nazev, 'skóre je', skore)
    if skore > 1000:
        print('Světový rekord!')
    elif skore > 100:
        print('Skvělé!')
    elif skore > 10:
        print('Ucházející.')
    elif skore > 1:
        print('Aspoň něco')
    else:
        print('Snad příště.')

napis_hlasku('Tvoje', 256)
napis_hlasku('Protivníkovo', 5)
```

Při volání funkce se hodnoty, se kterými funkci
zavoláš, přiřadí jednotlivým argumentům.
Takže když zavoláš třeba `napis_hlasku('Tvoje', 256)`,
můžeš si představit, že funkce dělá následující:

```python
nazev = 'Tvoje'
skore = 256

print(nazev, 'skóre je', skore)
if skore > 1000:
    ... # atd.
```
## Vracení

Speciální příkaz `return`, který jde použít jenom ve funkcích,
*ukončí* funkci a vrátí danou hodnotu ven z funkce.

Chová se tedy trochu jako `break`, jen místo cyklu opouští celou funkci.

```python
def ano_nebo_ne(otazka):
    "Vrátí True nebo False, podle odpovědi uživatele"
    while True:
        odpoved = input(otazka)
        if odpoved == 'ano':
            return True
        elif odpoved == 'ne':
            return False
        else:
            print('Nerozumím! Odpověz "ano" nebo "ne".')

if ano_nebo_ne('Chceš si zahrát hru? '):
    print('OK! Ale napřed si ji musíš naprogramovat.')
else:
    print('Škoda.')
```

> [note]
> Stejně jako `if` nebo `break` je `return` *příkaz*, ne funkce.
> Kolem „své“ hodnoty nepotřebuje závorky.

Zkus napsat funkci, která vrátí obsah elipsy
daných rozměrů.
Příslušný vzoreček je <var>A</var> = π<var>a</var><var>b</var>,
kde <var>a</var> a <var>b</var> jsou délky os.

Funkci zavolej a výsledek vypiš.

{% filter solution %}
```python
from math import pi

def obsah_elipsy(a, b):
    return pi * a * b

print('Obsah elipsy s osami 3 cm a 5 cm je', obsah_elipsy(3, 5), 'cm2')
```
{% endfilter %}


### Vrátit nebo vypsat?

Předchozí program se dá napsat i takto:

```python
from math import pi

def obsah_elipsy(a, b):
    print('Obsah je', pi * a * b)  # Pozor, `print` místo `return`!

obsah_elipsy(3, 5)
```

Program takhle funguje, ale přichází o jednu z hlavních výhod funkcí:
možnost vrácenou hodnotu použít i jinak jež jen v `print`.

Funkci, která výsledek vrací, můžeš použít v dalších výpočtech:

```python
def objem_eliptickeho_valce(a, b, vyska):
    return obsah_elipsy(a, b) * vyska

print(objem_eliptickeho_valce(3, 5, 3))
```

... ale kdyby výsledek přímo vypsala, nešlo by to.

Další důvod, proč hodnoty spíš vracet než vypisovat, je ten, že jedna funkce se
dá použít v různých situacích.
Funkci s `print` by nešlo rozumně použít tehdy, když nás příkazová
řádka vůbec nezajímá.
Třeba v grafické hře, webové aplikaci, nebo pro ovládání robota.

Podobně je to se vstupem: když použiju v rámci své funkce `input`, bude se
moje funkce dát použít jen v situacích, kdy je u počítače klávesnice a za ní
člověk.
Proto je lepší funkcím potřebné informace předávat jako argumenty
a `input` (nebo textové políčko či měření z čidla robota) nemít ve funkci,
ale vně:

```python
from math import pi

def obsah_elipsy(a, b):
    """Vrátí obsah elipsy s poloosami daných délek"""
    # Jen samotný výpočet:
    return pi * a * b

# print a input jsou "venku":
x = float(input('Zadej délku poloosy 1: '))
y = float(input('Zadej délku poloosy 2: '))
print('Obsah je', obsah_elipsy(x, y))
```

Samozřejmě existují výjimky: funkce která přímo vytváří textový výpis,
může používat `print`; funkce která načítá textové informace zase `input`.
Když ale funkce něco počítá, je dobré v ní `print` ani `input` nemít.


## None

Když funkce neskončí příkazem `return`,
automaticky se vrátí hodnota `None`.

Je to hodnota zabudovaná přímo do Pythonu, podobně jako `True` nebo `False`,
a znamená „nic“.

```python
def nic():
    "Tahle funkce nic nedělá"

print(nic())
```


## Lokální proměnné

Gratuluji, umíš definovat vlastní funkce!
Zbývá ještě vysvětlit jednu věc: lokální a globální proměnné.

Funkce může používat proměnné „zvnějšku“:

```python
pi = 3.1415926

def obsah_kruhu(polomer):
    return pi * polomer ** 2

print(obsah_kruhu(100))
```

Ale všechny argumenty a všechny proměnné, do kterých funkce přiřazuje,
jsou *úplně nové* proměnné, které nemají nic
společného s tím, co je „venku“ kolem funkce.

Těm úplně novým proměnným se říká
*lokální proměnné* (angl. *local variables*), protože existují
jen místně, v rámci volání jedné jediné funkce.
Takže tohle nebude fungovat tak, jak se zdá:

```python
x = 0

def nastav_x(hodnota):
    x = hodnota  # Přiřazení do lokální proměnné!

nastav_x(40)
print(x)
```


Proměnné, které nejsou lokální, jsou *globální* – ty
existují v celém programu.
(Jen ve funkcích, které mají náhodou
lokální proměnnou stejného jména, „nejsou vidět“ –
to jméno označuje lokální proměnnou.)

Pojďme si to ukázat.
Než spustíš tenhle program,
zkus předpovědět, co bude dělat.
Pak ho pusť, a pokud dělal něco jiného,
zkus vysvětlit proč.
Pozor, je tam chyták!

```python
from math import pi
obsah = 0
a = 30

def obsah_elipsy(a, b):
    obsah = pi * a * b  # Přiřazení do `obsah`
    a = a + 3  # Přiřazení do `a`
    return obsah

print(obsah_elipsy(a, 20))
print(obsah)
print(a)
```

Zkus odpovědět na tyto otázky:

* Je proměnná `pi` lokální, nebo globální?
* Je proměnná `obsah` lokální, nebo globální?
* Je proměnná `a` lokální, nebo globální?
* Je proměnná `b` lokální, nebo globální?

{% filter solution %}
* `pi` je globální – nepřiřazuje se do ní ve funkci;
  je „vidět“ v celém programu.
* Proměnné `obsah` jsou v programu dvě – jedna globální,
  a jedna je lokální pro funkci `obsah_elipsy`,
  protože do ní tahle funkce přiřazuje.
* Proměnné `a` jsou taky dvě, podobně jako `obsah`.
  Tady byl chyták: příkaz `a = a + 3` nemá žádný smysl;
  do `a` se sice uloží větší číslo, ale vzápětí funkce `obsah_elipsy` skončí
  a její lokální proměnná `a` přestane existovat.
* Proměnná `b` je jenom lokální – jako argument funkce `obsah_elipsy`.

{% endfilter %}


Jestli ti to celé připadá zmatené a složité, dá se tomu zatím vyhnout
dodržováním jednoho pravidla:
*nepřiřazuj ve funkcích do proměnných, které existují i vně funkce.*
(Parametr funkce se počítá jako přiřazení.)
