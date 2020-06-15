# Zápis řetězců

Teď se podíváme na zoubek řetězcům.
Už s nimi trochu umíš, tak začneme rekapitulací.

Textový *řetězec* (angl. *string*) je datový typ (druh *hodnot*),
který obsahuje text – třeba slovo nebo větu.

Když řetězec zadáváš do programu, musíš ho označit – uzavřít do
*uvozovek*, buď jednoduchých nebo dvojitých:

```python
'tohle je řetězec'
"tohle taky"
```

Je velký rozdíl mezi `print('cislo')` – vypiš slovo „cislo“ –
a `print(cislo)` – vypiš hodnotu výrazu `cislo`.
Jednou je `cislo` pět konkrétních písmen; podruhé *instrukce* k použití
proměnné.
Počítač, na rozdíl od lidí, rozdíl mezi textem a instrukcí nepozná z kontextu,
a tak je uvozovky potřeba používat důsledně.

{{ figure(
    img=static('quote-comic.svg'),
    alt='(Ilustrační komiks. Člověk říká robotovi: "Řekni Pavlovi, ať mi zavolá!". Robot odpoví: "PAVLOVI AŤ MI ZAVOLÁ!")',
) }}


## Znaky

Texty sestávají z jednotlivých písmenek.
Řetězce víceméně taky, ale aby bylo jasné, co přesně tím *písmenkem*
myslíme, říkáme, že řetězce sestávají ze *znaků* (angl. *characters*).

Takový znak může být písmenko (např. `A`) nebo číslice (`3`),
ale i jiný symbol (`!`).

Každý řetězec má určitý počet znaků.
Kolik, to zjistíš pomocí funkce `len()`.
Třeba řetězec `Ahoj!` má znaků pět:

```pycon
>>> len('Ahoj!')
5
```

Jeden ze zajímavějších znaků je *mezera*.
Je to taky znak. V řetězci se tedy chová stejně jako písmenko:

```pycon
>>> len(' ')
1
>>> len('K ní')
4
>>> len('3 + 2')
5
```

Mimochodem, řetězec může být i prázdný – pak má nula znaků:

```pycon
>>> len('')
0
>>> len("")
0
```


## Uvozovky

K uvození řetězce můžeš použít jednoduché nebo dvojité rovné uvozovky.
Není mezi nimi rozdíl.
Podobně `4.0` a `4.000` jsou dva zápisy téhož čísla,
tak `'slovo'` a `"slovo"` pro Python označuje stejnou
hodnotu, skládající se ze stejných pěti písmen.

Použité uvozovky nejsou součástí hodnoty – python si „nepamatuje“, jakým
způsobem byl řetězec uvozen.
Když má nějaký řetězec vypsat s uvozovkami, jedny si k tomu vybere – většinou
ty jednoduché:

```pycon
>>> "python"
'python'
>>> 'slovo'
'slovo'
```

> [note]
> Předchozí příklad je z interaktivního režimu Pythonu, který ukazuje hodnoty
> výrazů „programátorsky“ – pokud možno tak, jak se zapisují v Pythonu.
> Funkce `print()` vypisuje hodnoty „hezky“, „pro uživatele“ – v případě
> řetězců tedy bez uvozovek.


### Uvozovky v uvozovkách

Proč si při zadávání textu můžeš vybrat mezi dvěma druhy uvozovek?

Občas se stane, že v rámci textu potřebuješ použít samotnou uvozovku (nebo
apostrof).
Pak musíš „kolem“ řetězce použít tu druhou:

```python
print('Zpívala si: "Tralala!"')
print("Byl to Goa'uld, parazit z planety P3X-888")
```

Když v rámci textu použiješ stejnou uvozovku jako „kolem něj“, tak bude Python
naprosto zmatený.

```pycon
>>> len("Zpívala si: "Tralala"")
Traceback (most recent call last)
  File "<>", line 1
    len("Zpívala si: "Tralala"")
                      ^
SyntaxError: invalid syntax
```

Pokud používáš chytrý editor, doporučuju si zvyknout na to, jakou barvou
máš řetězce zvýrazněné.
Často to pomáhá odhalit chybky.


## Sekvence se zpětným lomítkem

Co dělat, když v řetězci potřebuješ *oba* druhy uvozovek,
jako ve větě `Vtom vnuk křik': "Hleď!"`?

Můžeš si pomoci tím, že spojíš dva řetězce:

```pycon
>>> print("Vtom vnuk křik': " + '"Hleď!"')
Vtom vnuk křik': "Hleď!"
```

Ale lepší způsob je použít speciální zápis se *zpětným lomítkem*.
Kdykoli se v řetězci objeví sekvence `\'` nebo `\"`, Python dá do řetězce danou
uvozovku.

```pycon
>>> print("Vtom vnuk křik': \"Hleď!\"")
Vtom vnuk křik': "Hleď!"
>>> print('"Jen ho nech," řek\' děd. "Kdo zná líp kraj?"')
"Jen ho nech," řek' děd. "Kdo zná líp kraj?"
```

Ve výsledném řetězci pak ovšem žádné zpětné lomítko *není*.
Sekvence `\'` je jen způsob, jak v Pythonu zadat `'` – jediný znak.
Tomu je celkem důležité porozumět.
Zkus si, jestli zvládneš předpovědět výsledek těchto výrazů:

```pycon
>>> print(".\".")
>>> len(".\".")
>>> ".\"."
```

{% filter solution %}
```pycon
>>> print(".\".")
.".
>>> len(".\".")
3
>>> ".\"."
'.".'
```
{% endfilter %}


Znaků, které se zadávají sekvencí se zpětným lomítkem, je více.
Jedna ze zajímavějších je `\t`, představující tabulátor – jediný znak, který
se, když ho vypíšeš, „roztáhne“ na víc mezer.

```pycon
>>> print("a\tb")   # Výpis "pro lidi"
a       b
>>> "a\tb"          # Výpis "pro programátory"
'a\tb'
>>> len("a\tb")     # Počet znaků v řetězci
3
```

Se zpětným lomítkem se dá zadat jakýkoli znak – včetně *emoji* – podle jména
(`\N{…}`) nebo identifikačního čísla (`\x..`, `\u....`, `\U........`)
standardu Unicode.
Stačí přesné jméno nebo číslo znát (nebo třeba dohledat na internetu).
V následujících řetězcích jsou takové znaky pro přehlednost mezi dvěma
pomlčkami `-`. Délka každého řetězce je tedy celkem 3:

```pycon
>>> print('-\N{GREEK CAPITAL LETTER DELTA}-')
-Δ-
>>> print('-\N{SECTION SIGN}-')
-§-
>>> print('-\N{GRINNING CAT FACE WITH SMILING EYES}-')
-😸-
>>> print('-\x60-')
-`-
>>> print('-\u30C4-')
-ツ-
>>> print('-\U0001F0BD-')
-🂽-
```


### Zpětné lomítko

Zpětné lomítko tedy začíná speciální sekvenci (známou pod anglickým
termínem *escape sequence*), kterou zadáš *jediný znak*.

Tahle vychytávka má jeden, někdy nepříjemný, důsledek: pokud chceš mít jako
součást řetězce zpětné lomítko (třeba ve jménech souborů na Windows),
nemůžeš použít přímo `\`.
Musíš použít speciální sekvenci `\\` – tedy lomítko zdvojit:

```python
print('C:\\PyLadies\\Nový adresář')
```

Podobně jako `\"` je zápis pro uvozovku a `\'` pro apostrof, sekvence `\\`
je zápis pro jedno zpětné lomítko.


### Nový řádek

Někdy potřebuješ řetězce, které obsahují více řádků.
Pythonní řetězce ale můžeš normálně napsat jen na *jeden* řádek.
(Python se tak snaží ulehčit hledání chyby, kdybys koncovou uvozovku
zapoměl{{a}}.)

Můžeš ale do řetězce znak pro nový řádek vložit pomocí sekvence `\n`:

```pycon
>>> print('Haló haló!\nCo se stalo?')
Haló haló!
Co se stalo?
```

Ono `\n` do řetězce vloží znak nového řádku.
Ten při výpisu ukončí stávající řádek a přejde na nový – ale jinak se chová
jako jakýkoli jiný znak:

```pycon
>>> print('-\n-')
-
-
>>> len('-\n-')
3
```


## Trojité uvozovky

Kromě `\n` je i druhý způsob, jak zadat řetězec se znakem nového řádku:
ohraničit ho *třemi* uvozovkami (jednoduchými nebo dvojitými)
na každé straně.
Dají se tak zadávat delší víceřádkové řetězce:

```python
basen = '''Haló haló!
Co se stalo?
Prase kozu potrkalo!'''
```

Víceřádkové řetězce se často používají jako dokumentační řetězce funkcí:

```python
def vynasob(a, b):
    """Vynásobí argumenty a vrátí výsledek.

    Oba argumenty by měly být čísla.
    """

    return a * b
```

Pozor na to, že pokud je tenhle řetězec
v odsazeném kódu, každý jeho řádek bude začínat
několika mezerami.
(V dokumentačních řetězcích tohle nevadí, tam se s odsazením počítá.)


## Cvičení

Jaká je délka těchto řetězců?

Výsledek zjistíš snadno, zkus se ale zamyslet a Python použít jen pro ověření.

{# Highlighted as plain text to avoid spoilers #}
```plain
{# 2, 3, 4, 5 -#}
print(len('ahoj'))
print(len("""Ahoj!"""))
print(len('a b'))
print(len( ' a b ' ))
print(len('\N{SNOWMAN}ové'))
print(len('a\nb'))
print(len('a\tb'))
print(len('"\'"'))

{# 3, 4, 5, 6 #}
print(len("""
abc"""))

{# 3, 5, 7, 9 #}
if True:
    print(len("""a
    b"""))

{# 7, 8, 9, more #}
print(len('C:\new_dir'))

print(len(f'{print}'))
```
