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

Pro vytvoření základní kostry dokumentace se používá jednoduchý průvodce:

```
$ . env/bin/activate
(env) $ python -m pip install sphinx
(env) $ python -m sphinx.quickstart
Welcome to the Sphinx 1.4.8 quickstart utility.
...
Enter the root path for documentation.
> Root path for the documentation [.]: docs
...
The project name will occur in several places in the built documentation.
> Project name: coolthing
> Author name(s): Pythonista Dokumentarista

Sphinx has the notion of a "version" and a "release" for the
software. Each version can have multiple releases. For example, for
Python the version is something like 2.5 or 3.0, while the release is
something like 2.5.1 or 3.0a1.  If you don't need this dual structure,
just set both to the same value.
> Project version: 0.5
...
Please indicate if you want to use one of the following Sphinx extensions:
> autodoc: automatically insert docstrings from modules (y/n) [n]: y
> doctest: automatically test code snippets in doctest blocks (y/n) [n]: y
...
```

V ukázce jsou zobrazeny jen věci, kde nestačí nechat výchozí hodnota.
K modulům `autodoc` a `doctest` se dostaneme později.

Průvodce vytvoří složku docs a v ní několik souborů.
Do gitu patří všechny nyní vytvořené soubory, kromě složky `docs/_build`,
která by měla být ignorována.

Zatím se nebudeme zabývat obsahem těchto souborů, ale zkusíme základní kostru
dokumentace sestavit do HTML.

**Poznámka:** Sphinx umí generovat dokumentaci ve více formátech (LaTeX,
manuálové stránky atd.), pro nás bude podstatné především HTML.

```
(env) $ cd docs
(env) $ make html
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
můžete použít [tahák].

[reStructuredText]: http://www.sphinx-doc.org/en/stable/rest.html
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

Soubory s kapitolami je třeba vytvořit ve složce `docs` s příponou `.rst`.
Obsah (ve smyslu *content*) lze pak přidávat samozřejmě do těchto souborů i do
`index.rst`.

Chcete-li odkazovat na některou sekci, označíme si ji pomocí `.. _label:`:

```rst
.. _my-reference-label:

Section to cross-reference
--------------------------

This is the text of the section.
```

Poté na ni lze odkazovat, odkudkoli z dokumentace, odkazovat pomocí
[konstrukce ref]:

```rst
It refers to the section itself, see :ref:`my-reference-label`.
It could refer to a different section as well :)
```

[konstrukce ref]: http://www.sphinx-doc.org/en/1.4.8/markup/inline.html#role-ref

doctest
-------

`doctest` je modul ze standardní knihovny, který najde v dokumentaci bloky kódu
a otestuje, jestli se váš kód chová tak, jak je to ukázáno v dokumentaci.

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

Výstup posledního testcode bloku. V dokumentaci nebude kód zobrazen, pokud
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

```
(env) $ make doctest
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

Pokud nemáte nainstalovaný vlastní balíček, a budete z něj chtít v doctestu
importovat, pravděpodobně dostanete `ImportError`.
V takovém případě pomůže drobná editace `conf.py`:

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
- '3.5'
install:
- python setup.py install
- pip install -r docs/requirements.txt
script:
- python setup.py test --addopts -v
- cd docs && make doctest
```

autodoc
-------

Pro dokumentaci API lze použít Sphinx rozšíření `autodoc`, které jsme povolili
v průvodci (případně to lze udělat v souboru `conf.py`), a to takto:

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

    (env) $ python -m sphinx.apidoc -o docs mymodule

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
odkázat pomocí konstrukce `:mod:`, `:func:`, `:cls:`, `:meth:` a dalších
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

Pokud svůj repositář na GitHubu změníte na veřejný
(což je v tuto chvíli již z hlediska předmětu v pořádku), můžete využít službu
[Read the Docs] k hostování dokumentace ve Sphinxu.
Dokumentace se sestaví při každém pushnutí na GitHub.

Pokud Read the Docs použijete, nezapomeňte na dokumentaci odkázat
z `README.rst`.

[Read the Docs]: https://readthedocs.org/

Úkol
----

Vaším úkolem za 5 bodů je vytvořit pomocí Sphinx dokumentaci k vašemu projektu.

Měla by obsahovat textovou část, ze které bude jasné, co je, k čemu je,
jak se nainstaluje a jak se používá vaše aplikace.
Můžete předpokládat, že uživatel ví, co je to Twitter, tweet, hashtag, retweet
apod.; GitHub, issue, pull request, label, repozitář apod.
Nepředpokládejte ale, že ví, kde najde API klíče či tokeny, že ví, co to je,
jak se k nim chovat apod. U GitHubu nepředpokládejte, že ví, co je to webhook.

Pokud hypoteticky ukážeme dokumentaci kolegům, kteří nikdy neviděli zadání
vašeho úkolu, musí to pro ně být stejně pochopitelné.

Dále by dokumentace měla obsahovat textovou část s ukázkami kódu, které se
testují pomocí doctestu. Tato část může vysvětlovat, jak váš kód použít pro
výrobu jiné aplikace, nebo může popisovat, jak aplikace uvnitř funguje.

V dokumentaci by měla existovat kapitola s kompletní API dokumentací vašich
modulů, tříd, funkcí apod. Všechny tyto věci musí mít v kódu dokumentační
řetězce, které v dokumentaci musí být zobrazeny (t.j. změna dokumentačního
řetězce se automaticky promítne ve vygenerované dokumentaci).

Jak sestavit a testovat dokumentaci by mělo být jasné z `README.rst`
(a to musí mít reStructuredText syntaxi).

Generování dokumentace ani doctesty nesmí způsobit chybu ani varování.
Potlačení chybových a varovných hlášek (např. konfigurací, přesměrováním
*stderr*, apod.) je povoleno jen po konzultaci s cvičícím.

Na Travis CI spouštějte dokumentační testy.

Dokumentace musí být v angličtině.

Dosavadní funkcionalita aplikace musí být samozřejmě zachována.

Úkol odevzdáváte tradičně s tagem v0.5 a nahráním nové verze na
(testovací či pravou) PyPI.
(Nahrání je nutné – čtenář dokumentace k verzi 0.5 se bude dívat po balíčku
této verze.)

Za fungující publikaci smysluplné dokumentace na [Read the Docs] je bod navíc.
