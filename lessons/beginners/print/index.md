# Print a chybové hlášky

Vytvoř v editoru nový soubor, ulož ho do adresáře pro dnešní lekci
pod jménem `printing.py` a napiš do něj teď už známý příkaz:

```python
print("Ahoj světe!")
```

Program spusť:
* pokud ti už na začátku příkazové řádky nesvítí `(venv)`,
  aktivuj si virtuální prostředí,
* pomocí `cd` donaviguj do adresáře s programem,
* zadej `python printing.py`.

Funguje? Doufám, že ano; za chvíli ho vylepšíme.


## Další příkazy

Zkus do programu postupně, po jednom, přidávat další řádky.
Po přidání každého dalšího `print` program znovu spusť a vyzkoušej, jestli
funguje.

Abys nemusel{{a}} v příkazové řádce stále dokola psát `python printing.py`,
zkus zmáčknout na klávesnici šipku nahoru, <kbd>↑</kbd>.
Vrátíš se tak k předchozímu příkazu, který stačí „odklepnout“ pomocí
<kbd>Enter</kbd>.


Úplně každý příkaz ti asi nebude fungovat hned napoprvé – kdyby program
dělal něco divného, přeskoč na další sekci, *jak číst chyby*.

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

> [note] Řetězce
> Proč jsou některé hodnoty v uvozovkách a některé ne?
> Pokud chceš v Pythonu pracovat s textem, musíš ho obalit do uvozovek, aby Python
> věděl, že se k němu má chovat jinak než například k číslům.
> Více se dozvíš později, zatím si zapamatuj, že se takovýto text označuje označuje v programovací
> hantýrce jako `řetězec`.

## Jak číst chyby

Často zjistíš, že program, který napíšeš, nebude fungovat hned napoprvé.
Počítač je hloupý stroj; pokud instrukce nenapíšeš přesně podle pravidel jazyka
Python, neumí si domyslet, co po něm chceš.
Ale nevěš hlavu, stává se to všem programátorům.
Důležité je vědět, jak chybu najít.
A k tomu ti pomůžou chybové výpisy.

Pokud program výše opíšeš přesně, vypíše po spuštění následující hlášku:

<pre>
  File "<span class="plhome">~/pyladies</span>/02/printing.py", line <span class="err-lineno">11</span>
    print(V míse je maso.)
               ^
<span class="err-exctype">SyntaxError</span>: invalid syntax
</pre>

Při chybě Python napřed zmíní jméno souboru a
<span class="err-lineno">číslo řádku</span>, na kterém si chyby všimnul.
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
Python občas nesdílí lidské představy o tom, kde přesně chyba *je*.
Ukáže jen, kde si jí sám *všimnul*.

V našem případě je chyba v tom, že kolem řetězce *V míse je maso* nejsou uvozovky.
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
počítač „čte“ odshora dolů a provádí příkazy jeden po druhém.


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
Třeba výraz `3 + 8` sčítá výrazy `3` a `8`.

V sekci o [proměnných]({{ lesson_url('beginners/variables') }}) se
na výrazy a jejich hodnoty podíváme podrobněji.

> [style-note] Typografická vsuvka
> Všimni si stylu zápisu: jako v češtině se po otevírací závorce a před
> uzavírací závorkou nepíše mezera; na rozdíl od češtiny ale mezera není
> mezi `print` a závorkou.
> ```python
> print("Ahoj!")
> ```
>
> S čárkou je to jako v češtině: mezeru píšeme po čárce, ale ne před ní:
> ```python
> print(1, 2, 3)
> ```
>
> Kolem operátorů jako `+` a `/` se obyčejně píše jedna mezera zleva a
> jedna zprava. Někdy je ale přehlednější obě vynechat:
> ```python
> print(2 + 8)
> print("Jedna a půl je", 1 + 1/2)
> ```
