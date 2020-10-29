# Mypy

Dnes se společně podíváme na knihovnu `mypy`, která nám do Pythonu přidá
možnost kontroly typů, jenž je jinak dostupná jen v jiných programovacích
jazycích.

## Statická a dynamická typová kontrola

Statická typová kontrola v programovacím jazyce počítá s tím, že pro každou
proměnnou či parametr je uveden datový typ. Proměnná definovaná s konkrétním
typem pak nemůže obsahovat hodnotu jiného datového typu a pokus o to vyvolá
výjimku. Jako např. tento kód v Javě:

```java
String name = "John";
name = 5;
```

První řádek definuje proměnnou `name` jako řetězec. Na druhém řádku se
pokoušíme do této proměnné přiřadit celé číslo, což není povoleno
a kompilace takového kódu skončí chybou.

Naproti tomu Python je typickým představitelem jazyků s dynamickou typovou
kontrolou. Program jako je ten následující bude fungovat naprosto
bez problémů:

```python
name = "John"
name = 5
name = ["John", "Peter", "Alice"]
```

Python obecně spoléhá na to, že si sám tvůrce dá pozor, aby proměnná
obsahovala v tom správném čase ten správný obsah a v případě nesrovnalostí
se s tím program za běhu nějak popasuje.

Oba přístupy mají své výhody a nevýhody. Statická typová kontrola by možná
pro začátečníky ubrala na čitelnosti kódu, zbytečně prodloužila krátké
jednoúčelové programy a nejspíše by ani nenadchla vědce či matematiky, kteří
v Pythonu tvoří většinu času prototypy a svůj kód zpravidla automaticky netestují.
Na druhou stranu může přispět k lepší čitelnosti složitějšího kódu,
editory a IDE mohou díky ní lépe napovídat programátorům a typová kontrola
může odhalit chyby ještě před spuštěním aplikace či jejich testů.

Pokud výhody statické typové kontroly znějí slibně, je tady pro vás `mypy`.

## Instalace a spuštění

`mypy` se instaluje standardním způsobem:

```console
$ python -m pip install mypy
```

A spouští se pak stejnojmenným příkazem:

```console
$ mypy program.py 
Success: no issues found in 1 source file
```

První spuštění nejspíše nezahlásí žádný problém, protože program neobsahuje
informace o typech proměnných a tak nemá `mypy` co kontrolovat.

```python
def hello(name):
    return "Hello {}!".format(name)

print(hello("World"))
```

Pokud budeme chtít do budoucna zařídit, aby `mypy` nepřeskakovala funkce bez
definovaných typů, dá se to zařídit přepínačem `--disallow-untyped-defs`.

```console
$ mypy --disallow-untyped-defs program.py 
program.py:1: error: Function is missing a type annotation
Found 1 error in 1 file (checked 1 source file)
```

> [note]
> Jakmile aplikace používá definice typů, je dobré je kontrolovat
> v rámci testů. Např. pro pytest existuje doplněk [`pytest-mypy`], který
> se o to postará.

[`pytest-mypy`]: https://pypi.org/project/pytest-mypy/

## Definice typů a jejich kontrola

Python sám o sobě sice statickou typovou kontrolu neobsahuje, ale od verze 3
je pro ni v jazyce připravena podpora. Náš moderní program
s definovanými typy bude vypadat následovně:

```python
def hello(name: str) -> str:
    return "Hello {}!".format(name)

print(hello("World"))
```

Úpravou jsme definovali, že funkce `hello` bere jako první a jediný argument
řetězec a vrací taktéž řetězec.

Tato úprava nemá na běh programu vůbec žádný vliv, protože Python samotný
definice typů ignoruje.

```console
$ python program.py                      
Hello World!
```

`mypy` nám ovšem potvrdí, že je vše v pořádku.

```console
$ mypy --disallow-untyped-defs program.py
Success: no issues found in 1 source file
```

Co když se teď naši vylepšenou funkci pokusíme zavolat znovu s nesprávným
typem argumentu?

```python
def hello(name: str) -> str:
    return "Hello {}!".format(name)

print(hello("World"))
print(hello(5))
```

```console
$ python program.py                      
Hello World!
Hello 5!
```

Funguje to, protože řetězcová metoda `.format()` si poradí i s argumenty
jiných typů. Ovšem, co na to `mypy` a typová kontrola?

```console
$ mypy --disallow-untyped-defs program.py
program.py:5: error: Argument 1 to "hello" has incompatible type "int"; expected "str"
Found 1 error in 1 file (checked 1 source file)
```

Té se to právem nelíbí, protože v definici jsme si stanovili, že funkce má
brát jako argument řetězec a místo toho jí na posledním řádku voláme
s celočíselným argumentem.


### Vlastní datové typy

V Pythonu často používáme vlastní třídy a jejich instance si všemi možnými
způsoby předáváme do/z funkcí. I s tím si umí mypy poradit.

```python
class Animal:
    def __init__(self, name: str):
        self.name = name


class Person:
    def __init__(self, name: str):
        self.name = name


def hello(pet: Animal) -> None:
    print('Hi, I am {}, your pet.'.format(pet.name))


rooster = Animal("Kokrhac")
guest = Person("Tichoslapek")

hello(rooster)
hello(guest)
```

Když se program pokusíme spustit, bude bez problémů fungovat:
```console
$ python program.py
Hi, I am Kokrhac, your pet.
Hi, I am Tichoslapek, your pet.
```

`mypy` nás ovšem upozorní, že funkci `hello` v druhém případě nepoužíváme správně:

```console
$ mypy program.py
program.py:19: error: Argument 1 to "hello" has incompatible type "Person"; expected "Animal"
Found 1 error in 1 file (checked 1 source file)
```


### Alternativní způsoby definice

Jak už bylo zmíněno, Python samotný definice typů ignoruje. I přes to ale
bylo potřeba na ně jazyk připravit, aby dvojtečka za parametrem a šipka za
definicí funkce nezpůsobily syntaktické chyby. Tyto možnosti však nejsou
v Pythonu 2, kde je nutné dávat definice typů do komentářů:

```python
def hello(name):  # type: (str) -> str
    return "Hello {}!".format(name)

print hello("World")
print hello(5)
```

A říci `mypy`, že kontroluje kód pro starší verzi Pythonu:

```console
$ mypy --py2 program.py                  
program.py:5: error: Argument 1 to "hello" has incompatible type "int"; expected "str"
Found 1 error in 1 file (checked 1 source file)
```

Poslední možností definice typů je využití tzv. „stub“ souborů. Takový soubor
má příponu `.pyi`, stejné jméno jako modul, ke kterému patří, a obsahuje
jen definice funkcí s definovanými typy. Například takto:

```python
def hello(name: str) -> str: pass
```

To se hodí především pro knihovny, kde je možné definice typů na jednu stranu
úplně ignorovat a na stranu druhou tyto definice snadno přidat, aniž bychom
museli měnit zdrojový kód samotný. Je tímto způsobem samozřejmě i možné přidat
definice typů ke kódu, který jinak nemáte právo upravovat.

Definice sama o sobě je validní Python kód a funguje ve stejné formě
pro Python 2 i 3.

## Složitější definice a modul `typing`

Změníme naši jednoduchou funkci tak, aby uměla přímo pozdravit a to hned
několikrát.

```python
def say_hello(names):
    for name in names:
        print("Hello {}!".format(name))

say_hello(["PyLadies", "Ostrava"])
```

```console
$ python say_hello.py 
Hello PyLadies!
Hello Ostrava!
```

Program funguje dobře. Přidejme tedy definice typů — seznam pro jména
na vstupu a protože funkce nic nevrací, tak `None` jako automatická návratová
hodnota.

Označit argument funkce za seznam můžeme pomocí `List` z modulu `typing`.
Modul `typing` obsahuje takových pomocných objektů celou řadu a my se některé
z nich postupně podíváme.


```python
from typing import List

def say_hello(names: List) -> None:
    for name in names:
        print("Hello {}!".format(name))

say_hello(["PyLadies", "Ostrava"])
```

```console
$ python say_hello.py
Hello PyLadies!
Hello Ostrava!

$ mypy say_hello.py  
Success: no issues found in 1 source file
```

Na fungování programu nemá změna žádný vliv a `mypy` je zdá se také spokojená.
Máme hotovo? Svým způsobem ano, ale naše funkce je přeci jen univerzálnější
než dokládá definice typu vstupního argumentu a bude fungovat bez problémů
i s n-ticí nebo slovníkem:

```python
say_hello(["PyLadies", "Ostrava"])
say_hello(("Tom", "Peter"))
say_hello({"Susan": 32, "Carol": 25})
```

Co s tím? U složitějších definic si musíme vzít na pomoc modul `typing`.
Ten je u Pythonu 3.5 a novějších dostupný ve standardní knihovně a pro starší
verze se dá standardním způsobem nainstalovat. Z něj si pak můžeme importovat
jednotlivé části, které nám pomohou s přesnější definicí typů.

```python
from typing import List, Tuple, Dict, Union, Any

def say_hello(names: Union[List[str], Tuple[str, ...], Dict[str, Any]]) -> None:
    for name in names:
        print("Hello {}!".format(name))

say_hello(["PyLadies", "Ostrava"])
say_hello(("Tom", "Peter"))
say_hello({"Susan": 32, "Carol": 25})
```

Definice se nám celkem nepříjemně rozrostla, ale i na to najdeme řešení.
V aktuální podobě specifikuje následující pravidla:
* `Union` — vyber si libovolnou definici z těch následujících
v hranatých závorkách
* `List[str]` — seznam řetězců
* `Tuple[str, ...]` — n-tice s jedním či více řetězci
* `Dict[str, Any]` — slovník s řetězcovými klíči a libovolnými hodnotami

> [note]
> U n-tic se počítá s tím, že hodnota na každé z pozic má nějaký specifický
> účel (např. n-tice se třemi souřadnicemi by měla
> `Tuple[float, float, float]`) a proto vypadá definice pro n-tici
> s libovolnou délkou jinak než pro seznam.

Takové konkrétní definice jsou zdlouhavé a proto modul `typing` obsahuje mnoho
užitečných zkratek. V našem případě by se dala definice zobecnit na libovolný
iterovatelný objekt obsahující řetězce.

```python
from typing import Iterable

def say_hello(names: Iterable[str]) -> None:
    for name in names:
        print("Hello {}!".format(name))

say_hello(["PyLadies", "Ostrava"])
say_hello(("Tom", "Peter"))
say_hello({"Susan": 32, "Carol": 25})
```

> [note]
> Importovat zvláštní `List`, `Dict` nebo `Tuple` jen pro potřeby typových
> anotací se nezdá být úplně praktické. Proto vznikl [PEP 585], který pro složitější
> struktury v typových anotacích umožní použít názvy tříd dostupné přímo v Pythonu.
> Toto je již implementováno v Pythonu od verze 3.9.0, ale mypy tento zápis ještě nepodporuje.
> Brzy si tedy i u složitějších anotací (např.: `argument: dict[str, list[int]]`) vystačíme
> bez importů z modulu `typing`

[PEP 585]: https://www.python.org/dev/peps/pep-0585/

U funkcí s argumenty s výchozí hodnotou se definice typů píše mezi jméno
argumentu a rovnítko.

```python
def pow(base: int, exp: int = None) -> int:
    if exp:
        return base ** exp
    else:
        return base ** 2

print(pow(5, 3))
print(pow(5))
```

Funkce `pow` ukazuje ještě jeden speciální případ. Často se stává, že funkce
jako argument může brát nějakou hodnotu daného typu nebo `None`. V takovém
případě by psaní `Union[str, None]` bylo příliš zdlouhavé a modul `typing`
proto obsahuje `Optional`. `Optional[str]` a `Union[str, None]` jsou naprosto identické definice.

V příkladu výše je navíc zápis `exp: int = None` díky výchozí hodnotě
argumentu exp nastavené na `None` konvertován na `Optional[int]` automaticky.

`mypy` umí samozřejmě kontrolovat nejen konstanty, ale i návratové hodnoty
funkcí předané jako argument jiné funkci.

```python
def pow(base: int, exp: int = None) -> int:
    if exp:
        return base ** exp
    else:
        return base ** 2

def hello(name: str) -> str:
    return "Hello {}!".format(name)

result = pow(5, 3)
print(hello(result))
```

```console
$ mypy program.py
program.py:11: error: Argument 1 to "hello" has incompatible type "int"; expected "str"
Found 1 error in 1 file (checked 1 source file)
```

## Globální proměnné

Ne vždy si `mypy` dokáže odvodit datové typy např. pro globální proměnné.

```python
global_dict = {}
```

```console
$ mypy global.py
global.py:1: error: Need type annotation for 'global_dict' (hint: "global_dict: Dict[<type>, <type>] = ...")
Found 1 error in 1 file (checked 1 source file)
```

V takovém případě se dá datový typ definovat velmi podobně jako u funkcí:

```python
from typing import Dict

global_dict: Dict[str, float] = {}
```

## A mnohem více

Tohle by na úvod mohlo stačit. O `mypy` se toho dá samozřejmě nejvíce dočíst
v [dokumentaci](https://mypy.readthedocs.io/en/stable/index.html)
a totéž platí pro modul `typing` a [dokumentaci standardní knihovny](https://docs.python.org/3/library/typing.html).
