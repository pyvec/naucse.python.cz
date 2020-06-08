
# Užitečné funkce

Ukažme si pár základních funkcí, které Python nabízí.

Tato kapitola ukazuje výběr z nástrojů, které jsou ti v Pythonu k dispozici.
Tvůj cíl není naučit se vše nazpaměť, ale mít přehled o tom, co je zhruba
možné.
Detaily můžeš vždycky dohledat – ať už na taháku (které jsou, na rozdíl od
školy, vždycky povoleny!), v těchto materiálech, nebo v oficiální
dokumentaci či jinde na Internetu.

Můžeš si stáhnout i
<a href="https://github.com/pyvec/cheatsheets/raw/master/basic-functions/basic-functions-cs.pdf">tahák</a>,
který se rozdává na srazech.
Doporučuji mít ho ze začátku při ruce.
Když narazíš na úkol, se kterým si nevíš rady, projdi si tahák a zamysli se,
která z funkcí by se dala použít.


## Vstup a výstup

Tyhle funkce už známe.
`print` vypíše nepojmenované argumenty, oddělené mezerou.
Pojmenovaný argument `end` určuje, co se vypíše na konci (místo přechodu
na nový řádek);
`sep` udává, co se vypíše mezi jednotlivými argumenty (místo mezery).

> [note]
> Příklad opět spusť ze souboru, ne interaktivně:

```python
print(1, 'dvě', False)
print(1, end=' ')
print(2, 3, 4, sep=', ')
```

Základní funkce pro načtení vstupu, `input`,
vypíše otázku, počká na text od uživatele a ten vrátí jako řetězec.

```python
input('zadej vstup: ')
```

Kontrolní otázky:

* Je `input` „normální“ funkce, nebo procedura?
* Co bere funkce `input` jako argument?
* Jaká je návratová hodnota funkce `input`?

{% filter solution %}
Funkce `input` vrací hodnotu, se kterou může program dál pracovat.
Zařadil bych ji tedy mezi „normální“ funkce.

Jako argument bere `input` otázku, na kterou se uživatele zeptá.

Návratová hodnota funkce `input` je řetězec s odpovědí uživatele.
{% endfilter %}



## Převádění typů


Co ale když nechceme pracovat s řetězcem, ale třeba s číslem?
Tady nám pomůže skupina funkcí, které umí převádět čísla na řetězce a zpátky.
Každý ze tří <em>typů</em> (angl. <em>types</em>) proměnných, které zatím známe,
má funkci, která vezme nějakou hodnotu a vrátí podobnou hodnotu „svého“ typu.
Na celá čísla je funkce `int` (z angl. *integer*), na reálná čísla je `float`
(z angl. *floating-point*), a pro řetězce `str` (z angl. *string*).

```python
int(x)              # převod na celé číslo
float(x)            # převod na reálné číslo
str(x)              # převod na řetězec
```

Příklady:

```python
3 == int('3') == int(3.0) == int(3.141) == int(3)
8.12 == float('8.12') == float(8.12)
8.0 == float(8) == float('8') == float(8.0)
'3' == str(3) == str('3')
'3.141' == str(3.141) == str('3.141')
```
Ne všechny převody jsou možné:

```python
int('blablabla')    # chyba!
float('blablabla')  # chyba!
int('8.9')          # chyba!
```

…a jak si poradit s chybou, která nastane,
když použiješ špatnou hodnotu, si řekneme později.

### Převádění a `input`

Převádění typů se často používá při načítání vstupu, třeba takto:

```python
cislo = int(input('Zadej číslo: '))
```

Jak Python vyhodnotí tento výraz?
Zadá-li uživatel <kbd>4</kbd><kbd>2</kbd><kbd>Enter</kbd>,
funkce `input` vrátí řetězec`'42'`.
Ten pak funkce `int` vezme jako argument, udělá podle něj číslo a to
číslo vrátí:

```python
cislo = int(input('Zadej číslo: '))
      #     ╰─────────┬─────────╯
cislo = int(        '42'          )
      # ╰────────────┬────────────╯
cislo =             42
```


## Matematické funkce

Matematika je občas potřeba, takže se pojďme
podívat, jak v Pythonu pracovat s čísly.

Jedna zajímavá matematická funkce je k dispozici vždy:

```python
round(cislo)    # zaokrouhlení
```

Spousta dalších není k dispozici od začátku programu.
Ne každý má rád matematiku, a ne ve všech druzích programu jsou takové operace
potřeba.
Proto musíš předem – typicky na začátku souboru – říct, že je budeš používat.
To se dělá *naimportováním* z modulu `math`:

```python
from math import sqrt, floor, ceil
```

Naimportované funkce pak můžeš použít:

```python
sqrt(cislo)                 # druhá odmocnina

floor(cislo)                # zaokrouhlení dolů
ceil(cislo)                 # zaokrouhlení nahoru
```

Kdybys potřeboval{{a}} goniometrické funkce jako sinus, jsou k dispozici taky.
Jen pozor na to, že počítají pro úhly v [radiánech].
Hodnoty ve stupních je potřeba na radiány převést.

[radiánech]: https://cs.wikipedia.org/wiki/Radi%C3%A1n

```python
from math import sin, cos, tan, degrees, radians

sin(uhel)       # sinus
cos(uhel)       # kosinus
tan(uhel)       # tangens

degrees(uhel)   # převod z radiánů na stupně
radians(uhel)   # převod ze stupňů na radiány
```

> [warning] Import a pojmenování souborů
> Při importování je potřeba si dávat pozor na pojmenování souborů:
> importuješ-li `from math`, nesmí se tvůj program jmenovat `math.py`.
>
> Proč? Když Python v adresáři, ze kterého program pouštíš, najde soubor
> `math.py`, bude se snažit importovat `sin` z něho místo
> z předpřipravené sady matematických funkcí.


## Náhoda

Nakonec si ukážeme dvě funkce, které vrací náhodná čísla.
Jsou užitečné třeba pro hry, ve kterých se hází kostkou nebo tahají
náhodné karty.

Opět nejsou potřeba tak často a je potřeba je *naimportovat*.
Tentokrát z modulu `random`:


```python
from random import randrange, uniform
```

Pak už se dají použít:

```python
randrange(a, b)   # náhodné celé číslo od a do b-1
uniform(a, b)     # náhodné reálné číslo od a do b
```

Pozor na to, že <code>randrange(a, b)</code>
nikdy nevrátí samotné <code>b</code>.
Pokud potřebuješ náhodně vybrat ze tří možností,
použij <code>randrange(0, 3)</code>,
což vrátí <code>0</code>, <code>1</code>, nebo
<code>2</code>:

```python
from random import randrange

cislo = randrange(0, 3)  # číslo je 0, 1, nebo 2
if cislo == 0:
    print('Kolečko')
elif cislo == 1:
    print('Čtvereček')
else:  # tady musí být číslo 2
    print('Trojúhelníček')
```

> [note]
> Pamatuj, když importuješ z modulu `random`, nesmí se tvůj soubor
> jmenovat `random.py`.

## A další
Python dává k dispozici obrovské množství dalších
funkcí a modulů, i když ne všem budeš ze začátku
rozumět.
Všechny jsou – anglicky – popsány v dokumentaci Pythonu, např.
<a href="https://docs.python.org/3/library/functions.html">vestavěné funkce</a>,
<a href="https://docs.python.org/3/library/math.html">matematika</a>.
