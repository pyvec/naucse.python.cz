# Klondike Solitaire: Karty

Pojďme vytvořit karetní hru *Klondike Solitaire*, kterou možná znáš v nějaké
počítačové verzi.

{{ figure(img=static('klondike.png'), alt="Jedna z grafických podob hry") }}

Naše hra bude ze začátku jednodušší – nebudeme se zabývat grafikou,
ale logikou hry.
„Grafiku“ zatím zajistí textová konzole. Obrázek výše se dá ukázat jako:

```plain
   U     V          W     X     Y     Z
 [???] [   ]      [   ] [   ] [   ] [   ]

   A     B     C     D     E     F     G
 [3♣ ] [???] [???] [???] [???] [???] [???]
       [5 ♥] [???] [???] [???] [???] [???]
             [6♣ ] [???] [???] [???] [???]
                   [5♠ ] [???] [???] [???]
                         [Q ♥] [???] [???]
                               [4♠ ] [???]
                                     [3 ♦]
```


## Pasiáns

*Klondike Solitaire* je [Pasiáns](https://cs.wikipedia.org/wiki/Pasi%C3%A1ns)
– karetní hra pro jednoho hráče.
Tyto hry obecně fungují takto:

* Karty se určitým způsobem *rozdají* do několika balíčků, hromádek nebo
  jiných skupin
* Dokud hráč *nevyhrál*:
  * Hráč *udělá tah*: podle určitých pravidel přesune karty z jedné hromádky
    na druhou

Než ale počítač naučíš hrát hru, je potřeba ho naučit pár základních věcí,
aby pak instrukce pro samotnou hru dávaly smysl.
Základní věci, které je potřeba počítač „naučit“, jsou:

* Co je to *karta*?
* Co je to *balíček*?

Odpovědí na tyhle otázky bude spousta vysvětlování a taky několik Pythonních
funkcí, které použiješ i ve zbytku hry.

Tady bych rád podotknul, že tyhle materiály ukazují předem vyzkoušený způsob,
jak napsat karetní hru.
Reálné projekty takhle nefungují: zahrnují spoustu plánování, slepých uliček,
oprav špatně navrženého kódu a jiných frustrací.
Neděláme tu reálný softwarový projekt – zatím stále *zkoušíme základy*,
jen z nich pak vyleze něco hezkého.


## Karta a balíček

Co je to *karta* a *balíček*?
Jak tyhle koncepty *reprezentovat* v Pythonu – tedy pomocí čísel, řetězců,
seznamů, <var>n</var>-tic a jiných datových typů – abys s nimi mohl{{a}}
dál pracovat?

Možností jak to udělat je více.
Dobrý návrh *datového modelu* je základ úspěšného projektu: odpověď na otázku
výše je základ k tomu, aby se pak program hezky psal.
Až budeš potřebovat dobrý návrh datového modelu pro nějaký svůj projekt,
doporučuju se ze začátku poradit se zkušenějším programátorem.

Pro Solitaire je tento úkol za tebe vyřešený: hrou Klondike si procvičíš
seznamy a <var>n</var>-tice (a později slovníky).


### Karta

O *kartě* potřebuješ znát tři kousky informace: hodnotu, barvu a to, jestli
je otočená rubem nebo lícem nahoru.

*Hodnoty* karet jsou čísla 2-10 a navíc `J`, `Q`, `K`, `A`.
Hodnoty „obrázkových“ karet je dobré převést na čísla: J=11, Q=12, K=14, A=1.
Hodnoty se tak budou dát jednoduše porovnávat, nebo zjišťovat následující kartu
(např. po desítce je jedenáct – `J`).
V programu budeme tedy pro hodnoty používat jen čísla, a teprve když bude
potřeba kartu „ukázat“ člověku, převedeme ji na písmenko.

Pro *barvu* jsou čtyři možnosti: ♥, ♦, ♣ nebo ♠.
Dají se reprezentovat v podstatě jakýmikoli čtyřmi různými hodnotami.
Různí programátoři by mohli použít čísla 0-3, symboly jako `♥`, nebo třeba jako
čtyři různé funkce.
My použijeme krátké řetězce bez diakritiky, aby se to dobře psalo:
`'Sr'` (srdce), `'Pi'` (piky), `'Ka'` (káry), `'Kr'` (kříže).
Použij prosím stejné řetězce (včetně velkých písmen), abys pak mohl{{a}}
kopírovat ukázkový kód.
Jako u hodnoty platí že tyhle řetězce budeme používat ve většině programu,
jen když bude potřeba kartu „ukázat“ člověku, převedeme je na hezčí symbol.

Pro *otočení* karty jsou dvě možné hodnoty: buď lícem nebo rubem nahoru.
Když dvě hodnoty, je dobré použít `True` a `False`.
Jen je pak potřeba vybrat (a dodržovat) která je která.
Řekněme že `True` znamená lícem nahoru; `False` rubem.
Ideální je podle toho důsledně pojmenovávat proměnné: v programu vždy
používej `je_licem_nahoru=True`, ne `otoceni=True`.

Samotná karta pak bude trojice těchto hodnot: (hodnota, barva, je_licem_nahoru).
Například:

* `(12, 'Sr', True)` je 🂽 – srdcová královna otočená lícem nahoru
* `(7, 'Pi', False)` je 🂠 – piková sedma otočená rubem nahoru


### Balíček

A balíček? Balíček bude seznam karet, tedy seznam trojic.
Jakákoli sekvence karet ve hře bude bude seznam trojic: dobírací a odkládací
balíčky, „sloupečky“ karet na herní ploše i „hromádky“ sežazených karet.

Například jeden ze sloupečků z obrázku výše obsahuje 4 karty rubem nahoru
a na konci srdcovou královnu.
Jako seznam by to mohlo být:

```python
[(7, 'Pi', False), (5, 'Kr', False), (1, 'Ka', False), (3, 'Pi', False), (12, 'Sr', True)]
```


### Seznamy a <var>n</var>-tice

Na balíčckích a kartách je vidět rozdíl v použití seznamů a <var>n</var>-tic:

* <var>N</var>-tice má pevně dané <var>N</var>: karta je trojice, ne čtveřice
  ani dvojice.
  Oproti tomu seznamy nemívají pevně danou délku: hromádka karet může být velká,
  malá, nebo dokonce prázdná.
  Dokonce může během hry růst nebo se zmenšovat, třeba když si „lízneš“ kartu
  nebo balíček rozdělíš na dvě části.
* Seznamy často dává smysl zamíchat nebo seřadit.
  Když zamíchám balíček karet, je to stále baliček karet.
  Když ale zamíchám pořadím prvků ve trojici *(hodnota, barva, je_licem_nahoru)*,
  bude to sice pořád trojice, ale už to nejspíš nebude *karta*.
* S tím souvisí to, že v seznamy bývají tzv. *homogenní*: každý prvek stejný
  typ. Máme balíček karet (trojic), ale karty jsou trojice
  (číslo, řetězec, pravdivostní hodnota).

> [note]
> Ne ve všech programech to bude takhle jednoznačné. Karta a balíček jsou
> skoro ideální příklady na seznamy a <var>n</var>-tice  :)

V Pythonu z použitých typů vyplývá, co se s nimi dá dělat.

<var>N</var>-tice nejdou měnit: abys změnil{{a}} např. otočení karty, bude
potřeba udělat úplně novou trojici (podobně jako např u tahu
z `--------------------` na `-------------o------` v 1D piškvorkách).

Seznamy ale měnit jdou. Seznamové operace dokonce často dávají smysl:

* *append* je přiložení karty na vršek hromádky.
* *pop* je líznutí karty (z balíčku zmizí, ale karta zůstane v ruce – jako návratová hodnota).
* *extend* je přidání jednoho balíčku ke druhému.
* *random.shuffle* je zamíchání karet.
* *sort* je seřazení karet.

Pozor ale na to, že se seznamem trojic toho jde dělat víc než s fyzickým
balíčkem karet.
Pro počítač není problém udělat kopii karty.


## Pomocné funkce

Označovat dsrdcovou dámu jako `(12, 'Sr', True)` je skvělé pro počítač,
ale pro lidi je to nepřehledné.
Bude tedy vhodné napsat funkci, která kartu „ukáže“ trochu srozumitelněji.
Taková funkce by měla vyřeši i to, že kartu, která je rubem nahoru
– jako `(5, 'Kr', False)`, je potřeba před hráčem skrýt.

Napsat tuhle funkci je docela otrava, a později bude potřeba
aby se chovala *přesně* podle mých očekávání
(včetně např. velkých písmen a mezer).
Proto ti ji dám k dispozici. Hlavičku má takovouhle:

```python
def popis_kartu(karta):
    """Vrátí popis karty, např. [Q ♥] nebo [6♣ ] nebo [???]

    Trojice čísla (2-13), krátkého řetězce ('Sr', 'Ka', 'Kr' nebo 'Pi')
    a logické hodnoty (True - lícem nahoru; False - rubem) se jednoduše
    zpracovává v Pythonu, ale pro "uživatele" není nic moc.
    Proto je tu tahle funkce, která kartu hezky "popíše".

    Aby měly všechny hodnoty jen jeden znak, desítka se vypisuje jako
    římská číslice "X".

    Aby se dalo rychle odlišit červené (♥♦) karty od černých (♣♠),
    mají červené mezeru před symbolem a černé za ním.
    """
```

Druhá užitečná funkce umí otočit karu buď rubem nebo lícem nahoru.
Podobně jako `tah` z piškvorek vezme „starou“ hodnotu, rozloží ji
části a výsledek slepí z kombinace „starých“ a „nových“ hodnot.

Projdi si ji řádek po řádku, abys věděl{{a}} jak funguje:

```python
def otoc_kartu(karta, pozadovane_otoceni):
    """Vrátí kartu otočenou lícem nahoru (True) nebo rubem nahoru (False)

    Nemění původní trojici; vytvoří a vrátí novou.
    (Ani by to jinak nešlo – n-tice se, podobně jako řetězce čísla, měnit
    nedají.)
    """

    # Rozbalení n-tice
    hodnota, barva, stare_otoceni = karta

    # Vytvoření nové n-tice (kombinací staré hodnoty/barvy a nového otočení)
    nova_karta = hodnota, barva, pozadovane_otoceni

    # Vrácení nové n-tice
    return nova_karta
```

Funkce najdeš v souboru [`karty.py`]. Projdi si je; rozumíš jim?

Testy k nim jsou v [`test_karty.py`] – ty procházet nemusíš.

[`karty.py`]: {{ static('karty.py') }}
[`test_karty.py`]: {{ static('test_karty.py') }}

Oba soubory si ulož.


### Testy a úkoly

Další pomocné funkce už napíšeš {{gnd('sám', 'sama')}}.
Aby sis ověřil{{a}} že fungují, mám pro tebe předpřipravené testy.

Stáhni si soubor s testy, [test_klondike.py], a dej ho do adresáře,
kde budeš tvořit hru a kde máš `karty.py`.

Na ulehčení testování si nainstaluj modul `pytest-level`.
Ten umožňuje pouštět jen určité testy – podle toho, jak jsi daleko.

    python -m pip install pytest pytest-level

Zkus pustit všechny testy. Asi ti neprojdou:

    python -m pytest -v

Pak zkus pustit testy pro úroveň 0:

    python -m pytest -v --level 0

Teď se nepustí žádné testy – všechny nové testy se přeskočí;
projdou jen testy z `test_karty.py`.
Uvidíš něco jako:

```pytest
===== 20 passed, 99 deselected in 0.06s ====
```

Zadáš-li v posledním příkazu `--level 1`, aktivuje se první z testů. Pravděpodobně neprojde – v dalším úkolu ho spravíš!

[test_klondike.py]: {{ static('test_klondike.py') }}



### Vytvoření balíčku

Do modulu `klondike` (tedy do nového souboru `klondike.py`) napiš
následující funkci:

```python
def vytvor_balicek():
    """Vrátí balíček 52 karet – od esa (1) po krále (13) ve čtyřech barvách

    Všechny karty jsou otočené rubem nahoru.
    """
```

Zkus si funkci pustit a podívej se, co vrací.

Aby sis ověřil{{a}}, že se chová správně, pusť na ni testy:

* level 10: Funkce existuje
* level 11: V balíčku je 52 karet, žádné se neopakují.
* level 12: V balíčku jsou všechny požadované karty.
* level 13: Balíček je zamíchaný.


### Rozepsání balíčku

Když výsledek funkce `vytvor_balicek`  vypíšeš, je docela nepřehledný.
Aby se ti s balíčky lépe pracovalo, vytvoř následující funkci:

```python
def popis_balicek(karty):
    """Vrátí popis všech karet v balíčku. Jednotlivé karty odděluje mezerami.
    """
```

Funkce by měla vracet řetězec složený z popisů jednotlivých karet.
Například:

```pycon
>>> karty = [
        (13, 'Pi', True),
        (12, 'Sr', True),
        (11, 'Ka', True),
        (10, 'Kr', False),
    ]

>>> popis_balicek(karty)
[K♠ ] [Q ♥] [J ♦] [???]
```

Jak na to?
Vytváření celého řetězce najednouby bylo složité, ale lze si to rozdělit
na kroky, které už znáš:

* Vytvoř prázdný seznam.
* Postupně do senamu přidej popisy jednotlivých karet.
  (Využij funkci `popis_kartu` z modulu `karty`!)
* Vrať popisky oddělené mezerami. (Koukni na tahák k seznamům!)

Funkci opět můžeš otestovat:

* level 20: Funkce existuje
* level 21: Funkce správně popisuje balíček
* level 22: Funkce umí popsat i prázdný balíček


### Popis balíčku

Občas je z balíčku vidět jen vrchní karta.
Napiš následující funkci, která popíše takový balíček:

```python
def popis_vrchni_kartu(balicek):
    """Vrátí popis daného balíčku karet -- tedy vrchní karty, která je vidět."""
```

Funkci nezapomeň otestovat:

* level 30: Funkce existuje
* level 31: Funkce vrátí popis poslední karty. (Bude se hodit funkce `popis_kartu` z modulu `karty`.)
* level 32: Funkce popíše prázdný balíček jako `[   ]` (3 mezery v hranatých závorkách).


Pokračování příště...
