# Definice funkcí
[Dříve]({{ lesson_url('beginners/functions') }}) jsme
volal{{gnd('i', 'y', both='i')}} funkce, které napsal někdo jiný:

```python
print('Ahoj světe!')
```

Dnes si ukážeme, jak psát funkce vlastní.


## K čemu jsou funkce?

Často se stává, že kód, který dělá nějakou jednoduchou věc, není úplně
jednoduchý.
Jako příklad uvedu nám už známý kód, který v určitém řetězci zamění znak
na dané pozici:

```python
zacatek = slovo[:pozice]
konec = slovo[pozice + 1:]
nove_slovo = zacatek + novy_znak + konec
```

Z takového kódu není na první pohled jasné, co přesně dělá.
Zvlášť když kód použiješ ve složitějším programu.

Dá se to vyřešit komentářem: ten, kdo bude program číst, si může přečíst
co to má dělat. Samotný složitější kód pak může ignorovat.

```python
# Ve slově `slovo` zaměnit znak na pozici `pozice` za `novy_znak`;
# výsledek bude v proměnné `nove_slovo`.
zacatek = slovo[:pozice]
konec = slovo[pozice + 1:]
nove_slovo = zacatek + novy_znak + konec
```

Ještě lepší ale bude si vytvořit *funkci*, která tenhle složitější postup
provede.
Jakmile takovou funkci vytvoříš, ve složitějším programu pak můžeš místo kódu
výše psát jen:

```python
nove_slovo = zamen(slovo, pozice, novy_znak)
```

Podobně fungují funkce, které už znáš: můžeš zavolat `print(123)`, aniž bys
potřeboval{{a}} znát jakékoli detaily postupu, kterým se číslo převede na
jednotlivé číslice a ty se pak vykreslí na obrazovce.
Nebo řekneš želvě `forward(100)` a nezatěžuješ se tím, jak si želva „pamatuje“
svůj aktuální úhel natočení nebo jak se vlastně kreslí čára.

Funkce umožňuje *pojmenovat* nějaký kousek programu, který se pak dá
použít pomocí jména bez detailních znalostí toho, jak to vevnitř funguje.


## Definice funkce

Protože už znáš `if` a `for`, které mají jednořádkovou hlavičku a odsazené tělo
příkazu, neměl by ti zápis funkce připadat příliš zvláštní:

```python
def zamen(slovo, pozice, novy_znak):
    """V daném slově zamění znak na dané pozici za daný nový znak."""
    zacatek = slovo[:pozice]
    konec = slovo[pozice + 1:]
    nove_slovo = zacatek + novy_znak + konec
    return nove_slovo

print(zamen('kočka', 1, 'a'))
print(zamen('kačka', 2, 'p'))
```

Jak to funguje?

Funkce se *definuje* příkazem `def`, za nějž napíšeš jméno funkce,
pak do závorky seznam *parametrů*, které funkce bere, a pak dvojtečku.

Potom následuje odsazené *tělo funkce* – příkazy, které funkce provádí.

Tělo může začít *dokumentačním řetězcem* (angl. *docstring*), který popisuje
co funkce dělá.
To může být jakýkoli řetězec, ale tradičně se uvozuje třemi uvozovkami
(i v případě že je jen jednořádkový).

Příkazem `return` pak můžeš z funkce *vrátit* nějakou hodnotu.

Při volání funkce se hodnoty, se kterými funkci
zavoláš, přiřadí jednotlivým parametrům.
Takže když zavoláš třeba `zamen('kočka', 1, 'a')`,
můžeš si představit, že se provede toto:

```python
# Nastavení proměnných podle zadaných argumentů
slovo = 'kočka'
pozice = 1
novy_znak = 'a'

# Samotné tělo funkce
zacatek = slovo[:pozice]
konec = slovo[pozice + 1:]
nove_slovo = zacatek + novy_znak + konec
return nove_slovo
```

Už víš, že volání `zamen('kočka', 1, 'a')` je výraz.
Aby ho Python vyhodnotil, udělá celý postup výše a jako hodnotu výrazu dosadí
návratovou hodnotu – tedy to, co následuje po `return`.

Tělo funkce může mít více příkazů – včetně podmínek, cyklů a podobně.
Následující procedura třeba vypíše skóre daného hráče a k tomu hlášku:

```python
def napis_hlasku(nazev, skore):
    """Popíše skóre. Název má být přivlastňovací přídavné jméno."""

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

## Cvičení

Zkus napsat funkci, která vrátí obsah obdélníka daných rozměrů.
Příslušný vzoreček je <var>S</var> = <var>a</var>×<var>b</var>,
kde <var>a</var> a <var>b</var> jsou délky stran.

Funkci zavolej a výsledek vypiš.

{% filter solution %}
```python
def obsah_obdelnika(a, b):
    return a * b

print('Obsah obdélníka se stranami 3 cm a 5 cm je', obsah_obdelnika(3, 5), 'cm2')
```
{% endfilter %}


## Vracení ukončuje funkci

Speciální příkaz `return`, který jde použít jenom ve funkcích, vrátí danou
návratovou hodnotu ven z funkce a zároveň *ukončí* provádění funkce.

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
     """Vrátí True nebo False podle odpovědi uživatele"""
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


### Vrátit nebo vypsat?

Podívejme se teď na následující program, který vypíše obsah elipsy:

```python
from math import pi

def obsah_elipsy(a, b):
    return pi * a * b

print('Obsah elipsy s poloosami 3 a 5 je', obsah_elipsy(3, 5), 'cm2')
```

Takový program se teoreticky dá napsat i s procedurou, tedy funkcí, která nic
nevrací.
Procedura může výsledek třeba vypsat na obrazovku:

```python
from math import pi

def obsah_elipsy(a, b):
    print('Obsah je', pi * a * b)  # Pozor, `print` místo `return`!

obsah_elipsy(3, 5)
```

Program takhle funguje, ale přichází o jednu z hlavních výhod funkcí:
možnost vrácenou hodnotu použít i jinak jež jen v `print`.

Funkci, která *vrací* výsledek, můžeš použít v dalších výpočtech:

```python
def objem_eliptickeho_valce(a, b, vyska):
    return obsah_elipsy(a, b) * vyska

print(objem_eliptickeho_valce(3, 5, 3))
```

... ale s procedurou, která výsledek přímo vypíše, by to nešlo.
Proto je dobré psát funkce, které spočítané hodnoty vrací,
a zpracování výsledku (např. vypsání) nechat na kód mimo funkci.

Další důvod proč hodnoty spíš vracet než vypisovat je ten, že jedna funkce se
dá použít v různých situacích.
Proceduru s `print` by nešlo rozumně použít tehdy, když nás příkazová
řádka vůbec nezajímá – třeba v grafické hře, webové aplikaci, nebo pro ovládání
robota.

Podobně je to se vstupem: když použiju v rámci své funkce `input`, bude se
moje funkce dát použít jen v situacích, kdy je u počítače klávesnice a za ní
člověk.
Proto je lepší funkcím potřebné informace předávat jako argumenty
a volání `input` (nebo čtení textového políčka či měření čidlem robota)
nemít ve funkci, ale vně, v kódu, který funkci volá:

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

Samozřejmě existují výjimky: procedura, která přímo vytváří textový výpis
(např. tabulku), může používat `print`; funkce, která načítá textové informace
(jako `ano_nebo_ne` výše), zase `input`.
Když ale funkce něco *počítá*, nebo když si nejsi jist{{gnd('ý', 'á')}},
je dobré ve funkci `print` ani `input` nemít.


## None

Když funkce neskončí příkazem `return`,
automaticky se vrátí hodnota `None`.

Je to hodnota zabudovaná přímo do Pythonu, podobně jako `True` nebo `False`,
a znamená „nic“.

```python
def nic():
     """Tahle funkce nic nedělá """

print(nic())
```

Procedury v Pythonu vracejí právě toto „nic“.
