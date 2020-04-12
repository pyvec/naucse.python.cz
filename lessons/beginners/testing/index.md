# Testování

Programátorská práce nespočívá jen v tom, program napsat.
Důležité je si i ověřit, že opravdu funguje (a případně ho pak opravit).
Ověřování, že program funguje, se říká *testování*.

Zatím jsi asi svoje programy testoval{{a}} tak, že jsi
je zkusil{{a}} spustit, něco zadal{{a}} a podíval{{a}} se,
jestli jsou výsledky v pořádku.
U větších programů, které budou mít více a více
možností, ale bude těžší a těžší takhle zkontrolovat,
jestli všechny ty možnosti fungují, jak mají.

Proto si programátoři, místo aby program zkoušeli ručně, píšou jiné programy,
které testují jejich výtvory za ně.

*Automatické testy* jsou funkce, které
zkontrolují, že náš program funguje správně.
Spuštěním testů můžeš kdykoli ověřit, že kód funguje.
Hlavní výhoda je, že když v otestovaném kódu
v budoucnu uděláš nějakou změnu,
testy ověří, že jsi nerozbil{{a}} nic, co dříve
fungovalo.


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

```console
(venv)$ python -m pip install pytest
```

> [note] Co to znamená?
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

Příkaz `assert` vyhodnotí výraz za ním
a pokud výsledek není pravdivý, vyvolá výjimku,
která způsobí, že test selže.
Můžeš si představit, že `assert a == b` dělá následující:

```python
if not (a == b):
    raise AssertionError('Test selhal!')
```

> [note]
> Zatím `assert` nepoužívej jinde než v testovacích funkcích.
> V „normálním” kódu má `assert` vlastnosti,
> do kterých teď nebudeme zabředávat.


## Spouštění testů

Testy se spouští zadáním příkazu
`python -m pytest -v` následovaným názvem souboru s testy.
Tedy v překladu: <strong>Python</strong>e, pusť
<strong>m</strong>odul <strong>pytest</strong>,
v „ukecaném” režimu (angl. <strong>v</strong>erbose) nad zadaným souborem.

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
jejichž jméno začíná na `test_`, a ověří, že nevyvolají žádnou
výjimku – typicky výjimku z příkazu `assert`.
Pokud výjimka nastane, dá to `pytest` velice červeně
najevo a přidá několik informací, které můžou
usnadnit nalezení a opravu chyby.

> [note]
> Argument s názvem souboru můžeme vynechat: `python -m pytest -v`
> V takovém případě `pytest` projde aktuální adresář a spustí testy
> ze všech souborů, jejichž jméno začíná na `test_`. Místo souboru
> lze též uvést adresář a `pytest` vyhledá testy v něm.

Zkus si změnit funkci `secti` (nebo její test) a podívat se,
jak to vypadá když test „neprojde“.


## Testovací moduly

Testy se většinou nepíšou přímo ke kódu,
ale do souboru vedle.
Je to tak přehlednější a taky to pak zjednodušuje
distribuci – předávání kódu někomu, kdo ho chce
jen spustit a testy nepotřebuje.

Rozděl soubor s testem sečítání: funkci `secti` přesuň do modulu `secteni.py`,
a v `test_secteni.py` nech jenom test.
Do `test_secteni.py` pak na začátek přidej `from secteni import secti`,
aby byla funkce testu k dispozici.

Test by měl opět projít.


## Spouštěcí moduly

Automatické testy musí projít „bez dozoru“.
V praxi se často automaticky spouští, případné chyby se automaticky
oznamují (např. e-mailem) a fungující kód se automaticky
začne používat dál (nebo se rovnou vydá zákazníkům).

Co to znamená pro nás?
Funkce `input` v testech nefunguje. Nemá koho by se zeptala; „za klávesnicí“
nemusí nikdo sedět.

To může někdy „ztěžovat práci“. Ukážeme si to na naší konzolové kalkulačce.

Kód pro kalkulačku si uložíme jako `kalkulacka.py` a může rámcově vypadat zhruba takto:

```python
# pokud potřebuji importovat jiné moduly, importují se vždy na začátku

def secti(prvni_cislo, druhe_cislo):
    """Vrátí součet dvou čísel."""
    ...

def odecti(prvni_cislo, druhe_cislo):
    """Vrátí rozdíl prvního a druhého čísla."""
    ...

def vynasob(prvni_cislo, druhe_cislo):
    """Vrátí součin dvou čísel."""
    ...

def vydel(prvni_cislo, druhe_cislo):
    """Vrátí podíl prvního a druhého čísla."""
    ...

def nacti_operand():
    """Načte od uživatele operand."""
    ...
    operand = input("Zadej operaci, + - * /")
    ...

def nacti_cislo(vyzva_uzivateli):
    """Zobrazí výzvu uživateli, načte od něj vstup a ten vrátí jako celé číslo."""
    ...
    cislo = input(vyzva_uzivateli)
    ...

def kalkulacka():
    """Spustí kalkulačku

    Od uživatele načte čísla, požadovanou operaci a vypíše výsledek."""
    ...
    prvni_cislo = nacti_cislo("Zadej první číslo")
    druhe_cislo = nacti_cislo("Zadej druhé číslo")
    operand = nacti_operand()
    ...

# Puštění kalkulačky!
kalkulacka()
```

Když tenhle modul naimportuješ, Python v něm postupně, odshora dolů,
provede všechny příkazy.

Definice funkcí (příkazy `def` a všechno v nich) jen definují funkce.
Ale zavoláním funkce `kalkulacka` se spustí hra:
funkce `kalkulacka` zavolá funkce `nacti_cislo()`  a `nacti_operand`, které zavolají `input()`.

Importuješ-li tenhle modul z testů, `input` selže a import se nepovede.

> [note]
> A kdybys modul importoval{{a}} odjinud – například bys chtěl{{a}} funkci
> `secti` použít v nějakém jiném programu – uživatel si bude muset v rámci importu
> nechat něco vypočítat!

Volání funkce `kalkulacka` je __vedlejší efekt__, a je potřeba ho odstranit.
No jo, ale po takovém odstranění
už nejde jednoduše spustit hra! Co s tím?

Můžeš na to vytvořit nový modul.
Pojmenuj ho `vypocet.py` a dej do něj jenom to odstraněné volání:

```python
import kalkulacka

kalkulacka.kalkulacka()
```

Tenhle modul nebudeš moci testovat (protože nepřímo volá funkci `input`),
ale můžeš ho spustit, když si budeš chtít nechat něco spočítat.
Protože k němu ale nemáš napsané testy, nepoznáš
z nich, když se takový spouštěcí modul rozbije.
Měl by být proto nejjednodušší – jeden import a jedno volání.

Původní modul teď můžeš importovat bez obav – ať už z testů nebo z jiných
modulů.
Test může vypadat třeba takhle:

```python
import kalkulacka

def test_secti():
    assert secti(1, 2) == 3
    assert secti(-1, -2) == -3
    assert secti(-1, 1) == 0
```

Asi těžko otestujeme všechny možné součty, proto je potřeba zvolit vhodná testovací data. U takových dat bychom si měli být jisti výsledkem (např. jsme si jisti, že 1 + 2 je opravdu 3) a zároveň by měly pokrýt i podmínky, kdy je větší pravděpodobnost, že se něco "rozbije" (např. sčítání záporných čísel).

## Pozitivní a negativní testy

Testům, které kontrolují že se program za správných podmínek chová správně,
se říká *pozitivní testy*.
Můžeš ale testovat i reakci programu na špatné nebo neočekávané podmínky.

Testy, které kontrolují reakci na „špatný“ vstup,
se jmenují *negativní testy*.
Můžou kontrolovat nějaký negativní výsledek (např.
že volání jako <code>secti(1, 2)</code> vrátí `4`),
a nebo to, že nastane „rozumná“ výjimka.

Například funkce `vydel` by měla způsobit
chybu (třeba `ZeroDivisionError`), když se pokusím dělit nulou.

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

import kalkulacka

def test_vydel():
    with pytest.raises(ZeroDivisionError):
        kalkulacka.vydel(1, 0)
```

