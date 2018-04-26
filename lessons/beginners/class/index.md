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
def count(retezec, znak):
    pocet = 0
    for c in retezec:
        if c == znak:
            pocet = pocet + 1
    return pocet
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
>>> with open('soubor.txt') as f:
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
>>> trida_retezcu = type("abc")
>>> trida_retezcu(8)
'8'
>>> trida_retezcu([1, 2, 3])
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
class Kotatko:
    def zamnoukej(self):
        print("Mňau!")
```

Tak jako se funkce definují pomocí `def`,
třídy mají klíčové slovo `class`,
za které napíšeš jméno třídy, dvojtečku,
a pak odsazené tělo třídy.
Podobně jako `def` dělá funkce, příkaz
`class` udělá novou třídu a přiřadí ji
do proměnné daného jména (tady `Kotatko`).

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
kotatko = Kotatko()

# Volání metody
kotatko.zamnoukej()
```

V tomhle příkladu si dej pozor na velikost písmen:
`Kotatko` (s velkým K) je třída – popis, jak
se koťátka chovají. `kotatko` (s malým k)
je konkrétní objekt (angl. *instance*) té třídy:
hodnota, která reprezentuje kotě.
Onen konkrétní objekt vytvoříme zavoláním třídy,
stejně jako zavoláním `str()` se dá vytvořit
konkrétní řetězec.

Mňau!

## Atributy

Objekty vytvořené z „vlastních“ tříd mají jednu
vlastnost, kterou třídy jako `str`
nedovolují: možnost si definovat vlastní
*atributy* – informace, které se uloží k danému
objektu.
Atributy se označují tak, že mezi hodnotu a jméno
jejího atributu napíšeš tečku:

```python
mourek = Kotatko()
mourek.jmeno = 'Mourek'

micka = Kotatko()
micka.jmeno = 'Micka'

print(mourek.jmeno)
print(micka.jmeno)
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
> micka = Kotatko()
> micka.zamnoukej = 12345
> micka.zamnoukej()
> ```

## Parametr `self`

A teď se na chvíli vrátíme k metodám,
konkrétně k parametru `self`.

Každá metoda má přístup ke konkrétnímu objektu, na
kterém pracuje, právě přes argument `self`.
Teď, když máš koťátka pojmenovaná,
můžeš pomocí `self` rozjet dialog:

```python
class Kotatko:
    def zamnoukej(self):
        print("{}: Mňau!".format(self.jmeno))

mourek = Kotatko()
mourek.jmeno = 'Mourek'

micka = Kotatko()
micka.jmeno = 'Micka'

mourek.zamnoukej()
micka.zamnoukej()
```

Co se stalo? Výraz `mourek.zamnoukej` udělá *metodu*, která, když ji zavoláš,
předá objekt `mourek` jako první argument
funkce `zamnoukej`.

> [note]
> Tohle je to, čím se *metoda* liší od normální *funkce*:
> metoda si „pamatuje“ objekt, na kterém pracuje.

A takový první argument, který obsahuje konkrétní
objekt právě definované třídy, se tradičně pojmenovává `self`.
(Když ho pojmenuješ jinak, ostatní programátoři se na tebe budou koukat hodně
divně.)


A může taková metoda brát víc než jeden argument?
Může – `self` se doplní na první místo,
a zbytek argumentů se vezme z volání metody.
Třeba:

```python
class Kotatko:
    def zamnoukej(self):
        print("{}: Mňau!".format(self.jmeno))

    def snez(self, jidlo):
        print("{}: Mňau mňau! {} mi chutná!".format(self.jmeno, jidlo))

mourek = Kotatko()
mourek.jmeno = 'Mourek'
mourek.snez('ryba')
```

## Metoda `__init__`

A když jsme u argumentů, je ještě jedno místo,
kde můžeš třídě poslat argumenty: když vytváříš
nový objekt (voláním třídy).
Dá se tak hezky vyřešit problém, který možná vidíš
v předchozím kódu: aktuálně každé koťátko potřebuje,
aby se mu po vytvoření nastavilo jméno, jinak
metoda `zamnoukej` nebude fungovat.
Třída se ale dá udělat i tak, že půjde jméno nastavit
už při vytváření, takhle:

```python
mourek = Kotatko(jmeno='Mourek')
```

Na tohle používá Python metodu,
která se jmenuje `__init__` (dvě podtržítka,
`init`, dvě podtržítka).
To „opodtržítkování“ znamená, že tohle jméno je nějakým způsobem speciální.
Metoda `__init__` se totiž zavolá
automaticky, když se vytvoří nový objekt.
Dá se tedy napsat:

```python
class Kotatko:
    def __init__(self, jmeno):
        self.jmeno = jmeno

    def zamnoukej(self):
        print("{}: Mňau!".format(self.jmeno))

    def snez(self, jidlo):
        print("{}: Mňau mňau! {} mi chutná!".format(self.jmeno, jidlo))

mourek = Kotatko('Mourek')
mourek.zamnoukej()
```

A teď už není možnost, jak vytvořit koťátko bez jména,
takže `zamnoukej` bude vždycky fungovat.

Podobných „opodtržítkovaných“ metod je víc,
třeba `__str__` se volá, když je potřeba
převést objekt na řetězec:

```python
class Kotatko:
    def __init__(self, jmeno):
        self.jmeno = jmeno

    def __str__(self):
        return '<Kotatko jmenem {}>'.format(self.jmeno)

    def zamnoukej(self):
        print("{}: Mňau!".format(self.jmeno))

    def snez(self, jidlo):
        print("{}: Mňau mňau! {} mi chutná!".format(self.jmeno, jidlo))

mourek = Kotatko('Mourek')
print(mourek)
```

## Cvičení: Kočka

Teď, když už umíš dělat koťátka, zkus vytvořit třídu pro kočku.

- Kočka umí mňoukat metodou `zamnoukej`.
- Kočka má na začátku (při vytvoření) 9 životů
(nemůže mít nikdy víc než 9 nebo míň než 0!).
- Kočka umí říct, jestli je živá (nemá 0 životů), metodou `je_ziva`.
- Kočka může ztratit život metodou `uber_zivot`.
- Kočku můžeš nakrmit metodou `snez`, která bere 1 argument -
nějaké konkrétní jídlo (řetězec). Pokud je toto jídlo `"ryba"`, kočce se obnoví
jeden život (pokud teda už není mrtvá, nebo nemá maximální počet životů).

{% filter solution %}
```python
class Kocka:
    def __init__(self):         # Init funkce nemusi brat jako parametr
        self.pocet_zivotu = 9   # pocet zivotu, ten je pokazde 9.

    def zamnoukej(self):
        print("Mnau, mnau, mnauuu!")

    def je_ziva(self):
        return self.pocet_zivotu > 0

    def uber_zivot(self):
        if not self.je_ziva():
            print("Nemuzes zabit uz mrtvou kocku!")
        else:
            self.pocet_zivotu -= 1

    def snez(self, jidlo):
        if not self.je_ziva():
            print("Je zbytecne krmit mrtvou kocku!")
            return
        if jidlo == "ryba" and self.pocet_zivotu < 9:
            self.pocet_zivotu += 1
            print("Kocka spapala rybu a obnovil se ji jeden zivot.")
        else:
            print("Kocka se krmi.")
```
{% endfilter %}

A to je o samotných třídách zatím vše.
[Příště](../inheritance/) si něco řekneme o dědičnosti.
A o štěňátkách.
