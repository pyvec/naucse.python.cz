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




Úkol
----

Vaším úkolem je vytvořit command line aplikaci nad vybraným webovým
API, pomocí knihoven [requests] a [click].

Co by aplikace měla dělat? Můžete si vybrat:

### Twitter Wall

Twitter Wall pro terminál. Aplikace, která bude zobrazovat tweety odpovídající
určitému hledání do terminálu v nekonečné smyčce.

Aplikace načte určitý počet tweetů odpovídající hledanému výrazu, zobrazí je
a v nějakém intervalu se bude dotazovat na nové tweety (použijte API argument
`since_id`).

Pomocí argumentů půjde nastavit:

 * cesta ke konfiguračnímu souboru s přístupovými údaji
 * hledaný výraz
 * počet na začátku načtených tweetů
 * časový interval dalších dotazů
 * nějaké vlastnosti ovlivňující chování (např. zda zobrazovat retweety)

### GitHub Issues Bot

Robot (založte mu vlastní účet na GitHubu), který v intervalech projde issues
v repozitáři na GitHubu a ty neolabelované olabeluje podle zadaných pravidel.
Nezapomeňte robotovi dát přístup do vašeho testovacího repozitáře.

Pravidla by měla být nějakým způsobem konfigurovatelná
(např. páry regulární výraz → label).

Pomocí argumentů půjde nastavit:

 * cesta ke konfiguračnímu souboru s přístupovými údaji
 * který repozitář se má procházet
 * kde je soubor s definovanými pravidly
 * jak často issues kontrolovat
 * jaký label nastavit, pokud žádné pravidlo nezabralo
 * nějaké vlastnosti ovlivňující chování (např. zda má robot vyhodnocovat i komentáře, či procházet i Pull Requesty)

### Vlastní nápad

Můžete využít i jiné API (např. [Sirius] či [KOSapi]) a vymyslet vlastní aplikaci.
Zadání vám ale musí schválit cvičící **už na cvičení**, protože v dalších cvičeních na tuto
aplikaci budeme nabalovat další a další funkce.
 
[Sirius]: https://github.com/cvut/sirius/wiki
[KOSapi]: https://kosapi.fit.cvut.cz/projects/kosapi/wiki
