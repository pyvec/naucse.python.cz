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

Budeme předpokládat, že znáte alespoň základy HTTP protokolu,
a vrhneme se rovnou na příklad.

> [note]
> Pokud základy neznáte, můžete se podívat na
> [začátečnickou lekci]({{ lesson_url('projects/github-api') }}),
> která vysvětluje o trošičku víc.

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

Příklady použití pro další HTTP metody najdete v [dokumentaci].

[dokumentaci]: http://docs.python-requests.org/en/master/user/quickstart/


## Použití session

Hlavně v budoucnu se nám bude hodit použití tzv. *session*.

Session má několik výhod.
První je, že využívá na pozadí jedno otevřené HTTP spojení a poskytuje tak
při více sousledných požadavcích výrazné zrychlení.

Dále pak session automaticky ukládá *cookies* a je možné u ní nastavit výchozí
hlavičky.

Zkuste si *cookies* vyzkoušet s [httpbin.org](http://httpbin.org) – službou
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

Jak můžete vidět v odpovědi, Twitter API neumožňuje data číst bez autentizace.
Jak se autentizovat byste při troše hledání našli v dokumentaci, ale protože
tu nevyučujeme úvod do OAuthu, ale Python, rozhodli jsme se ti to zjednodušit.

Po přihlášení na Twitter (pokud nemáte účet, můžete si vytvořit nějaký *dummy*
účet, ale budete potřebovat ověřitelné telefonní číslo)
jděte na [apps.twitter.com] a vytvořte aplikaci (URL si můžete vymyslet).
Po vytvoření najdete na kartě *Keys and Access Tokens* **API Key** a **API Secret**.
Pozor, jedná se prakticky o hesla k vašemu Twitter účtu,
a proto by je nikdo kromě vás neměl vidět.

> [warning] Ochrana přihlašovacích tokenů
> Ještě jednou – *API Key* a *API Secret* se chovají jako hesla.
> Nikomu je nesmíte ukazovat!
> Stane-li se přesto, že se k nim dostane někdo nepovolaný, na kartě
> *Keys and Access Tokens* je můžete zrušit.

Prozatím klíče nastavte do proměnných, později je schováme například do
konfiguračního souboru.

```pycon
>>> api_key = 'D4HJp6PKmpon9eya1b2c3d4e5'
>>> api_secret = 'rhvasRMhvbuHJpu4MIuAb4WO50gnoQa1b2c3d4e5f6g7h8i9j0'
```

Pomocí těchto kódů je potřeba si od Twitter API vyžádat přístupový token.
Používá se k tomu běžné HTTP přihlášení ([HTTP Basic authentication]),
kde je `api_key` použit jako uživatelské jméno a `api_secret` jako heslo.

Pro běžné HTTP přihlášení se v knihovně requests používá
`requests.auth.HTTPBasicAuth`:

[HTTP Basic authentication]: https://cs.wikipedia.org/wiki/Basic_access_authentication

```pycon
>>> r = session.post('https://api.twitter.com/oauth2/token',
                     auth=requests.auth.HTTPBasicAuth(api_key, api_secret),
                     data={'grant_type': 'client_credentials'})
>>> 
>>> r.json()
{'token_type': 'bearer', 'access_token': 'AAAAAAAAAAAAAAAAAAAAAHhKXAAAAAAAaA1abB2bcC3cdD4deE5efF6fgG7ghH8hiI9ijJ0ja1b2c3d4e5f6g7h8i9j0a1b2c3d4e5f6g7h8i9j0'}
>>> bearer_token = r.json()['access_token']
```

Parametr `auth` v příkladu výše je autentizační funkce, která nějakým způsobem
modifikuje HTTP požadavek za účelem autentizace, většinou přidává specifické
hlavičky.
`requests.auth.HTTPBasicAuth` zde dle specifikace zakóduje jméno a heslo pomocí
algoritmu base64 a přidá hlavičku `Authorization`.

Ve skutečnosti je základní HTTP přihlášení tak běžné, že lze použít zkratku:

```pycon
>>> r = session.post('https://api.twitter.com/oauth2/token',
                     auth=(api_key, api_secret),
                     data={'grant_type': 'client_credentials'})
```

Pro další komunikaci s Twitter API je nutné přidat hlavičku se získaným tokenem.
Jelikož používáte session, není nutné to dělat u každého požadavku zvlášť,
ale je možné nastavit autentizační funkci pro celou session.

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

Zde je pro zjednodušení k dispozici celá funkce pro vytvoření autentizované
*session*:

```python
import requests

def twitter_session(api_key, api_secret):
    session = requests.Session()

    r = session.post('https://api.twitter.com/oauth2/token',
                     auth=(api_key, api_secret),
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
(zatím není třeba zaškrtávat žádná oprávnění).
Token je opět třeba patřičně chránit.

Pomocí tokenu pak můžete z GitHubu získávat informace.
Tímto kódem lze například získat popis přihlášeného uživatele, tedy sebe sama.

```pycon
>>> token = 'xxxxxxx'
>>> session = requests.Session()
>>> session.headers = {'User-Agent': 'Python'}
>>> def token_auth(req):
...     req.headers['Authorization'] = 'token ' + token
...     return req
... 
>>> session.auth = token_auth
>>> r = session.get('https://api.github.com/user')
>>> r.json()
```

> [note]
> Všimněte si hlavičky `User-Agent`. Ta je potřeba při komunikaci s GitHub API
> explicitně nastavit. Nastavení na objektu session zajistí, že tato hlavička
> bude ve všech požadavcích.

Pokud budete chtít něco provést, například dát hvězdičku repozitáři s těmito
materiály, musíte tokenu nastavit patřičné oprávnění
(u hvězdičky je to `public_repo`).
To se dělá přes [nastavení] na GitHubu.

Hvězdičku pak přidáte takto:

```pycon
>>> r = session.put('https://api.github.com/user/starred/pyvec/naucse.python.cz')
>>> r.text
''
```

Jak vidíte, API nevrací žádný text (žádné tělo odpovědi).
Můžete ale zkontrolovat návratový stav:

```pycon
>>> r.status_code
204
```

Případně vyhodit výjimku, pokud je stavový kód divný (např _404 Nenalezeno_,
_401 Chybí oprávnění_ apod.):

```pycon
>>> r.raise_for_status()
```

Pokud hvězdičku chcete odebrat, použijte metodu DELETE.
My ale věříme, že ji odebrat nechcete :)

[Dokumentace] ke GitHub API.

[nastavení]: https://github.com/settings/tokens
[Dokumentace]: https://developer.github.com/v3/


### Chraňte své tokeny

Když ukládáte skript do gitu, mějte na paměti, že tokeny a klíče do něj nikdy
nepatří. Můžete je uložit do konfiguračního souboru, který bude gitem ignorován,
například takhle:

```ini
[twitter]
key = D4HJp6PKmpon9eya1b2c3d4e5
secret = rhvasRMhvbuHJpu4MIuAb4WO50gnoQa1b2c3d4e5f6g7h8i9j0

[github]
token = xxxxxxx
```

A následně konfiguraci načtete pomocí modulu
[configparser](https://docs.python.org/3/library/configparser.html):

```pycon
>>> import configparser
>>> config = configparser.ConfigParser()
>>> config.read('auth.cfg')
>>> config['twitter']['key']
D4HJp6PKmpon9eya1b2c3d4e5
```

Do souboru `.gitignore` pak musíte přidat název ignorovaného souboru, např.:

    auth.cfg

Jelikož ostatní tento konfigurační soubor neuvidí,
je vhodné jim vysvětlit, jak takový soubor (s jejich údaji) vytvořit.
Můžete například vložit do gitu soubor `auth.cfg.sample`
s vymyšlenými údaji, či příklad uvést v README.
