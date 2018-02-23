# Slovníky

Další základní datový typ, který si představíme –
po číslech, řetězcích, seznamech a <var>n</var>-ticích –
jsou *slovníky* (angl. *dictionary*, `dict`).

Podobně jako seznamy, slovníky v sobě obsahují další hodnoty.
Na rozdíl od seznamů, ve kterých jsou všechny prvky
uspořádané do jedné sekvence, ve slovnících máme dva druhy
prvků: takzvaný *klíč* (angl. *key*) a *hodnotu* (angl. *value*).
Každému klíči je přiřazena jedna hodnota.

Slovník můžeš použít, když máš několik kousků
informací, které se dají pojmenovat, ale chceš s nimi
pracovat jako s jednou proměnnou.

Tady je slovník, který má tři klíče, a k nim příslušné tři hodnoty:

```pycon
>>> ja = {'jméno': 'Anna', 'město': 'Brno', 'čísla': [3, 7]}
```

{# XXX - Only visible on Python 3.5 and below. How to teach this?
Když slovník vypíšeš, pravděpodobně zjistíš,
se klíče a hodnoty vypíšou v jiném pořadí.
Slovníky totiž, na rozdíl od seznamů, nemají dané
pořadí prvků – jen přiřazují hodnoty klíčům.
#}

Hodnoty ze slovníku můžeš získat podobně jako
ze seznamu, jen místo indexu (pozice) použiješ klíč:

```pycon
>>> ja['jméno']
'Anna'
```

Zeptáš-li se na neexistující klíč, nebude se to Pythonu líbit:

```pycon
>>> ja['věk']
Traceback (most recent call last):
  File "<stdin>", line 1, in &lt;module&gt;
KeyError: 'věk'
```

Hodnoty jdou podle klíče i měnit:

```pycon
>>> ja['čísla'] = [3, 7, 42]
>>> ja
{'jméno': 'Anna', 'město': 'Brno', 'čísla': [3, 7, 42]}
```

... nebo přidávat:

```pycon
>>> ja['jazyk'] = 'Python'
>>> ja
{'jméno': 'Anna', 'město': 'Brno', 'čísla': [3, 7, 42], 'jazyk': 'Python'}
```

... nebo ubírat příkazem `del`, podobně jako u seznamů:

```pycon
>>> del ja['čísla']
>>> ja
{'jméno': 'Anna', 'město': 'Brno', 'jazyk': 'Python'}
```

## Vyhledávací tabulka

Trochu jiné použití slovníku, než sdružování
„různých“ typů informací, je takzvaná
*vyhledávací tabulka* (angl. *lookup table*).
V ní mají typicky všechny hodnoty stejný typ.

Taková tabulka se hodí vždycky, když je potřeba
přiřadit nějaké hodnoty jiným hodnotám.
Jako v telefonním seznamu, kde každému jménu přísluší
nějaké číslo, nebo v překladovém slovníku, kde jsou slovům
přiřazeny překlady.

```python
cisla = {
    'Maruška': '153 85283',
    'Terka': '237 26505',
    'Renata': '385 11223',
    'Michal': '491 88047',
}

barvy = {
    'hruška': 'zelená',
    'jablko': 'červená',
    'meloun': 'zelená',
    'švestka': 'modrá',
    'ředkvička': 'červená',
    'zelí': 'zelená',
    'mrkev': 'červená',
}
```

## Iterace

Když dáš slovník do cyklu `for`, dostaneš klíče:

```pycon
>>> popisy_funkci = {'len': 'délka', 'str': 'řetězec', 'dict': 'slovník'}
>>> for klic in popisy_funkci:
...     print(klic)
str
dict
len
```

Pokud chceš hodnoty, stačí použít metodu `values`:

```pycon
>>> for hodnota in popisy_funkci.values():
...     print(hodnota)
řetězec
slovník
délka
```

Většinou ale potřebuješ jak klíče tak hodnoty.
K tomu mají slovníky metodu `items`,
která bude v cyklu `for` dávat dvojice:

```pycon
>>> for klic, hodnota in popisy_funkci.items():
...     print('{}: {}'.format(klic, hodnota))
str: řetězec
dict: slovník
len: délka
```

> [note]
> Existuje i metoda `keys()`, která vrací klíče.
>
> To, co `keys()`, `values()` a `items()` vrací, jsou speciální objekty,
> které kromě použití ve `for` umožňují další
> operace: například pracovat s klíči jako s množinou.
> V [dokumentaci](https://docs.python.org/3.0/library/stdtypes.html#dictionary-view-objects)
> Pythonu je to všechno popsáno.

V průběhu takového `for` cyklu nesmíš
do slovníku přidávat záznamy, ani záznamy odebírat:

```python
>>> for klic in popisy_funkci:
...     del popisy_funkci[klic]
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
RuntimeError: dictionary changed size during iteration
```

Hodnoty u už existujících klíčů ale měnit můžeš.


## Jak udělat slovník

Slovník se dá vytvořit dvěma způsoby.
První, pomocí {složených závorek}, jsme už viděl{{gnd('i', 'y', both='i')}};
další využívají funkci `dict`.
Ta, ve stylu `str`, `int` či `list`, převede cokoli, co jde, na slovník.

Slovník je ovšem dost specifická struktura –
čísla nebo typické seznamy na něj převádět nejdou.
Můžeme ale na slovník převést *jiný slovník*.
Nový slovník žije svým vlastním životem;
následné změny se promítnou jen do něj.

```python
barvy_po_tydnu = dict(barvy)
for klic in barvy_po_tydnu:
    barvy_po_tydnu[klic] = 'černo-hnědo-' + barvy_po_tydnu[klic]
print(barvy['jablko'])
print(barvy_po_tydnu['jablko'])
```

Druhá věc, která jde převést na slovník, je
*sekvence dvojic* klíč/hodnota:

```python
data = [(1, 'jedna'), (2, 'dva'), (3, 'tři')]
nazvy_cisel = dict(data)
```

A to je vše, co se na slovník dá převést.

Jako bonus umí funkce `dict` ještě
brát pojmenované argumenty.
Každé jméno argumentu převede na řetězec,
použije ho jako klíč, a přiřadí danou hodnotu:

```python
popisy_funkci = dict(len='délka', str='řetězec', dict='slovník')
print(popisy_funkci['len'])
```

> [note]
> Pozor na to, že v tomhle případě musí být klíče
> pythonní „jména“ – musí být použitelné jako jména proměnných.
> Například takhle nejde zadat jako klíč řetězec
> `"def"` nebo `"propan-butan"`.

Pojmenované argumenty jde kombinovat s ostatními
způsoby vytvoření `dict`.


## A to je zatím ke slovníkům vše

Chceš-li mít všechny triky, které  slovníky umí,
pěkně pohromadě, můžeš si stáhnout
[Slovníkový tahák](https://pyvec.github.io/cheatsheets/dicts/dicts-cs.pdf).

Kompletní popis slovníků najdeš
v [dokumentaci](https://docs.python.org/3.0/library/stdtypes.html#mapping-types-dict)
Pythonu.
