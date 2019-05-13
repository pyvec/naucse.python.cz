# Webový server - rozhraní k piškvorkám

Tato lekce navazuje na dřívější úkoly - 1D piškvorky. Pokud je nemáš udělané,
můžeš použít ukázkové následující soubory.

Soubor `util.py` musí obsahovat funkci `tah(pole, index, symbol)`, která se
pokusí umístit hráčův symbol do zadaného hracího pole a vrací nový stav hracího
pole (neúspěch je indikován vyvoláním výjimky `ValueError`). Může vypadat
například takto:
{% filter solution %}
```python
# util.py
def tah(pole, index, symbol):
    if index >= len(pole) or index < 0:
        raise ValueError
    if pole[index] != '-':
        raise ValueError
    if symbol not in ('x', 'o'):
        raise ValueError

    return pole[:index] + symbol + pole[index + 1:]


def vyhodnot(pole):
    if 'xxx' in pole:
        return 'x'
    if 'ooo' in pole:
        return 'o'
    if '-' not in pole:
        return '!'
    return '-'
```
{% endfilter %}

Podobně s `ai.py`. Ten musí obsahovat funkci `tah_pocitace(pole, symbol)`, který
se pokusí umístit zadaný symbol do hracího pole, vrací nový stav hracího pole.
použít velmi naivní strategii:
{% filter solution %}
```python
# ai.py
from random import randrange
from util import tah

def tah_pocitace(pole, symbol):
    delka = len(pole)

    while True:
        try:
            index = randrange(0, delka)
            return tah(pole, index, symbol)
        except ValueError:
            pass
```
{% endfilter %}


# První seznámení se serverem

Pro webový server dneska použijeme knihovnu `flask`. Již tradičně, nejprve si ji
nainstalujeme:

```bash
(venv) $ python -m pip install flask
```

Začneme s jednoduchou kostrou:
```python
# webpiskvorky.py
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hra():
    jmeno_zvirete = 'Andulka na bidýlku'

    return f'Ahoj, jmenuju se {jmeno_zvirete}.'
```

## Spuštění serveru

Aplikace ve Flasku se spouští trochu jinak, než programy, které jsme si doposud
napsali.  Nejprve je nutné nastavit několik proměnných prostředí a to se dělá na
různých počítačích jiným způsobem.

V linuxu/Mac:
```bash
$ export FLASK_APP=webpiskvorky.py
$ export FLASK_DEBUG=1
```

Pokud pracuješ na Windows:
```bash
> set FLASK_APP=webpiskvorky.py
> set FLASK_DEBUG=1
```

Tak, tím máme nachystané prostředí a konečně můžeme server spustit:
```bash
(venv) $ flask run
 * Serving Flask app "webpiskvorky.py" (lazy loading)
 * Environment: production
   WARNING: Do not use the development server in a production environment.
   Use a production WSGI server instead.
 * Debug mode: on
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 279-218-554
```

Otevři si v prohlížeči stránku http://127.0.0.1:5000 a mělo by se ti zobrazi
prázdná stránka pouze s textem
```
Ahoj, jmenuju se Andulka na bidýlku.
```

## Šablona

Psaní obsahu stránky přímo v pythonu je docela nepohodlné. Proto využijeme tzv.
šablon. To je soubor, do kterého ve kterém se dají nahradit proměnné za jejich
hodnoty.

Ve stejné složce, jako se nachází soubor `webpiskvorky.py` vytvoříme novou
složku `templates` a v ní následující `piskvorky.html`:

{% raw %}
Soubor `templates/piskvorky.html`:
```html
<!DOCTYPE html>
<html>
    <head>
        <title></title>
        <meta charset="utf-8">
    </head>
    <body>
        Ahoj, jmenuju se {{ jmeno }}
    </body>
</html>
```
{% endraw %}

Nyní upravíme naši funkci tak, abychom šabloně předali proměnné a výsledný obsah
vrátili jako odpověd serveru.

```python
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def hra():
    jmeno_zvirete = 'Andulka na bidýlku'

    return render_template('piskvorky.html', jmeno=jmeno_zvirete)
```

Pojmenovaný argument funkce `render_template` uvnitř šablony vezme jako název
proměnné uvnitř šablony. Hodnotu proměnné v šabloně vypíšeme pomocí dvojitých
složených závorek.













## Výsledná aplikace

{% filter solution %}
```python
# webpiskvorky.py

# Spouštění (v příkazové řádce):
# export FLASK_APP=webpiskvorky.py
# export FLASK_DEBUG=1
# flask run

# (na Windows "set" místo "export")

from flask import Flask, render_template, request

from util import tah
from ai import tah_pocitace

app = Flask(__name__)

@app.route('/')
def hra():
    if 'pole' in request.args:
        pole = request.args['pole']
    else:
        pole = '-' * 20
    if 'cislo' in request.args:
        cislo_policka = int(request.args['cislo'])
        pole = tah(pole, cislo_policka, 'x')
        pole = tah_pocitace(pole, 'o')

    return render_template(
        'hra.html',
        ocislovane_pole=enumerate(pole),
        pole=pole,
    )
```

{% raw %}
```html
<!DOCTYPE html>
<html>
    <head>
        <title>Piškvorky</title>
        <meta charset="utf-8">
    </head>
    <body>
        <h1>Piškvorky</h1>
        <form>
            <input type="hidden" name="pole" value="{{ pole }}">
            <div>
                {% for cislo, znak in ocislovane_pole %}
                    {% if znak == '-' %}
                        <input type="radio" name="cislo" value="{{ cislo }}">
                    {% else %}
                        {{ znak }}
                    {% endif %}
                {% endfor %}
            </div>
            <input type="submit" value="Odeslat!">
        </form>
        <a href="{{ url_for('hra') }}">Reset</a>
    </body>
</html>
```
{% endraw %}

{% endfilter %}
