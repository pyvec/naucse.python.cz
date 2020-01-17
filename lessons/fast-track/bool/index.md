# Porovnávání věcí

Programátoři často porovnávají různé hodnoty. Pojďme se podívat jak na to.

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
>>> 5 > 3 * 2
False
```

„Větší než“ a „menší než“ jsou značky známé z matematiky.
Chceš-li se ale zeptat, jestli jsou dvě čísla stejná, je potřba použít
trochu jiný zápis:

``` pycon
>>> 1 == 1
True
```

Jedno rovnítko `=` používáme pro *přiřazení* hodnoty do proměnné.
Když chceš zkontrolovat, jestli se věci navzájem *rovnají*, vždy, **vždy**
musíš dát dvě rovnítka `==`.

Další možnosti porovnávání jsou nerovnost (≠), větší nebo rovno (≤)
a meší nebo rovno (≥).
Většina lidí tyhle symboly nemá na klávesnici, a tak Python používá `!=`, `<=`
a `>=`.

``` pycon
>>> 5 != 2
True
>>> 3 <= 2
False
>>> 6 >= 12 / 2
True
```

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

Co se stane, když v minulé ukázce zaměníš `>` za `==`?

{% filter solution %}
```pycon
>>> 1 == 'krajta'
False
```

Jablka a hrušky nemůžeš porovnávat, ale můžeš si potvrdit že jsou to dvě různé
věci.
{% endfilter %}


## Logika

Chceš zkusit ještě něco? Zadej tohle:

``` pycon
>>> 6 > 2 and 2 < 3
True
>>> 3 > 2 and 2 < 1
False
>>> 3 > 2 or 2 < 1
True
>>> not 3 > 2
False
```

V Pythonu můžeš zkombinovat několik porovnání do jednoho!

*   Pokud použiješ operátor `and`, obě strany musí být pravdivé, aby byl celý výraz pravdivý.
*   Pokud použiješ operátor `or`, stačí aby jen jedna strana z porovnání byla pravdivá.
*   Operátor `not` “obrátí” výsledek porovnání.


## Přítomnost

Nebylo by pěkné zjistit, jestli tvoje číslo vyhrálo v loterii?
Máš-li seznam, operátorem `in` se můžeš zeptat, jestli je v něm daný prvek:

``` pycon
>>> loterie = [3, 42, 12, 19, 30, 59]
>>> 18 in loterie
False
>>> 42 in loterie
True
```

Není to úplně porovnání, ale dostaneš stejný druh výsledku jako s `<` či `==`.


## Pravdivostní hodnoty

Právě ses dozvěděl{{a}} o novém typu objektu v Pythonu.
Už známe typy řetězc, číslo, seznam nebo slovník; přidali jsme k nim
*pravdivostní hodnotu*, nebo častěji anglicky *boolean*.

Pravdivostní hodnoty jsou jenom dvě: `True` (pravda) nebo `False` (nepravda).

Aby Python pochopil, že se jedná o tento typ,
je potřeba dávat pozor na velikost písmen.
`true`, `TRUE`, `tRUE` nebude fungovat – jedině `True` je správně.

Jako každou hodnotu, i *boolean* můžeš uložit do proměnné:

``` pycon
>>> a = True
>>> a
True
```

Stejně tak můžeš uložit i výsledek porovnání:

``` pycon
>>> a = 2 > 5
>>> a
False
```

A všechno to můžeš použít v logických výrazech:

``` pycon
>>> a and True
False
```



## Shrnutí

V této sekci ses dozvěděl{{a}}:

*   V Pythonu můžeš **porovnávat** pomocí operátorů `>`, `>=`, `==` `<=`, `<`, `!=` a `in`
*   Operátory `and` a `or` umí **zkombinovat** dvě pravdivostní hodnoty.
*   Operátor `not` umí **obrátit** pravdivostní hodnotu.
*   **Boolean** (pravdivostní hodnota) je typ, který může mít jednu ze dvou
    hodnot: `True` (pravda) nebo `False` (nepravda).
