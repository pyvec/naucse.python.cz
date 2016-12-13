Generátory a AsyncIO
====================

Dnes bude opět potřeba PyQt5.
Můžete použít virtualenv z minula, nebo se nainstalovat znovu (viz minulá lekce).
(Nejde-li to, nevadí – úplně nezbytné dnes PyQt nebude.)

Knihovny pro dnešní den:

    python -m pip install --upgrade pip
    python -m pip install asyncio aiohttp quamash

---

Dnes se podíváme na dvě témata, která spolu souvisí čím dál tím méně, ale je dobré
porozumět napřed *generátorům*, a poté si vysvětlit *asynchronní programování*.


Generátory
==========

XXX: Iterátory; protokol: __iter__, __next__
XXX: yield
XXX: Generátorová funkce vs. generátorový iterátor
XXX: return
XXX: send
XXX: throw
XXX: yield from
XXX: contextmanager


AsyncIO
=======

A teď něco úplně jiného: asynchronní programování.

Jak jsme si řekli v lekci o C API, Python má globální zámek, takže pythonní kód
může běžet jen v jednom vlákně najednou.
Taky jsme si řekli, že to většinou příliš nevadí: typický síťový nebo GUI program
stráví hodně času čekáním na události (odpověď z 'netu, kliknutí myší), a u tohoto
čekání není potřeba držet zámek zamčený.

Servery typicky při zpracovávání požadavku stráví *většinu* času síťovou komunikací.
Proto se často spouští několik vláken nebo přímo procesů najednou, aby se mohl vytížit
procesor.
Při velkém množství vláken ale nastanou dva problémy.
První je, že vláken nemůže být neomezeně mnoho.
Každé vlákno potřebuje vlastní stack, tj. poměrně velkou část paměti; a počet vláken
bývá omezen i jinak (na Linuxu je globální limit počtu procesů, viz `cat /proc/sys/kernel/threads-max`).
Druhý problém je, že přepnutí z jednoho vlákna do druhého se může stát *kdykoli*.
Ověřit si, že je na to program připravený, je poměrně složité, a na zajištění
správné funkčnosti je potřeba zamykání či jiné techniky, které bývají relativně
pomalé, a tak se jim programátoři snaží vyhnout.
A chyby vzniklé nesprávným ošetřením přepínání vláken bývají složité na odhalení
a vyřešení.

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
jednoduchou animaci:

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
    print(*blinkies, sep=' ', end='\r')


blinkies = []

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
            time.sleep(random.expovariate(1/2))

blinkies = [Blinky() for i in range(15)]

for blinky in blinkies:
    threading.Thread(target=blinky.run).start()
```

Ale po docela jednoduchých změnách se může stát, že se jednotlivá vlákna začnou
přepínat nevhodně, a celý program se rozsype:

```python
    def __str__(self):
        time.sleep(0.001)
        return self._face
```

Tohle se samozřejmě dá řešit např. zámkem ve funkci `print_blinkies`.
Chyby tohoto typu ale mají tendenci se objevovat jen zřídka: i původní
program bez `sleep` byl napsaný špatně, jen se to *většinou* neprojevilo.

Jiný způsob, jak tohle vyřešit, je naimplementovat *smyčku událostí*.
Kdykoli je potřeba pozastavit běh některé úlohy, tak zbytek úlohy naplánujeme
na nějaký pozdější čas, a mezitím spouštíme úlohy, které byly naplánovány
na dříve.

```python
import random
import time


def print_blinkies():
    print(*blinkies, sep=' ', end='\r')


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


task_entries = []
def schedule(wait_time, task):
    """Schedule "task" to occur "wait_time" seconds from now"""
    task_entries.append([wait_time, task])

blinkies = [Blinky() for i in range(15)]


# Simple event loop
while task_entries:
    # Get the entry with the least remaining time
    task_entries.sort(reverse=True)
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
Chtěli jsme napsat smyčku, ale místo toho máme dvě funkce, co se volají
navzájem.
Složitější logika by pak byla ještě nepřehlednější.

Naštěstí ale v Pythonu umíme napsat funkce, které lze "pozastavit".
S drobnou změnou smyčky událostí lze náš program zapsat opět téměř
procedurálně, ale s tím, že k přepínání úloh dochází jen na
vyznačených místech: tam, kde použijeme `yield`.

```python
import random
import time


def print_blinkies():
    print(*blinkies, sep=' ', end='\r')


blinkies = []

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


task_entries = []
def schedule(wait_time, task):
    """Schedule "task" to occur "wait_time" seconds from now"""
    task_entries.append([wait_time, task])

blinkies = [Blinky() for i in range(15)]

task_entries = [[0, b.run()] for b in blinkies]


# Simple event loop
while task_entries:
    # Get the entry with the least remaining time
    task_entries.sort(key=lambda e: -e[0])
    wait_time, index, task = task_entries[-1]

    # Wait (this ignores the time needed to actually run code
    time.sleep(wait_time)

    # Decrease remaining time for all tasks by the time waited
    for entry in task_entries:
        entry[0] -= wait_time

    # Run the actual task
    new_time = next(task)
    task_entries[-1][0] = new_time
```


Souběžnost v Pythonu
--------------------

V Pythonu existovala a existuje řada knihoven, které nám umožňují "dělat více
věcí zároveň".
Základ jsou `threading`, tedy podpora pro vlákna, a `multiprocessing`, tedy
způsob jak spustit nový pythonní proces, ve kterém se provede určitá funkce
(přičemž vstup a výstup se předává serializovaný přes *pipes*).

Další knihovna je [greenlet]. Ta nám dává k dispozici tzv. *mikro-vlákna*,
která se mezi sebou přepínají v rámci jednoho procesu.
Na rozdíl od systémových vláken nepotřebují tolik paměti navíc, ale
stále jde o *preemptivní* strategii: k přepnutí může dojít kdykoli,
je tedy potřeba zamykat a složitě hledat málo časté chyby.

Byly vyvinuty i knihovny pro *kooperativní* přepínání, založené na tzv.
*futures* (které vysvětlíme vzápětí).
Nejznámější jsou [Twisted] a [Tornado].
Obě jsou relativně staré (2001, resp. 2009), ale stále populární.

Ačkoli byly Twisted, Tornado a podobné knihovny užitečné, jejich problém
byl v tom, že má každá jiné API.
Vznikaly tak kolem nich ekosystémy vázané na konkrétní knihovnu:
server napsaný pro Tornado se nedal použít pod Twisted, a aplikace
využívající Twisted nemohla využít knihovnu pro Tornado.

Jak to vyřešit?

Jeden standard
--------------

![XKCD 927](http://imgs.xkcd.com/comics/standards.png)

*Komiks z [XKCD](https://xkcd.com/927/), © Randall Munroe, [CC-BY-NC](http://creativecommons.org/licenses/by-nc/2.5/)*

Podobně jako přístup k různým SQL databázím je v Pythonu standardizovaný
(knihovny pro SQLite, Postgres, MySQL atd. všechny podporují API definované
v [PEP 249]), nebo je standardizované API webových serverů (WSGI, [PEP 3333]),
tak vzniklo standardizované API pro kooperativní multitasking.
Toto API je definováno v [PEP 3156], a jeho referenční implementace, `asyncio`,
je od Pythonu 3.4 ve standardní knihovně.
(Pro Python 3.3 se dá asyncio stáhnout [z PyPI][pypi-asyncio].)
Interně je `asyncio` postavené na konceptu *futures* inspirovaných Tornado/Twisted,
ale jedno "hlavní" API je postavené na *coroutines* podobných generátorům.

Od Pythonu verze 3.5 používá asyncio místo normálních generátorů (`yield from`)
speciální syntaxi, která "asynchronní funkce" dovoluje kombinovat s konstrukcemi\
`for` a `with` (a v budoucnu snad i `yield`).
Tuto syntaxi použijeme i tady; máte-li starší Python, podívejte se na potřebné změny uvedené níže.

Náš příklad s animací vypadá v `asyncio` takto:

```python
import random
import time
import asyncio


def print_blinkies():
    print(*blinkies, sep=' ', end='\r')


blinkies = []

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


blinkies = [Blinky() for i in range(15)]

loop = asyncio.get_event_loop()
loop.run_forever()
loop.close()
```



V Pythonu verze 3.4 a nižší neexistují klíčová slova `async` a `await`, takže je potřeba
místo:

    async def ...:

    await ...


psát:

    @asyncio.coroutine
    def ...:
        yield from ...

(Zajímavé je, že dekorátor `asyncio.coroutine` toho nedělá mnoho: označí funkci
jako *coroutine*, v *debug* módu zapne něco navíc, a pokud ve funkci není `yield`,
udělá z ní generátor. Dokonce bude téměř vše fungovat i bez dekorátoru – ale
doporučuje se ho použít, už jen jako dokumentaci.)

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
* `loop.run_until_complete` – tahle funkce skončí hned jakmile je hotová
  daná úloha, a vrátí její výsledek.



Futures
-------

Jak už bylo řečeno, knihovna `asyncio` je založená na *futures*.
Copak to je?

`Future` je objekt, který reprezentuje budoucí výsledek nějaké operace.
Poté, co tato operace skončí, se výsledek dá zjistit pomocí metody `result()`;
jestli je operace hotová se dá zjistit pomocí `done()`.
`Future` se dá popsat jako "krabička" na vrácenou hodnotu – než tam něco
tu hodnotu dá, musíme počkat, a poté je hodnota stále k dispozici.
Tohle čekání se dělá pomocí `await`.

XXX: Future

Do `Future` se dá vložit i výjimka: pokud proces, který by `Future`
naplnil, selže, může výjimku uložit do `Future` místo výsledku,
a `result()` potom tuto výjimku způsobí v kódu, který by výsledek zpracovával.

Na `Future` se navíc dají navázat funkce, které se zavolají jakmile je
výsledek k dispozici.
Dá se tak implementovat *callback* styl programování, který jsme si
popsali výše – takhle se před nástupem generátorů programovalo pro
knihovny jako `Twisted`.

A ještě jedna věc: `await` (podobně jako `yield`) je výraz, jehož
hodnota je výsledek dané `Future`.
Kód výše tak můžeme zjednodušit:

XXX: Future, await expression

Další vlastnost `Future` je ta, že se dá "zrušit": pomocí `Future.cancel()`
signalizujeme úloze, která má připravit výsledek, že už ten výsledek
nepotřebujeme.
Po zrušení bude `result()` způsobovat `CancelledError`.


Async funkce a Task
-------------------

Jak jsme viděli v příkladu s animací, používání *callback* funkcí
– a tedy samotných `Future` je těžkopádné.
V `asyncio` se `Future` používají hlavně proto, že je na ně jednoduché
navázat existující knihovny.
Aplikační kód je ale lepší psát pomocí `async` funkcí, tak jako v příkladu
výše.

Asynchronní funkce se dají kombinovat pomocí `await` podobně jako generátory
pomocí `yield from`.
Nevýhoda async funkcí spočívá v tom, že na každé zavolání async funkce lze
použít jen jeden `await`: na rozdíl od `Future` se výsledek nikam neukládá;
jen se po skončení jednou předá.

XXX: Rozepsat; přidat příklad

Tenhle problém můžeme vyřešit tak, že asynchronní funkci "zabalíme" do `Future`.
Na to ma dokonce `asyncio` speciální funkci `ensure_future`, která:

* dostane-li asynchronní funkci, "zabalí" ji do `Future`, a
* výsledek přímo naplánuje na smyčce událostí, takže se asynchronní funkce
  časem začne provádět.

Výsledek `ensure_future` je speciální druh `Future` zvaný `Task`.
Ten má oproti normální `Future` několik vlastností navíc, ale v podstatě
ho zmiňuji jen proto, abyste věděli co `Task` znamená, až se objeví v
chybové hlášce.


Fan-Out a Fan-In
----------------

S pomocí asynchronních funkcí můžeme nad našimi programy přemýšlet tak,
jako by to byly "normální" procedurálně zapsané algoritmy: máme jedno
"vlákno", které se provádí od začátku do konce, jen na některých místech
(označených `await`) se provádění přeruší a může se spustit jiný kus
kódu, zatímco náš kód čeká na výsledek nějaké operace.
Funkce, na které je takto potřeba čekat, jsou patřičně označeny – v síťovém
programování je to většinou čtení ze socketů (ale už ne zápis), nebo
inicializace serveru.

Pomocí `ensure_future` a `await` můžeme ale dělat něco navíc:
rozdělit běh našeho programu na víc úloh, které se budou vykonávat "souběžně" –
například autor scraperu chce stáhnout několik stránek najednou,
nebo server souběžně odpovídá na několik požadavků.
Tomuto rozdělení se říká *fan-out*.

Opačná operace je *fan-in*, kdy několik úloh opět spojíme do jedné.
Výše uvedený scraper může počkat, než jsou všechny stránky stažené –
typicky pomocí `await` pro každý `Task`.
Pak může pokračovat zpracováním získaných dat.

Co se týče Webového serveru, může se zdát, že tady není potřeba explicitně
počkat na výsledek každého úkolu.
Ale není to tak – i tady je poměrně důležité na každou úlohu nastartovanou
pomocí `ensure_future` "počkat" pomocí `await` – už jen proto, abychom
zachytili případnou výjimku.
Neuděláme-li to, `asyncio` bude (minimálně v *debug módu*) vypisovat
chybové hlášky.


Asynchronní cykly a kontexty
----------------------------

XXX: async for
XXX: async with


Komunikace
----------

Ono `io` v `asyncio` naznačuje, že je tato knihovna dělaná především na
vstup a výstup – konkrétně na komunikaci přes síť (případně s jinými procesy).

Ke komunikaci používá `asyncio` tři úrovně abstrakce: `Transport`, `Protocol`,
a `Stream`.
V krátkosti si je tu popíšeme; detaily pak najdete v dokumentaci.

`Transport` zajišťuje
samotné posílání bajtů mezi počítači (transportní vrstvu), kdežto
`Protocol` implementuje nějaký aplikační protokol.
Většinou `Transport` nepíšeme sami, použijeme existující.
V `asyncio` jsou zabudované transporty pro TCP, UDP a SSL.
`Protocol` použijeme pro implementaci konkrétních protokolů jako
`HTTP`, `FTP`, a podobně.
V dokumentaci najdete podrobnější popis včetně [příkladů][transport-proto-examples].

[transport-proto-examples]: https://docs.python.org/3/library/asyncio-protocol.html#tcp-echo-server-protocol

Transporty a protokoly jsou postaveny na konceptech knihovny `Twisted`.

Kromě toho existuje i API založené na asynchronních funkcích: `Stream`.
Většinou platí, že operace *otevření*, *čtení*, *flush* a *zavření* Streamu
jsou asynchronní funkce (v dokumentaci označované jako *coroutines*), a je
tedy nutné je použít s `await`; oproti tomu *zápis* asynchronní není – data
se uloží do bufferu a požlou se, až to bude možné.

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

        # Get the response (acts somewhat like a file; neds to be closed)
        async with session.get(url) as response:

            # Fetch the whole text
            html = await response.text()
            print(html)

loop = asyncio.get_event_loop()
loop.run_until_complete(main('http://python.cz'))
loop.close()
```


XXX: Synchronization primitives
XXX: Executors & Threads

XXX: Debug mode

    https://docs.python.org/3/library/asyncio-dev.html#asyncio-dev

    PYTHONASYNCIODEBUG=1



AsyncIO a Qt
------------

Jak bylo zmíněno na začátku, hlavní cíl `asyncio` je definovat společné rozhraní
pro různé asynchronní knihovny, aby bylo možné např. kombinovat knihovny pro
Tornado se smyčkou událostí v Twisted.
Knihovna `asyncio` je jen referenční implementace, a existují i jiné kompatibilní
implementace.
Zajímavá knihovna je [uvloop], která je asi 2-4× rychlejší než `asyncio` (ale má
závislosti, které se nehodí pro součást standardní knihovny).

Další zajímavá implementace je [Quamash], která pod společným `asyncio` API používá
smyčku událostí z Qt.
Umožňuje tak efektivně zpracovávat Qt události zároveň s asynchronními funkcemi
známými z `asyncio`.

Smyčku událostí z `quamash` je potřeba na začátku programu naimportovat a nastavit
jako hlavní smyčku událostí:


    from quamash import QEventLoop


    app = QApplication(sys.argv)

    loop = QEventLoop(app)

    asyncio.set_event_loop(loop)


a poté ji, místo `app.exec`, spustit:

    loop.run_forever()

Jednotlivé asynchronní funkce se pak používají jako v čistém `asyncio`:
pomocí `asyncio.ensure_future`, `await`, atd.

[uvloop]: https://pypi.python.org/pypi/uvloop/
[Quamash]: https://pypi.python.org/pypi/Quamash


Úkol
====

Vaším úkolem za 5 bodů je vytvořit asynchronní třídy reprezentující jednotlivé postavy v bludišti a rozhraní umožňující je spustit.

Do vizualizátoru bludiště doplňte funkci hry. V režimu hry:

 * nebudou zobrazeny čáry od postav k cíli
 * půjde pouze bořit či stavět zdi
  * (pokud máte dva typy zdí, půjde bořit/stavět pouze jeden druh z nich (`-1`))
  * postavit zeď půjde pouze tehdy, pokud by to žádnou postavu neodřízlo od cíle
   * není tedy možné začít hrát, pokud od všech postav nevede nějaká cesta k cíli, této situaci vhodně zabraňte
 * nebude vidět paleta
 * úkolem hráče je měnit bludiště tak, aby co nejdéle bránil postavám dojít do cíle
  * v případě že libovolná postava dojde do libovolného cíle, hra končí
   * v takovém případě informujte hráče o tom, jak dlouho vydržel odolávat náporu postav

Režim hry by měl jít ukončit (přechod zpět do editačního módu).

Máte k dispozici základní třídu `Actor`, která reprezentuje aktora/postavu v bludišti.

XXX class Actor

Tato třída definuje rozhraní jednotlivých postav a zároveň implementuje základní chování postavy - jde nejkratší cestou k cíli.
Aby to mohlo fungovat, musí kód, který postavu používá:

 * na začátku všechny postavy "vyndat" z matice z bludištěm a inicializovat je jako aktory
 * při zavolání `update_actor(actor)` zjistit, kde se postava nachází/nacházela a překreslit ji,
 * při ukončení hry nebo programu všem akotrům říct, že se mají zrušit svůj task

Zároveň je třeba použít quamash.

Rozhraní je definováno tak, aby nezáviselo na konkrétní implementaci vizualizace.

XXX
