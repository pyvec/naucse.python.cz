V tomto kurzu budeme používat *virtuální prostředí*.
Jedná se o oddělené prostředí pro Python, kam se dají instalovat jednotlivé
knihovny, které jsou potom aktivní jen uvnitř.
Použití prostředí má dvě hlavní výhody:

* Je-li prostředí aktivované,
  příkaz `python` spustí verzi Pythonu, se kterou bylo prostředí nainstalováno.
  Takže pak např. v materiálech nemusíme mít speciální instrukce pro
  Linux (`python3`) a Windows (`py -3`).

* Instalace knihoven nezasahuje do systémového nastavení, ani do jiných
  virtuálních prostředí.
  Můžeš tak oddělit jednotlivé projekty; v každém prostředí můžou být
  nainstalované jiné verze knihoven.
  A když se něco pokazí, adresář s virtuální prostředím můžeš prostě smazat
  a vytvořit znovu.

Následují zrychlené instrukce; předpokládám, že Python (3.4 a vyšší)
už máš nainstalovaný a že znáš základy práce
s [příkazovou řádkou]({{ lesson_url('beginners/cmdline') }})

Podrobný postup instalace Pythonu a vytvoření prostředí je je popsán
v příslušné [lekci pro začátečníky]({{ lesson_url('beginners/install') }}).
Modul `venv` je součást [standardní knihovny](https://docs.python.org/3/library/venv.html).

## Unix (Linux, MacOS)

Zkontroluj, že máš modul `ensurepip`:

```console
$ python -m ensurepip --version
pip 9.0.1 (nebo i jiná verze)
```

Jestli ne, postupuj podle [lekce pro začátečníky]({{ lesson_url('beginners/install') }}) –
jsou tam podrobnější instrukce.
Jinak použij:

```console
$ mkdir project
$ cd project
$ python3.5 -m venv __venv__  # vytvoření virtualenvu -- použij Python dle systému
$ . __venv__/bin/activate  # aktivace
(__venv__)$ python -m pip install requests  # příkaz na instalaci balíčků puštěný ve virtualenvu
(__venv__)$ ...  # práce "uvnitř"
(__venv__)$ deactivate  # vypnutí virtualenvu
```

## Windows

```console
> mkdir project
> cd project
> py -3 -m venv __venv__
> . __venv__/bin/activate
(__venv__)> python -m pip install requests  # příkaz na instalaci balíčků puštěný ve virtualenvu
(__venv__)> ...  # práce "uvnitř"
(__venv__)> deactivate  # vypnutí virtualenvu
```

<!-- XXX: Windows cmd prompt with active venv is not highlighted properly... -->

## Poznámky

Příkaz `__venv__/bin/activate` budeš muset zadat vždy než začneš na projektu
pracovat.

Ono `__venv__` je jen jméno adresáře. Můžeš si ho pojmenovat jak chceš; dokonce
nemusí být v rámci adresáře s projektem.
Někteří lidé mají všechny virtuální prostředí na jednom místě; dokonce existuje
nástroj [virtualenvwrapper] na správu takového řešení.
Autoři tohoto textu však doporučují `__venv__` v adresáři s projektem.

[virtualenvwrapper]: https://virtualenvwrapper.readthedocs.io/en/latest/

Příkaz `python -m pip install` nainstaluje danou knihovnu – může to být i jiná
než `requests` jako výše.
