# Moduly

Modul je v Pythonu něco, z čeho můžeme importovat.
Třeba z modulu `math` můžeš importovat funkci `sqrt`:

```python
from math import sqrt

print(sqrt(2))
```

Kromě importování jednotlivých proměnných z modulu
můžeš importovat i celý modul najednou.
K tomu, co modul nabízí, se pak dostaneš pomocí
tečky – podobně jako se pomocí `'Ahoj'.upper` dostaneš k metodě, kterou nabízí
řetězec.

Například:

```python
import turtle

turtle.left(90)
turtle.color('red')
turtle.forward(100)
turtle.exitonclick()
```

```python
import math

print(math.cos(math.pi))
```

> [note] Hvězdičky nechceme
>
> Možná jsi v dokumentaci nebo na jiném kurzu viděl{{a}} příkaz import
> s hvězdičkou (`*`).
> Pokud ano, v rámci tohoto kurzu na hvězdičku prosím
> zapomeň a importuj místo toho radši celý modul.
> Až začneš psát větší programy, zjednoduší ti
> to práci.


## Vlastní moduly

A teď to hlavní!
Můžeš vytvořit vlastní importovatelný modul
a to jen tak, že uděláš pythonní soubor.
Funkce, které v něm nadefinuješ, a globální proměnné,
které v něm nastavíš, pak budou k dispozici tam, kde modul naimportuješ.

Zkus si to!
Vytvoř soubor `louka.py` a do něj napiš:

```python
barva_travy = 'zelená'
pocet_kotatek = 28

def popis_stav():
    return 'Tráva je {barva}. Prohání se po ní {pocet} koťátek'.format(
        barva=barva_travy, pocet=pocet_kotatek)
```


A pak v dalším souboru, třeba `vypis.py`, napiš:

```python
import louka

print(louka.popis_stav())
```

a pak spusť:

```console
$ python vypis.py
```

Příkaz `import` hledá soubory (mimo jiné) v adresáři,
ve kterém je „hlavní modul” programu – tedy soubor,
který spouštíš (u nás `vypis.py`).
Oba soubory by proto měly být ve stejném adresáři.


## Vedlejší efekty

Co přesně dělá příkaz `import louka`?

Python najde příslušný soubor (`louka.py`) a provede v něm všechny příkazy,
odshora dolů, jako v normálním Pythonním programu.
Všechny globální proměnné (včetně nadefinovaných funkcí) pak dá k dispozici
kódu, který „louku“ importoval.

Když pak stejný modul importuješ podruhé, už se neprovádí všechno
znovu – stejná sada proměnných se použije znovu.

Zkus si to – na konci `louka.py` dopiš:

```python
print('Louka je zelená!')
```

Spusť `python` (máš-li ho už spuštěný, ukonči a spusť znovu)
a zadej v něm:

```pycon
>>> print('První import:')
>>> import louka
>>> print('Druhý import:')
>>> import louka
```

Výpis se objeví jen poprvé.

Když takhle modul při importu „dělá“ něco víc, než jen nastavuje proměnné
a funkce, říká se, že má *vedlejší efekt* (angl. *side effect*).
Vedlejší efekt může být vypsání něčeho na obrazovku nebo do souboru,
vykreslení okýnka na obrazovku, otázka na uživatele pomocí `input`, atp.

V modulech připravených na importování se vedlejším efektům vyhýbáme:
úloha takového modulu je dát k dispozici *funkce*, které něco dělají,
ne to udělat přímo.
Všimni si například, že `import turtle` neukáže okýnko – to se objeví až po
zavolání `turtle.forward()`.

Příkaz `print` proto radši z modulu zase smaž.


## Adresář pro každý projekt

Od teď budeš občas psát větší projekty,
které budou obsahovat více souvisejících souborů.
Pro každý takový projekt si udělej zvláštní adresář.
Lépe se pak vyznáš v tom, ke kterému projektu který soubor patří.
