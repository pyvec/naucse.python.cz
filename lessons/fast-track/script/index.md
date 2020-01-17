# Ulož to!

Zatím jsi psal{{a}} všechny programy v konzoli v interaktivním režimu Pythonu,
ve kterém Python vždy po napsání příkazu odpověděl výsledkem.
Když Python opustíš (nebo vypneš počítač),
všechno co jsi zatím naprogramoval{{a}} se ztratí.

Větší programy jsou trvanlivější: ukládají se do souborů a dají se kdykoli
spustit znovu.

Je čas si to vyzkoušet. Budeš potřebovat:

1. Ukončit interaktivní režim Pythonu
2. Otevřít editor kódu
3. Uložit kód do nového souboru
4. Spustit kód ze souboru!

Jako první krok vypni Python. Existuje na to funkce `exit()`:

``` pycon
>>> exit()
```

Tak se dostaneš zpět do příkazové řádky. Pamatuješ na ni?
Už neuvidíš `>>>`, ale řádek končící `$` nebo `>`.
Budou tu fungovat příkazy jako `cd` a `mkdir`,
ale ne příkazy Pythonu, jako `1 + 1`.


Doufám, že máš nainstalovaný [textový editor](../../beginners/install-editor/).
Ten teď otevři, udělej si nový soubor a do něj napiš tento příkaz:

```python
print('Hello, PyLadies!')
```

Nový soubor ulož pod nějakým popisným názvem: `python_intro.py`.
Ulož si jej do adresáře, kam si budeš dávat soubory k tomuto workshopu.
Jméno musí končit na `.py`: tahle přípona říká editoru nebo i
operačnímu systému, že jde o program v Pythonu a Python ho může spustit.

> [note] Obarvování
> Po uložení by se text měl obarvit.
> V interaktivním režimu Pythonu mělo vše stejnou barvu,
> ale nyní bys měla vidět, že jméno funkce `print` je vysázeno jinou barvou než
> řetězec v závorkách.
> Barvy nevolíš {{gnd('sám', 'sama')}}, vybírá je editor na základě toho,
> jak potom Python kódu porozumí.
>
> Nazývá se to "zvýrazňování syntaxe" a je to užitečná funkce.
> Chce to trochu praxe, ale barvy můžou napovědět
> že ti chybí uvozovka za řetězcem
> nebo máš překlep v klíčovém slově jako `del`.
> To je jeden z důvodů, proč používáme programátorské editory :)

Pokud máš soubor uložen, je čas jej spustit!
Pomocí dovedností, které jsi se naučil{{a}} v sekci
o příkazové řádce, *změň adresář* na ten, kam jsi soubor uložil{{a}}.
{% if var('coach-present') -%}
(Pokud nevíš jak dál, požádej o pomoc kouče.)
{% endif %}

Nyní pomocí Pythonu spusť kód v souboru: zadej příkaz `python`, mezeru
a jméno souboru ke spuštění.
(Je to podobné jako příkaz `cd` pro konkrétní adresář –
<code>cd <var>jmeno_adresare</var></code>.)

``` console
(venv) $ python python_intro.py
Hello, PyLadies!
```

Funguje? Vidíš text?
Jesli ano, právě jsi spustil{{a}} svůj první opravdový program v Pythonu!
Cítíš se úžasně?


## Výstup

Funkce `print()`, kterou jsi použil{{a}}, umí něco *vypsat* na obrazovku.
V konzoli se hodnoty výrazů vypisovaly automaticky, abys je mohl{{a}}
průběžně kontrolovat, ale programy v souborech bývají složitější a výpisy
z každého kroku by byly nepřehledné.
Proto na vypsání potřebuješ `print()`.
Zkus si s následujícím programem:

``` python
jmeno = 'Ola'

'Já jsem ' + jmeno  # Tohle Python nevypíše

print(jmeno * 8)    # Tohle jo!
```

Pak program spusť:

``` console
(venv) $ python python_intro.py
OlaOlaOlaOlaOlaOlaOlaOla
```

Co se stalo?
Když spustíš soubor s programem, Python jej prochází odshora dolů a postupně,
řádek po řádku, plní jednotlivé příkazy:
* proměnnou `jmeno` nastaví na řetězec `'Ola'`,
* spojí řetězce `'Já jsem '` a `'Ola'`, ale výsledek zahodí,
* zopakuje řetězec `'Ola'` osmkrát a výsledek vypíše pomocí `print()`.

Do závorek funkce `print()` můžeš dát i víc hodnot oddělených čárkami.
Zkus obsah souboru změnit na následující program a znovu ho spustit:

``` python
jmeno = 'Amálka'
vek = 5
print('Já jsem', jmeno, 'a je mi', vek)

print('Za rok mi bude', vek + 1)
```

## Vstup

Další užitečná funkce je `input()`, která se umí zeptat na otázku.
Odpověď pak vrátí jako řetězec, který si můžeš uložit do proměnné:

``` python
jmeno = input('Jak se jmenuješ? ')

print(jmeno, 'umí programovat!')
```

Když program spustíš, zeptá se na otázku.
Tu zadej na klávesnici *přímo do příkazové řádky*.
Python ji načte a použije jako výsledek funkce `input`,
který uloží do proměnné `jmeno`.
A v rámci dalšího řádku programu ho vytiskne.

``` console
(venv) $ python python_intro.py
Jak se jmenuješ? Ola
Ola umí programovat!
(venv) $ python python_intro.py
Jak se jmenuješ? Princezna
Princezna umí programovat!
```

Funkce `input()` z klávesnice vždycky načítá text: když uživatel zadá `1234`,
Python to bere jako řetězec číslic 1, 2, 3, 4.

Když budeš chtít z klávesnice načíst spíš číslo než text, musíš použít funkci,
která umí převést řetězec na číslo:

``` python
letopocet = int(input('Jaký je letos rok? '))

print('Loni byl rok', letopocet - 1)
```


## Komentáře

Všiml{{a}} sis u jednoho z předchozích programu poznámek za „mřížkou“ (`#`)?

``` python
jmeno = 'Ola'

'Já jsem ' + jmeno  # Tohle Python nevypíše

print(jmeno * 8)    # Tohle jo!
```

To jsou takzvané *komentáře*.
Jsou určené jen pro lidi: Python je úplně ignoruje.

Teď, když své programy ukládáš na disk a můžeš se k nim vracet,
je důležité aby byly *čitelné*: aby z nich nejen počítače, ale i lidi
poznali, co mají ty instrukce dělat.
Vždycky když napíšeš nějaký složitější kus kódu k němu zkus přidat komentář
s vysvětlivkou.
Až se k programu za pár dní nebo měsíců vrátíš, poděkuješ si!


## Shrnutí

* Příkaz **python** pustí uložený soubor jako program v Pythonu.
* Funkce **print** vypisuje hodnoty.
* Funkce **input** načítá řetězce, které uživatel zadá na klávesnici.
* **Komentáře** můžou zpřehlednit složitější kód. Python je ignoruje.
