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
My použijeme [OpenShift], protože je pro limitované použití zdarma,
protože je jednoduchý a protože jsme z Red Hatu :)

Nejprve se zaregistrujte na [OpenShift], poté jděte do [OpenShift Web Console].

Dole na stránce je tlačítko *Add Application...*, použijte ho a zvolte
*Python 3.3* (novější bohužel zatím není).

Aplikaci můžete přejmenovat, také můžete přidat adresu svého git repozitáře,
pokud je veřejný (použijte HTTPS adresu).

Potvrďte tlačítkem *Add Application* a vyčkejte.

Mezitím můžete v [nastavení](https://openshift.redhat.com/app/console/settings)
přidat svůj veřejný SSH klíč.

Až se aplikace vytvoří, zkopírujte si git URL, něco jako:

    ssh://123456789123456789123456@flask-hroncok.rhcloud.com/~/git/flask.git/

Přidejte ho jako remote do svého repozitáře s kódem:

    git add remote openshift ssh://123456789123456789123456@flask-hroncok.rhcloud.com/~/git/flask.git/

Aby naše aplikace běžela na OpenShiftu, musíme do repozitáře přidat dva soubory.
Soubor `requirements.txt` se závislostmi:

```
Flask
requests
click
```

A soubor `wsgi.py`, který slouží jako vstupní soubor pro OpenShift.
V něm je třeba importovat naší aplikaci jako `application`.
Zde předpokládáme, že soubor s aplikací se jmenuje `hello.py`.

```python
from hello import app as application
```

Nové commity pushněte na OpenShift:

    git push openshift master

Pokud jste při vytváření aplikace nepřidali váš repozitář,
možná budete muset použít sílu:

    git push --force openshift master

To je vše, aplikace by měla běžet na
[flask-hroncok.rhcloud.com](https://flask-hroncok.rhcloud.com/) (či podobně).
Nezapomeňte nové commity pushovat do hlavního repozitáře s kódem
(na Githubu nebo GiLabu) i na OpenShift:

    git push  # pushuje do původního repozitáře
    git push openshift master

[OpenShift]: https://www.openshift.com/
[OpenShift Web Console]: https://openshift.redhat.com/app/console/applications

### API klíče na OpenShiftu

Protože vaše tajné klíče nejsou v repozitáři, nabízí se otázka, jak je předat
OpenShiftu, aby o nich věděl. Kromě přístupu přes git můžete k aplikaci
přistupovat i přes ssh. Konfigurační soubor s API klíči tak můžete nakopírovat
do adresáře k tomu určenému (ten je soukromý, vidíte ho jen vy):

    scp auth.cfg 123456789123456789123456@flask-hroncok.rhcloud.com:app-root/data/

Z aplikace k němu přistoupíte třeba takto:

```python
import os

authfile = 'auth.cfg'

if 'OPENSHIFT_DATA_DIR' in os.environ:
    authfile = os.path.join(os.environ['OPENSHIFT_DATA_DIR'], authfile)
```

Stejnou složku použijte, bude-li vaše aplikace potřebovat nějaké trvalé
úložiště pro zapisování dat (databázím se zde věnovat nebudeme).

**Poznámka:** Doporučujeme pro tyto potřeby stejně raději nepoužívat API klíče
k vlastním účtům, raději si vyrobte nějaké účty pouze pro tento účel.
Twitter vyžaduje před vydáním API klíčů zadání a potvrzení telefonního čísla.

Úkol
----

Vaším úkolem za 5 bodů je vytvořit rozšířit command line aplikaci z minulého
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

Výslednou aplikaci nasaďte na OpenShift.
Odkaz na běžící aplikaci a repozitář nám pošlete e-mailem.
V repozitáři prosím nastavte tag `v0.2`.
Termín odevzdání je začátek příštího cvičení (dřívější paralelky).

### Twitter Wall

Konzole není pro Twitter Wall dostatečně vhodné médium,
doplňte do aplikace webový frontend, který bude zobrazovat
výsledky hledání. Hledaný pojem by měl jít zadat pomocí URL.

Pro plný počet bodů  musí rozhraní zobrazovat avatary uživatelů
a zpracovávat [entity] jako obrázky, odkazy a hash tagy.

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
