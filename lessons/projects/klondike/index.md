# Klondike Solitaire

Pojďme vytvořit karetní hru *Klondike Solitaire*, kterou možná znáš v nějaké
počítačové verzi.

{{ figure(img=static('klondike.png'), alt="Jedna z grafických podob hry") }}

Naše hra bude ze začátku jednodušší – nebudeme se zabývat grafikou,
ale logikou hry.
„Grafiku“ zatím zajistí textová konzole:

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

## Schéma hry

Hra funguje takto:

* Rozdej balíček a sloupečky karet
* Dokud hráč nevyhrál:
  * Zobraz stav hry
  * Zeptej se hráče, kam chce hrát
  * Je-li to možné:
    * Proveď tah
  * Jinak:
    * Vynadej hráči, že daný tah nedává smysl
* Pogratuluj hráči


## Karta

Karta je trojice (hodnota, barva, je_licem_nahoru) – viz sraz.
Následující funkce (v souboru [`karty.py`]) nám zjednoduší práci:

```python
def popis_kartu(karta):
    """Vrátí popis karty, např. [Q ♥] nebo [6♣ ] nebo [???]

    Trojice čísla (2-13), krátkého řetězce ('Sr', 'Ka', 'Kr' nebo 'Pi')
    a logické hodnoty (True - lícem nahoru; False - rubem) se jednoduše
    zpracovává v Pythonu, ale pro "uživatele" není nic moc.
    Proto je tu tahle funkce, která kartu hezky "popíše".

    Aby byly všechny karty jedno číslo nebo písmeno, se desítka
    se vypisuje jako "X".

    Aby se dalo rychle odlišit červené (♥♦) karty od černých (♣♠),
    mají červené mezeru před symbolem a černé za ním.
    """
```

```python
def otoc_kartu(karta, pozadovane_otoceni):
    """Vrátí kartu otočenou lícem nahoru (True) nebo rubem nahoru (False)

    Nemění původní trojici; vytvoří a vrátí novou.
    (Ani by to jinak nešlo – n-tice se, podobně jako řetězce čísla, měnit
    nedají.)
    """
```

Funkce najdeš v souboru [`karty.py`]. Projdi si je; rozumíš jim?

Testy k nim jsou v [`test_karty.py`] – ty procházet nemusíš, jestli nechceš.

[`karty.py`]: {{ static('karty.py') }}
[`test_karty.py`]: {{ static('test_karty.py') }}


## Testy a úkoly

Stáhni si soubor s testy, [test_klondike_lists.py], a dej ho do adresáře,
kde budeš tvořit hru a kde máš `karty.py`.

Na ulehčení testování si nainstaluj modul `pytest-level`.
Ten umožňuje pouštět jen určité testy – podle toho, jak jsi daleko.

    python -m pip install pytest-level

Zkus pustit všechny testy. Asi ti neprojdou:

    python -m pytest -v

Pak zkus pustit testy pro úroveň 0:

    python -m pytest -v --level 0

Teď se nepustí žádné testy – všechny se přeskočí. Výpis by měl končit nějak takto:

    collected N items / N deselected
    === N deselected in 0.01 seconds ===

Zadáš-li v posledním příkazu --level 1, aktivuje se první z testů. Pravděpodobně neprojde – v dalším úkolu ho spravíš!

[test_klondike_lists.py]: {{ static('test_klondike_lists.py') }}


## Popis balíčku

Jako první věc ve hře potřebujeme rozdat *balíček* karet.
Co je to ale takový balíček?

Sekvenci karet (*balíček* nebo *sloupeček*) budeme reprezentovat jako seznam
karet – tedy seznam trojic.
Například:

```python
balicek = [(4, 'Pi', True), (4, 'Sr', True), (4, 'Ka', False), (4, 'Kr', True)]
prazdny_balicek = []
```

Napiš následující funkci, která balíček popíše:

```python
def popis_balicku(balicek):
    """Vrátí popis daného balíčku karet -- tedy vrchní karty, která je vidět"""
```

* level 10: Funkce existuje
* level 11: Funkce vrátí popis poslední karty. (Bude se hodit funkce `popis_kartu` z modulu `karty`.)
* level 12: Funkce popíše prázdný balíček jako `[   ]` (3 mezery v hranatých závorkách).


## Vytvoření balíčku

Napiš následující funkci:

```python
def vytvor_balicek():
    """Vrátí balíček 52 karet – od esa (1) po krále (13) ve čtyřech barvách

    Karty jsou otočené rubem nahoru (nejsou vidět).
    """
```

* level 20: Funkce existuje
* level 21: V balíčku je 52 karet, žádné se neopakují.
* level 22: V balíčku jsou všechny požadované karty.
* level 23: Balíček je zamíchaný.


## Rozdání sloupečků

Napiš následující funkci:

```python
def rozdej_sloupecky(balicek):
    """Rozdá z daného balíčku 7 "sloupečků" -- seznamů karet

    Karty ve sloupečcích jsou odstraněny z balíčku.
    Vrátí všechny sloupečky -- tedy seznam sedmi seznamů.
    """
```

* level 30: Funkce existuje
* level 31: Funkce vrací seznam sedmi seznamů
* level 32:
  * V každém sloupečku je aspoň jedna karta
  * Poslední karta je lícem nahoru
* level 33: V každém sloupečku je správný počet karet rubem nahoru


## Vypsání sloupečků

Zatím to na hru nestačí, ale práce se seznamy je dost abstraktní.
Poďme sloupečky vypsat, tak jak se ukážou ve hře.

```python
def vypis_sloupecky(sloupecky):
    """Vypíše sloupečky textově.
    """
```

Například, pokud jsou sloupečky:

```python
sloupecky = [
    [(1, 'Pi', True), (7, 'Sr', True)],
    [(2, 'Sr', True), (6, 'Ka', True)],
    [(3, 'Ka', True), (5, 'Kr', False)],
    [(4, 'Kr', False), (4, 'Pi', True)],
    [(5, 'Pi', False), (3, 'Sr', True)],
    [(6, 'Sr', True), (2, 'Ka', True)],
    [(7, 'Ka', True), (1, 'Kr', True)],
]
```

vypíše `popis_sloupecky(sloupecky)` toto:

```plain
[A♠ ] [2 ♥] [3 ♦] [???] [???] [6 ♥] [7 ♦]
[7 ♥] [6 ♦] [???] [4♠ ] [3 ♥] [2 ♦] [A♣ ]
```


* level 40: Funkce existuje
* level 41: Funkce vypisuje karty ze věch sloupečků
* level 42: Funkce funguje, když jsou sloupečky nestejně dlouhé. (Na prázdné místo patří 5 mezer.)
