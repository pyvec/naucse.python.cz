# Seznamy

Vedle řetězců a celých čísel má Python další druhy hodnot.

Teď se podíváme na jeden, který se nazývá *seznam* (anglicky *list*).
To je hodnota, která v sobě obsahuje jiné hodnoty.

{# Anglické termíny všude! #}

Seznamy se zadávají tak, že dáš několik hodnot, oddělených čárkami,
do hranatých závorek.
Zkus si vytvořit třeba seznam čísel z loterie:

``` pycon
>>> [3, 42, 12, 19, 30, 59]
[3, 42, 12, 19, 30, 59]
```

Abys s takovým seznamem mohl{{a}} pracovat,
ulož si ho do proměnné:

``` pycon
>>> loterie = [3, 42, 12, 19, 30, 59]
```

Dobrá, máme seznam! Co s ním můžeme dělat?
Podíváme se, kolik čísel v seznamu je.
Dá se na to použít funkce, kterou už znáš.
Tipneš si, která to je?

{% filter solution %}
``` pycon
>>> len(loterie)
6
```

Funkce `len()` umí zjistit nejen délku řetězce, ale i délku seznamu – tedy
počet jeho prvků.
{% endfilter %}

Teď si zkus seznam seřadit. Na to existuje metoda `sort`:

``` pycon
>>> loterie.sort()
```

Tato funkce nic nevrátí, jen změní pořadí čísel v seznamu.
Znovu si ho vypiš, ať vidíš co se stalo:

``` pycon
>>> loterie
[3, 12, 19, 30, 42, 59]
```

Čísla v seznamu jsou nyní seřazena od nejnižší k nejvyšší hodnotě.

Podobně funguje metoda `reverse`, která obrátí pořadí prvků.
Vyzkoušej si ji!

``` pycon
>>> loterie.reverse()
>>> loterie
[59, 42, 30, 19, 12, 3]
```

Pokud chceš do svého něco přidat seznamu, můžeš to provést pomocí metody
`append`.
Ale pozor! Tahle metoda potřebuje vědět co má do seznamu přidat
Nová hodnota se zadává do závorek:

``` pycon
>>> loterie.append(199)
```

Metoda opět nic nevrací, takže je potřeba seznam pro kontrolu vypsat:

``` pycon
>>> loterie
[59, 42, 30, 19, 12, 3, 199]
```

## Vybírání prvků

Když se budeš chtít na jednu věc ze seznamu podívat podrobněji,
přijde vhod možnost vybrat si konkrétní prvek.
Na to se v Pythonu používají hranaté závorky.

{# XXX: MCQ #}

Chceš-li vybrat prvek, zadej jméno seznamu a hned za ním hranaté závorky
s pořadovým číslem prvku, který chceš:

``` pycon
>>> loterie[1]
```

Dostaneš první prvek?

{% filter solution %}
``` pycon
>>> loterie
[59, 42, 30, 19, 12, 3, 199]
>>> loterie[1]
42
```

Ne, dostaneš druhý prvek.

Programátoři počítají od nuly.
Chceš li tedy první prvek, popros Python o prvek číslo nula:

``` pycon
>>> loterie[0]
42
```

Je to zpočátku divné, ale dá se na to zvyknout.
{% endfilter %}

Číslu prvku se také říká *index* a procesu vybírání prvků *indexování*.

Zkus si indexování s dalšími indexy: 3, 100, 7, -1, -2, -6 nebo -100.
Pokus se předpovědět výsledek před zadáním příkazu.
Jak ti to půjde?

{% filter solution %}
``` pycon
>>> loterie
[59, 42, 30, 19, 12, 3, 199]

>>> loterie[3]
19
```
Index 3 označuje čtvrtý prvek.

``` pycon
>>> loterie[7]
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
IndexError: list index out of range

```
Prvek s indexem 100 v seznamu není – nastane chyba.

``` pycon
>>> loterie[1000]
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
IndexError: list index out of range
```
Prvek s indexem 7 v seznamu taky není.

``` pycon
>>> loterie[-1]
199
```
Index -1 označuje *poslední* prvek.

``` pycon
>>> loterie[-2]
3
```
Index -2 označuje předposlední prvek.

``` pycon
>>> loterie[-6]
42
```
Index -6 označuje šestý prvek od konce.

``` pycon
>>> loterie[-100]
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
IndexError: list index out of range
```
Stý prvek od konce v seznamu není. Nastane chyba.
{% endfilter %}

## Řezání

XXX Slicing

## Odstraňování

Chceš-li ze seznamu něco odstranit, můžeš opět použít indexy.
Tentokrát s příkazem `del`.
Následující kód odstraní počáteční číslo seznamu, tedy prvek číslo 0:

``` pycon
>>> del loterie[0]
```

Pak si seznam opět vypiš. Kousek chybí!

``` pycon
>>> loterie
[42, 30, 19, 12, 3, 199]
```

Zkusíš odstranit poslední prvek?

{% filter solution %}
``` pycon
>>> del loterie[-1]
>>> loterie
[42, 30, 19, 12, 3]
```
{% endfilter %}

A co prostřední tři?
Zkus si nejdřív vypsat, které to jsou, a pak teprve použít `del`.

{% filter solution %}
``` pycon
>>> loterie
[42, 30, 19, 12, 3]
>>> loterie[1:-1]
[30, 19, 12]
>>> del loterie[1:-1]
>>> loterie
[42, 3]
```
{% endfilter %}
