Testování
=========

V tomto cvičení se budeme zabývat automatickým testováním kódu.
Modul unittest ze standardní knihovny už byste měli znát,
co to jsou jednotkové testy a k čemu slouží tedy rovnou přeskočím.

> [note]
> Pokud základy testování neznáte, projděte si
> [začátečnickou lekci o testování]({{ lesson_url('beginners/testing') }}).
> Obsah se zčásti překrývá, ale základní principy jsou tam vysvětleny trošku
> podrobněji.

Pokud si chcete přečíst krátký text o tom, jak testovat, zkuste [blogový
zápisek Michala Hořejška](http://blog.horejsek.com/matka-moudrosti-jak-testovat).

pytest
------

Rovnou se podíváme na velmi oblíbený balíček [pytest], který oproti standardnímu
unittestu přináší mnoho výhod. Začneme jednoduchou ukázkou z modulu `isholiday`
z [cvičení o modulech]({{ lesson_url('intro/distribution') }}).

```python
import isholiday

def test_xmas_2016():
    """Test whether there is Christmas in 2016"""
    holidays = isholiday.getholidays(2016)
    assert (24, 12) in holidays
```

Test uložíme někam do projektu, třeba do souboru `tests/test_holidays.py` a
nainstalujeme a spustíme `pytest`:

```console
(__venv__) $ python -m pip install pytest
(__venv__) $ python -m pytest tests/test_holidays.py
```

```pytest
============================= test session starts ==============================
platform linux -- Python 3.7.1, pytest-4.0.1, py-1.7.0, pluggy-0.8.0
rootdir: /tmp/tmp.etepchwQWh, inifile:
collected 1 item

tests/test_holidays.py .                                                 [100%]

=========================== 1 passed in 0.01 seconds ===========================
```

Všimněte si několika věcí:

 * V testovacím souboru stačí mít funkci pojmenovanou `test_*` a `pytest` pozná,
   že se jedná o test.
 * V ukázce je použit obyčejný `assert`, nikoliv metoda z `unittest`.

Co se má testovat, se pytestu dá zadat pomocí argumentů příkazové řádky.
Můžou to být jednotlivé soubory nebo adresáře, ve kterých pytest
rekurzivně hledá všechny soubory začínající na `test_`.
Vynecháme-li argumenty úplně, hledá rekurzivně v aktuálním adresáři.
(To se často hodí, ale obsahuje-li aktuální adresář i vaše virtuální prostředí,
pytest prohledá i to a často v něm najde neprocházející testy.)

> [note]
> Pokud pytest nemůže naimportovat váš modul, můžete udělat několik věcí:
> 
>  * Nainstalovat svůj balíček (například v režimu `develop`).
>  * Nastavit proměnnou prostředí `PYTHONPATH` na `.`.
> 
> Testovat nainstalovaný balíček je výhodnější – ověříte zároveň, že
> nainstalovaný modul se chová dle očekávání. Je dobré testy psát tak, aby
> šly spouštět z jakéhokoliv adresáře, a pro jistotu je spouštět odjinud,
> než z adresáře s kódem. Odhalíte tím často balíčkovací chyby.

Pytest upravuje chování assertu, což oceníte především, pokud test selže:

```python
    ...
    assert (23, 12) in holidays
```

```console
(__venv__) $ python -m pytest tests/test_holidays.py
```

```pytest
============================= test session starts ==============================
platform linux -- Python 3.7.1, pytest-4.0.1, py-1.7.0, pluggy-0.8.0
rootdir: /tmp/tmp.etepchwQWh, inifile:
collected 1 item

tests/test_holidays.py F                                                 [100%]

=================================== FAILURES ===================================
________________________________ test_xmas_2016 ________________________________

    def test_xmas_2016():
        """Test whether there is Christmas in 2016"""
        holidays = isholiday.getholidays(2016)
>       assert (23, 12) in holidays
E       assert (23, 12) in {(1, 1), (1, 5), (5, 7), (6, 7), (8, 5), (17, 11), ...}

tests/test_holidays.py:6: AssertionError
=========================== 1 failed in 0.02 seconds ===========================
```

S obyčejným assertem si vystačíte pro většinu testovaných případů kromě
ověření vyhození výjimky. To se dělá takto:

```python
import pytest

def f():
    raise SystemExit(1)

def test_mytest():
    with pytest.raises(SystemExit):
        f()
```

Více o základním použití pytestu najdete v [dokumentaci].

[pytest]: http://pytest.org/
[dokumentaci]: http://docs.pytest.org/en/latest/getting-started.html

### Parametrické testy

Jednou z vlastností pytestu, která často přichází vhod, jsou [parametrické testy].
Pokud bychom například chtěli otestovat, jestli je Štědrý den svátkem nejen
v roce 2016, ale v jiných letech, nemusíme psát testů více, ani použít cyklus.

Nevýhoda více téměř stejných testů je patrná sama o sobě, nevýhoda cyklu je
v tom, že celý test selže, i pokud selže jen jeden průběh cyklem. Zároveň se
průběh testu při selhání ukončí.

Místo toho tedy použijeme parametrický test:

```python
import pytest
import isholiday

@pytest.mark.parametrize('year', (2015, 2016, 2017, 2033, 2048))
def test_xmas(year):
    """Test whether there is Christmas"""
    holidays = isholiday.getholidays(year)
    assert (24, 12) in holidays

```

Zápis je určitým způsobem podobný knihovně [click](../click/): funkce
s testem přijímá parametr vytvořený v dekorátoru.
Test se spustí pro každou uvedenou hodnotu, k jejich definici lze použít
jakýkoliv objekt, přes který jde iterovat, tedy kromě v ukázce použité
<var>n</var>-tice např. seznam, množinu, `range`, vlastní generátor...

Pro podrobnější výpis výsledku testů můžete použít přepínač `-v`:

```console
(__venv__) $ python -m pytest -v
```

```pytest
============================= test session starts ==============================
platform linux -- Python 3.7.1, pytest-4.0.1, py-1.7.0, pluggy-0.8.0 -- /tmp/tmp.etepchwQWh/__venv__/bin/python
cachedir: .pytest_cache
rootdir: /tmp/tmp.etepchwQWh, inifile:
collecting ... collected 5 items

tests/test_holidays.py::test_xmas[2015] PASSED                           [ 20%]
tests/test_holidays.py::test_xmas[2016] PASSED                           [ 40%]
tests/test_holidays.py::test_xmas[2017] PASSED                           [ 60%]
tests/test_holidays.py::test_xmas[2033] PASSED                           [ 80%]
tests/test_holidays.py::test_xmas[2048] PASSED                           [100%]

=========================== 5 passed in 0.02 seconds ===========================
```

Jednoduchým způsobem tak lze vyrobit z jednoho testu testů více.
Výhodou je, že každý se testuje zvlášť, což má vliv na čitelnost
výstupu, pokud nějaký test selže, a umožňuje to například testy pouštět
paralelně nebo distribuovaně. (Což s jedním testem, který více podmínek ověřuje
v cyklu, nejde, tedy alespoň ne jednoduše.)

Potřebujeme-li parametrizovat více argumentů, můžeme předat seznam jmen
argumentů a seznam jejich hodnot:

```python
import pytest
import isholiday

@pytest.mark.parametrize(
    ['year', 'month', 'day'],
    [(2015, 12, 24),
     (2016, 12, 24),
     (2017, 1, 1),
     (2033, 7, 5),
     (2048, 7, 6)],
)
def test_some_holidays(year, month, day):
    """Test a few sample holidays"""
    holidays = isholiday.getholidays(year)
    assert (day, month) in holidays
```

Vždy je dobré pokusit se nějaký test rozbít v samotném kódu, který testujeme,
abychom se ujistili, že testujeme správně.
Přidáme tedy dočasně na konec funkce `getholidays()` tento pesimistický kus kódu:

```python
    if year > 2020:
        # After the Zygon war, the puppet government canceled all holidays
        holidays = set()
```

```pytest
============================= test session starts ==============================
platform linux -- Python 3.7.1, pytest-4.0.1, py-1.7.0, pluggy-0.8.0 -- /tmp/tmp.etepchwQWh/__venv__/bin/python
cachedir: .pytest_cache
rootdir: /tmp/tmp.etepchwQWh, inifile:
collecting ... collected 5 items

tests/test_holidays.py::test_xmas[2015] PASSED                           [ 20%]
tests/test_holidays.py::test_xmas[2016] PASSED                           [ 40%]
tests/test_holidays.py::test_xmas[2017] PASSED                           [ 60%]
tests/test_holidays.py::test_xmas[2033] FAILED                           [ 80%]
tests/test_holidays.py::test_xmas[2048] FAILED                           [100%]

=================================== FAILURES ===================================
_______________________________ test_xmas[2033] ________________________________

year = 2033

    @pytest.mark.parametrize('year', (2015, 2016, 2017, 2033, 2048))
    def test_xmas(year):
        """Test whether there is Christmas"""
        holidays = isholiday.getholidays(year)
>       assert (24, 12) in holidays
E       assert (24, 12) in set()

tests/test_holidays.py:8: AssertionError
_______________________________ test_xmas[2048] ________________________________

year = 2048

    @pytest.mark.parametrize('year', (2015, 2016, 2017, 2033, 2048))
    def test_xmas(year):
        """Test whether there is Christmas"""
        holidays = isholiday.getholidays(year)
>       assert (24, 12) in holidays
E       assert (24, 12) in set()

tests/test_holidays.py:8: AssertionError
====================== 2 failed, 3 passed in 0.03 seconds ======================
```


[parametrické testy]: http://doc.pytest.org/en/latest/parametrize.html

### Fixtures

Často se stává, že před samotným testem potřebujte spustit nějaký kus kódu,
abyste získali to, co teprve chcete testovat. Příkladem může být například
inicializace objektu pro komunikaci s nějakým API.

V pytestu k tomuto účelu nejlépe slouží tz. [fixtures], které se v samotných
testech používají jako argumenty funkcí.


[fixtures]: http://doc.pytest.org/en/latest/fixture.html

```python
import pytest

@pytest.fixture
def client():
    import twitter
    return twitter.Client(...)

def test_search_python(client):
    tweets = client.search('python', size=1)
    assert len(tweets) == 1
    assert 'python' in tweets[0].text.lower()
```

Fixtures se hledají pomocí jména: když má testovací funkce (nebo i jiná
fixture) parametr, podle jména tohoto parametru se najde odpovídající fixture.
Fixtures můžou být definovány v aktuálním souboru,
v [pluginu](http://doc.pytest.org/en/latest/plugins.html),
[konfiguračním souboru](http://doc.pytest.org/en/latest/writing_plugins.html#conftest-py-local-per-directory-plugins)
a některé jsou zabudované přímo v pytestu.

Pokud potřebujete po použití s fixturou ještě něco udělat, můžete místo `return`
použít `yield`.
Často se to používá u zdrojů, které je po použití potřeba nějak finalizovat či
zavřít, například u databázových spojení.
Zde je ilustrační příklad, který si můžete rovnou vyzkoušet:

```python
import pytest


class DBConnection:
    def __init__(self, name):
        print('Creating connection for ' + name)
        ...

    def select(self, arg):
        return arg

    def cleanup(self):
        print('Cleaning up connection')
        ...


@pytest.fixture
def connection():
    d = DBConnection('sqlite')
    yield d
    d.cleanup()


@pytest.mark.parametrize('arg', (1, float, None))
def test_with_fixture(connection, arg):
    assert arg == connection.select(arg)
```

Standardní výstup (`stderr` a `stdout`) z testů se normálně zobrazuje,
jen když test selže.
Chceme-li výstup vidět u všech testů, je třeba použít přepínač `-s`.

I fixtury jdou parametrizovat, jen trochu jiným způsobem než testovací funkce:
parametry předané dekorátoru `pytest.fixture` získáme ze speciálního parametru
`request`, který obsahuje informace o probíhajícím testu:

```python
@pytest.fixture(params=('sqlite', 'postgres'))
def connection(request):
    d = DBConnection(request.param)
    yield d
    d.cleanup()
```

Hromadu dalších příkladů použití pytestu najdete dokumentaci v
[sekci s příklady](http://doc.pytest.org/en/latest/example/index.html).
Hledáte-li příklady krok za krokem, zkuste [příspěvek ze sborníku konference
PyCon PL](https://github.com/PyConPL/Book/blob/master/2017/workshops/pytest_parametric_tests/text.md).

„Podvádění“
-----------

Při psaní testů se občas hodí trochu podvádět. Například když nechceme,
aby testy měly nějaký vedlejší účinek, když chceme testovat něco, co závisí na
náhodě a podobně. Obecně se tomuto říká *mocking* \* či *test doubles* a existuje více různých
knihoven, které to umožňují. Jednou z nich je [flexmock].

[flexmock]: https://flexmock.readthedocs.io/

\* *mocking* je jen jeden druh podvádění, ale obecně se dá tento název použít
pro funkcionalitu knihoven, které mají v názvu *mock* :)

### Falešné objekty (fakes)

Při testování často potřebujeme nějaký objekt, který má určité atributy a
metody. Vytvářet si pro každý takový objekt třídu může být ubíjející:

```python
class FakePlane:
    operational = True
    model = 'MIG-21'
    def fly(self): pass

plane = FakePlane()  # this is tedious!
```
Flexmock umožňuje vytvoření objektu rychle a jednoduše:

```python
plane = flexmock(operational=True,
                 model='MIG-21',
                 fly=lambda: None)
```

### Částečně upravené objekty, třídy, moduly (stubs)

Stejně tak můžete vzít i nějaký existující objekt nebo třídu a upravit jen část
atributů nebo metod:

```python
>>> import flexmock
>>> class Train:
...     def get_speed(self):
...         return 0
... 
>>> flexmock(Train, get_speed=200)
<flexmock.Mock object at 0x7f88501d8908>
>>> train = Train()
>>> train.get_speed()
200
```

Můžete tak zfalšovat i volání *builtin* funkcí, jako je například `open()`:

```python
>>> import sys
>>> import flexmock
>>> import builtins
>>> from io import StringIO
>>> flexmock(builtins, open=StringIO('fake content'))
<module 'builtins' (built-in)>
>>> with open('/etc/passwd') as f:
...     f.readlines()
... 
['fake content']
```

### Očekávání (mocks, spies)

Pomocí flexmocku můžete zároveň [kontrolovat], že se vaší implementaci něco
zavolalo, a to dvojím způsobem: buďto zároveň změníte výsledek funkce (mocks),
nebo jen sledujete, jestli se zavolala (spies).
(Příklady na odkazu.)

[kontrolovat]: http://flexmock.readthedocs.io/en/latest/start/#creating-and-checking-expectations

### Integrace s pytestem

Dobrá mockovací knihovna se stará o to, aby platnost vašich změn byla omezená
kontextem jedné funkce a tedy jednoho testu. Implementovat vlastní *test double*
ale není nic těžkého a můžete to udělat sami (bez knihovny).
Pro přepsání nějaké metody, funkce apod. na omezenou dobu
můžete využít zabudovanou pytest fixturu
[monkeypatch](https://docs.pytest.org/en/latest/monkeypatch.html).

### Varování

Podvádění při testech občas vypadá nevyhnutelně. Pokud například vaše funkce
čte soubor `/etc/passwd` a vy chcete testovat, že se zachová správně, pokud
bude obsahovat daný obsah, musíte si trochu zapodvádět, protože nemůžete vědět,
co v tom souboru je doopravdy na daném systému, v daný čas.

Je ale jednoduché sklouznout do fáze, kdy jsou vaše testy natolik přemockované,
že už ani neplní svůj účel. Buďto proto, že příliš podvádíte a testy vždy
projdou, i když je implementace rozbitá; nebo proto, že při sebemenší úpravě
vnitřní implementace musíte vždy upravit i testy.

Mějte toto na paměti a k mockování se uchylujte až po vyčerpání „slušnějších”
možností.
Často jde trochu změnit kód, aby byl testovatelnější – například napsat funkci,
která čte soubor formátu `/etc/passwd`, ale jméno souboru jí předat argumentem.

> [note]
> Mohl by vás zajímat záznam z přednášky [Should I mock or should I not?]
> z konference [PyCon CZ] 2017. V přednášce se věnuji různým způsobům podvádění
> při psaní testů.

[PyCon CZ]: https://cz.pycon.org/
[Should I mock or should I not?]: https://www.youtube.com/watch?v=-nJ-ZW_LP7s

Testování HTTP komunikace: betamax
----------------------------------

Vaše programy často používají webová API. Při testování funkcionality API klientů
se vynoří řada problémů:

 * výsledky volání API mohou být pokaždé různé,
 * k některým volání API je potřeba mít přístupové údaje,
 * API může být zrovna nedostupné.

V zásadě můžete omockovat knihovnu requests tak, aby
jednotlivá volání jako `get()` apod. vracela předem definovanou odpověď.
Při ponoření do hloubky ale zjistíte, že komplexita takového mockování může
velmi přesáhnout komplexitu samotného kódu, který testujete.
Jednodušší je tak použít již hotové řešení. Jedno z nich je [betamax].

[betamax]: https://betamax.readthedocs.io/

Betamax umožňuje nahrát HTTP komunikaci do kazet (souborů), které se potom
použijí při testech. V zásadě to funguje takto:

 * Pokud daný HTTP požadavek ještě neproběhl, provede se a nahraje na kazetu.
 * Pokud již proběhl, použije se daná kazeta pro simulaci.

Betamax funguje pouze s knihovnou [requests](../requests/) při použití session.

V kombinaci s pytestem můžete použít předpřipravenou fixture:

```python
import betamax

with betamax.Betamax.configure() as config:
    # tell Betamax where to find the cassettes
    # make sure to create the directory
    config.cassette_library_dir = 'tests/fixtures/cassettes'

def test_get(betamax_session):
    betamax_session.get('https://httpbin.org/get')
```

Před spuštěním testu vytvořte složku `tests/fixtures/cassettes`.
Po spuštění testu ji prozkoumejte.
Měla by obsahovat soubor `test_filename.test_get.json`.
To je nahraná kazeta. Každý další průběh testu nevykoná GET požadavek,
ale pouze přehraje danou kazetu. Pokud chcete kazetu opět nahrát, prostě ji
smažte a pusťte test znovu.

Celé to ale funguje pouze, pokud kód vykonávaný uvnitř testu použije speciální
session, kterou máme od betamaxu. Jak to udělat?

Je třeba, aby implementační část kódu uměla session přejmout, například takto:

```python
class Client:
    def __init__(self, session=None):
        self.session = session or requests.Session()
        ...

def test_clent_foo(betamax_session):
    client = Client(session=betamax_session)
    assert client.foo() == 42
```

Pokud budete používat parametrizované testy, použijte
`betamax_parametrized_session`, aby kazety měly odlišné jméno při odlišných
parametrech.

> [note]
> Pro tip: Abyste nevytvářeli novou instanci třídy ve všech testech, můžete si
> vytvořit vlastní fixture, která použije fixture `betamax_session`:
> 
> ```python
> @pytest.fixture
> def client(betamax_session):
>     return Client(session=betamax_session)
> ```

### Citlivé údaje

Při práci s webovými API často létají vzduchem citlivé údaje jako tokeny apod.

Vyvstávají dvě otázky:

 1. Jak umožnit spuštění testů bez vlastního tokenu?
 2. Jak citlivé údaje skrýt v kazetách a nedávat je do gitu?

Na obě otázky se pokusím odpovědět jedním okomentovaným kódem:

```python
with betamax.Betamax.configure() as config:
    if 'AUTH_FILE' in os.environ:
        # If the tests are invoked with an AUTH_FILE environ variable
        TOKEN = my_auth_parsing_func(os.environ['AUTH_FILE'])
        # Always re-record the cassetes
        # https://betamax.readthedocs.io/en/latest/record_modes.html
        config.default_cassette_options['record_mode'] = 'all'
    else:
        TOKEN = 'false_token'
        # Do not attempt to record sessions with bad fake token
        config.default_cassette_options['record_mode'] = 'none'

    # Hide the token in the cassettes
    config.define_cassette_placeholder('<TOKEN>', TOKEN)
    ...

@pytest.fixture
def client(betamax_session):
    return Client(token=TOKEN, session=betamax_session)
```

Co když ale nevíme, jak bude vypadat citlivá část požadavku, protože se teprve
někde spočítá a získá, jako například v případě Twitter API?
Na tuto otázku podrobněji odpovídá
[dokumentace](https://betamax.readthedocs.io/en/latest/configuring.html#filtering-sensitive-data).

V každém případě je moudré před uložením do gitu zkontrolovat, že se v kazetách
nenachází žádný citlivý údaj, a pokud tam je, přepsat kód tak, aby se tam nenacházel.

#### Komprimované citlivé údaje

Problém může nastat, pokud je token či jiná citlivá informace uložena jako část v těle 
odpovědi (případně i požadavku) a zároveň je toto tělo zprávy zkomprimováno (defaultní
chování, viz [dokumentace](http://betamax.readthedocs.io/en/latest/implementation_details.html#gzip-content-encoding)). 
V takovém případě je potřeba k tomu, aby šlo v kazetě nahradit citlivé údaje, upravit 
hlavičku `Accept-Encoding` v `betamax_session` tak, aby neobsahovala `*`, `gzip`, 
`compress` ani `deflate`:

```
betamax_session.headers.update({'Accept-Encoding': 'identity'})
```

> [note]
> Kódování `'identity'` má shodné chování jako `''` a to, že data ve zprávě nejsou 
> nijak transformována, více viz [Wikipedia](https://en.wikipedia.org/wiki/HTTP_compression#Content-Encoding_tokens) 
> a [specifikace HTTP](https://www.w3.org/Protocols/rfc2616/rfc2616-sec14.html#sec14.3))

### Které HTTP požadavky jsou stejné?

Podle čeho se vyhodnotí, že HTTP požadavek odpovídá nahrané interakci a má se
pouze přehrát? Ve výchozím stavu podle HTTP metody a URL.
Pokud tedy na jedno URL provedete dva POST požadavky s jiným tělem, betamax
je bude považovat za stejné. Toto chování lze měnit zapnutím (nebo vypnutím)
různých *matcherů*. Těch je v betamaxu celá řada a je jednoduché napsat si
vlastní. Více informací najdete
v [dokumentaci](http://betamax.readthedocs.io/en/latest/matchers.html).

> [note]
> Mohl by vás zajímat záznam z přednášky [If it Moves, Test it Anyway]
> z konference [PyCon CZ] 2016. V přednášce se věnuji různým způsobům, jak
> testovat webové API klienty v Pythonu.

[If it Moves, Test it Anyway]: https://www.youtube.com/watch?v=iFqF5IaWfy0

Testování aplikací ve Flasku
----------------------------

Pro testování aplikací ve Flasku se
[používá](http://flask.pocoo.org/docs/1.0/testing/) `app.test_client()`:

```python
import pytest

@pytest.fixture
def testapp():
    from hello import app
    app.config['TESTING'] = True
    return app.test_client()

def test_hello(testapp):
    assert 'Hello' in testapp.get('/').get_data(as_text=True)
```

Pozor, metody na testovacím klientu vrací [Response], ale trochu jinou, než tu
z requests.
Proto nelze použít přímo `response.text`; text dostaneme pomocí
`response.get_data(as_text=True)`.

[Response]: http://flask.pocoo.org/docs/1.0/api/#flask.Response


Testování aplikací v clicku
---------------------------

Podobně funguje [testování aplikací v clicku](http://click.pocoo.org/6/testing/).
Click obsahuje třídu `CliRunner`, která pomáhá s testováním:

```python
from click.testing import CliRunner

def test_push_force():
    runner = CliRunner()
    result = runner.invoke(git_cli_made_in_click, ['push', '--force'])
    assert result.exit_code == 0
    assert 'forced update' in result.output
```


Kam dát testy?
--------------

[Dokumentace pytestu](http://doc.pytest.org/en/latest/goodpractices.html#choosing-a-test-layout-import-rules)
uvádí dvě možnosti, kam dát adresář s testy. Buď vedle adresáře s modulem:

```
setup.py
mypkg/
    __init__.py
    appmodule.py
tests/
    test_app.py
    ...
```

nebo do něj:

```
setup.py
mypkg/
    __init__.py
    appmodule.py
    ...
    test/
        test_app.py
        ...
```

První způsob je preferovaný, protože pomáhá udržovat kód a testy oddělené.
Pokud ho použijete, nedávejte do něj `__init__.py` – není to importovatelný
Pythonní modul, ale jen sada souborů s testy.

Ve druhém případě mějte na paměti, že pytest pouští testy jako samostatné
moduly, ne jako součást vašeho balíčku.
Relativní importy (`from ..appmodule import xyz`) v testech nebudou fungovat.

Pozor na to, aby testy byly součástí archivu s balíčkem (`setup.py sdist`), ale
pokud zvolíte první variantu umístění, aby se neinstalovaly (`setup.py install`),
protože by tam kolidovaly s ostatními testy z jiných balíčků.

Případné soubory potřebné k testování bývá zvykem dávat do složky `fixtures` ve
složce s testy.

Spouštění testů pomocí `setup.py test`
--------------------------------------

Standardně se testy v Pythonu nespouští pomocí `python -m pytest`, ale
`python setup.py test`, což funguje i s jinými nástroji než je pytest.
Pokud pytest používáme, je proto dobré `setup.py` naučit spouštět pytest.

K tomu potřebujeme nakonfigurovat závislosti: v `setup_requires` musí být
`pytest-runner` a v `tests_require` pak `pytest` a další testovací závislosti
(`flexmock`, `betamax`...).

```python
from setuptools import setup

setup(
    ...,
    setup_requires=['pytest-runner', ...],
    tests_require=['pytest', ...],
    ...,
)
```

a přidat následující sekci do `setup.cfg`:

```
[aliases]
test=pytest
```

Příkaz `python setup.py test` by měl fungovat, ale neočekává se, že bude
podporovat další argumenty pytestu (jako `-v`).
Na to uživatel spustí pytest samotný.

Další informace jsou v [dokumentaci pytestu](http://doc.pytest.org/en/latest/goodpractices.html#integrating-with-setuptools-python-setup-py-test-pytest-runner).

Travis CI
---------

Vaše testy nemusí běžet jen u vás na počítači, ale můžete je pouštět automaticky
na službě Travis CI při každém pushnutí na GitHub.

Travis CI je zadarmo pro veřejné repozitáře na [travis-ci.org], pro soukromé
repozitáře je placená verze na [travis-ci.com]. V rámci studentského balíčku
můžete i tuto verzi využít zdarma.

Přihlaste se na [travis-ci.com] pomocí GitHubu (vpravo nahoře).
Pak opět vpravo nahoře zvolte [Accounts](https://travis-ci.com/profile)
a povolte Travis pro váš repozitář.

Do repozitáře přidejte soubor `.travis.yml`:

```yaml
language: python
python:
- '3.6'
install:
- python setup.py install
script:
- python setup.py test
```

Uvedený příklad je pro Python 3.6.
Pro Python 3.7 je třeba nastavit novější verzi Ubuntu:

```yaml
language: python
python:
- '3.7'
dist: xenial
install:
- python setup.py install
script:
- python setup.py test
```

Verze Pythonu lze kombinovat:

```yaml
language: python
python:
- '3.6'
- '3.7'
dist: xenial
install:
- python setup.py install
script:
- python setup.py test
```

Po pushnutí by se na Travisu měl automaticky spustit test.
Více informací o použití pro Python najdete
v [dokumentaci](https://docs.travis-ci.com/user/languages/python/).

[travis-ci.org]: https://travis-ci.org/
[travis-ci.com]: https://travis-ci.com/

Kvíz
----

Co je špatně na této testovací sadě k funkci `is_even()`?

```python
def is_even(n):
    return n % 2 == 0


@pytest.mark.parametrize('n', range(0, 1000, 2))
def test_is_even(n):
    assert is_even(n)
```
