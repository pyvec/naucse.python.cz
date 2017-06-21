# Print a chybové hlášky

{% if var('pyladies') -%}
{% set rootname = 'pyladies' %}
{%- else -%}
{% set rootname = 'naucse-python' %}
{%- endif %}

Teď vytvoř soubor <code><span class="pythondir">~/{{ rootname }}</span>/02/printing.py</code>
a napiš do něj následující příkazy:

```python
print(1)
print(1, 2, 3)
print(1 + 1)
print(3 * 8)
print(10 - 2.2)
print(3 + (4 + 6) * 8 / 2 - 1)
print('*' * 80)
print("Ahoj" + " " + "PyLadies!")
print("Součet čísel 3 a 8 je", 3 + 8)
print('Máma má mísu')
print(V míse je maso.)
```

Program spusť. Funguje?

## Jak číst chyby

Často zjistíš, že program, který napíšeš, nebude fungovat hned napoprvé.
Počítač je hloupý stroj; pokud instrukce nenapíšeš přesně podle pravidel jazyka
Python, neumí si domyslet, co po něm chceš.
Ale nevěš hlavu, stává se to všem programátorům.
Důležité je vědět, jak chybu najít.
A k tomu ti pomůžou chybové výpisy.
Třeba program výše vypíše po spuštění následující chybu:

<pre>
  File "<span class="plhome">~/pyladies</span>/02/printing.py", line <span class="err-lineno">11</span>
    print(V míse je maso.)
               ^
<span class="err-exctype">SyntaxError</span>: invalid syntax
</pre>

Při chybě Python napřed vypíše
jméno souboru a <span class="err-lineno">číslo řádku</span>,
na kterém chyba je.
Potom vypíše celý řádek s chybou
a nakonec oznámí <span class="err-exctype">druh chyby</span>
(v tomto případě je to „syntaktická chyba“)
a případně nějaké bližší upřesnění.

> [note] Pro zvídavé
> Jak se od téhle chyby liší ta, která nastane, když zkusíš sečíst číslo a řetězec?
> Nebo když zkusíš dělit nulou?

Chybové hlášky můžou být ze začátku těžko pochopitelné,
zvyknout se na ně dá asi jenom praxí.
Pro tebe bude ze začátku důležité hlavně ono číslo řádku.
Když víš, že chyba je na řádku <span class="err-lineno">11</span>,
můžeš se podívat na tento řádek a zkusit chybu najít.

Když chyba není na daném řádku, může být ještě
o pár řádků výš nebo níž:
Python občas nesdílí lidské představy o tom, kde přesně chyba *je*,
a ukáže jen, kde si jí sám *všimnul*.

V našem případě je chyba v tom, že kolem řetězce nejsou uvozovky.
Přidej je a program znovu spusť.
Jestli funguje, gratuluji!
Jinak chybu opět oprav a opakuj, dokud to nebude fungovat :)

## Jak funguje program

Teď, když program běží, se můžeme podívat, co se při
jeho spuštění vlastně děje.
Je to zatím docela jednoduché: příkazy se provádějí jeden po druhém,
odshora dolů.
Program je jako recept na vaření: seznam instrukcí, které říkají co je potřeba
udělat.

Zanedlouho budou tvoje programy připomínat spíš recepty na
čarodějné lektvary (*počkej do úplňku a pokud je Mars
v konjunkci s Jupiterem, třikrát zamíchej*),
ale základní myšlenka je stále stejná:
počítač čte odshora dolů a provádí příkazy jeden po druhém.

## Print a výrazy

A z jakých že instrukcí se náš „recept“ skládá?

Ten `print`, který tu celou dobu používáš, je *funkce*.
O funkcích se ještě budeme bavit později,
teď stačí vědět, že když napíšeš `print`
a za to do závorky několik *výrazů* (angl. *expressions*)
oddělených čárkou, hodnoty těchto výrazů se vypíšou.

A co že je ten výraz?
V našem programu máš několik příkladů:
výraz je číslo, řetězec nebo nějaká (třeba matematická) operace
složená z více výrazů.
Třeba výraz `3 + 8` sečítá výrazy `3` a `8`.

V sekci o [proměnných]({{ lesson_url('beginners/variables') }}) se
na výrazy a jejich hodnoty podíváme podrobněji.
