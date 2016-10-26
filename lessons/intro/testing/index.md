Testování
=========

V tomto cvičení se budeme zabývat automatickým testováním kódu.
Modul unittest ze standardní knihovny už byste měli znát,
co to jsou jednotkové testy a k čemu slouží tedy rovnou přeskočím.

Pokud si chcete přečíst krátký text o tom, jak testovat, zkuste [blogový
zápisek Michala Hořejška](http://blog.horejsek.com/matka-moudrosti-jak-testovat).

pytest
------

Rovnou se podíváme na velmi oblíbený balíček [pytest], který oproti standardnímu
unittestu přináší mnoho výhod. Začneme jednoduchou ukázkou z modulu `isholiday`
z [předchozího cvičení](03_moduly.md).

```python
import isholiday

def test_xmas_2016():
    """Test whether there is Christmas in 2016"""
    holidays = isholiday.getholidays(2016)
    assert (24, 12) in holidays
```

Test uložíme někam do projektu, třeba do souboru `test/test_holidays.py` a
nainstalujeme a spustíme `pytest`:

```bash
(env)$ python -m pip install pytest
(env)$ PYTHONPATH=. python -m pytest test/test_holidays.py
=============================== test session starts ================================
platform linux -- Python 3.5.2, pytest-3.0.3, py-1.4.31, pluggy-0.4.0
rootdir: ..isholiday, inifile: 
collected 1 items 

test/test_holidays.py .

============================= 1 passed in 0.24 seconds =============================
```

Všimněte si několika věcí:

 * V testovacím souboru stačí mít funkci pojmenovanou `test_*` a `pytest` pozná,
   že se jedná o test.
 * Pokud balíček nemáme nainstalovaný, je třeba nastavit `PYTHONPATH`. Vždy je ale lepší testovat nainstalovaný balíček.
 * V ukázce je použit obyčejný `assert` a žádná metoda z `unittest`.

Co se má testovat se pytestu dá zadat argumenty příkazové řádky.
Buď to můžou být jednotlivé soubory, nebo adresáře, ve kterých pytest
rekurzivně hledá všechny soubory začínající na `test_`.
Vynecháme-li argumenty úplně, projdou se testy z aktuálního adresáře.
(To se často hodí, ale obsahuje-li aktuální adresář i vaše virtuální prostředí,
pytest prohledá i to a často v něm najde neprocházející testy.)

Pytest upravuje chování assertu, což oceníte především, pokud test selže:

```python
    ...
    assert (23, 12) in holidays
```

```
===================================== FAILURES =====================================
__________________________________ test_xmas_2016 __________________________________

    def test_xmas_2016():
        """Test whether there is Christmas in 2016"""
        holidays = isholiday.getholidays(2016)
>       assert (23, 12) in holidays
E       assert (23, 12) in {(1, 1), (1, 5), (5, 7), (6, 7), (8, 5), (17, 11), ...}

test/test_holidays.py:6: AssertionError
============================= 1 failed in 0.24 seconds =============================
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
Pokud bychom například chtěli otestovat, jestli je štědrý den svátkem nejen
v roce 2016, ale v jiných letech, nemusíme spát testů více ani použít cyklus.

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

(Místo výpisu hodnot v `tuple` lze použít jakýkoliv objekt, přes který jde
iterovat, tedy i např. volání `range()`.)

Pro více podrobný výpis výsledku testů můžete použít přepínač `-v`:

```bash
(env)$ PYTHONPATH=. python -m pytest -v
...
test/test_holidays.py::test_xmas[2015] PASSED
test/test_holidays.py::test_xmas[2016] PASSED
test/test_holidays.py::test_xmas[2017] PASSED
test/test_holidays.py::test_xmas[2033] PASSED
test/test_holidays.py::test_xmas[2048] PASSED
...
```

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
Přidám tedy dočasně na konec funkce `getholidays()` tento pesimistický kus kódu:

```python
    if year > 2020:
        # After the Zygon war, the puppet government canceled all holidays
        holidays = set()
```

```bash
(env)$ PYTHONPATH=. python -m pytest -v
...
test/test_holidays.py::test_xmas[2015] PASSED
test/test_holidays.py::test_xmas[2016] PASSED
test/test_holidays.py::test_xmas[2017] PASSED
test/test_holidays.py::test_xmas[2033] FAILED
test/test_holidays.py::test_xmas[2048] FAILED
...
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
[konfiguračním souboru](http://doc.pytest.org/en/latest/writing_plugins.html#conftest-py-local-per-directory-plugins),
a některé jsou zabudované přímo v pytestu.

Pokud potřebujete po použití s fixturou ještě něco udělat, můžete místo `return`
použít `yield`. Zde příklad, který si můžete rovnou vyzkoušet:

```python
import pytest


class Dummy:
    def __init__(self):
        print('Creating Dummy instance')
        ...

    def forward(self, arg):
        return arg

    def cleanup(self):
        print('Cleaning up Dummy instance')
        ...


@pytest.fixture
def dummy():
    d = Dummy()
    yield d
    d.cleanup()


@pytest.mark.parametrize('arg', (1, float, None))
def test_with_fixture(dummy, arg):
    assert arg == dummy.forward(arg)
```

Standardní výstup z testů se normálně zobrazuje jen když test selže.
Chceme-li výstup vidět u všech testů, je třeba použít `pytest -s`.

Hromadu dalších příkladů použití pytestu najdete dokumentaci, v
[sekci s příklady](http://doc.pytest.org/en/latest/example/index.html).

flexmock
--------

Při psaní testů se občas hodí trochu podvádět. Například když nechceme,
aby testy měli nějaký vedlejší účinek, když chceme testovat něco, co závisí na
náhodě a podobně. Obecně se tomuto říká *mocking* \*, a existuje více různých
knihoven, které to umožňují. Jednou z nich je [flexmock].

[flexmock]: https://flexmock.readthedocs.io/

\* *mocking* je jen jeden druh podvádění, ale obecně se dá tento název použít
pro funkcionalitu knihoven, které mají v názvu *mock* :)

### Falešné objekty (fakes)

Při testování často potřebujeme nějaký objekt, který má určité atributy a
metody. Vytvářet si pro každý takový objekt třídu (jako v příkladě výše)
může být ubíjející.

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
>>> from io import StringIO
>>> flexmock(sys.modules['builtins'], open=StringIO('fake content'))
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

### Varování

Podvádění při testech občas vypadá nevyhnutelně. Pokud například vaše funkce
čte soubor `/etc/passwd` a vy chcete testovat, že se zachová správně, pokud
bude obsahovat daný obsah, musíte si trochu zapodvádět, protože nemůžete vědět,
co v tom souboru je doopravdy na daném systému, v daný čas.

Je ale jednoduché sklouznout do fáze, kdy jsou vaše testy natolik přemockované,
že už ani neplní svůj účel. Buďto proto, že příliš podvádíte a testy vždy
projdou, i když je implementace rozbitá; nebo proto, že při sebemenší úpravě
vnitřní implementace musíte vždy upravit i testy.

Mějte toto na paměti, a k mockování se uchylujte až po vyčerpání „slušnějších”
možností.
Často jde trochu změnit kód, aby byl testovatelnější – například napsat funkci,
která čte soubor formátu `/etc/passwd`, ale jméno souboru jí předat argumentem.

betamax
-------

Vaše úlohy používají webová API. Při testování funkcionality API klientů
se vynoří řada problémů:

 * výsledky volání API mohou být pokaždé různé
 * k některým volání API je potřeba mít přístupové údaje
 * API může být zrovna nedostupné

V zásadě můžete omockovat knihovnu requests tak, aby
jednotlivé volání jako `get()` apod. vracela předem definovanou odpověď.
Při ponoření do hloubky ale zjistíte, že komplexita takového mockování může
velmi přesáhnout komplexitu samotného kódu, který testujete.
Jednodušší je tak použít již hotové řešení, [betamax].

[betamax]: https://betamax.readthedocs.io/

Betamax umožňuje nahrát HTTP komunikaci do kazet (souborů), které se potom
použijí při testech. V zásadě to funguje takto:

 * Pokud daný HTTP požadavek ještě neproběhl, provede se a nahraje na kazetu.
 * Pokud již proběhl, použije se daná kazeta pro simulaci.

Betamax funguje pouze s modulem requests při použití session.

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
    client = Client(betamax_session)
    assert client.foo() == 42
```

Pokud budete používat parametrizované testy, použijte
`betamax_parametrized_session`, aby kazety měly odlišné jméno při odlišných
parametrech.

Pro tip: Abyste nevytvářeli novou instanci třídy ve všech testech, můžete si
vytvořit vlastní fixture, která použije fixture `betamax_session`:

```python
@pytest.fixture
def client(betamax_session):
    return Client(session=betamax_session)
```

### Citlivé údaje

Při práci s webovými API často létají vzduchem citlivé údaje jako tokeny apod.

Vyvstávají dvě otázky:

 1. Jak umožnit spuštění testů bez vlastního tokenu?
 2. Jak citlivé údaje skrýt v kazetách a nedávat je do do gitu?

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
někde spočítá a získá, jako v případě Twitter API?
Na tuto otázku podrobněji odpovídá
[dokumentace](https://betamax.readthedocs.io/en/latest/configuring.html#filtering-sensitive-data).

V každém případě je moudré před uložením do gitu zkontrolovat, že se v kazetách
nenachází žádný citlivý údaj, a pokud tam je, přepsat kód tak, aby se tam nenacházel.

Testování aplikací ve Flasku
----------------------------

Pro testování aplikací ve Flasku se používá `app.test_client()`:

```python
import pytest

@pytest.fixture
def testapp():
    from hello import app
    app.config['TESTING'] = True
    return app.test_client()

def test_hello(testapp):
    assert 'Hello' in testapp.get('/').data.decode('utf-8')
```

Pozor, metody na testovacím klientu vrací [Response], ale trochu jinou, než tu
z requests.

[Response]: http://flask.pocoo.org/docs/0.11/api/#flask.Response

Jak to zapadá do našeho balíčku (odkazy)
----------------------------------------

[Kam dát testy?](http://doc.pytest.org/en/latest/goodpractices.html#choosing-a-test-layout-import-rules)
Tady pozor na to, aby testy byly součástí archivu s balíčkem (`setup.py sdist`), ale
pokud zvolíte první variantu umístění, aby se neinstalovaly (`setup.py install`),
protože by tam kolidovali s ostatními testy z jiných balíčků.
Případné soubory potřebné k testování bývá zvykem dávat do složky `fixtures` ve
složce s testy.

Spouštění testů pomocí
[setup.py test](http://doc.pytest.org/en/latest/goodpractices.html#integrating-with-setuptools-python-setup-py-test-pytest-runner).
Zde se také přidávají další testovací závislosti (`flexmock`, `betamax`...) do `tests_require`.

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
- '3.5'
install:
- python setup.py install
script:
- python setup.py test --addopts -v
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

Úkol
----

Vaším úkolem za 5 bodů je napsat testy k dosavadním úlohám pomocí pytestu.
Není nutné použít `flexmock` pokud to nepotřebujete.
Využití `betamax`u je silně doporučeno.

Podmínky:

 * Musí fungovat `setup.py test` a to nejen z gitu, ale i při rozbalení archivu z PyPI.
 * Všechny testovací závislosti se musí při uvedeném příkazu nainstalovat.
 * Testy samotné musí fungovat offline a bez nutnosti mít přístupové údaje k API.
 * Spuštění testů i znovu-nahrání kazet musí být zdokumentováno v README.
 * Nahrané kazety musí být v gitu a být součástí balíčku (ale neinstalují se).
 * Žádné nahrané kazety (ani jiné soubory) nesmí obsahovat citlivé údaje.
 * Alespoň část testu by měla být parametrická.
 * Musí být použit nativní způsob pytest testů (pytest umí spouštět i testy pro `unittest` apod.).
 * Testuje se všechno\*.
 * Testy musí běžet i na Travis CI.
 
\* Záměrně nestanovujeme podmínku na 100% pokrytí kódu testy.
Otestujte prostě kód tak, aby byly otestovány všechny podstatné součásti
včetně webové aplikace.
 
Úkol odevzdáváte tradičně s tagem v0.4 a nahráním nové verze na (testovací či pravou) PyPI.
