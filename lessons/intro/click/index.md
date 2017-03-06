click
=====

{% if var('mi-pyt') %}
Nechme internety na chvíli být a pojďme se podívat na úplně jinou knihovnu,
[click].
{% endif %}

Knihovna `click` slouží k vytváření rozhraní pro příkazovou řádku.
Primárně to je zpracování argumentů, ale Click umí zjednodušit i výstup.

## Argumenty příkazové řádky

Nástroje na zpracování argumentů z CLI jsou i přímo ve standardní knihovně,
a dokonce jich není málo: [os.environ], [argparse], [optparse], [getopt].
S knihovnou `click` je ale práce mnohem příjemnější, a výsledky většinou
lépe odpovídají zavedeným konvencím.

Cena za jednoduchost a konzistenci je, že některé styly návrhu CLI Click
nepodporuje.
Máš-li existující rozhraní které chceš jen převést do Pythonu,
nebude nejspíš Click správná volba.

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

Knihovna `click` toho umí mnohem víc – skupiny příkazů, argumenty,
vypisování obarveného textu, interakltivní prvky, nebo editaci souborů.
Všechno je popsáno v [dokumentaci](http://click.pocoo.org/5/).

