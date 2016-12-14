Generátory a AsyncIO
====================

Na část toto cvičení bude opět potřeba PyQt5.
Můžete použít virtualenv z minula, nebo PyQt5 nainstalovat znovu (viz [minulá lekce]).
(Nejde-li to, nevadí – úplně nezbytné dnes PyQt nebude.)

[minulá lekce]: 09_pyqt.md

Další knihovny pro dnešní den:

    python -m pip install --upgrade pip
    python -m pip install notebook aiohttp quamash

Případně pro Python 3.3:

    python -m pip install asyncio


---

Dnes se podíváme na dvě témata, která spolu souvisí čím dál tím méně, ale stále je
dobré je pochopit společně.
Napřed si ukážeme *generátory*, a poté si vysvětlíme *asynchronní programování*.


Generátory
==========

Nejdříve si popíšeme, jak v Pythonu fungují *generátory*, tedy funkce s příkazem `yield`.
Předpokládám, že většina z vás už nějaký jednoduchý generátor napsala, ale pojďme si je
vysvětlit od úplného začátku: od toho, jak se v Pythonu iteruje.


Iterace
-------

Když je v Pythonu potřeba iterovat přes nějakou kolekci, použije se *iterační protokol*,
který pracuje se dvěma druhy objektů: s *iterovatelnými objekty* a s *iterátory*.

Iterovatelné objekty (*iterables*) se vyznačují tím, že je na ně možné zavolat
funkci `iter()`, která vrátí příslušný iterátor:

```python
>>> iter([1, 2, 3])
<list_iterator object at 0x...>
```

Na iterátor pak je možné opakovaně volat funkci `next()`, čímž dostáváme jednotlivé
prvky iterace.
Po vyčerpání iterátoru způsobuje `next()` výjimku `StopIteration`:

```python
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

Zároveň platí, že každý iterátor je iterovatelný: zavoláním `iter()` na iterátor
dostaneme ten stejný iterátor (nikoli jeho kopii) zpět.
Naopak to ale obecně neplatí: seznamy jsou iterovatelné, ale nejsou samy o sobě
iterátory.

Iterátor je ve většině případů "malý" objekt, který si "pamatuje" jen původní iterovatelný
objekt a aktuální pozici. Příklady jsou iterátor seznamů (`iter([])`), slovníků (`iter({})`),
n-tic, nebo množin, iterátor pro `range`, a podobně.

Iterátory ale můžou být i "větší": třeba otevřený soubor je iterátor, z něhož `next()`
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

```python
>>> generate2()
<generator object generate2 at 0x...>
```

Voláním `next()` se pak stane zajímavá věc: funkce se provede až po první `yield`,
tam se *zastaví*, a hodnota `yield`-u se vrátí z `next()`.
Při dalším volání se začne provádět zbytek funkce od místa, kde byla naposled
zastavena.

```python
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

Tahle vlastnost přerušit provádění funkce je velice užitečná nejen pro vytváření
sekvencí, ale má celou řadu dalších užití.
Existuje třeba dekorátor, který generátorovou funkci s jedním `yield` převede na *context manager*:

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
dál, a vše po `yield` se provede na konci.
Můžeme si představit, že místo `yield` se "doplní" obsah bloku `with` –
funkce se tam na chvíli zastaví a může se tedy provádět něco jiného.


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

```python
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
Klíčové slovo `yield` totiž může fungovat jako výraz, a tento výraz nabývá poslanou
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
Ta do generátoru "vhodí" výjimku.
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

```python
>>> it = report_exception()
>>> next(it)  # opět – v první iteraci nelze throw() použít
>>> value = it.throw(ValueError())
Death by ValueError
>>> value
123
```

Podobná věc se děje, když generátorový iterátor zanikne: Python do generátoru
"vhodí" výjimku GeneratorExit.
Ta dědí z `BaseException`, ale ne `Exception`, takže klasické `except Exception:`
ji nechytí (ale např. `finally` funguje jak má).
Pokud generátor tuto výjimku chytá, měl by se co nejdřív ukončit.
(Když to neudělá a provede další `yield`, Python ho ukončí "násilně".)

```python
>>> import gc
>>> it = report_exception()
>>> next(it)
>>> del it; gc.collect()  # zbavíme se objektu "it" (i v interpretech, které nepoužívají reference counting)
Death by GeneratorExit
Exception ignored in: <generator object report_exception at 0x...>
RuntimeError: generator ignored GeneratorExit
0
```


Kombinace generátorů
--------------------

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

Tohle počtu řádků příliš nepomohlo. Existuje lepší způsob – místo:

```python
    for action in dance_hands():
        yield action
```

můžeme delegovat vytváření podsekvence na jiný generátor pomocí:

```python
    yield from dance_hands()
```

Příkaz `yield from` deleguje nejen hodnoty, které jdou z generátoru "ven" pomocí
`yield`, ale i ty, které jdou "dovnitř" pomocí `send()` či `throw()`.
A dokonce funguje jako výraz, jehož hodnota odpovídá tomu, co
daný generátor vrátil:

```python
def dance_hands():
    value = (yield 'putting hands forward')
    yield 'putting hands down'
    if value:
        yield 'putting {},- in pocket'.format(value)
        return value
    return 0

def dance():
    profit = 0
    profit += (yield from dance_hands())
    yield 'turning around'
    yield 'jumping'
    profit += (yield from dance_hands())
    if profit:
        yield 'spending {},- on sweets'.format(profit)

def performance():
    it = dance()
    print(next(it))
    print(it.send(100))
    for action in it:  # pokračujeme v načaté iteraci – implicitní "iter(it)" vrací zase "it"
        print(action)
```

```python
>>> performance()
putting hands forward
putting hands down
putting 100,- in pocket
turning around
jumping
putting hands forward
putting hands down
spending 100,- on sweets
```


AsyncIO
=======

A teď něco úplně jiného: asynchronní programování.

Jak jsme si řekli v lekci o C API, Python má globální zámek, takže pythonní kód
může běžet jen v jednom vlákně najednou.
Taky jsme si řekli, že to většinou příliš nevadí: typický síťový nebo GUI program
stráví hodně času čekáním na události (odpověď z internetu, kliknutí myší atp.),
a u tohoto čekání není potřeba držet zámek zamčený.

Servery typicky při zpracovávání požadavku stráví *většinu* času síťovou komunikací.
Proto se často spouští několik vláken nebo přímo procesů najednou, aby se mohl vytížit
procesor.
Při velkém množství vláken ale nastanou dva problémy.
První je, že vláken nemůže být neomezeně mnoho.
Každé vlákno potřebuje vlastní stack, tj. poměrně velkou část paměti; a počet vláken
bývá omezen i jinak (na Linuxu je globální limit počtu procesů, do kterého se počítají
i jednotlivá vlákna – viz `cat /proc/sys/kernel/threads-max`).
Druhý problém je, že přepnutí z jednoho vlákna do druhého se může stát *kdykoli*.
Ověřit si, že je na to program připravený, je poměrně složité, a na zajištění
správné funkčnosti je potřeba zamykání či jiné techniky, které bývají relativně
pomalé, a tak se jim programátoři snaží vyhnout.
A chyby vzniklé nesprávným ošetřením přepínání vláken bývají složité na odhalení
a vyřešení. Pokud jste absolvovali předmět BI-OSY, jistě víte, o čem mluvíme.

Vlákna jsou příklad *preemptivního multitaskingu*, kdy operační systém rozhoduje,
kdy přepne z jednoho vlákna do druhého, a tuto změnu si prakticky vynutí.
Jednotlivá vlákna se s tím musí vyrovnat.
Alternativou je *kooperativní multitasking*, kdy se jednotlivé úlohy umí *samy* vzdát
procesorového času, když např. čekají na síťovou komunikaci.
Programátor tak ví, že dokud takto nepředá kontrolu ostatním úlohám, žádná jiná
úloha mu pod rukama nemůže měnit stav procesu.
Na druhou stranu je ale potřeba dostatečně často kontrolu předávat, aby se všechny
úlohy dostaly ke slovu.
Tuto techniku tak nemůže používat operační systém, pod kterým můžou běžet i špatně
napsané programy. Ale v rámci jednoho procesu se to dá s úspěchem využít.

Pojďme si to ukázat na příkladu.
Místo síťové komunikace budeme pro názornost čekat, až uplyne nějaký čas: napíšeme si
jednoduchou animaci.
V reálném serveru bychom místo čekání, než uplyne určitý počet sekund, čekali na odpověď
ze sítě, ale principy zůstávají stejné.

```python
import random
import time


def print_blinky(blinky):
    print(blinky, end='\r')


class Blinky:
    def __init__(self):
        self._face = '(o.o)'

    def __str__(self):
        return self._face

    def set_face(self, new):
        self._face = new
        print_blinky(self)

    def run(self):
        while True:
            self.set_face('(-.-)')
            time.sleep(random.uniform(0.05, 0.1))
            self.set_face('(o.o)')
            time.sleep(random.uniform(0.5, 1))


Blinky().run()
```

Chceme-li spustit několik takových animací, můžeme to udělat ve vláknech:

```python
import random
import time
import threading


def print_blinkies():
    for blinky in blinkies:
        print(blinky, end=' ')
    print(end='\r')


class Blinky:
    def __init__(self):
        self._face = '(o.o)'

    def __str__(self):
        return self._face

    def set_face(self, new):
        self._face = new
        print_blinkies()

    def run(self):
        while True:
            self.set_face('(-.-)')
            time.sleep(random.uniform(0.05, 0.1))
            self.set_face('(o.o)')
            time.sleep(random.uniform(0.5, 1))


blinkies = [Blinky() for i in range(10)]

for blinky in blinkies:
    threading.Thread(target=blinky.run).start()
```

Ale po docela jednoduchých změnách se může stát, že se jednotlivá vlákna začnou
přepínat nevhodně, a celý program se rozsype.
Nám stačí malá změna ve funkci `print_blinkies` (podobná funkce by v reálném programu
mohla být z externí knihovny, která při přechodu na novou verzi trošku změnila
vnitřní implementaci):

```python
def print_blinkies():
    for blinky in blinkies:
        time.sleep(0.001)
        print(blinky, end=' ')
    print(end='\r')
```

Tohle se samozřejmě dá řešit např. zámkem kolem volání `print_blinkies`.
Chyby tohoto typu ale mají tendenci se projevovat jen zřídka: i původní
program bez `sleep` byl napsaný špatně, jen se to *většinou* neprojevilo.

Jiný způsob, jak tohle vyřešit, je naimplementovat *smyčku událostí*.
Kdykoli je potřeba pozastavit běh některé úlohy, tak zbytek úlohy naplánujeme
na nějaký pozdější čas, a mezitím spouštíme úlohy, které byly naplánovány
na dříve.

```python
import random
import time


def print_blinkies():
    for blinky in blinkies:
        print(blinky, end=' ')
    print(end='\r')


blinkies = []

class Blinky:
    def __init__(self):
        self.open_eyes()

    def __str__(self):
        return self._face

    def set_face(self, new):
        self._face = new
        print_blinkies()

    def close_eyes(self):
        self.set_face('(-.-)')
        schedule(random.uniform(0.05, 0.1), self.open_eyes)

    def open_eyes(self):
        self.set_face('(o.o)')
        schedule(random.expovariate(1/2), self.close_eyes)


# Scheduling via a list of [remaining time, function to run] pairs:

task_entries = []
def schedule(wait_time, task):
    """Schedule "task" to occur "wait_time" seconds from now"""
    task_entries.append([wait_time, task])

blinkies = [Blinky() for i in range(10)]


# Simple event loop
while task_entries:
    # Get the entry with the least remaining time
    task_entries.sort(key=lambda e: -e[0])
    wait_time, task = task_entries.pop()

    # Wait (this ignores the time needed to actually run code
    time.sleep(wait_time)

    # Decrease remaining time for all tasks by the time waited
    for entry in task_entries:
        entry[0] -= wait_time

    # Run the actual task
    task()
```

V tomto řešení nefigurují vlákna: každá funkce se provede celá najednou,
a ostatní úlohy běží pouze mezi jednotlivými funkcemi jedné úlohy.
Mnohem lépe se tak ověřuje správnost programu.

Tohle řešení je ale docela těžkopádné.
Chtěli jsme napsat *cyklus*, ale místo toho máme dvě funkce, co se "volají"
navzájem. Není z toho poznat, že jde o cyklus.
A to je jen jednoduchý příklad – složitější logika by byla ještě
nepřehlednější.
(Programy pro knihovny jako Twisted nebo Node.js se tradičně píšou tímto způsobem.
Jazyky jako JavaStript na to mají trochu pohodlnější syntaxi, přesto se
pro extrémní případy této nepřehlednosti vžilo označení *callback hell*.)

Naštěstí ale v Pythonu umíme napsat funkce, které lze "pozastavit" – generátory!
S drobnou změnou smyčky událostí lze náš program zapsat opět téměř
procedurálně, ale s tím, že k přepínání úloh dochází jen na
vyznačených místech: tam, kde použijeme `yield`.

```python
import random
import time


def print_blinkies():
    for blinky in blinkies:
        print(blinky, end=' ')
    print(end='\r')


class Blinky:
    def __init__(self):
        self._face = '(o.o)'

    def __str__(self):
        return self._face

    def set_face(self, new):
        self._face = new
        print_blinkies()

    def run(self):
        while True:
            self.set_face('(-.-)')
            yield random.uniform(0.05, 0.1)
            self.set_face('(o.o)')
            yield random.expovariate(1/2)


# Scheduling via a list of [remaining time, generator] pairs:

blinkies = [Blinky() for i in range(10)]

task_entries = [[0, b.run()] for b in blinkies]


# Simple event loop
while task_entries:
    # Get the entry with the least remaining time
    task_entries.sort(key=lambda e: -e[0])
    wait_time, task = task_entries[-1]

    # Wait (this ignores the time needed to actually run code
    time.sleep(wait_time)

    # Decrease remaining time for all tasks by the time waited
    for entry in task_entries:
        entry[0] -= wait_time

    # Run the actual task
    new_time = next(task)
    task_entries[-1][0] = new_time
```

Na tomto principu je postavené moderní API, které se pro podobné úlohy používá.
Než si ho ale ukážeme, pojďme se na chvíli podívat do historie.


Souběžnost v Pythonu
--------------------

V Pythonu existovala a existuje řada knihoven, které nám umožňují "dělat více
věcí zároveň".
Základ jsou `threading`, tedy podpora pro vlákna, a `multiprocessing`, tedy
způsob jak spustit nový pythonní proces, ve kterém se provede určitá funkce
(přičemž vstup a výstup se předává serializovaný přes *pipes*).

Další knihovna, kterou lze z PyPI nainstalovat, je [greenlet].
Ta nám dává k dispozici tzv. *mikro-vlákna*,
která se mezi sebou přepínají v rámci jednoho procesu.
Na rozdíl od systémových vláken nepotřebují tolik paměti navíc, ale
stále jde o *preemptivní* strategii: k přepnutí může dojít kdykoli,
je tedy potřeba zamykat a složitě hledat málo časté chyby.

Byly vyvinuty i knihovny pro *kooperativní* přepínání, založené na tzv.
*futures* (které vysvětlíme vzápětí).
Nejznámější jsou [Twisted] a [Tornado].
Obě jsou relativně staré (2002, resp. 2009), ale stále populární.

Ačkoli byly Twisted, Tornado a podobné knihovny užitečné, jejich problém
byl v tom, že má každá jiné API.
Vznikaly tak kolem nich ekosystémy vázané na konkrétní knihovnu:
server napsaný pro Tornado se nedal použít pod Twisted, a aplikace
využívající Twisted nemohla využít knihovnu pro Tornado.

Jak to vyřešit?


Jeden standard
--------------

![xkcd 927](http://imgs.xkcd.com/comics/standards.png)

*Komiks [xkcd](https://xkcd.com/927/), © Randall Munroe, [CC-BY-NC](http://creativecommons.org/licenses/by-nc/2.5/)*

Podobně jako přístup k různým SQL databázím je v Pythonu standardizovaný
(knihovny pro SQLite, Postgres, MySQL atd. všechny podporují API definované
v [PEP 249]), nebo je standardizované API webových serverů (WSGI, [PEP 3333]),
tak vzniklo standardizované API pro kooperativní multitasking.
Toto API je definováno v [PEP 3156], a jeho referenční implementace, `asyncio`,
je od Pythonu 3.4 ve standardní knihovně.
(Pro Python 3.3 se dá asyncio stáhnout [z PyPI][pypi-asyncio].)
Interně je `asyncio` postavené na konceptu *futures* inspirovaných Tornado/Twisted,
ale jeho "hlavní" API je postavené na *coroutines* podobných generátorům.

Od Pythonu verze 3.5 používá asyncio místo normálních generátorů (`yield from`)
speciální syntaxi, která "asynchronní funkce" dovoluje kombinovat s příkazy
`for` a `with` (a v budoucnu snad i se samotným `yield`).
Tuto syntaxi použijeme i tady; máte-li starší Python, podívejte se na potřebné změny uvedené níže.

Náš příklad s animací vypadá v `asyncio` takto:

```python
import random
import time
import asyncio


def print_blinkies():
    for blinky in blinkies:
        print(blinky, end=' ')
    print(end='\r')


class Blinky:
    def __init__(self):
        self._face = '(o.o)'
        asyncio.ensure_future(self.run())

    def __str__(self):
        return self._face

    def set_face(self, new):
        self._face = new
        print_blinkies()

    async def run(self):
        while True:
            self.set_face('(-.-)')
            await asyncio.sleep(random.uniform(0.05, 0.1))
            self.set_face('(o.o)')
            await asyncio.sleep(random.expovariate(1/2))


blinkies = [Blinky() for i in range(10)]

loop = asyncio.get_event_loop()
loop.run_forever()
loop.close()
```


V Pythonu verze 3.4 a nižší neexistují klíčová slova `async` a `await`, takže je potřeba
místo:

```python
async def ...:
    await ...
```

psát:

```python
@asyncio.coroutine
def ...:
    yield from ...
```

(Zajímavé je, že dekorátor `asyncio.coroutine` toho nedělá mnoho: označí funkci
jako *coroutine*, v *debug* módu zapne něco navíc, a pokud ve funkci není `yield`,
udělá z ní generátor. Téměř vše tak bude fungovat i bez tohoto dekorátoru – ale
doporučujeme ho použít, už jen jako dokumentaci.)

Starý způsob zatím funguje i v novějším Pythonu, a dokonce se objevuje i v dokumentaci.

[greenlet]: https://greenlet.readthedocs.io/en/latest/
[Tornado]: http://www.tornadoweb.org/en/stable/
[Twisted]: https://twistedmatrix.com/trac/
[PEP 249]: https://www.python.org/dev/peps/pep-0249/
[PEP 3333]: https://www.python.org/dev/peps/pep-3333/
[PEP 3156]: https://www.python.org/dev/peps/pep-3156/
[pypi-asyncio]: https://pypi.python.org/pypi/asyncio


Event Loop
----------

Knihovna `asyncio` nám dává k dispozici *smyčku událostí*, která se, podobně jako
`app.exec` v Qt, stará o plánování jednotlivých úloh.
Každé vlákno může mít vlastní smyčku událostí, kterou získáme pomocí
`asyncio.get_event_loop`, a pak ji můžeme spustit dvěma způsoby:

* `loop.run_forever` spustí smyčku na tak dlouho, dokud jsou nějaké úlohy
  naplánovány (to trochu odporuje názvu, ale většinou se nestává že by se
  úlohy "vyčerpaly"), nebo
* `loop.run_until_complete` – tahle funkce skončí hned, jakmile je hotová
  daná úloha, a vrátí její výsledek.



Futures
-------

Jak už bylo řečeno, knihovna `asyncio` je uvnitř založená na *futures*.
Copak to je?

`Future` je objekt, který reprezentuje budoucí výsledek nějaké operace.
Poté, co tato operace skončí, se výsledek dá zjistit pomocí metody `result()`;
jestli je operace hotová se dá zjistit pomocí `done()`.
`Future` se dá popsat jako "krabička" na vrácenou hodnotu – než tam něco
tu hodnotu dá, musíme počkat, a poté je hodnota stále k dispozici.
Tohle čekání se dělá pomocí `await` (nebo `loop.run_until_complete`).

```python
import asyncio


async def set_future(fut):
    """Sets the value of a Future, after a delay"""
    await asyncio.sleep(1)
    fut.set_result(123)


async def get_future(fut):
    """Receives the value of a Future, once it's ready"""
    await fut
    result = fut.result()
    return result


future = asyncio.Future()


# Schedule the "set_future" task (explained later)
asyncio.ensure_future(set_future(future))


# Run the "get_future" coroutine until complete
loop = asyncio.get_event_loop()
result = loop.run_until_complete(get_future(future))
loop.close()

print(result)
```

Do `Future` se dá vložit i výjimka: pokud proces, který by `Future`
naplnil, selže, může výjimku uložit do `Future` místo výsledku,
a `result()` potom tuto výjimku způsobí v kódu, který by výsledek zpracovával.

Na `Future` se navíc dají navázat funkce, které se zavolají jakmile je
výsledek k dispozici.
Dá se tak implementovat *callback* styl programování, který jsme si
popsali výše – takhle, pomocí *futures* & *callbacks* se před nástupem
generátorů programovalo pro knihovny jako `Twisted`.

A ještě jedna věc: `await` (podobně jako `yield`) je výraz, jehož
hodnota je výsledek dané `Future`.
Kód výše tak můžeme zjednodušit:

```python
async def get_future(fut):
    """Receives the value of a Future, once it's ready"""
    return (await fut)
```

Další vlastnost `Future` je ta, že se dá "zrušit": pomocí `Future.cancel()`
signalizujeme úloze, která má připravit výsledek, že už ten výsledek
nepotřebujeme.
Po zrušení bude `result()` způsobovat `CancelledError`.


Async funkce a Task
-------------------

Jak jsme viděli v příkladu s animací, používání *callback* funkcí je těžkopádné.
`Future` situaci trochu zlepšije, ale ne o moc.
V `asyncio` se `Future` používají hlavně proto, že je na ně jednoduché
navázat existující knihovny.
Aplikační kód je ale lepší psát pomocí `async` funkcí, tak jako v příkladu
výše.

Asynchronní funkce se dají kombinovat pomocí `await` podobně jako generátory
pomocí `yield from`.
Nevýhoda async funkcí spočívá v tom, že na každé zavolání async funkce lze
použít jen jeden `await`: na rozdíl od `Future` se výsledek nikam neukládá;
jen se po skončení jednou předá.

```python
import asyncio

async def add(a, b):
    await asyncio.sleep(1)
    return a + b

async def demo():
    coroutine = add(2, 3)
    print('The result is:', (await coroutine))
    print('The result is:', (await coroutine))  # chyba!


loop = asyncio.get_event_loop()
result = loop.run_until_complete(demo())
loop.close()
```

Tenhle problém můžeme vyřešit tak, že asynchronní funkci "zabalíme" do `Future`.
Na to ma dokonce `asyncio` speciální funkci `ensure_future`, která:

* dostane-li asynchronní funkci, "zabalí" ji do `Future`, a
* výsledek přímo naplánuje na smyčce událostí, takže se asynchronní funkce
  časem začne provádět.

```python
async def demo():
    coroutine = asyncio.ensure_future(add(2, 3))
    print('The result is:', (await coroutine))
    print('The result is:', (await coroutine))  # OK!
```

Výsledek `ensure_future` je speciální druh `Future` zvaný `Task`.
Ten má oproti normální `Future` několik vlastností navíc, ale v podstatě
ho zmiňujieme jen proto, abyste věděli co `Task` znamená, až se vám objeví v
chybové hlášce.


Fan-Out a Fan-In
----------------

S pomocí asynchronních funkcí můžeme nad našimi programy přemýšlet tak,
jako by to byly "normální" procedurálně zapsané algoritmy: máme jedno
"vlákno", které se provádí od začátku do konce, jen na některých místech
(označených `await`) se provádění přeruší a zatímco náš kód čeká na výsledek
nějaké operace, může se spustit jiný kus kódu.
Funkce, na které je takto potřeba čekat, bývají v dokumentaci patřičně
označeny.
V síťovém programování je to většinou čtení ze socketů nebo inicializace
či ukončení serveru.

Pomocí `ensure_future` a `await` můžeme ale dělat něco navíc:
rozdělit běh našeho programu na víc úloh, které se budou vykonávat "souběžně" –
například autor scraperu chce stáhnout několik stránek najednou,
nebo server souběžně odpovídá na několik požadavků.
Tomuto rozdělení se říká *fan-out*.

Opačná operace je *fan-in*, kdy několik úloh opět spojíme do jedné.
Výše uvedený scraper může počkat, než jsou všechny stránky stažené –
typicky pomocí jednoho `await` pro každý `Task`, po kterém může
pokračovat zpracováním získaných dat.

Co se týče Webového serveru, může se zdát, že tady není potřeba explicitně
počkat na výsledek každého úkolu.
Ale není to tak – i tady je poměrně důležité na každou úlohu nastartovanou
pomocí `ensure_future` "počkat" pomocí `await` – už jen proto, abychom
zachytili případnou výjimku.
Neuděláme-li to, `asyncio` bude (minimálně v *debug módu*) vypisovat
chybové hlášky.


Asynchronní cykly a kontexty
----------------------------

Až budete používat některé "asynchronní" knihovny, setkáte se pravděpodobně se dvěma
novými konstrukcemi: `async for` a `async with`.

Fungují jako jejich "ne-`async`" varianty, jen na začátku a konci každé iterace (resp.
na začátku a konci bloku) můžou přerušit vykonávání funkce – podobně jako `await`.

Typický příklad je u databází: začátek a konec transakce i získávání jednotlivých
řádků pravděpodobně potřebují komunikaci po síti, takže hypotetická databázová
knihovna by se mohla používat nějak takto:

```python
async with database.transaction():
    await database.execute('UPDATE ...')
    async for row in (await database.execute('SELECT ...')):
        handle(row)
```


Komunikace
----------

Ono `io` v `asyncio` naznačuje, že je tato knihovna dělaná především na
vstup a výstup – konkrétně na komunikaci přes síť (případně s jinými procesy).

Ke komunikaci používá `asyncio` tři úrovně abstrakce: `Transport`, `Protocol`,
a `Stream`.
V krátkosti si je tu popíšeme; detaily pak najdete v dokumentaci (je pro nás
totiž mnohem důležitější abyste pochopili principy, než abyste uměli konkrétní
API, které lze dohledat v dokumentaci).

Transporty a protokoly jsou postaveny na konceptech knihovny `Twisted`.

`Transport` zajišťuje samotné posílání bajtů mezi počítači (transportní vrstvu), kdežto
`Protocol` implementuje nějaký aplikační protokol.
`Transport` většinou nepíšeme sami, použijeme existující.
V `asyncio` jsou zabudované transporty pro TCP, UDP a SSL.
`Protocol` je pak použit pro implementaci konkrétních protokolů jako
`HTTP`, `FTP`, a podobně.
V dokumentaci najdete podrobnější popis včetně [příkladů][transport-proto-examples].

[transport-proto-examples]: https://docs.python.org/3/library/asyncio-protocol.html#tcp-echo-server-protocol

Kromě toho existuje i "Stream API" založené na asynchronních funkcích.
Většinou platí, že operace *otevření*, *čtení*, *flush* a *zavření* Streamu
jsou asynchronní funkce (v dokumentaci označované jako *coroutines*), a je
tedy nutné je použít s `await`; oproti tomu *zápis* asynchronní není – data
se uloží do bufferu a pošlou se, až to bude možné.

Typicky ale místo čistého `asyncio` použijeme existující knihovnu.
Tady je příklad z knihovny `aiohttp`, která implementuje server a klienta
pro HTTP:

```python
import asyncio
import aiohttp

async def main(url):
    # Use a a session
    session = aiohttp.ClientSession()
    async with session:

        # Get the response (acts somewhat like a file; needs to be closed)
        async with session.get(url) as response:

            # Fetch the whole text
            html = await response.text()
            print(html)

loop = asyncio.get_event_loop()
loop.run_until_complete(main('http://python.cz'))
loop.close()
```


A další
-------

Nakonec několik tipů, o kterých je dobré vědět.

V `asyncio` najdeme synchronizační mechanismy známé z vláknového programování, např.
`Lock` a `Semaphore` – viz [dokumentace](https://docs.python.org/3/library/asyncio-sync.html).

Musíme-li použít blokující funkci, která např. komunikuje po síti bez `await`, a která by
tedy zablokovala i všechny ostatní úlohy, můžeme použít
`loop.run_in_executor()`, a tím danou funkci zavolat ve vlákně nebo podprocesu, ale výsledek zpřístupnit
pomocí `asyncio.Future`.
Použití je opět popsáno v [dokumentaci](https://docs.python.org/3/library/asyncio-eventloop.html#executor).

Občas vás při programování s `asyncio` zaskočí zrádná chyba.
V takových případech je dobré zapnout *debug* režim pomocí proměnné prostředí `PYTHONASYNCIODEBUG=1`.
V tomto režimu asyncio upozorňuje na časté chyby, do některých chybových výpisů přidává informaci o tom,
kde aktuální `Task` vznikl, apod.
Více informací je zase v [dokumentaci](https://docs.python.org/3/library/asyncio-dev.html#asyncio-dev).


AsyncIO a Qt
------------

Jak bylo zmíněno na začátku, hlavní cíl `asyncio` je definovat společné rozhraní
pro různé asynchronní knihovny, aby bylo možné např. kombinovat knihovny pro
Tornado se smyčkou událostí v Twisted.
Samotná knihovna `asyncio` je jen jedna z mnoha implementací tohoto rozhraní.
Zajímavá je například knihovna [uvloop], která je asi 2-4× rychlejší než `asyncio`
(ale má závislosti, které se pro součást standardní knihovny nehodí).

Další zajímavá implementace je [Quamash], která pod standardním `asyncio` API používá
smyčku událostí z Qt.
Umožňuje tak efektivně zpracovávat Qt události zároveň s asynchronními funkcemi
známými z `asyncio`.

*Event loop* z `quamash` je potřeba na začátku programu naimportovat a nastavit
jako hlavní smyčku událostí:

```python
from quamash import QEventLoop

app = QtWidgets.QApplication([])
loop = QEventLoop(app)
asyncio.set_event_loop(loop)
```

a poté ji, místo Qt-ovského `app.exec()`, spustit:

```python
loop.run_forever()
```

Jednotlivé asynchronní funkce se pak používají jako v čistém `asyncio`:
pomocí `asyncio.ensure_future`, `await`, atd.

[uvloop]: https://pypi.python.org/pypi/uvloop/
[Quamash]: https://pypi.python.org/pypi/Quamash

Ukázka:

```python
import asyncio

from PyQt5 import QtGui, QtWidgets
from quamash import QEventLoop

app = QtWidgets.QApplication([])
loop = QEventLoop(app)
asyncio.set_event_loop(loop)

display = QtWidgets.QLCDNumber()
display.setWindowTitle('Stopwatch')

display.show()

async def update_time():
    value = 0
    while True:
        display.display(value)
        await asyncio.sleep(1)
        value += 1

asyncio.ensure_future(update_time())

loop.run_forever()
```


Úkol
====

Vaším úkolem za 5 bodů je vytvořit asynchronní třídy reprezentující jednotlivé postavy v bludišti a rozhraní umožňující je spustit.

Program musí stále splňovat zadání z předchozího cvičení, zejména:

 * nesmí při žádné interakci uživatele s rozhraním zhavarovat
 * musí se dát nainstalovat a spustit pomocí `python -m pip install -r requirements.txt`; `python setup.py develop`; `python -m maze`

Do programu přidejte rozhraní pro spuštění hry.
Doporučujeme přidat do menu a lišty nástrojů `QAction` s atributem `checkable=True`.
Můžete ale použít i jiný vhodný způsob, kterým lze režim hry zapnout, ale i vypnout (přechod zpět do editačního módu).

Není možné začít hrát, pokud od některé z postav nevede žádná cesta k cíli. Této situaci vhodně zabraňte.

Do vizualizátoru bludiště doplňte funkcionalitu hry. V režimu hry:

 * nebudou zobrazeny čáry od postav k cíli
 * půjde pouze bořit či stavět zdi
  * pokud máte více typů zdí, půjde bořit/stavět pouze jeden druh z nich (`-1`)
  * zeď nepůjde stavět na políčko, kde je aktuálně nějaké postava
  * postavit zeď půjde pouze tehdy, pokud to žádnou postavu neodřízne od cíle
 * nebude vidět paleta
 * úkolem hráče je měnit bludiště tak, aby co nejdéle bránil postavám dojít do cíle
  * v případě že libovolná postava dojde do libovolného cíle, hra končí
   * v takovém případě informujte hráče o tom, jak dlouho vydržel odolávat náporu postav

Máte k dispozici základní třídu `Actor`, která reprezentuje aktora (postavu v bludišti).

XXX class Actor

Tato třída definuje rozhraní jednotlivých postav a zároveň implementuje základní chování postavy - jde nejkratší cestou k cíli rychlostí jedno políčko za sekundu.
Aby to mohlo fungovat, musí kód, který postavu používá:

 * na začátku hry udělat kopii matici bludiště (aby se bylo možné vrátit do editačního módu) a všechny postavy z ní "vyndat" a inicializovat je jako aktory
 * při zavolání `update_actor(actor)` zjistit, kde se postava nachází a překreslit ji,
 * při ukončení hry nebo programu všem aktorům říct, že se mají zrušit svůj task
   * *tip:* na úklid po skončení hlavní smyčky událostí se hodí `loop.run_until_complete()`

Je třeba použít smyčku událostí z `quamash`.

Rozhraní je definováno tak, aby nezáviselo na konkrétní implementaci vizualizace, uvnitř aktorů byste tedy neměli používat nic z Qt.
Některé charaktery (viz další sekce) možná budou potřebovat použít další API vašeho gridu.

Kromě úpravy rozhraní musíte implementovat několik aktorů, kteří dědí z třídy Actor a chovají se trochu jinak.

Aktoři
------

V bludišti máte 5 typů postav. Každá by měla mít jiné chování.
Každá postava vychází svým chováním ze základního aktora, jde tedy k cíli nejkratší možnou cestou rychlostí jedno políčko za sekundu,
pokud popis neříká jinak.

Zde je seznam různých charakterů. Každé postavě přiřaďte jeden charakter podle typu postavy (barva na obrázku, číslo v matici).

Charakterů je více než 5. Můžete si vybrat, kterých 5 použijete, musíte jich však použít minimálně 5 různých.
Musíte implementovat alespoň dva z hvězdičkou označených charakterů.

Poznámka o rychlostech: Když je nějaká postava rychlejší, neznamená to, že ve vašem cyklu v metodě `behavior` bude dělat delší kroky,
ale že jeden krok bude trvat kratší dobu (metoda `step` má atribut `duration`).

Při rozhodování o chování postav berte v úvahu hratelnost hry.

### Rychlík

Rychlík má stabilně o 75 % vyšší rychlost než základní aktor.

### Zrychlovač

Zrychlovač může po každém kroku s určitou pravděpodobností trvale zvýšit svou rychlost.
Čím déle chodí, tím rychlejší může být. Pravděpodobnost nastavte tak, aby hra byla hratelná; zrychlení tak, aby bylo znatelné (např. o čtvrt políčka za sekundu).
Doporučujeme nastavit i rychlostní strop, případně zrychlovat stále o menší a menší hodnotu.

### Skokan \*

Pokud je za jedním políčkem zdi průchozí políčko, odkud je cesta do cíle alespoň o 5 políček kratší, než z místa, kde se Skokan nachází,
Skokan touto zdí projde (přeskočí ji). Kvůli hratelnosti doporučujeme nastavit limity na to, jak často se toto může dít,
případně zakázat projít zdí přímo na cíl apod.

Chcete-li, můžete implementovat animaci skoku přes zeď.

### Teleportér \*

Teleportér se místo kroku může s určitou pravděpodobností teleportovat na náhodné průchozí a dostupné místo bludiště.
Při teleportu se postavička na malou chvíli rozechvěje, pak se přemístí a po chvilce se přestane chvět.
Celá akce by měla trvat méně než sekundu.
Doporučujeme zakázat teleport na políčka příliš blízko cíli.

### Zmatkář

Zmatkář s určitou pravděpodobností místo kroku směrem k cíli provede krok náhodným průchozím směrem (pokud to je možné, tak jiným, než ze kterého přišel).

### Sprinter

Sprinter zrychluje na rovných trasách.
Pokud půjde klikatou cestou, je stejně pomalý jako základní aktor. Pokud ale půjde déle rovně, může být velmi rychlý.
Na začátku hry a po každé změně směru má rychlost jako základní aktor.
Každý další pohyb ve stejném směru ale vykonává rychleji, než ten předchozí.
Pohyb v jiném směru je opět základní rychlostí.

Doporučujeme nastavit rychlostní strop, případně zrychlovat stále o menší a menší hodnotu.

Poznámka: Sprinter může chodit stejnou cestou jako základní aktor, nemusí cestu optimalizovat pro svoji schopnost.

### Pravák \*

Pravák se pohybuje bludištěm podle [pravidla pravé ruky](https://en.wikipedia.org/wiki/Maze_solving_algorithm#Wall_follower), místo toho, aby šel rovnou nejkratší cestou k cíli.
Pokud má kolem sebe nějakou zeď, jde podél ní.
Pokud se nachází ve volném prostoru a pravidlo nemůže aplikovat (např. na začátku, nebo pokud mu hráč jeho zeď zboří), chová se jako standardní aktor, dokud zeď nenajde nebo nedojde do cíle.

Chcete-li, můžete detekovat, jestli se Pravák někde nezacyklil, a pokud ano, udělat nějaké rozumné kroky k tomu, aby se z prekérní situace dostal.

### Dobíječ

Dobíječ nejprve stojí na místě náhodnou dobu (s exponenciálním rozdělením a střední hodnotou 5 sekund), dobíjí energii.
Pak ujde tolik kroků, kolik celých sekund čekal, rychlostí 3 políčka za sekundu. A opět dobíjí/čeká...
Z dlouhodobého hlediska se tedy pohybuje pomaleji než základní aktor, ale je nevyzpytatelnější.
Při dobíjení si jednou za sekundu poskočí, aby hráč věděl, že tato postava se nezasekla.
(Dobíjení můžete signalizovat nějak sofistikovaněji.)

### Tanečník

Před každým krokem zkontroluje políčko před sebou (tj. ve směru cesty k cíli),
diagonálně vpravo před sebou, a vpravo od sebe. Pokud jsou všechna tři volná, projde je
a vrátí se zpět na původní políčko.
Poté to samé udělá s políčky před sebou, diagonálně vlevo před sebou, a vlevo
od sebe.
Pak teprve udělá krok dopředu.

Pokud hráč políčko, na které by měl Tanečník vstoupit, zastaví zdí,
Tanečník poskočí, zbytek aktuálního "tance" neprovede, a pokračuje z aktuálního políčka.

### Tlusťoch \*

Pohybuje se o 25 % pomaleji než základní aktor.

Nesmí vstoupit na políčko, na kterém je právě jiný aktor.
Měl-li by to udělat, stojí místo toho na místě a odpočívá.

Ostatní aktoři nesmí vstoupit na políčko, kde se právě nachází (nebo na které
právě vstupuje) Tlusťoch. Pohybují se tak, jako by na pozici Tlusťocha byla zeď,
tj. základní aktor se Tlusťocha snaží obejít, a pokud to nejde, skáče na místě.

(Pravák Tlusťocha nepovažuje za zeď, podél které má jít; v případě, že mu Tlusťoch překáží, skáče na místě.
Teleportér se na Tlusťocha nesmí teleportovat.)

Tlusťoch ale nemá vliv na hráčovu schopnost stavět zdi, tj. pro tento účel se
nepočítá jako překážka.

### Smraďoch \*

Smraďoch všem kromě ostatních Smraďochů smrdí, a chtějí od něj pryč.
Pokud je v bezprostředním okolí (určete sami) ostatních aktorů (jiných charakterů), tito aktoři, pokud mohou, jdou směrem pryč od Smraďocha
(bez ohledu na svou plánovanou trasu), až dokud se z dosahu Smraďocha nedostanou.
Pokud nemohou pryč, se smradem se smíří a chovají se normálně.

Při chůzi směrem pryč od Smraďocha se aktoři pohybují rychlostí dle svého charakteru.
Tanečník (pokud může) tančí, Dobíječ (pokud musí) se dobíjí atp.

Je na vás, jestli Smraďoch smrdí i přes zdi. Chcete-li, můžete rozsah smradu vizualizovat.

### Vlastní

Implementujte jiné netriviální chovaní. Svůj záměr popište v README.

Vyhněte se i triviálním variantám jiných chování, které jste již implementovali
(např. máte-li Rychlíka, nedělejte v rámci vlastního zadání "Pomalíka", který je jen o trochu pomalejší než základní aktor.)

Nakolik je chování netriviální, určujeme při hodnocení my.
V případě pochybností se zeptejte pomocí issue nebo na cvičení.


Odevzdání, deadliny apod.
-------------------------

Váš úkol se skládá prakticky ze dvou částí:

 * úprava GUI pro novou funkcionalitu
 * asynchronní programování aktorů

A zároveň je to poslední úkol kromě semestrálky.

Proto na něj máte čas až do středy 28.12. 11:00. Nekažte si ale prosím kvůli úkolu Vánoce (a ani od nás v průběhu svátků nečekejte velkou komunikaci).

Odevzdávejte standardně s tagem `v0.4`. V případě potřeby opět můžete využít naše [řešení](http://github.com/encukou/maze) minulého úkolu.
