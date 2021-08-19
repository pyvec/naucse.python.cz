# Ulož to!

Zatím jsi psal{{a}} všechny programy v konzoli v interaktivním režimu Pythonu,
který nás omezuje na jeden řádek kódu.
Když Python opustíš (nebo vypneš počítač),
všechno co jsi zatím naprogramoval{{a}} se ztratí.

Větší programy jsou trvanlivější: ukládají se do souborů a dají se kdykoli
spustit znovu.

Vyzkoušejme si to. Budeme potřebovat:

*   Ukončit interaktivní režim Pythonu
*   Otevřít editor kódu
*   Uložit kód do nového souboru
*   Spustit kód ze souboru!

Zkus vypnout Python. Existuje na to funkce `exit()`:

``` pycon
>>> exit()
```

Tak se dostaneš zpět do příkazové řádky. Pamatuješ na ni?
Už neuvidíš `>>>`, ale řádek končící `$` nebo `>`.
Budou tu fungovat příkazy jako `cd` a `mkdir`,
ale ne příkazy Pythonu, jako `1 + 1`.


Doufám, že máš nainstalovaný [textový editor](../../beginners/install-editor/).
Ten teď otevři, udělej si nový soubor a napiš do něj tento příkaz:

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
> ale nyní bys měla vidět, že jméno funkce `print` je jinou barvou než
> řetězec v závorkách.
> Barvy nevolíš {{gnd('sám', 'sama')}}, vybírá je editor na základě toho,
> jak potom Python kódu porozumí.
>
> Nazývá se to "zvýrazňování syntaxe" a je to užitečná funkce.
> Chce to trochu praxe, ale barvy můžou napovědět
> že ti chybí uvozovka za řetězcem
> nebo máš překlep v klíčovém slově jako `del`.
> To je jeden z důvodů, proč používáme editory kódu :)

Pokud máš soubor uložen, je čas jej spustit!
Pomocí dovedností, které jsi se naučil{{a}} v sekci
o příkazové řádce, *změň adresář* na ten, kam jsi soubor uložil{{a}}.

{% if var('coach-present') %}
Pokud nevíš jak dál, požádej o pomoc kouče.
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


## Vstup a výstup

Funkce `print()`, kterou jsi použil{{a}}, umí něco *vypsat* na obrazovku.
V konzoli se hodnoty výrazů vypisovaly automaticky, abys je mohl{{a}}
průběžně kontrolovat, ale programy v souborech bývají složitější a výpisy
z každého kroku by byly nepřehledné.
Proto na vypsání potřebuješ `print()`.
Zkus si to:

``` python
jmeno = 'Ola'

'Já jsem ' + jmeno  # Tohle Python nevypíše

print(jmeno * 8)    # Tohle jo!
```

Do závorek funkce `print()` můžeš dát i víc hodnot oddělených čárkami.

``` python
jmeno = 'Amálka'
vek = 5
print('Já jsem', jmeno, 'a je mi', vek)

print('Za rok mi bude', vek + 1)
```

Další užitečná funkce je `input()`, která se umí zeptat na otázku.
Odpověď pak vrátí jako řetězec, který si můžeš uložit do proměnné:

``` python
jmeno = input('Jak se jmenuješ? ')

print(jmeno, 'umí programovat!')
```

A co když budeš chtít spíš číslo než text?
Pamatuješ si na funkci, která umí převést řetězec na číslo?

``` python
letopocet = int(input('Jaký je letos rok? '))

print('Loni byl rok', letopocet - 1)
```


## Komentáře

Všiml{{a}} sis u předchozího programu poznámek za „mřížkou“ (`#`)?

``` python
jmeno = 'Ola'

'Já jsem ' + jmeno  # Tohle Python nevypíše

print(jmeno * 8)    # Tohle jo!
```

To jsou takzvané *komentáře*.
Jsou určené jen pro lidi: Python je úplně ignoruje.

Teď, když své programy ukládáš na disk a můžeš se k nim vracet,
je důležité aby byly *čitelné*: aby z nich nejen počítače, ale i lidi
poznali, co mají dělat.
Vždycky když napíšeš nějaký složitější kus kódu k němu zkus přidat komentář
s vysvětlivkou.
Až se k programu za pár dní nebo měsíců vrátíš, poděkuješ si!


## Shrnutí

* Příkaz **python** pustí uložený soubor jako program v Pythonu.
* Funkce **print** vypisuje hodnoty.
* **Komentáře** můžou zpřehlednit složitější kód. Python je ignoruje.
