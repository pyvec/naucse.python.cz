# Dekorátory

V této lekci se nebudeme věnovat žádné externí knihovně. Místo toho se seznámíme
s jednou vlastností Pythonu, kterou knihovny často využívají, a která obvykle
vypadá trochu magicky.

Touto vlastností jsou *dekorátory*.

*Dekorátory* se hodí tehdy, když potřebujeme upravit chování nějaké funkce, ale
nechceme ji přímo upravovat.

## Teorie do začátku

Co je to vlastně dekorátor? Dekorátor je vlastně jenom funkce, která dostane
jeden argument a vrátí jednu hodnotu. Je ale trochu speciální v tom, že jak
argument, tak návratová hodnota jsou zase jiné funkce.

> [note]
> Funkcím, které operují nad jinými funkcemi, říkáme *funkce vyššího řádu*.

Použití dekorátorů v kódu vypadá zhruba takto:

```python
@dekorator
def funkce():
    pass
```

Tento zápis se zavináčem je jenom *syntaktický cukr*. Usnadňuje nám zápis, ale
chová se přesně stejně jako následující kód, na kterém je lépe vidět, že
`dekorator` je funkce:


```python
def funkce():
    pass
funkce = dekorator(funkce)
```

Na řádku za zavináčem může být libovolný výraz, který po vyhodnocení vrátí
funkci, která má požadované rozhraní.


## Přiklad 0 – registrace funkcí

Jak už při programování bývá zvykem, náš první dekorátor nás pozdraví.

Začneme s jednoduchým programem, který definuje funkci pro pozdrav a zavolá ji.

```python
def ahoj():
    print("Ahoj")


if __name__ == "__main__":
    ahoj()
```

Do tohoto programu bychom rádi přidali další pozdravy, a zavolali je všechny.

```python
def ahoj():
    print("Ahoj")


def nazdar():
    print("Nazdar")


if __name__ == "__main__":
    ahoj()
    nazdar()
```

Tento přístup ale povede k tomu, že by na konci byl dlouhý seznam pozdravů.
Můžeme si funkce rovnou uložit do seznamu a potom přes něj jenom iterovat.

```python
def ahoj():
    print("Ahoj")


def nazdar():
    print("Nazdar")


if __name__ == "__main__":
    funkce = [ahoj, nazdar]
    for f in funkce:
        f()
```

A jako poslední krok přidáme dekorátor, který nám bude funkce rovnou přidávat
do seznamu.

```python
funkce = []


def pridej_pozdrav(func):
    funkce.append(func)
    return func


@pridej_pozdrav
def ahoj():
    print("Ahoj")


@pridej_pozdrav
def nazdar():
    print("Nazdar")


if __name__ == "__main__":
    for f in funkce:
        f()
```

Zkuste přidat ještě jeden pozdrav.

> [note]
> V tomto příkladu jde o docela zbytečné použití dekorátorů. Ukazuje ale
> praktický způsob, jak řešit registraci funkcí. Stejné řešení používá
> například knihovna `flask` pro definování webových služeb nebo `click` pro
> vytváření příkazů pro terminál.


## Příklad 1 – trasování volání funkcí

Podívejme se třeba na tuto na pohled nevinnou funkci. Počítá, jak vypadá *n*-té
číslo ve Fibonacciho posloupnosti. Funguje docela pěkně, pokud jí nezadáme jako
argument příliš velké číslo. Na autorově počítači příliš velká čísla začínají
kolem 35.

```python
def fib(x):
    """Spočítá x-té číslo ve Fibonacciho posloupnosti."""
    if x <= 1:
        return x
    return fib(x - 1) + fib(x - 2)
```

Napíšeme si jednoduchý dekorátor, který nám bude vypisovat informace o tom, co
se ve funkci děje.

```python
def co_se_deje(func):
    print("Aplikuju dekorátor")
    return func


@co_se_deje
def fib(x):
    """Spočítá x-té číslo ve Fibonacciho posloupnosti."""
    if x <= 1:
        return x
    return fib(x - 1) + fib(x - 2)

if __name__ == "__main__":
    print(fib(4))
```

Tento dekorátor funkci nijak nemění. Akorát nám oznámí, že byl aplikovaný. V
těle dekorátoru ale můžeme nadefinovat novou funkci a vrátit ji.

Zkusme si to:

```python
def co_se_deje(func):
    def nahradni_funkce(x):
        return "Spočítej si to sám!"

    return nahradni_funkce
```

Nebo můžeme vrátit funkci, která akorát zavolá tu původní.

```python
def co_se_deje(func):
    def nahradni_funkce(x):
        return func(x)

    return nahradni_funkce
```

Pojďme vracenou funkci rozšířit tak, aby vypisovala informace o tom, co dělá.

```python
def co_se_deje(func):
    def nahradni_funkce(x):
        print(f"Voláme {func.__name__}({x})")
        return func(x)

    return nahradni_funkce
```

Úkol: upravte dekorátor tak, aby vypisoval i vypočítanou hodnotu.

{% filter solution %}
```python
def co_se_deje(func):
    def nahradni_funkce(x):
        print(f"Voláme {func.__name__}({x})")
        vysledek = func(x)
        print(f"Výsledek {func.__name__}({x}) = {vysledek}")
        return vysledek

    return nahradni_funkce
```
{% endfilter %}

> [note]
> Tento dekorátor není úplně praktický. Pokud toho vypíše trochu víc, tak už se
> v tom logu nikdo nevyzná. Myšlenka jako taková ovšem není úplně špatná. Kdyby
> třeba dekorátor počítal, kolikrát se funkce spustí, a jak dlouho obvykle
> trvá, mohl by nám pomoct najít místa pro optimalizaci.


### Nápověda pro funkce

Zkuste si v interaktivní konzoli Pythonu spustit následující příklad:

```pycon
>>> help(print)
Help on built-in function print in module builtins:

print(...)
    print(value, ..., sep=' ', end='\n', file=sys.stdout, flush=False)

    Prints the values to a stream, or to sys.stdout by default.
    Optional keyword arguments:
    file:  a file-like object (stream); defaults to the current sys.stdout.
    sep:   string inserted between values, default a space.
    end:   string appended after the last value, default a newline.
    flush: whether to forcibly flush the stream.
```

Dostaneme krátkou nápovědu o tom, jak používat funkci `print`.

Odkud se tato nápověda bere? Z dokumentačního komentáře. Takže bychom měli
dostat pěknou nápovědu třeba i pro naši známou funkci `fib`.

```pycon
>>> from fib import fib
>>> help(fib)
Help on function nahradni_funkce in module fib:

nahradni_funkce(x)

>>>
```

Něco je špatně. Protože jsme původní implementaci funkce `fib` pomocí
dekorátoru nahradili naší pomocnou funkcí, komentář se cestou ztratil. Mohli
bychom přidat dokumentační komentář k náhradní funkci, ale přece nebudeme
stejný kód kopírovat dvakrát.

Standardní knihovna má naštěstí možnost, jak to snadno opravit. V modulu
`functools` je definovaný dekorátor `wraps`, který umí zkopírovat dokumentační
komentář a jméno z jedné funkce do druhé.

```python
import functools


def co_se_deje(func):
    @functools.wraps(func)
    def nahradni_funkce(x):
        pass
```

```pycon
>>> from fib import fib
>>> help(fib)
Help on function fib in module fib:

fib(x)
    Spočítá x-té číslo ve Fibonacciho posloupnosti.

>>>
```

### Předávání všech argumentů.

Při psaní dekorátorů je dobré myslet na to, jak moc univerzální by měly být.
Například náš `co_se_deje` momentálně funguje pouze pro funkce, které mají
jeden argument.

To je ale docela hloupé omezení. Stejně dobře bychom mohli chtít sledovat
volání jiné funkce, která má třeba argumentů víc.

Pokud dekorátor nepotřebuje vědět nic o argumentech funkce, je docela praktické
jej nadefinovat tak, aby byly prostě všechny předal dál, ať už jich je kolik
chce.

To můžeme udělat následovně:

```python
def co_se_deje(func):
    @functools.wraps(func)
    def nahradni_funkce(*args, **kwargs):
        print(f"Voláme {func.__name__}{args}")
        vysledek = func(*args, **kwargs)
        print(f"Výsledek {func.__name__}{args} = {vysledek}")
        return vysledek
    return nahradni_funkce
```

Do n-tice `args` posbíráme všechny poziční argumenty, do slovníku `kwargs`
všechny pojmenované argumenty. A při volání dekorované funkce je všechny zase
předáme dál.

Ve výstupu teď používáme pouze poziční argumenty. Přidání těch pojmenovaných je
cvičení pro čtenáře.


## Příklad 2 – opakování HTTP požadavků

Pokud náš program musí pracovat s nějakou externí službou nebo systémem, může
se stát, že komunikace mezi nimi nebude vždy bezproblémová. Pěkný příklad je
třeba stahování webové stránky se špatným připojením. S tím z Pythonu nic
udělat nemůžeme.

Můžeme ale zkusit požadavek zopakovat, pokud poznáme, že je to typ chyby, kde
opakování může pomoct.

Začneme s jednoduchým programem, který udělá HTTP požadavek.

> [note]
> Následující příklady používají knihovnu *requests*. Nainstalujte si ji, pokud ji
> ve virtuálním prostředí ještě nemáte.

```python
import requests

def stahni():
    """Stáhne stránku a něco s ní udělá."""
    print("Stahuju stránku")
    odpoved = requests.get("https://httpbin.org/status/200,400,500")
    print(f"Dostali jsme {odpoved.status_code}")
    odpoved.raise_for_status()
    return "OK"


if __name__ == "__main__":
    stahni()
```

Použitá stránka náhodně odpoví jedním z vyjmenovaných kódu, takže ve dvou
třetinách případů bychom měli dostat chybu. Pokud požadavek zkusíme zopakovat,
máme dobrou šanci, že to projde.

Začneme s jednoduchým dekorátorem, který jenom zavolá funkci.

```python
def opakuj_pri_neuspechu(func):
    """Pokud volání funkce vyhodí výjimku, budeme ji ignorovat a zkusíme funkci
    zavolat znovu.
    """
    @functools.wraps(func)
    def nahradni_funkce(*args, **kwargs):
        return func(*args, **kwargs)

    return nahradni_funkce


@opakuj_pri_neuspechu
def stahni():
    """Stáhne stránku a něco s ní udělá."""
    print("Stahuju stránku")
    odpoved = requests.get("https://httpbin.org/status/200,400,500")
    print(f"Dostali jsme {odpoved.status_code}")
    odpoved.raise_for_status()
    return "OK"
```

Co by měla dělat naše náhradní funkce? Donekonečna bude zkoušet zavolat
dekorovanou funkci. Pokud se to podaří, vrátí její výsledek. Pokud dostaneme
výjimku `requests.exceptions.HTTPError`, chvilku počkáme, a půjdeme na další
pokus.

```python
import functools
import time

import requests


def opakuj_pri_neuspechu(func):
    """Pokud volání funkce vyhodí výjimku, budeme ji ignorovat a zkusíme funkci
    zavolat znovu.
    """

    @functools.wraps(func)
    def nahradni_funkce(*args, **kwargs):
        while True:
            try:
                return func(*args, **kwargs)
            except requests.exceptions.HTTPError:
                print("Chyba, zkusíme to znovu")
                time.sleep(1)

    return nahradni_funkce


@opakuj_pri_neuspechu
def stahni():
    """Stáhne stránku a něco s ní udělá."""
    print("Stahuju stránku")
    odpoved = requests.get("https://httpbin.org/status/200,400,500")
    print(f"Dostali jsme {odpoved.status_code}")
    odpoved.raise_for_status()
    return "OK"
```

Teď by program měl vypisovat, že se snaží stránku stáhnout několikrát, a
opakovat to tak dlouho, dokud se to nepodaří.

Co když ale potřebujeme opakování pokusů na více místech, ale chceme reagovat
na jiné výjimky?

Mohli bychom si nadefinovat nový dekorátor pro každý typ výjimky, kterou
chceme chytat. To zní jako hodně práce a duplicitního kódu.

Místo toho můžeme dekorátor upravit tak, aby přijímal argumenty, a pak mu
s jejich pomocí řekneme, kterou výjimku ošetřovat.

Výraz za `@` musí při vyhodnocení vždy vracet funkci, která se chová jako
dekorátor. Takže musíme přidat jednu vrstvu do našich vnořených funkcí.

Funkce `opakuj_pri_neuspechu` je vlastně továrna na dekorátory. Vždy, když ji
zavoláme, vrátí nám funkci, která se chová podle našich potřeb a funguje jako
dekorátor.

```python
import functools
import time

import requests


def opakuj_pri_neuspechu(vyjimka):

    def dekorator(func):

        @functools.wraps(func)
        def nahradni_funkce(*args, **kwargs):
            while True:
                try:
                    return func(*args, **kwargs)
                except vyjimka:
                    print("Chyba, zkusíme to znovu")
                    time.sleep(1)

        return nahradni_funkce

    return dekorator


@opakuj_pri_neuspechu(requests.exceptions.HTTPError)
def stahni():
    """Stáhne stránku a něco s ní udělá."""
    print("Stahuju stránku")
    odpoved = requests.get("https://httpbin.org/status/200,400,500")
    print(f"Dostali jsme {odpoved.status_code}")
    odpoved.raise_for_status()
    return "OK"
```
