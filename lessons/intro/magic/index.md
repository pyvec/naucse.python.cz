Magie
=====

Co z Pythonu dělá tak užitečný jazyk?
Z velké části je to zaměření na čitelnost kódu. Pythonu se někdy říká „spustitelný pseudokód“: syntaxe je inspirovaná zápisem abstraktních algoritmů v matematice, používá se málo speciálních znaků jako `$`, `<<`, `&&`, `?`.
Čitelnosti je podřízena expresivita (proto v Pythonu nenajdeme makra jako v Lispu) i délka zápisu (některé věci se nedají napsat na jeden řádek).

Návrh jazyka (a knihoven pro něj) se řídí mimo jiné poučkou „There should be one– and preferably only one –obvious way to do it.“
Existuje ideálně jeden *zjevně nejlepší* způsob, jak dosáhnout určité funkčnosti.
Úkolem programátora je tento způsob najít a použít. Náš cíl by měl být kód, který ostatní programátoři pochopí na první pohled. A pokud je to možné, měli by ho pochopit i neprogramátoři. Není mezi nimi pevná hranice – váš kód můžou číst lidi, kteří programovací jazyk v životě neviděli; programátoři silní v jiných jazycích; průměrní Pythonisté; nebo ostřílení veteráni. Čím víc jich dokáže kód pochopit, tím bude váš kód udržovatelnější.

S tím souvisí koncept „magie“. Magie je něco, co funguje, ačkoli tomu nerozumíme. Pro každého čtenáře kódu může být magie něco jiného: pro začátečníka bude nepochopitelný zápis `zip(*args)`, matematik nemusí chápat princip dědičnosti tříd, ostřílený Pythonista nemusí chápat maticovou matematiku, neprogramátor netuší, jak funguje mobil nebo webová aplikace. Je to tedy subjektivní pojem, ale lze ho zobjektivnit: čím méně lidí váš kód pochopí, tím je kód magičtější.

Magie, která *funguje*, nevadí. Věci které nechápu, můžu stále používat – jen nevím jak fungují, a tudíž je neumím *opravit*. Problém nastane až v momentě, kdy se něco pokazí.

Přehlednost a udržitelnost kódu je samozřejmě potřeba vyvážit s ostatními aspekty. Kód musí být například dostatečně rychlý a optimalizace ho často znepřehlední. Proto je dobré optimalizovat až potom, co vím, že je kód *správný* a řeší opravdu problém, který potřebuji vyřešit. V ten moment napíšu testy a potom, když je potřeba, můžu optimalizovat – trochu přehlednosti vyměnit za rychlost.

Na jiný důvod, proč použít méně pochopitelné techniky, narazíme při psaní knihoven a frameworků. To je kód, který používá hodně programátorů – a často jsou to programátoři s méně zkušenostmi, než mají autoři knihovny. Tady proto bývá dobré občas použít nějakou tu magii – znepřehlednit kód knihovny, aby kód který knihovnu *používá*, mohl být přehlednější.

Typický příklad jsou dekorátory ve Flasku. Napsat dekorátor není úplně triviální, ale velice to zjednodušuje práci všem, co ve Flasku píšou web. Konstrukce `@app.route` je pro většinu lidí magická – nevíme přesně, co to dělá, ale to nám nebrání ji použít.


Velká moc a velká zodpovědnost
------------------------------

Druhý možný význam slova *magie* je něco, co neodpovídá „normálnímu“ chování podobných věcí.

Jazyk Python standardizuje syntaxi relativně malého počtu operací (operátory, volání funkcí, atributy, ...), způsobů řízení toku programu (cykly, `with`, ...) a strukturování kódu (moduly, `def`, `class`).
To, že je jich relativně málo, má dvě výhody: zaprvé fungují s ostatními části jazyka a zadruhé nebývá problém rozhodnout, který způsob je pro daný problém nejlepší.

Téměř všechno v Pythonu ale jde předefinovat. Operátor `/` nemusí jen dělit: můžu si napsat třídu pro jméno souboru, která umí pomocí `/` oddělovat adresáře \*.
Cyklus `for` nemusí iterovat přes předem danou sekvenci prvků; iterovatelný objekt může poskytovat jakékoli hodnoty podle jakýchkoli pravidel.
Příkaz `class` dokonce vůbec nemusí vytvořit třídu, jak uvidíme později.

Ačkoliv si ale můžeme dovolit téměř cokoli, je dobré mít na paměti, že odchylky od „normálního“ chování jsou *magické*. Jakmile někdo použije divnou třídu, která předefinovává dělení, ve svém kódu, musí každý čtenář toho kódu nejen opustit představu o tom, co operátor `/` dělá, ale hlavně si předtím uvědomit, že `/` *může* dělat něco divného. To samé platí u „divných“ iterovatelných objektů nebo tříd. Odchylka od normálního chování, je-li nezbytná, by měla být dobře promyšlená a zdokumentovaná.

Nadefinujeme-li vlastní nestandardní – „magické“ – chování některých objektů, často se stane, že nebudou fungovat s ostatními prvky jazyka tak dobře, jako to co je zabudované. Předefinujeme-li `<` tak, že nebude mít nic společného s porovnáváním, bude se funkce `sorted` chovat podivně. Když u svých objektů předefinuji přístup k atributům, musím si dávat zvlášť pozor na to, aby fungovala funkce `dir()`.

Následující principy (kromě jiných) je proto dobré při psaní knihoven používat jen po pečlivém zvážení, jestli by to nešlo i bez magie.

\* *Taková třída dokonce [existuje ve standardní knihovně](https://docs.python.org/3/library/pathlib.html).*


Speciální metody
----------------

Základní způsob, jak přizpůsobit chování objektů, jsou *speciální metody*.
Asi už víte, že všechny atributy, které začínají a končí dvojitým podtržítkem, jsou rezervované pro samotný Python, který je používá podle svých pravidel – například danou metodu volá, když je potřeba sečíst dvě čísla.

Speciální metody jsou popsané v [dokumentaci](https://docs.python.org/3/reference/datamodel.html#special-method-names). Zde uvedu jen přehled, který pokročilý Pythonista nosí v hlavě, aby věděl co je všechno možné.
Doporučuji si předtím, než nějakou naimplementujete, dokumentaci přečíst.

Metody pro předefinování aritmetických operátorů:
`__add__`, `__sub__`, `__mul__`, `__div__`, `__floordiv__`, `__pow__`, `__matmul__`, `__lshift__`, `__rshift__`, `__or__`, `__xor__` a varianty s `r` a `i` (`__radd__`, `__iadd__`, atd.);
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

Implementace *context manageru* (pro `with`):
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

Nejjednodušší použití dekorátorů je *registrace*:
k funkci přidáme dekorátor a funkce se někam zaregistruje, uloží,
aby se dala zavolat později.
Typický příklad je `@app.route` ve Flasku.

My si pro příklad budeme chtít udělat dekorátor pro kalkulačku,
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

Použití dekorátoru je jen zkrácený zápis pro volání dekorátoru jako
funkce – poslední tři řádky předchozího příkladu jsou ekvivalentní tomuto:

```python
def add(a, b):
    return a + b

add = register_operator(add)
```

Chování samotného `@` je tedy celkem triviální.
Magie (složitost) spočívá v tom, že dekorátor je většinou funkce vyššího řádu:
bere jinou funkci jako argument a taky jinou funkci vrací.
V případě registrace vrací stejnou funkci jako dostala – ale to není povinné.

Často se setkáme s dekorátory, které dekorovanou funkci nějak modifikují.
Například můžeme napsat dekorátor, který v naší kalkulačce převede vstup
na reálná čísla.
Dělá to tak, že definuje *novou funkci*, která volá tu původní – ale před nebo
po tomto volání může dělat i něco jiného.

```python
def to_floats(func):
    def outer_function(a, b):
        a = float(a)
        b = float(b)
        return func(a, b)
    return outer_function

@to_floats
def add(a, b):
    """Adds two numbers"""
    return a + b

print(add(1, '2'))
```

Takto funguje většina dekorátorů, které mění chování dekorované funkce.
Naráží s tím ale na jeden problém: nově nadefinovaná funkce má vlastní jméno
(a dokumentační řetězec a podobné informace), což kazí iluzi, že jsme
původní funkci jen trošku změnili:

```python
print(add)
help(add)
```

Řešení je jednoduché – zkopírovat jméno, dokumentační řetězec atd. z jedné
funkce na druhou.
Na to ve standardní knihovně existuje dekorátor jménem `functools.wraps`:


```python
import functools

def to_floats(func):
    @functools.wraps(func)
    def outer_function(a, b):
        a = float(a)
        b = float(b)
        return func(a, b)
    return outer_function
```

S `wraps` bude `help(add)` fungovat správně – ukáže původní jméno
a dokumentační řetězec.

Z volání `wraps(func)` je vidět, že jako dekorátor můžeme použít i volání
funkce, ne jen funkci samotnou.
Budeme-li chtít napsat dekorátor, který tohle umí, potřebujeme napsat
funkci ještě vyššího řádu – totiž funkci, která po zavolání vrátí dekorátor:

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

Řádek `@register_operator('+')` dělá (jak už víme) to stejné, jako bychom hned
za funkcí napsali `add = register_operator('+')(add)`.

Budete-li chtít napsat dekorátor, který bere argumenty, a přitom ještě
„mění“ dekorovanou funkci, dostanete se na tři funkce zanořené v sobě:

```python
import functools
operators = {}

def register_operator(name):
    def to_floats(func):

        @functools.wraps(func)
        def outer_function(a, b):
            a = float(a)
            b = float(b)
            return func(a, b)

        operators[name] = outer_function
        return outer_function

    return to_floats

@register_operator('+')
def add(a, b):
    return a + b

func = operators['+']
print(func(1, '2'))
```

Dekorátorů se na jedné funkci dá použít víc:

```python
@register_operator('×')
@register_operator('*')
def mul(a, b):
    return a * b
```

Úplně stejně jako funkce se dají dekorovat i třídy.
Dekorátor dostane třídu jako první argument a třída se nahradí tím,
co dekorátor vrátí.


Deskriptory
-----------

Jeden z nejmagičtějších operátorů v Pythonu je `.`, tečka.
Je magický v obou významech – většina lidí ho používá, ačkoli nemá tušení, co přesně dělá, a dá se předefinovat tolika různými způsoby, že to vydá na [celou přednášku](https://www.youtube.com/watch?v=NiSqG6s8skA).

Pomocí tečky zapisujeme tři operace: čtení atributu (`print(foo.bar)`), zapisování (`foo.bar = 3`) a mazání (`del foo.bar`).
Tady se zaměříme hlavně na nejmagičtější z nich, čtení.

Kdykoli atribut čteme pomocí tečky, hledá se na několika místech:

* na samotné instanci objektu,
* pokud se tam nenajde, tak na třídě,
* pokud se nenajde ani tam, tak na rodičovských třídách (v případě vícenásobné dědičnosti podle [MRO](https://www.python.org/download/releases/2.3/mro/)),
* a pokud stále není k nalezení, vyhodí se `AttributeError`.

To je trochu zjednodušený, ale užitečný model.

Speciální metody, které se nevolají pomocí tečky, přeskakují první krok: metoda `__add__` tedy musí být definována na *třídě*, aby se zavolala pro `a + b`.

> *(Poznámka navíc pro ty, kdo čtou tento text podruhé: na metatřídě se atribut nehledá; např. existuje-li `type.mro`, najde se `str.mro`, ale už ne `"".mro`)*

Podívejme se teď na získávání atributu trošku podrobněji. Je to poměrně komplikovaný proces a existuje několik způsobů, jak ho přizpůsobit. Nejjednodušší je dvojice speciálních metod:

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

(Předpokládám že znáte funkci `getattr`; kdyby ne: `getattr(foo, "bar")` dělá totéž co `foo.bar` – jen je jméno atributu předáno jako řetězec, takže může být např. v proměnné. Podobně existují `setattr(instance, attr_name, new_value)` a `delattr(instance, attr_name)`.)

Metoda `__getattr__` je většinou tak trochu kanón na vrabce: ve většině případů nepotřebujeme nastavit chování *všech* neexistujících atributů, ale jenom jednoho nebo několika konkrétních.
Například máme třídu pro 2D bod s atributy `x` a `y` a potřebujeme i atribut pro dvojici `(x, y)`.
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
    
    def __get__(self, instance, cls=None):
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
Výše uvedený deskriptor je *non-data*: ovládá jen čtení. Zápis funguje jako u normálních atributů:
přepíše aktuální hodnotu – a nová hodnota se pak použije místo volání deskriptoru:

```python
rect.pos = 'haha'
print(rect.pos)
```

Abychom tomu zabránili, můžeme na deskriptoru nadefinovat speciální metodu `__set__` (nebo `__delete__`), která popisuje,
jak se atribut nastavuje (resp. maže).
Tím vznikne *data descriptor*:


```python
class Descriptor2D:
    def __init__(self, name1, name2):
        self.name1 = name1
        self.name2 = name2
    
    def __get__(self, instance, cls=None):
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

Už zmíněný vestavěný deskriptor `property` je *data descriptor*.
Popisuje jak čtení, tak zápis atributu. Pokud mu nenastavíme funkci pro zápis, vyhodí ze své metody  `__set__` výjimku `AttributeError` se zprávou, že do atributu se zapisovat nedá. (To je trochu magická odchylka od normálního chování Pythonu, kdy atributy zapisovat jdou.)

Nejčastější příklad *non-data* deskriptoru je obyčejná funkce.
Každá funkce totiž funguje jako deskriptor: má speciální metodu `__get__`, která zajišťuje, že pokud je nastavena na třídě, daným atributem nedostaneme *funkci*, ale *metodu* (s „předvyplněným“ parametrem `self`).

```python
def foo(self):
    return 4

class C:
    foo = foo

c = C()
    
# Obyčejná funkce
print(C.foo)
print(foo)

# Metoda
print(C().foo)
print(foo.__get__(c))
```

Protože je to *non-data* deskriptor, můžeme v jednotlivých instancích třídy
daný atribut přepsat něčím jiným, čímž metodu znepřístupníme.


Jako zajímavost uvedu *non-data* deskriptor, který přepisuje svůj vlastní atribut.
Funguje podobně jako `@property`, jen se výsledek vypočítá pouze jednou a uloží se jako normální atribut.
Při dalším přístupu k atributu už se použije uložená hodnota.

```python
class reify:
    def __init__(self, func):
        self.func = func

    def __get__(self, instance, cls=None):
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

Kompletní implementace je např. ve frameworku Pyramid jako [pyramid.decorator.reify](http://docs.pylonsproject.org/projects/pyramid/en/latest/_modules/pyramid/decorator.html).


Konstruktor
-----------

Třídy v Pythonu můžou mít *konstruktor* – funkci, která se zavolá, aby
vytvořila objekt daného typu.
Toto není známá metoda `__init__` – ta objekt nevytváří, ta dostane už
předpřipravený `self`, který jen naplní atributy.
Opravdový konstruktor se jmenuje `__new__` a chová se jako `classmethod`:
místo `self` bere třídu, jejíž instanci má vytvořit.

Opravdový konstruktor se „hodí“ pro vytváření *singletonů*, tříd, které mají jen
jednu instanci:

```python
class Singleton:
    def __new__(cls):
        try:
            return cls._instance
        except AttributeError:
            cls._instance = super().__new__(cls)
            return cls._instance

assert Singleton() is Singleton()
```

Podobný trik lze použít pro třídu podobnou `bool`, která má pouze dvě instance:
`bool(1) is bool(2)`.

Metoda `__new__` se hodí, když chceme dědit z neměnitelné (*immutable*)
třídy jako `tuple`.
Metoda `__init__` sice dostane `self`, ale cokoli z nadtřídy už nemůže měnit.
Je ale možné předefinovat `__new__`.

Normálně bere `tuple` jediný argument, `tuple([1, 2])`.
Chceme-li brát dva, dá se to udělat takto:

```python
class Point(tuple):
    def __new__(cls, x, y):
        return super().__new__(cls, (x, y))

print(Point(3, 4))
```


Metatřídy
---------

Poslední věc, na kterou se podíváme, jsou metatřídy.

Začneme zlehka: pokud při definici třídy zadáme nějakou funkci jako pojmenovaný
parametr `metaclass`, funkce se zavolá s informacemi potřebnými pro vytvoření
třídy.
Ty můžeme použít, nebo úplně ignorovat a vrátit něco jiného:

```python
def fake_metaclass(name, bases, namespace):
    return 42

class NotAClass(metaclass=fake_metaclass):
    pass

print(NotAClass)
```

Argumenty, které „metatřída” dostane, jsou tři: jméno třídy, *n*-tice
nadtříd a jmenný prostor – slovník s proměnnými, které vznikly vykonáním
těla příkazu `class`.
(Ve jmenném prostoru jsou implicitně nastavené záznamy `__module__`
a `__qualname__`, které přidává samotný příkaz `class`.)

```python
def fake_metaclass(name, bases, namespace):
    print('name:', name)
    print('bases:', bases)
    print('namespace:', namespace)
    return 42

class NotAClass(int, metaclass=fake_metaclass):
    foo = 123
    def inc(self):
        return self + 1
```

Když `metaclass` nezadáme, použije se výchozí *metatřída*, tedy třída třídy.
V Pythonu je to `type`.
Pokud ji zavoláme s vhodnými argumenty, dostaneme normální třídu:

```python
MyInt = type('MyInt', (int, ), {'foo': 123, 'inc': lambda self: self + 1})

three = MyInt(3)
print(three.inc())
```

Kromě toho se `type` dá zavolat i s jedním argumentem; v tom případě vrátí
typ (třídu) daného argumentu.
(Tohle chování – funkce, která dělá úplně různé věci v závislosti na počtu
argumentů – v Pythonu často nevidíme.
Je to nešťastná výjimka, která přežívá z historických důvodů.)

Pojďme se podívat na třídy několika základních objektů:

```python
# Třída základních objektů
print(type(1))
print(type("abc"))

# Třída třídy – metatřída.
# Třída většiny tříd v Pythonu je `type`
print(type(int))
print(type(type(1)))

# Třída třídy třídy
# Samotná `type` je jedna z té většiny tříd; její třída je `type`
print(type(type))
print(type(type(type(1))))
```

Objekty třídy `type` (tedy třídy) se normálně tvoří příkazem `class`.
Explicitně to můžeme napsat takto:

```python
class NormalClass(metaclass=type):
    foo = 123
```

Když budeme chtít chování třídy změnit, budeme postupovat podobně jako
u jiných objektů.
Kdybych chtěl celé číslo, přes které jde iterovat, podědím z `int`
a předefinuji `__iter__`.
Pokud chci třídu, přes kterou jde iterovat (tedy ne přes objekty dané
třídy – přes třídu samotnou!), podědím z `type` a předefinuji `__iter__`:

```python
class IterableMeta(type):
    def __init__(cls, name, bases, namespace):
        cls.items = sorted(n for n in namespace
                           if not n.startswith('__'))
        super().__init__(name, bases, namespace)

    def __iter__(cls):
        return iter(cls.items)

class SimpleEnum(metaclass=IterableMeta):
    a = 1
    b = 2
    c = 3
    d = 4

print(SimpleEnum.a)
print(list(SimpleEnum))
```

(V metatřídě se většinou používá `cls` místo `self`, aby bylo jasné, že
instance, se kterou pracujeme, je třída – ale to je jen konvence.)

Metatřídy se dědí.
Pokud v příkazu `class` nezadám explicitně `metaclass`, použije
se metatřída nadtřídy:

```python
class AnotherEnum(SimpleEnum):
    x = 10
    y = 20
    z = 30

print(AnotherEnum.a)
print(list(AnotherEnum))
```

Tímto způsobem lze vnuknout třídám magické schopnosti bez toho, aby
uživatel naší knihovny musel použít `metaclass` – stačí mu podědit z námi
připravené třídy.

Další věc, kterou metatřídy umí, je připravit počáteční jmenný prostor.
Metoda `__init__` (nebo `__new__`) v metatřídě normálně dostane slovník,
což nemusí být vždy to, co potřebuji.
Můžu si chtít třeba „zapamatovat” pořadí, v jakém byly jednotlivé atributy
vytvořeny – a slovník toto pořadí neuchovává (alespoň v některých verzích Pythonu).

Na to existuje speciální metoda `__prepare__`, která se, když na metatřídě
existuje, zavolá pro vytvoření jmenného prostoru:

```python
from collections import OrderedDict

class OrderRememberingMeta(type):
    def __prepare__(cls, name):
        return OrderedDict()

    def __init__(cls, name, bases, namespace):
        cls.items = list(namespace)
        super().__init__(name, bases, namespace)

    def __iter__(cls):
        return iter(cls.items)

class OrderedEnum(metaclass=OrderRememberingMeta):
    first = 1
    second = 2
    third = 3
    fourth = 4
    fifth = 5

print(list(OrderedEnum))
```

Toho se dá využít třeba v mapování objektů na databázi (např. v Django Models
nebo SQLAlchemy), kdy chceme, aby pořadí sloupců tabulky odpovídalo
tomu, jak jsou sloupce/atributy nadefinovány ve třídě.

A další
-------

Další (bohužel?) oblíbený trik je vnuknutí magických schopností modulu.

Naimportované moduly Python ukládá do slovníku `sys.modules`, aby při dalším
importu nemusel načítat znovu – `sys.modules` tedy slouží jako cache.
A tuto cache můžeme změnit (tzv. *cache poisoning*) – přidat si do ní
vlastní „modul“, který ovšem vůbec nemusí být modul, a tudíž může umět věci,
které moduly normálně neumí:

```python
import sys

sys.modules['fake'] = 'a string'

...

import fake

print(fake[2])
```

Když toto uděláme přímo z modulu, uživatel naší knihovny dostane podstrčený
objekt hned při prvním importu.
K tomu se hodí proměnná `__name__`, jméno aktuálního modulu:

```python
sys.modules[__name__] = ReplacementModule()
```


Jiný trik je registrace „built-in“ („superglobální”) proměnné:

```
import builtins
builtins.ANSWER = 42

...

# Třeba v jiném modulu
print(ANSWER)
```

Tímto způsobem se dají i předefinovat vestavěné funkce, což může být někdy
užitečné pro ladění. V produkčním kódu to ale, prosím, nedělejte.


Úkol
----

Úkol není!

Budete-li chtít některé techniky z této lekce ve svém kódu (včetně semestrálky) použít, zamyslete se, jestli se problém nedá vyřešit jednodušeji, čitelněji, přehledněji, udržovatelněji.
Dobrý mág ví, kdy magii *nepoužít*.
