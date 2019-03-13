Dnes budeme potřebovat do virtuálního prostředí nainstalovat tyto knihovny:

```console
$ python -m pip install --upgrade pip
$ python -m pip install notebook numpy cython pytest pytest-profiling
```

Také je potřeba nainstalovat překladač jazyka C
a hlavičkové soubory Pythonu:

* Na Linuxu bude stačit nainstalovat balíčky `gcc`
  a `python3-devel` (Fedora) nebo `python3-dev` (Ubuntu/Debian).
* Na Windows se řiďte instrukcemi pro vaši verzi Pythonu
  na [Python wiki](https://wiki.python.org/moin/WindowsCompilers).


---

C API
=====

Mluvíme-li o „Pythonu“, máme často na mysli jak jazyk samotný, tak i interpret,
program, který programy v tomto jazyce umí spouštět.
Správně je ale „Python“ pouze jméno jazyka.
Interpretů tohoto jazyka je více, například:

* CPython, referenční implementace napsaná v C; interpret, který spouštíme příkazem `python3`
* PyPy, implementace zaměřená na rychlost, napsaná v Pythonu
* MicroPython, implementace pro mikroprocesory a zařízení s minimem paměti
* Jython, implementace napsaná v Javě, která umožňuje využívat javovské třídy
* IronPython, napsaný v C#, s integrací do .NET
* Batavia, Brython, pyjs – různé pokusy o integraci do JavaScriptu

Jednotlivé interprety se liší v detailech jako jsou přesnost reálných čísel,
vypisování chybových hlášek, řazení záznamů ve slovnících nebo přístup
k interním strukturám interpretu.
Správně napsaný pythonní program by neměl na takových detailech záviset, pokud
není k nekompatibilitě mezi interprety dobrý důvod.

Někdy to ale je potřeba, a dnešní přednáška bude specifická pro CPython
a přímé využití jeho API pro jazyk C.


Rychlost
--------

Častý důvod proč sáhnout k C API je rychlost: CPython je celkem pomalý.
Tradiční metoda optimalizace je zjistit, které části jsou kritické, a přepsat
je do C.
Využijí se tak výhody obou jazyků: Python pro rychlý vývoj, snadné
prototypování a přehlednost kódu, a C pro rychlost.

Když je náš program příliš pomalý, je potřeba ho optimalizovat.
První krok k tomu je vždy zkontrolovat, co zabírá více času, než by mělo.
K tomu se dá použít nástroj `profile` ze standardní knihovny, který vypíše
tabulku počtu volání jednotlivých funkcí a času v nich stráveného:

```console
$ python -m profile -s cumtime program.py
```

Profilovat běh pytest testů se dá jednoduše pomocí modulu [pytest-profiling]:

```console
$ python -m pip install pytest-profiling
$ python -m pytest --profile
```

[pytest-profiling]: https://pypi.python.org/pypi/pytest-profiling

Když máme představu o tom, co nás brzdí, můžeme začít přepisovat do C způsoby
popsanými níže.

Jiná možnost, jak program zrychlit, je ho pustit, tak jak je, pod interpretem
PyPy, který obsahuje optimalizovaný překladač. To je ale jiná kapitola.


Externí knihovny
----------------

Druhý důvod, proč programátoři používají C API, je použití knihoven, které mají
rozhraní pro C.
Takových knihoven existuje mnoho – pokud není něco specifické pro určitý jazyk,
často se to dá volat i z C.

Pro práci s externími knihovnami se dá použít C API nebo vestavěný modul
[ctypes], ale v dnešní době je dobré místo toho použít [CFFI], knihovnu
která funguje i s PyPy (a teoreticky jinými implementacemi). 

[ctypes]: https://docs.python.org/3/library/ctypes.html
[CFFI]: http://cffi.readthedocs.io/en/latest/


CPython
-------

Třetí důvod, proč použít C API, je práce s CPythonem samotným.
Když člověk zabředne do složitého problému, může na CPython pustit C debugger
jako [gdb] nebo [Valgrind], prozkoumat potíže na nižší úrovni
a zjistit, kde přesně se chyba nachází.

[gdb]: https://en.wikipedia.org/wiki/GNU_Debugger
[Valgrind]: http://valgrind.org/


Modul v C
---------

Pojďme začít příkladem.
Vytvořte si následující soubor, který implementuje rozšíření
(importovatelný modul) s jednou funkcí.

(Nebudeme chtít, abyste podobný kód uměli napsat, ale měli byste být schopní
porozumět tomu, co dělá.)

demo.c:

```c
#include <Python.h>

PyDoc_STRVAR(
    mod_docstring, 
    "Demo extension module with a Python wrapper for the system(3) function");

static PyObject *demo_system(PyObject *self, PyObject *args){
    const char *command;
    int retval;

    /* Parse the given arguments: expect one string, convert to char* */
    if (!PyArg_ParseTuple(args, "s", &command)) {
        /* Error handling: if PyArg_ParseTuple returns zero, return NULL */
        return NULL;
    }

    /* Call the C function */
    retval = system(command);

    /* Return result as Python int (error handling built in) */
    return PyLong_FromLong(retval);
}

/* List of all methods in the module */
static PyMethodDef DemoMethods[] = {
    {"system",  demo_system, METH_VARARGS,
            PyDoc_STR("Execute a shell command.")},
    {NULL, NULL, 0, NULL}        /* Sentinel */
};

/* Module specification */
static struct PyModuleDef demo_module = {
   PyModuleDef_HEAD_INIT,
   "demo",          /* name of module */
   mod_docstring,   /* dosctring (may be NULL) */
   0,               /* size of per-interpreter state of the module */
   DemoMethods,     /* list of methods */
};


/* Module entrypoint */
PyMODINIT_FUNC
PyInit_demo(void)
{
    return PyModuleDef_Init(&demo_module);
}
```

Z tohoto souboru by měla být patrná struktura podobných rozšíření:
máme funkci (`demo_system`), která převádí objekty Pythonu
na datové typy C, volá samotnou funkci a výsledek převádí zpět na pythonní
objekt.

Dále máme pole záznamů o funkcích (`DemoMethods`), kde je ke každé funkci
přiřazeno jméno, dokumentační řetězec a způsob volání (v našem případě
METH_VARARGS, tedy volání s proměnným počtem nepojmenovaných argumentů,
podobně jako bychom v Pythonu napsali `def system(*args)`).

Další potřebná proměnná, `demo_module`, obsahuje  informace o modulu:
jméno, dokumentační řetězec a seznam funkcí.
Kdybychom potřebovali kromě funkcí definovat i třídy nebo konstanty,
zde bychom pomocí [slotů][PyModuleDef_Slot] definovali funkci, která modul
inicializuje, t.j. má podobnou funkci jako `__init__` u třídy v Pythonu.

[PyModuleDef_Slot]: https://docs.python.org/3/c-api/module.html#c.PyModuleDef_Slot

Poslední část je funkce `PyInit`, jediná která není definována jako `static`,
takže jediná, která je exportována jako API knihovny, kterou vytváříme.
Až bude Python tento modul importovat, najde tuto funkci podle jména, spustí ji
a podle vrácené struktury typu `PyModuleDef` vytvoří pythonní objekt s modulem.


Překlad
-------

Abychom mohli takovýto modul naimportovat, musíme ho nejdřív přeložit a sestavit
z něj sdílenou knihovnu – soubor .so (nebo .dll) – s názvem modulu:
buď jen `demo.so`, nebo i s identifikací architektury a verze Pythonu,
např. `demo.cpython-35m-x86_64-linux-gnu.so`.
(Výhoda delších názvů je v tom, že v jednom adresáři může být víc modulů pro
různé architektury a že se Python nebude snažit načíst nekompatibilní moduly.)

Překlad je nutné provést se správnými přepínači a volbami, nejlépe takovými,
s jakými byl sestaven samotný Python.

Pro zjednodušení tohoto procesu můžeme použít setuptools: do nám už známého
souboru `setup.py` přidáme argument `ext_modules` se seznamem rozšiřovacích modulů.
Podrobný popis třídy `Extension` je v [dokumentaci][Extension]; nám bude stačit
jen jméno a seznam zdrojových souborů:

[Extension]: https://docs.python.org/3/distutils/apiref.html#distutils.core.Extension

setup.py:

```python
from setuptools import setup, Extension

module1 = Extension(
    'demo',
    sources=['demo.c'],
)

setup(
    name = 'demo',
    version = '0.1',
    description = 'Demo package',
    ext_modules = [module1]
)
```

Příkazy `python setup.py sdist` a `python setup.py install` budou fungovat jako normálně,
jen je na instalaci potřeba překladač jazyka C.

Aby uživatelé překladač mít nemuseli, můžeme nainstalovat knihovnu `wheel` (`python -m pip install wheel`) a pak příkazem `python setup.py bdist_wheel` vygenerovat tzv. *wheel* archiv,
např. `dist/demo-0.1-cp35-cp35m-linux_x86_64.whl`. Tento archiv jde nahrát na PyPI a následně
nainstalovat, ovšem jen na architektuře a verzi Pythonu, pro které byl vytvořen.

Existuje způsob, jak vytvořit co nejvíce platformě nezávislý linuxový wheel.
Jedná se o platformu nazvanou `manulinux1`, což je ve zkratce velmi stará verze
Linuxu (CentOS 5), na které se wheely vytvoří, aby šly použít na různých
novějších i relativně starých distribucích. Pro tvorbu wheelů se používá
[Docker obraz manylinux](https://github.com/pypa/manylinux),
vývojáři samozřejmě nepoužívají pro vývoj CentOS 5 (tedy většina ne).

> [note]
> Zajímavým nástrojem, který stojí za zmínku, je [cibuildwheel].
> Zjednodušuje tvorbu wheelů pro Linux, macOS i Windows pomocí
> CI služeb [Travis CI] a [AppVeyor].

[cibuildwheel]: https://github.com/joerick/cibuildwheel#cibuildwheel
[Travis CI]: https://travis-ci.org/
[AppVeyor]: https://www.appveyor.com/

Wheels jdou vytvářet i pro moduly tvořené jen pythonním kódem.
Nejsou pak vázané na verzi a architekturu.
Jejich výhoda oproti `sdist` archivům spočívá v tom, že se rychleji instalují.

Alternativa k instalaci, alespoň pro lokální vývoj, je rozšíření jen přeložit a dát do
aktuálního adresáře (nebo jakéhokoli jiného adresáře, odkud se importují moduly).
K tomu slouží příkaz `python setup.py build_ext --inplace`.
Pozor na to, že po každé změně zdrojového kódu je potřeba rozšíření znovu přeložit.

Příkaz `python setup.py develop` bude fungovat jako dřív (používá `build_ext --inplace`),
jen je opět potřeba příkaz po každé změně znovu spustit.


PyObject
--------

Podívejme se teď na základní mechanismy interpretu CPython.

Základní datová struktura, která reprezentuje jakýkoli objekt Pythonu, je PyObject
([dokumentace](https://docs.python.org/3/c-api/structures.html#c.PyObject), 
[definice](https://github.com/python/cpython/blob/3.5/Include/object.h#L106)).
Skládá se ze dvou prvků:

```c
typedef struct _object {
    Py_ssize_t ob_refcnt;
    struct _typeobject *ob_type;
} PyObject;
```

První je počet referencí (*reference count*), který se dá popsat jako počet míst,
ze kterých je možné k tomuto objektu přistoupit.
Když objekt uložíme do proměnné nebo do seznamu, zvýší se počet referencí o 1.
Když seznam nebo proměnná zanikne (nebo náš objekt přepíšeme jiným),
počet referencí se zase sníží.
Když počet referencí dosáhne nuly, znamená to, že se k objektu už nedá dostat a Python ho
uvolní z paměti.

Druhý prvek struktury PyObject je ukazatel na typ.
Typ je pythonní objekt (`class`), který definuje chování třídy objektů: operátory,
atributy a metody, které ten objekt má.

Struktura PyObject slouží jako hlavička, za kterou pak následují data interpretovaná podle
typu daného objektu.
Například pythonní [objekt typu float][float] vypadá následovně:

```c
typedef struct {
    PyObject ob_base;
    double ob_fval;
} PyFloatObject;
```

...tedy struktura PyObject, za kterou je v paměti číselná hodnota.

[Seznamy][list] obsahují za hlavičkou např. velikost a (ukazatel na) pole ukazatelů na jednotlivé
prvky.
Podobně [objekty typu int][int] (které mají v Pythonu neomezený rozsah) mají délku a pole
jednotlivých 30bitových „číslic“.
NumPy matice mají metadata (velikost, typ, popis rozložení v paměti) a ukazatel na pole hodnot.

[float]: https://github.com/python/cpython/blob/3.5/Include/floatobject.h#L15
[list]: https://github.com/python/cpython/blob/3.5/Include/listobject.h#L23
[int]: https://github.com/python/cpython/blob/3.5/Include/longintrepr.h#L89

To základní, co potřebujeme vědět, je, že na úrovni C je každý pythonní objekt reprezentován
jako struktura počtu referencí, ukazatele na typ a dat specifických pro daný typ.


Reference counting
------------------

Tak jako v C je důležité správně alokovat a dealokovat paměť, při tvorbě rozšíření do CPythonu
je třeba správně pracovat s referencemi: ke každému [Py_INCREF] (přičtení 1 k počtu referencí)
je potřeba později zavolat [Py_DECREF] (odečtení 1 a případné uvolnění objektu).
Jakákoli práce s objektem se smí provádět jen mezi INCREF a příslušným DECREF.

Platí konvence, že argumenty funkcí se předávají jako tzv. *borrowed reference*: o počitadlo
se stará volající a v průběhu volané funkce se objekt dá používat.
Pokud bychom ale argument potřebovali i po skončení volané funkce (např. si ho uložíme
do globální proměnné), je potřeba mu počitadlo zvýšit (a po skončení práce zase snížit).

V našem modulu `demo` přebíráme jako parametr n-tici.
Zodpovědnost zavolat na tuto n-tici Py_DECREF má ale volající, ne my.
Zavoláním funkce `PyArg_ParseTuple` získáme `char*`, který ale můžeme používat jen v rámci naší
funkce: po jejím skončení může volající argumenty funkce uvolnit, a tím řetězec zrušit.

Funkce, které vracejí pythonní objekty, předpokládají, že na vrácenou hodnotu provede DECREF volající.
V modulu `demo` voláme funkci [PyLong_FromLong], která vytvoří nové pythonní číslo.
Za vzniklou referenci naše funkce přebírá zodpovědnost, je tedy na nás, abychom se postarali
o zavolání Py_DECREF.
Vrácením výsledku tuto zodpovědnost ale předáváme na funkci, která volá tu naši.

[Py_INCREF]: https://docs.python.org/3/c-api/refcounting.html#c.Py_INCREF
[Py_DECREF]: https://docs.python.org/3/c-api/refcounting.html#c.Py_DECREF
[PyLong_FromLong]: https://docs.python.org/3/c-api/long.html#c.PyLong_FromLong


Hodnoty a výjimky
-----------------

Další konvence, kterou většina funkcí v C API dodržuje, je způsob vracení výjimek.

Funkce, které vrací pythonní objekty, na úrovni C vrací `PyObject*`.
Nastane-li výjimka, objekt výjimky se zaznamená do globální (přesněji, *thread-local*)
proměnné a funkce vrátí NULL.

V našem modulu `demo` voláme funkci `PyArg_ParseTuple`, která může vyvolat výjimku: typicky
`TypeError` kvůli nesprávnému počtu nebo typu argumentů.
V takovém případě tato funkce výjimku zaznamená a vrátí NULL.
Naší funkci `system` už stačí vrátit NULL, protože víme, že výjimka už je zaznamenaná.

Další funkce, která může neuspět, je `PyLong_FromLong`.
Vzhledem k tomu, že její výsledek rovnou vracíme, není potřeba úspěch kontrolovat – vrátíme
buď správnou hodnotu nebo NULL se zaznamenanou výjimkou.


GIL
---

Poslední omezení, kterého si autor rozšíření musí být vědom, je *Global Interpreter Lock*.
Stručně řečeno, s objekty `PyObject*` může pracovat pouze jedno vlákno.
Toto vlákno drží globální zámek, který čas od času odemkne a znovu se pokusí zamknout,
aby mohly běžet i ostatní vlákna.

Díky GIL je vícevláknové programování v Pythonu relativně bezpečné: nemůže např. nastat souběh
(*race condition*), kdy by se nastavilo počitadlo referencí na špatnou hodnotu.
Na druhou stranu tento zámek ale omezuje paralelismus, a tedy i rychlost programu.

Globální zámek se dá odemknout v situacích, kdy nepracujeme s `PyObject*` a nevoláme pythonní kód.
Například čtení ze souboru nebo sítě ostatní vlákna neblokuje.
Stejně tak maticové operace v NumPy typicky nedrží GIL zatímco počítají na úrovni C nebo Fortranu.


Cython
======

Teď, když víme jak to všechno funguje, se můžeme podívat na způsob, jak rozšíření psát
jednoduše.
C API se totiž dá použít nejen z C, ale z jakéhokoli jazyka, který umí volat funkce se
stejnými konvencemi, např. C++ (s pomocí `extern C`).
Další způsob, jak použít C API ale nepsat C, je použít překladač z příjemnějšího jazyka do C.

Jeden takový jazyk je Cython (neplést s CPython).

Cython je jazyk podobný Pythonu, který ale lze přeložit na C a dále optimalizovat.

Cython si nainstalujte pomocí příkazu:

```console
$ python -m pip install cython
```


Kompilace Pythonu
-----------------

Když chceme převést modul z Pythonu do Cythonu, nejjednodušší začátek je přejmenovat soubor `.py`
na `.pyx`, aby bylo jasné, že jde o jiný jazyk, který nepůjde naimportovat přímo.


Jazyky Python a Cython nejsou 100% kompatibilní, ale zvláště u kódu, který pracuje hlavně s
čísly, se nekompatibilita neprojeví.
Vývojáři Cythonu považují každou odchylku od specifikace jazyka za chybu, kterou je nutno opravit.

Jako příklad můžete použít tuto naivní implementaci celočíselného a maticového násobení.
Uložte si ji jako `matmul.py`:

```python
import numpy

def intmul(a, b):
    result = a * b
    return result

def matmul(a, b):
    n = a.shape[0]
    m = a.shape[1]
    if b.shape[0] != m:
        raise ValueError('incompatible sizes')
    p = b.shape[1]
    result = numpy.zeros((n, p))
    for i in range(n):
        for j in range(p):
            for k in range(m):
                x = a[i, k]
                y = b[k, j]
                result[i, j] += x * y
    return result
```

Stáhněte si [testy](static/test_matmul.py) a zkontrolujte, že prochází.

Potom soubor přejmenujte na `matmul.pyx`.

Výsledek bychom mohli převést na C pomocí příkazu `cython -3 matmul.pyx`, čímž
vznikne `matmul.c`. Ten můžeme přeložit výše uvedeným způsobem.

Jednodušší varianta je použít Cython v `setup.py`.
Pro naše účely bude `setup.py` s Cythonem a NumPy vypadat takto:

```python
from setuptools import setup
from Cython.Build import cythonize
import numpy

setup(
    name='matmul',
    ext_modules=cythonize('matmul.pyx', language_level=3),
    include_dirs=[numpy.get_include()],
    setup_requires=[
        'Cython',
        'NumPy',
    ],
    install_requires=[
        'NumPy',
    ],
)
```

> [note]
> V případě problémech s nefungujícím `include_dirs` na systému macOS
> použijte komplikovanější variantu:
> ```python
> from distutils.extension import Extension
> ...
> ext_modules = cythonize([Extension('matmul', ['matmul.pyx'],
>                                    include_dirs=[numpy.get_include()])],
>                         language_level=3)
> ```

Po zadání `python setup.py develop` nebo `python setup.py build_ext --inplace` atp.
se modul `matmul.pyx` zkompiluje s použitím nainstalovaného NumPy a bude připraven na použití.
(Zkontrolujte, že testy prochází i se zkompilovaným modulem.)

Nevýhoda tohoto přístupu je, že k spuštění takového `setup.py` je již potřeba
mít nainstalovaný `cython` a `numpy`.
Instalace z archivu `sdist` se tedy nemusí povést – je potřeba uživatelům říct,
že dané moduly už musí mít nainstalované.
Tento problém aktuálně řeší PyPA (správci `pip` a `setuptools`).

Instalace z archivů `wheel` by měla být bezproblémová.


Anotace
-------

Kód, který takto vznikne, není o moc rychlejší než původní Python.
Je to tím, že sekvence příkazů ve funkci je sice převedená do C a přeložená do strojového kódu,
ale každá operace pracuje s generickými pythonními objekty, takže musí pro každé číslo
číslo z matice zkonstruovat pythonní objekt, vyhledat implementaci sčítání pro dvě celá čísla,
a výsledek převést zpět na `int64` a uložit do matice.

Na situaci se můžeme podívat pomocí přepínače `--annotate`:

```console
$ cython -3 --annotate matmul.pyx
```

To vygeneruje soubor `matmul.html`, kde jsou potencionálně pomalé operace vysvíceny žlutě.
Ke každému řádku se navíc dá kliknutím ukázat odpovídající kód v C (který bývá docela složitý,
protože řeší věci jako zpětnou kompatibilitu a ošetřování chyb, a navíc používá hodně pomocných
maker).

Obecně nebývá problém mít „žluté“ ty řádky, které se ve funkci provádí pouze jednou.
Ale v cyklech, zvláště těch třikrát zanořených, se autor rozšíření typicky snaží žlutým řádkům
vyhnout.
Nejjednodušší způsob, jak toho docílit, je doplnění statických informací o typech.


Doplnění typů
-------------

Začneme u funkce `intmul`, kde doplníme informaci o tom, že parametry `a` a `b` a proměnná
`result` jsou typu `int`.
Parametrům stačí doplnit typ podobně jako v C, ostatní lokální proměnné potřebují definici pomocí
příkazu `cdef`:

```python
def intmul(int a, int b):
    cdef int result
    result = a * b
    return result
```

Teď bude funkce nepatrně rychlejší, ale také méně obecná: nejde jí násobit řetězec číslem,
ale ani reálná čísla (`float`), a dokonce ani celá čísla, která se nevejdou do 64 bitů (příp.
jiné velikosti, dle systému).
Typ int v Cythonu je totiž int z C, ne ten neomezený z Pythonu.

Další věc, kterou můžeme udělat, je změnit příkaz `def` na `cpdef` a doplnit typ návratové
hodnoty:
    
```python
cpdef int intmul(int a, int b):
    cdef int result
    result = a * b
    return result
```

Tím se zbavíme nákladného převodu výsledku na PyObject.
Bohužel ale toto zrychlení pocítíme, jen když takovou funkci zavoláme
z jiné funkce napsané v Cythonu.

Tři typy funkcí
---------------

Funkce jdou deklarovat třemi způsoby:

 * `def func(...):` je funkce, která jde volat z Pythonu i z Cythonu, ale volání z Cythonu je pomalé (argumenty a výsledek se převádí na pythonní objekty a zpět),
 * `cdef <type> func(...):` je funkce, která jde volat pouze z Cythonu, ale volání je rychlé (pracuje se s C typy),
 * `cpdef <type> func(...):` je funkce, která se z Cythonu volá rychle, ale jde volat i z Pythonu (ve skutečnosti Cython vytvoří dva druhy této funkce).

Třídy
-----

Cython umožňuje vytvářet tzv. *built-in* třídy: stejný druh tříd jako je
např. `str` nebo `int`.
Práce s takovými třídami je rychlejší, ale mají pevně danou strukturu.
Ani jim ani jejich instancím nelze z Pythonu nastavovat nové atributy:

```python
>>> "foo".bar = 3
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
AttributeError: 'str' object has no attribute 'bar'
```

Příklad definice *built-in* třídy:

```python
cdef class Foo:
    # Všechny členské proměnné musí být nadefinované tady
    cdef int foo
    ...

    def __cinit__(self, int f):
        # Inicializace třídy.
        # Cython zajistí, že se tato funkce zavolá pouze jednou (na rozdíl
        # od __init__, kterou lze z pythonního kódu zavolat kdykoli)
        self.foo = f
        ...

    def __dealloc__(self):
        # Deinicializace třídy
        ...

    cpdef int method(self):
        ...
        return self.foo
```

Více o definici tříd najdete v [dokumentaci Cythonu](http://cython.readthedocs.io/en/latest/src/tutorial/cdef_classes.html).

Používání NumPy
---------------

Pro funkci `matmul` můžeme nadefinovat číselné proměnné (`n`, `m`, `p`, `i`, `j`, `k`, `x`, `y`)
jako `int`, ale tím si moc nepomůžeme: většinu času program stráví vybíráním a ukládáním hodnot
z/do matic, a protože Cython nemá informace o tom, že jsou to NumPy matice, používá obecný
protokol pro pythonní kontejnery, takže se každá hodnota převede na pythonní objekt.

Je tedy potřeba říct Cythonu, že používáme NumPy matice.
Naštěstí v NumPy existuje integrace s Cythonem, takže můžeme na úrovni C „naimportovat“
rozšíření pro NumPy:

```python
cimport numpy
```

... a potom použít typ „dvourozměrná matice celých čísel“, který se v Cythonu jmenuje
`numpy.ndarray[numpy.int64_t, ndim=2]`.
Naše funkce tedy bude začínat takto:

```python
cpdef numpy.ndarray[numpy.int64_t, ndim=2] matmul(
        numpy.ndarray[numpy.int64_t, ndim=2] a,
        numpy.ndarray[numpy.int64_t, ndim=2] b):
    cdef numpy.ndarray[numpy.int64_t, ndim=2] result
    ...
```

Kdybychom si nebyli jistí typem matice, můžeme si ho nadefinovat pomocí `ctypedef`:

```python
ctypedef numpy.int64_t DATATYPE
```

...a pak používat tento alias.
Na maticové typy bohužel typedef zatím nefunguje.

Pro práci s maticí ASCII znaků lze použít typ `numpy.int8_t`, ale je třeba při zapisování přímo na konkrétní pozice zapisovat číselný typ `char`:

```python
cdef numpy.ndarray[numpy.int8_t, ndim=2]  directions = numpy.full((h, w), b'#', dtype=('a', 1))
directions[maze >= 0] = b' '  # Python level, using b' '
directions[1, 2] == ord('x')  # C level, using char
```

> [note]
> Použití `matrix[a, b]` je v Cythonu rychlejší než `matrix[a][b]`, protože se
> uvnitř dějí jiné věci. Při použití `matrix[a, b]` u matice deklarované jako
> dvourozměrné pole nějakého typu Cython přistoupí přímo k obsahu na úrovni
> jazyka C. Při použití `matrix[a][b]` se ale dějí operace dvě, nejprve
> `matrix[a]` vrací jeden řádek matice a až poté `[b]` vrací jeden prvek z
> tohoto řádku. Obě operace probíhají na úrovni Pythonu a proto budou pomalejší
> a při použití `--annotate` bude řádek s takovou operací označen žlutě.


Direktivy
---------

Anotací typů matic se naše demo maticového násobení dostalo skoro na úroveň
C, ale ne úplně: řádky, které pracují s maticemi, jsou ve výstupu `--annotate`
stále trochu žluté.
Cython totiž při každém přístupu k matici kontroluje, jestli nečteme nebo
nezapisujeme mimo pole a případně vyvolá `IndexError`.

Pokud víme – jako v našem případě – že je taková kontrola zbytečná,
můžeme Cythonu říct, aby ji nedělal.
Přístupy mimo pole pak způsobí nedefinované chování (většinou program spadne,
nebo hůř, bude pracovat se špatnými daty).
Kontrola se vypíná direktivou `boundscheck`, která se dá zadat dvěma hlavními
způsoby: dekorátorem:

    @cython.boundscheck(False)
    cpdef funkce():
        ...

... nebo příkazem `with`:

    with cython.boundscheck(False):
        ...

... případně i pro celý soubor, viz [dokumentace][set-directives].

Další zajímavá direktiva je `cython.wraparound(False)`, která podobným způsobem
vypíná pythonní způsob indexování zápornými čísly: místo indexování od konce
s ní dostaneme nedefinované chování.

Seznam dalších direktiv najdete v [dokumentaci][directives].

Cython podporuje ještě blok `with cython.nogil:`, který je podobný direktivám,
ale dá se použít jen s `with`.
V rámci tohoto bloku je odemčený GIL (globální zámek).
Smí se použít, pouze pokud nepracujeme s pythonními objekty – například když
operujeme jen na obsahu už existujících maticí.
Opak je `with cython.gil:`, kterým zámek zase zamkneme – například když
potřebujeme vyhodit výjimku.

[set-directives]: https://cython.readthedocs.io/src/userguide/source_files_and_compilation.html#how-to-set-directives
[directives]: https://cython.readthedocs.io/src/userguide/source_files_and_compilation.html#compiler-directives


Struktury, ukazatele a dynamická alokace
-----------------------------------------

Přestože v Cythonu můžete používat pythonní *n*-tice, slovníky, seznamy a další
podobné nehomogenní typy, jejich použití je pomalé, protože vždy pracují
s pythonními objekty.

Pokud máte kód, který potřebuje dočasné pole takových záznamů,
je pro časově kritické části kódu lepší k problému přistoupit spíše „céčkovsky“,
přes alokaci paměti a ukazatele.

Následující příklad ukazuje, jak naplnit pole heterogenních záznamů:

```python
# Import funkcí pro alokaci paměti – chovají se jako malloc() apod.
from cpython.mem cimport PyMem_Malloc, PyMem_Realloc, PyMem_Free

# Definice struktury
cdef struct coords:
    int row
    int column
    char data

MAXSIZE = ...

def path(...):
    # Definice ukazatele, přetypování
    cdef coords * path = <coords *>PyMem_Malloc(MAXSIZE*sizeof(coords))
    if path == NULL:
        # nedostatek paměti
        raise MemoryError()

    cdef int used = 0
    for ...:
        ...

        #
        path[used] = coords(row, column, data)
        used += 1

    # pole můžeme používat
    ...

    # a musíme ho před vrácením předělat na list
    lpath = []
    cdef int i
    for i in range(used):
        lpath.append(path[i])

    # a uvolnit
    PyMem_Free(path)
    return lpath
```

Pro homogenní pole ale doporučujeme spíše NumPy matice.

Následující příklad ukazuje, jak lze přiřazovat do struktur:

```python
cdef struct coord:
    float x
    float y
    float z

cdef coord a = coord(0.0, 2.0, 1.5)

cdef coord b = coord(x=0.0, y=2.0, z=1.5)

cdef coord c

c.x = 42.0
c.y = 2.0
c.z = 4.0

cdef coord d = {'x':2.0,
                'y':0.0,
                'z':-0.75}
```

Použití knihoven z C
--------------------

Pro použití C knihoven z Pythonu je lepší použít [CFFI].
Ale když už píšete kód v Cythonu
a potřebujete zavolat nějakou C funkci, můžete to udělat takto:

```python
cdef extern from "stdlib.h":
    int rand()
    void srand(long int seedval)

cdef extern from "time.h":
    ctypedef long time_t
    long int time(time_t *)

srand(time(NULL))
print(rand())
```

Deklarace můžete vložit přímo do `.pyx` souboru, ale pokud je chcete používat
z různých míst, pojmenujte soubor `.pxd`, to vám umožní na něj použít `cimport`.

Pro části standardní knihovny jsou takové deklarace již v Cythonu
předpřipravené, můžete tedy použít `cimport` rovnou:

```python
from libc.stdlib cimport rand, srand
from libc.time cimport time

srand(time(NULL))
print(rand())
```


Zkratky: `pyximport` a `%%cython`
---------------------------------

Pro interaktivní práci v Jupyter Notebook má Cython vlastní „magii“.
Na začátku Notebooku můžeme zadat:

```python
%load_ext cython
```

a potom můžeme na začátku kterékoli buňky zadat `%%cython`:

```python
%%cython

cpdef int mul(int a, int b):
    return a * b
```

Kód v takové buňce pak Notebook zkompiluje Cythonem a funkce/proměnné v něm
nadefinované dá k dispozici.

Můžeme použít i `%%cython --annotate`, což vypíše anotace přímo do Notebooku.

Další zkratka je modul `pyximort`, který dává možnost importovat moduly `.pyx`
přímo: hledají se podobně jako `.py` nebo `.so` a před importem se zkompilují.
Zapíná se to následovně:

```python
import pyximport
pyximport.install()

import matmul
```


Video
-----

Před nedávnem měl [Miro] na Středisku unixových technologií nahrávanou ukázku přepsání
úlohy ruksaku z předmětu MI-PAA z Pythonu do Cythonu (včetně nepříjemného záseku a live
ukázky debugování problému).
Na [video] se můžete podívat, mohlo by vám prozradit spoustu tipů, které se vám mohou hodit
ke splnění úlohy.
K obsahu jen dodáme, že místo `malloc` a `free` je lepší použít `PyMem_Malloc` a
`PyMem_Free` z ukázky výše.

[Miro]: https://github.com/hroncok/
[video]: https://www.youtube.com/watch?v=Ksv4RA6yhkY
