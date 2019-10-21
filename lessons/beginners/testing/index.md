# Testování

Programátorská práce nespočívá jen v tom, program napsat.
Důležité je si i ověřit, že opravdu funguje, a případně ho pak opravit.
Ověřování, že program funguje, se říká *testování* (angl. *testing*).

Zatím jsi asi svoje programy testoval{{a}} tak, že jsi
je zkusil{{a}} spustit, něco zadal{{a}} a podíval{{a}} se,
jestli jsou výsledky v pořádku.
U větších programů, které budou mít více a více
možností, ale bude těžší a těžší takhle zkontrolovat,
jestli všechny ty možnosti fungují jak mají.

Proto si programátoři často nezkouší programy „ručně“.
Píšou jiné programy, které jejich výtvory testují za ně.

*Automatické testy* jsou funkce, které
zkontrolují že program funguje správně.
Spuštěním testů můžeš kdykoli ověřit, že kód funguje.
Když v otestovaném kódu v budoucnu uděláš nějakou změnu,
testy ověří, že jsi nerozbil{{a}} nic, co dříve fungovalo.


## Instalace knihovny pytest

Zatím jsme v kurzu pracoval{{ gnd('i', 'y') }} s tím, co se instaluje
se samotným Pythonem – s moduly jako `math` a `turtle`.
Kromě takových modulů ale existuje ale velká spousta
dalších *knihoven*, které nejsou přímo v Pythonu, ale dají se doinstalovat
a používat.

Na testy je v samotném Pythonu zabudovaná knihovna `unittest`.
Ta je ale celkem složitá na použití, proto ji my používat nebudeme.
Nainstalujeme si knihovnu <code>pytest</code>, která se používá
mnohem jednodušeji a je velice populární.

Knihovny se instalují do aktivního virtuálního prostředí.
Jak se dělá a spouští virtuální prostředí
ses naučil{{a}} při [instalaci Pythonu]({{ lesson_url('beginners/install') }}),
ale teprve teď to začíná být opravdu důležité.
Ujisti se, že máš virtuální prostředí aktivované.

Potom zadej následující příkaz.
(Je to příkaz příkazové řádky, podobně jako
`cd` nebo `mkdir`; nezadávej ho do Pythonu.)

> [warning] Opisuj opatrně!
> Příkaz níže instaluje software z Internetu.
> Za knihovnu `pytest` autoři tohoto kurzu ručí.
> Jiné knihovny ale můžou dělat neplechu nebo být dokonce „zavirované“.
> Dej si proto pozor a ve jménu `pytest` neudělej překlep!

```console
(venv)$ python -m pip install pytest
```

> [note] Co ten příkaz znamená?
> `python -m pip` zavolá Python s tím, že má pustit modul
> `pip`. Tento modul umí instalovat nebo
> odinstalovávat knihovny.
> (Jestli si pamatuješ vytváření virtuálního prostředí, použil{{a}} jsi tam
> příkaz `python -m venv` – modul `venv` umí vytvářet virtuální prostředí.)
> No a slova `install pytest` říkají Pipu, že má nainstalovat `pytest`.
>
> Nápověda k použití Pipu se dá vypsat pomocí příkazu
> `python -m pip --help`.

> [warning] Pro Windows
> Jsi-li na Windows, od této lekce začne být důležité
> spouštět pythonní programy pomocí `python program.py`, ne jen
> `program.py`.
> Ačkoli se v těchto materiálech všude používá `python` na začátku, zatím
> mohlo všechno fungovat i bez toho.
> Program se ale bez příkazu `python` může spustit v jiném Pythonu,
> než v tom z virtuálního prostředí – a tam `pytest` nebude k dispozici.


## Psaní testů

Nejdříve si testování ukážeme na jednoduchém příkladu.
Tady je funkce `secti`, která umí sečíst
dvě čísla, a další funkce, která testuje, jestli se
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

Příkaz `assert` vyhodnotí výraz za ním a pokud výsledek není pravdivý,
vyvolá výjimku která způsobí že test selže.
Můžeš si představit, že `assert a == b` dělá následující:

```python
if not (a == b):
    raise AssertionError('Test selhal!')
```

> [note]
> Zatím `assert` nepoužívej jinde než v testovacích funkcích.
> V „normálním” kódu se `assert` může chovat trochu jinak než výše,
> ale do toho teď nebudeme zabředávat.


## Spouštění testů

Testy se spouští zadáním příkazu
`python -m pytest -v` následovaným názvem souboru s testy.
Tedy v překladu: <strong>Python</strong>e, pusť
<strong>m</strong>odul <strong>pytest</strong>,
v „ukecaném” režimu (angl. <strong>v</strong>erbose) a se zadaným souborem.

```console
$ python -m pytest -v test_secteni.py
```

```pytest
============================= test session starts ==============================
platform linux -- Python 3.7.1, pytest-3.6.4, py-1.5.4, pluggy-0.6.0 -- venv/bin/python
cachedir: .pytest_cache
rootdir: naucse, inifile:
collecting ... collected 1 item

test_secteni.py::test_secti PASSED                                       [100%]

=========================== 1 passed in 0.00 seconds ===========================
```

Tento příkaz projde zadaný soubor, zavolá v něm všechny funkce,
jejichž jméno začíná na `test_`, a ověří že nevyvolají žádnou
výjimku – typicky výjimku z příkazu `assert`.
Pokud výjimka nastane, dá to `pytest` velice červeně
najevo a přidá několik informací, které můžou
usnadnit nalezení a opravu chyby.

> [note]
> Argument s názvem souboru můžeš vynechat: `python -m pytest -v`.
> V takovém případě `pytest` projde aktuální adresář a spustí testy
> ze všech souborů, jejichž jméno začíná na `test_`. Místo souboru
> lze též uvést adresář: `pytest` vyhledá testy v něm.

Zkus si změnit funkci `secti` (nebo její test) a podívat se,
jak to vypadá když test „neprojde“.


## Testovací moduly

Testy se většinou nepíšou přímo ke kódu,
ale do souboru vedle.
Je to tak přehlednější a taky to pak zjednodušuje
*distribuci* – předání kódu někomu, kdo ho chce
jen spustit a testy nepotřebuje.

Rozděl soubor s testem sečítání: funkci `secti` přesuň do modulu `secteni.py`,
a v `test_secteni.py` nech jenom test.
Do `test_secteni.py` pak na začátek přidej `from secteni import secti`,
aby byla funkce testu k dispozici.

Test by měl opět projít.


## Spouštěcí moduly

Automatické testy musí projít „bez dozoru“.
V praxi se často automaticky spouští, případné chyby se automaticky
oznamují (např. e-mailem) a fungující otestovaný kód se automaticky
začne používat dál (nebo se rovnou vydá zákazníkům).

Co to znamená pro nás?
Funkce `input` v testech nefunguje. Nemá koho by se zeptala; „za klávesnicí“
nemusí nikdo sedět.

To může někdy „ztěžovat práci“. Ukážeme si to na složitějším projektu:
na 1D piškvorkách.

> [note]
{% if var('coach-present') -%}
> Nemáš-li hotové 1D piškvorky, následující sekce budou jen teorietické.
{% endif -%}
> Učíš-li se z domu, dodělej si Piškvorky než budeš pokračovat dál!
> Zadání najdeš (prozatím)
> v [projektech pro PyLadies](http://pyladies.cz/v1/s004-strings/handout/handout4.pdf)
> na straně 2.

Kód pro 1D Piškvorky může rámcově vypadat zhruba takto:

```python
import random  # (příp. import jiných věcí, které budou potřeba)

def tah(pole, cislo_policka, symbol):
    """Vrátí pole s daným symbolem umístěným na danou pozici"""
    ...

def tah_hrace(pole):
    """Zeptá se hráče kam chce hrát a vrátí pole se zaznamenaným tahem"""
    ...
    input('Kam chceš hrát? ')
    ...

def piskvorky1d():
    """Spustí hru

    Vytvoří hrací pole a střídavě volá tah_hrace a tah_pocitace
    dokud někdo nevyhraje"""
    while ...:
        ...
        tah_hrace(...)
        ...

# Puštění hry!
piskvorky1d()
```

Když tenhle modul naimportuješ, Python v něm postupně, odshora dolů,
provede všechny příkazy.

První příkaz, `import`, jen zpřístupní nějaké proměnné a funkce;
je-li importovaný modul správně napsaný, nemá vedlejší účinek.
Definice funkcí (příkazy `def` a všechno v nich) podobně jen definují funkce.
Ale zavoláním funkce `piskvorky1d` se spustí hra:
funkce `piskvorky1d` zavolá funkci `tah_hrace()` a ta zavolá `input()`.

Importuješ-li tenhle modul z testů, `input` selže a import se nepovede.

> [note]
> A kdybys modul importoval{{a}} odjinud – například bys chtěl{{a}} funkci
> `tah` použít v nějaké jiné hře – uživatel si bude muset v rámci importu
> zahrát Piškvorky!

Volání funkce `piskvorky1d` je vedlejší efekt, a je potřeba ho odstranit.
No jo, ale po takovém odstranění
už nejde jednoduše spustit hra! Co s tím?

Můžeš na to vytvořit nový modul.
Pojmenuj ho `hra.py` a dej do něj jenom to odstraněné volání:

```python
import piskvorky

piskvorky.piskvorky1d()
```

Tenhle modul nebudeš moci testovat (protože nepřímo volá funkci `input`),
ale můžeš ho spustit, když si budeš chtít zahrát.
Protože k němu nemáš napsané testy, nepoznáš
z nich, když se takový spouštěcí modul rozbije.
Měl by být proto nejjednodušší – jeden import a jedno volání.

Původní modul teď můžeš importovat bez obav – ať už z testů nebo z jiných
modulů.
Test může vypadat třeba takhle:

```python
import piskvorky

def test_tah_na_prazdne_pole():
    pole = piskvorky.tah_pocitace('--------------------')
    assert len(pole) == 20
    assert pole.count('x') == 1
    assert pole.count('-') == 19
```

## Pozitivní a negativní testy

Testům, které kontrolují, že se program za správných podmínek chová správně,
se říká *pozitivní testy*.
Můžeš ale testovat i reakci programu na špatné nebo neočekávané podmínky.

Testy, které kontrolují reakci na „špatný“ vstup,
se jmenují *negativní testy*.
Můžou kontrolovat nějaký negativní výsledek (např.
že volání jako <code>cislo_je_sude(7)</code> vrátí `False`),
a nebo to, že nastane „rozumná“ výjimka.

Například funkce `tah_pocitace` by měla způsobit
chybu (třeba `ValueError`), když je herní pole už plné.

> [note]
> Vyvolat výjimku je mnohem lepší než alternativy, např. kdyby takové volání
> „tiše“ – bez oznámení – zablokovalo celý program.
> Když kód pak použiješ ve větším programu,
> můžeš si být jistá, že při špatném volání
> dostaneš srozumitelnou chybu – tedy takovou,
> která se co nejsnadněji opravuje.

Na otestování výjimky použij příkaz `with` a funkci `raises` naimportovanou
z modulu `pytest`.
Jak příkaz `with` přesně funguje, se dozvíme později;
teď stačí říct, že ověří, že odsazený blok kódu
pod ním vyvolá danou výjimku:

```python
import pytest

import piskvorky

def test_tah_chyba():
    with pytest.raises(ValueError):
        piskvorky.tah_pocitace('oxoxoxoxoxoxoxoxoxox')
```

