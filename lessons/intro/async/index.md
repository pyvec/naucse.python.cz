
Ve cvičení použijeme ukázku z PyQt5.
Máte-li ještě virtualenv s nainstalovaným PyQt, použijte ho, případně ho
podle [lekce o PyQt] nainstalujte znovu.

K PyQt si přiinstalujte knihovnu `asyncqt`:

```console
$ python -m pip install asyncqt
```

Nejde-li to, nevadí – nezbytné dnes PyQt nebude.

[lekce o PyQt]: {{ lesson_url('intro/pyqt') }}


Navíc si nainstalujte knihovnu `aiohttp`:

```console
$ python -m pip install aiohttp
```

{% if not var('coach-present') %}
---

> [note]
> V minulosti byly na této stránce popsány i [generátory](../../advanced/generators/).
> Neovládáte-li je ještě, přečtěte si o nich.
{% endif %}

---


AsyncIO
=======

Pojďme si povídat o souběžnosti – možnostech, jak nechat počítač dělat víc
úloh věcí najednou.

Jak jsme si řekli v [lekci o C API](../cython/), Python má globální zámek, takže pythonní kód
může běžet jen v jednom vlákně najednou.
Taky jsme si řekli, že to většinou příliš nevadí: typický síťový nebo GUI program
stráví hodně času čekáním na události (odpověď z internetu, kliknutí myší atp.)
a u tohoto čekání není potřeba držet zámek zamčený.

Servery typicky při zpracovávání požadavku stráví *většinu* času síťovou komunikací.
Proto se často spouští několik vláken nebo přímo procesů najednou, aby se mohl vytížit
procesor.
Při velkém množství vláken ale nastanou dva problémy.
První je, že vláken nemůže být neomezeně mnoho.
Každé vlákno potřebuje vlastní *stack*, tj. poměrně velkou část paměti; a počet vláken
bývá omezen i jinak (na Linuxu je globální limit počtu procesů, do kterého se počítají
i jednotlivá vlákna – viz `cat /proc/sys/kernel/threads-max`).
Druhý problém je, že přepnutí z jednoho vlákna do druhého se může stát *kdykoli*.
Ověřit si, že je na to program připravený, je poměrně složité a na zajištění
správné funkčnosti je potřeba zamykání či jiné techniky. Ty bývají relativně
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
napsané programy. V rámci jednoho procesu se to ale dá s úspěchem využít.


Souběžnost v Pythonu
--------------------

V Pythonu existovala a existuje řada knihoven, které nám umožňují „dělat více
věcí zároveň“.
Pro preemptivní multitasking jsou tu `threading`, tedy podpora pro vlákna,
a `multiprocessing`, tedy způsob jak spustit nový pythonní proces,
ve kterém se provede určitá funkce
(přičemž vstup a výstup se předává serializovaný přes *pipes*).

Další knihovna, kterou lze z PyPI nainstalovat, je [greenlet].
Ta nám dává k dispozici tzv. *mikro-vlákna*,
která se mezi sebou přepínají v rámci jednoho procesu.
Na rozdíl od systémových vláken nepotřebují tolik paměti navíc, ale
stále jde (alespoň z pohledu programátora) o *preemptivní* strategii:
k přepnutí může dojít kdykoli,
je tedy potřeba zamykat a složitě hledat málo časté chyby.

Byly vyvinuty i knihovny pro *kooperativní* přepínání, založené na tzv.
*futures*.
Nejznámější jsou [Twisted] a [Tornado].
Obě jsou relativně staré (2002, resp. 2009), ale stále populární.

Ačkoli byly Twisted, Tornado a podobné knihovny užitečné, měly zásadní problém
v tom, že každá má jiné API.
Vznikaly tak kolem nich ekosystémy vázané na konkrétní knihovnu:
server napsaný pro Tornado se nedal použít pod Twisted a aplikace
využívající Twisted nemohla využít knihovnu pro Tornado.

Jak to vyřešit?


Jeden standard
--------------

![xkcd 927](https://imgs.xkcd.com/comics/standards.png)

*Komiks [xkcd](https://xkcd.com/927/), © Randall Munroe, [CC-BY-NC](https://creativecommons.org/licenses/by-nc/2.5/)*

Podobně jako přístup k různým SQL databázím je v Pythonu standardizovaný
(knihovny pro SQLite, Postgres, MySQL atd. všechny podporují API definované
v [PEP 249]) nebo je standardizované API webových serverů (WSGI, [PEP 3333]),
tak vzniklo standardizované API pro kooperativní multitasking.
Toto API je definováno v [PEP 3156] a jeho referenční implementace, `asyncio`,
je ve standardní knihovně Pythonu.
(Ne že by to zabránilo vzniku dalších asynchronních knihoven jako
Curio a [Trio](https://trio.readthedocs.io/en/stable/tutorial.html).
Ty ovšem spíš experimentují s novými paradigmaty a osvědčené principy se z nich
postupně dostávají do `asyncio`.)

Interně je `asyncio` postavené na konceptu *futures* inspirovaných Tornado/Twisted,
ale jeho „hlavní“ API je postavené na *coroutines* podobných generátorům.

Od Pythonu verze 3.5 používá `asyncio` místo „normálních“ generátorů
speciální syntaxi, která umožňuje kombinovat asynchronní funkce s příkazy
`for` a `with` nebo i `yield`.
Tuto syntaxi použijeme i tady; máte-li starší Python, podívejte se na potřebné změny uvedené níže.

Jak vypadá taková asynchronní funkce?
Definuje se pomocí `async def` místo `def`, a může používat příkaz `await`.

Ukažme si to na příkladu:

```python
import asyncio

async def count(name, interval):
    """Prints numbers from 0 in regular intervals"""
    i = 0
    while True:
        print(name, 'counts', i)
        await asyncio.sleep(interval)
        i += 1


loop = asyncio.get_event_loop()
loop.run_until_complete(count('Counter', 1))
loop.close()
```

Co se tu děje?
Příkazem `await asyncio.sleep(interval)` se asynchronní funkce pozastaví
(podobně jako generátor při `yield`) a předá kontrolu knihovně `asyncio`
s informací že za daný čas by kontrolu chtěla zase zpátky.
Než daný interval uplyne, `asyncio` může spouštět jiné úlohy;
po jeho uplynutí pozastavenou funkci „probudí“ a její algoritmus pokračuje dál.

Když žádné jiné úlohy neexistují, je pomalé počítání trochu nudné.
Zkuste proto spustit počítadla dvě.
(Detaily funkce `ensure_future` a příkazu `await task` vysvětlíme níže.)

```python
import asyncio

async def count(name, interval):
    ...

async def run_two_counters():
    fast_task = asyncio.ensure_future(count('Fast', 0.3))
    slow_task = asyncio.ensure_future(count('Slow', 1))
    await fast_task
    await slow_task

loop = asyncio.get_event_loop()
loop.run_until_complete(run_two_counters())
loop.close()
```

Spouštění a ukončení – poslední tři řádky – je poněkud složité na zápis,
ale typicky to v každém programu potřebujete napsat jen jednou.

> [note]
> V Pythonu verze 3.7 a vyšší lze ty tři poslední řádky nahradit jednodušším:
>
> ```python
> asyncio.run(run_two_counters())
> ```

> [note]
> V Pythonu verze 3.4 a nižší ještě neexistovala klíčová slova `async` a
> `await`; asynchronní funkce byly implementovány jako generátory.
> Ve starších verzích Pythonu bylo potřeba místo:
>
> ```python
> async def ...:
>     await ...
> ```
>
> psát:
>
> ```python
> @asyncio.coroutine
> def ...:
>     yield from ...
> ```
>
> Starý způsob zatím funguje i v novějším Pythonu a dokonce se ještě někdy
> objeví i v dokumentaci.
> Od Pythonu 3.8 je ale *deprecated*.

[greenlet]: https://greenlet.readthedocs.io/en/latest/
[Tornado]: http://www.tornadoweb.org/en/stable/
[Twisted]: https://twistedmatrix.com/trac/
[PEP 249]: https://www.python.org/dev/peps/pep-0249/
[PEP 3333]: https://www.python.org/dev/peps/pep-3333/
[PEP 3156]: https://www.python.org/dev/peps/pep-3156/
[pypi-asyncio]: https://pypi.org/project/asyncio/


Event Loop
----------

Knihovna `asyncio` nám dává k dispozici *smyčku událostí*, která se, podobně jako
`app.exec` v Qt, stará o plánování jednotlivých úloh.
Smyček událostí může být více.
Tradiční způsob je, že každé vlákno může mít vlastní smyčku událostí,
kterou získáme pomocí `asyncio.get_event_loop` a pak ji můžeme spustit dvěma
způsoby:

* `loop.run_forever()` spustí smyčku na tak dlouho, dokud jsou nějaké úlohy
  naplánovány (to trochu odporuje názvu, ale většinou se nestává, že by se
  úlohy „vyčerpaly“), nebo
* `loop.run_until_complete(task)` – tahle funkce skončí hned, jakmile je hotová
  daná úloha, a vrátí její výsledek.

Nakonec je smyčku potřeba uzavřít (`loop.close()`), což např. dá použitým
knihovnám možnost korektně uzavřít zbylá síťová spojení.

Od Pythonu 3.7 můžete použít `asyncio.run(task)`, což vytvoří *novou*
smyčku událostí, spustí v ní danou úlohu (pomocí `run_until_complete`)
a zase ji zavře.
Chcete-li ji použít (a tedy psát kód jen pro Python 3.7+), používejte pak všude
místo `ensure_future` funkci `create_task`, která vás lépe ochrání před
těžko nalezitelnými chybami.


Async funkce a Task
-------------------

Smyčka událostí provádí úlohy a asynchronní funkce.

Asynchronní funkce se definují pomocí `async def` a umožňují použít příkaz
(nebo operátor) `await`, kterým se provádění funkce pozastaví a kontrola se
předá jiným úlohám do doby, než nastane nějaká událost (např. uplynul časový
intervaluj, jsou dostupná nová data ze socketu…).

Pozastavení funguje podobně jako `yield` u generátoru.

Zavoláním asynchronní funkce dostaneme *coroutine* pozastavenou na začátku
těla funkce:

```pycon
>>> async def demo():
...     print('Demo')
...
>>> coroutine = demo()
>>> coroutine
<coroutine object demo at 0x7fda8be22b90>
```

Naplánujeme-li provádění *coroutine* na smyčce událostí
(např. pomocí `run_until_complete`), tělo funkce se začne vykonávat:

```pycon
>>> loop = asyncio.get_event_loop()
>>> result = loop.run_until_complete(coroutine)
Demo
```

V rámci jedné *coroutine* pak lze provedení jiné *coroutine* naplánovat
a počkat na jejich skončení pomocí `await`.
Jak `run_until_complete` tak `await` nám dají k dispozici návratovou hodnotu
příslušné asynchronní funkce.

```python
import asyncio

async def add(a, b):
    await asyncio.sleep(1)  # schedule a "sleep" and wait for it to finish
    return a + b

async def demo():
    coroutine = add(2, 3)
    result = await coroutine  # schedule "add" and wait for it to finish
    print('The result is:', result)

loop = asyncio.get_event_loop()
result = loop.run_until_complete(demo())
loop.close()
```

Nevýhoda čistých *coroutines* spočívá v tom, že na každé zavolání
takové funkce lze použít jen jeden `await`.
Výsledek se nikam neukládá, jen se po skončení jednou předá.
Druhý `await` pro stejné zavolání asynchronní funkce skončí s chybou.
Zkuste si to – v kódu výše přidejte daší řádek s `await coroutine`:

```python
    print('The result is:', (await coroutine))
```

Tenhle problém můžeme vyřešit tak, že asynchronní funkci „zabalíme“
jako úlohu, *Task*.
V Pythonu 3.7 se Task tvoří pomocí `asyncio.create_task`;
pro kompatibilitu se staršími verzemi ale použijeme ekvivalentní
`asyncio.ensure_future`.
Task se chová stejně jako *coroutine* – lze použít v `await` nebo
`run_until_complete`, ale navíc:

* výsledek je k dispozici kdykoli po ukončení funkce (např. pro druhý `await`) a
* úloha se naplánuje hned po zavolání `ensure_future`.

Druhou vlastnost je lepší ukázat na příkladu:

```python
import asyncio

async def print_and_wait():
    print('Async function starting')
    await asyncio.sleep(0.5)
    print('Async function done')
    return 'result'

async def demo_coro():
    coroutine = print_and_wait()
    await asyncio.sleep(1)
    print('Awaiting coroutine')
    print(await coroutine)     # schedule coroutine and wait for it to finish

async def demo_task():
    task = asyncio.ensure_future(print_and_wait())  # schedule the task
    await asyncio.sleep(1)
    print('Awaiting task')
    print(await task)  # task is finished at this point; retreive its result


loop = asyncio.get_event_loop()
print('Coroutine:')
result = loop.run_until_complete(demo_coro())
print('Task:')
result = loop.run_until_complete(demo_task())
loop.close()
```

Fan-Out a Fan-In
----------------

S pomocí asynchronních funkcí můžeme nad našimi programy přemýšlet tak,
jako by to byly „normální“ procedurálně zapsané algoritmy: máme jedno
„vlákno“, které se provádí od začátku do konce, jen na některých místech
(označených `await`) se provádění přeruší a zatímco náš kód čeká na výsledek
nějaké operace, může se spustit jiný kus kódu.
Funkce, na které je takto potřeba čekat, bývají v dokumentaci patřičně
označeny (v síťovém programování je to většinou čtení ze socketů nebo inicializace
či ukončení serveru).

Pomocí `ensure_future` a `await` můžeme k tomu dělat něco navíc:
rozdělit běh našeho programu na víc úloh, které se budou vykonávat „souběžně“ –
například autor scraperu chce stáhnout několik stránek najednou
nebo server souběžně odpovídá na několik požadavků.
Tomuto rozdělení se říká *fan-out*.

Opačná operace je *fan-in*, kdy několik úloh opět spojíme do jedné.
Výše uvedený scraper může počkat, než jsou všechny stránky stažené –
třeba pomocí jednoho `await` pro každý *Task* nebo asynchronní funkce
[gather](https://docs.python.org/3/library/asyncio-task.html#asyncio.gather).
Poté může pokračovat zpracováním získaných dat.

Počkáním na úlohu (pomocí `await`, `gather`, `run_until_complete` atp.)
získáte její návratovou hodnotu.
Ale na všechny úlohy, i na ty, které nic zajímavého nevrací, je důležité počkat.
Neuděláte-li to, bude `asyncio` vypisovat varovné hlášky:

```pycon
>>> import asyncio
>>> asyncio.sleep(1)  # no await
>>> exit()
sys:1: RuntimeWarning: coroutine 'sleep' was never awaited
```

Toto varování nikdy neignorujte. Kdyby váš program nedělal co má, spolu s
varováním byste ignorovali výjimky v této *coroutine*.


Asynchronní cykly a kontexty
----------------------------

Až budete používat některé „asynchronní“ knihovny, setkáte se pravděpodobně se dvěma
novými konstrukcemi: `async for` a `async with`.

Fungují jako jejich „ne-`async`“ varianty, jen na začátku a konci každé iterace (resp.
na začátku a konci bloku) můžou přerušit vykonávání funkce – podobně jako `await`.

Typický příklad je u databází: začátek a konec transakce i získávání jednotlivých
řádků pravděpodobně potřebují komunikaci po síti, takže hypotetická databázová
knihovna by se mohla používat nějak takto:

```python
async with database.transaction_context():
    await database.execute('UPDATE ...')
    async for row in (await database.execute('SELECT ...')):
        handle(row)
```


A další
-------

Nakonec několik tipů, o kterých je dobré vědět.

V `asyncio` najdeme synchronizační mechanismy známé z vláknového programování, např.
`Lock` a `Semaphore` – viz [dokumentace](https://docs.python.org/3/library/asyncio-sync.html).

Musíme-li použít blokující funkci, která např. komunikuje po síti bez `await` a která by
tedy zablokovala i všechny ostatní úlohy, můžeme použít
`loop.run_in_executor()`, a tím danou funkci zavolat ve vlákně nebo podprocesu, ale výsledek zpřístupnit
jako objekt, na který lze počkat pomocí `await`.
Použití je opět popsáno v [dokumentaci](https://docs.python.org/3/library/asyncio-eventloop.html#executor).

Občas vás při programování s `asyncio` zaskočí zrádná chyba.
V takových případech je dobré zapnout *debug* režim pomocí proměnné prostředí `PYTHONASYNCIODEBUG=1`.
V tomto režimu `asyncio` upozorňuje na časté chyby, do některých chybových výpisů přidává informaci o tom,
kde aktuální `Task` vznikl, apod.
Více informací je zase v [dokumentaci](https://docs.python.org/3/library/asyncio-dev.html#asyncio-dev).


Alternativní smyčky událostí
----------------------------

Jak bylo zmíněno na začátku, hlavní cíl `asyncio` je definovat společné rozhraní
pro různé asynchronní knihovny, aby bylo možné např. kombinovat knihovny pro
Tornado se smyčkou událostí v Twisted.
Samotné `asyncio` je jen jedna z mnoha implementací tohoto rozhraní.
Zajímavá je například knihovna [uvloop], která je asi 2-4× rychlejší než `asyncio`
(ale má závislosti, které se pro součást standardní knihovny nehodí).

Další zajímavá implementace je [asyncqt], která pod standardním `asyncio` API používá
smyčku událostí z Qt.
Umožňuje tak efektivně zpracovávat Qt události zároveň s asynchronními funkcemi
známými z `asyncio`.

*Event loop* z `asyncqt` je potřeba na začátku programu naimportovat a nastavit
jako hlavní smyčku událostí, a poté ji, místo Qt-ovského `app.exec()`, spustit.
Jednotlivé asynchronní funkce se pak používají jako v čistém `asyncio`:
pomocí `asyncio.ensure_future`, `await`, atd.

[uvloop]: https://pypi.org/project/uvloop/
[asyncqt]: https://pypi.org/project/asyncqt/

Ukázka:

```python
import asyncio

from PyQt5 import QtGui, QtWidgets
from asyncqt import QEventLoop

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


Komunikace
----------

Ono `io` v `asyncio` naznačuje, že je tato knihovna dělaná především na
vstup a výstup – konkrétně na komunikaci přes síť (případně s jinými procesy).

Ke komunikaci používá `asyncio` tři úrovně abstrakce: `Transport`, `Protocol`
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
`HTTP`, `FTP` a podobně.
V dokumentaci najdete podrobnější popis včetně [příkladů][transport-proto-examples].

[transport-proto-examples]: https://docs.python.org/3/library/asyncio-protocol.html#tcp-echo-server-protocol

Kromě toho existuje i „Stream API“ založené na asynchronních funkcích.
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
