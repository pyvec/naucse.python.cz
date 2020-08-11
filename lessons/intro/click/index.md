click
=====

{% if var('mi-pyt') %}
Nechme internety na chvíli být a pojďme se podívat na úplně jinou knihovnu,
[click](https://click.palletsprojects.com/en/7.x/).
{% endif %}

Knihovna `click` slouží k vytváření rozhraní pro příkazovou řádku
(angl. *command line interface*, CLI).
Primárně to je zpracování argumentů, ale click umí zjednodušit i výstup.

Click je dobré používat s knihovnou `colorama`, která se stará o obarvování
textu na příkazové řádce ve Windows (a na Unixu nedělá nic).
Nainstalujte si tedy obě:

```console
$ python -m pip install click colorama
```


## Argumenty příkazové řádky

Nástroje na zpracování argumentů z CLI jsou i přímo ve standardní knihovně,
a dokonce jich není málo: [sys.argv], [argparse], [optparse], [getopt].
S knihovnou `click` je ale práce mnohem příjemnější a výsledky většinou
lépe odpovídají zavedeným konvencím.

> [note]
> Cena za jednoduchost a konzistenci je, že některé styly návrhu CLI click
> nepodporuje.
> Máte-li existující rozhraní, které chcete jen převést do Pythonu,
> click nejspíš nebude nejlepší volba.

[sys.argv]: https://docs.python.org/3/library/sys.html#sys.argv
[argparse]: https://docs.python.org/3/library/argparse.html
[optparse]: https://docs.python.org/3/library/optparse.html
[getopt]: https://docs.python.org/3/library/getopt.html

Takto jednoduše se dá vytvořit aplikace s přepínači:

```python
import click

@click.command()
@click.option('--count', default=1,  metavar='COUNT',
              help='Number of greetings.')
@click.option('--name', prompt='Your name', metavar='NAME',
              help='The person to greet.')
def hello(count, name):
    """Simple program that greets NAME for a total of COUNT times."""
    for x in range(count):
        click.echo(f'Hello {name}!')

if __name__ == '__main__':
    hello()
```

Vyzkoušejte si ji! Máte-li ji uloženou jako `hello.py`, zkuste:

```console
$ python hello.py
$ python hello.py --help
$ python hello.py --name Pythonista
$ python hello.py --count 5
```


## Příkazy a přepínače

Funkce s dekorátorem `@click.command` je *příkaz* – když ji zavoláte,
click zpracuje argumenty příkazové řádky a zavolá původní funkci
s příslušnými pythonními hodnotami.
Proto se dává do bloku `if __name__ == '__main__':`, který se spustí, jen
když se pythonní soubor spoustí „přímo“.
Když je soubor importován, tenhle blok se neprovede.

Dekorátory `@click.option` a `@click.argument` pak přidávají přepínače
a argumenty.

[*Přepínače*](https://click.palletsprojects.com/en/7.x/options/) (angl. *options*), přidávané pomocí `option`, jsou nepovinné
parametry, kterými se nějak obměňuje chování programu.
Pokud uživatel nějaký přepínač nezadá, použije se hodnota zadaná jako `default`
(nebo `None`, když `default` chybí).

Podle `default` se řídí i typ argumentu, není-li dán explicitně.
Takže `count` v příkladu výše je celé číslo.

Jména přepínačů začínají, podle Unixové konvence, pomlčkami: jednou pomlčkou
pro jednopísmenné zkratky, dvěma pomlčkami pro vícepísmenná jména.
Jeden přepínač může mít i víc jmen.

Speciální případ jsou booleovské přepínače, které mají jedno jméno
pro `True` a jiné pro `False`. Lze samozřejmě také vytvořit bezhodnotový
přepínač pomocí `is_flag`.

```python
import click

@click.command()
@click.option('-n', '--name', default='world',
              help='Name of the person to greet')
@click.option('-c/-C', '--color/--no-color',
              help='Make the output colorful')
@click.option('-v', '--verbose', is_flag=True,
              help='More verbose output')
def hello(name, color, verbose):
    if color:
        name = click.style(name, fg='blue')
    click.echo(f'Hello {name}!')
    if verbose:
        click.echo('Nice to meet you.')

if __name__ == '__main__':
    hello()
```

```console
$ python hello.py
Hello world!
$ python hello.py --name Guido
Hello Guido!
$ python hello.py --name Jane -v
Hello Jane!
Nice to meet you.
$ python hello.py -n 'Mr. Git'
Hello Mr. Git!
$ python hello.py --help
Usage: hello.py [OPTIONS]

Options:
  -n, --name TEXT               Name of the person to greet
  -c, --color / -C, --no-color  Make the output colorful
  --help                        Show this message and exit.
```

Přepínač `--help` přidává click sám.


## Argumenty

Kromě přepínačů podporuje click i [*argumenty*](https://click.palletsprojects.com/en/7.x/arguments/).
Přepínače musí uživatel na řádce pojmenovat; argumenty se zadávají beze jména,
ale záleží u nich na pořadí.
Používají se ve dvou případech: pro povinné parametry a pro parametry, kterých
může být zadán libovolný počet.
Na všechno ostatní radši použijte přepínače.

Například příkaz `cd` potřebuje jeden argument: jméno adresáře,
do kterého má přepnout.
Jeho rozhraní by v clicku vypadalo takto:

```python
@click.command()
@click.argument('directory')
def cd(directory):
    """Change the current directory"""
    click.echo(f'Changing to directory {directory}')
```

Proměnný počet argumentů se zadává pomocí `nargs=-1` (0 nebo víc argumentů)
nebo `nargs=-1, required=True` (1 nebo víc).

Například příkaz `mv` bere <var>N</var> souborů a adresář, kam je přesune.
Takové rozhraní by v clicku vypadalo následovně:

```python
@click.command()
@click.argument('source', nargs=-1, required=True)
@click.argument('destination')
def mv(source, destination):
    """Move any number of files to one destination"""
    for filename in source:
        click.echo(f'Moving {filename} to {destination}')
```


## Soubory

Má-li uživatel zadat jméno souboru, nepoužívejte řetězce, ale speciální typ
[`click.File()`](https://click.palletsprojects.com/en/7.x/api/#click.File).
Click za vás soubor automaticky otevře a zavře.
Kromě toho podporuje unixovskou konvenci, že `-` znamená standardní
vstup/výstup.

Argument pro `File` je mód, ve kterém se soubor otevírá, podobně jako pro
funkci [`open`](https://docs.python.org/3/library/functions.html#open):
`'r'` pro čtení, `'w'` pro zápis.

```python
@click.command()
@click.argument('files', nargs=-1, type=click.File('r'))
def cat(files):
    """Print out the contents of the given files"""
    for file in files:
        print(file.read(), end='')
```

Existuje i varianta [`click.Path()`](https://click.palletsprojects.com/en/7.x/api/#click.Path),
která soubor neotvírá. Pomocí ní jde např. zadat jméno adresáře. Click takto 
poskytuje i jiné [další typy](https://click.palletsprojects.com/en/7.x/api/#types).


## Validace vstupů

Vstupy získané z přepínačů i argumentů lze ověřit pomocí 
vlastních podmínek a podle toho naprogramovat chování včetně
chybových hlášek. Click však opět nabízí pohodlnější způsob, 
a to pomocí [`callback`](https://click.palletsprojects.com/en/7.x/options/#callbacks-for-validation).
V rámci callback funkce můžete ověřit libovolně hodnotu a/nebo
ji vhodně transformovat. Pokud hodnota neodpovídá požadavkům, 
můžete použít vyjímku [`click.UsageError`](https://click.palletsprojects.com/en/7.x/api/#click.UsageError)
nebo [`click.BadParameter`](https://click.palletsprojects.com/en/7.x/api/#click.BadParameter)
(vztahuje-li se přímo ke konkrétnímu parametru). Click se pak 
sám postará o případné ukončení programu s odpovídající chybovou
hláškou a kódem.

```python
def validate_username(ctx, param, value):
    if 2 <= len(value) <= 8 and re.match('^[a-zA-Z]+[0-9]*$', value):
        return value.lower()
    else:
        raise click.BadParameter('not valid CTU username')

@click.command()
@click.option('-u', '--username', callback=validate_username)
def email(username):
    click.echo(f'{username}@fit.cvut.cz')

if __name__ == '__main__':
    email()
```


## Podpříkazy

Click má dobrou podporu pro *podpříkazy* známé z verzovacích systémů jako git:
příkaz `git` sám o sobě nedělá nic, jen sdružuje podpříkazy jako `git add`
a `git commit`.

Umí-li váš program více akcí, souhrnný příkaz označte `@click.group()`
a jednotlivé podpříkazy pak přidávejte pomocí `command()`:

```python
@click.group()
def git2():
    pass

@git2.command()
def commit():
    message = click.edit('Made some changes')
    click.echo(f'Making commit with message: {message}')

@git2.command()
@click.argument('files', nargs=-1)
def add(files):
    for file in files:
        click.echo(f'Adding {file}')
```


## A další

Tahle lekce není popis všeho, co click umí – je to jen ochutnávka,
abyste věděli, co od téhle knihovny očekávat.

Click má velice dobrou [dokumentaci], ve které najdete detaily i všechny
ostatní možnosti.

[dokumentaci]: https://click.palletsprojects.com/en/7.x/

