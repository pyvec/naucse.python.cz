click
=====

{% if var('mi-pyt') %}
Nechme internety na chvíli být a pojďme se podívat na úplně jinou knihovnu,
[click](http://click.pocoo.org/5/).
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
a dokonce jich není málo: [os.environ], [argparse], [optparse], [getopt].
S knihovnou `click` je ale práce mnohem příjemnější a výsledky většinou
lépe odpovídají zavedeným konvencím.

> [note]
> Cena za jednoduchost a konzistenci je, že některé styly návrhu CLI click
> nepodporuje.
> Máte-li existující rozhraní, které chcete jen převést do Pythonu,
> click nejspíš nebude nejlepší volba.

[os.environ]: https://docs.python.org/3/library/os.html#os.environ
[argparse]: https://docs.python.org/3/library/argparse.html
[optparse]: https://docs.python.org/3/library/optparse.html
[getopt]: https://docs.python.org/3/library/getopt.html

Takto jednoduše se dá vytvořit aplikace s přepínači:

```python
import click

@click.command()
@click.option('--count', default=1, help='Number of greetings.')
@click.option('--name', prompt='Your name',
                help='The person to greet.')
def hello(count, name):
    """Simple program that greets NAME for a total of COUNT times."""
    for x in range(count):
        click.echo('Hello {}!'.format(name))

if __name__ == '__main__':
    hello()
```


## Příkazy a přepínače

Funkce s dekorátorem `@click.command` je *příkaz* – když ji zavoláte,
click zpracuje argumenty příkazové řádky a zavolá původní funkci
s příslušnými pythonními hodnotami.
Proto se dává do bloku `if __name__ == '__main__':`, který se spustí, jen
když se pythonní soubor spoustí „přímo“.
Když je importován, tenhle blok se neprovede.

Dekorátory `@click.option` a `@click.argument` pak přidávají přepínače
a argumenty.

*Přepínače* (angl. *options*), přidávané pomocí `option`, jsou nepovinné
parametry, kterými se nějak obměňuje chování programu.
Pokud uživatel nějaký přepínač nezadá, použije se hodnota zadaná jako `default`
(nebo `None`, když `default` chybí).

Podle `default` se řídí i typ argumentu, není-li dán explicitně.
Takže `count` v příkladu výše je celé číslo.

Jména přepínačů začínají, podle Unixové konvence, pomlčkami: jednou pomlčkou
pro jednopísmenné zkratky, dvěma pomlčkami pro vícepísmenná jména.
Jeden přepínač může mít i víc jmen.

Speciální případ jsou booleovské přepínače, které mají jedno jméno
pro `True` a jiné pro `False`.

```python
import click

@click.command()
@click.option('-n', '--name', default='world',
              help='Name of the person to greet')
@click.option('-c/-C', '--color/--no-color',
              help='Make the output colorful')
def hello(name, color):
    if color:
        name = click.style(name, fg='blue')
    click.echo('Hello {}!'.format(name))

if __name__ == '__main__':
    hello()
```

```console
$ python hello.py
Hello world!
$ python hello.py --name Guido
Hello Guido!
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

Kromě přepínačů podporuje click i *argumenty*.
Přepínače musí uživatel na řádce pojmenovat; argumenty se zadávají pozičně.
Používají se ve dvou případech: pro povinné argumenty a pro argumenty, kterých
může být libovolný počet.
Na všechno ostatní radši použijte přepínače.

```python
@click.command()
@click.argument('directory')
def cd(directory):
    click.echo('Changing to directory {}'.format(directory))

@click.command()
@click.argument('source', nargs=-1)
@click.argument('destination', nargs=1)
def mv(source, destination):
    for filename in source:
        click.echo('Moving {} to {}'.format(filename, destination))
```


## Soubory

Má-li uživatel zadat jméno souboru, nepoužívejte řetězce, ale speciální typ
`click.File()`.
Click za vás soubor automaticky otevře a zavře.
Kromě toho podporuje unixovskou konvenci, že `-` znamená standardní
vstup/výstup.

```python
@click.command()
@click.argument('files', nargs=-1, type=click.File('r'))
def cat(files):
    for file in files:
        print(file.read(), end='')
```

Existuje i varianta `click.Path()`, která soubor neotvírá.


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
    click.echo('Making commit with message: {}'.format(message))

@git2.command()
@click.argument('files', nargs=-1)
def add(files):
    for file in files:
        click.echo('Adding {}'.format(file))
```


## A další

Tahle lekce není popis všeho, co click umí – je to jen ochutnávka,
abyste věděli, co od téhle knihovny očekávat.

Click má velice dobrou [dokumentaci], ve které najdete detaily i všechny
ostatní možnosti.

[dokumentaci]: http://click.pocoo.org/5/

