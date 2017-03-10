requests
========

Knihovna requests je určená pro HTTP požadavky (klienty).
Přestože vytvářet HTTP požadavky jde i bez requests, pomocí standardní knihovny
Pythonu, requests mají mnohem lidštější rozhraní a používají se mnohem
jednodušeji.

Instaluje se standardním způsobem:

```console
$ python -m pip install requests
```

Budeme předpokládat, že znáš alespoň základy HTTP protokolu a
vrhneme se rovnou na příklad.

!!! note ""
    Pokut základy neznáš, můžeš se podívat na
    [začátečnickou lekci]({{ lesson_url('projects/github-api') }}),
    která vysvětluje o trošičku víc.

```pycon
>>> import getpass
>>> import requests
>>> username = input('Username: ')
Username: hroncok
>>> password = getpass.getpass()
Password: 
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

Příklady použití pro další HTTP metody najdeš v [dokumentaci].

[dokumentaci]: http://docs.python-requests.org/en/master/user/quickstart/


## Použití session

Hlavně v budoucnu se nám bude hodit použití tz. *session*.

Session má několik výhod.
První je, že využívá na pozadí jedno otevřené HTTP spojení a poskytuje tak
při více sousledných požadavcích výrazné zrychlení.

Dále pak session automaticky ukládá *cookies* a je možné u ní nastavit výchozí
hlavičky.

Zkus si *cookies* vyzkoušet s [httpbin.org](http://httpbin.org) – službou
k testování HTTP dotazů:

```pycon
>>> session = requests.Session()
>>> session.get('http://httpbin.org/cookies/set/mipyt/best')
<Response [200]>
>>> r = session.get('http://httpbin.org/cookies')
>>> r.json()
{'cookies': {'mipyt': 'best'}}
>>> session.headers.update({'x-test': 'true'})
>>> r = session.get('http://httpbin.org/headers', headers={'x-test2': 'true'})
>>> r.json()
{'headers': {'Accept': '*/*', 'User-Agent': 'python-requests/2.10.0', 'X-Test2': 'true', 'Host': 'httpbin.org', 'Accept-Encoding': 'gzip, deflate', 'X-Test': 'true', 'Cookie': 'mipyt=best'}}
```

## Twitter API

Pro reálné použití si ukážeme, jak se dá pomocí requests získat seznam tweetů.
Z Twitteru nebudeme samozřejmě nic parsovat, ale použijeme jejich [API].

```pycon
>>> r = session.get('https://api.twitter.com/1.1/search/tweets.json')
>>> r.json()
{'errors': [{'code': 215, 'message': 'Bad Authentication data.'}]}
```

Jak můžeš vidět v odpovědi, Twitter API neumožňuje data číst bez autentizace.
Jak se autentizovat bys při troše hledání našel v dokumentaci, ale protože
tu nevyučujeme úvod do OAuthu, ale Python, rozhodli jsme se ti to zjednodušit.

Po přihlášení na Twitter (pokud nemáš, můžeš si vytvořit nějaký *dummy* účet)
jdi na [apps.twitter.com] a vytvoř aplikaci (URL si můžeš vymyslet).
Po vytvoření najdeš na kartě *Keys and Access Tokens* **API Key** a **API Secret**.
Pozor, jedná prakticky o hesla k tvému Twitter účtu,
a proto by je nikdo kromě tebe neměl vidět.

!!! warning "Ochrana přihlašovacích tokenů"
    Ještě jednou – *API Key* a *API Secret* se chovají jako hesla.
    Nikomu je nesmíš ukazovat!
    Stane-li se přesto, že se k nim dostane někdo nepovolaný, na kartě
    *Keys and Access Tokens* je můžeš zrušit.

Prozatím klíče nastav do proměnných, později je schováme například do
konfiguračního souboru.

```pycon
>>> api_key = 'D4HJp6PKmpon9eya1b2c3d4e5'
>>> api_secret = 'rhvasRMhvbuHJpu4MIuAb4WO50gnoQa1b2c3d4e5f6g7h8i9j0'
```

Tyto kódy je potřeba určitým způsobem slepit a poslat Twitteru,
aby vytvořil token, které pak půjde použít pro API.

```pycon
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

Pro komunikaci s Twitter API musíš přidat hlavičku se získaným tokenem,
tady využij faktu, že používáš *session* a nastav *autentizační funkci*:

```pycon
>>> def bearer_auth(req):
...     req.headers['Authorization'] = 'Bearer ' + bearer_token
...     return req
... 
>>> session.auth = bearer_auth
```

Pak už by mělo API fungovat:

```pycon
>>> r = session.get(
...     'https://api.twitter.com/1.1/search/tweets.json',
...     params={'q': '#python'},
... )
>>> for tweet in r.json()['statuses']:
...     print(tweet['text'])
... 
Once a framework decides to abstract the HTML layer from you. Customizing your UI becomes sorcery. #django #Python
...
```

Zde máš pro zjednodušení k dispozici celou funkci pro vytvoření autentizované
*session*:

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
získáš token). Stačí jít do [nastavení] a vyrobit nový token
(zatím není třeba zaškrtávat žádná opravnění).
Token musíš opět patřičně chránit.

Pomocí tokenu pak můžeš z Githubu získávat informace.
Tímto kódem například pak získáš popis přihlášeného uživatele, tedy sebe.

```pycon
>>> token = 'xxxxxxx'
>>> session = requests.Session()
>>> session.headers = {'Authorization': 'token ' + token, 'User-Agent': 'Python'}
>>> r = session.get('https://api.github.com/user')
>>> r.json()
```

Pokud budeš chtít něco provést, například dát hvězdičku repozitáři s těmito
materiály, musíš tokenu nastavit patřičné oprávnění
(u hvězdičky je to `public_repo`).
To se dělá přes [nastavení] na GitHubu.

Hvězdičku pak přidáš takto:

```pycon
>>> r = session.put('https://api.github.com/user/starred/pyvec/naucse.python.cz')
>>> r.text
''
```

Jak vidíš, API nevrací žádný text. Můžeš ale zkontrolovat návratový stav:

```pycon
>>> r.status_code
204
```

Případně vyhodit výjimku, pokud je stavový kód divný (např 404 Nenalezeno,
401 Chybí oprávnění, apod.):

```pycon
>>> r.raise_for_status()
```

Pokud hvězdičku chceš odebrat, použij metodu DELETE.
My ale věříme, že ji odebrat nechceš :)

[Dokumentace] ke GitHub API.

[nastavení]: https://github.com/settings/tokens
[Dokumentace]: https://developer.github.com/v3/


### Chraň své tokeny

Když ukládáš skript do Gitu, měj na paměti, že tokeny a klíče do něj nikdy
nepatří. Můžeš je uložit do konfiguračního souboru, který bude gitem ignorován,
například takhle:

```ini
[twitter]
key = D4HJp6PKmpon9eya1b2c3d4e5
secret = rhvasRMhvbuHJpu4MIuAb4WO50gnoQa1b2c3d4e5f6g7h8i9j0

[github]
token = xxxxxxx
```

A následně konfiguraci načteš pomocí modulu
[configparser](https://docs.python.org/3/library/configparser.html):

```pycon
>>> import configparser
>>> config = configparser.ConfigParser()
>>> config.read('auth.cfg')
>>> config['twitter']['key']
D4HJp6PKmpon9eya1b2c3d4e5
```

Do souboru `.gitignore` pak musíš přidat název ignorovaného souboru, např.:

    auth.cfg

Jelikož ostatní tvůj konfigurační soubor neuvidí,
je vhodné jim vysvětlit, jak takový soubor (s jejich údaji) vytvořit.
Můžeš například vložit do gitu soubor `auth.cfg.sample`
s vymyšlenými údaji, či příklad uvést v README.
