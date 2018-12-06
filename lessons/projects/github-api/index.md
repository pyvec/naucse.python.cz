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
 
## Requests

K práci s internetovými stránkami použijeme knihovnu Requests.
V aktivovaném virtuálním prostředí si ji nainstaluj příkazem:

```console
(env)$ python -m pip install requests
```

A potom v Pythonu zkus stáhnout nějakou stránku:

```python
import requests

# stažení stránky
stranka = requests.get('https://cs.wikipedia.org', timeout=5)

# ověření, že dotaz proběhl v pořádku
stranka.raise_for_status()

# vypsání obsahu
print(stranka.text)
```

Měl by se vypsat obsah stránky
[https://cs.wikipedia.org](https://cs.wikipedia.org) –
HTML kód, který se objeví když v prohlížeči dáš
„Ukázat zdroj” (*View Page Source*, většinou <kbd>Ctrl</kbd>+<kbd>U</kbd>)
a ze kterého prohlížeč umí vykreslit stránku.

Ale my nechceme obsah pro lidi.
Podívejme se, co Wikipedia zpřístupňuje počítačům.


## Data pro strojové zpracování

Nyní si načteme stránku, která nám vrátí výsledek v JSON:

```python
import requests

# klíčové slovo, podle kterého budeme vyhledávat
klic = 'Vánoce'

# stažení stránky
stranka = requests.get('https://cs.wikipedia.org/w/api.php?action=query&prop=extracts&explaintext&exintro&format=json&titles={}'.format(klic), timeout=5)

# ověření, že dotaz proběhl v pořádku
stranka.raise_for_status()

# vypsání obsahu
print(stranka.text)
```

Na náš dotaz Wikipedia vrátí základní informace o zadaném vyhledávacím klíči v JSONU. 

Zkus řetězec `stranka.text` převést z JSON na slovník
a vypsat trochu srozumitelněji:

```python
import json

# Převedeme do Pythoních struktur
data = json.loads(stranka.text)

# vypíšeme s odsazením 
print(json.dumps(data, ensure_ascii=False, indent=2))
```

