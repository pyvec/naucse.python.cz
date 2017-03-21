Webové aplikace: Flask
======================

Python je víceúčelový jazyk.
Na minulém cvičení jsme tvořili aplikace pro příkazovou řádku,
nyní se podíváme na aplikace webové.

Webových frameworků pro Python je více, mezi nejznámější patří [Django],
[Flask] nebo [Pyramid].

Pro naše účely použijeme Flask, protože je nejrychlejší na pochopení a
nevyžaduje striktně použití [MVC] paradigmatu.

[Django]: https://www.djangoproject.com/
[Flask]: http://flask.pocoo.org/
[Pyramid]: http://www.pylonsproject.org/
[MVC]: https://cs.wikipedia.org/wiki/Model-view-controller

Flask
-----

Flask opět můžete nainstalovat do virtualenvu, nejlépe použít projekt
z minulého cvičení:

```console
$ cd project
$ . env/bin/activate 
(env)$ python -m pip install Flask
```

Základní použití Flasku je poměrně primitivní.
Do souboru `hello.py` napište:

```python
from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello():
    return 'MI-PYT je nejlepší předmět na FITu!'

```

Pak aplikaci spusťte pomocí následujících příkazů.
(Na Windows použijte místo `export` příkaz `set`.)

```console
(env)$ export FLASK_APP=hello.py
(env)$ export FLASK_DEBUG=1
(env)$ flask run
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger pin code: 189-972-345
```
Na zmíněné adrese byste měli v prohlížeči vidět použitý text.

Proměnná prostředí `FLASK_APP` říká Flasku, kde aplikaci najít.
V daném souboru Flask hledá automaticky proměnnou jménem `app`.
([Jde nastavit](http://flask.pocoo.org/docs/0.12/cli/) i jiná.)

Proměnná `FLASK_DEBUG` říká, že se aplikace má spustit v ladícím režimu:
je zapnutý příjemnější výpis chyb, a aplikace se automaticky restartuje
po změnách.
Tento mód je užitečný, ale nebezpečný – návštěvníkům stránky může umožňit
spustit jakýkoli Pythonní kód.
Navíc aplikaci zpomaluje.
Používejte ho proto pouze na svém počítači.

V příkladu jsme vytvořili flaskovou aplikaci (`app`), pomocí dekorátoru
`@app.route` jsme vytvořili takzvanou routu (cestu). Říkáme tím, že na adrese
`/` bude k dispozici obsah, který vrátí definovaná funkce.
Více různých cest lze vytvořit jednoduše přidáním další funkce.

```python
@app.route('/')
def index():
    return 'Index Page'

@app.route('/hello')
def hello():
    return 'Hello, World'
```

Na adrese `http://127.0.0.1:5000/hello` pak uvidíte druhou stránku.

### Dynamické routy

Když vytváříte dynamický web, ne vždy můžete všechna URL znát dopředu.
Pokud například chcete zobrazit informace o uživatelích na adrese
`/user/hroncok` apod., musíte použít dynamické routy:

```python
@app.route('/user/<username>')
def profile(username):
    return 'User {}'.format(username)
```

Proměnnou část cesty ohraničíte lomenými závorkami a použijte jako parametr
funkce. Pokud chcete, můžete specifikovat, na jaký obsah se pravidlo vztahuje:

```python
@app.route('/post/<int:post_id>')
```

Můžete použít různá pravidla, např.:

 * `string` akceptuje jakýkoliv text bez lomítek (výchozí)
 * `int` akceptuje celá čísla
 * `float` akceptuje i desetinná čísla s tečkou
 * `path` akceptuje text i s lomítky

### Získání URL

Opačným způsobem jak k routám přistupovat je, když potřebujete získat URL
nějaké stránky, například protože potřebujete zobrazit odkaz.
K tomu se používá funkce `url_for()`, která jako první parametr bere jméno
routy (neboli jméno funkce, která routu obsluhuje):

```python
from flask import url_for
...
url_for('profile', username='hroncok')
```

Tuto funkci jde použít jen uvnitř funkce obsluhující cestu, pokud ji chcete
vyzkoušet například v interaktivní konzoli, můžete použít speciální kontext
manager:

```pycon
>>> with app.test_request_context():
...     print(url_for('profile', username='hroncok'))
... 
/user/hroncok
```

Možná si říkáte, proč tu URL prostě nevytvořit ručně, ale mohli byste narazit
na problém, pokud cestu později změníte – což se může stát např. i když web
nasadíte na jiný server.

### Šablony

Zatím jsou naše webové stránky poměrně nudné, protože nepoužívají HTML.
Klidně byste mohli udělat něco jako:

```python
@app.route('/')
def hello():
    return '<html><head><title>...'
```

...ale asi by to nebylo příliš příjemné.
Lepší je použít šablony:

```python
from flask import render_template

@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)
```

Pak je třeba vedle souboru vytvořit složku `templates` a v ní `hello.html`:

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
        <a href=" {{ url_for('hello') }} ">Go back home</a>
        {% else %}
        <h1>Hello, World!</h1>
        {% endif %}
    </body>
</html>
```
{% endraw %}

{% raw %}
Šablony používají v Pythonu velmi oblíbený šablonovací jazyk [Jinja2].
Kompletní popis jazyka najdete v [dokumentaci][Jinja2], ale
pro většinu stránek se obejdete s `{% if %}` a `{{ promenna }}` jako výše,
případně s `{% for %}/{% endfor %}`.
{% endraw %}

Veškerý kontext (proměnné) do šablony musí přijít z volání `render_template()`,
navíc můžete automaticky použít např. funkci `url_for()`.

[Jinja2]: http://jinja.pocoo.org/latest/templates/

Pro debugování je vhodné nastavit automatické načítání změn šablon:

```python
if app.config.get('DEBUG'):
    app.config['TEMPLATES_AUTO_RELOAD'] = True
```

#### Filtry

Není úplně elegantní vzít nějaká data (např. tweety z Twitter API) a ještě před
předáním šabloně do nich cpát svoje úpravy (např. HTML).
Od toho jsou tu filtry. Filtr transformuje hodnotu na řetězec,
který pak ukážeme uživateli.

Zde je například filtr `time`, který načte čas v určitém formátu
a převede do jiného:

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

V šabloně `date_example.html`:

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

Například když v aplikaci výše navštívíme URL `/hello/<script>alert("Foo")`,
bude výsledné HTML vypadat takto:

```html
<!doctype html>
<title>Hello from Flask</title>

  <h1>Hello &lt;script&gt;alert(&#34;Foo&#34;)!</h1>
```

Někdy je ovšem potřeba do stránky opravdu vložit HTML.
To se dá zajistit dvěma způsoby. Nejjednodušší je vestavěný filtr `safe`:

{% raw %}
```html+jinja
{{ "<em>Text</em>" | safe }}
```
{% endraw %}

Z Pythonu pak lze použít [jinja2.Markup](http://jinja.pocoo.org/docs/dev/api/#jinja2.Markup),
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

### Statické soubory

Pokud budete potřebovat nějaké statické soubory (např. css soubory nebo
obrázky), dejte je do složky `static` a přistupujte k nim pomocí:

```python
url_for('static', filename='style.css')
```

V šabloně pak například:

{% raw %}
```html+jinja
<link href="{{ url_for('static', filename='style.css') }}" rel="stylesheet">
```
{% endraw %}

### A další

Flask umí i další věci – například zpracování formulářů, chybové stránky nebo
přesměrování.

Všechno to najdete
[v dokumentaci](http://flask.pocoo.org/docs/0.11/quickstart/).

Deployment
----------

Aplikace běží na našem počítači, ale jak ji dostat do internetu?
Existují různé možnosti, jednou z nich je nasadit ji do cloudu.
My použijeme [Python Anywhere], protože je pro limitované použití zdarma.

K posílání kódu na produkční prostědí budeme používat Git.
Nejprve proto uložte celý projekt do Gitu a nahrajte na Github.

Potom se zaregistrujte na
[www.pythonanywhere.com](https://www.pythonanywhere.com/) a vyberte
Beginner Account.
Po přihlášení se ukáže záložka "Consoles", kde vytvoříme "Bash" konzoli.
V té vytvořte a aktivujte virtuální prostředí, a nainstalujte Flask (plus
případně další závislosti).

PythonAnywhere je postavený na Ubuntu, takže příkaz na vytvoření prostředí
vypadá jinak než na vašich počítačích.
Napište příkazy takto (bez úvodního `$`):

```console
$ virtualenv --python=python3.5 env
$ . env/bin/activate
$ python -m pip install flask
```

Následně naklonujte na PythonAnywhere náš kód.
S veřejným repozitářem je to jednodušší – stačí ho naklonovat „anonymně”
(`git clone https://github.com/<github-username>/<github-repo>`).
Pokud ale používáme privátní repozitář, bude potřeba si vygenerovat SSH klíč:

```console
$ ssh-keygen  # (zeptá se na hesla ke klíči)
$ cat ~/.ssh/id_rsa.pub
```

Obsah souboru `~/.ssh/id_rsa.pub` je pak potřeba přidat na Github v osobním
nastavení v sekci "SSH and GPG Keys".
Pak můžeme klonovat přes SSH:

```console
$ git clone git@github.com:<github-username>/<github-repo>.git
```

Zbývá nastavit, aby PythonAnywhere tento kód spustil jako webovou aplikaci.

Přejděte na stránkách PythonAnywhere do Dashboard do záložky Web,
a vytvořte novou aplikaci.
V nastavení zvolte Manual Configuration a Python 3.5.

V konfiguraci vzniklé webové aplikace je potřeba nastavit "Virtualenv"
na cestu k virtuálnímu prostředí (`/home/<jméno>/env`),
a obsah "WSGI Configuration File" přepsat.
To jde buď kliknutím na odkaz v konfiguraci (otevře se webový editor),
nebo zpět v bashové konzoli pomocí editoru jako `vi` nebo `nano`.

Nový obsah souboru by měl být:

```python
import sys
path = '/home/<uživatelské-jméno>/<jméno-adresáře>'
if path not in sys.path:
    sys.path.append(path)

from <jméno-souboru> import app as application
```

(Za `<uživatelské-jméno>`, `<jméno-adresáře>` a `<jméno-souboru>` je samozřejmě potřeba doplnit
vaše údaje. Jméno souboru je zde bez přípony `py`.)

Nakonec restartujte aplikaci velkým zeleným tlačítkem na záložce Web,
a na adrese `<uživatelské-jméno>.pythonanywhere.com` si ji můžete
prohlédnout.

[Python Anywhere]: https://www.pythonanywhere.com/


### Deployment API klíčů

Protože vaše tajné klíče nejsou v repozitáři, je nutné je předat aplikaci
zvlášť.
Konfigurační soubor jde nahrát v záložce Files, nebo opět vytvořit
a editovat ve webové konzoli.

!!! note ""
    Doporučujeme pro tyto potřeby stejně raději nepoužívat API klíče
    k vlastním účtům, raději si vyrobte nějaké účty pouze pro tento účel.
    Twitter vyžaduje před vydáním API klíčů zadání a potvrzení telefonního čísla.


### Aktualizace

Když nahrajeme nový kód na Github, je vždy potřeba provést na PythonAnywhere
v konzoli `git pull` a pak v záložce Web aplikaci restartovat.

