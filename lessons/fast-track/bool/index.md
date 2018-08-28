# Porovnávání věcí

Programátoři často porovnávají různé hodnoty. Pojďme se podívat, jak na to.

``` pycon
>>> 5 > 2
True
>>> 5 > 8
False
>>> 5 < 8
True
```

Když se Pythonu zeptáš, jestli je jedno číslo větší než druhé, odpoví ti
`True` (pravda) nebo `False` (nepravda).

Funguje to i se složitějšími výrazy:

``` pycon
>>> 5 > 2 * 2
True
```

„Větší než“ a „menší než“ používají značky známé z matematiky.
Chceš-li se ale zeptat, jestli jsou dvě čísla stejná, je to trochu jiné:

``` pycon
>>> 1 == 1
True
```

Jedno rovnítko `=` používáme pro přiřazení hodnoty do proměnné.
Když chceš zkontrolovat, jestli se věci navzájem rovnají, vždy, **vždy** musíš dát dvě rovnítka `==`.

Další možnosti porovnávání jsou nerovnost (≠), větší než (≤) a meší než (≥).
Většina lidí tyhle symboly nemá na klávesnici, a tak se používá `!=`, `<=`
a `>=`.

``` pycon
>>> 5 != 2
True
>>> 3 <= 2
False
>>> 6 >= 12 / 2
True
```

## Logika

Chceš zkusit ještě něco? Zkus tohle:

``` pycon
>>> 6 > 2 and 2 < 3
True
>>> 3 > 2 and 2 < 1
False
>>> 3 > 2 or 2 < 1
True
```

V Pythonu můžeš zkombinovat několik porovnání do jednoho!

*   Pokud použiješ operátor `and`, obě strany musí být pravdivé, aby byl celý výraz pravdivý.
*   Pokud použiješ operátor `or`, stačí aby jen jedna strana z porovnání byla pravdivá.

Už jsi někdy slyšel{{a}} výraz „srovnávat jablka a hrušky“? Zkusme v Pythonu ekvivalent:

``` pycon
>>> 1 > 'krajta'
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: '>' not supported between instances of 'int' and 'str'
```

Stejně jako nelze srovnávat „jablka a hrušky“,
Python není schopen porovnávat řetězce (`str`) a čísla (`int`).
Místo toho zobrazí `TypeError` a říká nám, že tyto dva typy nelze porovnat.


## Pravdivostní hodnoty

Mimochodem, právě ses dozvěděl{{a}} o novém typu objektu v Pythonu.
Říká se mu *pravdivostní hodnota*, nebo častěji anglicky *boolean*.

Může mít jednu z dvou hodnot: `True` a `False`.

Aby Python pochopil, že se jedná o tento typ,
je potřeba dávat pozor na velikost písmen.
`true`, `TRUE`, `tRUE` nebude fungovat – jedině `True` je správně.

Jako každou hodnotu, i pravdivostní hodnotu můžeš uložit do proměnné:

``` pycon
>>> a = True
>>> a
True
```

Stejně tak můžeš uložit i výsledek porovnání:

```
>>> a = 2 > 5
>>> a
False
```
