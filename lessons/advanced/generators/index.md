Generátory
==========


Dnes si popíšeme, jak v Pythonu fungují *generátory*, tedy funkce s příkazem `yield`.
Někteří z vás možná už nějaký jednoduchý generátor napsali, ale pojďme si je
vysvětlit od úplného začátku: od toho, jak se v Pythonu iteruje.


Iterace
-------

Když je v Pythonu potřeba iterovat (např. příkazem `for`) přes nějakou kolekci
(seznam, řetězec, soubor, …), použije se *iterační protokol*,
který pracuje se dvěma druhy objektů: s *iterovatelnými objekty* a s *iterátory*.

Iterovatelné objekty (*iterables*) se vyznačují tím, že je na ně možné zavolat
funkci `iter()`. Ta vrátí příslušný iterátor:

```pycon
>>> iter([1, 2, 3])
<list_iterator object at 0x...>
```

Na iterátor pak je možné opakovaně volat funkci `next()`, čímž dostáváme jednotlivé
prvky iterace.
Po vyčerpání iterátoru způsobuje `next()` výjimku `StopIteration`:

```pycon
>>> it = iter([1, 2, 3])
>>> next(it)
1
>>> next(it)
2
>>> next(it)
3
>>> next(it)
Traceback (most recent call last):
  ...
StopIteration
>>> next(it)
Traceback (most recent call last):
  ...
StopIteration
```

Cyklus `for x in collection: ...` tedy dělá něco jako:

```python
iterator = iter(collection)
while True:
    try:
        x = next(iterator)
    except StopIteration:
        break

    ...  # tělo původního cyklu
```

Platí, že každý iterátor je iterovatelný: zavoláním `iter()` na iterátor
dostaneme ten stejný iterátor (nikoli jeho kopii) zpět.
Naopak to ale obecně neplatí: např. seznamy jsou iterovatelné, ale nejsou samy
o sobě iterátory.
Každé zavolání `iter(seznam)` vrací nový iterátor, který má svou vlastní
„aktuální pozici“ a iteruje od začátku.

Iterátor je ve většině případů „malý“ objekt, který si „pamatuje“ jen původní iterovatelný
objekt a aktuální pozici. Příklady jsou iterátory seznamů (`iter([])`), slovníků (`iter({})`),
*n*-tic nebo množin, iterátor pro `range` a podobně.

Iterátory ale můžou být i „větší“: třeba otevřený soubor je iterátor, z něhož `next()`
načítá jednotlivé řádky.


Generátory
----------

Asi nejzajímavější druh iterátoru je tzv. *generátor*: funkce, která umí postupně
dávat k dispozici hodnoty.
Definuje se pomocí klíčového slova `yield`: každá funkce, která obsahuje `yield`,
je *generátorová funkce* (angl. *generator function*).

```python
def generate2():
    """generates 2 numbers"""
    print('A')
    yield 0
    print('B')
    yield 1
    print('C')
```

Zavoláním takové funkce dostáváme *generátorový iterátor* (angl. *generator iterator*):

```pycon
>>> generate2()
<generator object generate2 at 0x...>
```

Voláním `next()` se pak stane zajímavá věc: funkce se provede až po první `yield`,
tam se *zastaví* a hodnota `yield`-u se vrátí z `next()`.
Při dalším volání se začne provádět zbytek funkce od místa, kde byla naposled
zastavena.

```pycon
>>> it = generate2()
>>> next(it)
A
0
>>> next(it)
B
1
>>> next(it)
C
Traceback (most recent call last):
  ...
StopIteration
```


Další použití generátorů
------------------------

Vlastnost přerušit provádění funkce je velice užitečná nejen pro vytváření
sekvencí, ale má celou řadu dalších užití.
Existuje třeba dekorátor, který generátorovou funkci s jedním `yield` převede na *context manager*,
tedy objekt použitelný s příkazem `with`:

```python
import contextlib

@contextlib.contextmanager
def ctx_manager():
    print('Entering')
    yield 123
    print('Exiting')


with ctx_manager() as obj:
    print('Inside context, with', obj)
```

Vše před `yield` se provede při vstupu do kontextu, hodnota `yield` se předá
dál a vše po `yield` se provede na konci.
Můžeme si představit, že místo `yield` se „doplní“ obsah bloku `with`.
Funkce se tam na chvíli zastaví a může se tedy provádět něco jiného.


Vracení hodnot z generátorů
---------------------------

V rámci generátorové funkce můžeme použít i `return`, který funkci ukončí.
Vrácená hodnota se však při normální iteraci (např. ve `for`) nepoužije.
Objeví se pouze jako hodnota výjimky `StopIteration`, která signalizuje konec
iterace:

```python
def generator(a, b):
    """Yield two numbers and return their sum"""
    yield a
    yield b
    return a + b
```

```pycon
>>> it = generator(2, 3)
>>> next(it)
2
>>> next(it)
3
>>> next(it)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
StopIteration: 5
```


Obousměrná komunikace
---------------------

Oproti normálním iterátorům, které hodnoty jen poskytují, mají generátory metodu
`send()`, kterou je možné posílat hodnoty *do* běžícího generátoru.
Klíčové slovo `yield` totiž může fungovat jako výraz a tento výraz nabývá poslanou
hodnotu (nebo `None`, byl-li použit normální `next()`).

```python
def running_sum():
    total = 0
    while True:
        num = (yield total)
        if num:
            total += num

it = running_sum()
next(it)  # pro první iteraci nelze použít send() -- nečekáme zatím na yield-u
it.send(2)
it.send(3)
assert next(it) == 5
```

Upřímě řečeno, metoda `send()` není příliš užitečná.
(Když byste něco takového potřebovali, radši si napište třídu, která si bude
stav uchovávat v atributech, a měňte ji třeba metodami. Bude to pravděpodobně
přehlednější.)
Existuje ale příbuzná metoda, která už je užitečnější: `throw()`.
Ta do generátoru „vhodí“ výjimku.
Z pohledu generátorové funkce to vypadá, jako by výjimka nastala na příkazu
`yield`.

```python
def report_exception():
    try:
        yield
    except BaseException as e:
        print('Death by', type(e).__name__)
    yield 123
```

```pycon
>>> it = report_exception()
>>> next(it)  # opět – v první iteraci nelze throw() použít
>>> value = it.throw(ValueError())
Death by ValueError
>>> value
123
```

Podobná věc se děje, když generátorový iterátor zanikne: Python do generátoru
„vhodí“ výjimku GeneratorExit.
Ta dědí z `BaseException`, ale ne `Exception`, takže klasické `except Exception:`
ji nechytí (ale např. `finally` funguje jak má).
Pokud generátor tuto výjimku chytá, měl by se co nejdřív ukončit.
(Když to neudělá a provede další `yield`, Python ho ukončí „násilně“.)

```pycon
>>> import gc
>>> it = report_exception()
>>> next(it)
>>> del it; gc.collect()  # zbavíme se objektu "it"
Death by GeneratorExit
Exception ignored in: <generator object report_exception at 0x...>
RuntimeError: generator ignored GeneratorExit
0
```


Delegace na podgenerátor – `yield from`
---------------------------------------

Máme následující generátor:

```python
def dance():
    yield 'putting hands forward'
    yield 'putting hands down'
    yield 'turning around'
    yield 'jumping'
    yield 'putting hands forward'
    yield 'putting hands down'

for action in dance():
    print(action)
```

Opakuje se v něm jistá sekvence, kterou bychom jako správní programátoři chtěli
vyčlenit do samostatné funkce.
Pomocí samotného `yield` to ale jde celkem těžko:

```python
def dance_hands():
    yield 'putting hands forward'
    yield 'putting hands down'

def dance():
    for action in dance_hands():
        yield action
    yield 'turning around'
    yield 'jumping'
    for action in dance_hands():
        yield action

for action in dance():
    print(action)
```

Tohle počtu řádků příliš nepomohlo. Existuje lepší způsob – místo cyklu
můžeme použít `yield from`:


```python
def dance_hands():
    yield 'putting hands forward'
    yield 'putting hands down'

def dance():
    yield from dance_hands()
    yield 'turning around'
    yield 'jumping'
    yield from dance_hands()

for action in dance():
    print(action)
```

Navíc lze `yield from` použít jako výraz, který nabývá hodnoty
kterou podgenerátor vrátil (t.j. hodnota výjimky `StopIteration`).

```python
def fibonacci(limit):
    a = 0
    b = 1
    count = 0
    while b < limit:
        yield b
        count += 1
        a, b = b, a + b
    return count

def fib_annotated():
    count = (yield from fibonacci(10))
    print('LOG: Generated {} numbers'.format(count))

for value in fib_annotated():
    print('Got', value)
```

```
Got 1
Got 1
Got 2
Got 3
Got 5
Got 8
LOG: Generated 6 numbers
```

Kromě toho `yield from` deleguje hodnoty poslané pomocí `send()` či `throw()`.
