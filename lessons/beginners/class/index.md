# Hodnoty a objekty

Než se dnes začneme zabývat třídami,
podíváme na objekty.

Co pro programátory znamená slovo *objekt*?

V Pythonu je to jednoduché – každá hodnota
(tj. něco, co můžeš uložit do proměnné, vrátit
z funkce nebo třeba seznamu) je objekt.
Některé jazyky (třeba Javascript, C++ nebo Java) mají
i jiné hodnoty než objekty, v některých
jazycích (třeba v C) objekty vůbec nejsou.
Ale v Pythonu mezi hodnotou a objektem není rozdíl,
takže je na jednu stranu trošku složitější pochopit,
v čem spočívá ta „objektovitost“, ale na druhou stranu
to zase není potřeba vědět do detailů.

Základní vlastnost objektů je to, že obsahují jak data
(informace), tak *chování* – instrukce nebo metody,
které s těmito daty pracují.
Třeba řetězce v Pythonu obsahují jak informace
(nějakou sekvenci znaků), tak užitečné metody jako
`upper` nebo `count`.
Kdyby řetězce nebyly objekty, musel by Python mít
spoustu funkcí jako `str_upper` a `str_count`.
Objekty spojují data a funkčnost dohromady.

> [note]
> Možná namítneš, že třeba `len` je funkce.
> Je to tak, Python není „stoprocentně“ objektový jazyk.
> Funkce `len` ale funguje i na
> objektech, které s řetězci nemají nic společného.

# Třídy

Data každého objektu jsou specifická pro konkrétní
objekt (`"abc"` obsahuje jiné znaky než
`"def"`), ale funkčnost – metody – bývají
společné pro všechny objekty daného typu.
Třeba řetězcová metoda `count()` by se dala
napsat zhruba jako:

```python
def count(input_string, character):
    quantity = 0
    for c in input_string:
        if c == character:
            quantity = quantity + 1
    return quantity
```

… a ačkoliv bude vracet jinou hodnotu pro každý řetězec,
samotná metoda je společná všem řetězcům.

Tohle společné chování určuje
*typ* (angl. *type*) neboli *třída* (angl. *class*) daného objektu.

> [note]
> V historických verzích Pythonu byl rozdíl mezi „typem“
> a „třídou“, ale dnes už jsou to synonyma.

Typ objektu umí zjistit funkce `type`:

```pycon
>>> type(0)
<class 'int'>
>>> type(True)
<class 'bool'>
>>> type("abc")
<class 'str'>
>>> with open('file.txt') as f:
...     type(f)
... 
<class '_io.TextIOWrapper'>
```

Takže `type` vrací nějaké třídy.
A co je to třída? Popis, jak se chovají všechny objekty
daného typu.

Většinu tříd jde navíc v Pythonu zavolat, jako by
to byly funkce, a vytvořit tak nový objekt dané třídy:

```pycon
>>> class_of_strings = type("abc")
>>> class_of_strings(8)
'8'
>>> class_of_strings([1, 2, 3])
'[1, 2, 3]'
```

Chová se to stejně jako funkce `str`! Není to podivné?

Tady se musím omluvit:
[materiály k funkcím](../functions/)
tak trochu lhaly. Funkce `str`, `int`, `float` apod. totiž vůbec
nejsou funkce – jsou to právě třídy.

```pycon
>>> str
<class 'str'>
>>> type('abcdefgh')
<class 'str'>
>>> type('abcdefgh') == str
True
```

Ale dají se, podobně jako funkce, zavolat.
Třída tedy většinou obsahuje nejen „popis“, jak se
objekty daného typu budou chovat, ale umí i objekty
daného typu vytvořit.

## Vlastní třídy

A proč najednou tolik informací o třídách?
Protože si zkusíme napsat třídu vlastní.

Třídu se hodí napsat, když plánuješ mít ve svém
programu více objektů s podobným chováním.
Třeba karetní hra by mohla mít třídu Karta,
webová aplikace třídu Uživatel,
tabulkový procesor třídu Řádek.

My teď potřebujeme napsat program o zvířátkách.
Začni tím, že napíšeš třídu pro koťátka, která umí mňoukat:

```python
class Kitten:
    def meow(self):
        print("Meow!")
```

Tak jako se funkce definují pomocí `def`,
třídy mají klíčové slovo `class`,
za které napíšeš jméno třídy, dvojtečku,
a pak odsazené tělo třídy.
Podobně jako `def` dělá funkce, příkaz
`class` udělá novou třídu a přiřadí ji
do proměnné daného jména (tady `Kitten`).

Třídy se tradičně pojmenovávají s velkým písmenem,
aby se nepletly s „normálními“ hodnotami.

> [note]
> Základní třídy (`str`, `int` atd.)
> velká písmena nemají, a to hlavně z historických
> důvodů – původně to byly opravdu funkce.

V těle třídy můžeš definovat metody, které vypadají
úplně jako funkce – jen mají první argument `self`.
Ten si ale vysvětlíme později – zamňoukání má přednost:

```python
# Vytvoření konkrétního objektu
kitten = Kitten()

# Volání metody
kitten.meow()
```

V tomhle příkladu si dej pozor na velikost písmen:
`Kitten` (s velkým K) je třída – popis, jak
se koťátka chovají. `kitten` (s malým k)
je konkrétní objekt (angl. *instance*) té třídy:
hodnota, která reprezentuje kotě.
Onen konkrétní objekt vytvoříme zavoláním třídy,
stejně jako zavoláním `str()` se dá vytvořit
konkrétní řetězec.

Meow!

## Atributy

Objekty vytvořené z „vlastních“ tříd mají jednu
vlastnost, kterou třídy jako `str`
nedovolují: možnost si definovat vlastní
*atributy* – informace, které se uloží k danému
objektu.
Atributy se označují tak, že mezi hodnotu a jméno
jejího atributu napíšeš tečku:

```python
mourek = Kitten()
mourek.name = 'Mourek'

micka = Kitten()
micka.name = 'Micka'

print(mourek.name)
print(micka.name)
```

Na začátku jsme si řekl{{gnd('i', 'y', both='i')}}, že objekty spojují chování
a data.
Chování je definováno ve třídě, data se schovávají
právě v atributech jednotlivých objektů.
Podle atributů jako jméno můžeš jednotlivá koťátka
rozlišit.

> [note]
> Asi sis všiml{{a}}, že tečkou se dostaneš jak k metodám
> převzaným z třídy, tak k atributům specifickým
> pro konkrétní objekt.
> Co se stane, když má atribut stejné jméno jako
> metoda z třídy? Vyzkoušej si to:
>
> ```python
> micka = Kitten()
> micka.meow = 12345
> micka.meow()
> ```

## Parametr `self`

A teď se na chvíli vrátíme k metodám,
konkrétně k parametru `self`.

Každá metoda má přístup ke konkrétnímu objektu, na
kterém pracuje, právě přes argument `self`.
Teď, když máš koťátka pojmenovaná,
můžeš pomocí `self` rozjet dialog:

```python
class Kitten:
    def meow(self):
        print("{}: Meow!".format(self.name))

mourek = Kitten()
mourek.name = 'Mourek'

micka = Kitten()
micka.name = 'Micka'

mourek.meow()
micka.meow()
```

Co se stalo? Výraz `mourek.meow` udělá *metodu*, která, když ji zavoláš,
předá objekt `mourek` jako první argument
funkce `meow`.

> [note]
> Tohle je to, čím se *metoda* liší od normální *funkce*:
> metoda si „pamatuje“ objekt, na kterém pracuje.

A takový první argument, který obsahuje konkrétní
objekt právě definované třídy, se tradičně pojmenovává `self`.
(Když ho pojmenuješ jinak, ostatní programátoři se na tebe budou koukat hodně
divně.)


A může taková metoda brát víc než jeden argument?
Může – `self` se doplní na první místo,
a zbytek argumentů se vezme z volání metody.{} mi chutná
        print("{}: Meow!".format(self.name))

```python
def eat(self, food):
    print("{}: Meow meow! I like {}!".format(self.name, food))

mourek = Kitten()
mourek.name = 'Mourek'
mourek.eat('fish')
```


## Metoda `__init__`

A když jsme u argumentů, je ještě jedno místo,
kde můžeš třídě poslat argumenty: když vytváříš
nový objekt (voláním třídy).
Dá se tak hezky vyřešit problém, který možná vidíš
v předchozím kódu: aktuálně každé koťátko potřebuje,
aby se mu po vytvoření nastavilo jméno, jinak
metoda `meow` nebude fungovat.
Třída se ale dá udělat i tak, že půjde jméno nastavit
už při vytváření, takhle:

```python
mourek = Kitten(name='Mourek')
```

Na tohle používá Python metodu,
která se jmenuje `__init__` (dvě podtržítka,
`init`, dvě podtržítka).
To „opodtržítkování“ znamená, že tohle jméno je nějakým způsobem speciální.
Metoda `__init__` se totiž zavolá
automaticky, když se vytvoří nový objekt.
Dá se tedy napsat:

```python
class Kitten:
    def __init__(self, name):
        self.name = name

    def meow(self):
        print("{}: Meow!".format(self.name))

    def eat(self, food):
        print("{}: Meow meow! I like {}!".format(self.name, food))

mourek = Kitten('Mourek')
mourek.meow()
```

A teď už není možnost, jak vytvořit koťátko bez jména,
takže `meow` bude vždycky fungovat.

Podobných „opodtržítkovaných“ metod je víc,
třeba `__str__` se volá, když je potřeba
převést objekt na řetězec:

```python
class Kitten:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return '<Kitten named {}>'.format(self.name)

    def meow(self):
        print("{}: Meow!".format(self.name))

    def eat(self, food):
        print("{}: Meow meow! I like {}!".format(self.name, food))

mourek = Kitten('Mourek')
print(mourek)
```

## Cvičení: Cat

Teď, když už umíš dělat koťátka, zkus vytvořit třídu pro kočku.

- Kočka umí mňoukat metodou `meow`.
- Kočka má na začátku (při vytvoření) 9 životů
(nemůže mít nikdy víc než 9 nebo míň než 0!).
- Kočka umí říct, jestli je živá (nemá 0 životů), metodou `is_alive`.
- Kočka může ztratit život metodou `lose_life`.
- Kočku můžeš nakrmit metodou `eat`, která bere 1 argument -
nějaké konkrétní jídlo (řetězec). Pokud je toto jídlo `"fish"`, kočce se obnoví
jeden život (pokud teda už není mrtvá, nebo nemá maximální počet životů).

{% filter solution %}
```python
class Cat:
    def __init__(self):         # Init funkce nemusi brat jako parametr
        self.number_of_lives = 9   # pocet zivotu, ten je pokazde 9.

    def meow(self):
        print("Moew, moew, meooooow!")

    def is_alive(self):
        return self.number_of_lives > 0

    def lose_life(self):
        if not self.is_alive():
            print("Cannot kill dead cat!")
        else:
            self.number_of_lives -= 1

    def eat(self, food):
        if not self.is_alive():
            print("It is pointless to feed dead cat!")
            return
        if food == "fish" and self.number_of_lives < 9:
            self.number_of_lives += 1
            print("Cat ate fish and gained one.")
        else:
            print("Cat is eating.")
```
{% endfilter %}

A to je o samotných třídách zatím vše.
[Příště](../inheritance/) si něco řekneme o dědičnosti.
A o štěňátkách.
