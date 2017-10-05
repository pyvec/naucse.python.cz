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
tečky – podobně jako třeba k metodám, které nabízí
řetězce (či jiné objekty).

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
Funkce, které v něm nadefinuješ, a proměnné,
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

## Adresář pro každý projekt

Od teď budeme občas psát větší projekty,
které budou obsahovat více souvisejících souborů.
Je dobré pro každý takový projekt udělat
zvláštní adresář.

(A to samozřejmě znamená i zvláštní gitový repozitář.)
