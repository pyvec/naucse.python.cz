Webové aplikace: Flask
======================

Python je víceúčelový jazyk.
V minulých lekcích jsme tvořili aplikace pro příkazovou řádku,
nyní se podíváme na aplikace webové.

Webových frameworků pro Python je více, mezi nejznámější patří [Django] nebo [Flask].
Pro naše účely použijeme [Flask], protože je nejrychlejší na pochopení.

[Django]: https://www.djangoproject.com/
[Flask]: http://flask.pocoo.org/

Flask
-----

Flask opět můžete nainstalovat do virtuálního prostředí.

```console
(__venv__) > python -m pip install Flask
```

Základní použití Flasku je poměrně primitivní.
Do souboru `hello.py` napište:

```python
# soubor hello_flask.py
# nejjednodušší Flask webová aplikace

from flask import Flask

app = Flask(__name__)
app.config['DEBUG'] = True


@app.route('/')
def index():
    """Tato funce se zavolá, když uživatel přijde
    na domovskou stránku naší aplikace.
    Vrátí řetězec, který se zobrazí v prohlížeči.
    """
    return 'Ahoj Pyladies!'


if __name__ == "__main__":
    # spustí aplikaci
    app.run()
```

Pak aplikaci spusťte následovně:

```console
(__venv__) > python hello.py
 * Serving Flask app "hello"
 * Forcing debug mode on
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 189-972-345
```
Na zmíněné adrese byste měli v prohlížeči vidět použitý text.

Tím, že jsme nastavili konfigurační hodnotu `DEBUG` jsme zapli ladícím režim,
který si popíšeme za chvíli.

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

Při povolení ladícího režimu (konfigurační proměnná `DEBUG`) zapneme příjemnější
výpis chyb a aplikace se automaticky restartuje po změnách.

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
Budete například chtít zobrazit informace o uživatelích na adresách
jako `/user/pylady/`, ale nemůžete při každé registraci nového uživatele
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

Rout můžete definovat i víc pro jednu funkci.
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
    return url_for('profile', username='pylady')
```

Tuto funkci jde použít jen uvnitř pohledové funkce,
Pokud ji chcete vyzkoušet například v interaktivní konzoli,
můžete použít speciální kontext:

```pycon
>>> with app.test_request_context():
...     print(url_for('profile', username='pylady'))
...
/user/pylady/
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
> O webových technologiích [HTML] a [CSS] se můžete dočíst více
> např. na stránkách [MDN].

[HTML]: https://developer.mozilla.org/en-US/docs/Web/HTML
[CSS]: https://developer.mozilla.org/en-US/docs/Web/CSS
[MDN]: https://developer.mozilla.org/en-US/docs/Web

HTML se dá psát přímo v Pythonu:

```python
@app.route('/')
def hello():
    return '<html><head><title>...'
```

...ale není to nebylo příliš příjemné.
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

### A další

Flask umí i další věci – například zpracování formulářů, chybové stránky nebo
přesměrování.

Všechno to najdete
[v dokumentaci](http://flask.pocoo.org/docs/1.0/quickstart/).
