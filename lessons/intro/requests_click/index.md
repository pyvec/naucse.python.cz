requests a click
================

Na úvod ověříme vaše znalosti Pythonu při použití dvou oblíbených knihoven
[requests] a [click].
Pro instalaci na školní počítače (i na svoje) můžeme využít virtualenv:

```
$ mkdir project && cd $_
$ python3 -m venv env  # vytvoření virtualenvu
$ . env/bin/activate  # aktivace
(env)$ python -m pip install requests click  # příkaz na instalaci balíčků puštěný ve virtualenvu
(env)$ ...  # práce "uvnitř"
(env)$ deactivate  # vypnutí virtualenvu
```

Pokud ještě neznáte virtualenv, vysvětlíme jej operativně na cvičení.
Jedná se o oddělené prostředí pro Python, kam se dají instalovat jednotlivé
moduly, které jsou aktivní jen uvnitř.
Pro naše potřeby si zatím vystačíme s příkladem výše.

[requests]: http://docs.python-requests.org/
[click]: http://click.pocoo.org/

requests
--------

Knihovna requests je určená pro HTTP požadavky (klienty).
Přestože vytvářet HTTP požadavky jde i bez requests, pomocí standardní knihovny
Pythonu, requests mají mnohem lidštější rozhraní a používají se mnohem
jednodušeji. Budeme předpokládat, že znáte alespoň základy HTTP protokolu a
vrhneme se rovnou na příklad:

```python
>>> import getpass
>>> import requests
>>> password = getpass.getpass()
Password: 
>>> username = 'hroncok'
>>> r = requests.get('https://api.github.com/user', auth=(username, password))
>>> r.status_code
200
>>> r.headers['content-type']
'application/json; charset=utf8'
>>> r.encoding
'utf-8'
>>> r.text
'{"login":"hroncok"...'
>>> r.json()
{'avatar_url': 'https://avatars.githubusercontent.com/u/2401856?v=3', ...}
```

Příklady použití pro další HTTP metody najdete v [dokumentaci].

[dokumentaci]: http://docs.python-requests.org/en/master/user/quickstart/

### Použití session

Hlavně v budoucnu se nám bude hodit použití tz. session.
Session využívá na pozadí jedno otevřené HTTP spojení a poskytuje tak
při více sousledných požadavcích výrazné zrychlení.

Kromě jiného session automaticky ukládá cookies a je možné ji nastavit výchozí
hlavičky.

```python
>>> session = requests.Session()
>>> session.get('http://httpbin.org/cookies/set/mipyt/best')
<Response [200]>
>>> r = session.get('http://httpbin.org/cookies')
>>> r.json()
{'cookies': {'mipyt': 'best'}}
```

### Twitter API

Pro reálné použití si ukážeme, jak se dá pomocí requests získat seznam tweetů.
Z Twitteru nebudeme samozřejmě nic parsovat, ale použijeme jejich [API].

```python
>>> r = session.get('https://api.twitter.com/1.1/search/tweets.json')
>>> r.json()
{'errors': [{'code': 215, 'message': 'Bad Authentication data.'}]}
```

Jak můžete vidět v odpovědi, Twitter API neumožňuje data číst bez autentizace.
Jak se autentizovat byste při troše hledání našli v dokumentaci, ale protože
nevyučujeme úvod do OAuthu, ale Python, rozhodli jsme se vám to zjednodušit.

Po přihlášení na Twitter (pokud nemáte, můžete si vytvořit nějaký dummy účet)
jděte na [apps.twitter.com] a vytvořte aplikaci (URL si můžete vymyslet).
Po vytvoření najdete na kartě *Keys and Access Tokens* API Key a API Secret.
Nemusíme doufám zdůrazňovat, že se jedná prakticky o hesla k vašemu
Twitter účtu, a proto by je nikdo kromě vás neměl vidět.

Prozatím je nastavte do proměnných, později je schováme například do
konfiguračního souboru.

```python
>>> api_key = 'D4HJp6PKmpon9eya1b2c3d4e5'
>>> api_secret = 'rhvasRMhvbuHJpu4MIuAb4WO50gnoQa1b2c3d4e5f6g7h8i9j0'
```

Tyto kódy je potřeba určitým způsobem slepit a poslat Twitteru,
aby vytvořil token, které pak půjde použít pro API.

```python
>>> import base64
>>> secret = '{}:{}'.format(api_key, api_secret)
>>> secret64 = base64.b64encode(secret.encode('ascii')).decode('ascii')
>>> headers = {
...     'Authorization': 'Basic {}'.format(secret64),
...     'Host': 'api.twitter.com',
... }
>>> r = session.post('https://api.twitter.com/oauth2/token',
...                  headers=headers,
...                  data={'grant_type': 'client_credentials'})
>>> 
>>> r.json()
{'token_type': 'bearer', 'access_token': 'AAAAAAAAAAAAAAAAAAAAAHhKXAAAAAAAaA1abB2bcC3cdD4deE5efF6fgG7ghH8hiI9ijJ0ja1b2c3d4e5f6g7h8i9j0a1b2c3d4e5f6g7h8i9j0'}
>>> bearer_token = r.json()['access_token']
```

Pro komunikaci s Twitter API je třeba přidat hlavičku se získaným tokenem,
využijeme faktu, že používáme session a nastavíme autentizační funkci:

```python
>>> def bearer_auth(req):
...     req.headers['Authorization'] = 'Bearer ' + bearer_token
...     return req
... 
>>> session.auth = bearer_auth
```

Pak už by mělo API fungovat:

```python
>>> r = session.get(
...     'https://api.twitter.com/1.1/search/tweets.json',
...     params={'q': '#python'},
... )
>>> for tweet in r.json()['statuses']:
...     print(tweet['text'])
... 
Download our Guide to Python for quick hints and tips when learning to code in #Python https://t.co/sKnX7yaAKv https://t.co/cndHnBBbfh
...
```

Zde máte pro zjednodušení k dispozici funkci pro vytvoření autentizované
session:

```python
import requests
import base64

def twitter_session(api_key, api_secret):
    session = requests.Session()
    secret = '{}:{}'.format(api_key, api_secret)
    secret64 = base64.b64encode(secret.encode('ascii')).decode('ascii')

    headers = {
        'Authorization': 'Basic {}'.format(secret64),
        'Host': 'api.twitter.com',
    }

    r = session.post('https://api.twitter.com/oauth2/token',
                     headers=headers,
                     data={'grant_type': 'client_credentials'})

    bearer_token = r.json()['access_token']

    def bearer_auth(req):
        req.headers['Authorization'] = 'Bearer ' + bearer_token
        return req
    
    session.auth = bearer_auth
    return session
```

[API]: https://dev.twitter.com/rest/public
[apps.twitter.com]: https://apps.twitter.com/

### GitHub API

Podíváme se i na GitHub API, které má jednodušší autentizaci (od GitHubu přímo
získáte token). Stačí jít do [nastavení] a vyrobit nový token
(zatím není třeba zaškrtávat žádná opravnění).
Token je opět třeba patřičně chránit.

```python
>>> token = 'xxxxxxx'
>>> session = requests.Session()
>>> session.headers = {'Authorization': 'token ' + token, 'User-Agent': 'Python'}
>>> r = session.get('https://api.github.com/user')
>>> r.json()
```

Pokud chcete něco provést, například dát hvězdičku repozitáři s těmito
materiály, musíte tokenu nastavit patřičné oprávnění
(u hvězdičky je to `public_repo`).
To se dělá přes [nastavení] na GitHubu.

Hvězdičku přidáte takto:

```python
>>> r = session.put('https://api.github.com/user/starred/cvut/MI-PYT')
>>> r.text
''
```

Jak vidíte, API nevrací žádný text, můžete tedy zkontrolovat návratový status:

```python
>>> r.status_code
204
```

Případně vyhodit výjimku, pokud je stavový kód divný:

```python
>>> r.raise_for_status()
```

Pokud hvězdičku chcete odebrat, použijte metodu DELETE.
My ale věříme, že ji odebrat nechcete :)

[nastavení]: https://github.com/settings/tokens

### Chraňte své tokeny

Když ukládáte skript do gitu, mějte na paměti, že tokeny a klíče do něj nikdy
nepatří. Můžete je uložit do konfiguračního souboru, který bude gitem ignorován,
například takto:

```
[twitter]
key = D4HJp6PKmpon9eya1b2c3d4e5
secret = rhvasRMhvbuHJpu4MIuAb4WO50gnoQa1b2c3d4e5f6g7h8i9j0

[github]
token = xxxxxxx
```

```python
>>> import configparser
>>> config = configparser.ConfigParser()
>>> config.read('auth.cfg')
>>> config['twitter']['key']
D4HJp6PKmpon9eya1b2c3d4e5
```

V takovém přídě je vhodné vložit do gitu například soubor `auth.cfg.sample` s
vymyšlenými údaji, či příklad uvést v README.

click
-----

Nechme internety na chvíli být a pojďme se podívat na úplně jinou knihovnu,
[click]. Slouží opět k něčemu, co jde  v Pythonu i bez ní, ale umožňuje to
dělat příjemněji: čtení argumentů z příkazové řádky.

```python
import click

@click.command()
@click.option('--count', default=1, help='Number of greetings.')
@click.option('--name', prompt='Your name',
              help='The person to greet.')
def hello(count, name):
    """Simple program that greets NAME for a total of COUNT times."""
    for x in range(count):
        click.echo('Hello {}!'.format(name))

if __name__ == '__main__':
    hello()
```

Takto jednoduše se dá vytvořit command line aplikace s přepínači.

Úkol
----

Vaším úkolem za 5 bodů je vytvořit command line aplikaci nad vybraným webovým
API, pomocí knihoven [requests] a [click].
Hotovou aplikaci odevzdáte jako gitový repozitář na GitHubu, případně fakultním
GitLabu. V obou případech nám nezapomeňte [dát přístup](00_uvod.md).

Nebráníme se veřejným repozitářům, ale neradi bychom viděli, že jednu úlohu
odevzdá úplně stejně několik různých lidí, pokud chcete, udělejte repozitář
privátní.

Odkaz na repozitář nám pošlete e-mailem.
V repozitáři prosím nastavte tag `v0.1`.
Termín odevzdání je začátek příštího cvičení (dřívější paralelky).

Co by aplikace měla dělat? Můžete si vybrat:

### Twitter Wall

Twitter Wall pro terminál. Aplikace, která bude zobrazovat tweety odpovídající
určitému hledání do terminálu v nekonečné smyčce.

Aplikace načte určitý počet tweetů odpovídající hledanému výrazu, zobrazí je
a v nějakém intervalu se bude dotazovat na nové tweety (použijte API argument
`since_id`).

Pomocí argumentů půjde nastavit:

 * cesta ke konfiguračnímu souboru s přístupovými údaji
 * hledaný výraz
 * počet na začátku načtených tweetů
 * časový interval dalších dotazů
 * nějaké vlastnosti ovlivňující chování (např. zda zobrazovat retweety)

### GitHub Issues Bot

Robot (založte mu vlastní účet na GitHubu), který v intervalech projde issues
v repozitáři na GitHubu a ty neolabelované olabeluje podle zadaných pravidel.
Nezapomeňte robotovi dát přístup do vašeho testovacího repozitáře.

Pravidla by měla být nějakým způsobem konfigurovatelná
(např. páry regulární výraz → label).

Pomocí argumentů půjde nastavit:

 * cesta ke konfiguračnímu souboru s přístupovými údaji
 * který repozitář se má procházet
 * kde je soubor s definovanými pravidly
 * jak často issues kontrolovat
 * jaký label nastavit, pokud žádné pravidlo nezabralo
 * nějaké vlastnosti ovlivňující chování (např. zda má robot vyhodnocovat i komentáře, či procházet i Pull Requesty)

### Vlastní nápad

Můžete využít i jiné API (např. [KOSapi]) a vymyslet vlastní aplikaci.
Zadání vám ale musí schválit cvičící, protože v dalších cvičeních na tuto
aplikaci budeme nabalovat další a další funkce.

[KOSapi]: https://kosapi.fit.cvut.cz/projects/kosapi/wiki
