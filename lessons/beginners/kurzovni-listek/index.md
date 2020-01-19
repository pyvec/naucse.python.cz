# Requests + Click

## Co je cílem tohoto cvičení?

Po projití této lekce byste měli být obeznámeni se základním použitím knihoven
`requests` a `click`. Skončíme s programem, který bude umět převádět peníze z
českých korun do jiných měn podle aktuálního kurzu.

## Předpoklady

Předpokládáme základní znalost Pythonu. Měli byste mít počítač s nainstalovaným
interpretem jazyka Python ve verzi aspoň 3.6. Pro začátek si také vytvořte nové
virtuální prostředí.

Dále se vám bude hodit základní přehled o tom, jak funguje internet, co je to
URL a podobné drobnosti. Pokud si nejste jistí, začněte [tímto shrnutím pro
začátečníky]({{ lesson_url('fast-track/http') }}).


## Requests

Začneme seznámením s knihovnou [requests]. Je to knihovna určená pro HTTP
požadavky na straně klienta. Poskytuje mnohem pohodlnější rozhraní než
standardní knihovna Pythonu.

[requests]: http://docs.python-requests.org/en/master/

Prvním krokem by měla být instalace ve virtuálním prostředí:

```console
(venv) $ python -m pip install requests
```

První pokus je ideální provádět v interaktivní konzoli Pythonu. Začneme tím, že
si naimportujeme modul `requests`. Komunikace přes protokol HTTP používá model
požadavek/odpověď (*request*/*response*). Klient tedy nejprve pošle požadavek,
a server potom odpovídá. Takto se střídají, dokud klient nemá vše, co
potřebuje, nebo nedojde k chybě.

Pro začátek se podíváme na stránku `https://example.com`.

```pycon
>>> import requests
>>> response = requests.get("https://example.com/")
>>> response
<Response [200]>
```

Takto vypsaná odpověď není příliš užitečná. To naštěstí není zase takový
problém. V proměnné `response` teď máme object, který má potřebná data uložená
v různých atributech.

Zkuste si vypsat, co obsahují atributy `response.text`, `response.status_code`,
`response.encoding` a `response.history`. Taky vyzkoušejte zavolat metodu
`response.json()`. Existuje jich mnohem více, ale tyto jsou docela zajímavé a
relativně často užívané.

Na tyto experimenty použijte dvě jiné adresy (protože `example.com` není příliž
zajímavý web).

* `https://httpbin.org/get`
* `https://httpbin.org/redirect-to?url=http://example.com&status_code=301`

> [note]
> <https://httpbin.org/> je velice užitečná služba, pokud si potřebujete
> vyzkoušet komunikaci přes HTTP. Bude vám odpovídat na všemožné požadavky
> podle toho, jak si řeknete. Podívejte se v prohlížeči a uvidíte docela pěkný
> seznam všech možností (akorát v angličtině)

Pojďme se tedy podívat, co dělají zmíněné jednotlivé atributy:

Atribut `text` obsahuje tělo odpovědi, tak jak nám oze serveru přišla. Pro
většinu stránek to bude kód v jazyku HTML, nebo v data v různých formátech.

Každá odpověď od serveru obsahuje číselný kód, který popisuje výsledek akce.
Tento kód si můžete přečíst z atributu `status_code`. `1xx` jsou informační
zprávy, na které moc často nenarazíte. `2xx` jsou úspěšné odpovědi. Někdy se
může stát, že server místo odpovědi, kterou chcete, odešle *přesměrování*. To
má podobu odpovědi s kódem `3xx`. Přímo tuto odpověď neuvidíte, protože
knihovna `requests` ví, že je to přesměrování a proto automaticky půjde na
adresu, kam vás server poslal.

Ke každému číselnému kódu existuje i texotvý popis. Ty najdete třeba na
[Wikipedii](), nebo můžete použít <https://http.cat>.

Pokud dojde k přesměrování (a může jich být i několik), můžete se podívat na
jednotlivé odpovědi v atributu `history`. Je to seznam, který bude pro každé
přesměrování obsahovat jeden objekt.

Atribut `encoding` je užitečný v případě, že vám správně nefungují české znaky
v odpovědi. Můžete se v něm podívat, co vám server tvrdí o datech, která vám
posílá.

Nakonec nám zůstává metoda `json()`. JSON je datový formát, který používá mnoho
různých webových služeb. Proto `requests` nabízí tuto zkratku, jak se k datům
dostat. Ale pozor! Pokud v odpovědit nejsou data v tomto formátu, dostanete
chybu! (A toto je očekávané chování u druhé testovací URL.)


### Parametry pro GET

Ve druhé testovací URL si můžete všimnout, že obsahuje otazník a za ním nějaké
další informace. Toto jsou parametry pro server, které mu říkají, co přesně od
něj chceme. Typický příklad ze života je vyhledávací políčko na libovolném
webu. Vyhledávaná fráze se na server stejným způsobem jako parametr.

Ruční zpracování a přilepení k samotné URL ale není úplně jednoduché. Musíte
myslet na to, že některé znaky je potřeba zakódovat. Proto `requests` poskytují
lepší možnost, jak s parametry pracovat.

Můžeme si nadefinovat slovník, kde klíče budou názvy parametrů (které obvykle
závisí na tom, co server očekává), a hodnoty budou samotná data, která chceme
posílat.


```pycon
>>> parametry = {"status_code": 301, "url": "https://example.com"}
>>> r = requests.get("https://httpbin.org/redirect-to", params=parametry)
```

V tomto případě *httpbin* potřebuje informaci o tom, kam a jak nás má
přesměrovat.

### Posílání dat

Knihovna `requests` umí data nejenom přijímat, ale i posílat. K tomu slouží
metoda `post()`.

Jendoduchý příklad je:

```pycon
>>> r = requests.post("https://httpbin.org/post", {"ahoj": "svete"})
```

V praxi bývá často potřeba řešit situaci, že server vyžaduje přihlášení. A tam
je potřeba pracovat případ od případu. Každopádně knihovna `requests` vám
umožní použít všechny obvyklé přihlašovací metody.

### Stažení velkého souboru

Jeden detail, který je poměrně snadné přehlédnout, je to, že všechny příklady
výše provedou požadavek, a potom stáhnou celou odpoveď a uloží ji v paměti
počítače. To je v pohodě, pokud to je něco relativně malého. Pokud budete
stahovat třeba video, úplně fajn to není. Proto můžete použít tento recept,
který vytvoří spojení se serverem, potom čte kousky dat po 8 kilobajtech a
rovnou je zapisuje do souboru.

```python
import requests
with requests.get("https://placekitten.com/400/600") as r:
    r.raise_for_status()
    with open("kitten.jpg", "w") as f:
        for chunk in r.iter_content(8196):
            if chunk:
                f.write(chunk)
```

Za vypíchnutí tady stojí jedna nová metoda: `raise_for_status()`. Po provedení
požadavku je potřeba zkontrolovat, jestli se nám to podařilo. Klasicky se to
dělá kontrolou hodnoty atributu `status_code`. Metoda `raise_for_status()` je
zkratka: pokud nám server vrátil nějakou chybu, tato metoda vyhodí výjimku,
kterou můžeme zpracovat. Pro úspěšnou odpověď tato metoda neědělá nic.


### Cvičení

Česká národní banka zveřejňuje denní kurzy, které je možné si stáhnout. Navíc
jsou v pěkném textovém formátu, se kterým se nám bude pěkně pracovat.

Adresa je
<http://www.cnb.cz/cs/financni_trhy/devizovy_trh/kurzy_devizoveho_trhu/denni_kurz.txt?date=01.04.2019>.
Datum je ve formátu den.měsíc.rok. Pokud datum nezadáte nebo je špatně,
dostanete poslední kurzy.

Napište si funkci, která dostane jeden argument: datum ve správném formátu
(jako řetezec). Tato funkce stáhne kurzovní lístek a vrátí data v libovolné
podobě, se kterou se nám bude dále pracovat.

Mohla by se vám hodit tato funkce, která přečte textovou odpoveď, rozseká ji na
kousky a vrátí slovník. Klíče jsou zkratky měn, hodnoty jsou kurzy.

```python
def parse_rates(text):
    hlavicka, jmena, *radky = text.splitlines()
    kurzy = {}
    for radek in radky:
        _, _, castka, mena, hodnota = radek.replace(",", ".").split("|")
        kurzy[mena] = float(castka) / float(hodnota)
    return kurzy
```

Řešení najdete na konci této stránky.


## Click

Když instalujete knihovnu, zadáváte příkaz `python -m pip install foo`. V tomto
případě `python` je název příkazu, který chcete spustit, a ostatní slova na
tomto řádku (oddělená mezerami), jsou argumenty tohoto příkazu.

Dříve nebo později narazíte na to, že vaše programy budou potřebovat nějaký
vstup od uživatele. Číst je vždy přes funkci `input()` není úplně pohodlné ani
pro uživatele, ani pro programátora. Proto je dobré vědět, jak definovat a
používat argumenty.

Existuje hodně knihoven, které umožňují zpracovávat argumenty na příkazové
řádce. Jenom samotná standardní knihovna Pythonu má `getopt`, `optparse` a
`argparse`. Ty ale nejsou úplně příjemné na používání.

Oproti tomu knihovna [click] poskytuje rozhraní, ve kterém můžete jednoduché
programy sekat jako Baťa cvičky. Cenou je lehce magický způsob, jak argumenty
definovat, a taky ztráta možnosti ovlivnit do nejjemnějších detailů, jak se
program má chovat. To ale obvykle není problém.

[click]: https://click.palletsprojects.com/en/7.x/

### Trocha teorie

Různé systémy používají různé konvence, jak by měly argumenty vypadat a
fungovat. Tady si popíšeme, jak se slušně vychované programy chovají na Linuxu
(nebo na Macu).

Existují dvě základní kategorie: argumenty a přepínače. Argumenty jsou většinou
(ale ne vždy) vyžadované, přepínače obvykle potřeba nejsou. Argumenty jsou dané
pořadím (pokud jich je víc), přepínače mají jména.

Jména přepínačů obvykle začínají dvěmi pomlčkami, pokud mají hezké čitelné
jméno, nebo jednou pomlčkou, pokud je to jenom jedno písmeno. Dost často jeden
přepínač může mít jak jednopísmenné jméno, tak i delší a čitelnější.


### Instalace

Nic překvapivého:

```console
(venv) $ python -m pip install click
```

### Hello world

Na tomto jednoduchém programu si ukážeme, jak se dá funkce změnit v něco, co
bude pěkně použitelné na příkazové řádce.

```python
import click

@click.command()
@click.option("--kolikrat", default=1, help="Kolikrát budeme zdravit")
@click.option("--jmeno", prompt="Tvoje jméno",
              help="Koho budeme zdravit")
def hello(kolikrat, jmeno):
    for x in range(kolikrat):
        click.echo(f"Ahoj {jmeno}!")


if __name__ == "__main__":
    hello()
```

Funguje to takto:

```console
(venv) $ python hello.py --kolikrat 3 --jmeno Adame
Ahoj Adame!
Ahoj Adame!
Ahoj Adame!
```

Příkazům začínajícím zavináčem před definicí funkce říkáme dekorátory. Je to
možnost, jak v Pythonu můžeme ovlivnit chování funkce (a pravděpodobně se jim
budeme věnovat trochu více v některé následující lekci).

První řádek `@click.command()` říká, že následující funkce by se měla chovat
jako příkaz.

Další dva řádky definují přepínače tohoto příkazu.

První z nich se jmenuje `--kolikrat`, a pokud ho nezadáme, dostane výchozí
hodnotu 1. *Click* z této výchozí hodnoty pozná, že hodnotou toho přepínače
bude vždy číslo. Takže když zkusíme zadat jiný text, dostaneme chybu. Argument
předaný do funkce `hello()` bude už typu `int`.

Druhý argument bude jméno. Typ nijak nespecifikuje, takže to bude řetězec.
`prompt` říká, že pokud přepínač nezadáme, program se nás zeptá.

Zkuste si s tímto programem chvilku hrát. Nezapomeňte, že *click* vypíše pěknou
nápovědu, pokud program spustíte s přepínačem `--help`.


### Další možnosti


Možné typy přepínačů (použití: `@click.option(…, type=click.X, …`):

 * `click.INT` – celé číslo
 * `click.FLOAT` – číslo s desetinnou tečkou
 * `click.FILE` – název souboru na příkazové řádce, ale funkce už dostane
   otevřený soubor a *click* se sám postará i o zavření

Další možnosti jsou třeba `multiple=True`. Tím přepínač změníme tak, že ho bude
možné zadávat několikrát. Funkce potom dostane n-tici hodnot.

Argumenty se definují velmi podobně jako přepínače. Jediný rozdíl je v použitém
dekorátoru `@click.argument()`. Jména argumentů se zadávají bez úvodních
pomlček.

*Click* taky umožňuje vypisování na výstup. `click.echo` se chová velmi podobně
jako `print`, akorát se snaží lépe fungovat, pokud máte rozbitý terminál.


### Cvičení

Napište program, který bude vypisovat tuto nápovědu:

```console
(venv) $ python cnb.py --help
Usage: cnb.py [OPTIONS] CASTKA

Options:
  --datum TEXT
  --mena TEXT  může být zadaný vícekrát
  --help       Show this message and exit.
```


## Dokončení programu

Zkombinujte výsledky obou cvičení do jednoho programu. Tento program bude
vyžadovat jedno číslo. To bude částka v korunách. Program načte buď kurzy podle
zadaného data, nebo poslední zveřejněné.

Pokud nebude zadaná žádná měna, program převede částku do všech dostupných měn
a vypíše je v nějakém pěkném formátu. Pokud budou nějaké měny zadané, bude
převádět jen do nich.


## Řešení

Zkus si ale cvičení nejdřív vyřešit bez pomoci :)

```python
import click
import requests


def parse_rates(text):
    hlavicka, jmena, *radky = text.splitlines()
    kurzy = {}
    for radek in radky:
        _, _, castka, mena, hodnota = radek.replace(",", ".").split("|")
        kurzy[mena] = float(castka) / float(hodnota)
    return kurzy


def get_exchange_rates(datum=None):
    parametry = {}
    if datum:
        # Pokud máme datum, použijeme ho. Prázdný slovník parametrů nemá na
        # výsledek žádný vliv.
        parametry["date"] = datum
    response = requests.get(
        "http://www.cnb.cz/cs/financni_trhy/devizovy_trh/kurzy_devizoveho_trhu/denni_kurz.txt",
        params=parametry,
    )
    return parse_rates(response.text)


@click.command()
@click.option("--datum")
@click.option("--mena", multiple=True)
@click.argument("castka", type=click.FLOAT)
def cnb(castka, datum, mena):
    kurzy = get_exchange_rates(datum)
    for zkratka_meny in sorted(kurzy):
        # Pokud nemáme žádné měny, nebo tato měna byla zadaná …
        if not mena or zkratka_meny in mena:
            # … tak převedeme částku a vypíšeme ji.
            prevedeno = castka * kurzy[zkratka_meny]
            click.echo(f"{castka} CZK = {prevedeno} {zkratka_meny}")


if __name__ == "__main__":
    cnb()
```
