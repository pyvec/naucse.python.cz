{% if var('pyladies') %}

> [note] Pro kouče
> Slajdy jsou k dispozici na stránkách
> [PyLadies](http://pyladies.cz/v1/s003-looping/functions.html#/).

Pokud jsi minule udělal{{a}} projekt navíc, tak jsi nejspíš
do programu zadal{{a}} hotnotu čísla π.
{% else %}
Pokud jsi v minulých lekcíh pracoval{{a}} s kruhy, tak jsi nejspíš
do programu zadal{{a}} hotnotu čísla π.
{% endif %}

Python má ale spoustu vychytávek zabudovaných – není třeba je přímo psát,
stačí jen vědět, kam se podívat.

*Pí* můžeme zpřístupnit *importem* z modulu `math`.

```python
from math import pi

print(pi)
```

Jak je vidět, π je tak trochu schované.
Přece jen, `print` nebo `if` potřebují všichni, ale ne všichni mají
rádi matematiku…

Teď ale u matematiky ještě chvilku zůstaneme.


## Výrazy

V matematice máme spoustu různých operací,
které se zapisují symboly – třeba plus a minus.
Stejné symboly používá i Python:

* 3 + 4
* <var>a</var> - <var>b</var>

S násobením a dělením už je to složitější,
matematický zápis se na běžné klávesnici nedá napsat:

* 3 · 4
* ¾

V Pythonu si ale pořád vystačíme s operátorem.

Matematici ovšem psali na papír,
a tak vymýšleli stále nezapsatelnější klikyháky,
které se programátorům nechtělo přepisovat:

* <var>x</var>²
* <var>x</var> ≤ <var>y</var>
* sin θ
* Γ(<var>x</var>)
* ∫<var>x</var>
* ⌊<var>x</var>⌋
* <var>a</var> ★ <var>b</var>
* <var>a</var> ⨁ <var>b</var>

Ne že by neexistovaly programovací jazyky,
na které je potřeba speciální klávesnice.
Ale programy v nich se většinou nedají
dost dobře psát, ani číst.

> [note]
> Třeba tady je program v jazyce APL:
>
> <!--z http://catpad.net/michael/apl/ -->
>
>     ⍎’⎕’,∈Nρ⊂S←’←⎕←(3=T)∨M∧2=T←⊃+/(V⌽”⊂M),(V⊖”⊂M),(V,⌽V)⌽”(V,V←1¯1)⊖”⊂M’


V Pythonu je operátorů poměrně málo.
Už z nich známe skoro půlku!
A i tak některé místo symbolů používají slova.
Tady jsou všechny Pythonní operátory:

<div>
    <code>==</code> <code>!=</code>
    <code>&lt;</code> <code>&gt;</code>
    <code>&lt;=</code> <code>&gt;=</code>
    <code class="text-muted">|</code> <code class="text-muted">^</code>
    <code class="text-muted">&amp;</code>
    <code class="text-muted">&lt;&lt;</code> <code class="muted">&gt;&gt;</code>
    <code>+</code> <code>-</code>
    <code>*</code> <code class="text-muted">@</code> <code>/</code>
    <code>//</code> <code>%</code>
    <code class="text-muted">~</code>
    <code>**</code>
    <code class="text-muted">[ ]</code> <code class="text-muted">( )</code>
    <code class="text-muted">{ }</code>
    <code class="text-muted">.</code>
</div>

<div>
    <code class="muted">lambda</code>
    <code class="muted">if else</code>
    <code>or</code> <code>and</code> <code>not</code>
    <code class="muted">in</code> <code class="muted">not in</code>
    <code class="muted">is</code> <code class="muted">is not</code>
</div>

Je asi jasné, že většina operací,
které v programu budeme chtít udělat,
se nedá vyjádřit operátorem.


Co s tím?

Jeden z matematických zápisů, které jsem před chvilkou ukázal,
používá pro operace jména.

* <var>x</var> = sin <var>a</var>

A to jde napsat na klávesnici!
Python jenom přidá závorky,
aby bylo jasnější, k čemu se operace vztahuje:

```python
x = sin(a)
```

Ten `sin` musíš *naimportovat*,
jako předtím *pí*
(přece jen, ne všichni mají rádi matematiku).
Takže celý program vypadá následovně:

```python
from math import sin

x = sin(1)  # (v radiánech)
print(x)
```

> [warning] Import a pojmenování souborů
> Při importování je potřeba si dávat pozor na pojmenování souborů:
> importuješ-li `from math`, nesmí se tvůj program jmenovat `math.py`.
>
> Proč? Když Python v adresáři, ze kterého program pouštíš, najde soubor
> `math.py`, bude se snažit importovat `sin` z něho místo
> z předpřipravené sady matematických funkcí.

## Volání funkcí

Funkci voláme *jménem*.

Je to jméno jako u proměnných – vlastně to *je* proměnná,
jen je v ní, místo čísla nebo řetězce, funkce.

Za jméno funkce patří závorky,
do nichž uzavřeme *argument* (neboli *vstup*) funkce.
To je informace, se kterou bude naše funkce
pracovat – třeba `sin()` ze svého argumentu vypočítá <em>sinus</em>.

Volání funkce je *výraz* a výsledná, neboli *návratová*, hodnota
(angl. *return value*) se dá třeba přiřadit do proměnné.

```
        jméno funkce
                 │
                ╭┴╮
            x = sin(1)
            ▲      ╰┬╯
            │     argument
            │
            ╰── návratová hodnota
```

Nebo se dá použít místo čísla v součtu:

```python
a = sin(1) + cos(2)
```

Nebo v podmínce ifu:

```python
if sin(1) < 3:
```

Nebo dokonce jako argument jiné funkce:

```python
print(sin(1))
```

… a podobně.


### Argumenty

Některým funkcím můžeme předat i více argumentů.
Třeba funkci `print`, která všechny své argumenty vypíše na řádek.
Jednotlivé argumenty oddělujeme čárkami:

```python
print(1, 2, 3)
```

```python
print("Jedna plus dva je", 1 + 2)
```

Některé funkce nepotřebují žádný argument.
Příkladem je zase `print`.
Je ale nutné napsat závorky – i když jsou prázdné.
Hádej, co tohle volání udělá?

```python
print()
```

{% filter solution %}
Funkce `print` zavolaná bez argumentů napíše prázdný řádek.

(Je to přesně podle definice – funkce `print` všechny své argumenty vypíše
na řádek.)
{% endfilter %}

### Funkce je potřeba volat

Pozor na to, že když nenapíšeš závorky, funkce se nezavolá!
(Nedostaneš návratovou hodnotu, ale samotnou funkci.)
Zkus si, co dělají tyhle příklady, abys pak podobné chyby poznala:

```python
from math import sin
print(sin(1))
print(sin)
print(sin + 1)
```

### Pojmenované argumenty

Některé funkce umí pracovat i s *pojmenovanými* argumenty.
Píšou se podobně jako přiřazení do proměnné,
s rovnítkem, ale uvnitř závorek.

Třeba funkce `print` normálně ukončí výpis novým řádkem,
ale pomocí argumentu `end` se dá vypsat i něco jiného.

> [note]
> Tenhle příklad je potřeba napsat do souboru; v interaktivní konzoli
> nebude výstup vypadat, jak má.

```python
print('1 + 2', end=' ')
print('=', end=' ')
print(1 + 2, end='!')
print()
```

## Užitečné funkce

Nakonec si ukážeme pár základních funkcí, které nám Python nabízí.
Můžeš si stáhnout i
<a href="https://github.com/encukou/cheatsheets/raw/master/basic-functions/basic-functions-cs.pdf">přehled</a>,
který se rozdává na srazech.

### Vstup a výstup

Tyhle funkce už známe.
`print` vypíše nepojmenované argumenty, oddělené mezerou.
Pojmenovaný argument `end` určuje, co se vypíše na konci (místo přechodu
na nový řádek);
`sep` zase, co se vypíše mezi jednotlivými argumenty (místo mezery).

> [note]
> Příklad opět doporučuji spustit ze souboru, ne
> interaktivně:

```python
print(1, "dvě", False)
print(1, end=" ")
print(2, 3, 4, sep=", ")
```

Základní funkce na načtení vstupu, `input`,
vypíše otázku, počká na text od uživatele
a ten vrátí jako řetězec.

```python
input('zadej vstup: ')
```

### Převádění typů


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
{%- if var('pyladies') %}
Teď je hlavní to, že už víš, jak funguje
`int(input('zadej číslo: '))` z minula!
{% endif %}


### Matematické funkce

Matematika je občas potřeba, takže se pojďme
podívat, jak v Pythonu pracovat s čísly.

Jedna zajímavá matematická funkce je k dispozici vždy:

```python
round(cislo)    # zaokrouhlení
```

Spousta dalších se dá importovat z modulu `math`:

```python
from math import sin, cos, tan, sqrt, floor, ceil

sin(uhel)       # sinus
cos(uhel)       # kosinus
tan(uhel)       # tangens
sqrt(cislo)     # druhá odmocnina

floor(cislo)    # zaokrouhlení dolů
ceil(cislo)     # zaokrouhlení nahoru
```

### Nápověda

Další funkce pomáhá programátorům:
Můžeš si přímo z programu (nebo z interaktivního
režimu) vyvolat nápovědu k nějaké funkci.
(Občas bývá srozumitelná i pro začátečníky,
občas bohužel spíš ne – v takovém případě zkus
Google).

Nápověda se zobrazí podle systému buď v prohlížeči,
nebo přímo v terminálu.
Když je nápověda v terminálu příliš dlouhá, dá se v ní
pohybovat (<kbd>↑</kbd>, <kbd>↓</kbd>,
<kbd>PgUp</kbd>, <kbd>PgDn</kbd>) a „ven“
se dostaneš klávesou <kbd>Q</kbd> (od *Quit*).

Nápověda k funkci <code>print</code> se zobrazí příkazem:

```python
help(print)
```

Nápověda se dá vypsat i k celému modulu.

```python
import math

help(math)
```

### Náhoda

Nakonec si ukážeme dvě funkce z modulu
`random`, které jsou velice
užitečné pro hry.

```python
from random import randrange, uniform

randrange(a, b)   # náhodné celé číslo od a do b-1
uniform(a, b)     # náhodné reálné číslo od a do b
```

Pozor na to, že <code>randrange(a, b)</code>
nikdy nevrátí samotné <code>b</code>.
Pokud potřebujeme náhodně vybrat ze tří možností,
použij <code>randrange(0, 3)</code>,
což vrátí <code>0</code>, <code>1</code>, nebo
<code>2</code>:

```python
from random import randrange

cislo = randrange(0, 3)  # číslo je od 0, 1, nebo 2
if cislo == 0:
    print('Kolečko')
elif cislo == 1:
    print('Čtvereček')
else:  # 2
    print('Trojúhelníček')
```

> [note]
> Pamatuj, když importuješ z modulu `random`, nesmí se tvůj soubor
> jmenovat `random.py`.

### A další
Python dává k dispozici obrovské množství dalších
funkcí a modulů, i když ne všem budeš ze začátku
rozumět.
Všechny jsou – anglicky – popsány v dokumentaci Pythonu, např.
<a href="https://docs.python.org/3/library/functions.html">vestavěné funkce</a>,
<a href="https://docs.python.org/3/library/math.html">matematika</a>.
