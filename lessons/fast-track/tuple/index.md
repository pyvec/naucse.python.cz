# <var>N</var>-tice

Už víš, že pomocí `return` lze z funkce vracet hodnotu:

``` python
def dvojnasobek(x):
    return x * 2
```

Jak ale napsat funkci, která vrátí dvě hodnoty?
Chci třeba napsat funkci, která spočítá podíl a zbytek po dělení.

Dvě hodnoty se dají vrátit jako seznam:

``` python
def podil_a_zbytek(a, b):
    podil = a // b
    zbytek = a % b

    return [podil, zbytek]

print(podil_a_zbytek(5, 2))
```

Lepší je ale vrátit *dvojici* čísel – dvě čísla oddělená čárkou:

``` python
def podil_a_zbytek(a, b):
    podil = a // b
    zbytek = a % b

    return podil, zbytek

print(podil_a_zbytek(5, 2))
```

Tomuhle se říká dvojice – a podobně se tvoří trojice, čtveřice, pětice,
šestice, prostě <var>n</var>-tice (angl. *tuple*) hodnot.
Funguje podobně jako seznam, ale nedá se měnit – např. se do ní nedají
přidávat další prvky pomocí `append`.
Když mám trojici, vždycky zůstane jako trojice.

Když máš <var>n</var>-tici, můžeš ji přiřazením *rozbalit* (angl. *unpack*)
do několika proměnných:

``` python
podil, zbytek = podil_a_zbytek(5, 2)

print(podil)
print(zbytek)
```

<var>N</var>-tice mají spoustu využití, například:

* Bod v prostoru má 3 souřadnice – trojice čísel!
* Hrací karta má barvu a hodotu – dvojice čísla a řetězce, např. `(2, 'piky')`

Občas je potřeba dát <var>n</var>-tice do seznamu, např. abys uložil{{a}}
informace o celém balíčku hracích karet.
V podobných případech je potřeba každou <var>n</var>-tici uzavřít do závorek,
aby bylo jasné kde začíná a kde končí.
Tady je seznam dvojic:

```python
ruka = [(2, 'piky'), (10, 'kříže'), (8, 'káry')]
```

Když takový seznam máš, můžeš ho projít v cyklu `for` s pomocí rozbalování:

``` python
for hodnota, barva in ruka:
    print('Hraju', hodnota, 'a jsou to', barva)
```

## Zip

<var>N</var>-tice, respektive sekvenci <var>n</var>-tic, vrací funkce `zip`,
která umožňuje projít zároveň několik seznamů,
jejichž prvky si navzájem odpovídají:

``` python
veci = ['tráva', 'slunce', 'mrkev', 'řeka']
barvy = ['zelená', 'žluté', 'oranžová', 'modrá']
mista = ['na zemi', 'nahoře', 'na talíři', 'za zídkou']

for vec, barva, misto in zip(veci, barvy, mista):
    print(barva, vec, 'je', misto)
```

V tomhle cyklu dostaneš napřed trojici prvních prvků ze všech tří seznamů,
pak trojici všech druhých prvků, pak třetích, a tak dále.

## Shrnutí

Co ses dozvěděl{{a}} tentokrát?

* Pomocí *<var>n</var>-tice* se dá spojit několik hodnot do jedné.
* <var>N</var>-tice se dají rozbalit do několika proměnných.
* Funkce `zip` vrací sekvenci <var>n</var>-tic, ve kterých jsou prvky
  z několika seznamů.

A je to.
*Jsi naprosto skvěl{{gnd('ý', 'á')}}!*
Tohle byla složitá lekce, takže bys na sebe měl{{a}} být hrd{{gnd('ý', 'á')}}.
My jsme na tebe velmi hrdí za to, že ses dostal{{a}} tak daleko!

Běž si krátce odpočinout – protáhnout se, projít se,
zavřít oči – než se pustíš do další kapitoly. :)

🧁

