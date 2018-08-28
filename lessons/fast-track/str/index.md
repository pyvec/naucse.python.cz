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
Řetězec je programátorský termín pro *text* – posloupnost znaků (písmenek), které mohou být zpracovány počítačem.

Když řetězec zadáváš, musíš ho vždy uzavřít do uvozovek (apostrofů).
Jinak by Python nepoznal, co je text a co jsou instrukce.

{# XXX: Assessment here: adding strings together #}

Řetězce se dají spojovat – „sečítat“ – pomocí `+`. Zkus toto:

``` pycon
>>> 'Já jsem ' + 'Ola'
'Já jsem Ola'
```

> [note]
> Pozor na mezeru! Když zadáš `'Já jsem'+'Ola'`, spojí se ti dvě slova
> dohromady.
> Počítač považuje i mezeru za *znak*; chová se k ní stejně jako k jakémukoli
> písmenku.
> Když nedáš mezeru do uvozovek, nebude součástí řetězce.
>
> Zkus si:
>
> ``` pycon
> >>> 'Já jsem' + ' ' + 'Ola'
> 'Já jsem Ola'
> ```

Také můžeš řetězce opakovat – násobit číslem:

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

Už umíš řetězce „sčítat“ pomocí `+` (`'Ahoj ' + 'Olo!'`)
a „násobit“ pomocí `*` (`'la' * 3`).
Na všechny ostatní věci, které se s textem dají dělat,
ale na klávesnici není dost symbolů.
Proto jsou některé operace pojmenované slovně – třeba takzvané *funkce*.

Chceš-li znát počet písmen ve svém jméně, zavolej funkci `len`.
Napiš `len` (bez uvozovek), pak kulaté závorky, a do těch závorek
své jméno (jako řetězec – v uvozovkách):

``` pycon
>>> len('Ola')
3
```

{# XXX: Existuje funkce `type`. Jak bych ji zavolal? #}

Kromě funkcí existují *metody*, které se zapisují trochu jinak.

Chceš-li vidět své jméno velkými písmeny, zavolej metody `upper`.
Napiš řetězec, pak tečku, jméno metody `upper` (bez uvozovek) a prázdné
závorky:

``` pycon
>>> 'Ola'.upper()
'OLA'
```

Zkus si zavolat metodu `lower`.

{# XXX: Existuje funkce `type`. Jak bych ji zavolal? #}

Co je metoda (které voláš s `.`, jako `'Ola'.upper()`) a co je funkce
(kde vložíš informaci do závorek jako (`len('Ola')`)


{# XXX: Move elsewhere? #}
## Skládání

Volání funkce nebo metody můžeš použít jako jinou hodnotu.

Nech Python spočítat matematický výraz `(1 + 3) / 2`:

```pycon
>>> (1 + 3) / 2
2.0
```

Python napřed sečte `1 + 3` a vyjde mu 4.
Čtverku doplní místo `1 + 3` do původního příkladu, a dostane `4 / 2`.
To vydělí a dostane `2`.

Neboli: `(1 + 3) / 2` = `4 / 2` = `2`

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
týdnů – a pak je po celou svou progrmátorskou kariéru skládá do
složitějších a složitějších konstrukcí.

### Shrnutí

OK, dost bylo řetězců. Co ses zatím naučil{{a}}:

*   **Interaktivní režim Pythonu** umožňuje zadávat příkazy (kód) pro
    Python a zobrazuje výsledky/odpovědi.
*   **Čísla a řetězce** se používají na matematiku a práci s textem.
*   **Operátor** jako `+` a `*` kombinuje hodnoty a vytvoří výsledek.
*   **Funkce** a **metody** jako `len()` a `upper()` provádí na hodnotách
    nějaké akce.

Čísla, řetězce a operátory a funkce jsou základy většiny programovacích jazyků.

Připraven{{a}} na něco dalšího? Vsadíme se, že ano!
