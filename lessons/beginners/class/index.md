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
> V jiných jazycích než Python 3 můžou slova „typ“ a „třída“ označovat různé
> věci. Pro nás to budou synonyma.

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

A co je to třída? Třída je *popis*, jak se všechny objekty
daného typu chovají.

Například `<class 'int'>` obsahuje všechno, co je společné všem celým číslům:
že (a jak) se dají sčítat, jak takové číslo převést na řetězec, a tak dále.


## Tvoření objektů třídy

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
nejsou funkce – jsou to právě třídy:

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
její objekty budou chovat, ale „umí“ takové objekty i vytvořit.

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
za které napíšeš jméno třídy, dvojtečku a pak odsazené tělo třídy.
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
úplně jako funkce – jen mají první parametr `self`.
Ten si ale vysvětlíme později – napřed zkus zamňoukat:

```python
# Vytvoření konkrétního objektu
kotatko = Kotatko()

# Volání metody
kotatko.zamnoukej()
```

V tomhle příkladu si dej pozor na velikost písmen:
`Kotatko` (s velkým K) je třída – popis, jak
se koťátka chovají.
`kotatko` (s malým k)
je konkrétní objekt (angl. *instance*) té třídy:
hodnota, která reprezentuje kotě.

Když definuješ třídu (pomocí bloku `class`), neznamená to zatím, že ve tvém
programu je nějaké koťátko.
Třída je jako recept nebo manuál: když si koupíš kuchařku, budeš teoreticky
vědět jak upéct dort, jak bude takový dort vypadat a že se dá sníst.
Ale neznamená to ještě, že máš samotný dort!

Konkrétní objekt vytvoříš až zavoláním třídy.
Stejně jako zavoláním `str()` se dá vytvořit konkrétní řetězec,
volání `Kotatko()` vytvoří nový objekt tvé třídy, který už můžeš použít.

Mňau!

## Atributy

Objekty vytvořené z „vlastních“ tříd mají funkčnost, kterou třídy jako `str`
nedovolují: máš možnost si definovat vlastní
*atributy* – informace, které se uloží k danému objektu.
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
Chování je definováno ve třídě; data se schovávají
právě v atributech jednotlivých objektů.
Podle atributů jako `jmeno` pak můžeš jednotlivá koťátka
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

Teď se na chvíli vraťme k metodám. Konkrétně k parametru `self`.

Každá metoda má přístup ke konkrétnímu objektu, na
kterém pracuje, právě přes argument `self`.
Teď, když máš koťátka pojmenovaná, můžeš v metodě `zamnoukej` použít `self`
a dostat se tak ke jménu daného koťátka:

```python
class Kotatko:
    def zamnoukej(self):
        print(f"{self.jmeno}: Mňau!")

mourek = Kotatko()
mourek.jmeno = 'Mourek'

micka = Kotatko()
micka.jmeno = 'Micka'

mourek.zamnoukej()
micka.zamnoukej()
```

Co se stalo? Výraz `mourek.zamnoukej` udělá *metodu*.
Když ji pak zavoláš (`mourek.zamnoukej()`),
objekt `mourek` se předá funkci `zamnoukej` jako první argument, `self`.

> [note]
> Onen první argument metody můžeš teoreticky pojmenovat i jinak než `self`,
> ale když to uděláš, ostatní programátoři se na tebe budou koukat hodně divně.


Může taková metoda brát víc než jeden argument?
Může – `self` se doplní na první místo,
zbytek argumentů se vezme z volání metody.
Třeba:

```python
class Kotatko:
    def zamnoukej(self):
        print(f"{self.jmeno}: Mňau!")

    def snez(self, jidlo):
        print(f"{self.jmeno}: Mňau mňau! {jidlo} mi chutná!")

mourek = Kotatko()
mourek.jmeno = 'Mourek'
mourek.snez('ryba')
```

## Metoda `__init__`

Co se stane, když koťátku zapomeneš nastavit jméno?
Metoda `zamnoukej` přestane fungovat:

```pycon
>>> micka = Kotatko()
>>> micka.snez('ryba')
Traceback (most recent call last):
  File "<zvirata.py>", line 5, in snez
AttributeError: 'Kotatko' object has no attribute 'jmeno'
```

Aby tahle chyba nemohla nastat, můžeš zařídit, aby každé kotě *muselo* být
pojmenované – a to už od okamžiku kdy vznikne.
Jméno pak budeš zadávat už při vytváření kotěte, nějak takhle:

```python
mourek = Kotatko(jmeno='Mourek')
```

To ale zatím nefunguje; musíš na to třídu `Kotatko` připravit.

Použij na to speciální metodu, která se jmenuje `__init__` (dvě podtržítka,
`init`, dvě podtržítka).
To „opodtržítkování“ znamená, že tohle jméno je nějakým způsobem speciální.
Metodu `__init__` totiž Python zavolá
automaticky, když vytvoří nový objekt.
Můžeš tedy napsat:

```python
class Kotatko:
    def __init__(self, jmeno):
        self.jmeno = jmeno

    def zamnoukej(self):
        print(f"{self.jmeno}: Mňau!")

    def snez(self, jidlo):
        print(f"{self.jmeno}: Mňau mňau! {jidlo} mi chutná!")

mourek = Kotatko('Mourek')
mourek.zamnoukej()
```

A teď už není možnost, jak vytvořit koťátko beze jména.
Metoda `zamnoukej` bude vždycky fungovat.

Jako u jiných funkcí je možné jméno koťátka zadat buď jako pojmenovaný
argument, nebo jako poziční. Obojí funguje stejně:

```
mourek = Kotatko('Mourek')  # 'Mourek' je hodnota prvního argument pro __init__ (po self)
micka = Kotatko(jmeno='Micka')  # 'Micka' je hodnota argumentu `jmeno`
```

### Metoda `__str__`

Podobných „opodtržítkovaných“ (speciálních) metod je víc.
Třeba metodu `__str__` Python zavolá, když je potřeba
převést objekt na řetězec:

```python
class Kotatko:
    def __init__(self, jmeno):
        self.jmeno = jmeno

    def __str__(self):
        return f'<Kotatko jmenem {self.jmeno}>'

    def zamnoukej(self):
        print(f"{self.jmeno}: Mňau!")

    def snez(self, jidlo):
        print(f"{self.jmeno}: Mňau mňau! {jidlo} mi chutná!")

mourek = Kotatko('Mourek')
print(mourek)
```


A to je o samotných třídách zatím vše.
[Příště](../inheritance/) si něco řekneme o dědičnosti.
A o štěňátkách.
