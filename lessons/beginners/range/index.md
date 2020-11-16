# Range – sekvence čísel

Funkce `range(10)` vrátí speciální hodnotu,
která v sobě obsahuje čísla od 0 do 9:

```pycon
>>> sekvence = range(10)
>>> sekvence
range(0, 10)
```

Je to hodnota typu `range`, podobně jako čísla jsou typu `int`, řetězce typu
`str`, nebo seznamy typu `list`.

Chceš-li se podívat, co v tomhle `range(0, 10)` vlastně je, máš dvě základní
možnosti – projít ho cyklem `for` nebo převést na seznam konkrétních čísel:

```pycon
>>> sekvence
range(0, 10)
>>> for i in sekvence:
...     print(i)
0
1
2
3
4
5
6
7
8
9
>>> list(sekvence)
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
```

Možná se ptáš – proč tak složitě?
Proč se místo `range(0, 10)` prostě ta čísla neukážou rovnou?

Je to proto, že `range` se dá použít na opravdu dlouhé řady čísel:

```pycon
>>> range(10000)
range(0, 10000)
>>> list(range(10000))
[0, 1, 2, 3, ..., 9999]
```

Kdybys zkusil{{a}} třeba `list(range(1000000000000000))`, počítači
dojde paměť.
Biliarda čísel se tam prostě nevejde.
Python vyhodí výjimku  `MemoryError`.


> [warning]
> Pokud máš na počítači v jiném okně neuloženou práci, radši `list(range(...))`
> s hodně vysokými čísly nezkoušej.
>
> U absurdně vysokého čísla jako `1000000000000000` Python předem ví,
> že mu paměť dojde, a tak ohlásí chybu ještě než se bude snažit seznam vytvořit.
> U trochu menšího čísla (např. `1000000000`, ale na každém počítači je to
> jinak) se může stát, že se Python pokusí seznam začít tvořit, zaplní přitom
> většinu dostupné paměti a počítač „zamrzne“.
> V závislosti na systému se pak třeba může stát že reakce na
> <kbd>Ctrl</kbd>+<kbd>C</kbd> bude trvat hodně dlouho.

Se samotným `range(1000000000000000)` ale není problém.
S konceptem *všech čísel od 0 do biliardy* se počítač vypořádá, i když si je
neumí „zapamatovat“ všechny *najednou*.

Je spousta věcí, které Python umí s `range` udělat, aniž by potřeboval
„spočítat“ každé z čísel.
Spousta operací, které znáš od seznamů, bude fungovat i s `range`:

```pycon
>>> zajimava_cisla = range(8, 10000, 3)  # Každé třetí číslo od 8 do 9999
>>> zajimava_cisla[80]          # Osmdesáté "zajímavé číslo"
248
>>> zajimava_cisla[:5]          # Prvních 5 "zajímavých čísel"
range(8, 23, 3)
>>> list(zajimava_cisla[:5])    # Vypsání prvních 5 "zajímavých čísel"
[8, 11, 14, 17, 20]
>>> len(zajimava_cisla)         # Kolik tam je čísel?
3331
>>> 1337 in zajimava_cisla      # Je v této sekvenci moje konkrétní číslo ?
True
>>> zajimava_cisla.index(1337)  # Kolikáté je?
443
```

```pycon
>>> import random
>>> random.choice(zajimava_cisla)
1229
```

```pycon
>>> for i in zajimava_cisla:
...     print(i)
...     if i > 20:
...         break  # Stačilo!
8
11
14
17
20
23
```

Objekt `range` ale nejde měnit – mazání prvků nebo metody jako
`zajimava_cisla.sort()`, `zajimava_cisla.pop()` fungovat nebudou.

> [note] Proč ne?
> Když máš objekt jako `range(8, 10000, 3)`, osmdesátý prvek je jen trocha
> matematiky: spočítáš `8 + 3 * 80` a zkontroluješ že to nepřesáhlo `10000`.
> Podobně je to s ostatními sekvencemi „všech <var>X</var>-tých čísel od
> <var>A</var> do <var>B</var>“, tedy s ostatními `range`.
>
> Kdyby ale šlo udělat něco jako:
>
> ```python
> sekvence = range(8, 10000, 3)
> del sekvence[10]
> sekvence.insert(103, 'ježek')
> ```
>
> … jde najednou o mnohem složitější koncept, kde se N-tý prvek hledá mnohem
> hůř. Už to není jednoduchá sekvence čísel – už to není `range`, ale spíš
> seznam jakýchkoli hodnot.

Pokud budeš něco, co `range` neumí, potřebovat, převeď `range` na seznam.
