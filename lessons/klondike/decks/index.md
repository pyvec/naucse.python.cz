# Klondike Solitaire: Balíčky

> [warning] Předbíháš!
> Tyto materiály nejsou dopsané. Nemusí dávat smysl.

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
