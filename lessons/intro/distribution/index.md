moduly
======

Zatím jsme tvořili programy v Pythonu tak nějak na divoko, tedy v jednom nebo
více souborech bez nějakého zvláštního řádu. Na dnešním cvičení se podíváme na
to, jak tvořit redistribuovatelné moduly, které jdou instalovat pomocí pipu.

Za příklad si vezmeme kód Ondřeje Caletky, který umožňuje určit české svátky
v zadaném roce. Jako příklad je ideální, protože obsahuje jak funkce, které
můžeme volat z Pythonu, tak lze volat z příkazové řádky.

 * [oskar456/isholiday.py](https://gist.github.com/oskar456/e91ef3ff77476b0dbc4ac19875d0555e)


Volání z příkazové řádky, pomocí příkazu `python isholiday.py` nebo
`python -m isholiday`, zajišťuje blok `if __name__ == '__main__':`.
Toto je rychlý způsob, jak napsat modul který jde jak importovat, tak spustit.
Když nějaký modul importujeme, má v proměnné `__name__` k dispozici své jméno.
„Hlavní” modul ale není importován, a jeho jméno není vždy k dispozici
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

Všimněte si, že jsme balíček pojmenoval stejně jako soubor se zdrojovým kódem.
Je to dobrá konvence, ale není to technicky nutné.

Balíček můžeme zkusit nainstalovat do virtualenvu:

```bash
$ python3.5 -m venv env
$ . env/bin/activate
(env)$ python setup.py install
...
(env)$ python
>>> import isholiday
>>> 
(env)$ python -m pip freeze
isholiday==0.1
```

Přes `setup.py` můžeme dělat další věci, například vytvořit archiv s balíčkem:

```bash
(env)$ python3 setup.py sdist
...
warning: sdist: standard file not found: should have one of README, README.rst, README.txt
...
```

Extra soubory do zdrojového balíčku
-----------------------------------

Jak vidíte, `setuptools` si stěžuje, že náš projekt nemá `README`.
Můžeme jej vytvořit a uložit jako `README` přímo v kořenovém adresáři projektu,
tedy tam, kde byste jej nejspíš čekali.

```
Czech public holiday checker...
```

```bash
(env)$ python3 setup.py sdist
```

V adresáři `dist` najdete archiv, jeho obsah můžete zkontrolovat, měl by tam
být i soubor `README`.

Skvělé, pojďme vytvořit i další speciální soubor, `LICENSE`, který bude
obsahovat text licence, v tomto případě Public Domain.
Obsah najdete třeba na [CC0].

[CC0]: https://creativecommons.org/publicdomain/zero/1.0/legalcode.txt

Pokud ale se souborem `LICENSE` vytvoříte zdrojový balíček, soubor v archivu
nebude. Je to proto, že se standardně do archivu přidávají jen některé soubory.
Další soubory lze přidat pomocí souboru `MANIFEST.in`, dle [dokumentace].

[dokumentace]: https://docs.python.org/3/distutils/sourcedist.html#specifying-the-files-to-distribute

V tomto případě takto:

```
include LICENSE
```
```bash
(env)$ python3 setup.py sdist
...
hard linking LICENSE -> isholiday-0.1
hard linking MANIFEST.in -> isholiday-0.1
hard linking README -> isholiday-0.1
...
```

Více argumentů pro setup()
--------------------------

Na chvíli se vrátíme k volání funkce `setup()` a přidáme co nejvíc dalších
položek ([jejich vysvětlení](https://packaging.python.org/distributing/#setup-args)).

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
        ]
)
```

Všimněte si několika věcí. V první řadě v `long_description` vidíte, že jsme
pořád ještě v Pythonu a můžeme si ušetřit duplikaci nějakých informací pomocí
malého kousku kódu. Dalším zajímavým argumentem je `classifiers`. Jsou to
v podstatě takové tagy nebo strukturované informace o balíčku.
Nevymýšlíme je sami, ale hledáme je v
[seznamu](https://pypi.python.org/pypi?%3Aaction=list_classifiers).
Tyto informace jsou později vidět na [PyPI](https://pypi.python.org/pypi).

Více souborů s Python kódem
---------------------------

Doteď jsme vytvářeli balíček jen z jednoho zdrojového souboru `isholiday.py`.
Co ale dělat, pokud je náš projekt větší a obsahuje souborů více?
Teoreticky je možné je přidat všechny do `py_modules`, ale není to dobrý nápad.

V takovém případě uděláme modul ve formě složky. V našem případě soubor
`isholiday.py` zatím přesuneme do `isholiday/__init__.py`:

```bash
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

Soubor `__init__.py` jednak značí, že adresář `isholiday` je Pythoní modul,
také obsahuje kód, který se spustí při importu modulu `isholiday`.

Musíme ještě mírně upravit `setup.py`:

```patch
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
pouze importovat veřejné rozhraní, například takto:

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
narazíme na problém: na rozdíl od souboru se složka s kódem takto spustit nedá.
Namísto spuštění souboru (typicky s blokem `if __name__ == '__main__':`) totiž
Python v tomto případě hledá *soubor* pojmenovaný `__main__.py`, a spustí ten.

Soubor `__main__.py` není určený k tomu, aby se z něho importovalo, proto
by měl obsahovat co nejméně kódu – ideálně jen volání funkce, která je
definovaná jinde. Vytvořte proto `__main__.py` s následujícím obsahem:

```python
from .holidays import main

main()
```

a v `holidays.py` zaměňte `if __name__ == '__main__':` za `def main():`.

Skript teď bude možné použít pomocí `python -m isholiday`.


Programy pro příkazovou řádku
-----------------------------

Pokud chcete, aby váš modul umožňoval spouštění z příkazové řádky, měli byste
použít [entrypoints]:

[entrypoints]: https://setuptools.readthedocs.io/en/latest/setuptools.html#dynamic-discovery-of-services-and-plugins

```python
setup(
    entry_points={
        'console_scripts': [
            'executable_name = isholiday.holidays:main'
        ]
    },
)
```

`isholiday.holidays:main` je cesta k funkci ve tvaru `modul:funkce`, funkce může
být v modulu definovaná nebo importovaná.

Skript bude možné použít, je-li aktivní prostředí kde je nainstalován, jen
zadáním jména *entrypointu*:

    $ executable_name


Specifikace závislostí
----------------------

Balíčky na PyPI mohou záviset na dalších balíčkách. V případě `isholiday` to
potřeba není, ale v úlohách z minulých cvičení ano.

Možná jste se setkali se souborem `requirements.txt`. Pomocí `setuptools` to
jde ale lépe. Existuje několik úrovní závislostí, ve většině případů si
vystačíte s argumentem `install_requires`:

```python
setup(
    install_requires=['Flask', 'click>=6'],
)
```

Kromě závislostí v `setup.py` se u Pythoních projektů často setkáme se souborem
`requirements.txt`, který obsahuje přesné verze všech závislosti, včetně
tranzitivních – t.j. závisí-li náš balíček na `Flask`, a `Flask` na `Jinja2`,
najdeme v `requirements.txt` mimojiné řádky:

```
Flask==0.11.1
Jinja2==2.8
```

Tento soubor se používá, když je potřeba přesně replikovat prostředí, kde
program běží, například mezi testovacím strojem a produkčním nasazením
webové aplikace.
Tento soubor se dá vygenerovat z aktuálního prostředí zadáním
`python -m pip freeze > requirements.txt`, a nainstalovat pomocí
`python -m pip install -r requirements.txt`.
My ho používat nebudeme, vystačíme si s volnější specifikací závislostí
v `setup.py`.


Upload na PyPI
--------------

Balíček jde zaregistrovat a nahrát na PyPI. Původně k tomu sloužily příkazy
`setup.py` `register` a `upload`, ale tyto příkazy používají HTTP, což není
bezpečné. Prototo je lepší použít program `twine` (instalovatelný přes pip).

Budete potřebovat [účet na PyPI](https://pypi.python.org/pypi?%3Aaction=register_form).
[účet na testovací PyPI](https://testpypi.python.org/pypi?%3Aaction=register_form)
a konfigurační soubor `~/.pypirc`:

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
se souborem `.pypirc`.

Registrace projektu a nahrání na testovací PyPI se provádí pomocí:

```bash
(env)$ twine register -r pypitest dist/<soubor>
Registering package to https://testpypi.python.org/pypi
Registering <soubor>
(env)$ twine upload -r pypitest dist/<soubor>
Uploading distributions to https://testpypi.python.org/pypi
Uploading <soubor>
[================================] 8379/8379 - 00:00:02
```

Registrace se zdaří jen pokud jméno projektu již není zabrané.
Po úspěšném nahrání lze nahrát už jen novější verze modulu.

Pro nahrání na opravdovou PyPi stačí vynechat `-r pypitest`.

Další
-----

 * [instalace datových souborů](https://docs.python.org/3/distutils/setupscript.html#installing-package-data)
 * [obsáhlá dokumentace](https://packaging.python.org/)

Úkol
----

Vaším úkolem za 5 bodů je udělat z vašeho dosavadního projektu balíček
instalovatelný přes pip a nahrát jej na testovací nebo opravdovou PyPI.

Na opravdovou PyPI prosím nahrávejte pouze s rozumným názvem a pokud jde o dílo
s nějakou open-source licencí.

Pokud svůj kód za žádných okolností nechcete zveřejnit ani na testovací PyPI,
dejte nám vědět a domluvíme se.

Podmínky (je jich hodně, ale jsou triviální):

 * Váš balíček musí fungovat (viz zadání předchozích úkolů) po instalaci pomocí pipu do "prázdného" virtualenvu.
 * Musí instalovat potřebné závislosti.
 * Musí obsahovat rozumný počet classsifiers a voleb pro `setup.py`.
 * Podpříkaz `sdist` nesmí skončit chybou ani vyvolat varování.
 * Musí splňovat zde uvedené konvence.
 * Hlavní skript musí jít spouštět pomocí entry pointu i pomocí `-m`.
 * Modul musí obsahovat `__init__.py` a logiku importovat z ostatních souborů.
 * Zabalený modul musí obsahovat soubor s textem licence (`LICENSE`, `COPYING`) \*
 * `long_description` musí být načten z `README`

\* Vhodnou licenci můžete najít na [choosealicense.com].
V případě, že váš kód nechcete šířit pod svobodnou licencí,
napište to do souboru vlastní podmínky. Nevymýšlejte si ale prosím vlastní
open-source licence.

[choosealicense.com]: http://choosealicense.com/

Odevzdáte tagem v0.3 v obvyklém repozitáři
(ten můžete klidně přejmenovat podle modulu - na GitHubu v *Settings*).
Odkaz na (testovací) PyPI můžete napsat někam do README, do release na GitHubu apod.
V každém případě bychom ho měli mít možnost jednoduše najít.
