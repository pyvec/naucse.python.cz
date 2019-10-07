# Funkce
[Dříve]({{ lesson_url('beginners/functions') }}) jsme
volal{{gnd('i', 'y', both='i')}} funkce, které napsal někdo jiný:

```python
print('Ahoj světe!')
```

Dnes si ukážeme, jak psát funkce vlastní.

Pokud umíš `if` a `for` – s jednořádkovou hlavičkou a odsazeným tělem příkazu –
neměl by ti zápis funkce připadat nijak zvláštní:

```python
def obvod_obdelnika(sirka, vyska):
    "Vrátí obvod obdélníka daných rozměrů"
    obvod = 2 * (sirka + vyska)
    return obvod

print(obvod_obdelnika(4, 2))
```

Jak to funguje?


Funkce se *definuje* příkazem `def`, za nějž napíšeš jméno funkce,
pak do závorky seznam *parametrů*, které funkce bere, a pak dvojtečku.

Potom následuje odsazené *tělo funkce* – příkazy, které funkce provádí.
Tělo může začít *dokumentačním řetězcem*, který popisuje, co funkce dělá.

Příkazem `return` pak můžeš z funkce *vrátit* nějakou hodnotu.

Tělo funkce může mít více příkazů – včetně podmínek, cyklů a podobně.
Následující procedura třeba vypíše skóre daného hráče a k tomu hlášku:

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
zavoláš, přiřadí jednotlivým parametrům.
Takže když zavoláš třeba `napis_hlasku('Tvoje', 256)`,
můžeš si představit, že funkce dělá následující:

```python
# Nastavení proměnných podle parametrů
nazev = 'Tvoje'
skore = 256

# Samotné tělo funkce
print(nazev, 'skóre je', skore)
if skore > 1000:
    print('Světový rekord!')
elif skore > 100:
    ... # atd.
```
## Vracení

Speciální příkaz `return`, který jde použít jenom ve funkcích,
*ukončí* funkci a vrátí danou hodnotu ven z funkce.

Chová se tedy trochu jako `break`, jen místo cyklu opouští celou funkci.

Podobně jako `break` se dá použít v případech, kdy potřebuješ od uživatele
dostat odpověď – a opakuješ dotaz tak dlouho, dokud požadovanou odpověď
nedostaneš.
Třeba, chceš-li odpověď „ano“ nebo „ne“:

* Takhle se zjišťuje odpověď ano (Pravda) nebo ne (Nepravda) na danou *otázku*:
  * Pořád dokola:
    * Zeptej se na *otázku*; zapamatuj si *odpověď*.
    * Je-li odpověď „ano“:
      * Výsledek je Pravda. Hotovo; dál nepokračuj.
    * Jinak, je-li odpověď „ne“:
      * Výsledek je Nepravda. Hotovo; dál nepokračuj.
    * Pouč uživatele, ať odpoví „ano“ nebo „ne“.
      <br>*(a zkus to znovu – viz „Pořád dokola“)*

```python
def ano_nebo_ne(otazka):
    "Vrátí True nebo False podle odpovědi uživatele"
    while True:
        odpoved = input(otazka)
        if odpoved == 'ano':
            return True
        elif odpoved == 'ne':
            return False

        print('Nerozumím! Odpověz "ano" nebo "ne".')

# Příklad použití
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

Předchozí program se dá napsat i jako procedura, tedy funkce která nic nevrací.
Výsledek může třeba vypsat na obrazovku:

```python
from math import pi

def obsah_elipsy(a, b):
    print('Obsah je', pi * a * b)  # Pozor, `print` místo `return`!

obsah_elipsy(3, 5)
```

Program takhle funguje, ale přichází o jednu z hlavních výhod funkcí:
možnost vrácenou hodnotu použít i jinak jež jen v `print`.

Funkci, která vrací výsledek, můžeš použít v dalších výpočtech:

```python
def objem_eliptickeho_valce(a, b, vyska):
    return obsah_elipsy(a, b) * vyska

print(objem_eliptickeho_valce(3, 5, 3))
```

... ale s procedurou, která výsledek přímo vypíše, by to nešlo.

Další důvod, proč hodnoty spíš vracet než vypisovat, je ten, že jedna funkce se
dá použít v různých situacích.
Proceduru s `print` by nešlo rozumně použít tehdy, když nás příkazová
řádka vůbec nezajímá – třeba v grafické hře, webové aplikaci, nebo pro ovládání
robota.

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

Samozřejmě existují výjimky: procedura která přímo vytváří textový výpis
může používat `print`; funkce která načítá textové informace zase `input`.
Když ale funkce něco *počítá*, nebo když si nejsi jist{{gnd('ý', 'á')}},
je dobré ve funkci `print` ani `input` nemít.


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

Procedury v Pythonu vracejí právě toto „nic“.
