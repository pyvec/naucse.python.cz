Magie
=====

Co z Pythonu dělá tak užitečný jazyk?
Z velké části je to zaměření na čitelnost kódu. Pythonu se někdy říká „spustitelný pseudokód“: syntaxe je inspirovaná zápisem abstraktních algoritmů v matematice, používá se málo speciálních znaků jako $, <<, &&, ?.
Čitelnosti je podřízena expresivita (proto v Pythonu nenajdeme makra jako v Lispu) i délka zápisu (některé věci se nedají napsat na jeden řádek).

Návrh jazyka (a knihoven pro něj) se řídí mimo jiné poučkou „There should be one– and preferably only one –obvious way to do it.“
Existuje ideálně jeden *zjevně nejlepší* způsob, jak dosáhnout určité funkčnosti.
Úkolem programátora je tento způsob najít a použít. Náš cíl by měl být kód, který ostatní programátoři pochopí na první pohled. A pokud je to možné, měli by ho pochopit i neprogramátoři. Není mezi nimi pevná hranice – váš kód můžou číst lidi, kteří programovací jazyk v životě neviděli; programátoři silní v jiných jazycích; průměrní Pythonisté; nebo ostřílení veteráni. Čím víc jich dokáže kód pochopit, tím bude váš kód udržovatelnější.

S tím souvisí koncept „magie“. Magie je něco, co funguje, ačkoli tomu nerozumíme. Pro každého čtenář kódu může být magie něco jiného: pro začátečníka bude nepochopitelný zápis `zip(*args)`, matematik nemusí chápat princip dědičnosti tříd, ostřílený Pythonista nemusí chápat maticovou matematiku, neprogramátor netuší, jak funguje mobil nebo webová aplikace. Je to tedy subjektivní pojem, ale lze ho zobjektivnit: čím méně lidí váš kód pochopí, tím je kód magičtější.

Magie, která *funguje*, nevadí. Věci které nechápu, můžu stále používat – jen nevím jak fungují, a tudíž je neumím *opravit*. Problém nastane až v momentě, kdy se něco pokazí.

Přehlednost a udržitelnost kódu je samozřejmě potřeba vyvážit s ostatními aspekty. Kód musí být například dostatečně rychlý, a optimalizace ho často znepřehlední. Proto je dobré optimalizovat až potom, co vím, že je kód *správný* a řeší opravdu problém, který potřebuji vyřešit. V ten moment napíšu testy, a potom, když je potřeba, můžu optimalizovat – trochu přehlednosti vyměnit za rychlost.

Na jiný důvod, proč použít méně pochopitelné techniky, narazíme při psaní knihoven a frameworků. To je kód, který používá hodně programátorů – a často jsou to programátoři s méně zkušenostmi, než mají autoři knihovny. Tady proto bývá dobré občas použít nějakou tu magii – znepřehlednit kód knihovny, aby kód který knihovnu *používá*, mohl být přehlednější.

Typický příklad jsou dekorátory ve Flasku. Napsat dekorátor není úplně triviální, ale velice to zjednodušuje práci všem, co ve Flasku píšou web. Konstrukce `@app.route` je pro většinu lidí magická – nevíme přesně, co to dělá, ale to nám nebrání ji použít.


Velká moc a velká zodpovědnost
------------------------------

Druhý možný význam slova *magie* je něco, co neodpovídá „normálnímu“ chování podobných věcí.

Jazyk Python standardizuje syntaxi relativně malého počtu operací (operátory, volání funkcí, atributy, ...), způsobů řízení toku programu (cykly, `with`, ...) a strukturování kódu (moduly, `def`, `class`).
To, že je jich relativně málo, má dvě výhody: zaprvé fungují s ostatními části jazyka, a zadruhé nebývá problém rozhodnout, který způsob je pro daný problém nejlepší.

Téměř všechno v Pythonu ale jde předefinovat. Operátor `/` nemusí jen dělit: můžu si napsat třídu pro jméno souboru, která umí pomocí `/` oddělovat adresáře \*.
Cyklus `for` nemusí iterovat přes předem danou sekvenci prvků; iterovatelný objekt může poskytovat jakékoli hodnoty podle jakýchkoli pravidel.
Příkaz `class` dokonce vůbec nemusí vytvořit třídu, jak uvidíme později.

Ačkoliv si ale můžeme dovolit téměř cokoli, je dobré mít na paměti, že odchylky od „normálního“ chování jsou *magické*. Jakmile někdo použije divnou třídu, která předefinovává dělení, ve svém kódu, musí každý čtenář toho kódu nejen opustit představu o tom, co operátor `/` dělá, ale hlavně si předtím uvědomit, že `/` *může* dělat něco divného. To samé platí u „divných“ iterovatelných objektů nebo tříd. Odchylka od normálního chování, je-li nezbytná, by měla být dobře promyšlená a zdokumentovaná.

Nadefinujeme-li vlastní nestandardní – „magické“ – chování některých objektů, často se stane, že nebudou fungovat s ostatními prvky jazyka tak dobře, jako to co je zabudované. Předefinujeme-li `<` tak, že nebude mít nic společného s porovnáváním, bude se funkce `sorted` chovat podivně. Když u svých objektů předefinuji přístup k atributům, pravděpodobně přestane fungovat `dir()`.
Zvlášť složité je promyslet interakci několika „magických“ principů mezi sebou.

Následující principy proto není dobré při psaní knihoven používat příliš často.

\* *Taková třída dokonce [existuje ve standardní knihovně](https://docs.python.org/3/library/pathlib.html).*


Speciální metody
----------------

Základní způsob, jak přizpůsobit chování objektů, jsou *speciální metody*.
Asi už víte, že všechny atributy, které začínají a končí dvojitým podtržítkem, jsou rezervované pro samotný Python, který je používá podle svých pravidel – například danou metodu volá, když je potřeba sečíst dvě čísla.

Speciální metody jsou popsané v [dokumentaci](https://docs.python.org/3/reference/datamodel.html#special-method-names). Zde uvedu jen přehled, který pokročilý Pythonista nosí v hlavě, aby věděl co je všechno možné.
Doporučuji si předtím, než nějakou naimplementujete, dokumentaci přečíst.

Metody pro předefinování aritmetických operátorů:
`__add__`, `__sub__`, `__mul__`, `__div__`, `__floordiv__`, `__pow__`, `__matmul__`, `__lshift__`, `__rshift__`, `__or__`, `__xor__` a varianty s `r` a `i` (`__radd__`, `__iadd__`, atd.)
`__neg__`, `__pos__`, `__abs__`, `__invert__`.

Metody pro předefinování porovnávání:
`__eq__`, `__ne__`, `__lt__`, `__gt__`, `__le__`, `__ge__`, `__hash__`.

Metoda pro zavolání objektu jako funkce:
`__call__`.

Metody pro funkčnost sekvencí a kontejnerů:
`__len__`, `__iter__`, `__next__`, `__reversed__`; `__contains__` pro operátor `in`.

Metody pro „hranaté závorky“:
`__getitem__`, `__setitem__`, `__delitem__`.

Převádění na řetězce:
`__repr__`, `__str__`, `__format__`.

Převádění na čísla:
`__complex__`, `__float__`, `__index__`, `__round__`, `__floor__`, `__ceil__`.

Převádění na `bool` (např. i v `if`):
`__bool__`.

Vytváření a rušení objektů:
`__new__` (konstruktor – *vytvoří* objekt dané třídy), `__init__` (*inicializuje* objekt dané třídy), `__del__` (zavoláno před *zrušením* objektu).

Předefinování přístupu k atributům:
`__getattr__` (zavolá se, pokud se atribut nenajde), `__getattribute__` (zavolá se pro *každý* přístup k atributu), `__setattr__`, `__delattr__`, `__dir__`.

Implementace *context manageru*:
`__enter__`, `__exit__`.

Implementace deskriptoru (viz níže):
`__get__`, `__set__`, `__delete__`.

Implementace asynchronní funkcionality:
`__await__`, `__aiter__`, `__anext__`, `__aenter__`, `__aexit__`.

Předefinování hierarchie dědičnosti:
`__instancecheck__`, `__subclasscheck__`.


Dekorátory
----------

Další věc, na kterou se podíváme, jsou *dekorátory* – způsob, jak si
přizpůsobovat funkce.

Nejjednodušší použití dekorátorů je *registrace*: to, co dělá Flask
se svým `app.route`.
K funkci přidáme dekorátor, a funkce se někam uloží.

Pro příklad budeme chtít udělat dekorátor pro kalkulačku,
`@register_operator`, aby fungoval tento kód:

```python
operators = {}

@register_operator
def add(a, b):
    return a + b

@register_operator
def mul(a, b):
    return a * b


a = int(input('First number: '))
operator_name = input('Operation: ')
b = int(input('Second number: '))

func = operators[operator_name]
print(func(a, b))
```

Bez použití dekorátorů by se to dalo napsat takto:

```python
def register_operator(func):
    operators[func.__name__] = func

def add(a, b):
    return a + b

register_operator(add)
```

S použitím dekorátoru je funkce `register_operator` téměř stejná,
jen použijeme speciální syntaxi se zavináčem.

```python
def register_operator(func):
    operators[func.__name__] = func
    return func

@register_operator
def add(a, b):
    return a + b

```

Použití dekorátoru je jen zkrácený zápis pro volání funkce – zápis
s dekorátorem je ekvivalentní tomuto:

```python
def add(a, b):
    return a + b

add = register_operator(add)
```

Chování samotného `@` je tedy celkem triviální.
Magie (složitost) spočívá v tom, že dekorátor je většinou funkce vyššího řádu:
bere jinou funkci jako argument, a taky jinou funkci vrací.
V případě registrace vrací stejnou funkci jako dostala – ale to není povinné.

Často se setkáme s dekorátory, které dekorovanou funkci nějak modifikují.
Například můžeme napsat dekorátor, který dělá něco velice nepythonistického:
zkontroluje, že argumenty funkce jsou konkrétního typu.
Dělá to tak, že definuje *novou funkci*, která volá tu původní – ale kromě
toho dělá i něco jiného.


```python
def check_ints(func):
    def outer_function(a, b):
        if not isinstance(a, int) or not isinstance(b, int):
            raise TypeError('only int is supported')
        return func(a, b)
    return outer_function

@check_ints
def add(a, b):
    return a + b

print(add(1, 2))
print(add(1.0, 2.0))
```

Takto funguje většina dekorátorů, které nějak mění chování dané funkce:
nadefinují funkci novou.
S tím ale narazí na jeden problém: nově nadefinovaná funkce má vlastní jméno
(a dokumentační řetězec, a podobné informace), což kazí iluzi, že jsme
původní funkci jen trošku změnili:

```python
print(add)
```

Řešení je použít *další dekorátor* – `functools.wraps`, který zkopíruje
jméno, dokumentační řetězec, atd. z jedné funkce na druhou.

```python
import functools

def check_ints(func):
    @functools.wraps(func)
    def outer_function(a, b):
        if not isinstance(a, int) or not isinstance(b, int):
            raise TypeError('only int is supported')
        return func(a, b)
    return outer_function
```

Zde je vidět, že jako dekorátor můžeme použít libovolný výraz – dokonce
i volání jiné funkce.
Budeme-li chtít napsat dekorátor, který tohle umí, potřebujeme opět
napsat funkci vyššího řádu – totiž funkci, která po zavolání vrátí dekorátor
(tj. další funkci).

```python
operators = {}

def register_operator(name):
    def decorator(func):
        operators[name] = func
        return func
    return decorator

@register_operator('+')
def add(a, b):
    return a + b

@register_operator('*')
def mul(a, b):
    return a * b

a = int(input('First number: '))
operator_name = input('Operation: ')
b = int(input('Second number: '))

func = operators[operator_name]
print(func(a, b))
```

Řádek `@register_operator('+')` dělá to stejné, jako bychom hned za funkcí
napsali `add = register_operator('+')(add)`

Budete-li chtít napsat dekorátor, který bere argumenty, a přitom ještě
„mění“ dekorovanou funkci, dostanete se na tři funkce zanořené v sobě.

XXX: Ukázka?
XXX: Dekorátor třídy


Deskriptory
-----------

Jeden z nejmagičtějších operátorů v Pythonu je `.`, tečka.
Je magický v obou významech – většina lidí ho používá, ačkoli nemá tušení, co přesně dělá, a dá se předefinovat tolika různými způsoby, že to vydá na [celou přednášku](https://www.youtube.com/watch?v=NiSqG6s8skA).

Pomocí tečky zapisujeme tři operace: čtení atributu (`print(foo.bar)`), zapisování (`foo.bar = 3`) a mazání (`del foo.bar`).
Tady se zaměříme hlavně na nejmagičtější z nich, čtení.

Kdykoli atribut čteme pomocí tečky, hledá se několika místech:

* na samotné instanci objektu,
* pokud se tam nenajde, tak na třídě,
* pokud se nenajde ani tam, tak na rodičovských třídách (v případě vícenásobné dědičnosti podle [MRO](https://www.python.org/download/releases/2.3/mro/)),
* a pokud stále není k nalezení, vyhodí se `AttributeError`.

To je trochu zjednodušený, ale užitečný model.

Speciální metody, které se nevolají pomocí tečky, přeskakují první krok: metoda `__add__` tedy musí být definovány na *třídě*, aby se zavolala pro `a + b`.

*(Poznámka navíc pro ty, kdo čtou tento text podruhé: na metatřídě se atribut nehledá; např. existuje-li `type.mro`, najde se `str.mro`, ale už ne `"".mro`)*

Podívejme se teď na získávání atributu trošku podrobněji. Zjistíme, že je to poměrně komplikovaný proces, protože existuje několik způsobů, jak ho přizpůsobit. Nejjednodušší je dvojice speciálních metod:

* `__getattribute__`, která *kompletně předefinuje* funkci `.` pro čtení atributu, a
* `__getattr__`, která se zavolá, až když se atribut nenajde normálním způsobem.

První z nich nedoporučuji používat, protože je *příliš* obecná (pokusy se z ní dostat ke stavu objektu končívají nekonečnou rekurzí).
Příklad druhé:

```python
class Palette:
    red = 255, 0, 0
    green = 0, 255, 0
    
    def __getattr__(self, attr_name):
        prefix, sep, suffix = attr_name.partition('_')
        if prefix == 'dark':
            original_color = getattr(self, suffix)
            return tuple(c//2 for c in original_color)
        else:
            raise AttributeError(attr_name)

palette = Palette()
print(palette.dark_red)
```

(Předpokládám že znáte funkci `getattr`; kdyby ne: `getattr(foo, "bar")` dělá totéž co `foo.bar` – jen je jméno atributu předáno jako řetězec, takže může být např. v proměnné.)

Metoda `__getattr__` je většinou tak trochu kanón na vrabce: ve většině případů nepotřebujeme nastavit chování *všech* neexistujících atributů, ale jenom jednoho.
Například máme třídu pro 2D bod s atributy `x` a `y`, a potřebujeme i atribut pro dvojici `(x, y)`.
Toto se často dělá pomocí dekorátoru `property`:

```python
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    @property
    def pos(self):
        return self.x, self.y

point = Point(41, 8)
print(point.pos)
```

Jak to ale funguje? Dekorátor `property` je třída, jakou můžete teoreticky napsat sami v Pythonu.
Je to *deskriptor*, objekt, který v rámci nějaké třídy *popisuje* jak přistupovat k nějakému atributu.

Nejlépe se deskriptory vysvětlí na příkladu:

```python
# (Omluvte prosím češtinu v kódu)

class Descriptor2D:
    """Popisuje atribut, který kombinuje dva jiné atributy do dvojice"""

    def __init__(self, name1, name2):
        self.name1 = name1
        self.name2 = name2
    
    def __get__(self, instance, cls):
        """Volá se, když je třeba načíst atribut dané `instance` na dané třídě `cls`.
        """

        if instance is not None:
            # Je-li instance nastavena, čteme atribut z ní.
            return getattr(instance, self.name1), getattr(instance, self.name2)
        else:
            # Je-li instance None, čteme atribut přímo ze třídy `cls`;
            # v tomto případě slušné deskriptory většinou vrací deskriptor samotný.
            return self

class Rect:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
    
    pos = Descriptor2D('x', 'y')
    size = Descriptor2D('w', 'h')

rect = Rect(1, 2, 3, 4)
print(rect.pos)
print(rect.size)

# Čtení atributu přímo ze třídy:
print(Rect.pos)
```

Deskriptory jsou tedy součást třídy – atributy s nějakým jménem. Popisují, jak se bude přistupovat k atributu daného jména.

Existují dva druhy deskriptorů: *data descriptor* a *non-data descriptor*.
Liší se v tom, jestli popisují jen, jak se daný atribut *čte*, nebo i jak se do něj *zapisuje*.
Výše uvedený deskriptor je *non-data*: ovládá jen čtení; zápis funguje jako u normálních atributů:
přepíše aktuální hodnotu:

```python
rect.pos = 'haha'
print(rect.pos)
```

Abychom tomu zabránili, můžeme na deskriptoru nadefinovat speciální metodu `__set__` (nebo `__delete__`), která popisuje,
jak se atribut nastavuje (resp. maže), a tím z něj vytvořit *data descriptor*:


```python
class Descriptor2D:
    def __init__(self, name1, name2):
        self.name1 = name1
        self.name2 = name2
    
    def __get__(self, instance, cls):
        if instance is not None:
            return getattr(instance, self.name1), getattr(instance, self.name2)
        else:
            return self

    def __set__(self, instance, new_value):
        a, b = new_value
        setattr(instance, self.name1, a)
        setattr(instance, self.name2, b)

    def __delete__(self, instance):
        delattr(instance, self.name1)
        delattr(instance, self.name2)

class Rect:
    # jako předtím

rect = Rect(1, 2, 3, 4)
rect.pos = 123, 456
print(rect.pos)
```

Už zmíněný vestavěný deskriptor `property`, je *data descriptor*.
Popisuje jak čtení, tak zápis atributu – pokud mu nenastavíme funkci pro zápis, vyhodí `AttributeError` se zprávou, že do atributu se zapisovat nedá (což je odchylka od normálního chování Pythonu).

Častý příklad *non-data* deskriptoru je *funkce*.
Každá funkce totiž funguje jako deskriptor: má speciální metodu `__get__`, která zajišťuje, že pokud je nastavena na třídě, daným atributem nedostaneme *funkci*, ale *metodu* s „předvyplněným“ parametrem `self`.
Kdyby byly funkce (XXX metody?) definované jako třída v Pythonu (což samozřejmě nejsou), mohly by vypadat nějak takto:

```python
class Function:
    def __init__(self, code):
        self.code = code  # XXX ?

    def __call__(self, *args, **kwargs):
        self.code.run(*args, **kwargs)  # XXX ?

    def __get__(self, instance, cls):
        if instance is not None:
            return Method(self.code, first_argument=instance)
        else:
            return self
```


Jako zajímavost uvedu *non-data* deskriptor, který přepisuje svůj vlastní atribut.
Funguje podobně jako `@property`, jen se výsledek vypočítá pouze jednou a uloží se jako normální atribut.
Při dalším přístupu k atributu už se použije uložená hodnota.
[pyramid.decorator.reify](http://docs.pylonsproject.org/projects/pyramid/en/latest/_modules/pyramid/decorator.html)

```python
class reify(object):
    def __init__(self, func):
        self.func = func

    def __get__(self, instance, cls):
        if instance is None:
            return self
        val = self.func(instance)
        setattr(instance, self.func.__name__, val)
        return val

class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    @reify
    def length(self):
        print('Running expensive computation...')
        return (self.x ** 2 + self.y ** 2) ** 0.5

vect = Vector(3, 4)
print(vect.length)
print(vect.length)
print(vect.length)
```


Metatřídy
---------

XXX: Metaclass
XXX: __init__, __new__, __prepare__


Úkol
----

Úkol není!

Budete-li chtít některé techniky z této lekce ve svém kódu (včetně semestrálky) použít, zamyslete se, jestli se problém nedá vyřešit jednodušeji, čitelněji, přehledněji, udržovatelněji.
Dobrý mág ví, kdy magii *nepoužít*.


