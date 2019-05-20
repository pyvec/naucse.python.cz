
# Cesty a soubory s Pathlib

Základní práci se soubory – čtení z nich a psaní do nich – rozebírá
[lekce o souborech](naucse:page?lesson=beginners/files). Pro zopakování:

``` python
# Otevření textového souboru "basnicka.txt" pro čtení
with open('basnicka.txt', encoding='utf-8') as soubor:
    # Přečtení obsahu
    contents = soubor.read()

# Velikost souboru
print(len(soubor))
```

Jméno souboru, případně cesta k němu, se tradičně zadává jako řetězec.
Jednotlivé adresáře jsou odděleny lomítkem (případně na Windows zpětným lomítkem);
fungují tu absolutní i relativní cesty.

Pro prosté otvírání známých souborů to stačí.
Když ale potřebuješ s cestami k souborům pracovat víc,
řetězce jsou docela nepohodlné.
A navíc je problém pamatovat na všechny různé případy, které můžou nastat.

Zkus pro příkad napsat funkce, které dostanou cestu k souboru a:

* `vrat_casti` rozdělí cestu na jednotlivé adresáře (a vrátí je jako seznam),
* `vrat_priponu` vrátí příponu souboru.

Na mém Linuxovém počítači cesty vypadají jako
`/home/janca/Documents/archiv.tar.gz`, takže bych mohl napsat něco jako:

```python
def vrat_casti(path):
    """Vrátí seznam komponentů cesty (jednotlivých adresářů/souborů)"""
    return path.split('/')

def vrat_priponu(path):
    """Vrátí příponu souboru"""
    parts = path.split('.')
    return parts[-1]
```

Pro mou cestu to funguje:

```pycon
>>> retezcova_cesta = '/home/janca/Documents/archiv.tar.gz'

>>> vrat_casti(retezcova_cesta)
['', 'home', 'janca', 'Documents', 'archiv.tar.gz']
>>> vrat_pripona(retezcova_cesta)
'gz'
```

Ale pro jinou cestu na jiném počítači už ne:

```pycon
>>> retezcova_cesta = 'C:\\Users\\Jana\\Programy\\superprojekt\\README'

>>> vrat_casti(retezcova_cesta)
['C:\\Users\\Jana\\Programy\\superprojekt\\README']
>>> vrat_priponu(retezcova_cesta)
'C:\Users\Jana\Programy\superprojekt\README'
```

> [note]
> To, že programátoři používali na cesty řetězce a nepromýšleli všechny možné
> podivnosti souborových systémů, je hlavní důvod proč si ještě dnes spousta
> programů neporadí s diakritikou nebo mezerami v názvech souborů.

Jde to líp? Samozřejmě!


## Knihovna pathlib

Od verze 3.4 obsahuje Python knihovnu `pathlib`, jejíž třída `Path` reprezentuje
cestu k souboru a umožňuje s takovými cestami jednoduše a bezpečně manipulovat.

```pycon
>>> from pathlib import Path

>>> # Cesta, která na Windows i Unixu funguje podobně:
>>> cesta = Path('/home/janca/Documents/archiv.tar.gz')
>>> cesta.parts
('/', 'home', 'janca', 'Documents', 'archiv.tar.gz')
>>> cesta.suffix
'.gz'
```

Ukázka s cestou pro Windows (která by na Unixu nefungovala):

> [note]
> Pouštíš-li ukázku na Windows, můžeš místo `PureWindowsPath` použít rovnou
> `Path`.

```pycon
>>> from pathlib import PureWindowsPath

>>> win_cesta = PureWindowsPath('C:\\Users\\Jana\\Programy\\superprojekt\\README')
>>> win_cesta.parts
('C:\\', 'Users', 'Jana', 'Programy', 'superprojekt', 'README')
>>> win_cesta.suffix
''
```

Ukažme si teď něco z toho, co `pathlib` umožňuje.
Nebude to všechno – další možnosti najdeš [na taháku] nebo v angličtině
v [dokumentaci].

[dokumentaci]: https://docs.python.org/3/library/pathlib.html
[na taháku]: https://pyvec.github.io/cheatsheets/pathlib/pathlib-cs.pdf


## Tvoření cest

Cesty v `pathlib` se tvoří zavoláním třídy `Path`.
Na Windows se tím vytvoří `WindowsPath`, na Unixu `PosixPath`.

Obě považují dopředná lomítka za oddělovač adresářů,
takže následující bude fungovat na všech systémech:

```pycon
>>> docs_cesta = Path('/home/janca/Documents')
>>> docs_cesta
PosixPath('/home/janca/Documents')
```

Už při vytvoření cesty se tato *normalizuje*, zjednoduší bez změny významu.
Víc lomítek za sebou se spojí do jednoho, zbytečné adresáře nebo lomítka na
konci se vynechají.

```pycon
>>> Path('/tmp//foo/./bar/')
PosixPath('/tmp/foo/bar')
```

Když chci k takové cestě něco připojit, použiju operátor `/` (který by se měl
používat na dělení, ale psst!):

```pycon
>>> docs_cesta / 'archiv.tar.gz'
PosixPath('/home/janca/Documents/archiv.tar.gz')
```

Přidávat se takhle dají řetězcové cesty, nebo i další `Path`:

```pycon
>>> Path('/') / 'home/janca' / Path('archiv.tar.gz')
PosixPath('/home/janca/archiv.tar.gz')
```

Pozor ale na to, že absolutní cesta (s lomítkem nebo jménem disku na začátku)
znamená, že procházení začíná znovu od kořenového adresáře.
Když k něčemu připojím absolutní cestu, předchozí cesta se zahodí.

```pycon
>>> Path('/home/janca') / '/tmp/foo'
PosixPath('/tmp/foo')
```

Občas lomítko není pohodlné.
V takových případech jde použít metoda `joinpath`, která má stejný efekt:

```pycon
>>> Path('/').joinpath('home', 'janca/archiv.tar.gz')
PosixPath('/home/janca/archiv.tar.gz')
```


## Atributy

Cesty v pathlib mají spoustu užitečných atributů – vlastností, ke kterým se
dostaneš pomocí tečky:

```pycon
>>> # Příklady ukážeme opět na téhle cestě:
>>> cesta = Path('/home/janca/Documents/archiv.tar.gz')
>>> cesta
PosixPath('/home/janca/Documents/archiv.tar.gz')

>>> # jméno
>>> cesta.name
'archiv.tar.gz'

>>> # Přípona (poslední)
>>> cesta.suffix
'.gz'

>>> # Věchny přípony
>>> cesta.suffixes
['.tar', '.gz']

>>> # "kořen" jména (bez poslední přípony)
>>> cesta.stem
'archiv.tar'

>>> # "rodič" – adresář, který tuto cestu obsahuje
>>> cesta.parent
PosixPath('/home/janca/Documents')

>>> cesta.parent.parent
PosixPath('/home/janca')
>>> cesta.parent.parent.parent.parent
PosixPath('/')
```

Všechny "předky" -- rodiče, prarodiče, atd. -- nabízí atribut "parents".
Výsledek je ale *iterátor*; aby se ukázaly jednotlivé hodnoty,
je potřeba ho projít cyklem `for`, převést na seznam, atp.

```pycon
>>> cesta.parents
<PosixPath.parents>

>>> list(cesta.parents)
[PosixPath('/home/janca/Documents'),
 PosixPath('/home/janca'),
 PosixPath('/home'),
 PosixPath('/')]

>>> # Je cesta absolutní?
>>> cesta.is_absolute()
True
>>> Path('foo/archiv.zip').is_absolute()
False

>>> # Jaká by byla relativní vzhledem k jiné, nadřazené cestě?
>>> relativni_cesta = cesta.relative_to('/home/janca')
>>> relativni_cesta
PosixPath('Documents/archiv.tar.gz')

>>> # Spojením té nadřazené cesty a této relativní dostanu zpátky původní cestu
>>> Path('/home/janca') / relativni_cesta
PosixPath('/home/janca/Documents/archiv.tar.gz')

>>> # Přepsání jména souboru (poslední části cesty)
>>> cesta.with_name('hrad.jpeg')
PosixPath('/home/janca/Documents/hrad.jpeg')

>>> # Přepsání koncovky
>>> cesta.with_suffix('.bz2')
PosixPath('/home/janca/Documents/archiv.tar.bz2')

>>> # Pokud existující koncovka není, `with_suffix` ji přidá
>>> Path('myproject/README').with_suffix('.xz')
PosixPath('myproject/README.xz')
```


## Zkoumání disku

Všechno uvedené výše jsou čistě „textové“ operace – pracují jen se jmény.
Soubor `archiv.zip` (ani jiné) počítači mít, aby ses dostal{{a}} k příponě
nebo ke jménům nadřazených adresářů.

> [note]
> Dokonce si můžeš vyzkoušet, jak by to fungovalo na jiném systému – místo `Path`
> naimportuj a použij `PureWindowsPath` nebo `PurePosixPath`, které reprezentují
> Windowsové, resp. Unixové cesty.

Zamysli se: k čemu se hodí umět pojmenovat soubor, který neexistuje?
{% filter solution %}
Jméno potřebuješ třeba když chceš soubor vytvořit.
{% endfilter %}

Teď se dostaneme k operacím pro které je potřeba mít přístup k souborovému
systému.

Nejdříve dvě funkce, které vrací cesty k užitečným adresářům:

```pycon
>>> # Aktuální adresář
>>> Path.cwd()
PosixPath('/home/janca/pyladies/barvy')

>>> # Můj domovský adresář
>>> Path.home()
PosixPath('/home/janca')
```

A základní otázky – existuje daný soubor?
Je to normální soubor nebo adresář?

```pycon
>>> # Existuje na té ukázkové cestě nějaký soubor?
>>> cesta.exists()
False

>>> # Existuje můj domovský adresář?
>>> Path.home().exists()
True

>>> # A je to vůbec adresář?
>>> Path.home().is_dir()
True

>>> # Je to normální datový soubor?
>>> Path.home().is_file()
False
```


## Ukázka

Abychom měli všichni stejné podmínky, stáhni si na další experimenty
[archiv s testovacími soubory](static/archiv.tar.gz).
Dej si ho do aktuálního adresáře (`Path.cwd()`), a pak ho rozbal pomocí
`tarfile`:

```pycon
>>> import tarfile

>>> cesta_k_archivu = Path("archiv.tar.gz")

>>> # Co je v archivu?
>>> tarfile.open(cesta_k_archivu, 'r|gz').getnames()
['soubory',
 'soubory/hrad.jpeg',
 'soubory/hrad.attribution',
 'soubory/.gitignore',
 'soubory/kolecko.png',
 'soubory/texty',
 'soubory/texty/vodnik.txt',
 'soubory/texty/lidove',
 'soubory/texty/lidove/pes.txt',
 'soubory/texty/lidove/holka.txt',
 'soubory/texty/vladimir.txt',
 'soubory/texty/cizojazycne',
 'soubory/texty/cizojazycne/iroha.txt',
 'soubory/texty/cizojazycne/witch.txt',
 'soubory/hlad.txt',
 'soubory/hraz.attribution',
 'soubory/ententyky.txt',
 'soubory/hraz.jpeg',
 'soubory/README']

>>> # Extrakce archivu. (Kdybys to zkoušel/a pro jiné archivy, vždy před
>>> # rozbalením zkontroluj cesty všech souborů v archivu -- ať se rozbalením
>>> # nepřepíše nějaký důležitý soubor!)
>>> tarfile.open(cesta_k_archivu, 'r|gz').extractall()
```

Rozbalením archivu vznikl `./soubory/` (tedy: adresář `soubory` v aktuálním
adresáři).
Pojď se mu kouknout na zoubek:

```pycon
>>> zaklad = Path('./soubory')
>>> zaklad
PosixPath('soubory')

>>> print('Je to adresář?', zaklad.is_dir())
Je to adresář? True
>>> print('Je to normální soubor?', zaklad.is_file())
Je to normální soubor? False
```

Podle informací o archivu je v soubory nějaký `ententyky.txt` – podle přípony
soubor s textem.

```pycon
>>> ententyky = zaklad / 'ententyky.txt'
>>> print('Je to adresář?', ententyky.is_dir())
Je to adresář? False
>>> print('Je to normální soubor?', ententyky.is_file())
Je to normální soubor? True
```

Objekty `Path` lze používat v naprosté většině situací, kdy jde použít cesta
jako řetězec.
Například pro funkci `open`:

```python
with open(ententyky, encoding='utf-8') as file:
    print(file.read())
```

`Path` ale má `open` i jako metodu:

```python
with ententyky.open(encoding='utf-8') as file:
    print(file.read())
```

A protože je čtení celého textového obsahu souboru docela užitečné,
existuje i zkratka která soubor otevře, přečte a zavře najednou:

```python
print(ententyky.read_text())
```

(Větší soubory je ale lepší otevřít ve `with` a zpracovávat třeba po řádcích,
aby se obsah nemusel do paměti počítače načíst celý najednou.)

Existuje i `write_text`:

```python
cesta = Path.cwd() / 'pisnicka.txt'
cesta.write_text('Holka modrooká\nNesedávej u potoka!')
```

{#
## Zpátky na stromy... tedy řetězce

Ve většině případů jde Path použít tam, kde se cesta dá zadat jako řetězec. Na ale vždy – pathlib existuje teprve od roku 2014, a některé Pythonní knihovny stále ještě vyžadují řetězce.

Jedna z výjimek je IPython.display.Image, která umí v Notebooku vykreslit obrázek.

```pycon
>>> from IPython.display import Image
```

Image potřebuje (aspoň začátkem roku 2018) řetězcovou cestu.
Příkaz `Image(base / 'hrad.jpeg')` mi skončil chybou typu –
`TypeError: a bytes-like object is required, not 'PosixPath'`.

V takových případech ale stačí Path převést na řetězec.

```pycon
>>> str(base / 'hrad.jpeg')
'soubory/hrad.jpeg'

>>> Image(str(base / 'hrad.jpeg'))

>>> # Informace o autorství obrázku (díky, Millenium187!)
>>> print(base.joinpath('hrad.attribution').read_text())

"hrad.jpg" is (c) 2011, Wikipedia user Millenium187
    https://commons.wikimedia.org/wiki/User:Millenium187
Here used under the Creative Commons Attribution-Share Alike 3.0 Unported license.

See: https://commons.wikimedia.org/wiki/File:Hrad_%C5%A0pilberk_II.jpg
```
#}

## A co adresáře?

I s adresáři umí `pathlib` pracovat.
Nejzákladnější operace je získání cest k obsaženým souborům:

```pycon
>>> zaklad.iterdir()
<generator object Path.iterdir at 0x7fbd4443b9e8>
```

Metoda iterdir opět vrací *iterátor* – objekt, přes který musíš „projít“
(cyklem for, převedením na seznam ap.), abys z něj dostal{{a}} obsah.

```pycon
>>> list(zaklad.iterdir())
[PosixPath('soubory/hrad.jpeg'),
 PosixPath('soubory/hrad.attribution'),
 PosixPath('soubory/.gitignore'),
 PosixPath('soubory/kolecko.png'),
 PosixPath('soubory/texty'),
 PosixPath('soubory/hlad.txt'),
 PosixPath('soubory/hraz.attribution'),
 PosixPath('soubory/ententyky.txt'),
 PosixPath('soubory/hraz.jpeg'),
 PosixPath('soubory/README')]

>>> for cesta in zaklad.iterdir():
>>>    print(cesta)
soubory/hrad.jpeg
soubory/hrad.attribution
soubory/.gitignore
soubory/kolecko.png
soubory/texty
soubory/hlad.txt
soubory/hraz.attribution
soubory/ententyky.txt
soubory/hraz.jpeg
soubory/README
```

{#

## Glob Glob

Zajímavější operace je ale `glob`, která vyfiltruje soubory, které odpovídají
určité šabloně.

V šabloně můžeš použít `*`, které odpovídá 0 a více písmenům
(v rámci jména jednoho souboru):

```pycon
>>> # Soubory končící na ".txt"
>>> list(base.glob('*.txt'))
[PosixPath('soubory/hlad.txt'), PosixPath('soubory/ententyky.txt')]

>>> # Soubory, které mají ve jméně tečku
>>> list(base.glob('*.*'))
[PosixPath('soubory/hrad.jpeg'),
 PosixPath('soubory/hrad.attribution'),
 PosixPath('soubory/.gitignore'),
 PosixPath('soubory/kolecko.png'),
 PosixPath('soubory/hlad.txt'),
 PosixPath('soubory/hraz.attribution'),
 PosixPath('soubory/ententyky.txt'),
 PosixPath('soubory/hraz.jpeg')]
```

… nebo ?, což odpovídá jednomu písmenu:

```pycon
>>> # Slovo na čtyři, první je `h` a třetí `a`
>>> list(base.glob('h?a?.*'))
[PosixPath('soubory/hrad.jpeg'),
 PosixPath('soubory/hrad.attribution'),
 PosixPath('soubory/hlad.txt'),
 PosixPath('soubory/hraz.attribution'),
 PosixPath('soubory/hraz.jpeg')]
```

Případně jde použít výčet písmen v hranatých závorkách, viz modul fnmatch.

```pycon
>>> list(base.glob('h?a[zd].????'))
[PosixPath('soubory/hrad.jpeg'), PosixPath('soubory/hraz.jpeg')]
>>> list(base.glob('[!hv]*'))
[PosixPath('soubory/.gitignore'),
 PosixPath('soubory/kolecko.png'),
 PosixPath('soubory/texty'),
 PosixPath('soubory/ententyky.txt'),
 PosixPath('soubory/README')]
```

Poslední speciální kombinace je `**`.
Dvě hvězdičky odpovídají základnímu adresáři a všem jeho podadresářům,
pod-podadresářům, pod-pod-podadresářům atd.

```pycon
>>> list(base.glob('**'))
[PosixPath('soubory'),
 PosixPath('soubory/texty'),
 PosixPath('soubory/texty/lidove'),
 PosixPath('soubory/texty/cizojazycne')]
```

S pomocí ** se často hledají soubory s danou příponou:

```pycon
>>> list(base.glob('**/*.txt'))
[PosixPath('soubory/hlad.txt'),
 PosixPath('soubory/ententyky.txt'),
 PosixPath('soubory/texty/vodnik.txt'),
 PosixPath('soubory/texty/vladimir.txt'),
 PosixPath('soubory/texty/lidove/pes.txt'),
 PosixPath('soubory/texty/lidove/holka.txt'),
 PosixPath('soubory/texty/cizojazycne/iroha.txt'),
 PosixPath('soubory/texty/cizojazycne/witch.txt')]
```

#}


## Strom adresářů – rekurze

Adresáře, podadresáře a soubory v nich tvoří strukturu, na kterou se často
používají rekurzivní funkce.

Tady je funkce `vypis_soubory`, která ypíše všechny soubory v daném adresáři.
Před každé jméno dá odrážku `-`, aby to líp vypadalo:

```python
from pathlib import Path

def vypis_soubory(odrazka, adresar):
    """Vypíše odrážkový seznam jmen souborů v daném adresáři"""
    for soubor in adresar.iterdir():
        print(odrazka, soubor.name)

vypis_soubory('-', Path.cwd())
```

Odrážka se dá zadat:

```python
vypis_soubory('*', Path.cwd())
vypis_soubory('  *', Path.cwd())
```

Tahle funkce se dá změnit, aby vypsala i obsahy *podadresářů*.
Jak?
Poté, co vypíše jméno nějakého podadresáře, zavolá funkci která vypíše
obsah toho podadresáře.
Takovou funkci ale už máš napsanou – stačí trochu změnit odrážku, aby bylo
poznat co je podadresář.

```python
from pathlib import Path

def vypis_soubory(odrazka, adresar):
    """Vypíše odrážkový seznam jmen souborů v daném adresáři i podadresářích"""
    for soubor in adresar.iterdir():
        print(odrazka, soubor.name)
        if soubor.is_dir():
            vypis_soubory('  ' + odrazka, soubor)

vypis_soubory('-', Path.cwd())
```

Podobně lze například spočítat soubory v nějakém adresáři (i všech
podadresářích).

```python
from pathlib import Path

def spocitej_normalni_soubory(adresar):
    """Vrátí počet normálních souborů v daném adresáři i všech podadresářích"""
    pocet = 0
    for soubor in adresar.iterdir():
        if soubor.is_dir():
            pocet = pocet + spocitej_normalni_soubory(soubor)
        elif soubor.is_file():
            pocet = pocet + 1
    return pocet

print(spocitej_normalni_soubory(Path.cwd()))
```
