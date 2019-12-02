# Kódování dat

Teď se podívejme na to, jak zapisovat do souborů jiné hodnoty než jen
řetězce.

V Pythonu informace spravuješ v seznamech, slovnících a jiných datových
strukturách.
Řekněme, že máš následující slovník plný seznamů, řetězců a čísel:

```python
data = {
    'jméno': 'Anna',
    'město': 'Brno',
    'jazyky': ['čeština', 'angličtina', 'Python'],
    'věk': 26,
}
```

Taková data nejdou přímo zapsat na disk nebo přenést přes Internet.
Python si je „pamatuje“ tak, aby s nimi mohl jednoduše pracovat;

Když Python vypneš, stuktura informací se ztratí.

Abys mohl{{a}} informace zapsat, musíš je *zakódovat*:
převést na sekvenci *bytů* (čísel od 0 do 255).

V Pythonu na to existuje modul zvaný `pickle`, jehož funkce `dumps`
převede Pythonní informace na ony byty:

```pycon
>>> import pickle
>>> kod = pickle.dumps(data)
```

Když si výsledné bajty vypíšeš, zobrazí se něco jako:

```pycon
>>> kod
b'\x80\x03}q\x00(X\x06\x00\x00\x00jm\xc3\xa9noq\x01X\x04\x00\x00\x00Annaq\x02X\x06\x00\x00\x00m\xc4\x9bstoq\x03X\x04\x00\x00\x00Brnoq\x04X\x06\x00\x00\x00jazykyq\x05]q\x06(X\t\x00\x00\x00\xc4\x8de\xc5\xa1tinaq\x07X\x0b\x00\x00\x00angli\xc4\x8dtinaq\x08X\x06\x00\x00\x00Pythonq\teX\x04\x00\x00\x00v\xc4\x9bkq\nK\x1au.'
```

Začáteční `b'` označuje, že jde o *byty* (čísla od 0 do 255), které jsou pak
zobrazeny trošku nečitelně, se spoustou `\x`.
Převedením na seznam ale můžeš zjistit, o jaká čísla jde.

```pycon
>>> list(kod)
[128, 3, 125, 113, 0, 40, 88, 6, 0, 0, 0, 106, 109, 195, 169, 110, 111, 113, 1, 88, 4, 0, 0, 0, 65, 110, 110, 97, 113, 2, 88, 6, 0, 0, 0, 109, 196, 155, 115, 116, 111, 113, 3, 88, 4, 0, 0, 0, 66, 114, 110, 111, 113, 4, 88, 6, 0, 0, 0, 106, 97, 122, 121, 107, 121, 113, 5, 93, 113, 6, 40, 88, 9, 0, 0, 0, 196, 141, 101, 197, 161, 116, 105, 110, 97, 113, 7, 88, 11, 0, 0, 0, 97, 110, 103, 108, 105, 196, 141, 116, 105, 110, 97, 113, 8, 88, 6, 0, 0, 0, 80, 121, 116, 104, 111, 110, 113, 9, 101, 88, 4, 0, 0, 0, 118, 196, 155, 107, 113, 10, 75, 26, 117, 46]
```

A sekvence *bytů* je něco, co se dá zapsat do souboru.
Python standardně otevírá soubory jako *textové*; aby šly zapsat byty,
je potřeba otevřít pomocí `'wb'` (pro zápis) nebo `rb` (pro čtení)
a bez argumentu `encoding`.

```python
with open('data.pickle', 'wb') as soubor:
    soubor.write(kod)
```

V jiném programu (nebo i na jiném počítači, pokud tam soubor nakopíruješ)
lze soubor otevřít a přečíst:

```python
with open('data.pickle', 'rb') as soubor:
    kod = soubor.read()
```

A nakonec z nich dostat zpět původní slovník pomocí `pickle.loads`:

```python
data = pickle.loads(kod)
```


# Jiná kódování

Pickle je jen jeden ze způsobů, kterými lze data zakódovat.
Slovník `data` zakódovaný modulem `marshal` by byl trochu jiný – ale opět
by se dal (s pomocí správné funkce) na jiném počítači správně dekódovat:

```plain
b'\xfbu\x06\x00\x00\x00jm\xc3\xa9noZ\x04Annau\x06\x00\x00\x00m\xc4\x9bstoZ\x04BrnoZ\x06jazyky[\x03\x00\x00\x00u\t\x00\x00\x00\xc4\x8de\xc5\xa1tinau\x0b\x00\x00\x00angli\xc4\x8dtina\xda\x06Pythonu\x04\x00\x00\x00v\xc4\x9bk\xe9\x1a\x00\x00\x000'
```

Existují i kódování, které na textový řetězec místo sekvence bajtů.
Soubor v takovém kódování často přečíst i člověk; některé dokonce vypadají
podobně jako zápis v Pythonu.

Jako příklad uvedu [YAML]:

```yaml
jméno: Anna
město: Brno
jazyky:
  - čeština
  - angličtina
  - Python
věk: 26
```

Nebo [TOML]:

```toml
"jméno" = "Anna"
"město" = "Brno"
jazyky = [ "čeština", "angličtina", "Python",]
"věk" = 26
```

Nebo [JSON]:

```json
{
  "jméno": "Anna",
  "město": "Brno",
  "jazyky": ["čeština", "angličtina", "Python"],
  "věk": 26
}
```

Každý má svá pro a proti.
Nejpopulárnější ze všech je aktuálně JSON, proto se více zaměříme na něj.


## JSON

Máš-li nějaké informace:

```python
data = {
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

… dají se do formátu JSON zakódovat pomocí funkce `dumps` z modulu `json`:

```python
>>> kod = json.dumps(data)
>>> kod
'{"v\\u011bk": 26, "jm\\u00e9no": "Anna", "jazyky": ["\\u010de\\u0161tina", "angli\\u010dtina", "Python"], "m\\u011bsto": "Brno"}'
```

Výsledek je řetězec, který lze zapsat do souboru:

```python
with open('data.json', 'w', encoding='utf-8') as soubor:
    print(kod, file=soubor)
```

V jiném programu nebo na jiném počítači lze informace opět přečíst
a pomocí `json.loads` převést na Pythonní slovník:

```python
with open('data.json', encoding='utf-8') as soubor:
    kod = soubor.read()

data = json.loads(kod)
```

### Hezký výstup

To, co vrací `json.dumps`, je vhodné pro počítačové zpracování.
Má-li výsledný soubor číst člověk, je možné zpřehlednit
pomocí pojmenovaných argumentů
`ensure_ascii=False` (aby se písmenka s diakritikou nekódovala pomocí `\`)
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

Tenhle kód lze taky zapsat do souboru nebo načíst pomocí `json.loads`,
jen se trochu líp čte lidem.

> [note]
> Pozor na to, že ačkoli JSON vypadá podobně jako zápis
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

## Typy

Údaje zapsané do souborů nebo poslané přes Internet se často kódují tak,
aby s nimi mohly pracovat i jiné progarmovací jazyky než Python.

Ostatní jazyky neumí pracovat s pythonními hodnotami
a informace je jim potřeba předávat v nějaké zjednodušené podobě.

Většina programovacích jazyků má nějaká čísla, nějaký druh seznamů,
nějakou odrůdu řetězců a nějakou variaci na slovníky
(často jen s řetězcovými klíči).
Dále má spousta jazyků způsob, jak zapsat
`True`, `False` a `None`.

Tyhle základní typy většinou stačí na předání
jakékoli informace v rozumně čitelné podobě,
i když ne všechny jazyky mají přesné ekvivalenty
(třeba Python má dva základní druhy čísel – `int` a `float`).
Kódování jako JSON se proto omezují pouze na ně.

U JSON se toto omezení projevuje tak, že <var>n</var>-tice převádí na seznamy
a klíče slovníků převádí na řetězce:

```python
>>> data = {'dvojice': (1, 2), 'seznam': [3, 4], 2: 'dva', 11: 'jedenáct'}
>>> kod = json.dumps(data)
>>> json.loads(kod)
{'dvojice': [1, 2], 'seznam': [3, 4], '2': 'dva', '11': 'jedenáct'}
```


## Shrnutí formátů

Pro úplnost uvádím tabulku formátů, 
Každou funkci je potřeba naimportovat (např. `from json import dumps`).

| Formát   | Kódování                      | Dekódování                      |
|----------|-------------------------------|---------------------------------|
| [JSON]   | `json.dumps`                  | `json.loads`                    |
| [pickle] | `pickle.dumps`                | `pickle.loads`                  |
| [TOML]   | `toml.dumps` *                | `toml.loads` *                  |
| [YAML]   | `yaml.safe_dump` *            | `yaml.safe_load` *              |
| [Python] | `repr` **                     | `ast.literal_eval`              |

Poznámky:

\* vyžaduje nainstalování externí knihovny: `python -m pip install pyyaml`,
resp. `python -m pip install toml`.

\** Ne všechny kódování získaná pomocí `repr` jdou načíst zpátky pomocí
`ast.literal_eval`.

[JSON]: https://www.json.org
[pickle]: https://docs.python.org/3/library/pickle.html
[TOML]: https://github.com/toml-lang/toml
[YAML]: https://yaml.org/
[Python]: https://docs.python.org/3/library/functions.html#repr
