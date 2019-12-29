Webové aplikace: Flask
======================

Python je víceúčelový jazyk.
Na minulém cvičení jsme tvořili aplikace pro příkazovou řádku,
nyní se podíváme na aplikace webové.

Webových frameworků pro Python je více, mezi nejznámější patří [Django],
[Flask] nebo [Pyramid].

Pro naše účely použijeme [Flask], protože je nejrychlejší na pochopení a
nevyžaduje striktně použití [MVC] paradigmatu.

[Django]: https://www.djangoproject.com/
[Flask]: https://flask.palletsprojects.com
[Pyramid]: http://www.pylonsproject.org/
[MVC]: https://cs.wikipedia.org/wiki/Model-view-controller

Flask
-----

Flask opět můžete nainstalovat do virtualenvu, nejlépe použít projekt
z minulého cvičení:

```console
$ cd project
$ . __venv__/bin/activate 
(__venv__) $ python -m pip install Flask
```

Základní použití Flasku je poměrně primitivní.
Do souboru `hello.py` napište:

```python
from flask import Flask
app = Flask(__name__)

@app.route('/')
def index():
    return 'MI-PYT je nejlepší předmět na FITu!'

```

Pak aplikaci spusťte pomocí následujících příkazů.
(Na Windows použijte místo `export` příkaz `set`.)

```console
(__venv__) $ export FLASK_APP=hello.py
(__venv__) $ export FLASK_DEBUG=1
(__venv__) $ flask run
 * Serving Flask app "hello"
 * Forcing debug mode on
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 189-972-345
```
Na zmíněné adrese byste měli v prohlížeči vidět použitý text.

Proměnná prostředí `FLASK_APP` říká Flasku, kde aplikaci najít.
V daném souboru Flask hledá automaticky proměnnou jménem `app`.
([Jde nastavit](https://flask.palletsprojects.com/en/1.1.x/cli/) i jiná.)
Proměnná `FLASK_DEBUG` nastavuje ladícím režim, který si popíšeme za chvíli.

V programu jsme jako `app` vytvořili flaskovou aplikaci.
Argument `__name__` je jméno modulu – Flask podle něj hledá soubory,
které k aplikaci patří (viz `static` a `templates` níže).

Pomocí dekorátoru [`@app.route`] jsme zaregistrovali takzvaný *view* (pohled) –
funkci, která vrací obsah pro danou [cestu v URL][URL].
Tomuto spojení cesty a pohledové funkce se říká *route* (nebo počeštěně „routa“).
My konkrétně říkáme, že na cestě `/` (tedy na „domovské stránce“) bude
k dispozici obsah, který vrátí funkce `index`.

[URL]: ../../fast-track/http/#url-anatomy

Více různých adres lze obsloužit jednoduše přidáním dalších funkcí:

```python
@app.route('/')
def index():
    return 'Index Page'

@app.route('/hello/')
def hello():
    return 'Hello, World'
```

Na adrese [`http://127.0.0.1:5000/hello/`][local-hello] pak uvidíte druhou stránku.

[`@app.route`]: https://flask.palletsprojects.com/en/1.1.x/api/#flask.Flask.route
[local-hello]: http://127.0.0.1:5000/hello/

### Ladící režim

Proměnná `FLASK_DEBUG` říká, že se aplikace má spustit v ladícím režimu:
je zapnutý příjemnější výpis chyb a aplikace se automaticky restartuje
po změnách.

Zkuste ve funkci `hello()` vyvolat výjimku (například dělení nulou – `1/0`)
a podívat se, jak chyba v ladícím režimu „vypadá“:
Flask ukáže *traceback* podobný tomu z příkazové řádky a navíc vám na každé
úrovni umožní pomocí malé ikonky spustit konzoli.
Bezpečnostní PIN k této konzoli najdete v terminálu, kde server běží.

Ladící režim je užitečný, ale nebezpečný – návštěvníkům stránky může
(po prolomení celkem jednoduchého „hesla“) umožnit spustit jakýkoli pythonní kód.
Navíc aplikaci zpomaluje.
Používejte ho proto *pouze* na svém počítači.

### Dynamické routy

Když vytváříte dynamický web, ne vždy můžete všechna URL znát dopředu.
Budete například chctít zobrazit informace o uživatelích na adresách
jako `/user/hroncok/`, ale nemůžete při každé registraci nového uživatele
přidávat novou funkci do kódu.
Musíte použít [dynamické routy]:

[dynamické routy]: https://flask.palletsprojects.com/en/1.1.x/quickstart/#variable-rules

```python
@app.route('/user/<username>/')
def profile(username):
    return 'User {}'.format(username)
```

Proměnnou část cesty ohraničíte lomenými závorkami a použijte jako parametr
funkce. Pokud chcete, můžete specifikovat, na jaký obsah se pravidlo vztahuje.
Například číselný idenifikátor článku pro adresy jako `/post/42/` můžete zadat
takto:

```python
@app.route('/post/<int:post_id>/')
```

Můžete použít různá pravidla, např.:

 * `string` akceptuje jakýkoliv text bez lomítek (výchozí)
 * `int` akceptuje celá čísla (a pohledové funkci je předá jako `int`, ne text)
 * `float` akceptuje i desetinná čísla s tečkou (a předá je jako `float`)
 * `path` akceptuje text i s lomítky

Rout můžte definovat i víc pro jednu funkci.
Často se to používá s výchozí hodnotou argumentu:

```python
@app.route('/hello/')
@app.route('/hello/<name>/')
def hello(name='world'):
    return 'Hello, {}!'.format(name)
```

### Získání URL

Opačným způsobem jak k routám přistupovat je, když potřebujete získat URL
nějaké stránky, například protože potřebujete zobrazit odkaz.
K tomu se používá funkce [`url_for()`], která jako první parametr bere jméno
routy (neboli jméno funkce, která routu obsluhuje), a pak pojmenované argumenty
pro pravidla v dynamické routě:

[`url_for()`]: https://flask.palletsprojects.com/en/1.1.x/api/#flask.url_for

```python
from flask import url_for

...

@app.route('/url/')
def show_url():
    return url_for('profile', username='hroncok')
```

Tuto funkci jde použít jen uvnitř pohledové funkce,
Pokud ji chcete vyzkoušet například v interaktivní konzoli,
můžete použít speciální kontext:

```pycon
>>> with app.test_request_context():
...     print(url_for('profile', username='hroncok'))
... 
/user/hroncok/
```

Možná si říkáte, proč tu URL prostě nevytvořit ručně.
S takovým přístupem byste ale mohli narazit na problém, pokud cestu později
změníte – což se může stát např. i když web nasadíte na jiný server.
Generování URL vám také může zjednodušit nasazení statické verze stránek.

Pro URL v rámci vašich stránek proto doporučujeme `url_for` používat důsledně.

### Šablony

Zatím jsou naše webové stránky poměrně nudné: obsahují jen prostý text,
nepoužívají HTML.

> [note]
> Předpokládáme, že víte co je to [HTML] a [CSS].
> Jestli ne, doporučujeme si projít základy těchto webových technologií
> např. na stránkách [MDN].

[HTML]: https://developer.mozilla.org/en-US/docs/Web/HTML
[CSS]: https://developer.mozilla.org/en-US/docs/Web/CSS
[MDN]: https://developer.mozilla.org/en-US/docs/Web

Klidně byste mohli udělat něco jako:

```python
@app.route('/')
def hello():
    return '<html><head><title>...'
```

...ale asi by to nebylo příliš příjemné.
Python je jazyk dělaný na popis algoritmů, procesů a logiky spíš než obsahu.
Lepší je HTML dát do zvláštního souboru a použít ho jako *šablonu*
(angl. *template*).
Z Flasku vypadá použití šablony takto:

```python
from flask import render_template

@app.route('/hello/')
@app.route('/hello/<name>/')
def hello(name=None):
    return render_template('hello.html', name=name)
```

Funkce `render_template` nejen vrátí HTML z daného souboru, ale umí do něj
i doplnit informace, které dostane v pojmenovaných argumentech.

Ukažme si to na příkladu: vedle souboru s kódem vytvořte složku `templates`
a v ní `hello.html` s tímto obsahem:

{% raw %}
```html+jinja
<!doctype html>
<html>
    <head>
        <title>Hello from Flask</title>
    </head>
    <body>
        {% if name %}
            <h1>Hello {{ name }}!</h1>
            <a href="{{ url_for('hello') }}">Go back home</a>
        {% else %}
            <h1>Hello, World!</h1>
        {% endif %}
    </body>
</html>
```
{% endraw %}

{% raw %}
Šablony používají (jako výchozí variantu) šablonovací jazyk [Jinja2],
který se s Flaskem a jinými frameworky pro Python používá často.
Kompletní popis jazyka najdete v [dokumentaci][Jinja2], ale
pro většinu stránek se obejdete s doplněním hodnoty (`{{ promenna }}`)
a podmíněným obsahem (`{% if %}`) jako výše,
případně s [cyklem][jinja-for]: `{% for %}`/`{% endfor %}`. Ve větších
aplikacích se pak hodí použití `{% include ... %}`, `{% extends ... %}` 
a případně také tvorba maker `{% macro ... %}`/`{% endmacro %}`.
{% endraw %}

Veškerý kontext (proměnné) do šablony musí přijít z volání `render_template()`.
Navíc můžete použít vybrané funkce, např. `url_for()`.
(Jiné funkce známé z Pythonu ale použít nejdou – ač jsou podobné, je Jinja2
jiný jazyk než Python.)

[Jinja2]: https://jinja.palletsprojects.com/en/2.10.x/templates/
[jinja-for]: https://jinja.palletsprojects.com/en/2.10.x/templates/#for

#### Filtry

Není úplně elegantní vzít nějaká data (např. tweety z Twitter API) a ještě před
předáním šabloně do nich cpát svoje úpravy (např. převod na HTML).
Od toho jsou tu filtry. Filtr transformuje hodnotu na řetězec,
který pak ukážeme uživateli.

Zde je například filtr `time`, který načte čas v určitém formátu
a převede ho do jiného:

```python
from datetime import datetime

@app.template_filter('time')
def convert_time(text):
    """Convert the time format to a different one"""
    dt = datetime.strptime(text, '%a %b %d %H:%M:%S %z %Y')
    return dt.strftime('%c')

@app.route('/date_example')
def date_example():
    return render_template(
        'date_example.html',
        created_at='Tue Mar 21 15:50:59 +0000 2017',
    )
```

V šabloně `date_example.html` se pak filtr použije pomocí svislítka:

{% raw %}
```html+jinja
{{ created_at|time }}
```
{% endraw %}

Pokud potřebujete velmi obecný filtr, je vhodné se podívat do [seznamu těch vestavěných](https://jinja.palletsprojects.com/en/2.10.x/templates/#builtin-filters).

#### Escaping

V textu, který se vkládá do šablon, jsou automaticky nahrazeny znaky, které
mají v HTML speciální význam.
Zabraňuje se tak bezpečnostním rizikům, kdy se vstup od uživatele interpretuje
jako HTML.

Například když v aplikaci výše navštívíme URL `/hello/<script>alert("Foo")/`,
bude výsledné HTML vypadat takto:

```html
<!doctype html>
<title>Hello from Flask</title>

  <h1>Hello &lt;script&gt;alert(&#34;Foo&#34;)!</h1>
```

> [note]
> Některé prohlížeče (či doplňky do nich) proti podobným útokům různým způsobem
> chrání. Budete-li na své stránky zkoušet „zaútočit”, zkontrolujte v konzoli
> URL, které vaše aplikace v požadavku reálně dostává.
> Pro příklad výše to může být `/hello/%3Cscript%3Ealert(%22Foo%22)/`.

Někdy je ovšem potřeba do stránky opravdu vložit HTML.
To se dá zajistit dvěma způsoby. Nejjednodušší je vestavěný filtr `safe`:

{% raw %}
```html+jinja
{{ "<em>Text</em>" | safe }}
```
{% endraw %}

V Pythonu pak lze použít [jinja2.Markup](https://jinja.palletsprojects.com/en/2.10.x/api/#jinja2.Markup),
čímž se daný text označí jako „bezpečný”.

```python
import jinja2

@app.template_filter('time')
def convert_time(text):
    """Convert the time format to a different one"""
    dt = datetime.strptime(text, '%a %b %d %H:%M:%S %z %Y')
    result = dt.strftime('<strong>%c</strong>')
    return jinja2.Markup(result)
```

Při použití `safe` a `Markup` však vždycky myslete na to, aby nikdo
(ani nikdo mnohem chytřejší než vy) nemohl na vaší stránce provést něco
nekalého.


### Statické soubory

Pokud budete potřebovat nějaké statické soubory (např. styly CSS nebo
obrázky), dejte je do adresáře `static` vedle souboru s kódem
a přistupujte k nim pomocí routy `static`:

```python
url_for('static', filename='style.css')
```

V šabloně pak například:

{% raw %}
```html+jinja
<link href="{{ url_for('static', filename='style.css') }}" rel="stylesheet">
```
{% endraw %}

### Logování

Při vytváření webové aplikace chcete často komunikovat nejen prostřednictvím 
HTTP odpovědí na dotazy (ať už ve formě webové stránky, JSON odpovědi či jiného
formatu), ale také vypisovat různé chybové, informační či ladící hlášky na
straně serveru. Možností je použít například funkci `print`, ale ta není 
dostatečně flexibilní. Brzy narazíte na problémy, jako že výstup není konzistentní 
s jinými hláškami z Flasku, že pro různé typy výpisů, časová razítka, přesměrování 
logu do souboru a další potřebujete vytvářet spoustu logiky kolem namísto vytváření 
samotné webové aplikace.

Řešením je použít standardní logovací modul [logging], který řeší vše potřebné 
(úrovně zpráv, filtry, formátování časového razítka a dalších meta-informací o
běhu programu) a výstup bude konzistentní s jinými aplikacemi (jiní správci 
vaší webové aplikace pak nebudou z formátu výstupů zmatení). Protože používáme
Flask a ten také [loguje tímto modulem](https://flask.palletsprojects.com/en/1.1.x/logging/),
stačí použít předpřipravený `app.logger`.

```python
from flask import Flask

app = Flask(__name__)
app.logger.debug("I've just initialized the Flask app")

@app.route('/')
def index():
    app.logger.warning('Someone is accessing the index page!')
    return 'Index Page'
```

Ve výchozím nastavení se loguje pouze od úrovně upozornění výše (`warning`, 
`error`, `critical`). Při spuštění aplikace v ladícím režimu se loguje vše
(navíc i `debug` a `info`). Aktuální úroveň je možné také změnit pomocí metody
`setLevel`, viz dokumentace modulu [logging].

[logging]: https://docs.python.org/3/library/logging.html#module-logging

### Větší Flask aplikace

Flask je sice označován jako mikroframework, to ale neznamená, že jej nelze 
použít na větší a složitější webové aplikace. Pokud chcete vytvářet vytvářet 
aplikaci s databází a ORM modely, je nutné propojit Flask s dalšími knihovnami
(například [flask-sqlalchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/), 
nebo [flask-pymongo](https://flask-pymongo.readthedocs.io/en/latest/)).

Jiné frameworky postavené nad [Model-View-Controller](https://cs.wikipedia.org/wiki/Model-view-controller)
paradigmatem mají tyto vlastnosti již zabudovány v sobě (například [Django]).

Následující sekce popisují některé zajímavé techniky, které se mohou u větších 
a složitějších aplikací hodit.

#### create_app factory

Mimo vytváření Flask aplikace přímo v modulu, je možné aplikaci tvořit pomocí
funkce, tzv. [`application_factory`](https://flask.palletsprojects.com/en/1.1.x/patterns/appfactories/), 
standardně pojmenované `create_app`. Takový přístup má výhodu, že aplikace se 
neinicializuje hned při importu modulu, ale až při zavolání funkce. Voláním funkce
můžete navíc předat i konfigurační parametry (typicky cesta ke konfiguračnímu 
souboru). Díky tomu lze snadněji vytvářet Flask aplikace s různými konfiguracemi
pro testování nebo dokonce vytvářet více Flask aplikací v rámci jednoho Python skriptu.

```python
def create_app(config=None):
    app = Flask(__name__)

    app.config.from_pyfile(config or 'config.py')
    app.config['the_answer'] = 42
    app.secret_key = os.environ.get('MY_SECRET', None)

    return app
```

#### Blueprint moduly

Ve velkých webových aplikacích je již vhodné seskupovat jednotlivé pohledy do
samostatných celků. K tomuto účelu slouží ve Flasku [blueprinty] (hezky česky 
„modrotisk” nebo také [„modrák”](https://cs.wikipedia.org/wiki/Diazotypie)).
Výhodou je, že můžete vytvořit blueprint (instanci
třídy [Blueprint]) s několika views, vlastní `templates` složkou a dalším 
nastavením nezávisle na tom, v jaké Flask aplikaci pak bude použitý. Takový 
blueprint pak můžete využívat i v několika různých aplikacích a snadno tak
dosáhnout znovupouželnosti.

```python
from flask import Blueprint

auth = Blueprint('auth', __name__, template_folder='templates')

@auth.route('/login')
def login():
    ...

@auth.route('/logout')
def logout():
    ...

@auth.app_template_filter('userlink')
def user_link(username):
    ...
```

Blueprint pak stačí ve Flask aplikaci [registrovat](https://flask.palletsprojects.com/en/1.1.x/api/#flask.Flask.register_blueprint)
a je jedno, zda ji vytváříte pomocí `create_app` nebo napřímo. Navíc můžete mimo 
jiné přidat i prefix pro všechny cesty v blueprintu.

```python
from flask import Flask
from auth.views import auth

app = Flask(__name__)
# this will create the /auth/login and /auth/logout endpoints
app.register_blueprint(auth, url_prefix='/auth')
```

V případě použití `url_for` je třeba cesty z blueprintu namespacovat, např.:

```python
url_for('auth.login')
```

[blueprinty]: https://flask.palletsprojects.com/en/1.1.x/blueprints/
[Blueprint]: https://flask.palletsprojects.com/en/1.1.x/api/#flask.Blueprint

#### Vlastní podtřída Flask

Třída `Flask` je uzpůsobena k tomu, aby bylo možné snadno rozšiřovat a přepisovat 
výchozí chování. Mimo přidávání vlastních metod lze například měnit třídy, které 
budou použity pro HTTP požadavky a odpovědi, měnit výchozí konfiguraci `flask` a
spoustu dalšího. Nezapomeňte volat konstruktor nadtřídy.

```python
from flask import current_app, Flask, Response

class MIPYTResponse(Response):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_cookie('MI-PYT', 'best')


class GreeterApp(Flask):
    response_class = MIPYTResponse

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.greetings = 0
    
    def greet(self):
        self.greetings += 1
        return 'Hello!'


app = GreeterApp(__name__)


@app.route('/')
def greet():
    return current_app.greet()


@app.route('/number/')
def greetings_number():
    return str(current_app.greetings)
```

### A další

Flask umí i další věci – například zpracování formulářů, chybové stránky nebo
přesměrování. Také existuje i řada [rozšíření](https://flask.palletsprojects.com/en/1.1.x/extensions/?highlight=extensions),
které mohou ušetřit práci s běžnými úkony jako například správa uživatelů,
 tvorba REST API nebo integrace s různými službami.

Všechno to najdete
[v dokumentaci](https://flask.palletsprojects.com/en/1.1.x/quickstart/).
