# Import a náhoda

V Pythonu je spousta funkčnosti k dispozici přímo – funkce jako `print`, `len`
nebo `int` můžeš rovnou použít.
Ještě víc věcí je v Pythonu sice k dispozici, ale jen když si „o ně řekneš“.
Jsou sdružené do *modulů* – souborů funkcí (a dalších věcí), které spolu nějak
souvisí.

Například když chceme pracovat s náhodnými hodnotami, můžeš využít modul
`random`.
Naimportuj z něj funkci `randrange`:

```pycon
>>> from random import randrange
```

Jakmile to uděláš, funkce `randrange` ti bude k dispozici.
Můžeš ji zavolat, a dostat tak náhodné číslo:

```pycon
>>> randrange(6)
3
>>> randrange(6)
1
>>> randrange(6)
2
>>> randrange(6)
4
>>> randrange(6)
5
>>> randrange(6)
3
>>> randrange(6)
0
>>> randrange(6)
3
>>> randrange(6)
1
```

Argument funkce `randrange` udává, kolik možných výsledků může vrátit.
Funkce pak vrací čísla od nuly, takže `randrange(6)` může vrátit od 0, 1, 2,
3, 4 nebo 5. Šestku už ne.


## Náhoda a seznamy

Naimportuj si ještě dvě funkce:

```pycon
>>> from random import choice, shuffle
```

První z nich, `choice`, umí vybrat náhodný prvek ze seznamu:

```pycon
>>> loterie = [3, 42, 12, 19, 30, 59]
>>> choice(loterie)
12
>>> choice(loterie)
30
```

Druhá, `shuffle`, umožní seznam náhodně zamíchat.
Podobně jako metoda `sort`, `shuffle` nic nevrací – jen potichu změní pořadí:

```pycon
>>> loterie = [3, 42, 12, 19, 30, 59]
>>> shuffle(loterie)
>>> loterie
[12, 59, 19, 42, 3, 30]
>>> shuffle(loterie)
>>> loterie
[59, 3, 30, 19, 12, 42]
```

## Shrnutí

Tohle byla docela krátká sekce – ale důležitá!

* **Import** nám může zpřístupnit funkce z **modulů**,
  které nejsou k dispozici přímo v Pythonu.
* Modul `random` obsahuje funkce na výběr náhodných čísel nebo náhodných
  prvků ze seznamu.
