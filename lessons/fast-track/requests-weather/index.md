# Stahování z internetu a API

Část těchto materiálů pochází z [jiného kurzu PyLadies](https://naucse.python.cz/2019/brno-jaro-knihovny/beginners/kurzovni-listek/).

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

Zkuste si vypsat, co obsahují atributy `response.text`, `response.status_code`.
Taky vyzkoušejte zavolat metodu `response.json()`. Existuje jich mnohem více,
ale tyto jsou docela zajímavé a
relativně často užívané.

Pojďme se tedy podívat, co dělají zmíněné jednotlivé atributy:

Atribut `text` obsahuje tělo odpovědi, tak jak nám ze serveru přišla. Pro
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

> [note]
> <https://httpbin.org/> je velice užitečná služba, pokud si potřebujete
> vyzkoušet komunikaci přes HTTP. Bude vám odpovídat na všemožné požadavky
> podle toho, jak si řeknete. Podívejte se v prohlížeči a uvidíte docela pěkný
> seznam všech možností (akorát v angličtině)

Nakonec nám zůstává metoda `json()`. JSON je datový formát, který používá mnoho
různých webových služeb. Proto `requests` nabízí tuto zkratku, jak se k datům
dostat. Ale pozor! Pokud v odpovědit nejsou data v tomto formátu, dostanete
chybu!


## Kurzy měn

Začneme zvolna - zkusíme si stáhnout aktuální kurzy měn, které poskyuje [Česká
národní banka](https://www.cnb.cz/) na adrese:

Výstup pro lidi:

https://www.cnb.cz/cs/financni-trhy/devizovy-trh/kurzy-devizoveho-trhu/kurzy-devizoveho-trhu/

Výstup pro vývojáře:

https://www.cnb.cz/cs/financni-trhy/devizovy-trh/kurzy-devizoveho-trhu/kurzy-devizoveho-trhu/denni_kurz.txt




# Příklad: Jaké bude počasí v Brně?

Vyzkoušíme si napsat program, který nám dokáže zjistit předpověď počasí v námi
vybraném městě.

Co k tomu budeme potřebovat? Znalosti o proudění vzduchu, historická data,
srážky... tak ty to nejsou. Ta už pro nás naštěstí připravili jiní lidé a tyto
informace volně poskytují na internetu. Zbývá tedy se jich akorát správně doptat.


## OpenWeathermap API

Existuje mnoho služeb pro vývojáře, které poskytují data o počasí ve strojově
čitelné formě. Jedním z nich je například [OpenWeatherMap](https://openweathermap.org/)

### Přístup ke službě

Data jsou přístupná pro kohokoli volně, jen je třeba poskytovateli dát vědět, že
je používáte zrovna vy. Častým způsobem této indentifikace je pomocí tzv.
*tokenu*, což není nic jiného, než náhodně vygenerovaný řetězec znaků, který
nahrazuje zadávání uživatelského jména a hesla. Každý uživatel má token jiný.

Zařiď si tedy účet na https://home.openweathermap.org


Na webu si udělej registraci (Sign Up) - stačí zatrhnout potvrzení, že jste
starší 16 let a že souhlasíte s podmínkami použití této služby.

Po odeslání pak na stránce *API keys* najdeš v kolonce *Key* řetězec podobný
tomuto (může to trvat několik minut, než ti pak reálně povolí přístup k datům):
```
1faf9fd2f2d64a383e7c0011fa127956
```

Tento řetězec použijeme pro všechny tvé požadavky na získání dat. Kvůli limitům
používání této služby si ale nechej vygenerovat vlastní token. Uvedený výše je
už neplatný.

## Dotaz na počasí

V [dokumentaci](https://openweathermap.org/forecast5#JSON) k API se podíváme,
jak má požadavek vypadat a jaké parametry můžeme předat. 

```python
import requests

token = '1faf9fd2f2d64a383e7c0011fa127956'
url = 'http://api.openweathermap.org/data/2.5/forecast'

parametry = {
    'APIKEY': token,
    'q': 'brno',
    'units': 'metric'
}

odpoved = requests.get(url, params=parametry)
```

Server poskytuje data ve formátu JSON, který je velmi rozšířený a knihovna `requests` pro něj má metodu, která odpověď převede na slovník.

```python
predpoved = odpoved.json()
```

V dokumentaci se dočteme s jakou strukturou máme tu čest. Nejsnazší je však si
ji rovnou vypsat. Vypadá přibližně takto:

```
{'cod': '200',
 'message': 0.0094,
 'cnt': 40,
 'list': [{'dt': 1557122400,
   'main': {'temp': 4.95,
    'temp_min': 4.05,
    'temp_max': 4.95,
    'pressure': 1015.8,
    'sea_level': 1015.8,
    'grnd_level': 958.41,
    'humidity': 74,
    'temp_kf': 0.9},
   'weather': [{'id': 600,
     'main': 'Snow',
     'description': 'light snow',
     'icon': '13d'}],
   'clouds': {'all': 90},
   'wind': {'speed': 5.63, 'deg': 341.687},
   'snow': {'3h': 0.125},
   'sys': {'pod': 'd'},
   'dt_txt': '2019-05-06 06:00:00'},
  {'dt': 1557133200,
   'main': {'temp': 8.92,
    'temp_min': 8.25,
    'temp_max': 8.92,
    'pressure': 1015.93,
    'sea_level': 1015.93,
    'grnd_level': 959,
    'humidity': 57,
    'temp_kf': 0.67},
   'weather': [{'id': 804,
     'main': 'Clouds',
     'description': 'overcast clouds',
     'icon': '04d'}],
   'clouds': {'all': 94},
   'wind': {'speed': 5.99, 'deg': 344.69},
   'sys': {'pod': 'd'},
   'dt_txt': '2019-05-06 09:00:00'},
   ...
```

Nás budou nejvíce zajímat klíče `temp` (údaj o teplotě) a `dt_txt` (tzv. časové
razítko).

Vypíšeme si je jednoduše pod sebe.

```python
for vzorek in predpoved['list']:
    datum = vzorek["dt_txt"]
    teplota = vzorek['main']['temp']

    print(f'{datum} {teplota}')
```

Takto dostaneme:

```
2019-05-06 06:00:00 6.24
2019-05-06 09:00:00 9.69
2019-05-06 12:00:00 9.96
2019-05-06 15:00:00 9.64
2019-05-06 18:00:00 6.2
2019-05-06 21:00:00 3
2019-05-07 00:00:00 0.62
...
```

V řadě číslech se ale moc dobře neorientuje. Proto si z nich uděláme jednoduchý
textový graf. Zkus si výstup upravit tak, aby se za každý stupeň vypsala jedna
tečka (3 stupně `...`, 10 stupňů `..........`).

> [note]
> Pro zjednodušení se teďka nebudeme trápit s mrazy (zápornou teplotou) - nad
> tím se můžeš zamyslet potom doma.

{% filter solution %}
```python
for vzorek in predpoved['list']:
    (...)
    sloupek = '.' * int(teplota)

    print(f'{datum} {sloupek} {teplota}')
```
{% endfilter %}

Výsledek bude vypadat nějak takto:
```
2019-05-05 15:00:00 ....... 7.44
2019-05-05 18:00:00 ..... 5.26
2019-05-05 21:00:00 .... 4.41
2019-05-06 00:00:00 ... 3.68
2019-05-06 03:00:00 .. 2.55
2019-05-06 06:00:00 .... 4.85
2019-05-06 09:00:00 ........ 8.65
2019-05-06 12:00:00 ......... 9.15
2019-05-06 15:00:00 ......... 9.88
2019-05-06 18:00:00 ..... 5.92
2019-05-06 21:00:00 .. 2.11
2019-05-07 00:00:00  0.39
2019-05-07 03:00:00  -0.33
2019-05-07 06:00:00 ..... 5.25
2019-05-07 09:00:00 ......... 9.21
...
```


## Přidáváme obrázky

Zatím je naše předpověď složena stále jen z běžných ASCII znaků. Pojďme si tam
přidat i obrázky oblohy.

Součástí předpovědi je tento údaj ve formě textu, např. `Clear`, `Rain`, `Snow`,
`Clouds`. My se s tím ale nespokojíme a nahradíme si ho obrázky. Můžeme využít
například ty z Unicode tabulky http://xahlee.info/comp/unicode_weather_symbols.html

> [note]
> Písma v příkazové řádce ve Windows stále emoji umí jen ve velmi omezené míře.
> Změň si ho dočasně na `MS Gothic`, pokud ho máš nainstalované.
> Můžeš použít třeba tyto vyzkoušené znaky z UNICODE tabulky:
> ```
> SNOWFLAKE
> CLOUD
> UMBRELLA WITH RAIN DROPS
> FLOWER
> WHITE SMILING FACE
> BLACK SMILING FACE
> ```



Chceme tedy řetězec `Snow` přeložit na `❄` a napíšeme si na to funkci.

```python
def ziskej_obrazek(pocasi):
    mapovani = {
        'Snow': '\N{SNOWFLAKE}',
        'Rain': '\N{UMBRELLA WITH RAIN DROPS}',
        'Clouds': '\N{WHITE SUN WITH SMALL CLOUD}',
        'Clear': '\N{SUN WITH FACE}'
    }

    return mapovani.get(pocasi, '?')
```

Po zakomponování do kódu:
```python
for vzorek in predpoved['list']:
    datum = vzorek["dt_txt"]
    teplota = vzorek['main']['temp']
    sloupek = '.' * int(teplota)
    pocasi = ziskej_obrazek(vzorek['weather'][0]['main'])

    print(f'{datum} {pocasi} {sloupek} {teplota} \N{DEGREE CELSIUS}')
```


Finální podoba předpovědi:
```
2019-05-06 09:00:00 🌤 ........ 8.76 ℃
2019-05-06 12:00:00 ☔ ......... 9.37 ℃
2019-05-06 15:00:00 ☔ ......... 9.4 ℃
2019-05-06 18:00:00 ☔ ...... 6.3 ℃
2019-05-06 21:00:00 🌤 ... 3 ℃
2019-05-07 00:00:00 🌤  0.62 ℃
2019-05-07 03:00:00 🌞  -0.54 ℃
2019-05-07 06:00:00 🌞 ..... 5.25 ℃
2019-05-07 09:00:00 🌞 ......... 9.65 ℃
2019-05-07 12:00:00 ☔ .......... 10.72 ℃
2019-05-07 15:00:00 ☔ .......... 10.12 ℃
2019-05-07 18:00:00 ☔ ....... 7.42 ℃
2019-05-07 21:00:00 ☔ ..... 5.72 ℃
2019-05-08 00:00:00 🌤 ... 3.52 ℃
2019-05-08 03:00:00 🌤 .. 2.25 ℃
2019-05-08 06:00:00 🌤 ...... 6.39 ℃
```

Služba OpenWeatherMap umí zjistit předpověď počasí nejen pro města, ale libovolné
místo na Zemi, zadané pomocí GPS souřadnic. Pro převod názvu (např. hory) na
souřadnice se používá tzv. geocoding. Poskytovatelů této služby je opět mnoho.
Jedním z nich je například https://locationiq.com/

API můžeme kombinovat dohromady: Název místa → GPS souřadnice→ OpenWeatherMap →
teploty.
