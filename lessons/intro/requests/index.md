Requests
========

Knihoven pro HTTP klienty (tedy “programy, které stahují webové stránky“)
je celá řada.
Jedna z nich, [`urllib.request`], je dokonce součástí standardní knihovny Pythonu.
Pokud tedy budete chtít HTTP používat a seznam závislostí
svého projektu nemůžete rozšířit o další knihovnu, jde to.

Mnohem snáze se vám ale bude pracovat s knihovnou [Requests],
která má mnohem “lidštější” rozhraní a používá se mnohem jednodušeji.
Rozdíl je největší u pokročilejších vlastností
jako *cookies*, autentizace nebo sdílení spojení (*Keep-alive*),
které s Requests zvládnete i bez detailních znalostí protokolu HTTP.

Dokonce i v dokumentaci modulu `urllib` se píše:
*The [Requests package][Requests] is recommended for a higher-level HTTP
client interface.*
Zaměříme se tedy na Requests hned od začátku.

[`urllib.request`]: https://docs.python.org/3/library/urllib.request.html#module-urllib.request
[Requests]: https://requests.readthedocs.io/en/master/

Knihovna Requests se instaluje standardním způsobem:

```console
$ python -m pip install requests
```

Budeme předpokládat, že znáte alespoň základy HTTP protokolu,
a vrhneme se rovnou na příklad.

> [note]
> Pokud základy neznáte, můžete se podívat na
> [shrnutí pro začátečníky]({{ lesson_url('fast-track/http') }}),
> které vysvětluje vše potřebné.

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

> [note]
> Tento příklad pracuje přímo se jménem a heslem.
> To se většinou nedělá a webové API to často ani nepodporují.
> Pokud na GitHub používáte dvoufaktorovou autentizaci, příklad nebude fungovat.

Příklady použití pro další HTTP metody najdete v [dokumentaci].

[dokumentaci]: http://docs.python-requests.org/en/master/user/quickstart/


## Použití session

Hlavně v budoucnu se nám bude hodit použití tzv.
[*session*](http://docs.python-requests.org/en/master/user/advanced/#session-objects).

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
{'headers': {'Accept': '*/*', 'Accept-Encoding': 'gzip, deflate', 'Connection': 'close', 'Cookie': 'mipyt=best', 'Host': 'httpbin.org', 'User-Agent': 'python-requests/2.19.1', 'X-Test': 'true', 'X-Test2': 'true'}}
```

## GitHub API

Podíváme se teď, podobně jako v úvodním příkladu, na [GitHub API],
které má poměrně jednoduchou autentizaci (od GitHubu přímo
získáte token). Stačí jít do [nastavení] a vyrobit nový token
(zatím není třeba zaškrtávat žádná oprávnění).

> [warning] Ochrana přihlašovacích tokenů
> Váš token je něco jako vaše heslo.
> Nikomu je nesmíte ukazovat a nesmíte jej dát do Gitu.
> Stane-li se přesto, že se k němu dostane někdo nepovolaný,
> můžete jej v [nastavení] opět smazat.

Pomocí tokenu můžete z GitHubu získávat informace.
Prozatím token nastavte do proměnné, později jej schováme například do
konfiguračního souboru.

Tímto kódem lze například získat popis přihlášeného uživatele, tedy sebe sama.

```pycon
>>> token = 'd7313dab254b7fd0d0f3ec3cbf754b3abce462d5'
>>> session = requests.Session()
>>> session.headers = {'User-Agent': 'Python'}
>>> def token_auth(req):
...     req.headers['Authorization'] = f'token {token}'
...     return req
... 
>>> session.auth = token_auth
>>> r = session.get('https://api.github.com/user')
>>> r.json()
```

Funkce `session.auth` v příkladu výše je autentizační funkce,
která nějakým způsobem modifikuje HTTP požadavek za účelem autentizace,
většinou přidává specifické hlavičky (jak je tomu i zde).
Lze ji nastavit buďto na celé session nebo předat argumentem `auth` s každým
požadavkem.

Existují předpřipravené funkce v modulu `requests.auth`, například 
`requests.auth.HTTPBasicAuth` provádí základní HTTP přihlášení.
Dle specifikace zakóduje jméno a heslo pomocí
algoritmu base64 a přidá hlavičku `Authorization`.

[Základní HTTP přihlášení](https://cs.wikipedia.org/wiki/Basic_access_authentication)
je tak běžné, že pro něj Requests mají zkratku –
místo `HTTPBasicAuth` se dá použít i dvojice (jméno, heslo):

```pycon
>>> requests.get('https://httpbin.org/basic-auth/AzureDiamond/hunter2',
                 auth=requests.auth.HTTPBasicAuth('AzureDiamond', 'hunter2'))
>>> 
>>> requests.get('https://httpbin.org/basic-auth/AzureDiamond/hunter2',
                 auth=('AzureDiamond', 'hunter2'))
```

> [note]
> Všimněte si také hlavičky `User-Agent`.
> Ta je potřeba při komunikaci s GitHub API explicitně nastavit.
> Nastavení na objektu session zajistí, že tato hlavička
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
[GitHub API]: https://developer.github.com/v3

## Chraňte své tokeny

Když ukládáte skript do gitu, mějte na paměti, že tokeny a klíče do něj nikdy
nepatří. Můžete je uložit do konfiguračního souboru, který bude gitem ignorován,
například takhle:

```ini
[github]
token = d7313dab254b7fd0d0f3ec3cbf754b3abce462d5
```

A následně konfiguraci načtete pomocí modulu
[configparser](https://docs.python.org/3/library/configparser.html):

```pycon
>>> import configparser
>>> config = configparser.ConfigParser()
>>> with open('auth.cfg') as f:
...     config.read_file(f)
>>> config['github']['token']
'd7313dab254b7fd0d0f3ec3cbf754b3abce462d5'
```

Do souboru `.gitignore` pak musíte přidat název ignorovaného souboru, např.:

    auth.cfg

Ověřte si, že git soubor `auth.cfg` opravdu ignoruje, t.j. soubor se neukáže
ve výstupu `git status`.

Jelikož ostatní tento konfigurační soubor neuvidí,
je vhodné jim vysvětlit, jak takový soubor (s jejich údaji) vytvořit.
Můžete například vložit do gitu soubor `auth.cfg.sample`
s vymyšlenými údaji, či příklad uvést v README.

> [note]
> ConfigParser změní velikost písmen klíčů z konfiguračního souboru na malá.
> Pokud potřebujete, aby byly klíče přesně tak, jak jsou v souboru, musíte
> před načtením nastavit `config.optionxform = str`.
