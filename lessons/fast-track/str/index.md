# Řetězce

Čísla jsou pro počítače dost užitečná (ostatně slovo *počítač* to naznačuje),
ale Python umí pracovat i s jinými druhy informací.
Třeba s textem.

Zkus si to: zadej své jméno do uvozovek, jak vidíš níže:

``` pycon
>>> 'Ola'
'Ola'
```

Nyní jsi vytvořil{{a}} svůj první *řetězec*!
Řetězec (angl. *string*) je programátorský termín pro *text* – posloupnost
znaků (písmenek),
které mohou být zpracovány počítačem.

Když řetězec zadáváš, musíš ho vždy uzavřít do uvozovek (apostrofů).
Jinak by Python nepoznal, co je text se kterým má pracovat a co jsou instrukce
které má provést.
To je pro počítač docela důležité – lidem podobné věci dojdou z kontextu,
ale počítač je hloupé zařízení.

{{ figure(
    img=static('quote-comic.svg'),
    alt='(Ilustrační komiks. Člověk říká robotovi: "Řekni Pavlovi, ať mi zavolá!". Robot odpoví: "PAVLOVI AŤ MI ZAVOLÁ!")',
) }}

Řetězce se dají spojovat – „sečítat“ – pomocí `+`. Zkus toto:

``` pycon
>>> 'Já jsem ' + 'Ola'
'Já jsem Ola'
```

Pozor na mezeru! Když zadáš `'Já jsem'+'Ola'`, spojí se ti dvě slova dohromady.
Počítač považuje i mezeru za *znak*; chová se k ní stejně jako k jakémukoli
písmenku.
Když nedáš mezeru do uvozovek, nebude součástí řetězce.

Zkus si dát do uvozovek i mezeru samotnou:

``` pycon
>>> 'Já jsem' + ' ' + 'Ola'
'Já jsem Ola'
```

Kromě „sečítání“ můžeš řetězce i opakovat – násobit číslem:

``` pycon
>>> 'Ola' * 3
'OlaOlaOla'
```

## Uvozování

A co když budeš chtít dát dovnitř do svého řetězce apostrof?
Můžeš kolem řetězce použít dvojité uvozovky:

``` pycon
>>> "To bych řek', že jsou pořádně praštěný!"
"To bych řek', že jsou pořádně praštěný!"
```

Pythonu je jedno, se kterým druhem uvozovek řetězec zadáš.
Podstatná jsou jen písmenka uvnitř.
Když Python řetězec vypisuje, může si vybrat jiný druh uvozovek
než jsi použil{{a}} ty:

``` pycon
>>> "Ola"
'Ola'
```

## Funkce a metody

Už umíš řetězce „sčítat“ (`'Ahoj ' + 'Olo!'`)
a „násobit“ (`'la' * 3`).
Na všechny ostatní věci, které se s textem dají dělat,
ale na klávesnici není dost symbolů.
Proto jsou některé operace pojmenované slovně – třeba takzvané *funkce*.

Chceš-li znát počet písmen ve svém jméně, zavolej funkci `len`.
Napiš `len` (bez uvozovek), pak kulaté závorky, a do těch závorek
své jméno jako řetězec (v uvozovkách):

``` pycon
>>> len('Ola')
3
```

Existuje funkce `type`, která zjistí jestli je něco číslo nebo řetězec.
Jak bych ji zavolal?

{% filter solution %}
``` pycon
>>> type(123)
<class 'int'>
>>> type('123')
<class 'str'>
```
{% endfilter %}

Kromě funkcí existují *metody*, které se zapisují trochu jinak.

Chceš-li vidět své jméno velkými písmeny, zavolej metodu `upper`.
Napiš řetězec, pak tečku, jméno metody `upper` (bez uvozovek) a prázdné
závorky:

``` pycon
>>> 'Ola'.upper()
'OLA'
```

Řetězce mají i metodu `lower`. Zkus ji zavolat na své jméno.

{% filter solution %}
``` pycon
>>> 'Ola'.lower()
'ola'
```
{% endfilter %}

Co je metoda (které voláš s tečkou, jako `'Ola'.upper()`) a co je funkce
(kde vložíš informaci do závorek jako `len('Ola')`),
to se budeš muset vždycky zapamatovat nebo vyhledat.


{# XXX: Move elsewhere? #}
## Skládání výrazů

Volání funkce nebo metody můžeš použít jako jinou hodnotu.

Nech Python spočítat matematický výraz `(1 + 3) / 2`:

```pycon
>>> (1 + 3) / 2
2.0
```

Python napřed sečte `1 + 3` a vyjde mu 4.
Čtverku doplní místo `1 + 3` do původního příkladu, a dostane `4 / 2`.
To vydělí a dostane `2.0`.

Neboli: `(1 + 3) / 2` = `4 / 2` = `2.0`

Zkus se zamyslet, jak Python zpracuje tyto výrazy:

```pycon
>>> len('Ola') + 1
4
```

```pycon
>>> 'Já jsem ' + 'Ola'.upper()
'Já jsem OLA'
```

```pycon
>>> len('Ola'.upper())
4
```

```pycon
>>> len('Ola' * 3)
9
```

{% filter solution() %}
`'Já jsem ' + 'Ola'.upper()` → `'Já jsem ' + 'OLA'` → `'Já jsem OLA'`

`len('Ola') + 1` → `3 + 1` → `4`

`len('Ola'.upper())` → `len('OLA')` → `3`

`len('Ola' * 3)` → `len('OlaOlaOla')` → `9`
{% endfilter %}


Podobné skládání je v programování velice časté.
Většinu základních stavebních bloků se začátečník naučí za pár
týdnů – a pak po celou svou progrmátorskou kariéru objevuje nové způsoby,
jak je poskládat do složitějších a složitějších konstrukcí.

### Shrnutí

OK, dost bylo řetězců. Co ses zatím naučil{{a}}:

*   **Řetězce** se používají na práci s textem.
*   **Operátory** `+` a `*` se používají na spojování a opakování řetězců.
*   **Funkce** a **metody** jako `len()` a `upper()` provádí na řetězcích
    nějaké akce.
*   **Výrazy** se dají skládat dohromady.

Čísla, řetězce a operátory a funkce jsou základy většiny programovacích jazyků.

Připraven{{a}} na něco dalšího? Vsadíme se, že ano!
