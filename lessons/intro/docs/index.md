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
`sphinx.quickstart`.

Postupujte podle následující ukázky. Jsou v ní zobrazeny jen věci,
kde nestačí nechat výchozí hodnota; u ostatních otázek stačí výchozí hodnotu
potvrdit (<kbd>Enter</kbd>).
K modulům `autodoc` a `doctest` se dostaneme později.

```ansi
␛[36m$␛[0m . __venv__/bin/activate
␛[36m(__venv__) $␛[0m python -m pip install sphinx
␛[36m(__venv__) $␛[0m python -m sphinx.quickstart
␛[01mWelcome to the Sphinx 1.5.5 quickstart utility.␛[39;49;00m

Please enter values for the following settings (just press Enter to
accept a default value, if one is given in brackets).

Enter the root path for documentation.
␛[35m> Root path for the documentation [.]: ␛[39;49;00mdocs

...

The project name will occur in several places in the built documentation.
␛[35m> Project name: ␛[39;49;00mcoolthing
␛[35m> Author name(s): ␛[39;49;00mPythonista Dokumentarista

Sphinx has the notion of a "version" and a "release" for the
software. Each version can have multiple releases. For example, for
Python the version is something like 2.5 or 3.0, while the release is
something like 2.5.1 or 3.0a1.  If you don't need this dual structure,
just set both to the same value.
␛[35m> Project version []: ␛[39;49;00m0.1
␛[35m> Project release [0.1]: ␛[39;49;00m

...

Please indicate if you want to use one of the following Sphinx extensions:
␛[35m> autodoc: automatically insert docstrings from modules (y/n) [n]: ␛[39;49;00my
␛[35m> doctest: automatically test code snippets in doctest blocks (y/n) [n]: ␛[39;49;00my
␛[35m> intersphinx: link between Sphinx documentation of different projects (y/n) [n]: ␛[39;49;00my

...

␛[01mFinished: An initial directory structure has been created.␛[39;49;00m
```

Průvodce vytvoří složku `docs` a v ní několik souborů:

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
(__venv__) $ cd docs
(__venv__) $ make html
...
Build finished. The HTML pages are in _build/html.
```

Ve zmíněné složce byste měli najít `index.html`, ten si můžete prohlédnout
v prohlížeči.

Textový obsah v dokumentaci
---------------------------

Text dokumentace začíná v souboru `index.rst` a píše se ve značkovacím formátu
[reStructuredText] neboli rst. Bohužel nelze psát v Markdownu, ačkoli existují
složité triky, jak docílit nějaké konverze.

reStructuredText se od Markdownu liší v syntaxi, která je komplikovanější na
psaní, ale umožňuje dělat komplexnější věci.

Pro přehled o tom, co reStructuredText umí a jakou má syntaxi,
můžete použít [přehled] z dokumentace Sphinxu, případně [tahák].

[reStructuredText]: http://www.sphinx-doc.org/en/stable/rest.html
[přehled]: http://www.sphinx-doc.org/en/stable/rest.html
[tahák]: https://github.com/ralsina/rst-cheatsheet

V `index.rst` je seznam kapitol:

```rst
.. toctree::
   :maxdepth: 2
```

Tam můžete přidat další kapitoly:

```rst
.. toctree::
   :maxdepth: 2

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

[konstrukce ref]: http://www.sphinx-doc.org/en/1.4.8/markup/inline.html#role-ref


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
* ukázku – u knihovny příklad kódu, u aplikace screenshot, u webové stránky
  odkaz na běžící instanci;
* návod na instalaci;
* odkazy na zbytek dokumentace;
* odkazy pro přispěvatele – kde je repozitář, kde nahlásit chybu;
* licenci.

Delší dokumentace knihoven pak většinou obsahuje:

* tutoriál – návod, který uživatele provede použitím a možnostmi knihovny;
* popis architektury, návrhu, použitých konceptů;
* API dokumentaci – popis všech veřejných modulů, tříd, funkcí a podobně;
* podrobný návod jak přispívat.


doctest
-------

`doctest` je modul ze standardní knihovny, který najde v dokumentaci bloky kódu
a otestuje, jestli odpovídají ukázanému výstupu.

Pro nás to bude způsob, jak testovat *dokumentaci* – tedy jestli jsou ukázky
kódu v ní stále platné.
Dá se sice použít i k testování samotného kódu, ale na to existují
[lepší nástroje]({{lesson_url('intro/testing')}}).

V kombinaci se Sphinxem se dá použít rozšíření `doctest`, které jsme v průvodci
aktivovali. Můžete to dělat dvěma způsoby. První je mít v dokumentaci
příklad vypadající jako interaktivní konzole.
Takový příklad nemusí být odsazený ani ničím uvozený; stačí `>>>` na začátku.

```python
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

Testy se také dají zařazovat do skupin, více
v [dokumentaci](http://www.sphinx-doc.org/en/1.4.8/ext/doctest.html).

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
# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys
sys.path.insert(0, os.path.abspath('..'))
```

### Travis CI

Neexistuje žádný unifikovaný způsob, jak specifikovat závislosti pro sestavení
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
- '3.6'
install:
- python setup.py install
- pip install -r docs/requirements.txt
script:
- python setup.py test --addopts -v
- cd docs && make doctest
```

autodoc
-------

Pro dokumentaci API lze použít `autodoc`, rozšíření Sphinxu, které jsme povolili
v průvodci.

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
[jiné direktivy](http://www.sphinx-doc.org/en/1.4.8/ext/autodoc.html#directive-automodule).

Pro vygenerování hezké struktury si můžete pomoci příkazem `apidoc`:

```console
(__venv__) $ python -m sphinx.apidoc -o docs mymodule
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

[Napoleon]: http://www.sphinx-doc.org/en/1.4.8/ext/napoleon.html


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

[domény Python]: http://www.sphinx-doc.org/en/1.4.8/domains.html#cross-referencing-python-objects
[index]: http://www.sphinx-doc.org/en/1.4.8/markup/misc.html#index-generating-markup


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
