# Výjimky

Pojďme si prohloubit znalosti o chybách, neboli odborně o *výjimkách*
(angl. *exceptions*).

Vezmi následující funkci:

```python
def nacti_cislo():
    odpoved = input('Zadej číslo: ')
    return int(odpoved)
```

Když uživatel nezadá číslice, ale třeba text `cokolada`,
nastane výjimka jménem `ValueError` (chyba hodnoty) a Python vypíše
odpovídající chybovou hlášku.

```pycon
Traceback (most recent call last):
  File "ukazka.py", line 3, in nacti_cislo
    cislo = int(odpoved)
ValueError: invalid literal for int() with base 10: 'cokolada'
```

Program volá funkci `int()` pro něco, co nedává smysl jako číslo.
Co s tím má chudák funkce `int` dělat?
Není žádná rozumná hodnota, kterou by mohla vrátit.
Převádění tohoto textu na celé číslo nedává smysl.

Až funkce `nacti_cislo` nejlíp „ví“, co se má stát, když uživatel nezadá
číslice.
Stačí se uživatele zeptat znovu!
Kdybys měl{{a}} funkci, která zjistí jestli jsou v řetězci jen číslice,
mohlo by to fungovat nějak takhle:

```python
def nacti_cislo():
    while True:
        odpoved = input('Zadej číslo: ')
        if obsahuje_jen_cislice(odpoved):
            return int(odpoved)  # máme výsledek, funkce končí
        else:
            print('To nebylo číslo!')
            # ... a zeptáme se znovu -- cyklus `while` pokračuje
```

Kde ale vzít funkci `obsahuje_jen_cislice`?
Nemá smysl ji psát znovu – funkce `int` sama nejlíp pozná, co se dá převést na
číslo a co ne.
A dokonce nám to dá vědět – chybou, kterou můžeš *zachytit*.

> [note]
> Ono „obsahuje_jen_cislice“ v Pythonu existuje. Dokonce několikrát.
> Místo řešení problému to ale spíš ilustruje, v čem problém spočívá:
> * Řetězcová metoda `isnumeric` vrací `True` pokud řetězec obsahuje číslice:
>   `'123'.isnumeric()` je pravda; `'abc'.isnumeric()` nepravda.
>   Problém je, že funkci `int` potřebuje jeden konkrétní druh číslic:
>   pro řetězce jako `'½'` nebo `'௩三๓໓`' (trojka v tamilském, japonském,
>   thajském nebo laoském písmu) platí `isnumeric`, ale `int` si na nich
>   vyláme zuby stejně jako na `'abc'`.
> * Řetězcová metoda `isdecimal` vrací `True` pokud řetězec obsahuje arabské
>   číslice 0-9. To už je lepší, ale stejně to úplně nesedí: `int` si poradí
>   s mezerou na začátku, např. s `' 3'`, ale funkce `isdecimal` takový řetězec
>   odmítne.
>
> Chceš-li zjistit jestli funkce `int` umí daný řetězec převést na číslo,
> nejlepší je použít přímo funkci `int`.


## Ošetření chyby

Pro zachycení chyby má Python příkaz `try`/`except`.

```python
def nacti_cislo():
    while True:
        odpoved = input('Zadej číslo: ')
        try:
            return int(odpoved)
        except ValueError:
            print('To nebylo číslo!')
```

Jak to funguje?
Příkazy v bloku uvozeném příkazem `try` se normálně provádějí, ale když
nastane uvedená výjimka, Python přeskočí zbytek bloku `try` a provede všechno 
v bloku `except`.
Pokud výjimka nenastala, přeskočí se celý blok `except`.


## Druhy chyb

A co je to `ValueError`? To je typ chyby.
Podobných typů je spousta.
Všechny jsou popsané [v dokumentaci](https://docs.python.org/3/library/exceptions.html#exception-hierarchy); pro nás jsou (nebo budou) důležité tyto:

```plain
BaseException
 ├── SystemExit                     vyvolána funkcí exit()
 ├── KeyboardInterrupt              vyvolána po stisknutí Ctrl+C
 ╰── Exception
      ├── ArithmeticError
      │    ╰── ZeroDivisionError    dělení nulou
      ├── AssertionError            nepovedený příkaz `assert`
      ├── AttributeError            neexistující atribut/metoda, např. 'abc'.len
      ├── ImportError               nepovedený import
      ├── LookupError
      │    ╰── IndexError           neexistující index, např. 'abc'[999]
      ├── NameError                 použití neexistujícího jména proměnné
      │    ╰── UnboundLocalError    použití proměnné, která ještě nebyla nastavená
      ├── SyntaxError               špatná syntaxe, program je nečitelný/nepoužitelný
      │    ╰── IndentationError     špatné odsazení
      │         ╰── TabError        kombinování mezer a tabulátorů v odsazení
      ├── TypeError                 špatný typ, např. len(9)
      ╰── ValueError                špatná hodnota, např. int('xyz')
```

Tohle si není potřeba pamatovat – druh chyby, kterou je potřeba zachytit,
vždy najdeš v příslušné chybové hlášce.

Když odchytáváš obecnou výjimku,
chytnou se i všechny podřízené typy výjimek –
například `except ArithmeticError:` zachytí i `ZeroDivisionError`.
A `except Exception:` zachytí *všechny* výjimky, které běžně chceš zachytit.


## Nechytej je všechny!

Většinu chyb *není* potřeba ošetřovat.

Nastane-li *nečekaná* situace, je téměř vždy
mnohem lepší program ukončit, než se snažit
pokračovat dál a počítat se špatnými hodnotami.
Navíc chybový výstup, který Python standardně
připraví, může hodně ulehčit hledání chyby.

Zachytávej tedy jenom ty chyby, které *očekáváš* – víš přesně, která chyba může
nastat a proč; máš možnost správně zareagovat.

V našem příkladu to platí pro `ValueError` z funkce `int`: víš že uživatel
nemusí vždy zadat číslo ve správném formátu a víš že správná
reakce na tuhle situaci je problém vysvětlit a zeptat se znovu.

Co ale dělat, kdyš uživatel chce ukončit program a zmáčkne
<kbd>Ctrl</kbd>+<kbd>C</kbd>?
Nebo když se mu porouchá klávesnice a selže funkce `input`?
Nejlepší reakce na takovou nečekanou situaci ukončit program a informovat
uživatele (nebo lépe, programátora), že (a kde) je něco špatně.
Neboli vypsat chybovou hlášku.
A to se stane normálně, bez `try`.


## Další přílohy k `try`

Pro úplnost: kromě `except` existují dva jiné bloky,
které můžeš „přilepit“ k `try`, a to `else` a `finally`.
První se provede, když v `try` bloku
žádná chyba nenastane; druhý se provede vždy – ať
už chyba nastala nebo ne.

Můžeš taky použít více bloků `except`. Provede se vždy maximálně jeden:
ten první, který danou chybu umí ošetřit.

```python
try:
    neco_udelej()
except ValueError:
    print('Tohle se provede, pokud nastane ValueError')
except NameError:
    print('Tohle se provede, pokud nastane NameError')
except Exception:
    print('Tohle se provede, pokud nastane jiná chyba')
    # (kromě SystemExit a KeyboardInterrupt, ty chytat nechceme)
except TypeError:
    print('Tohle se neprovede nikdy')
    # ("except Exception" výše ošetřuje i TypeError; sem se Python nedostane)
else:
    print('Tohle se provede, pokud chyba nenastane')
finally:
    print('Tohle se provede vždycky; i pokud v `try` bloku byl např. `return`')
```



## Vyvolání chyby

Občas se stane, že výjimku budeš potřebovat vyvolat {{gnd('sám', 'sama')}}.

Často se to stává když píšeš nějakou obecnou funkci.
Třeba funkci na výpočet obsahu čtverce.
Co se stane, když někdo zavolá `obsah_ctverce(-5)`?

* Zadal-li ono `-5` uživatel, je potřeba mu vynadat a zeptat se znovu.
* Naměřil-li `-5` nějaký robotický aparát, je potřeba ho líp zkalibrovat.
* Vyšel-li čtverec se stranou `-5` v nějakém výpočtu, je nejspíš potřeba opravit
  chybu v tom výpočtu.

Samotná funkce `obsah_ctverce` ale „neví“, proč ji někdo volá.
Jejím úkolem je jen něco spočítat.
Měla by být použitelná ve všech případech výše – a v mnoha dalších.

Když někdo zavolá `obsah_ctverce(-5)`, *neexistuje* správný výsledek, který by
funkce mohla vrátit.
Místo vrácení výsledku musí tato funkce *signalizovat chybu*.
S tou se pak může program, který `obsah_ctverce(-5)` zavolal,
vypořádat – vynadat uživateli, zkalibrovat měřák, nebo, pokud na chybu není
připravený, sám skončit s chybou (a upozornit tak programátora, že je něco
špatně).

Jak na to prakticky?
Chybu můžeš vyvolat pomocí příkazu `raise`.
Za příkaz dáš druh výjimky a pak do závorek nějaký popis toho, co je špatně.

```python
def obsah_ctverce(strana):
    if strana > 0:
        return strana ** 2
    else:
        raise ValueError(f'Strana musí být kladná, číslo {strana} kladné není!')
```

Podobně jako `return`, i příkaz `raise` ukončí funkci.
A nejen tu – pokud na tuhle konkrétní chybu není program předem připravený,
ukončí se celý program.

Ze začátku není u `raise` příliš důležité dumat nad tím, který typ výjimky je
ten správný.
Klidně „střílej od boku“.
`ValueError` bývá často správná volba.
