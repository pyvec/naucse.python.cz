# Kódování dat

V Pythonu informace spravuješ v seznamech, slovnících a jiných datových
strukturách.
Když si vytvoříš nějaký slovník slovník plný seznamů, řetězců a čísel,
můžeš s ním v Pythonu dál pracovat. Třeba:

```python
data = {
    'jméno': 'Anna',
    'město': 'Brno',
    'jazyky': ['čeština', 'angličtina'],
    'věk': 26,
}
data['jazyky'].append('Python')
```

Taková data ale nejdou přímo zapsat na disk nebo přenést přes Internet.
Python si je „pamatuje“ tak, aby s nimi mohl jednoduše pracovat;
když Python vypneš, stuktura informací se ztratí.

Abys mohl{{a}} informace zapsat, uložit nebo dokonce přenést na jiný počítač,
musíš je *zakódovat* – převést na řetězec.
Řetězec pak lze zapsat do souboru nebo třeba poslat přes Internet.

> [note]
> Doopravdy se do souborů zapisují (a po síti posílají)
> sekvence *bytů* (čísel od 0 do 255).
> Python řetězce na byty ale převádí automaticky (pomocí kódování
> `UTF-8`, nastaveného pomocí `encoding='utf-8'`.
> Vystačíme si proto s převáděním na řetězce, se kterými – na rozdíl od bytů
> – už umíš pracovat.


## Typy

Když budeš informace ukládat nebo posílat po internetu,
je dobré zařídit, aby je uměly přečít i jiné programy než ten tvůj.
A ty jiné programy nemusí být napsané v Pythonu.

Ostatní jazyky často neumí přímopracovat s pythonními hodnotami – seznamy,
slovníky, `range`, nebo funkcemi.
Budeš-li se chtít s takovými programy „domluvit” –
předat jim nějaké informace ke zpracování
nebo od nich dostat výsledky –
musíš informace předávat v nějaké zjednodušené podobě.

Většina programovacích jazyků má nějaká čísla, nějaký druh seznamů,
nějakou odrůdu řetězců a nějakou variaci na slovníky
(nebo několik způsobů jak slovníky vytvořit).
Dále má spousta jazyků způsob, jak zapsat
`True`, `False` a `None`.

Tyhle základní typy většinou stačí na předání
jakékoli informace v rozumně čitelné podobě,
i když ne ve všech jazycích mají přesné ekvivalenty
(třeba Python má dva základní druhy čísel – `int` a `float`).
Často se proto v komunikaci omezíme na ně.


## Kódování

Existuje spousta způsobů, jak zakódovat data do textu.
Každý způsob se snaží najít vhodnou rovnováhu mezi
čitelností pro lidi/počítače, délkou zápisu,
bezpečností, možnostmi a rozšiřitelností.
Už známe syntaxi Pythonu; která jak už název napovídá, funguje jen pro Python:

```python
{
    'jméno': 'Anna',
    'město': 'Brno',
    'jazyky': ['čeština', 'angličtina', 'Python'],
    'věk': 26,
}
```

Jiný způsob zápisu dat je třeba [YAML](http://www.yaml.org/):

```yaml
jméno: Anna
město: Brno
jazyky:
  - čeština
  - angličtina
  - Python
věk: 26
```

Nebo třeba [Bencode](http://en.wikipedia.org/wiki/Bencode):

```plain
d6:jazykyl9:čeština11:angličtina6:Pythone4:věki26e6:město4:Brno6:jméno4:Annae
```

Existují i netextové formáty, jako
[Pickle 3](https://docs.python.org/3/library/pickle.html).
Převedením do textu bys dostal{{a}} „guláš“ jako:

```plain
}q(XjmÃ©noqXAnnaqXmÄtoqXBrnoqXjazykyq]q(X       ÄeÅ¡tinaqX
                                                          angliÄtinaXPythonq       eXvÄq
K▒u.
```

A nakonec uvedu [JSON](http://json.org/)
(z angl. *Javascript Object Notation* „zápis Javascriptových objektů”),
který se pro svou jednoduchost rozšířil na Internetu nejvíc:

```json
{
  "jméno": "Anna",
  "město": "Brno",
  "jazyky": ["čeština", "angličtina", "Python"],
  "věk": 26
}
```

> [note]
> Pozor na to, že ačkoli JSON vypadá podobně jako zápis
> v Pythonu, je to jiný formát s vlastními pravidly.
> Nezaměňuj je!
>
> Aspoň ze začátku nedoporučuji JSON psát ručně;
> nech na počítači, aby dal na správné místo správné
> čárky a uvozovky.


## JSON

Pojďme se zaměřit na populární JSON; práce s ostatními formáty funguje podobně.

K zakódování dat do textu použij funkci `dumps` z modulu `json`
(který je potřeba naimportovat).

```pycon
>>> import json
>>> kod = json.dumps(data)
>>> kod
'{"jm\\u00e9no": "Anna", "m\\u011bsto": "Brno", "jazyky": ["\\u010de\\u0161tina", "angli\\u010dtina", "Python"], "v\\u011bk": 26}'
```

Výsledný řetězec obsahuje ty správné informace – ale je psaný spíš pro
počítačové zpracování než k tomu, aby ho četl člověk.

Zapiš tenhle řetězec do souboru:

```python
with open('data.json', 'w') as soubor:
    print(kod, file=soubor)
```

Jinde – třeba v jiném programu, nebo dokonce na jiném počítači, pokud tam
soubor zkopíruješ – můžeš pak řetězec s kódem načíst:

```python
with open('data.json') as soubor:
    kod = soubor.read()
```

A pomocí `json.loads` ho pak převedeš zpátky na původní slovník,
se kterým můžeš dál pracovat:

```pycon
>>> data = json.loads(kod)
>>> print(data)
{'jméno': 'Anna', 'město': 'Brno', 'jazyky': ['čeština', 'angličtina', 'Python'], 'věk': 26}
>>> print(data['věk'] + 1)
27
```


### Typy

JSON neumožňuje věrně zakódovat jakýkoli Pythonní objekt.
Zaměřuje se na výměnu informací mezi různými programy – a to i programy
napsanými v jiných programovacích jazycích než v Pythonu.

Jiné jazyky často neumí pracovat s Pthonními hodnotami
a informace je jim potřeba předávat v nějaké společné, zjednodušené podobě.

Většina programovacích jazyků má nějaká čísla, nějaký druh seznamů,
nějakou odrůdu řetězců a nějakou variaci na slovníky
(často jen s řetězcovými klíči).
Dále má spousta jazyků způsob, jak zapsat
`True`, `False` a `None`.

Tyhle základní typy většinou stačí na předání
jakékoli informace v rozumně čitelné podobě,
i když ne všechny jazyky mají přesné ekvivalenty
(třeba Python má dva základní druhy sekvencí – seznamy a <var>n</var>-tice).

Převod na JSON je proto „ztrátový“: po rozkódování nedostaneš přesně stejný
objekt jako ten, který jsi zakódoval{{a}}, ale nějaký podobný.
Konkrétně modul `json` převádí <var>n</var>-tice na seznamy
a klíče slovníků převádí na řetězce:

```python
>>> data = {'dvojice': (1, 2), 'seznam': [3, 4], 2: 'dva', 11: 'jedenáct'}
>>> kod = json.dumps(data)
>>> json.loads(kod)
{'dvojice': [1, 2], 'seznam': [3, 4], '2': 'dva', '11': 'jedenáct'}
```


### Hezký výstup

To, co vrací `json.dumps`, je vhodné pro počítačové zpracování:

```pycon
>>> kod = json.dumps(data)
>>> print(kod)
{"jm\u00e9no": "Anna", "m\u011bsto": "Brno", "jazyky": ["\u010de\u0161tina", "angli\u010dtina", "Python"], "v\u011bk": 26}
```

Má-li výsledný soubor číst člověk, je ho možné zpřehlednit
pomocí pojmenovaných argumentů `ensure_ascii=False`
(aby se písmenka s diakritikou nekódovala pomocí `\`)
a `indent=2` (odsazení dvěma mezerami).

```pycon
>>> kod = json.dumps(data, ensure_ascii=False, indent=2)
>>> print(kod)
{
  "věk": 26,
  "jméno": "Anna",
  "jazyky": [
    "čeština",
    "angličtina",
    "Python"
  ],
  "město": "Brno"
}
```

Tenhle kód lze taky zapsat do souboru nebo načíst zpět pomocí `json.loads`,
jen se trochu líp čte lidem.

> [note]
> Pozor na to, že ačkoli „hezký“ JSON vypadá podobně jako zápis
> v Pythonu, je to jiný formát s vlastními pravidly.
> Nezaměňuj je!
>
> Aspoň ze začátku nedoporučuji JSON psát ručně;
> nech na počítači, aby dal na správné místo správné
> čárky a uvozovky.

> [note]
> kompletní popis modulu `json` –
> včetně funkcí na zápis/čtení přímo do/ze souborů –
> je v příslušné [dokumentaci](https://docs.python.org/3/library/json.html).




## Jiná kódování

Jak už bylo řečeno, JSON je jen jeden ze způsobů, kterými lze data zakódovat.
Jiná kódování mají své pro a proti, ale v podstatě fungují stejně:
jedna funkce (často `dumps`) zakóduje Pythonní objekt do řetězce a druhá
(často `loads`) dekóduje řetězec na původní (nebo podobný) Pythonní objekt.

V případech, kdy má soubor s informacemi psát člověk,
se často používají formáty [TOML] nebo [YAML].


### TOML

Knihovnu pro TOML potřeba si nainstalovat:

```console
(venv)$ python -m pip install toml
```

Data pak lze kódovat pomocí `toml.dumps` a dekódovat pomocí `toml.loads`:


```pycon
>>> import toml
>>> print(toml.dumps(data))
"věk" = 26
"jméno" = "Anna"
jazyky = ["čeština", "angličtina", "Python"]
"město" = "Brno"
```


### YAML

Knihovnu pro YAML, je také potřeba doinstalovat:

```console
(venv)$ python -m pip install pyyaml
```

Data pak lze kódovat pomocí `yaml.safe_dump` (nebo „hezky“
pomocí `yaml.safe_dump(data, indent=4, allow_unicode=True)`)
a zapisovat pomocí `yaml.safe_load(kod)`.
Výsledný soubor vypadá takto:

```yaml
jazyky:
- čeština
- angličtina
- Python
jméno: Anna
město: Brno
věk: 26
```


[JSON]: https://www.json.org
[TOML]: https://github.com/toml-lang/toml
[YAML]: https://yaml.org/
