# Ignorování souborů

Často se stává, že některé soubory v repozitáři nechceš.
Takových souborů jsou tři hlavní druhy:

Pomocné soubory nástrojů
:   Python občas „sám od sebe“ vytváří adresář `__pycache__` s pomocnými
    soubory, aby zrychlil importování modulů.
    Některé počítače vytváří skryté soubory s názvy jako
    `.Thumbnails`, `.DS_Store` nebo `Thumbs.db`.
    Takové věci v repozitáři nemají co dělat – je
    dobrým zvykem do Gitu nedávat nic, co jde vytvořit automaticky.

Výstup programu a nastavení
:   Píšeš-li program, který kreslí obrázky, většinou chceš v repozitáři
    jen samotný program.
    Obrázky si může pomocí programu každý vytvořit sám.
:   Podobně fungují soubory s heslem: pokud program potřebuje heslo
    např. k nějaké webové službě, ale svoje heslo nechceš dávat veřejně
    k dispozici, musí si každý vytvořit soubor s heslem sám.

Osobní soubory
:   Občas se stane, že v adresáři s repozitářem máš soubor s osobními
    poznámkami.
    Zbytek repozitáře plánuješ zveřejnit, ale tyto soubory by měly zůstat
    jen ve tvé kopii. A to včetně informace o tom, že takové soubory máš.

Adresář s virtuálním prostředím
:   Jistě už sis zvykl{{a}} na virtuální prostředí.
    Adresář s ním se může jmenovat různě, v začátečnickém kurzu používáme název `venv`.
    Není dobré tento adresář dávat do Gitu,
    protože je jednoduché jej vždy vytvořit znovu
    a pokud na projektu spolupracuje více lidí
    (nebo ty z více počítačů), mohlo by dělat neplechu, kdyby virtuální
    prostředí nebylo vždy na úplně stejném místě.
    Virtuální prostředí z adresáře `/home/helena/projektABC/venv`
    nebude fungovat z adresáře `C:\Users\Helena\projektABC\venv`,
    ale ani z `/home/mirka/projektABC/venv`.

My budeme chtít Git nastavit tak, aby tyto soubory ignoroval: aby
`git status` neukazoval červeně, že ještě nejsou v repozitáři.

## Příprava

Pojďme si to ukázat na příkladu.
Založ si nový repozitář a vytvoř v něm tři soubory s tímto obsahem:

* `obrazek.py`

  ```python
  from turtle import forward, left, right, getcanvas

  forward(50)
  left(60)
  forward(50)
  right(60)
  forward(50)

  getcanvas().postscript(file='obrazek.ps')
    ```

* `poznamky.txt`

  ```plain
  Tohle je tajné!
  ```

* `Autofile.tmp`

  Do tohohle souboru napiš cokoliv.
  Různé operační systémy a (jiné programy) vytváří různé soubory
  podivných jmen; `Autofile.tmp` pro nás bude představovat takový
  automaticky vzniklý soubor.

Pythonní program spusť (pomocí `python obrazek.py`).
Mělo by se na chvíli ukázat okno s želvou a měl by vzniknout nový soubor
`obrazek.ps`.

> [note]
> Obrázek ve formátu PostScript (.ps) se dá otevřít ve většině programů, které
> zvládají i PDF, případně v [Inkscape](https://inkscape.org/).

Jak se na to dívá Git?

```ansi
␛[36m$␛[0m git status
On branch master

No commits yet

Untracked files:
  (use "git add <file>..." to include in what will be committed)
	␛[31mAutofile.tmp␛[m
	␛[31mobrazek.ps␛[m
	␛[31mobrazek.py␛[m
	␛[31mpoznamky.txt␛[m

nothing added to commit but untracked files present (use "git add" to track)
```

Spousta souborů, ale jen jeden z nich chceš v repozitáři.
Co s těmi ostatními?


## Výstupy programu a pomocné soubory společných nástrojů

Nejjednodušší je vyrovnat se se souborem `obrazek.ps`.
V repozitáři ho nechceš (je to repozitář *zdrojového* kódu; výsledky bývá
lepší schraňovat jinde než v Gitu).
Zároveň víš, že každý, kdo s repozitářem bude pracovat, pravděpodobně
tenhle soubor vytvoří.
Bylo by tedy dobré říct *všem* lidem, kteří se k repozitáři dostanou, že tento
soubor do Gitu nepatří.
To se dělá záznamem ve speciálním souboru v repozitáři.

Udělej soubor s názvem `.gitignore`.
(Pozor na tečku ve jménu souboru; na některých systémech se špatně zadává –
doporučuji soubor vytvořit v programátorském editoru.)
Do něj napiš:

```plain
obrazek.ps
```

Pak se podívej na `git status`. Obrázek už by ve výpisu neměl být!

```ansi
␛[36m$␛[0m git status
On branch master

No commits yet

Untracked files:
  (use "git add <file>..." to include in what will be committed)
	␛[31m.gitignore␛[m
	␛[31mAutofile.tmp␛[m
	␛[31mobrazek.py␛[m
	␛[31mpoznamky.txt␛[m

nothing added to commit but untracked files present (use "git add" to track)
```

Nový soubor `.gitignore` přidej do repozitáře společně se samotným programem:

```ansi
␛[36m$␛[0m git add .gitignore obrazek.py
␛[36m$␛[0m git status
On branch master

No commits yet

Changes to be committed:
  (use "git rm --cached <file>..." to unstage)
	␛[32mnew file:   .gitignore␛[m
	␛[32mnew file:   obrazek.py␛[m

Untracked files:
  (use "git add <file>..." to include in what will be committed)
	␛[31mAutofile.tmp␛[m
	␛[31mpoznamky.txt␛[m
```

Když uděláš `git commit` a repozitář nasdílíš s ostatními, všichni dostanou
`.gitignore` s instrukcí, že `obrazek.ps` do repozitáře nepatří.

Jak ignorovat zbylé dva soubory?


## Osobní poznámky

Soubor `poznamky.txt` se taky dá zařadit do `.gitignore`, ale moc se tam nehodí.
Existuje jen u tebe; není důvod předpokládat, že si někdo jiný vytvoří
soubor se stejným jménem.

Dej ho tedy do souboru, který se nebude šířit s repozitářem.
Tento soubor je `.git/info/exclude`.
(Může být trochu složité ho najít, protože adresář `.git` je skrytý. 
Nevidíš–li ho, napiš v editoru do okýnka pro otevření souboru `.git` a dostaneš
se do něj.)

Soubory v adresáři `.git` bys neměl{{a}} měnit, protože se tak dá přijít
o historii projektu.
Ale `exclude` je výjimka. Napiš na konec tohoto souboru:

```plain
poznamky.txt
```

A po uložení budou poznámky ignorovány!

```ansi
␛[36m$␛[0m git status
On branch master

No commits yet

Changes to be committed:
  (use "git rm --cached <file>..." to unstage)
	␛[32mnew file:   .gitignore␛[m
	␛[32mnew file:   obrazek.py␛[m

Untracked files:
  (use "git add <file>..." to include in what will be committed)
	␛[31mAutofile.tmp␛[m
```

## Další haraburdí

Některé programy automaticky vytvářejí pomocné soubory.
Často to dělají správci souborů (často `.Thumbnails` na Linuxu,
`.DS_Store` na Macu nebo `Thumbs.db` na Windows).
Některé editory si taky nechávají na disku nastavení.

Podobné soubory se dají dát do `.gitignore`.
Je ale lepší si je dát do osobního nastavení, protože ostatní lidé,
kteří na projektu můžou spolupracovat, nemusí používat stejný systém
a programy.

> [note]
> Pokud si můžeš být jist{{gnd('ý', 'á')}}, že ostatní budou používat právě
> ten program, který používáš ty, použij `.gitignore`.
> Příklad je adresář `__pycache__`, který vytváří Python při importu modulu.

Soubor s osobním nastavením si můžeš pojmenovat, jak chceš, a můžeš ho uložit
kde budeš chtít.
Já doporučuji ho pojmenovat `.gitignore_global` a dát ho do tvého domovského
adresáře.

Do souboru zase napiš jméno ignorovaného souboru:

```plain
Autofile.tmp
```

Potom řekni Gitu, kde tento soubor najít:

```ansi
␛[36m$␛[0m git config --global core.excludesfile /tmp/tmp.1spGPvBL5W/.gitignore_global
```

A měl by být ignorován:

```ansi
␛[36m$␛[0m git status
On branch master

No commits yet

Changes to be committed:
  (use "git rm --cached <file>..." to unstage)
	␛[32mnew file:   .gitignore␛[m
	␛[32mnew file:   obrazek.py␛[m
```


## Formát ignorovacího souboru

Ve všech třech „ignorovacích“ souborech lze samozřejmě uvést víc souborů:
každý na zvláštní řádek.
Kromě toho je možné použít několik vychytávek:

* `*` ve jméně souboru nahradí část jména souboru.
  Takže pokud chceš ignorovat všechny soubory s příponou `.tmp`, můžeš napsat:

  ```plain
  *.tmp
  ```

* `/` na konci jména značí adresář. Chceš-li tedy ignorovat adresáře
  `__pycache__` (což v Pythonním projektu chceš), napiš do `.gitignore`:

  ```plain
  __pycache__/
  ```

Další detaily je možné najít v [dokumentaci](https://git-scm.com/docs/gitignore).


## Automatické přidávání

Teď, když umíš ignorovat soubory, si můžeme ukázat zkratku. Místo

```console
$ git add soubor1 soubor2
$ git commit
```

můžeš napsat jen `git commit` s tečkou na konci:

```console
$ git commit .
```

To automaticky přidá *všechny* neignorované soubory, které `git status` ukazuje
červeně.
Tečka je jméno pro aktuální adresář – celý adresář a všechno pod ním se přidá
do revize.

Doporučuji si před použitím téhle zkratky zkontrolovat `git status`, aby sis
ověřil{{a}}, že nepřidáváš nic, co nechceš.

Taky doporučuji si nastavit Git, aby se v editoru, kam píšeš popisek revize,
ukazovala poznámka s tím, co vlastně v nové revizi bude.
Uvidíš tak něco jako `git status` vždy, když začneš psát popisek k revizi:

```console
$ git config --global commit.verbose 1
```
