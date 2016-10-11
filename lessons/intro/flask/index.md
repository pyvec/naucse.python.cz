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

```bash
$ cd project
$ . env/bin/activate 
(env)$ python -m pip install Flask
```

Základní použití Flasku je poměrné primitivní:

```python
from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello():
    return 'MI-PYT je nejlepší předmět na FITu!'

if __name__ == '__main__':
    app.run(debug=True)
```

```bash
(env)$ python hello.py
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger pin code: 189-972-345
```
Na zmíněné adrese byste měli v prohlížeči vidět použitý text.

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

Pomocí `app.run()` jsme aplikaci spustili na lokálním počítači.
V případě reálného nasazení pak aplikaci předáme nějakému webovému serveru.
Argument `debug` slouží k zjednodušení debugování
(např. případné výjimky uvidíte přímo v prohlížeči),
pro reálné nasazení by však tento režim neměl být zapnut, kvůli bezpečnosti a
dopadům na výkon.

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

Opačným způsobem jak k routám přistupovat, je když potřebujete získat URL
nějaké stránky, například protože potřebujete zobrazit odkaz.
K tomu se používá funkce `url_for()`:

```python
from flask import url_for
...
url_for('profile', username='hroncok')
```

Tuto funkci jde použít jen uvnitř funkce obsluhující cestu, pokud ji chcete
vyzkoušet například v interaktivní konzoli, můžete použít speciální kontext
manager:

```python
>>> with app.test_request_context():
...     print(url_for('profile', username='hroncok'))
... 
/user/hroncok
```

Možná si říkáte, proč tu cestu prostě nevytvořit ručně, ale mohli byste narazit
na problém, pokud cestu později změníte.

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

```html
<!doctype html>
<title>Hello from Flask</title>
{% if name %}
  <h1>Hello {{ name }}!</h1>
{% else %}
  <h1>Hello, World!</h1>
{% endif %}
```

Šablony používají v Pythonu velmi oblíbený [Jinja2].
(Základní použití najdete na odkaze.)

Veškerý kontext do šablony musí přijít z volání `render_template()`,
navíc můžete automaticky použít např, `url_for()`.

[Jinja2]: http://jinja.pocoo.org/docs/dev/templates/

Pro debugování je vhodné nastavit automatické načítání změn šablon:

```python
if __name__ == "__main__":
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug=True)
```

#### Filtry

Není úplně elegantní vzít nějaká data (např. tweety z Twitter API) a před
předáním šabloně do nich cpát svoje úpravy (např. HTML).
Od toho jsou tu filtry. Filtr je funkce na transformaci řetězce, kterou lze
použít v šabloně.

Zde je například filtr, který načte čas v určitém formátu a převede do jiného:

```python
@app.template_filter('time')
def convert_time(text):
    """Convert the time format to a different one"""
    dt = datetime.strptime(text, '%a %b %d %H:%M:%S %z %Y')
    return dt.strftime('%c')
```

V šabloně:

```html
{{ tweet.created_at|time }}
```

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

```
{{ "<em>Text</em>" | safe }}
```

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

```html
<link href="{{ url_for('static', filename='style.css') }}" rel="stylesheet">
```

Další věci, které možná budete potřebovat, jako například zpracování formulářů,
najdete [v dokumentaci](http://flask.pocoo.org/docs/0.11/quickstart/).

Deployment
----------

Aplikace běží na našem počítači, ale jak ji dostat do internetu?
Existují různé možnosti, jednou z nich je nasadit ji do cloudu.
My použijeme [Python Anywhere], protože je pro limitované použití zdarma.

K posílání kódu na produkční prostědí budeme používat Git.
Nejprve proto uložte celý projekt do Gitu a nahrajte na Github.

Potom se zaregistrujte na [https://www.pythonanywhere.com/] a vyberte
Beginner Account.
Po přihlášení se ukáže záložka "Consoles", kde vytvoříme "Bash" konzoli.
V té vytvoříme a aktivujeme virtuální prostředí, a nainstalujeme Flask.
(Příkaz vypadá kvůli balíčkovací politice Debianu
trochu jinak než na našich počítačích.)

```bash
virtualenv --python=python3.5 env
. env/bin/activate
python -m pip install flask
```

Následně naklonujeme na PythonAnywhere náš kód.

```bash
git clone https://github.com/<github-username>/<github-repo>
```

Následně přejdi na stránkách PythonAnywhere do Dashboard do záložky Web,
a vytvoř novou aplikaci.
V nastavení zvol Manual Configuration a Python 3.5.

V konfiguraci vzniklé webové aplikace je potřeba nastavit "Virtualenv"
na cestu k virtuálnímu prostředí (`/home/<jméno>/env`),
a obsah "WSGI Configuration File" přepsat na:

```python
import sys
path = '/home/encukou/flapp'
if path not in sys.path:
    sys.path.append(path)

from flapp import app as application
```

To jde buď kliknutím na odkaz v konfiguraci (otvíře se webový editor),
nebo zpět v Bashové konzoli pomocí editoru jako `vi` nebo `nano`.

[Python Anywhere]: https://www.pythonanywhere.com/


### Deployment API klíčů

Protože vaše tajné klíče nejsou v repozitáři, je nutné je předat aplikaci
zvlášť.
Konfigurační soubor jde nahrát v záložce Files, nebo opět vytvořit
a editovat ve webové konzoli.

**Poznámka:** Doporučujeme pro tyto potřeby stejně raději nepoužívat API klíče
k vlastním účtům, raději si vyrobte nějaké účty pouze pro tento účel.
Twitter vyžaduje před vydáním API klíčů zadání a potvrzení telefonního čísla.

Úkol
----

Vaším úkolem za 5 bodů je rozšířit command line aplikaci z minulého
cvičení o webové rozhraní. Stávající funkcionalita ale musí být zachována,
k tomu můžete použít například podpříkazy pro click:

```python
@click.group()
def cli():
    pass

@cli.command()
def wev():
    """Run the web app"""
    click.echo('Running the web app')

@cli.command()
def console():
    """Run the console app"""
    click.echo('Running the console app')
```

Výslednou aplikaci nasaďte na PythonAnywhere, nebo jiný veřejný hosting.
Odkaz na běžící aplikaci a repozitář nám pošlete e-mailem.
V repozitáři prosím nastavte tag `v0.2`.
Termín odevzdání je začátek příštího cvičení (dřívější paralelky).

### Twitter Wall

Konzole není pro Twitter Wall dostatečně vhodné médium,
doplňte do aplikace webový frontend, který bude zobrazovat
výsledky hledání. Hledaný pojem by měl jít zadat pomocí URL.

Pro plný počet bodů  musí rozhraní zobrazovat avatary uživatelů
a zpracovávat [entity] jako obrázky, odkazy, zmínky a hash tagy.
Ideální je k tomu využít filtr.

[entity]: https://dev.twitter.com/overview/api/entities-in-twitter-objects

### GitHub Issues Bot

Bylo by dobré, kdyby labelovací robot neprocházel issues v určitém intervalu,
ale dozvěděl se o nově založených issues.
Vyrobte webovou aplikaci, která bude na nějakém URL naslouchat událostem na
GitHubu a nově založenou issue olabeluje hned po založení.
K tomu použijte [webhook].

Pro načtení dat od GitHubu použijte globální objekt `request`:

```python
from flask import request

@app.route('/hook', methods=['POST'])
def hook():
    data = request.get_json()
    ...
    return ''
```

Ve výchozí routě `/` by aplikace měla informovat uživatele, jak lze použít.

[webhook]: https://developer.github.com/webhooks/

### Vlastní zadání

Pokud jste minule pracovali na jiném API, konzultujte s cvičícím, co máte dělat.
