# Web Scraping

## Co je cílem tohoto cvičení?

Jak říká [XKCD #903](https://xkcd.com/903/), pokud na Wikipedii budete klikat
na první odkaz v textu článku, který není v závorkách nebo kurzívou, dříve nebo
později se dostanete na článek o filosofii.

Dneska si to ověříme v praxi. Během tohoto ověřování se naučíme používat
knihovnu [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/) a
procvičíme si [requests](http://docs.python-requests.org/en/master/).


## Předpoklady

Předpokládáme základní znalost Pythonu. Měli byste mít počítač s nainstalovaným
interpretem jazyka Python ve verzi aspoň 3.6. Pro začátek si také vytvořte nové
virtuální prostředí (na kurzu s lektorem můžete použít prostředí z [minulé
lekce]({{ lesson_url('beginners/kurzovni-listek') }}).


## Teorie do začátku

Webové stránky jsou super, pokud je čtete v prohlížečí, jako je třeba Firefox
nebo Chrome. Občas ale potřebuje vytáhnout nějaké informace, a potom s nimi
dále pracovat. Ruční kopírování je moc náročné.

Některé webové služby poskytují API, přes které je možné se k datům dostat v
nějakém civilizovaném formátu. Toto bohužel není až tak časté, a obvykle je
potřeba data vytáhnout ze samotné stránky, tak jak je určená pro prohlížeče.

Webové stránky jsou napsané v jazyku HTML. Je to značkovací jazyk, kde se míchá
text určený pro lidi se značkami (*tagy*) určenými pro prohlížeč. Tyto *tagy*
definují, jak se má text zobrazovat.


## Instalace

```console
(venv) $ python -m pip install beautifulsoup4 requests
```

Knihovna `beautifulsoup` existuje v několika verzích. My chceme tu poslední,
verzi 4. Protože hodně existujících programů pořád používá starší verzi 3, jsou
pro instalaci stále dostupné obě.


## Použití

Hodně zjednodušený pohled na knihovnu `beautifulsoup` vypadá takto: z textu
reprezentujícího HTML kód můžete vytvořit strukturu, ve které je potom možné
hledat požadované značky a pracovat s nimi.


```pycon
>>> from bs4 import BeautifulSoup
>>> soup = BeautifulSoup("<html><body><h1>Ahoj</h1></body></html>")
>>> soup
<html><body><h1>Ahoj</h1></body></html>
>>> soup.name
'[document]'
>>> soup.html.body.h1.text
'Ahoj'
>>>
```

Vyzkoušíme si nejdřív prohledávání malého dokumentu:

```pycon
>>> html_doc = """
... <html><head><title>O třech prasátkách</title></head>
... <body>
... <p class="title"><b>O třech prasátkách</b></p>
... <p class="story">Byla nebyla tři prasátka. Postavila si domky ze
... <a href="http://example.com/slama" class="material">slámy</a>,
... <a href="http://example.com/drevo" class="material">dřeva</a> a
... <a href="http://example.com/cihly" class="material">cihel</a>.
... </p>
... <p class="story">...</p>
... </body>
... </html>
... """
>>>
```

Nejdříve ho zpracujeme. Druhý argument upřesňuje, že se jedná o HTML.

```pycon
>>> soup = BeautifulSoup(html_doc, "html.parser")
>>>
```

Přístup přes název tagu už jsme viděli. Dostaneme tak první tag s daným jménem.
Můžeme se ale zeptat na všechny.

```pycon
>>> soup.a
<a class="material" href="http://example.com/slama">slámy</a>
>>> soup.find_all("a")
[<a class="material" href="http://example.com/slama">slámy</a>, <a class="material" href="http://example.com/drevo">dřeva</a>, <a class="material" href="http://example.com/cihly">cihel</a>]
>>>
```

Můžeme taky zkoumat obsah tagů:

```pycon
>>> hlavicka = soup.head
>>> hlavicka
<head><title>O třech prasátkách</title></head>
>>> hlavicka.contents
[<title>O třech prasátkách</title>]
>>> titulek = hlavicka.contents[0]
>>> titulek
<title>O třech prasátkách</title>
>>> titulek.contents
['O třech prasátkách']
>>>
```

Pokud chceme iterovat v cyklu přes všechny věci uvnitř nějakého tagu, je lepší
použít `children` než `contents`. Ušetříme si tak vytváření seznamu.

Pokud element obsahuje jenom text, můžeme se k němu dostat přes atribut `string`:

```pycon
>>> titulek.string
'O třech prasátkách'
>>>
```

Ve stromu značek se můžeme pohybovat nejenom dolů, ale i nahoru a do stran.

* `parent` – nadřazený element
* `parents` – iterátor, přes který můžeme vylézt až ke kořenovému elementu
* `next_sibling`, `previous_sibling` – skok na další nebo předchozí element,
  který má stejného rodiče (v reálném dokumentu soused většiny elementů bude
  pravděpodobně text plný mezer)


### Vyhledávání

Už jsme zmínili metodu `find_all`. Podle čeho všecho můžeme vyhledávat? Zatím
jsme viděli vyhledávání podle názvu elementu. Můžeme ale hledat i podle seznamu
elementů, případně podle regulárního výrazu.

Můžeme taky udělat `find_all(True)`. Tím dostaneme všechny elementy, ale ne
text.

Taky můžeme hledat podle funkce. Tato funkce dostane jako argument jeden
element, a pokud vrátí `True`, element bude považovaný za nalezený.

Jakýkoli pojmenovaný argument bude fungovat jako filtr na atributy elementu.
Často se hodí vyhledávat podle atributu `class`, který ale nejde použít pro
argument funkce v Pythonu. Naštěstí `class_` se dá použít jako náhrada.


## Nepraktický příklad z neživota

> [note]
> Na tomto místě je asi fajn zmínit, že na *scraping* neexistuje univerzální
> návod. Typický vývoj programu vypadá tak, že ho ladíme na datech, dokud se
> nechová rozumně. První aktualizace stránek ho typicky rozbije a můžeme začít
> ladit znovu. Je to možná ale jednodušší než se snažit vymyslet něco
> dokonalého.

Jak to bude celé fungovat: budeme postupně stahovat stránky z Wikipedie.
Začneme náhodnout stránkou. Na každé stránce najdeme první vhodný odkaz a
budeme na něj pokračovat. Program skončí, až se znovu dostane na stránku, kde
už byl, nebo pokud nenajde žádný pěkný odkaz.
