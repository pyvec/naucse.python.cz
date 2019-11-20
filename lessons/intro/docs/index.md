Dokumentace
===========

Jednou ze zásadních součástí každého kvalitního Python projektu je dokumentace.
Protože chceme, abyste vytvářeli kvalitní projekty, podíváme se tedy i na
dokumentaci.

Sphinx
------

Nejpoužívanějším nástrojem na vytváření dokumentace Python projektů je [Sphinx].
Když jste se dívali do dokumentace Flasku, requests, clicku, flexmocku, pytestu,
betamaxu či Pythonu samotného, viděli jste dokumentaci vytvořenou ve Sphinxu.

[Sphinx]: http://www.sphinx-doc.org/

Pro vytvoření základní kostry dokumentace se používá jednoduchý průvodce,
`sphinx-quickstart`.

Postupujte podle následující ukázky. Jsou v ní zobrazeny jen věci,
kde nestačí nechat výchozí hodnota; u ostatních otázek (dostanete-li je)
stačí výchozí hodnotu potvrdit (<kbd>Enter</kbd>).

```ansi
␛[36m$␛[0m . __venv__/bin/activate
␛[36m(__venv__) $␛[0m python -m pip install sphinx
␛[36m(__venv__) $␛[0m mkdir docs
␛[36m(__venv__) $␛[0m cd docs
␛[36m(__venv__) $␛[0m sphinx-quickstart
␛[01mWelcome to the Sphinx 1.8.1 quickstart utility.␛[39;49;00m

Please enter values for the following settings (just press Enter to
accept a default value, if one is given in brackets).

␛[01mSelected root path: .␛[39;49;00m

You have two options for placing the build directory for Sphinx output.
Either, you use a directory "_build" within the root path, or you separate
"source" and "build" directories within the root path.
␛[35m> Separate source and build directories (y/n) [n]: ␛[39;49;00m

The project name will occur in several places in the built documentation.
␛[35m> Project name: ␛[39;49;00mcoolthing
␛[35m> Author name(s): ␛[39;49;00mPythonista Dokumentarista
␛[35m> Project release []: ␛[39;49;00m 0.1

...

␛[01mFinished: An initial directory structure has been created.␛[39;49;00m
```

Průvodce vytvoří ve složce `docs` několik souborů:

* `conf.py` – konfigurační soubor,
* `index.rst` – vlastní text dokumantace,
* `Makefile`, `make.bat` – spouštěcí soubory,
* `_static` –  adresář na obrázky, CSS apod.,
* `_templates` – Adresář na vlastní šablony,
* `_build` – adresář pro výstup, tedy hotovou dokumentaci.

Do gitu patří všechny nyní vytvořené soubory, kromě složky `docs/_build`,
která by měla být ignorována.

Zatím se nebudeme zabývat obsahem těchto souborů, ale zkusíme základní kostru
dokumentace sestavit do HTML.

> [note]
> Sphinx umí generovat dokumentaci ve více formátech (LaTeX,
> manuálové stránky atd.), pro nás bude podstatné především HTML.

```console
(__venv__) $ make html
...
The HTML pages are in _build/html.
```

Ve zmíněné složce byste měli najít `index.html`, ten si můžete prohlédnout
v prohlížeči.

Textový obsah v dokumentaci
---------------------------

Text dokumentace začíná v souboru `index.rst` a píše se ve značkovacím formátu
[reStructuredText] neboli rst.
Ten se od Markdownu liší v syntaxi, která je komplikovanější na
psaní, ale umožňuje dělat komplexnější věci.

> [note]
> Dokumentaci [lze psát i ve formátu Markdown][sphinx-md],
> ale tato možnost je poměrně nová.
> Jazyk Markdown nebyl navržen pro složitější strukturované texty
> a nepodporuje přímo všechny možnosti, které Sphinx nabízí.
> V dokumentaci se tak dočtete, jak chybějící možnosti doplnit
> [vložením reStructuredText do Markdownového dokumentu][eval_rst].
> My budeme používat reStructuredText.

Pro přehled o tom, co reStructuredText umí a jakou má syntaxi,
můžete použít [přehled] z dokumentace Sphinxu, případně [tahák].

[reStructuredText]: http://www.sphinx-doc.org/en/stable/rest.html
[přehled]: http://www.sphinx-doc.org/en/stable/rest.html
[tahák]: https://github.com/ralsina/rst-cheatsheet

[sphinx-md]: https://www.sphinx-doc.org/en/master/usage/markdown.html
[eval_rst]: https://recommonmark.readthedocs.io/en/latest/auto_structify.html#embed-restructuredtext

V `index.rst` je seznam kapitol:

```rst
.. toctree::
   :maxdepth: 2
   :caption: Contents:
```

Tam můžete přidat další kapitoly:

```rst
.. toctree::
   :maxdepth: 2
   :caption: Contents:

   intro
   tutorial/foo
   tutorial/bar
   ...
```

Soubory s kapitolami je třeba vytvořit ve složce `docs` s příponou `.rst`
(např. `tutorial/foo.rst`).
Text lze pak přidávat samozřejmě do těchto souborů i do
`index.rst`.

Chcete-li odkazovat na některou sekci, označíme si ji pomocí `.. _label:`:

```rst
.. _my-reference-label:

Section to cross-reference
--------------------------

This is the text of the section.
```

Poté na ni lze odkazovat odkudkoli z dokumentace pomocí
[konstrukce ref]:

```rst
It refers to the section itself, see :ref:`my-reference-label`.
It could refer to a different section as well :)
```

[konstrukce ref]: http://www.sphinx-doc.org/en/master/markup/inline.html#role-ref


Co do dokumentace psát
----------------------

Teď, když víte jak něco napsat, pojďme si povědět *co* vlastně psát.
K čemu dokumentace vlastně je?

Dobrá dokumentace vysvětluje, proč a jak by váš projekt měl někdo používat.
Jak říká Eric Holscher v [jedné své prezentaci](http://www.writethedocs.org/guide/writing/beginners-guide-to-docs/),

> Když lidi neví, že váš projekt existuje,<br>
> nebudou ho používat.<br>
> Když lidi nepřijdou na to, jak váš projekt nainstalovat,<br>
> nebudou ho používat.<br>
> Když lidi nepřijdou na to, jak váš projekt použít,<br>
> nebudou ho používat.<br>

Pokud pracujete v malém týmu, teoreticky jde to všechno kolegům prostě říct,
ale potom se musíte spoléhat na to, že to nezapomenete (a neodejdete z týmu).
Mnohem lepší je dokumentaci sepsat co nejdřív, dokud máte všechno čerstvě
v hlavě.

Nechce-li se vám nastavovat Sphinx, můžete informace napsat aspoň do malého
README. Ale i tam by měl být stejný druh informací jako ve „velké“ dokumentaci.

Na první stránce dokumentace (nebo v README) typicky najdeme:

* krátký text o tom, co projekt dělá;
* ukázku – u knihovny příklad kódu, u aplikace screenshot, u webové aplikace
  odkaz na běžící instanci;
* návod na instalaci;
* odkazy na zbytek dokumentace;
* odkazy pro přispěvatele – kde je repozitář, kde nahlásit chybu;
* licenci.

Delší dokumentace knihoven pak většinou obsahuje:

* tutoriál – návod, který uživatele provede použitím a možnostmi knihovny;
* popis architektury, návrhu, použitých konceptů;
* dokumentaci API – popis všech veřejných modulů, tříd, funkcí a podobně;
* podrobný návod jak přispívat.


Nastavení a rozšíření
---------------------

Průvodce `sphinx-quickstart` generuje soubor s nastavením, `conf.py`,
ve kterém můžete měnit nastavení Sphinxu a jeho rozšíření, včetně detailů
jako jméno a verze projektu.

Průvodce automaticky aktivuje tři rozšíření, která jsou obecně užitečná.
To se ale může v jiných verzích Sphinxu měnit, proto teď nastavení
zkontrolujte a případně rozšíření doplňte:

```python
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.doctest',
    'sphinx.ext.intersphinx',
]
```


doctest
-------

`doctest` je modul ze standardní knihovny, který najde v dokumentaci bloky kódu
a otestuje, jestli odpovídají ukázanému výstupu.
Rozšíření `sphinx.ext.doctest` integruje `doctest` do dokumentů
ve formátu reStructuredText.

Pro nás to bude způsob, jak testovat *dokumentaci* – tedy jestli jsou ukázky
kódu v ní stále platné.
Dá se sice použít i k testování samotného kódu, ale na to existují
[lepší nástroje]({{lesson_url('intro/testing')}}).

Můžete to dělat dvěma způsoby. První je mít v dokumentaci
příklad vypadající jako interaktivní konzole.
Takový příklad nemusí být odsazený ani ničím uvozený; stačí `>>>` na začátku.

```pycon
>>> 1 + 1
2
```

Doctest v tomto případě otestuje, že vše funguje, jak má.
V tomto případě se provede součet a zkontroluje se, zda výsledek je 2.

Druhý způsob je mít v dokumentaci nejdříve kód:

```python
print('foo')
```

A dále někde jinde výstup volání:

```python
foo
```

K tomu všemu složí několik direktiv:

### .. testsetup::

Direktiva pro potřebný kód, který se musí provést, aby příklad fungoval, ale
nebude v dokumentaci zobrazen (např. kód pro vytvoření falešného objektu,
import...).

### .. testcleanup::

Podobná direktiva jako `.. testsetup::` provedená po skončení testů.
V dokumentaci nebude kód zobrazen.

### .. doctest::

Test s interaktivní konzolí. V dokumentaci bude zobrazen, pokud nepoužijete flag
`:hide:`.

### .. testcode::

Kód testu bez interaktivní konzole, co chcete kontrolovat, musíte dát na
standardní výstup. V dokumentaci bude zobrazen, pokud nepoužijete flag
`:hide:`.

### .. testoutput::

Výstup posledního testcode bloku. V dokumentaci bude kód zobrazen, pokud
nepoužijete flag `:hide:`.

### Kompletní příklad

Zde můžete vidět výše zmíněné direktivy použité dohromady.
Jedná se o umělý příklad, kdy použitou třídu připravíme v direktivě `testsetup`.
V praxi pak doctestem testujeme, jestli naše dokumentace odpovídá chování
naší implementace, třídu `Parrot` bychom tedy odněkud naimportovali.

```rst
The parrot module
=================

.. testsetup::

   class Parrot:
       def voom(self, voltage):
           print('This parrot wouldn\'t voom if you put {} volts through it!'.format(voltage))

       def die(self):
           return 'RIP'


   parrot = Parrot()

The parrot module is a module about parrots.

Doctest example:

.. doctest::

   >>> parrot.voom(3000)
   This parrot wouldn't voom if you put 3000 volts through it!

Test-Output example:

.. testcode::

   parrot.voom(3000)

This would output:

.. testoutput::

   This parrot wouldn't voom if you put 3000 volts through it!

You can use other values:

.. testcode::

   parrot.voom(230)

.. testoutput::
   :hide:

   This parrot wouldn't voom if you put 230 volts through it!


.. testcleanup::

   parrot.die()
```

Testy se také dají např. zařazovat do skupin. Více najdete
v [dokumentaci](http://www.sphinx-doc.org/en/master/ext/doctest.html).

```console
(__venv__) $ make doctest
...
Document: intro
---------------
1 items passed all tests:
   3 tests in default
3 tests in 1 items.
3 passed and 0 failed.
Test passed.
1 items passed all tests:
   1 tests in default (cleanup code)
1 tests in 1 items.
1 passed and 0 failed.
Test passed.

Doctest summary
===============
    3 tests
    0 failures in tests
    0 failures in setup code
    0 failures in cleanup code
...
```

### Import z vlastního kódu

Pokud nemáte nainstalovaný vlastní balíček a budete z něj chtít v doctestu
importovat, pravděpodobně dostanete `ImportError`.
V takovém případě pomůže drobná editace na začátku `conf.py`.
Musíte přidat adresář, ze kterého lze váš kód importovat, do `sys.path`.
Pokud jste postupovali podle návodu výše, máte dokumentaci v adresáři `docs`,
je tedy potřeba přidat nadřazený adresář (`..`):

```python
# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys
sys.path.insert(0, os.path.abspath('..'))
```

### Travis CI

Neexistuje zatím unifikovaný způsob, jak specifikovat závislosti pro sestavení
dokumentace. Proto, pokud chcete mít nějaký jednoduchý způsob, jak pouštět
doctesty na Travisu, vytvořte například soubor `docs/requirements.txt`
a do něj dejte závislosti potřebné pro sestavení dokumentace.
Je na vás, jestli tam budou pouze extra závislosti oproti těm v `setup.py`
(většinou pouze `sphinx`), nebo všechny závislosti, aby šel použít soubor
samostatně.

Poté na Travisu můžete udělat něco jako:

```yaml
language: python
python:
- '3.7'
install:
- python setup.py install
- pip install -r docs/requirements.txt
script:
- python setup.py test --addopts -v
- cd docs && make doctest
```

> [note]
> Chcete-li jít s dobou, můžete vyzkoušet strukturovaný způsob závislostí
> pro vývoj pomocí *extras*. Aktuálně pro to neexistuje standard,
> ale vypadá to, že následující způsob je nejlepší kandidát na
> standardizaci.
>
> Do `setup.py` přidejte:
>
> ```python
> extras_require={
>     'dev':  ["sphinx"],
> }
> ```
>
> Projekt pak lze nainstalovat pomocí `.[dev]` (tedy jméno balíčku a za ním
> jméno *extras* v hranatých závorkách):
>
> ```
> install:
> - python -m pip install .[dev]
> ```


autodoc
-------

Pro dokumentaci API lze použít `sphinx.ext.autodoc`, další rozšíření Sphinxu,
které průvodce přidává automaticky.

> [note]
> Nemáte-li toto rozšíření povolené, přidejte jej do `conf.py`:
>
> ```python
> extensions = [
>     'sphinx.ext.autodoc',
>     'sphinx.ext.doctest',
>     'sphinx.ext.intersphinx',
> ]
> ```

Rozšíření `autodoc` se používá takto:

```rst
.. automodule:: mymodule
   :members:
```

Tento příklad na dané místo vygeneruje dokumentaci složenou z dokumentačních
řetězců jednotlivých funkcí, tříd a metod v modulu `mymodule`.

Pokud chcete selektivně vybrat, dokumentaci čeho chcete generovat,
můžete použít i
[jiné direktivy](http://www.sphinx-doc.org/en/master/ext/autodoc.html#directive-automodule).

Pro vygenerování hezké struktury si můžete pomoci příkazem `sphinx-apidoc`:

```console
(__venv__) $ sphinx-apidoc -o docs mymodule
```

V dokumentačních řetězcích samozřejmě můžete použít [reStructuredText] a je to
dokonce žádoucí.

Zde je ukázka z betamaxu (*Copyright 2013 Ian Cordasco*):

```python
class Betamax:

    """This object contains the main API of the request-vcr library.

    This object is entirely a context manager so all you have to do is:

    .. code::

        s = requests.Session()
        with Betamax(s) as vcr:
            vcr.use_cassette('example')
            r = s.get('https://httpbin.org/get')

    Or more concisely, you can do:

    .. code::

        s = requests.Session()
        with Betamax(s).use_cassette('example') as vcr:
            r = s.get('https://httpbin.org/get')

    This object allows for the user to specify the cassette library directory
    and default cassette options.

    .. code::

        s = requests.Session()
        with Betamax(s, cassette_library_dir='tests/cassettes') as vcr:
            vcr.use_cassette('example')
            r = s.get('https://httpbin.org/get')

        with Betamax(s, default_cassette_options={
                're_record_interval': 1000
                }) as vcr:
            vcr.use_cassette('example')
            r = s.get('https://httpbin.org/get')
    """
```

Existují různé způsoby, jak dokumentovat argumenty, návratové hodnoty apod.
Zvídavým studentům doporučujeme podívat se na rozšíření [Napoleon].

[Napoleon]: http://www.sphinx-doc.org/en/master/ext/napoleon.html


Odkazy na třídy a moduly
------------------------

Máte-li zdokumentovaný modul, funkci, třídu, metodu apod., je možné na ni
odkázat pomocí konstrukce `:mod:`, `:func:`, `:class:`, `:meth:` a dalších
ze Sphinxové [domény Python]:

```rst
To test the parrot's electrical resistance, use :meth:`parrot.voom()`.
```

V této části dokumentace Sphinxu též najdete způsob, jak dokumentovat API
bez použití `autodoc`.

Všechny zdokumentované objekty se automaticky přidávají do rejstříku.
Chcete-li do rejstříku přidat něco navíc, použijte direktivu [index].

[domény Python]: http://www.sphinx-doc.org/en/master/domains.html#cross-referencing-python-objects
[index]: http://www.sphinx-doc.org/en/master/markup/misc.html#index-generating-markup


README.rst
----------

Když už se stejně zabýváme [reStructuredText]em, je dobré váš README přepsat
nebo převést do stejného formátu. Na PyPI pak bude váš projekt vypadat lépe.

Při přejmenování na `README.rst` dejte pozor na patřičné změny v `setup.py`.

Read the Docs
-------------

Pokud svůj repositář na GitHubu změníte na veřejný, můžete využít službu
[Read the Docs] k hostování dokumentace ve Sphinxu.
Dokumentace se sestaví při každém pushnutí na GitHub.

Pokud Read the Docs použijete, nezapomeňte na dokumentaci odkázat
z `README.rst`.

[Read the Docs]: https://readthedocs.org/
