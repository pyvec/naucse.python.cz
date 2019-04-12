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
Začneme náhodnou stránkou. Na každé stránce najdeme první vhodný odkaz a
budeme na něj pokračovat. Program skončí, až se znovu dostane na stránku, kde
už byl, nebo pokud nenajde žádný pěkný odkaz.

Není ale úplně dobrý nápad napsat velký program na první pokus. Budeme postupně
přidávat malé kousky funkcionality, abychom mohli pořád opakovaně testovat, že
všechno dělá to, co má.


### Krok 1 – kostra programu

Začneme jednoduchou kostrou, kde si v komentářích vyznačíme, co se bude dít.

```python
URL = "https://en.wikipedia.org"
START = "/wiki/Special:Random"


def stahuj(stranka):
    while True:
        # 1. Stáhni stránku
        # 2. Napiš titulek
        # 3. Vytáhni další odkaz
        break


if __name__ == "__main__":
    stahuj(START)
```


### Krok 2 – stažení stránky

První úkol: nahraďte první komentář kódem, který stáhne stránku, zkontroluje
připadné chyby a vypíše text odpovědi od serveru. Adresu stránky ke stažení
dostanete spojením proměnných `URL` a `stranka`.

Očekávané chování po tomto kroku: program vypíše dlouhý kus HTML kódu a skončí.
Při každém běhu bude výstup jiný (pracujeme s náhodnou stránkou).

{% filter solution %}
```python
import requests


URL = "https://en.wikipedia.org"
START = "/wiki/Special:Random"


def stahuj(stranka):
    while True:
        odpoved = requests.get(URL + stranka)
        odpoved.raise_for_status()
        print(odpoved.text)
        # 2. Napiš titulek
        # 3. Vytáhni další odkaz
        break


if __name__ == "__main__":
    stahuj(START)
```
{% endfilter %}


### Krok 3 – hledání titulku

Úkol: doplňte tělo funkce `najdi_titulek()` a upravte funkci `stahuj()` tak,
aby místo celé stránky vypsala jenom titulek stránky.

```python
def najdi_titulek(html):
    """Najde titulek v HTML kódu. Titulek je v elementu s identifikátorem
    `firstHeading`. Budeme předpokládat, že tento element vždycky existuje.

    Funkce vrátí titulek jako řetězec.
    """
```

Očekávané chování: program vypíše titulek náhodné stránky a skončí.

{% filter solution %}
```python
import requests
from bs4 import BeautifulSoup


URL = "https://en.wikipedia.org"
START = "/wiki/Special:Random"


def najdi_titulek(html):
    soup = BeautifulSoup(html, "html.parser")
    return soup.find(id="firstHeading").text


def stahuj(stranka):
    while True:
        odpoved = requests.get(URL + stranka)
        odpoved.raise_for_status()
        print(najdi_titulek(odpoved.text))
        # 3. Vytáhni další odkaz
        break


if __name__ == "__main__":
    stahuj(START)
```
{% endfilter %}


### Krok 4 – úklid před další funkcionalitou


V dalším kroku konečně budeme hledat odkaz na další stránku. K tomu vytvoříme
ještě jednu funkci: `najdi_odkaz()`. Ta bude velmi podobná funkci
`najdi_titulek()`.

Volání `BeautifulSoup()` je pomerně náročný výpočet, a asi ho nechceme dělat
dvakrát.

Úkoly:

1. Upravte program tak, aby se polévka elementů vytvořila už ve funkci
   `stahuj()`, a do `najdi_titulek()` se předala jako argument.
2. Vytvořte funkci `najdi_odkaz()`. Bude mít stejný argument jako
   `najdi_titulek()`. Prozatím bude vždycky vracet `None`.
3. Přidejte volání `najdi_odkaz()` do `stahuj()`. Vrácený odkaz uložte do
    proměnné `stranka`.
4. Zavolejte `break` jenom tehdy, když `stranka` je `None`
5. Na konec `while` cyklu přidejte volání `time.sleep(1)`. Nezapomeňte
    naimportovat modul `time`.

> [note]
> `time.sleep(1)` náš program zastaví na 1 sekundu po zpracování každé stránky.
> Chceme si totiž procvičit programování, ne zbytečně vytěžovat cizí servery.

Očekávané chování: žádná změna oproti předchozímu kroku.

{% filter solution %}
```python
import time

import requests
from bs4 import BeautifulSoup


URL = "https://en.wikipedia.org"
START = "/wiki/Special:Random"


def najdi_titulek(soup):
    return soup.find(id="firstHeading").text


def najdi_odkaz(soup):
    pass


def stahuj(stranka):
    while True:
        odpoved = requests.get(URL + stranka)
        odpoved.raise_for_status()

        soup = BeautifulSoup(odpoved.text, "html.parser")
        print(najdi_titulek(soup))

        stranka = najdi_odkaz(soup)
        if not stranka:
            break

        time.sleep(1)


if __name__ == "__main__":
    stahuj(START)
```
{% endfilter %}


### Krok 5 – hledání odkazů

1. Nejdříve na stránce najdeme element s atributem `class` s hodnotou
   `mw-parser-output`. To je box s hlavním textem článku.
2. V cyklu projdeme přes každý odstavec (`p`) v tomto elementu.
3. Vytiskneme odstavec.
4. Pro každý odkaz (`a`) v tomto odstavci:
5. vytiskneme tento odkaz,
6. a vytáhneme z odkazu hodnotu atributu `href` a vrátíme ji. Tady se bude
   hodit metoda `get()`.

Očekávané chování: program vytiskne titulek náhodné stránky, první odstavec na
ní, potom první odkaz v tomto odstavci. Pak vytiskne další nadpis, odstavec,
odkaz a tak dále. Nikdy neskončí. Ukončit ho bude třeba ručně klávesovou
zkratkou Ctrl-C.

{% filter solution %}
```python
import time

import requests
from bs4 import BeautifulSoup


URL = "https://en.wikipedia.org"
START = "/wiki/Special:Random"


def najdi_titulek(soup):
    return soup.find(id="firstHeading").text


def najdi_odkaz(soup):
    hlavni_text = soup.find(class_="mw-parser-output")
    for odstavec in hlavni_text.find_all("p"):
        print(odstavec)
        for odkaz in odstavec.find_all("a"):
            print(odkaz)
            return odkaz.get("href")


def stahuj(stranka):
    while True:
        odpoved = requests.get(URL + stranka)
        odpoved.raise_for_status()

        soup = BeautifulSoup(odpoved.text, "html.parser")
        print(najdi_titulek(soup))

        stranka = najdi_odkaz(soup)
        if not stranka:
            break

        time.sleep(1)


if __name__ == "__main__":
    stahuj(START)
```
{% endfilter %}


### Krok 6 – ukončení programu

Úkol: zajistíme, aby program někdy skončil. Pokud se dostaneme na stránku, kde
už jsme byli, můžeme skončit.

1. Na začátku funkce `stahuj()` si vytvořte proměnnou `navstivene`. Začne
   jako prázdná množina (`set()`).
2. Jako první věc uvnitř `while` cyklu zkontrolujte, jestli `stranka` je v
   navštívených. Pokud ano, ukončete cyklus.
3. Přidejte stránku mezi navštívené.

Očekávané chování: program bude vypisovat spoustu textu jako předtím, ale
časem by měl skončit. Pořád začíná na náhodné stránce, takže to někdy může
chvilku trvat.


{% filter solution %}
```python
import time

import requests
from bs4 import BeautifulSoup


URL = "https://en.wikipedia.org"
START = "/wiki/Special:Random"


def najdi_titulek(soup):
    return soup.find(id="firstHeading").text


def najdi_odkaz(soup):
    hlavni_text = soup.find(class_="mw-parser-output")
    for odstavec in hlavni_text.find_all("p"):
        print(odstavec)
        for odkaz in odstavec.find_all("a"):
            print(odkaz)
            return odkaz.get("href")


def stahuj(stranka):
    navstivene = set()
    while True:
        if stranka in navstivene:
            break
        navstivene.add(stranka)

        odpoved = requests.get(URL + stranka)
        odpoved.raise_for_status()

        soup = BeautifulSoup(odpoved.text, "html.parser")
        print(najdi_titulek(soup))

        stranka = najdi_odkaz(soup)
        if not stranka:
            break

        time.sleep(1)


if __name__ == "__main__":
    stahuj(START)
```
{% endfilter %}


### Krok 7 – odstranění textu v závorkách

Úkol: teď odstraníme text v závorkách. Začneme pomocnou funkci
`odstran_zavorky()`, která by se měla chovat podle přiloženého dokumentačního
komentáře.

Zavolejte tuto funkci v `najdi_odkaz()`. Jako argument jí dáte odstavec
převedený na řetězec (pomocí `str(odstavec)`). Vrácený výsledek vypíšete hned
potom, co se vypisuje odstavec.

Očekávané chování: stejné jako dřív, akorát odstavec bude vypsaný vždy dvakrát.
Poprvé tak, jak se nachází na stránce. Podruhé bez ozávorkovaných částí.

> [note]
> Vzhledem k tomu, že v tomto kroku akorát pracujeme s řetězci, můžete ho
> přeskočit a rovnou se podívat na řešení. Ale je to relativně zajímavý
> problém.


```python
def odstran_zavorky(text):
    """Odstraní uzávorkované výrazy z textu. HTML elementy mimo závorky budou
    zachované. Funkce předpokládá, že každá otevírací závorka má i uzavírací
    závorku, a že závorky a HTML elementy se nekříží.

    >>> odstran_zavorky("Ahoj (nazdar)!")
    'Ahoj !'
    >>> odstran_zavorky("<b>Ahoj</b>")
    '<b>Ahoj</b>'
    >>> odstran_zavorky("A (<i>písmeno</i>) B")
    'A  B'
    >>> odstran_zavorky("a (b (c) d) e")
    'a  e'
    """
```

{% filter solution %}
```python
import time

import requests
from bs4 import BeautifulSoup


URL = "https://en.wikipedia.org"
START = "/wiki/Special:Random"


def odstran_zavorky(text):
    # V kolika závorkách jsme vnoření. 0 = mimo závorky
    hloubka = 0
    # Jsme zrovna uvnitř nějakého HTML elementu?
    v_tagu = False
    vysledek = ""
    for znak in text:
        # Pokud jsme v nějakém elementu…
        if v_tagu:
            # …chceme zachovat veškerý text.
            vysledek += znak
            # Končí tady značka?
            if znak == ">":
                v_tagu = False
        else:
            if znak == "(":
                # Pokud vstupujeme do uzávorkovaného výrazu, jsme o jednu
                # úroveň hlouběji.
                hloubka += 1
            elif znak == ")":
                # Pokud vystupujeme, úroveň o jedna zmenšíme.
                hloubka -= 1
            elif hloubka == 0:
                # Jsme mimo závorky, chceme si znak nechat.
                vysledek += znak
                # Ale musíme zkontrolovat, jestli nevstupujeme do nějakého HTML
                # elementu.
                if znak == "<":
                    v_tagu = True

    return vysledek


def najdi_titulek(soup):
    return soup.find(id="firstHeading").text


def najdi_odkaz(soup):
    hlavni_text = soup.find(class_="mw-parser-output")
    for odstavec in hlavni_text.find_all("p"):
        print(odstavec)
        print(odstran_zavorky(str(odstavec)))
        for odkaz in odstavec.find_all("a"):
            print(odkaz)
            return odkaz.get("href")


def stahuj(stranka):
    navstivene = set()
    while True:
        if stranka in navstivene:
            break
        navstivene.add(stranka)

        odpoved = requests.get(URL + stranka)
        odpoved.raise_for_status()

        soup = BeautifulSoup(odpoved.text, "html.parser")
        print(najdi_titulek(soup))

        stranka = najdi_odkaz(soup)
        if not stranka:
            break

        time.sleep(1)


if __name__ == "__main__":
    stahuj(START)
```
{% endfilter %}


### Krok 8 – použití nové funkce

Úkol: Místo vypisování odstavce bez závorek ho znovu převeďte na značkovou
polévku. Odkazy hledejte v ní. Teď už je na čase odstranit vypisování odstavce
i odkazu.

Očekávané chování: program bude vypisovat titulky stránek a následovat odkazy
na nich. Až dojde na stránku, kde už byl (nebo kde není žádný odkaz), tak
skončí.

{% filter solution %}
```python
import time

import requests
from bs4 import BeautifulSoup


URL = "https://en.wikipedia.org"
START = "/wiki/Special:Random"


def odstran_zavorky(text):
    hloubka = 0
    v_tagu = False
    vysledek = ""
    for znak in text:
        if v_tagu:
            vysledek += znak
            if znak == ">":
                v_tagu = False
        else:
            if znak == "(":
                hloubka += 1
            elif znak == ")":
                hloubka -= 1
            elif hloubka == 0:
                vysledek += znak
                if znak == "<":
                    v_tagu = True

    return vysledek


def najdi_titulek(soup):
    return soup.find(id="firstHeading").text


def najdi_odkaz(soup):
    hlavni_text = soup.find(class_="mw-parser-output")
    for odstavec in hlavni_text.find_all("p"):
        html = odstran_zavorky(str(odstavec))
        odstavec = BeautifulSoup(html, "html.parser")
        for odkaz in odstavec.find_all("a"):
            return odkaz.get("href")


def stahuj(stranka):
    navstivene = set()
    while True:
        if stranka in navstivene:
            break
        navstivene.add(stranka)

        odpoved = requests.get(URL + stranka)
        odpoved.raise_for_status()

        soup = BeautifulSoup(odpoved.text, "html.parser")
        print(najdi_titulek(soup))

        stranka = najdi_odkaz(soup)
        if not stranka:
            break

        time.sleep(1)


if __name__ == "__main__":
    stahuj(START)
```
{% endfilter %}


### Krok 9 – filtrování pouze pěkných odkazů

Úkol: Někdy první odkaz nevede na jinou stránku (typicky odkazy na zdroje
uvedené na konci stránky). Upravte funkci `najdi_odkaz()` tak, aby vracela
adresu stránky jenom tehdy, pokud ta vracená hodnota začíná řetězecem `/wiki/`.

Očekávané chování: program se bude chovat stejně jako dřív, ale bude trochu
chytřejší v hledání správného odkazu.


### Finální řešení

Na anglické wikipedii by tento program měl poměrně spolehlivě dojít na stránku
*Philosophy*. Pokud to zkusíte s českou verzí, až tak slavné to není. Ale i tam
jsou výsledky relativně zajímavé.


{% filter solution %}
```python
import time

import requests
from bs4 import BeautifulSoup


URL = "https://en.wikipedia.org"
START = "/wiki/Special:Random"
# Česká wikipedie:
# URL = "https://cs.wikipedia.org"
# START = "/wiki/Speciální:Náhodná_stránka"


def odstran_zavorky(text):
    hloubka = 0
    v_tagu = False
    vysledek = ""
    for znak in text:
        if v_tagu:
            vysledek += znak
            if znak == ">":
                v_tagu = False
        else:
            if znak == "(":
                hloubka += 1
            elif znak == ")":
                hloubka -= 1
            elif hloubka == 0:
                vysledek += znak
                if znak == "<":
                    v_tagu = True

    return vysledek


def najdi_titulek(soup):
    return soup.find(id="firstHeading").text


def najdi_odkaz(soup):
    hlavni_text = soup.find(class_="mw-parser-output")
    for odstavec in hlavni_text.find_all("p"):
        html = odstran_zavorky(str(odstavec))
        odstavec = BeautifulSoup(html, "html.parser")
        for odkaz in odstavec.find_all("a"):
            href = odkaz.get("href")
            if href.startswith("/wiki/"):
                return href


def stahuj(stranka):
    navstivene = set()
    while True:
        if stranka in navstivene:
            break
        navstivene.add(stranka)

        odpoved = requests.get(f"{URL}{stranka}")
        odpoved.raise_for_status()

        soup = BeautifulSoup(odpoved.text, "html.parser")
        print(najdi_titulek(soup))

        stranka = najdi_odkaz(soup)
        if not stranka:
            break
```
{% endfilter %}
