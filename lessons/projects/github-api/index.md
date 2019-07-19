# Webové API

Jak už bylo řečeno v [lekci o JSON]({{ lesson_url('intro/json') }}),
hlavní výhoda formátu JSON je, že se na Internetu rozšířil nejvíc.
Pojďme toho využít!

Spousta webových služeb poskytuje takzvané
*API* (z *application programming interface*,
programátorské rozhraní), přes které je možné s danou
službou komunikovat programově.
Místo klikání na tlačítka a čtení stránek „očima”
dostaneme data ve formátu, kterým rozumí počítače –
a v dnešní době to bude většinou formát JSON.

Z minulých lekcí bys měl{{a}} mít založený účet na github.com,
tak se zkusme zeptat Githubu, co o nás ví.


## Autorizace

První, a mnohdy nejsložitější, krok k použití API
je přihlášení. Počítače se totiž přihlašují jinak
než lidi a problematika bezpečnosti a oprávnění by vydala na samostatný kurz.
My to uděláme co nejjednodušeji, ať se rychle dostaneme k jádru věci:

* Přihlaš se na [github.com](https://github.com).
* Jdi na [nastavení Personal Accesss Tokens](https://github.com/settings/tokens).
* Vytvoř si nový token ("Generate new token"). Nezaškrtávej žádná oprávnění navíc.
* Zkopíruj si heslo, které takto dostaneš, do souboru `token.txt`.

> [warning] Pozor!
> Vygenerovaný kód je heslo, které držitele
> opravňuje pracovat s Githubem pod tvým jménem!
> Drž ho v tajnosti. Kdyby se přece jen dostalo „ven”, na stránce
> [Personal Accesss Tokens](https://github.com/settings/tokens) ho deaktivuj.

    
## Requests

K práci s internetovými stránkami použijeme knihovnu Requests.
V aktivovaném virtuálním prostředí si ji nainstaluj příkazem:

```console
(venv)$ python -m pip install requests
```

A potom v Pythonu zkus stáhnout nějakou stránku:

```python
import requests

# stažení stránky
stranka = requests.get('https://github.com')

# ověření, že dotaz proběhl v pořádku
stranka.raise_for_status()

# vypsání obsahu
print(stranka.text)
```

Měl by se vypsat obsah stránky
[https://github.com](https://github.com) –
HTML kód, který se objeví když v prohlížeči dáš
„Ukázat zdroj” (*View Page Source*, většinou <kbd>Ctrl</kbd>+<kbd>U</kbd>)
a ze kterého prohlížeč umí vykreslit stránku.

Ale my nechceme obsah pro lidi.
Podívejme se, co Github zpřístupňuje počítačům.


## Uživatelský účet

Zkus, co dělá tento kód:

```python
import requests

with open('token.txt') as soubor:
    token = soubor.read().strip()

headers = {'Authorization': 'token ' + token}

stranka = requests.get('https://api.github.com/user', headers=headers)
stranka.raise_for_status()
print(stranka.text)
```

Co se stalo? Tím, že jsi Githubu dal{{a}} svůj token
(načtený ze souboru, předaný přes slovník `headers`),
poznal, že jde dotaz od tebe a vrátil nějaké informace
ve formátu JSON.

Zkus řetězec `stranka.text` převést z JSON na slovník
a vypsat trochu srozumitelněji:

```python
data = json.loads(stranka.text)

print(json.dumps(data, ensure_ascii=True, indent=2))
```

Teď už je lépe vidět celý tvůj profil
(možná včetně neveřejných informací – proto musíš svůj token
udržovat v tajnosti).

S profilem, který máš v proměnné `data`,
se dá pracovat jako s každým jiným slovníkem.
Třeba adresu svého obrázku můžeš vypsat pomocí:

```python
print(data['avatar_url'])
```


## API Githubu

API Githubu toho umí mnohem víc. Třeba na adrese
[https://api.github.com/emojis](https://api.github.com/emojis) na tebe čeká
slovník s adresami malých obrázků.
(Tenhle slovník funguje jako vyhledávací tabulka.)
Celé API je zdokumentováno na adrese
[developer.github.com](https://developer.github.com/v3/).


## Interakce

Pomocí webových API se dají informace nejen číst, ale i měnit.

Na stránce
[github.com/pyvec/naucse.python.cz/stargazers](https://github.com/pyvec/naucse.python.cz/stargazers)
je seznam lidí, kteří „ohvězdičkovali” tyto učební materiály.
Je jich zatím málo; pojďme se k nim pomocí webového API přidat.

Napřed svému tokenu (na Githubu v nastavení
[Personal Accesss Tokens](https://github.com/settings/tokens))
přidej právo `public_repo`.
Od teď token střež obzvlášť pečlivě, protože se pomocí
něj dají informace na Githubu i měnit.

Chceme-li měnit informace, musíme knihovně Requests
říct, aby použila jinou „HTTP metodu” než `GET`.
Co to přesně jsou HTTP metody je na trochu delší povídání
(viz [Wikipedia](https://en.wikipedia.org/wiki/Hypertext_Transfer_Protocol#Request_methods)),
ale stručně řečeno, pomocí `GET` se většinou stahuje
obsah, pomocí `POST` se přidává nový,
`PUT` mění něco, co už na webu existuje
a `DELETE` něco maže.
Jakou metodu poujeme závisí na tom, co chceme udělat;
většinou to bude `POST`, `PUT` nebo `DELETE`.

Podle [dokumentace Githubu](https://developer.github.com/v3/activity/starring/#star-a-repository)
se přidání hvězdičky dělá pomocí `PUT`
dotazu na adresu `/user/starred/:owner/:repo`.
Za `:owner` a `:repo`
dosadíš vlastníka a jméno repozitáře
(v našem případě `pyvec` a `naucse.python.cz`)
a `PUT` metodu zvolíš tak, že zavoláš místo `get` funkci `put`:

```python
import requests

with open('token.txt') as soubor:
    token = soubor.read().strip()

headers = {'Authorization': 'token ' + token}

stranka = requests.put('https://api.github.com/user/starred/pyvec/naucse.python.cz', headers=headers)
stranka.raise_for_status()
```

Tenhle dotaz nevrátí žádný text, ale na
[github.com/pyvec/naucse.python.cz/stargazers](https://github.com/pyvec/naucse.python.cz/stargazers)
se můžeš přesvědčit, že to funguje.

Chceš-li hvězdičku zase odstranit, použij metodu
`DELETE` na stejnou adresu.
(Ale nezapomeň tam pak ★ zase vrátit! ☺)
