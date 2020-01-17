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

Tak, a máš seznam! Co s ním ale můžeš dělat?
Podívej se, kolik čísel v seznamu je.
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

Tato metoda nic nevrátí, ale „potichu“ změní pořadí čísel v seznamu.
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

## Přidávání do seznamu

Podobně jako u řetězců se seznamy dají spojovat pomocí `+`:

``` pycon
>>> loterie + [5, 6, 7, 8]
[59, 42, 30, 19, 12, 3, 5, 6, 7, 8]
```

Tím se vytvoří nový seznam, ten původní zůstává nezměněný:

``` pycon
>>> loterie
[59, 42, 30, 19, 12, 3]
```

Pokud chceš něco přidat do původního seznamu, můžeš to provést pomocí metody
`append`.
Ale pozor! Tahle metoda potřebuje vědět co má do seznamu přidat.
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


## Odstraňování

Chceš-li ze seznamu něco odstranit, můžeš opět použít indexy.
Tentokrát s příkazem `del`.
Následujícím kódem odstraň počáteční číslo seznamu, tedy prvek číslo 0:

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

Občase se stane, že nechceš smazat prvek podle pozice, ale podle toho,
co v seznamu je.
K tomu slouží hodnota `remove`, která najde a odstraní danou hodnotu:

```pycon
>>> loterie
[42, 3]
>>> loterie.remove(3)
>>> loterie
[42]
```


## Řezání

Ze seznamu se dá kromě jednoho prvku vybrat i prvků několik – část seznamu,
takzvaný *podseznam*.

Udělej si opět delší seznam čísel:

``` pycon
>>> cisla = ["První", "Druhý", "Třetí", "Čtvrtý"]
```

Budeš-li chtít vybrat prvky od druhého dál, dej do hranatých závorek číslo
tohohle prvku, a za něj dvojtečku.

``` pycon
>>> cisla[1]
'Druhý'
>>> cisla[1:]
['Druhý', 'Třetí"', 'Čtvrtý']
```

Vybráním podseznamu se seznam nemění, tak můžeš vybírat dál:

```pycon
>>> cisla
['První', 'Druhý', 'Třetí', 'Čtvrtý']
>>> cisla[1:]
['Druhý', 'Třetí"', 'Čtvrtý']
>>> cisla[2:]
['Třetí', 'Čtvrtý']
>>> cisla[3:]
['Čtvrtý']
>>> cisla[4:]
[]
```

Budeš-li chtít vybrat prvky od začátku *až po* některý prvek, dej dvojtečku
*před* číslo prvku, který už ve výsledku nechceš


``` pycon
>>> cisla[2]
'Třetí'
>>> cisla[:2]
['První', 'Druhý']
```

Úkol: máš-li nějaký seznam, jak z něj vybereš všechny prvky kromě posledního?

{% filter solution %}
Poslední číslo má index -1, vyberu tedy prvky do -1:

``` pycon
>>> cisla[:-1]
['První', 'Druhý', 'Třetí']
```

Taky v zápisu pro vybrání všeho kromě posledního prvku vidíš smajlík?
\[:-1]

{% endfilter %}

Začátek a konec se dá kombinovat – číslo můžeš dát před i za dvojtečku:

```pycon
>>> cisla
['První', 'Druhý', 'Třetí', 'Čtvrtý']
>>> cisla[1:-1]
['Druhý', 'Třetí']
```

Řezání funguje i pro příkaz `del`.
Zkus vymazat prostřední dvě čísla:

``` pycon
>>> cisla
['První', 'Druhý', 'Třetí', 'Čtvrtý']
>>> del cisla[1:-1]
>>> cisla
['První', 'Čtvrtý']
```


## Řezání řetězců

Hranaté závorky fungují i u řetězců, kde vybírají písmenka:

``` pycon
>>> jidlo = 'čokoláda'
>>> jidlo[3]
'o'
>>> jidlo[1:4]
'oko'
```

Řetězce se ale nedají měnit: `del`, `sort` nebo `append` fungují jen
na seznamech.

Úkol: Představ si, že máš v proměnné `jmeno` ženské jméno jako `'Ola'`,
`'Krystýna'` nebo `'Růžena'`.
Jak z něj vytvoříš druhý pád (např. bez `'Růženy'`)?

{% filter solution %}
Vezmi jméno až po poslední písmeno a přidej `'y'`. Například:
``` python
>>> jmeno = 'Růžena'
>>> jmeno[:-1] + 'y'
'Růženy'
>>> jmeno = 'Krystýna'
>>> jmeno[:-1] + 'y'
'Krystýny'
```
{% endfilter %}


## Shrnutí

Uf! O seznamech toho bylo k naučení celkem hodně. Shrňme si, co už umíš:

* **Seznam** je seřazená sekvence hodnot.
* Pomocí **metod** se seznam dá řadit (`sort`) a obrátit (`reverse`),
  nebo se do něj dá přidat (`append`) či odebrat (`remove`) prvek.
* Prvky se dají **vybrat** nebo **odstranit** (`del`) podle indexu.
* Číslování začíná **od nuly**, záporná čísla berou prvky od konce.
* **Podseznam** je určitá část seznamu.
* U **řetězců** funguje vybírání prvků a podřetězců podobně

Jsi připraven{{a}} na další část?
