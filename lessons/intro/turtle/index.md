# 🐍 🐢

V této lekci si vyzkoušíš *želví kreslení*.

Pusť Python v *interaktivním módu* (bez souboru .py).

```pycon
$ python

>>>
```

> [note]
> (Znaky `>` a `$` píše počítač, ne ty.
> Na Windows bude místo `$` znak
> `>` a před `$` nebo
> `>` může být ještě něco dalšího.)

Pak napiš:

```python
from turtle import forward

forward(50)
```

Ukáže se okýnko se šipkou, které nezavírej.
Dej ho tak, abys viděla i příkazovou řádku
i nové okýnko.

## A kde je ta želva?

Želva je zrovna převlečená za šipku.
Ale funkce `shape` ji umí odmaskovat:

```python
from turtle import shape

shape('turtle')
```

Modul `turtle` obsahuje spoustu dalších funkcí, kterými můžeš želvu ovládat.
Pojďme se na ně kouknout zblízka.


## Otáčení

Želva se umí otáčet (doleva – `left` a doprava – `right`) a lézt po papíře
(dopředu – `forward`).
Na ocase má připevněný štětec, kterým při pohybu kreslí čáru.

```python
from turtle import forward, left, right

forward(50)
left(60)
forward(50)
right(60)
forward(50)
```

Zkus chvíli dávat želvě příkazy.
Když se ti výsledek nelíbí, můžeš zavřít kreslící okno a zkusit to znovu.
(Nebo místo zavření okna můžeš naimportovat a použít funkci `clear()`.)


## Želví program

Interaktivní mód je skvělý na hraní,
ale teď přejdeme zase na soubory.

Vytvoř si v editoru nový soubor.
Ulož ho do adresáře pro dnešní lekci pod jménem `zelva.py`.

> [note]
> Jestli adresář pro dnešní lekci ještě nemáš, vytvoř si ho!
> Pojmenuj ho třeba `02`.

> [warning]
> Soubor nepojmenovávej `turtle.py` – z modulu `turtle` budeš importovat.

Jestli chceš pro soubor použít jiné jméno, můžeš, ale
nepojmenovávej ho `turtle.py`.

Do souboru napiš příkazy na nakreslení obrázku
a – pozor! – na konci programu zavolej funkci `exitonclick`
(naimportovanou z modulu `turtle`).

> [note] Otázka
> Co dělá funkce <code>exitonclick</code>, kterou voláš na konci programu?

## Přerušovaná čára

Funkce `penup` řekne želvě, aby zvedla ocásek se štětcem: bude se tak hýbat
aniž by za sebou nechávala stopu.
Funkcí `pendown` můžeš želvě říct, aby kreslit zase začala.
Zkus si to:

```python
from turtle import forward, penup, pendown, exitonclick

forward(30)
penup()         # od teď želva nekreslí
forward(5)
pendown()       # od teď želva zase kreslí
forward(30)

exitonclick()
```

Až to budeš mít hotové, zkus začít kreslit trochu složitější obrázky:

### Čtverec

Nakresli čtverec.

![Želví čtverec](static/turtle-square.png)

Čtverec má čtyři rovné strany
a čtyři rohy po 90°.

{% filter solution %}
```python
from turtle import forward, left, exitonclick

forward(50)
left(90)
forward(50)
left(90)
forward(50)
left(90)
forward(50)
left(90)

exitonclick()
```
{% endfilter %}

### Obdélník

Nakresli obdélník.

Zkus zařídit, aby se po nakreslení „dívala” želva doprava (tak jako na začátku).

![Želví obdélník](static/turtle-rect.png)

{% filter solution %}
```python
from turtle import forward, left, exitonclick

forward(100)
left(90)
forward(50)
left(90)
forward(100)
left(90)
forward(50)
left(90)

exitonclick()
```
{% endfilter %}

### Tři čtverce

Nakresli tři čtverce, každý otočený třeba o 20°.

![Tři želví čtverce](static/turtle-squares.png)

{% filter solution %}
```python
from turtle import forward, left, exitonclick

forward(50)
left(90)
forward(50)
left(90)
forward(50)
left(90)
forward(50)
left(90)

left(20)

forward(50)
left(90)
forward(50)
left(90)
forward(50)
left(90)
forward(50)
left(90)

left(20)

forward(50)
left(90)
forward(50)
left(90)
forward(50)
left(90)
forward(50)
left(90)

exitonclick()
```
{% endfilter %}

Tolik kódu! Tohle musí jít nějak zjednodušit!

Jde.
Pojďme se naučit, jak v Pythonu nějakou činnost opakovat.


## Jak opakovat – a neopakovat *se*

Udělej v editoru nový soubor a ulož ho jako `cykly.py`.
Budeš v něm zkoušet *cykly*.

První opakovací program, který napíšeš, bude dělat tohle:

* Stokrát po sobě:
  * Napiš "Nikdy nebudu odsazovat o tři mezery!"

Přeložené do jazyka Python to vypadá následovně:

```python
for i in range(100):
    print('Nikdy nebudu odsazovat o tři mezery!')
```

Na ono `for i in range(100)` se detailněji podíváme za chvíli,
teď to pro nás bude “hlavička”, která říká “opakuj stokrát”.

Podobnou “hlavičku” už jsi viděl{{a}} u příkazu `if`.
Stejně jako u `if` tu je na konci dvojtečka a za ní následuje
odsazený blok – *tělo* příkazu; to na co se hlavička vztahuje.
Tělo příkazu `if` se provede jen někdy;
tělo příkazu `for` se opakuje několikrát dokola.


### Výčet

Zkus napsat ještě jeden vzorový program, který v češtině zní:

* Pro každý <var>pozdrav</var> z výčtu: „Ahoj“, “Hello”, “Hola”, ”Hei”, "SYN":
  * Vypiš <var>pozdrav</var> a za ním vykřičník.

A v Pythonu:

```python
for pozdrav in 'Ahoj', 'Hello', 'Hola', 'Hei', 'SYN':
    print(pozdrav + '!')
```

Opět je tu hlavička a tělo příkazu.
Tentokrát se na hlavičku podívej pozorněji.
Pythonní <code>for <var>promenna</var> in <var>sekvence</var></code>
znamená „Pro každé <var>promenna</var> ze <var>sekvence</var>“.

Jméno proměnné si volíš {{gnd('sám', 'sama')}}.
Příkaz `for` danou proměnnou vždy *nastaví* na aktuální
hodnotu a pak provede všechno, co je v odsazeném těle cyklu.
Program výše tedy funguje úplně stejně, jako kdybys napsal{{a}}:

```python
pozdrav = 'Ahoj'
print(pozdrav + '!')

pozdrav = 'Hello'
print(pozdrav + '!')

pozdrav = 'Hola'
print(pozdrav + '!')

pozdrav = 'Hei'
print(pozdrav + '!')

pozdrav = 'SYN'
print(pozdrav + '!')
```


### Range

Vraťme se k `for i in range(100)`.
Už víš, že to znamená „Pro každé <var>i</var> ze sekvence `range(100)`“.
Co je ale to `range`? Když si ho vypíšeš, nevypadne nic vysvětlujícího:

```pycon
>>> range(100)
range(0, 100)
```

Je ale použité jako „sekvence“
v <code>for <var>promenna</var> in <var>sekvence</var></code>.
Je to nějaký výčet, nějaká posloupnost hodnot.
A teď už umíš vypsat, jaké to jsou!

```python
for i in range(5):   # Doporučuju použít jen 5 místo 100
    print(i)
```

neboli česky:

* Pro každé <var>i</var> z `range(5)`:
  * Vypiš <var>i</var>

Program spusť. Jaká čísla se vypíšou? (Neboli: co je v sekvenci `range(5)`?)

{% filter solution %}
Vypíšou se čísla od 0 do 4!
Program funguje steně, jako kdybys napsal{{a}}:

```python
i = 0
print(i)

i = 1
print(i)

i = 2
print(i)

i = 3
print(i)

i = 4
print(i)
```

V sekvenci `range(5)` jsou čísla 0, 1, 2, 3 a 4. Je jich celkem pět.
{% endfilter %}

Funkce `range(n)` vrací *sekvenci čísel*.
Začíná od 0 a čísel v ní je přesně <var>n</var>.
(Na samotné <var>n</var> se tedy už nedostane.)

Často budeš potřebovat Pythonu říct, ať něco „<var>n</var>-krát zopakuje“.
Na to můžeš použít `for i in range(n)` („pro každé <var>i</var> od 0 do
<var>n</var>-1“) s tím, že proměnná <var>i</var> – „počitadlo“ – tě nezajímá.
V programu ji jednoduše nepoužiješ.

Teď by už mělo být jasné, jak funguje původní program:

```python
for i in range(100):
    print('Nikdy nebudu odsazovat o tři mezery!')
```

* Zopakuj 100krát:
  * Vypiš `'Nikdy nebudu odsazovat o tři mezery!'`

Python píše hlášky, jednu za druhou, a u toho si v promněnné <var>i</var>
počítá, jak už je daleko.

> [style-note]
> Proměnná <var>i</var> se v matematice typicky používá pro *celá čísla*;
> je to zkratka z termínu *index* (číslo prvku).
> V programování se tradičně používá pro číslo průchodu cyklem,
> jako v příkladu výše.
> Pro lepší pochopení bývá dobré použít popisnější jméno proměnné, tady
> například `cislo_vypisu`; v krátkých a přehledných cyklech – a zvlášť v těch
> které proměnnou nepoužívají – se ale často setkáš s krátkým `i`, `j`, `k`…
>
> Někteří programátoři pojmenovávají ignorovanou proměnnou `_` (podtržítko).
> To je pro Python jméno jako jakékoli jiné, ničím se neliší od `i` nebo `x`:
>
> ```python
> for _ in range(100):
>    print('Nikdy nebudu odsazovat o tři mezery!')
> ```

## Dlouhá přerušovaná čára

Už víš, že pomocí `penup` a `pendown` lze nakreslit přerušenou čáru:

```python
from turtle import forward, penup, pendown, exitonclick

forward(30)
penup()         # od teď želva nekreslí
forward(5)
pendown()       # od teď želva zase kreslí
forward(30)

exitonclick()
```

Zkus nakreslit dlouhou přerušovanou čáru.

![Želva a přerušovaná čára](static/turtle-dashed.png)

{% filter solution %}
```python
from turtle import forward, penup, pendown, exitonclick

for i in range(10):
    forward(10)
    penup()
    forward(5)
    pendown()

exitonclick()
```
{% endfilter %}


Pak zkus zařídit, aby jednotlivé čárky byly postupně
větší a větší.

![Želva a přerušovaná čára](static/turtle-dashed2.png)

> [note] Nápověda
>
> První čárka je dlouhá 1 jednotku, druhá 2 jednotky, třetí 3, atd.
>
> Dokonce můžeš na začátek dát prázdnou čárku (0 jednotek)
> a mít tak délky 0, 1, 2, 3, 4, …
>
> V jaké proměnné máš při prvním průchodu cyklem 0, ve druhém 1, atd.?

{% filter solution %}
```python
from turtle import forward, penup, pendown, left, exitonclick

for i in range(20):
    forward(i)
    penup()
    forward(5)
    pendown()

exitonclick()
```
{% endfilter %}


## Čtverec II

A teď znovu nakresli čtverec, tentokrát lépe – s použitím cyklu!

Čtverec se kreslí následovně:

* Čtyřikrát:
  * Popojdi dopředu (a kresli přitom čáru)
  * Otoč se o 90°

![Želví čtverec](static/turtle-square.png)

{% filter solution %}
```python
from turtle import forward, left, exitonclick

for i in range(4):
    forward(50)
    left(90)

exitonclick()
```
{% endfilter %}

### Tři čtverce

Nakonec nakresli 3 čtverce, každý otočený o 20°.
Tentokrát už víš, jak to dělat chytře: opakuj pomocí příkazu
`for`, ne kopírováním kódu.

![Tři želví čtverce](static/turtle-squares.png)

* Třikrát:
  * Nakresli čtverec (viz jedna z předchozích úloh)
  * Otoč se o 20°

{% filter solution %}
```python
from turtle import forward, left, right, speed, exitonclick

# Třikrát:
for i in range(3):

    # Nakresli čtverec (kód zkopírovaný z předchozí úlohy a odsazený)
    for j in range(4):
        forward(50)
        left(90)

    # Otoč se o 20°
    left(20)

exitonclick()
```
{% endfilter %}


## Úkol navíc

Máš-li hotovo, zkus nakreslit schody:

![Želví schody](static/turtle-stairs.png)

A máš-li i schody, zkus nakreslit těchto šest (nebo sedm?) šestiúhelníků:

![Želví plástev](static/turtle-hexagons.png)
