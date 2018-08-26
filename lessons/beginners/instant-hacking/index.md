## Interaktivní příkazová řádka Pythonu

Zkontroluj si, že máš aktivované virtuální prostředí (na začátku příkazové
řádky ti svítí `(venv)`).

Je-li tomu tak, nezbývá než – konečně – pustit Python.
K tomu použij příkaz `python`:

``` plain
(venv)$ python
Python 3.4.0 (default, Jan 26 2014, 18:15:05)
[GCC 4.8.2 20131212 (Red Hat 4.8.2-7)] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>>
```

Zkus napsat do příkazového řádku příkaz:

```
>>> print("Hello, world!")
```

Když stiskneš Enter, měl by se ti objevit nýsledující výstup:

```
Hello, world!
>>>
```

Pokud jste zvyklí z jiných programovacícj jazyků, že řádka musí být ukončena středníkem, pak v Pythonu to není zapotřebí.

Toto značí příkazový řádek:

```
>>>
```

Pokud do něj napíšeš řetězec v uvozovkách:

```
>>> "Hello world!"
```

dostaneš následující výstup:

```
'Hello world!'
>>>
```

Pokud ale zkusíš napsat podobný příkaz:

```
>>> Have fun!
  File "<stdin>", line 1
    Have fun!
           ^
SyntaxError: invalid syntax
>>>
```

Obdržíš chybové hlášení, že Python interpret nerozumí příkazu.

### Čísla a výrazy

Zkus následující příkazy:

```
>>> 2 + 2
4
```

Výsledkem sčítání je celé číslo. Pokud budeme dělit, výsledkem bude číslo s pohyblivou čárkou (floating-point number).


```
>>> 1 / 2
0.5
>>> 1 / 1
1.0
```

Pokud tě zajímá celočíselné dělení, zkus:

```
>>> 1 // 2
0
>>> 1 // 1
1
>>> 5.0 // 2.4
2.0
```

Operátor modulo:

```
>>> 1 % 2
1
```

Některé příklady celočíselného dělení a zbytku po celočíselném dělení:

```
>>> 10 // 3
3
>>> 10 % 3
1
>>> 9 // 3
3
>>> 9 % 3
0
```

Poslední operátor na který se podíváme je operátor exponenciální operátor:

```
>>> 2 ** 3
8
>>> -3 ** 2
-9
>>> (-3) ** 2
9
```

#### Hexadecimální, osmičkový a binární zápis čísel

```
>>> 0xAF
175
>>> 010
8
>>> 0b1011010010
722
```

> [note]
> V závislosti na verzi Pythonu se může stát, že osmičkový zápis čísel selže s chybou jako je náseldující:
> 
> ```
> >>> 0l0
>  File "<stdin>", line 1
>    0l0
>       ^
> SyntaxError: invalid syntax
> ```
>
>
> Pokud se to stane, budeš muset zadávat osmičkový zápis ve tvaru:
>
> ```
> >>> 0o10
> 8
> ```
> Jedná se o změnu v Python3, popsanou v [PEP-3127](http://www.python.org/dev/peps/> pep-3127/)

### Proměnné

Pokud máš alespoň malé zkušenosti s programováním, je ti asi známý koncept *proměnných (variables)*. Proměnná reprezentuje nějakou hodnotu. Touto hodnotou může být řetězec, číslo atd. Přiřadit hodnotu do proměnné můžeme v Pythonu snadno takto:

```
>>> x = 2
```

Poté, co přiřadíme proměnné nějakou hodnotu, můžeme proměnnou použít v dalším kódu:

```
>>> x * 2
4
```

>[note]
>
> Jméno proměnné může obsahovat písmena, čísla a znak podržítka (_). Nemůžou začínat číslem, takže proměnná s názvem **variable1** je validní, ale **1variable** už ne.
>


### Příkazy

Rozdíl mezi výrazy a příkazy je následující, zatímco výraz *je* něco, příkaz *dělá* něco. Například výraz 3 \* 3 *je* 9:

```
>>> 3 * 3
9
```

ale příkaz print(3 \* 3) *vytiske* hodnotu 9.

```
print(3 * 3)
9
```

### Získání vstupu od uživatele

Pokud potřebuješ v programu získat od uživatele nějakou vstupní hodnotu, můžeš použít funkci input.

```
>>> input('Zadejte velikost vasich bot: ')
Zadejte velikost vasich bot: 45
'45'
```

Pomocí funce input můžeš přiřadit nejakou hodnotu do proměnné, například takto:

```
>>> x = input("x: ")
x: 45
>>> y = input("y: ")
y: 23
```

A nyní můžeš ověřit, že hodnoty byly přiřazeny proměnným x a y a můžeš je dále použít:

```
>>> print(int(x) * int(y))
1035
```

>[note]
> Všimni si, že jsme uvnitř funkce print museli u proměnných x a y použít funkci *int()*.  Jedná se o tzn. přetypování, které jsme museli udělat, protože uživatel zadal hodnoty do proměnných x a y jako řetězce a ne jako čísla. Zkus si, co by se stalo, kdyby jsi přetypování neprovedl.

## Funkce

Funkce jsou jako malé programy, které slouží k vykonání určité specifické akce. Python má mnoho funkcí, které můžeš využívat. Tyto se nazývají *built-in* funkce. Dále si pak každý uživatel může vytvářet své flastní funkce dle potřeby.

```
>>> 2 ** 3
8
>>> pow(2, 3)
8
```

Zde vidíme, že funkce pow() vykonává stejnou funci, jako výraz 2 ** 3.

## Moduly

Moduly jsou rozšířením výchozích schopností Pythonu a mohou být importovány do tvého kódu.

```
>>> import math
>>> math.floor(11.9)
11
```

```
>>> from math import sqrt
>>> sqrt(9)
3.0
```
Mnoho modulů je standarní součástí Pythonu (jako například modul *math*), další pak mohou být naprogramovány tebou nebo někým dalším.

## Uložení a spuštění vašich programů

Doposud jsme si ukazovali, jak zadávat příkazy v Python interaktivní příkazové řádce. Co ale, když chceme náš program ulozžit pro pozdější použití? Pokud totiž zavřeme okno s Python interaktivní příkazovou řádkou, všw co jsem napsali je ztraceno.

Pokud chcete psát programy pro další použití, musíte jej uložit so souboru a později jej spustit. Pro psaní programu v Pythonu budeš potřebovat textový editor. Jak jej získat a nainstalovat je popsáno v kapitole [Instalace editoru](../../beginners/install-editor/).

Otevři nový soubor, pojmenuj ho hello.py a vlož do něj následující řádky:

```
name = input("What is your name? ")
print("Hello, " + name  + "!")
```

Ulož soubor a spusť pomocí příkazu ve Windows:

```
C:\>python hello.py
```

a nebo v UNIXu:

```
$ python hello.py
```

## Nastavení skriptu jako spustitelný soubor

Nyní jsi tedy schopný spustit Python program pomocí programu *python*. Co ale, když chceš svůj skript spouštět jako běžný program na počítači a nemuset se odvolávat na Python interpretr? Na operačních systémech typu UNIX se to dělá tak, že jako první řádku tvého skriptu přidáš následující:

```
#!/usr/bin/env python
```

a dále pak nastavíš práva na soubor tak, aby byl soubor se skriptem spustitelný.

```
$ chmod a+x hello.py
```

Nyní můžeš skript spustit pomocí:

```
./hello.py
```

Ve Windows použijte dvojklik ke spuštění svého skriptu. Problém je, že DOS okno s programem se uzavře ihned po proběhnutí skriptu. Jako možné řešení můžeš přidat následující řádek na konec programu:

```
input("Press <enter>")
```

## Komentáře

Znak hash (mřížka) je speciální znak v Pythonu. Kdekoliv jej použiješ, vše napravo od tohoto znaku je bráno jako jako komentář a je ignorováno pro běh programu.

```
# Collect the user's name
name = input("What is your name?") # This is also comment
```


