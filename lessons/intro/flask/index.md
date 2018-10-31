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
[Flask]: http://flask.pocoo.org/
[Pyramid]: http://www.pylonsproject.org/
[Flask]: http://flask.pocoo.org/
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
([Jde nastavit](http://flask.pocoo.org/docs/1.0/cli/) i jiná.)
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

[`@app.route`]: http://flask.pocoo.org/docs/1.0/api/#flask.Flask.route
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

[dynamické routy]: http://flask.pocoo.org/docs/1.0/quickstart/#variable-rules

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

[`url_for()`]: http://flask.pocoo.org/docs/1.0/api/#flask.url_for

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
případně s [cyklem][jinja-for]: `{% for %}`/`{% endfor %}`.
{% endraw %}

Veškerý kontext (proměnné) do šablony musí přijít z volání `render_template()`.
Navíc můžete použít vybrané funkce, např. `url_for()`.
(Jiné funkce známé z Pythonu ale použít nejdou – ač jsou podobné, je Jinja2
jiný jazyk než Python.)

[Jinja2]: http://jinja.pocoo.org/docs/2.10/templates/
[jinja-for]: http://jinja.pocoo.org/docs/2.10/templates/#for

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

V Pythonu pak lze použít [jinja2.Markup](http://jinja.pocoo.org/docs/dev/api/#jinja2.Markup),
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

### Vlastní podtřída Flask

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
přesměrování.

Všechno to najdete
[v dokumentaci](http://flask.pocoo.org/docs/1.0/quickstart/).
