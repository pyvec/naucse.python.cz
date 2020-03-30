# Testování

Programátorská práce nespočívá jen v tom, program napsat.
Důležité je si i ověřit, že opravdu funguje, a případně ho pak opravit.
Tomu ověřování že program funguje se říká *testování* (angl. *testing*).

Zatím jsi asi svoje programy testoval{{a}} tak, že jsi
je zkusil{{a}} spustit, něco zadal{{a}} a podíval{{a}} se,
jestli jsou výsledky v pořádku.
U větších programů, které budou mít více a více
možností, ale bude těžší a těžší takhle zkontrolovat,
jestli všechny ty možnosti fungují jak mají.

Proto programátoři často nezkouší programy „ručně“.
Píšou jiné programy, které jejich výtvory testují za ně.

*Automatické testy* jsou funkce, které
zkontrolují že program funguje správně.
Spuštěním testů můžeš kdykoli ověřit, že kód funguje.
Když v otestovaném kódu v budoucnu uděláš nějakou změnu,
testy ověří, že jsi nerozbil{{a}} nic co dříve fungovalo.


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
Ujisti se, že máš virtuální prostředí aktivované – na začátku příkazové řádky
máš `(venv)`.

Potom zadej následující příkaz.
(Je to příkaz příkazové řádky, podobně jako
`cd` nebo `mkdir`; nezadávej ho do Pythonu.)

> [warning] Opisuj opatrně!
> Příkaz níže instaluje software z internetu.
> Nahrát takovou knihovnu na internet může kdokoli – hodný nebo zlý,
> chytrý nebo hloupý.
> Za knihovnu `pytest` autoři tohoto kurzu ručí.
> Jiné knihovny ale můžou dělat neplechu nebo být dokonce „zavirované“;
> už při instalaci můžou něco pokazit.
> Dej si proto pozor a ve jménu `pytest` neudělej překlep!
>
> Nainstaluješ-li přesto omylem něco cos nechtěl{{a}}, dej co nejdřív vědět
> zkušenějšímu programátorovi, aby zkontroloval jaký to mohlo mít efekt.

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
dvě čísla, a další funkce, která testuje jestli se
`secti` pro určité hodnoty chová správně.

Kód si opiš do souboru `test_secteni.py` v novém prázdném adresáři.
Jméno je důležité: `pytest` ve výchozím nastavení předpokládá,
že jména jak souborů s testy tak samotných testovacích funkcí začínají na
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
na Kámen-Nůžky-Papír.

Kód pro Kámen-Nůžky-Papír může, velice zjednodušeně, vypadat zhruba takto:

```python
import random  # (příp. import jiných věci, které budou potřeba)

tah_pocitace = 'kámen'
tah_hrace = input('Kam chceš hrát?')

if tah_hrace == 'papír':
    print('Vyhrál{{a}} jsi!')
else:
    print('Nevyhrál{{a}} jsi...')

```

Když tenhle modul naimportuješ, Python v něm postupně, odshora dolů,
provede všechny příkazy.

První příkaz, `import`, jen zpřístupní nějaké proměnné a funkce;
je-li importovaný modul správně napsaný, nemá vedlejší účinek.
Definice funkcí (příkazy `def` a všechno v nich) podobně jen definují funkce.
Ale zavoláním funkce `input` se spustí interakce: program potřebuje vstup
od uživatele.

Importuješ-li tenhle modul z testů, `input` selže a import se nepovede.

> [note]
> A kdybys modul importoval{{a}} odjinud – například bys chtěl{{a}} tuhle
> funkčnost použít v nějaké jiné hře – uživatel si bude muset v rámci importu
> zahrát Kámen-Nůžky-Papír!

Volání funkce `input` je vedlejší efekt.
Je potřeba ho odstranit.
Importovatelné moduly by měly pouze dát k dispozici nějaké funkce nebo hodnoty.
Dej tedy hru do funkce:

```python
# knp.py -- importovatelný modul

import random  # (příp. import jiných věci, které budou potřeba)

def hrej_hru():
    tah_pocitace = 'kámen'
    tah_hrace = input('Kam chceš hrát?')

    # (tady reálně bude spousta zanořených ifů)
    if tah_hrace == 'papír':
        print('Vyhrál{{a}} jsi!')
    else:
        print('Nevyhrál{{a}} jsi...')

```

No jo, ale po takovém odstranění
už nejde jednoduše spustit hra! Co s tím?

Můžeš na to vytvořit nový modul, ve kterém bude jenom volání funkce:

```python
# hra.py -- spouštěcí modul

import knp

knp.hrej_hru()
```

Tenhle modul nebudeš moci testovat (protože nepřímo volá funkci `input`),
ale můžeš ho spustit, když si budeš chtít zahrát.
Protože k němu nemáš napsané testy, nepoznáš
z nich, když se takový spouštěcí modul rozbije.
Spouštěcí modul by proto měl být co nejjednodušší – jeden import a jedno volání.

Původní modul teď můžeš importovat bez obav – ať už z testů nebo z jiných
modulů.
Pořád se ale, kvůli funkcím `input` a `print`, špatně testuje.
Aby se testoval líp, můžeš kousek funkčnosti dát do jiné funkce:

```python
# knp.py -- importovatelný modul

import random  # (příp. import jiných věci, které budou potřeba)

def vyhodnot(tah_pocitace, tah_hrace):
    # (tady reálně bude spousta zanořených ifů)
    if tah_hrace == 'papír':
        return 'Vyhrál{{a}} jsi!'
    else:
        return 'Nevyhrál{{a}} jsi...'


def hrej_hru():
    tah_pocitace = 'kámen'
    tah_hrace = input('Kam chceš hrát?')

    vysledek = vyhodnot(tah_pocitace, tah_hrace)
    print(vysledek)
```

A vida! Funkce `vyhodnot` teď neobsahuje ani `print` ani `input`.
Půjde tedy docela jednoduše otestovat:

```python
# test_knp.py -- testy

import knp

def test_vyhry():
    assert vyhodnot('kámen', 'papír') == 'Vyhrál{{a}} jsi!'
    assert vyhodnot('papír', 'nůžky') == 'Vyhrál{{a}} jsi!'
    assert vyhodnot('nůžky', 'kámen') == 'Vyhrál{{a}} jsi!'
```

Funkce `hrej_hru` ovšem tak dobře otestovat nejde.
Musíš ji testovat ručně.
Protože ale hlavní část programu (`vyhodnot`) jde pokrýt automatickými testy,
ruční testování nemusí být tak důkladné.


## Pozitivní a negativní testy

Test `test_vyhry`, ukázaný výše, není úplný.
Splnila by ho i funkce jako:

```python
def vyhodnot(tah_pocitace, tah_hrace):
    return 'Vyhrál{{a}} jsi!'
```

Kromě „pozitivních“ výsledků je potřeba kontrolovat i ty „negativní“:
ať už očekávaný negativní výsledek (jako prohru nebo remízu)
nebo reakci programu na špatné nebo neočekávané podmínky.

Co třeba má dělat volání `vyhodnot(8, 'kukačka')`?

Testy, které kontrolují reakci na „špatný“ vstup,
se jmenují *negativní testy*.
Často kontrolují to, že nastane „rozumná“ výjimka.

Na otestování výjimky použij příkaz `with` a funkci `raises` naimportovanou
z modulu `pytest`.
Jak příkaz `with` přesně funguje, to se dozvíme později;
teď stačí říct, že ověří, že odsazený blok kódu
pod ním vyvolá danou výjimku:

```python
def test_spatneho_tahu():
    """🤘 vs. 🖖 není správný vstup"""
    with pytest.assert_raises(ValueError):
        vyhodnot('metal', 'spock')
```
