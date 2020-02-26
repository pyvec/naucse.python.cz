# Šablony (formátovací řetězce)

Řekněme, že chceš uživateli vypsat určitou hodnotu s nějakou „omáčkou“ okolo.
Dá se na to použít `print()`, kterému můžeš předat „mix“ řetězců a čísel:

```pycon
>>> soucet = 3 + 4
>>> print('Součet je', soucet)
```

Co ale když chceš celý tento výpis uložit do proměnné – jako jeden řetězec?
Čárka tu fungovat nebude, ta odděluje argumenty ve volání funkce.
Je potřeba `soucet` převést na řetězec a ten pak připojit k „omáčce“:


```pycon
>>> hlaska = 'Součet je ' + str(soucet)
```

To ale není tak přehledné, jak by mohlo.
Lze to zpřehlednit použitím šablony.

Takovou šablonu si představ jako formulář s vynechanými místy:

```plain
Součet je __________.
```

Složitější šablona by byla třeba tahle:

```plain
Mil[ý/á] _______,
Váš výsledek je __________.

S pozdravem,
_________
```

Aby Python věděl, do kterého vynechaného místa co doplnit, je potřeba
jednotlivá vynechaná místa ve formuláři nějak jednoznačně označit.
Použijme jména v „kudrnatých“ závorkách:

```plain
Součet je {soucet}.
```

```plain
Mil{y_a} {osloveni},
Váš výsledek je {soucet}.

S pozdravem,
{podpis}.
```

Takovou šablonu můžeš použít jako *formátovací řetězec*
(angl. [*formatted string literal*](https://docs.python.org/3.6/reference/lexical_analysis.html#formatted-string-literals),
zkráceně *f-string*).
Jako jakýkoli jiný řetězec ji vlož do uvozovek.
A aby bylo jasné, že jde o šablonu, před první uvozovky přidej navíc značku `f`.

```python
f"Součet je {soucet}."
```

Takový formátovací řetězec jde použít v Pythonu – jako jakýkoli jiný řetězec:

```python
soucet = 3 + 4
hlaska = f'Součet je {soucet}'
print(hlaska)
```

```python
y_a = 'á'
osloveni = 'Anežko'
soucet = 3 + 4
podpis = 'Váš Program'

print(f"""
Mil{y_a} {osloveni},
Váš výsledek je {soucet}.

S pozdravem,
{podpis}
""")
```

A nakonec – v šabloně můžeš použít nejen jména proměnných, ale jakékoli výrazy.

```pycon
>>> hlaska = f'Součet je {3 + 4}'
```

Ale nepřežeň to!
Většinou je program přehlednější, když si každou vypisovanou hodnotu zvlášť
pojmenuješ – tedy uložíš do vhodně pojmenované proměnné.


## Metoda format

Někdy se stane, že jednu šablonu potřebuješ použít vícekrát.
Pak formátovací řetězec použít nemůžeš, protože se do něj proměnné doplňují
automaticky a hned.
V takovém případě můžeš šablonu napsat do normálního řetězce (bez `f` na
začátku) a použít metodu `format`:

```python
sablona = 'Ahoj {jmeno}! Tvoje číslo je {cislo}.'
print(sablona.format(cislo=7, jmeno='Hynku'))
print(sablona.format(cislo=42, jmeno='Viléme'))
print(sablona.format(cislo=3, jmeno='Jarmilo'))
```

Oproti formátovacím řetězcům umí `format` užitečnou zkratku: nepojmenované
argumenty dosadí postupně do nepojmenovaných míst v šabloně:

```python
vypis = '{} krát {} je {}'.format(3, 4, 3 * 4)
print(vypis)
```

Výrazy jako `f'Součet je {3 + 4}'` ale `format` dosadit neumí.
Složitější dosazované hodnoty si proto vždycky pojmenuj.
