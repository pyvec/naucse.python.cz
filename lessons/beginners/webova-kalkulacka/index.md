# Webová kalkulačka

## Co je cílem tohoto cvičení?

Na tomto příkladu si vyzkoušíme použít knihovnu Flask na vytvoření jednoduché
webové aplikace.


## Předpoklady

Předpokládáme základní znalost Pythonu. Měli byste mít počítač s nainstalovaným
interpretem jazyka Python ve verzi aspoň 3.6. Pro začátek si také vytvořte nové
virtuální prostředí.

Dále se vám bude hodit základní přehled o tom, jak funguje internet, co je to
URL a podobné drobnosti. Pokud si nejste jistí, začněte [tímto shrnutím pro
začátečníky]({{ lesson_url('fast-track/http') }}).


## Krok 0 – kostra programu

Pro tento příklad si vystačíme s jedním zdrojovým souborem pro Python, ale bude
potřebovat i několik dalších souborů se šablonami.

Zkopírujte si tyto soubory do libovolného adresáře. Šablona musí být v
podadresáři `templates/`. Zkuste program spustit pomocí `flask run`
(nezapomeňte nejdřív nastavit proměnnou `FLASK_APP=kalk.py`).

Výsledkem by měl být jednoduchý formulář, kam můžeme zadat dvě čísla a potom
vybrat jednu ze čtyř operací.

```python
# kalk.py
from flask import Flask, render_template


app = Flask(__name__)


@app.route("/")
def index():
    return render_template("kalkulacka.html")
```

```html+jinja
{% raw -%}
# templates/kalkulacka.html
<html>
    <head>
        <title>Kalkulačka</title>
    </head>
    <body>
        <h1>Kalkulačka</h1>
        <form method="POST" action="{{ url_for("index") }}">
            <label for="prvni">První číslo</label>
            <input type="text" name="prvni">
            <label for="druhe">Druhé číslo</label>
            <input type="text" name="druhe">
            <input type="submit" name="operace" value="plus">
            <input type="submit" name="operace" value="minus">
            <input type="submit" name="operace" value="krat">
            <input type="submit" name="operace" value="deleno">
        </form>
    </body>
</html> 
{% endraw %}
```


## Zpracování formuláře

Pokud teď vybereme některou z operací, dostaneme chybu. Naše kalkulačka zatím
nevím, že by měla zpracovávat i požadavky metodou `POST` (která se používá pro
odeslání formuláře). Napravíme to přidáním argumentu do dekorátor, kde
nastavíme `methods` na seznam s hodnotami `GET` a `POST`.

{% filter solution %}
```python
@app.route("/", methods=["GET", "POST"])
def index():
    …
```
{% endfilter %}

Teď už formulář umíme přijmout, ale zatím se kalkulačka pořád chová, jako by
uživatel chtěl jenom zobrazit formulář. Která metoda byla použitá,
poznáme z atributu `method` objektu `request`, který potřeba nejdříve
naimportovat.

Přidejte tento import, a upravte funkci, tak, aby při metodě `POST` vypsala
nějakou informativní hlášku. Také si můžeme vypsat atribut `form`, který
obsahuje data z formuláře.

{% filter solution %}
```python
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("kalkulacka.html")
    elif request.method == "POST":
        print(request.form)
        return "Dostali jsme data"
```
{% endfilter %}

`request.form` se chová jako slovník, ze kterého můžeme vytáhnout hodnoty. Naše
šablona definuje klíče `prvni`, `druhe` a `operace`. První dva jsou čísla,
poslední je jméno požadované operace. Všechna data ale dostaneme jako řetězce.

Spočítejte výsledek požadované operace a zobrazte ho v prohlížeči. Návratová
hodnota z funkce musí být řetězec nebo komplikovanější objekt.

{% filter solution %}
```python
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("kalkulacka.html")
    elif request.method == "POST":
        prvni = int(request.form["prvni"])
        druhe = int(request.form["druhe"])
        operace = request.form["operace"]

        if operace == "plus":
            vysledek = prvni + druhe
        elif operace == "minus":
            vysledek = prvni - druhe
        ...

        return str(vysledek)
```
{% endfilter %}

Teď už bychom měli mít téměř funkční kalkulačku.

Dlouhá řada podmínek sice funguje, ale je to docela ukecané řešení. Můžeme ho
zkusit zkrátit. Python nemá konstrukci typu `switch` nebo `case`. Můžeme ale
trochu podvádět a použít slovník. Klíči budou názvy operací, hodnotami funkce,
které danou operaci provádí.

```python
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("kalkulacka.html")
    elif request.method == "POST":
        vsechny_operace = {
            "plus": lambda x, y: x + y,
            "minus": lambda x, y: x - y,
            "krat": lambda x, y: x * y,
            "deleno": lambda x, y: x / y,
        }
        prvni = int(request.form["prvni"])
        druhe = int(request.form["druhe"])
        operace = request.form["operace"]

        fce = vsechny_operace[operace]
        vysledek = fce(prvni, druhe)
        return str(vysledek)
```

Pro další pokračování příkladu můžete použít libovolnou variantu.

Jako další krok by bylo fajn zobrazit výsledek pomocí šablony v pěkně čitelném
formátu.

Zkopírujte si šablonu `kalkulacka.html` do souboru `vysledek.html` a upravte ho
tak, aby zobrazoval obě zpracovaná čísla, použitou operaci a výsledek.

{% filter solution %}
```python
# kalk.py
@app.route("/", methods=["GET", "POST"])
def index():
        vsechny_operace = {
            "plus": ("+", lambda x, y: x + y),
            "minus": ("-", lambda x, y: x - y),
            "krat": ("×", lambda x, y: x * y),
            "deleno": ("÷", lambda x, y: x / y),
        }
        prvni = int(request.form["prvni"])
        druhe = int(request.form["druhe"])
        operace = request.form["operace"]
        op, fce = vsechny_operace[operace]
        vysledek = fce(prvni, druhe)
        return str(vysledek)
```

```html+jinja
# templates/vysledek.html
{% raw -%}
<html>
    <head>
        <title>Kalkulačka</title>
    </head>
    <body>
        <h1>Kalkulačka</h1>
        <p>
        {{ prvni }} {{ symbol }} {{ druhe }} = {{ vysledek }}
        </p>
    </body>
</html>
{% endraw %}
```
{% endfilter %}

Další drobná potíž s naší kalkulačkou je v tom, že se těžko vrací na zadání
dalšího výpočtu ze stránky s výsledky. To můžeme opravit přidáním odkazu na
stránku s výsledkem. Přidejte ještě jeden odstavec, ve kterém bude odkaz na
formulář.

Místo zadávání adresy natvrdo jako `"/"` je lepší použít funkci
`url_for("index")`, která bude fungovat i tehdy, až se rozhodneme adresu
změnit. Potom nám bude stačit změnit dekorátor na jednom místě.

{% filter solution %}
```html+jinja
# templates/vysledek.html
{% raw -%}
<html>
    <head>
        <title>Kalkulačka</title>
    </head>
    <body>
        <h1>Kalkulačka</h1>
        <p>
        {{ prvni }} {{ symbol }} {{ druhe }} = {{ vysledek }}
        </p>
        <p>
        <a href="{{ url_for('index') }}">Další výpočet</a>
        </p>
    </body>
</html>
{% endraw %}
```
{% endfilter %}


## Ošetření chyb

Zkuste si, co se stane při zadání vstupů, které nejsou čísla. Měli bychom dostat
dlouhou chybovou stránku, která obsahuje příliš mnoho detailů, které určitě
nechceme ukazovat uživatelům. Upravte program tak, aby zachytil výjimku, a
zavolal funkci `abort` s argumentem `400`. Tím prohlížeči (nebo jinému
programu) řekneme, že zadal nesprávná data.

{% filter solution %}
```python
        ...
        try:
            prvni = int(request.form["prvni"])
            druhe = int(request.form["druhe"])
        except ValueError:
            abort(400)
        operace = request.form["operace"]
        ...
```
{% endfilter %}

Teď dostaneme kratší chybovou stránku. Co kdybychom ji ale chtěli změnit?

Můžeme na to použít nový dekorátor: `errorhandler`. Takto označená funkce bude
zavolaná vždycky, když dojde dojde k zavolání `abort(400)`. Stejně dobře bychom
ale mohli ošetřit jakoukoli jinou výjimku. Z této funkce můžeme třeba vrátit
hezky naformátovanou chybu.

```python
@app.errorhandler(400)
def spatny_pozadavek(chyba):
    return "Tohle nejde počítat", 400
```

Zkuste si přidat další chybovou stránku pro chybu 404: vyzkoušet ji můžete
zadáním nesmyslné adresy do prohlížeče. Třeba
<http://127.0.0.1:5000/neexistuju>.


## Zjednodušení šablon

Momentálně naše aplikace používá dvě šablony. Obě mají velmi podobnou
strukturu, liší se pouze několika málo detaily uvnitř.

Této duplicity by bylo dobré se zbavit.

K tomu můžeme použít systém založený na dědičnosti šablon.

Vytvoříme si novou šablonu, která obsahuje společné části.

```html+jinja
# templates/base.html
{% raw -%}
<!DOCTYPE html>
<html>
    <head>
        <title>Kalkulačka</title>
    </head>
    <body>
        <h1>{% block titulek %}Kalkulačka{% endblock titulek %}</h1>
        {% block obsah %}
        {% endblock %}
    </body>
</html>
{% endraw %}
```

Další šablony potom budou definovat blok pojmenovaný `obsah`. Ten se vloží na
příslušné místo. Stejně tak můžeme nadefinovat `titulek`. Pro ten ale máme
výchozí hodnotu.

```html+jinja
# templates/kalkulacka.html
{% raw -%}
{% extends "base.html" %}

{% block titulek %}
Moje kalkulačka
{% endblock %}

{% block obsah %}
<form method="POST" action="{{ url_for("index") }}">
    <label for="prvni">První číslo</label>
    <input type="text" name="prvni">
    <label for="druhe">Druhé číslo</label>
    <input type="text" name="druhe">
    <input type="submit" name="operace" value="plus">
    <input type="submit" name="operace" value="minus">
    <input type="submit" name="operace" value="krat">
    <input type="submit" name="operace" value="deleno">
</form>
{% endblock %}
{% endraw %}
```

Na začátku nadefinujeme, že tato šablona rozšiřuje šablonu jménem `base`. Potom
nadefinujeme vlastní titulek a nakonec samotný blok s obsahem stránky.

Zkuste podle stejného vzoru zjednodušit šablonu pro výsledek.
