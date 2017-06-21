Moduly
======

Zatím jsme tvořili programy v Pythonu tak nějak na divoko, tedy v jednom nebo
více souborech bez nějakého zvláštního řádu. V této lekci se podíváme na
to, jak tvořit redistribuovatelné moduly, které jdou nahrát na PyPI (veřejný
seznam pythonních balíčků) a instalovat pomocí pipu.

Za příklad si vezmeme kód Ondřeje Caletky, který umožňuje určit české svátky
v zadaném roce. Jako příklad je ideální, protože obsahuje jak funkce, které
můžeme volat z Pythonu, tak lze volat z příkazové řádky.

 * [oskar456/isholiday.py](https://gist.github.com/oskar456/e91ef3ff77476b0dbc4ac19875d0555e)


Volání z příkazové řádky, pomocí příkazu `python isholiday.py` nebo
`python -m isholiday`, zajišťuje blok `if __name__ == '__main__':`.
Toto je rychlý způsob, jak napsat modul který jde jak importovat, tak spustit.
Když nějaký modul importujeme, má v proměnné `__name__` k dispozici své jméno.
„Hlavní” modul ale není importován a jeho jméno není vždy k dispozici
(např. v `cat isholiday.py | python`).
Python proto `__name__` „hlavního” modulu nastavuje na `'__main__'`,
čehož se často využívá.

Později se podíváme na elegantnější způsob jak to zařídit; teď se vraťme
zpět k balíčkování.

setup.py
--------

Základním stavebním kamenem Python balíčku je soubor `setup.py`, který
obsahuje všechna potřebná metadata ve volání funkce `setup()` z modulu
`setuptools`.

Pojďme vytvořit jeho minimální variantu:

```python
from setuptools import setup


setup(
    name='isholiday',
    version='0.1',
    description='Finds Czech holiday for given year',
    author='Ondřej Caletka',
    author_email='ondrej@caletka.cz',
    license='Public Domain',
    url='https://gist.github.com/oskar456/e91ef3ff77476b0dbc4ac19875d0555e',
    py_modules=['isholiday'],
)
```

Všimněte si, že jsme balíček pojmenovali stejně jako soubor se zdrojovým kódem.
Je to dobrá konvence, ale není to technicky nutné.

Balíček můžeme zkusit nainstalovat do virtualenvu:

```console
$ python3.5 -m venv env     # (nebo jinak -- podle vašeho OS)
$ . env/bin/activate        # (nebo jinak -- podle vašeho OS)
(env)$ python setup.py install
...
(env)$ python
>>> import isholiday
>>> 
(env)$ python -m pip freeze
isholiday==0.1
```

Přes `setup.py` můžeme dělat další věci, například vytvořit archiv s balíčkem:

```console
(env)$ python setup.py sdist
...
warning: sdist: standard file not found: should have one of README, README.rst, README.txt
...
```

Extra soubory do zdrojového balíčku
-----------------------------------

Jak vidíte, `setuptools` si stěžuje, že náš projekt nemá `README` – soubor,
do kterého se tradičně píšou základní informace o projektu.
Můžeme jej vytvořit a uložit jako `README` přímo v kořenovém adresáři projektu,
tedy tam, kde byste jej nejspíš čekali.

```
Czech public holiday checker...
```

Poté spustíme `setup.py sdist` znovu:

```console
(env)$ python setup.py sdist
```

V adresáři `dist` najdete archiv, jeho obsah můžete zkontrolovat. Měl by tam
být i soubor `README`.

Skvělé, pojďme vytvořit i další speciální soubor, `LICENSE`, který bude
obsahovat text licence, v tomto případě Public Domain.
Obsah najdete třeba na [CC0].

[CC0]: https://creativecommons.org/publicdomain/zero/1.0/legalcode.txt

Pokud ale se souborem `LICENSE` vytvoříte zdrojový balíček, soubor v archivu
nebude. Je to proto, že se standardně do archivu přidávají jen některé soubory.
Další soubory lze přidat pomocí souboru `MANIFEST.in`, dle [dokumentace].

[dokumentace]: https://docs.python.org/3/distutils/sourcedist.html#specifying-the-files-to-distribute

V našem případě bude `MANIFEST.in` vypadat takto:

```
include LICENSE
```

Při dalším spuštění už `setup.py` přidá i soubor `LICENSE`.
To můžete zkontrolovat i ve výsledném archivu.

```console
(env)$ python setup.py sdist
...
hard linking LICENSE -> isholiday-0.1
hard linking MANIFEST.in -> isholiday-0.1
hard linking README -> isholiday-0.1
...
```

Hotový balíček pak můžete nainstalovat pomocí nástroje `pip`.
Doporučuji to dělat v jiném virtuálním prostředí – v aktuálním už ho máte
nainstalovaný.

```console
(v jiné konzoli, v jiném adresáři)
$ python3 -m venv other_env     # (nebo jinak -- podle vašeho OS)
$ . other_env/bin/activate      # (nebo jinak -- podle vašeho OS)
(other_env)$ python -m pip install cesta/k/projektu/dist/isholiday-0.1.tar.gz
Processing cesta/k/projektu/dist/isholiday-0.1.tar.gz
Installing collected packages: isholiday
  Running setup.py install for isholiday ... done
Successfully installed isholiday-0.1
```


Více argumentů pro setup()
--------------------------

Na chvíli se vrátíme k volání funkce `setup()` a přidáme co nejvíc dalších
položek.
Jejich vysvětlení najdete [v dokumentaci](https://packaging.python.org/distributing/#setup-args).

```python
from setuptools import setup


with open('README') as f:
    long_description = ''.join(f.readlines())


setup(
    name='isholiday',
    version='0.1',
    description='Finds Czech holiday for given year',
    long_description=long_description,
    author='Ondřej Caletka',
    author_email='ondrej@caletka.cz',
    keywords='holiday,dates',
    license='Public Domain',
    url='https://gist.github.com/oskar456/e91ef3ff77476b0dbc4ac19875d0555e',
    py_modules=['isholiday'],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: Public Domain',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Topic :: Software Development :: Libraries',
        ],
    zip_safe=False,
)
```

Všimněte si několika věcí. V první řadě v `long_description` vidíte, že jsme
pořád ještě v Pythonu a můžeme si ušetřit duplikaci nějakých informací pomocí
malého kousku kódu. Dalším zajímavým argumentem je `classifiers`. Jsou to
v podstatě takové tagy nebo strukturované informace o balíčku.
Zásadně si je nevymýšlíme sami, ale hledáme je v
[seznamu](https://pypi.python.org/pypi?%3Aaction=list_classifiers).
Tyto informace budou později vidět na [PyPI](https://pypi.python.org/pypi) a
půjde podle nich hledat.

Argument `zip_safe=False` zajistí, že se modul nainstaluje do adresáře.
Setuptools totiž mají nepříjemný zlozvyk instalovat moduly jako `zip`,
což komplikuje práci s datovými soubory (např. *templates* pro Flask).
Je proto lepší `zip_safe=False` uvést.


Více souborů s Python kódem
---------------------------

Doteď jsme vytvářeli balíček jen z jednoho zdrojového souboru `isholiday.py`.
Co ale dělat, pokud je náš projekt větší a obsahuje souborů více?
Teoreticky je možné je přidat všechny do `py_modules`, ale není to dobrý nápad.

Raději uděláme modul ve formě složky. V našem případě soubor
`isholiday.py` zatím přesuneme do `isholiday/__init__.py`:

```console
(env)$ tree
.
├── isholiday
│   └── __init__.py
├── LICENSE
├── MANIFEST.in
├── README
└── setup.py

1 directory, 5 files
```

Soubor `__init__.py` jednak značí, že adresář `isholiday` je pythonní modul,
a také obsahuje kód, který se spustí při importu modulu `isholiday`.

Musíme ještě mírně upravit `setup.py` – místo `py_modules` použijeme `packages`:

```diff
diff --git a/setup.py b/setup.py
index 3a69792..6b453ab 100644
--- a/setup.py
+++ b/setup.py
@@ -11,7 +11,7 @@ setup(
     keywords='holiday,dates',
     license='Public Domain',
     url='https://gist.github.com/oskar456/e91ef3ff77476b0dbc4ac19875d0555e',
-    py_modules=['isholiday'],
+    packages=['isholiday'],
     classifiers=[
         'Intended Audience :: Developers',
         'License :: Public Domain',
```

Případně, což je ještě lepší, můžeme použít `find_packages()`:

```python
from setuptools import setup, find_packages

setup(
    ...
    packages=find_packages(),
    ...
)
```

Momentálně máme všechen kód přímo v `__init__.py`, což sice funguje,
ale ideální to není. Dobré je mít kód v samostatných souborech a v `__init__.py`
pouze importovat veřejné rozhraní, tedy to, co budou z vašeho modulu importovat
jeho uživatelé.

Přesuňte tedy obsah `__init__.py` do `holidays.py` a do `__init__.py`
místo toho napište:

```python
from .holidays import getholidays, isholiday

__all__ = ['getholidays', 'isholiday']

```

Do `__init__.py` ideálně nepatří žádný kód kromě tohoto.

Tečka v příkazu `import` není chyba: je to zkratka pro aktuální modul.
Můžeme psát i `from isholiday.holidays import ...`,
což ale trochu ztěžuje případné přejmenování modulu.


Spouštění balíčku
-----------------

Pokusíme-li se teď program spustit pomocí `python -m isholiday`,
narazíme na problém: na rozdíl od souboru se složka s kódem takto spustit nedá:

```console
$ python -m isholiday
python: No module named isholiday.__main__; 'isholiday' is a package and cannot be directly executed
```

Namísto spuštění souboru (typicky s blokem `if __name__ == '__main__':`) totiž
Python v tomto případě hledá *soubor* pojmenovaný `__main__.py` a spustí ten.

Soubor `__main__.py` není určený k tomu, aby se z něho importovalo, proto
by měl obsahovat co nejméně kódu – ideálně jen volání funkce, která je
definovaná jinde. Vytvořte proto `__main__.py` s následujícím obsahem:

```python
from .holidays import main

main()
```

a v `holidays.py` zaměňte `if __name__ == '__main__':` za `def main():`.

Skript teď bude možné použít pomocí `python -m isholiday`.
Bude to fungovat i tehdy, když vytvoříte balíček (`python setup.py sdist`)
a nainstalujete ho v jiném virtuálním prostředí.


Programy pro příkazovou řádku
-----------------------------

Pokud chcete, aby váš modul umožňoval spouštění přímo z příkazové řádky,
bez `python -m`, měli byste použít [entrypoints].
K tomu je potřeba přidat do volání `setup` v `setup.py` příslušný argument:

[entrypoints]: https://setuptools.readthedocs.io/en/latest/setuptools.html#dynamic-discovery-of-services-and-plugins

```python
setup(
    ...
    entry_points={
        'console_scripts': [
            'isholiday_demo = isholiday.holidays:main',
        ],
    },
)
```

`isholiday_demo` je jméno *entrypointu*, tedy příkazu pro příkazovou řádku.
`isholiday.holidays:main` je pak cesta k funkci ve tvaru `modul:funkce`;
funkce může být v modulu definovaná nebo importovaná.

Skript bude možné použít, je-li aktivní prostředí, kde je nainstalován, jen
zadáním jména *entrypointu*:

```console
(env)$ python setup.py sdist
```

```console
(v jiné konzoli, v jiném virtuálním prostředí)
(other_env)$ python -m pip install --upgrade cesta/k/projektu/dist/isholiday-0.1.tar.gz
(other_env)$ isholiday_demo
...
Mon Mar 28 00:00:00 2016 True
Tue Mar 28 00:00:00 2017 False
Fri Apr 14 00:00:00 2017 True
```


Specifikace závislostí
----------------------

Balíčky na PyPI mohou záviset na dalších balíčkách. V případě `isholiday` to
potřeba není, ale v úlohách z minulých cvičení ano.

Existuje několik úrovní závislostí, ve většině případů si
vystačíte s argumentem `install_requires`.
Balíček, který závisí na knihovnách `Flask` (jakékoli verze) a
`click` (verze 6 a vyšší) by v `setup.py` měl mít:

```python
setup(
    ...
    install_requires=['Flask', 'click>=6'],
)
```

### Soubor requirements.txt

Kromě závislostí v `setup.py` se u pythonních projektů často setkáme se souborem
`requirements.txt`, který obsahuje přesné verze všech závislostí, včetně
tranzitivních – t.j. závisí-li náš balíček na `Flask` a `Flask` na `Jinja2`,
najdeme v `requirements.txt` mimojiné řádky:

```
Flask==0.11.1
Jinja2==2.8
```

Tento soubor se používá, když je potřeba přesně replikovat prostředí, kde
program běží, například mezi testovacím strojem a produkčním nasazením
webové aplikace.
Tento soubor se dá vygenerovat z aktuálního prostředí zadáním
`python -m pip freeze > requirements.txt` a balíčky v něm se dají nainstalovat
pomocí `python -m pip install -r requirements.txt`.
My ho používat nebudeme, vystačíme si s volnější specifikací závislostí
v `setup.py`.


Upload na PyPI
--------------

Balíček jde zaregistrovat a nahrát na PyPI. Původně k tomu sloužily příkazy
`setup.py` `register` a `upload`, ale tyto příkazy používají HTTP, což není
bezpečné. Prototo je lepší použít program `twine` (instalovatelný přes pip),
který používá HTTPS.

Budete si potřebovat zařídit
[účet na PyPI](https://pypi.python.org/pypi?%3Aaction=register_form),
[účet na testovací PyPI](https://testpypi.python.org/pypi?%3Aaction=register_form)
a vytvořit konfigurační soubor `~/.pypirc`:

```ini
[distutils]
index-servers=
    pypi
    pypitest

[pypi]
repository = https://pypi.python.org/pypi
username = <your user name goes here>
password = <your password goes here>

[pypitest]
repository = https://testpypi.python.org/pypi
username = <your user name goes here>
password = <your password goes here>
```

Hesla můžete vynechat, pokud je budete chtít pokaždé zadávat.

Používáte-li Windows, je potřeba nastavit proměnnou prostředí `HOME` na adresář
se souborem `.pypirc`, např:

```console
> set HOME=C:\cesta\k\nastaveni
```

Registrace projektu a nahrání na testovací PyPI se provádí pomocí dvou příkazů:
`register` zaregistruje nový projekt a `upload` nahraje samotný balíček:

```console
(env)$ twine register -r pypitest dist/isholiday-0.1.tar.gz
Registering package to https://testpypi.python.org/pypi
Registering isholiday-0.1.tar.gz
(env)$ twine upload -r pypitest dist/isholiday-0.1.tar.gz
Uploading distributions to https://testpypi.python.org/pypi
Uploading isholiday-0.1.tar.gz
[================================] 8379/8379 - 00:00:02
```

Registrace se zdaří, jen pokud jméno projektu již není zabrané.
Po úspěšném nahrání lze nahrávat další verze modulu, ale musí být novější
než ta, co už na PyPI je. Nejde tedy jednou nahraný modul přepsat.

Pro nahrání na opravdovou PyPI stačí vynechat `-r pypitest`.
Zabírat jména na opravdové PyPI jen tak není hezké vůči ostatním Pythonistům;
registrujte tedy prosím jen moduly, které budou nějak pro ostatní užitečné.


Instalace pomocí pip
--------------------

Projekt nahraný na PyPI by mělo jít nainstalovat pomocí pipu.
V případě použití ostré verze PyPI stačí k instalaci zadat název balíčku:

```console
(env)$ python -m pip install <název_balíčku>
```

Pokud však použijeme testovací PyPI, je nutné pipu říct, aby balíček hledal tam.
[Postup](https://wiki.python.org/moin/TestPyPI) uvedený v dokumentaci není
v tomto případě nejvhodnější, protože z testovací PyPI vezme jak náš balíček,
tak i případné závislosti, které mohou být zastaralé, rozbité či jinak škodlivé.

Lepší by bylo, kdyby pip nainstaloval závislosti z ostré PyPI a na testovací
hledal jen náš projekt. Toho se dá docílit přepínačem `--extra-index-url`.

```console
(env)$ python -m pip install --extra-index-url https://testpypi.python.org/pypi <název_balíčku>
```

V tomto případě pip nejdřív prohledá ostrou PyPI, a pokud nenajde požadovaný
balíček, použije testovací PyPI. Zde je potřeba dávat pozor na název projektu,
protože případné konflikty mezi ostrou a testovací PyPI se nekontrolují.
Pokud tedy máme projekt na testovací PyPI a na ostré existuje projekt se
stejným názvem, nainstaluje se ten z ostré verze.

V případě, že tento problém nastane, je možné ho částečně obejít specifikací
verze instalovaného balíčku:

```console
(env)$ python -m pip install --extra-index-url https://testpypi.python.org/pypi <název_balíčku>==0.3
```

Pokud u duplicitního projektu na ostré PyPI neexistuje požadovaná verze,
nainstaluje se náš projekt z testovací PyPI.

Jiná možnost je zadat přímo cestu k archivu s balíčkem místo jeho názvu.
Zde pak na umístění balíčku ani verzi nezáleží:

```bash
(env)$ python -m pip install https://testpypi.python.org/packages/.../<název_balíčku>-0.3.tar.gz
```

Archiv se dá najít na informační stránce o našem projektu na PyPI.


Datové soubory
--------------

Některé balíčky kromě samotného kódu potřebují i datové soubory.
Například aplikace ve Flasku potřebují *templates*.
Taková data se dají přidat parametrem `package_data`:

```python
setup(...,
    packages=['hello_flask'],
    ...
    package_data={'hello_flask': ['templates/*.html']},
)
```


Další informace jsou odkázané v [dokumentaci](https://packaging.python.org/distributing/#package-data).


Další
-----

K balíčkování existuje [obsáhlá dokumentace](https://packaging.python.org/).
Budete-li chtít dělat něco, co v tomto kurzu není, podívejte se tam!


Úkol
----

Úkol je k dispozici na [stránkách předmětu MI-PYT](https://github.com/cvut/MI-PYT/blob/master/tutorials/03_moduly.md#%C3%9Akol).
