# JSON

Existují i jiné programovací jazyky než Python.

Ostatní jazyky neumí pracovat s pythonními hodnotami.
Budeš-li se chtít s takovými programy „domluvit” –
předat jim nějaké informace ke zpracování
nebo od nich dostat výsledky –
musíš informace předávat v nějaké zjednodušené podobě.


## Typy

Většina programovacích jazyků má nějaká čísla, nějaký druh seznamů,
nějakou odrůdu řetězců a nějakou variaci na slovníky
(nebo několik způsobů jak slovníky vytvořit).
Dále má spousta jazyků způsob, jak zapsat
`True`, `False` a `None`.

Tyhle základní typy většinou stačí na předání
jakékoli informace v rozumně čitelné podobě,
i když ne ve všech jazycích mají přesné ekvivalenty
(třeba Python má dva základní druhy čísel – `int` a `float`).
Často se proto v komunikaci omezíme na ně.


## Kódování dat

Další problém je přenos dat:
abys mohl{{a}} informace zapsat na disk nebo přenést
přes Internet, musíš je převést na sekvenci *bytů* (čísel od 0 do 255).
Zjednodušeně řečeno, musíš je převést na řetězec.

Existuje spousta způsobů, jak zakódovat data do textu.
Každý způsob se snaží najít vhodnou rovnováhu mezi
čitelností pro lidi/počítače, délkou zápisu,
bezpečností, možnostmi a rozšiřitelností.
My už známe syntaxi Pythonu:

```python
{
    'jméno': 'Anna',
    'město': 'Brno',
    'jazyky': ['čeština', 'angličtina', 'Python'],
    'věk': 26,
}
```

Jiný způsob zápisu dat je [YAML](http://www.yaml.org/):

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
[Pickle 3](https://docs.python.org/3/library/pickle.html):

```plain
}q(XjmÃ©noqXAnnaqXmÄtoqXBrnoqXjazykyq]q(X       ÄeÅ¡tinaqX
                                                          angliÄtinaXPythonq       eXvÄq
K▒u.
```

A nakonec uvedu [JSON](http://json.org/)
(z angl. *Javascript Object Notation* „zápis Javascriptových objektů”),
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
> v Pythonu, je to jiný formát s vlastními pravidly.
> Nezaměňuj je!
>
> Aspoň ze začátku nedoporučuji JSON psát ručně;
> nech na počítači, aby dal na správné místo správné
> čárky a uvozovky.

## JSON v Pythonu

Kódování objektů v JSONu je jednoduché: existuje modul `json`,
jehož metoda `loads` načte data z řetězce:

```python
import json

json_retezec = """
    {
      "jméno": "Anna",
      "město": "Brno",
      "jazyky": ["čeština", "angličtina", "Python"],
      "věk": 26
    }
"""

data = json.loads(json_retezec)
print(data)
print(data['město'])
```

A pak tu je metoda `dumps`, která naopak daná data zakóduje
a vrátí řetězec:

```pycon
>>> print(json.dumps(data))
{"v\u011bk": 26, "jm\u00e9no": "Anna", "jazyky": ["\u010de\u0161tina", "angli\u010dtina", "Python"], "m\u011bsto": "Brno"}
```

To, co vrátí jednoduché zavolání `dumps(data)` je vhodné pro počítačové
zpracování;
má-li výsledná data číst člověk, nastav
`ensure_ascii=False` (aby se písmenka s diakritikou nekódovala pomocí `\`)
a `indent=2` (odsazení dvěma mezerami).

```pycon
>>> print(json.dumps(data, ensure_ascii=False, indent=2))
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

Kompletní popis modulu `json` –
včetně funkcí na zápis/čtení přímo do/ze souborů –
je v příslušné [dokumentaci](https://docs.python.org/3/library/json.html).
