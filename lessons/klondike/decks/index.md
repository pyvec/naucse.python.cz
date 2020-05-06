# Klondike Solitaire: Balíčky

Postupně tvoříme hru *Klondike Solitaire*, která bude nakonec fungovat takto:

* Karty se určitým způsobem *rozdají* do několika balíčků, hromádek nebo
  jiných skupin
* Dokud hráč *nevyhrál*:
  * Hráč *udělá tah*: podle určitých pravidel přesune karty z jedné hromádky
    na druhou

Pro počítačovou verzi to bude potřeba doplnit o zobrazení stavu hry
a o načítání hráčova tahu:

* Rozdej karty
* Dokud hráč nevyhrál:
  * Zobraz stav hry
  * Zeptej se hráče, kam chce hrát
  * Je-li to možné:
    * Proveď tah
  * Jinak:
    * Vynadej hráči, že daný tah nedává smysl
* Pogratuluj hráči

(Hráč může i prohrát, ale na to může přijít sám a hru ukončit.)

Minule jsme počítač naučil{{gnd('i', 'y', both='i')}} co to je *karta*
a jak vytvořit zamíchaný *balíček*.
Pojďme se konečně vrhnout na první krok výše: rozdávání.


## Rozdání sloupečků

Karty se určitým způsobem *rozdají* do několika balíčků, hromádek nebo
jiných skupin.
Pro přehlednost si tyto skupiny označíme písmenky:

* Dobírací balíčky `U`, `V`, ze kterých se berou karty.
* Cílové hromádky `W`-`Z`, kam se dávají seřazené karty. Cíl hry je do těchto
  hromádek dát všechny karty.
* 7 sloupečků `A`-`G`, kde hráč může s kartami manipulovat.

Prvotní rozdání karet spočívá v tom, že rozdáš karty do 7 sloupečků.
Nerozdané karty zůstanou v balíčku `U`; ostatní místa na karty budou prázdná:

{{ figure(img=static('game.png'), alt="Ukázka sloupečků") }}

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

V <var>N</var>-tém sloupečku (počítáno od nuly) je <var>N</var>
karet rubem nahoru plus jedna karta lícem nahoru.
Karty do sloupečků se z balíčku rozdávají postupně: vždy se lízne
vrchní (poslední) karta z balíčku a dá se na konec sloupečku.


Napiš následující funkci:

```python
def rozdej_sloupecky(balicek):
    """Rozdá z daného balíčku 7 "sloupečků" -- seznamů karet

    Karty ve sloupečcích jsou odstraněny z balíčku.
    Vrátí všechny sloupečky -- tedy seznam (nebo n-tici) sedmi seznamů.
    """
```

Například:

```pycon
>>> balicek = priprav_balicek()
>>> sloupecky = rozdej_sloupecky(balicek)
>>> popis_seznam_karet(sloupecky[0])
[3♣ ]
>>> popis_seznam_karet(sloupecky[1])
[???] [5 ♥]
>>> popis_seznam_karet(sloupecky[2])
[???] [???] [6♣ ]
>>> popis_seznam_karet(sloupecky[6])
[???] [???] [???] [???] [???] [???] [3 ♦]
>>> len(balicek)    # Z balíčku zmizely karty, které jsou ve sloupečcích
24
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

Pro ověření spusť testy:

* level 40: Funkce existuje
* level 41: Funkce vrací seznam sedmi seznamů
* level 42:
  * V každém sloupečku je aspoň jedna karta
  * Poslední karta je lícem nahoru
* level 43: V každém sloupečku je správný počet karet rubem nahoru


## Vypsání sloupečků

Vzpomínáš si na základní schéma hry?

* Rozdej karty
* Dokud hráč nevyhrál:
  * Zobraz stav hry
  * Zeptej se hráče, kam chce hrát
  * Je-li to možné:
    * Proveď tah
  * Jinak:
    * Vynadej hráči, že daný tah nedává smysl
* Pogratuluj hráči

Rozdání balíčku a sloupečků už víceméně máš!
Pro teď přeskočíme zjišťování, jestli hráč vyhrál, a koukneme se na zobrazení
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

Pozor, bude tu potřeba pořádně se zamyslet.

```python
def vypis_sloupecky(sloupecky):
    """Vypíše sloupečky textově.

    Tato funkce je jen pro zobrazení, používá proto přímo funkci print()
    a nic nevrací.
    """
```

* level 50: Funkce existuje
* level 51: Funkce vypisuje karty ze věch sloupečků
* level 52: Funkce funguje, když jsou sloupečky nestejně dlouhé. (Na prázdné místo patří 5 mezer.)


## Práce se sloupečky

Aby sis v budoucnu ušetřil{{a}} práci, a aby sis procvičila seznamy,
zkus teď napsat dvě funkce, které přesunují karty mezi balíčky.

Použij na to metody seznamů (`append`, `extend`, `pop`, příkaz `del`)
a pomocné funkce, které už máš (`otoc_kartu`).

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

* level 60: Funkce `presun_kartu` existuje
* level 61: Funkce `presun_kartu` funguje dle zadání
* level 70: Funkce `presun_nekolik_karet` existuje
* level 71: Funkce `presun_nekolik_karet` funguje dle zadání
