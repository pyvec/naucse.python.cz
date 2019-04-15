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
  * Zeptej se hráče, odkud a kam chce hrát
  * Je-li to možné:
    * Proveď tah
  * Jinak:
    * Vynadej hráči, že daný tah nedává smysl
* Pogratuluj hráči


## Karta

Karta bude trojice (hodnota, barva, je_licem_nahoru) – viz sraz.
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

Stáhni si soubor s testy, [test_klondike.py], a dej ho do adresáře,
kde budeš tvořit hru a kde máš `karty.py`.

Na ulehčení testování si nainstaluj modul `pytest-level`.
Ten umožňuje pouštět jen určité testy – podle toho, jak jsi daleko.

    python -m pip install pytest pytest-level

Zkus pustit všechny testy. Asi ti neprojdou:

    python -m pytest -v

Pak zkus pustit testy pro úroveň 0:

    python -m pytest -v --level 0

Teď se nepustí žádné testy – všechny se přeskočí. Výpis by měl končit nějak takto:

    collected N items / N deselected
    === N deselected in 0.01 seconds ===

Zadáš-li v posledním příkazu --level 1, aktivuje se první z testů. Pravděpodobně neprojde – v dalším úkolu ho spravíš!

[test_klondike.py]: {{ static('test_klondike.py') }}


## Popis balíčku

Jako první věc ve hře potřebujeme rozdat *balíček* karet.
Co je to ale takový balíček?
Jak se dá balíček karet reprezentovat pomocí řetězců, čísel, seznamů,
<var>n</var>-tic a podobně?

Způsobů, jak takový balíček karet reprezentovat, je více.
Abychom měli projekt všichni stejný (a aby k němu mohly být testy),
je v těchto materiálech tento úkol už vyřešený.

Balíček karet bude *seznam* karet – tedy seznam trojic.
To dává smysl – karet v balíčku může být různý počet (klidně 0),
kar se z něj dají brát nebo do něj přidávat, balíček se dá zamíchat nebo
seřadit.

Balíček bude například:

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


## Rozepsání balíčku

Když výsledek funkce `vytvor_balicek`  vypíšeš, je docela nepřehledný.
Funkce `popis_balicku` tomu příliš nepomáhá, protože popisuje jen vrchní kartu.
Aby se ti s balíčkem lépe pracovalo, vytvoř následující funkci:

```python
def popis_seznam_karet(karty):
    """Vrátí popis všech karet v balíčku. Jednotlivé karty odděluje mezerami.
    """
```

Nezapomeň využít funkci `popis_kartu`!

Například:

```pycon
>>> karty = [
        (13, 'Pi', True),
        (12, 'Sr', True),
        (11, 'Ka', True),
        (10, 'Kr', False),
    ]

>>> popis_seznam_karet(karty)
[A♠ ] [2 ♥] [3 ♦] [???]
```

* level 25: Funkce existuje
* level 26: Funkce správně popisuje balíček
* level 27: Funkce umí popsat i prázdný balíček


## Rozdání sloupečků

Teď zkus rozdat 7 sloupečků karet, tedy konečně první krok hry.

V <var>N</var>-tém sloupečku (počítáno od nuly) je <var>N</var>
karet rubem nahoru plus jedna karta lícem nahoru.
Karty do sloupečků se z balíčku rozdávají postupně: vždy se lízne
vrchní (poslední) karta z balíčku a dá se na konec sloupečku.

{{ figure(img=static('klondike.png'), alt="Ukázka sloupečků") }}

Napiš následující funkci:

```python
def rozdej_sloupecky(balicek):
    """Rozdá z daného balíčku 7 "sloupečků" -- seznamů karet

    Karty ve sloupečcích jsou odstraněny z balíčku.
    Vrátí všechny sloupečky -- tedy seznam sedmi seznamů.
    """
```

Například:

```pycon
>>> balicek = priprav_balicek()
>>> sloupecky = rozdej_sloupecky(balicek)
24
>>> popis_seznam_karet(sloupecky[0])
[3♣ ]
>>> popis_seznam_karet(sloupecky[1])
[???] [5 ♥]
>>> popis_seznam_karet(sloupecky[2])
[???] [???] [6♣ ]
>>> popis_seznam_karet(sloupecky[6])
[???] [???] [???] [???] [???] [???] [3 ♦]
>>> len(balicek)    # Z balíčku zmizely karty, které jsou ve sloupečcích
```

Jak tahle funkce funguje?

* Vytvoří prázdný seznam sloupečků
* Sedmkrat (pro <var>N</var> od 0 do 6):
  * Vytvoří prázdný sloupeček (seznam)
  * <var>N</var>-krát za sebou:
    * „Lízne“ (`pop`) kartu zvrchu balíčku
    * Dá líznutou kartu na vršek sloupečku (`append`)
  * „Lízne“ (`pop`) kartu zvrchu balíčku
  * Líznutou kartu otočí lícem nahoru (`otoc_kartu`)
    a dá vršek sloupečku (`append`)
  * Hotový sloupeček přidá do seznamu sloupečků
* Výsledné sloupečky vrátí

Testy:

* level 30: Funkce existuje
* level 31: Funkce vrací seznam sedmi seznamů
* level 32:
  * V každém sloupečku je aspoň jedna karta
  * Poslední karta je lícem nahoru
* level 33: V každém sloupečku je správný počet karet rubem nahoru


## Vypsání sloupečků

Vzpomínáš si na základní schéma hry?

* Rozdej balíček a sloupečky karet
* Dokud hráč nevyhrál:
  * Zobraz stav hry
  * Zeptej se hráče, kam chce hrát
  * Je-li to možné:
    * Proveď tah
  * Jinak:
    * Vynadej hráči, že daný tah nedává smysl
* Pogratuluj hráči

Rozdání balíčku a sloupečků už víceméně máš!
Pro teď přeskoč zjišťování, jestli hráč vyhrál, a podívej se na vypsání
stavu hry.

Například, pokud jsou sloupečky tyto:

```python
sloupecky = [
    [(1, 'Pi', True), (7, 'Sr', True)],
    [(2, 'Sr', True), (6, 'Ka', True)],
    [(3, 'Ka', True), (5, 'Kr', False)],
    [(4, 'Kr', False), (4, 'Pi', True)],
    [(5, 'Pi', False), (3, 'Sr', True)],
    [(6, 'Sr', True), (2, 'Ka', True)],
    [(7, 'Ka', True), (1, 'Kr', True), (10, 'Ka', True)],
]
```

… můžeš je vypsat jednotlivě:


```pycon
>>> for sloupecek in sloupecky:
>>>     print(popis_seznam_karet(sloupecek))
[A♠ ] [7 ♥]
[2 ♥] [6 ♦]
[3 ♦] [???]
[???] [4♠ ]
[???] [3 ♥]
[6 ♥] [2 ♦]
[7 ♦] [A♣ ] [X ♦]
```

To ale není to, co chceme vypsat ve hře: tam se karty v jednom sloupečku
ukazují pod sebou.

Budeš potřebovat na prvním řádku ukázat první karty ze všech sloupečků,
na druhém řádku druhé karty ze všech sloupečků, na třetím třetí, atd.
Pro příklad výše by tedy mělo vyjít:


```plain
[A♠ ] [2 ♥] [3 ♦] [???] [???] [6 ♥] [7 ♦]
[7 ♥] [6 ♦] [???] [4♠ ] [3 ♥] [2 ♦] [A♣ ]
                                    [X ♦]
```

Znáš funkci, která vezme několik seznamů, a dá ti k dispozici napřed první
prvky těch seznamů, potom druhé, a tak dál?
Zkus ji použít!

```python
def vypis_sloupecky(sloupecky):
    """Vypíše sloupečky textově.

    Tato funkce je jen pro zobrazení, používá proto přímo funkci print()
    a nic nevrací.
    """
```

* level 40: Funkce existuje
* level 41: Funkce vypisuje karty ze věch sloupečků
* level 42: Funkce funguje, když jsou sloupečky nestejně dlouhé. (Na prázdné místo patří 5 mezer.)


## Práce se sloupečky

Aby sis v budoucnu ušetřil{{a}} práci, a aby sis procvičila seznamy,
zkus teď napsat dvě funkce, které přesunují karty mezi balíčky:

```python
def presun_kartu(sloupec_odkud, sloupec_kam, pozadovane_otoceni):
    """Přesune vrchní kartu ze sloupce "odkud" do sloupce "kam".
    Karta bude otocena lícem nebo rubem nahoru podle "pozadovane_otoceni".
    """

def presun_nekolik_karet(sloupec_odkud, sloupec_kam, pocet):
    """Přesune "pocet" vrchních karet ze sloupce "odkud" do sloupce "kam".
    Karty se přitom neotáčí.
    """
```

* level 50: Funkce `presun_kartu` existuje
* level 51: Funkce `presun_kartu` funguje dle zadání
* level 60: Funkce `presun_nekolik_karet` existuje
* level 61: Funkce `presun_nekolik_karet` funguje dle zadání


## Hra

Vzpomínáš si na schéma hry?

* Rozdej balíček a sloupečky karet
* Dokud hráč nevyhrál:
  * Zobraz stav hry
  * Zeptej se hráče, odkud a kam chce hrát
  * Je-li to možné:
    * Proveď tah
  * Jinak:
    * Vynadej hráči, že daný tah nedává smysl
* Pogratuluj hráči

V Pythonu to bude vypadat následovně.
Program si ulož do modulu `hra.py`:

```python
hra = udelej_hru()

while not hrac_vyhral(hra):
    vypis_hru(hra)
    odkud, kam = nacti_tah()
    try:
        udelej_tah(hra, odkud, kam)
    except ValueError as e:
        print('Něco je špatně:', e)

vypis_hru(hra)
print('Gratuluji!')
```

K tomu, abys doplnila funkce do této hry, budeš potřebovat namodelovat
onu `hru`.
Ta se skládá z několika balíčků/sloupečků, tedy seznamů karet.
Ve výpisu butou pojmenované A-Z:

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

* `U` je dobírací balíček, ze kterého se doplňuje `V`.
* `V` je balíček, ze kterého můžeš brát karty
* `W-Z` jsou cílové hromádky. Cílem hry je na ně přemístit všechny
  karty.
* `A-G` jsou sloupečky, kde se karty dají přeskládávat.

Těchto 13 pojmenovaných seznamů reprezentuje celý stav rozehrané hry.
Hru proto budeme reprezentovat slovníkem, kde klíče budou písmenka
a hodloty pak jednotlivé seznamy.

Následující funkce takovou hru vytvoří:

```python
def udelej_hru():
    """Vrátí slovník reprezentující novou hru.
    """
    balicek = vytvor_balicek()

    hra = {
        'U': balicek,
    }
    # V-Z začínají jako prázdné seznamy
    for pismenko in 'VWXYZ':
        hra[pismenko] = []

    # A-G jsou sloupečky
    for pismenko, sloupec in zip('ABCDEFG', rozdej_sloupecky(balicek)):
        hra[pismenko] = sloupec

    return hra
```

A takhle se hra dá vypsat:

```python
def vypis_hru(hra):
    """Vypíše hru textově.

    Tato funkce je jen pro zobrazení, používá proto přímo funkci print()
    a nic nevrací.
    """
    print()
    print('  U     V           W     X     Y     Z')
    print('{} {}       {} {} {} {}'.format(
        popis_balicku(hra['U']),
        popis_balicku(hra['V']),
        popis_balicku(hra['W']),
        popis_balicku(hra['X']),
        popis_balicku(hra['Y']),
        popis_balicku(hra['Z']),
    ))
    print()
    print('  A     B     C     D     E     F     G')
    vypis_sloupecky([hra['A'], hra['B'], hra['C'], hra['D'],
                     hra['E'], hra['F'], hra['G']])
    print()
```

Pro kontrolu můžeš pustit testy:

* Level 70: Funkce `udelej_hru` existuje
* Level 71: Funkce `udelej_hru` funguje dle zadání
* Level 80: Funkce `vypis_hru` existuje
* Level 81: Funkce `vypis_hru` funguje dle zadání


## Načtení tahu

Hra se bude ovládat zadáním dvou jmen balíčku: odkud a kam hráč chce kartu
přesunout.

Tahle funkce není součást logiky hry. Dej ji do `hra.py`.

```
def nacti_tah():
    while True:
        tah = input('Tah? ')
        try:
            jmeno_zdroje, jmeno_cile = tah.upper()
        except ValueError:
            print('Tah zadávej jako dvě písmenka, např. UV')
        else:
            return jmeno_zdroje, jmeno_cile
```

## Zástupné funkce

K úplné hře nám chybí ještě samotná logika hry: `hrac_vyhral` a `udelej_tah`.

Aby nám hra aspoň trochu fungovala, vytvoř si zástupné funkce,
které nic nekontrolují a nenechají tě vyhrát:

```
def hrac_vyhral(hra):
    """Vrací True, pokud je hra vyhraná.
    """
    return False

def udelej_tah(hra, jmeno_odkud, jmeno_kam):
    presun_kartu(hra[jmeno_odkud], hra[jmeno_kam], True)
```

Obě bude ještě potřeba upravit, ale teď už si můžeš hru víceméně zahrát!
Zkus si to!


## Jiné rozhraní

Celý tento projekt píšeš ve funkcích s daným jménem a s daným počtem a významem
argumentů.
To má dvě výhody.

První z nich je testování: připravené testy importují tvé funkce a zkouší je,
takže si můžeš být jist{{a}}, že fungují.

Druhá je zajímavější: máš-li logiku hry, funkce `udelej_hru` `udelej_tah`
a `hrac_vyhral`, napsané podle specifikací, může je použít i jakýkoli jiný
program – ne jen ten, který jsi napsal{{a}} ty.

Jeden takový si můžeš vyzkoušet:

* Nainstaluj si do virtuálního prostředí knihovnu `pyglet`:

  ```console
  (venv)$ python -m pip install pyglet
  ```

* Stáhni si do aktuálního adresáře soubory [ui.py] a [cards.png].

  [ui.py]: {{ static('ui.py') }}
  [cards.png]: {{ static('cards.png') }}

* Hru spusť pomocí:

  ```console
  (venv)$ python ui.py
  ```

  
*Obrázky karet jsou z [Board Game Pack](https://kenney.nl/assets/boardgame-pack)
studia [kenney.nl](https://kenney.nl).*


## Logika hry

Zbývá doplnit „pravidla hry“ do dvou funkcí, `hrac_vyhral` a `udelej_tah`.
To už bude na tobě.

### hrac_vyhral

Hráč vyhrál, pokud jsou všechny karty na cílových hromádkách `W`-`Z`.

### udelej_tah

Když tah není podle pravidel, funkce `udelej_tah` vyhodí `ValueError`.

Možné tahy:
* `U`→`V`:
  * V balíčku `U` musí něco být
  * Přesouvá se jedna karta; otočí se lícem nahoru
* `V`→`U`:
  * V balíčku U nesmí být nic
  * Přesouvají se všechny karty, seřazené v opačném pořadí;
    otočí se rubem nahoru (tj. volej dokola
    `presun_kartu(hra['V'], hra['U'], False)` dokud ve V něco je)
* Balíček `V` nebo sloupeček `A`-`G` (zdroj) → cíl `W`-`Z`: 
  * Přesouvá se jedna karta
  * Je-li cíl prázdný:
    * Musí to být eso
  * Jinak:
    * Přesouvaná karta musí mít stejnou barvu jako vrchní karta cíle
    * Přesouvaná karta musí být o 1 vyšší než vrchní karta cíle
  * Je-li zdroj po přesunu neprázdný, jeho vrchní karta se otočí lícem nahoru
* Balíček `V` → „cílový“ sloupeček `A`-`G`
  * Přesouvá se jedna karta
  * Přesouvaná karta musí pasovat\*⁾ na cílový sloupeček
* „Zdrojový“ sloupeček `A`-`G` → „cílový“ sloupeček `A`-`G`
  * Přesouvá se několik karet
    * (zkontroluj všechny možnosti: 1 až počet karet ve zdrojovém sloupečku;
      vždy je max. jedna správná možnost) 
  * Všechny přesouvané karty musí být otočené lícem nahoru
  * První z přesouvaných karet musí pasovat*) na cílový sloupeček
* Cíl `W`-`Z` → sloupeček `A`-`G` (nepovinné – jen v některých variantách hry)
  * Přesouvá se jedna karta
  * Přesouvaná karta musí pasovat*) na cílový sloupeček

\*⁾ Kdy přesouvaná karta pasuje na sloupeček?
* Je-li sloupeček prázdný:
  * Karta musí být král
* Jinak:
  * Barva přesouvané karty musí být opačná než barva vrchní karty sloupečku, tedy:
    * Červená (♥ nebo ♦) jde dát jen na černou (♠ nebo ♣)
    * Černá (♠ nebo ♣) jde dát jen na červenou (♥ nebo ♦)
  * Hodnota přesouvané karty musí být o 1 nižší než hodnota vrchní karty sloupečku
