# Ulož to!

Zatím jsi psal{{a}} všechny programy v konzoli v interaktivním režimu Pythonu,
který nás omezuje na jeden řádek kódu.
Když Python opustíš (nebo vypneš počítač),
všechno co jsi zatím naprogramoval{{a}}, se ztratí.

Větší programy jsou trvanlivější: ukládají se do souborů a dají se kdykoli
spustit znovu.

Vyzkoušejme si to. Budeme potřebovat:

*   Ukončit interaktivní režim Pythonu
*   Otevřít editor kódu
*   Uložit kód do nového souboru
*   Spustit ho!

Zkus vypnout Python. Existuje na to funkce `exit()`:

``` pycon
>>> exit()
```

Tak se dostaneš zpět do příkazové řádky.
Budou tu fungovat příkazy jako `cd` a `mkdir`,
ale ne příkazy Pythonu, jako `1 + 1`.

Chceš-li opustit interaktivní režim Pythonu, který jsme dosud používaly, jednoduše zadejte ~ ~ ~ exit() ~ ~ ~ funkci:


{# (((((((( XXX )))))))) #}
> [Note]
> Pokud budeš chtít Python konzoli ukončit, zadej `exit()` nebo použíj
> zkratku `Ctrl + D` (pro Mac/Linux) nebo `Ctrl + Z` (na Windows).
> Pak již neuvidíš `>>>`.


Tak se dostaneš zpět do příkazové řádky.

Doufám, že máš nainstalovaný textový editor.
Ten teď otevři a napiš do nového souboru tento příkaz:

```python
print('Hello, PyLadies!')
```

Teď vytvořený soubor ulož pod nějakým popisným názvem.
Pojďme ho nazvat `python_intro.py` a ulož si jej na plochu.
Soubor můžeš pojmenovat jakkoliv chceš, ale jméno musí končit na `.py`
Tahle přípona říká editoru nebo i operačnímu systému,
že jde o program v Pythonu a Python ho může spustit.

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
> nebo máš překlep v klíčovém slovu jako `del`.
> To je jeden z důvodů, proč používáme editory kódu :)

Pokud máš soubor uložen, je čas jej spustit!
Pomocí dovedností, které jsi se naučil{{a}} v sekci příkazová řádka,
*změň adresář* terminálu na plochu.

Na Macu bude příkaz vypadat přibližně takto:

``` console
(venv) $ cd ~/Desktop
```

Na Linuxu to bude vypadat takto (slovo "Desktop" (Plocha) může být
přeloženo třeba do češtiny):

``` console
(venv) $ cd ~/Desktop
```

A na Windows to bude vypadat takto:

``` doscon
(venv) > cd Desktop
```

Pokud nevíš jak dál, požádej o pomoc kouče.

Nyní pomocí Pythonu spusť kód v souboru:

``` console
(venv) $ python python_intro.py
Hello, PyLadies!
```

Funguje? Vidíš text?
Jesli ano, právě jsi spustil{{a}} svůj první opravdový program v Pythonu!
Cítíš se úžasně?

## Vstup a výstup

Funkce `print()`, kterou jsi použila, umí něco *vypsat* na obrazovku.
V konzoli se hodnoty výrazů vypisovaly automaticky, abys je mohl{{a}}
průběžně kontrolovat, ale programy v souborech bývají složitější a výpis
každého kroku by byl nepřehledný.
Proto na vypsání potřebuješ `print()`.
Zkus si to:

``` python
jmeno = 'Ola'

'Já jsem ' + jmeno  # Tohle Python nevypíše

print(jmeno * 8)    # Tohle jo!
```

Do závorek funkce `print()` můěš dát i víc hodnot oddělených čárkami.

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
