# Testování

Programátorská práce nespočívá jen v tom, program napsat.
Důležité je si i ověřit, že opravdu funguje (a případně ho pak opravit).
Ověřování, že program funguje, se říká *testování*.

Zatím jsi asi svoje programy testoval{{a}} tak, že jsi
je zkusil{{a}} spustit, něco zadal{aa}, a podíval{{a}} se
jestli jsou výsledky v pořádku.
U větších programů, které budou mít více a více
možností, ale bude těžší a těžší takhle zkontrolovat,
jestli všechny ty možnosti fungují jak mají.

Proto si programátoři, místo aby program zkoušeli ručně, píšou jiné programy,
které testují za ně.

*Automatické testy* jsou funkce, které
zkontrolují, že náš program funguje správně.
Spuštěním testů můžeš kdykoli ověřit že kód funguje.
Hlavní výhoda je, že když v otestovaném kódu
v budoucnu uděláš nějakou změnu,
testy ověří, že jsi nerozbil{{a}} nic co dříve
fungovalo.


## Instalace knihovny pytest

Na testy je v samotném Pythonu zabudovaná knihovna `unittest`.
My ji však používat nebudeme: nainstalujeme si
kniihovnu <code>pytest</code>, která se používá
mnohem jednodušeji a je velice populární.

Je ji ale potřeba nainstalovat.

!!! note ""
    Zatím jsme v kurzu pracovaly s tím, co se instaluje
    se samotným Pythonem.
    Kromě věcí jako `math` nebo `turtle` ale existuje ale spousta
    dalších užitečných *knihoven*, které se dají jednoduše doinstalovat
    a používat.

Následující příkaz nainstaluje do aktivního virtuálního prostředí knihovnu
`pytest`.
Je to příkaz příkazové řádky, podobně jako
`cd` nebo `mkdir`; nezadávej ho do Pythonu.

(Jak se dělá a spouští virtuální prostředí
ses naučil{{a}} při [instalaci Pythonu]({{ lesson_url('beginners/install') }}),
ale teprve teď to začíná být důležité. Ujisti se, že máš virtuální prostředí
aktivované.)

```console
(venv)$ python -m pip install pytest
```

!!! note "Co to znamená?"
    `python -m pip` zavolá Python s tím, že má pustit modul
    `pip`. Tento modul umí instalovat nebo
    odinstalovávat knihovny.
    Jestli si pamatuješ vytváření virtuálního prostředí, použil{{a}} jsi tam
    příkaz `python -m venv`.
    Modul `venv` umí vytvářet virtuální prostředí.
    No a slova `install pytest` říkají Pipu, že má nainstalovat `pytest`.

    Nápověda k použití Pipu se dá vypsat pomocí příkazu
    `python -m pip --help`.

!!! warning "Pro Windows"
    Jsi-li na Windows, od této lekce bude důležité
    spouštět Pythoní programy pomocí `python program.py`, ne jen
    `program.py`.
    Ačkoli se v těchto materiálech všude používá `python` na začátku, zatím
    mohlo všechno fungovat i bez toho.
    Program se ale bez příkazu `python` spouští v jiném Pythonu,
    než v tom z virtuálního prostředí.


## Psaní testů

Tady je funkce `secti`, která umí sečíst
dvě čísla, a další funkce která testuje, jestli se
`secti` pro určité hodnoty
chová správně.

Kód si opiš do souboru `test_secteni.py`,
v novém prázdném adresáři.
Pro `pytest` je (ve výchozím nastavení)
důležité, aby jména jak souborů s testy, tak
samotných testovacích funkcí, začínala na
`test_`.

```python
def secti(a, b):
    return a + b

def test_secti():
    assert secti(1, 2) == 3
```

Co se v té testovací funkci děje?

Příkaz `assert` vyhodnotí výraz za ním,
a pokud výsledek není pravdivý, vyvolá výjimku,
která způsobí že test selže.
Můžeš si představit, že `assert a == b` dělá následující:

```python
if not (a == b):
    raise AssertionError('Test selhal!')
```

Zatím `assert` nepoužívej jinde než v testovacích funkcích.
V „normálním” kódu má `assert` vlastnosti,
do kterých teď nebudeme zabředávat.


## Spouštění testů

Testy se spouští zadáním příkazu
`python -m pytest -v`,
tedy v překladu: <strong>Python</strong>e, pusť
<strong>m</strong>odul <strong>pytest</strong>,
v „ukecaném” režimu (angl. <strong>v</strong>erbose).

```ansi
$ python -m pytest -v test_secteni.py 
␛[1m============= test session starts =============␛[0m
platform linux -- Python 3.6.0, pytest-3.0.6, py-1.4.32, pluggy-0.4.0 -- env/bin/python
cachedir: .cache
rootdir: naucse, inifile: 
␛[1mcollecting ...␛[0m collected 1 items

test_secteni.py::test_secti ␛[32mPASSED␛[0m

␛[32m============= 1 passed in 0.00 seconds =============␛[0m
```

Tento příkaz projde všechny soubory v aktuálním
adresáři, jejichž jméno začíná na `test_`, zavolá v nich všechny funkce,
jejichž jméno začíná na `test_`, a ověří, že nevyvolají žádnou výjimku.
Pokud výjimka nastane, dá to velice červeně
najevo, a přidá několik informací které můžou
usnadnit nalezení a opravu chyby.


## Testovací moduly

Testy se většinou nepíšou přímo ke kódu,
ale do souboru vedle.
Je to tak přehlednější, a taky to zjednodušuje
distribuci – předávání kódu někomu, kdo ho chce
jen spustit a testy nepotřebuje

!!! note ""
    Máš-li hotové 1D piškvorky, zkus si následující
    příklad.
    Jinak si rozděl soubor s testem sečítání: do
    `secteni.py` dej funkci `secti`,
    a do `test_secteni.py` test.
    Do `test_secteni.py` pak přidej
    `from secteni import secti`, aby byla
    funkce testu k dispozici.

Vytvoř si modul `test_piskvorky` (tedy soubor
`test_piskvorky.py`), a do něj napiš:

```python
import piskvorky

def test_tah_na_prazdne_pole():
    pole = piskvorky.tah_pocitace('--------------------')
    assert len(pole) == 20
    assert pole.count('x') == 1
    assert pole.count('-') == 19
```

Pak vedle něj (t.j. do stejného adresáře)
zkopíruj svůj program
`piskvorky.py`, ze kterého vyndej
kód, který není ve funkcích
(t.j. samotné volání funkce `piskvorky1d`).
Příkazem `python -m pytest` teď můžeš
kdykoli otestovat, že funkce `tah_pocitace`
funguje s prázdným hracím polem!


## Spouštěcí moduly

Jsi-li na sraze a nemáš-li hotové 1D piškvorky,
následující sekce budou jen teorietické.
Učíš-li se z domu, dodělej si Piškvorky před němi!

Příkaz `import` provede všechny příkazy,
které jsou v importovaném modulu: nejen definice
funkcí, ale i všelijaké volání `print`, `input` nebo jiné příkazy mimo funkce.
Má-li být modul použitelný na `import`, chceme se
většinou podobných efektů vyvarovat.

Konkrétně v Piškvorkách: Definice funkcí
(příkazy `def` a všechno v nich)
jen definují funkce, nemají žádný další účinek,
ale *volání* funkce `piskvorky1d` spustí hru: zavolá se `tah_hrace`
a z ní i `input`.
Testy ale nemají jak se ptát uživatele na vstup, takže v nich `input` nefunguje.
Volání funkce `piskvorky1d` je proto potřeba odstranit.

No jo, ale po takovém odstranění
už nejde jednoduše spustit hra! Co s tím?

Můžeš na to vytvořit nový modul.
Pojmenuj ho `hra.py`, a dej to něj jenom to odstraněné volání:

```python
import piskvorky

piskvorky.piskvorky1d()
```

Tenhle modul nebudeš moci testovat (protože nepřímo volá funkci `input()`),
ale můžeš ho spustit, když si budeš
chtít zahrát.
Protože k němu nemáš napsané testy, nepoznáš
z nich, když se takový spouštěcí modul rozbije.
Měl by být proto nejjednodušší.


## Pozitivní a negativní testy

Můžeš testovat i reakci programu na
neočekávaný vstup, například funkce
`tah_pocitace` by měla způsobit
chybu (třeba `ValueError`),
když je herní pole už plné.

Na to použij příkaz `with` a funkci `raises` naimportovanou
z modulu `pytest`.
Jak příkaz `with` přesně funguje se dozvíme později;
teď stačí říct, že ověří, že odsazený blok kódu
pod ním vyvolá danou výjimku:

```python
import pytest

import piskvorky

def test_tah_chyba():
    with pytest.raises(ValueError):
        piskvorky.tah_pocitace('oxoxoxoxoxoxoxoxoxox')
```

Testy, které kontrolují reakci na „špatný“ vstup,
se jmenují *negativní testy*.
Většinou kontrolují že nastane (správná) chyba,
nebo nějaký negativní výsledek (např.
že volání jako <code>cislo_je_sude(7)</code> vrátí `False`).
Když kód pak použiješ ve větším programu,
můžeš si být jistá, že při špatném volání
dostaneš srozumitelnou chybu – tedy takovou,
která se co nejsnadněji opravuje.
