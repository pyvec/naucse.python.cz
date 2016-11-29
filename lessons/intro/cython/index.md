C API
=====

Mluvíme-li o „Pythonu“, máme často na mysli jak jazyk samotný, tak i interpret,
program, který programy v tomto jazyce umí spouštět.
Správně je ale „Python“ pouze jméno jazyka.
Interpretů tohoto jazyka je více, například:

* CPython, referenční implementace napsaná v C; interpret, který spouštíme příkazem `python3`
* PyPy, implementace zaměřená na rychlost, napsaná v Pythonu
* MicroPython, implementace pro mikroprocesory a zařízení s minimem paměťi
* Jython, implementace napsaná v Javě, která umožňuje využívat Javovské třídy
* IronPython, napsaný v C#, s integrací do .NET
* Batavia, Brython, pyjs – různé pokusy o integraci do Javascriptu

Jednotlivé interprety se liší v detailech jako jsou přesnost reálných čísel,
vypisování chybových hlášek, řazení záznamů ve slovnících nebo přístup
k interním strukturám interpretu.
Správně napsaný Pythoní program by neměl na takových detailech záviset, pokud
není k nekompatibilitě mezi interprety dobrý důvod.

Někdy to ale je potřeba, a dnešní přednáška specifická pro CPython,
a přímé využití jeho API pro jazyk C.


Rychlost
--------

Častý důvod proč sáhnout k C API je rychlost: CPython je celkem pomalý,
a tradiční metoda optimalizace je zjistit, které části jsou kritické, a přepsat
je do C.
Využijí se tak výhody obou jazyků: Python pro rychlý vývoj, snadné
prototypování, a přehlednost kódu, a C pro rychlost.

Jiná možnost, jak program zrychlit, je ho pustit tak jak je pod interpretem
PyPy, který obsahuje optimalizovaný překladač. To je ale jiná kapitola.

Když je náš program příliš pomalý, je potřeba ho optimalizovat.
První krok k tomu je vždy zkontrolovat, co zabírá více času, než by mělo.
K tomu se dá použít nástroj `profile` ze standardní knihovny, který vypíše
tabulku počtu volání jednotlivých funkcí a času v nich stráveného:

    python -m profile -s cumtime program.py

Profilovat běh pytest testů se dá jednoduše pomocí modulu [pytest-profiling]:

    python -m pytest --profile

[pytest-profiling]: https://pypi.python.org/pypi/pytest-profiling

Když máme představu o tom, co nás brzdí, můžeme začít přepisovat do C způsoby
popsanými níže.


Externí knihovny
----------------

Druhý důvod proč programátoři používají C API je použití knihoven, které mají
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
jako [gdb] nebo [Valgrind] a prozkoumat potíže na nižší úrovni.

Případné chyby v CPythonu pak se znalostmi C API jdou i
[pomoci opravit][devguide]. tenhle kus není hotový?

[gdb]: https://en.wikipedia.org/wiki/GNU_Debugger]
[valgrind]: http://valgrind.org/
[devguide]: https://docs.python.org/devguide/


Modul v C
---------

Pojďme začít příkladem.
Vytvořte si následující soubory, který implementuje rozšíření
(importovatelný modul) s jednou funkcí.

(Nebudeme chtít, abyste podobný kód uměli napsat, ale měli byste být schopní
porozumět tomu, co dělá)

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
na datové typy C, volá samotnou funkci, a výsledek převádí zpět na Pythoní
objekt.

Dále máme pole záznamů o funkcích (`DemoMethods`), kde je ke každé funkci
přiřazeno jméno, dokumentační řetězec, a způsob volání (v našem případě
METH_VARARGS, tedy volání s proměnným počtem nepojmenovaných argumentů,
podobně jako bychom v Pythonu napsali  `def system(*args)`).

Další potřebná proměnná, `demo_module`, obsahuje  informace o modulu:
jméno, dokumnetační řetězec, a seznam funkcí.
Kdybychom potřebovali kromě funkcí definovat i třídy nebo konstanty,
zde bychom pomocí [slotů][PyModuleDef_Slot] definovali funkci, která modul
inicializuje, t.j. má podobnou funkci jako `__init__` u třídy v Pythonu.

[PyModuleDef_Slot]: https://docs.python.org/3/c-api/module.html#c.PyModuleDef_Slot

Poslední část je funkce `PyInit`, jediná která není definována jako `static`,
takže jediná, která je exportována jako API knihovny, kterou vytváříme.
Až bute Python tento modul importovat, najde tuto funkci podle jména, spustí ji,
a podle vrácené struktury typu `PyModuleDef` vytvoří Pythoní objekt s modulem.


Překlad
-------

Abychom mohli takovýto modul naimportovat, musíme ho nejdřív přeložit a sestavit
z něj sdílenou knihovnu – soubor .so (nebo .dll) – s názvem modulu:
buď jen `demo.so`, nebo i s identifikací architektury a verze Pythonu,
např. `demo.cpython-35m-x86_64-linux-gnu.so`.
(Výhoda delších názvů je v tom, že v jednom adresáři může být víc modulů pro
různé archirektury, a že se Python nebude snažit načíst nekompatibilní moduly.)

Překlad je nutné provést se správnými přepínači a volbami, nejlépe takovými,
s jakými byl sestaven samotný Python.

Pro zjednodušení tohoto procesu můžeme použít Setuptools: do nám už známého
souboru setup.py přidáme argument `ext_modules` se seznamem rozšířovacích modulů.
Podrobný popis třídy `Extension` je v [dokumentaci][Extension]; nám bude stačit
jen jméno a seznam zdrojových souborů:

[Extension]: (https://docs.python.org/3/distutils/apiref.html#distutils.core.Extension)

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

Aby uživatelé překladač mít nemuseli, můžeme nainstalovat knihovnu `wheel` (`python -m pip install wheel`), a pak příkazem `python setup.py bdist_wheel` vygenerovat tzv. *wheel* archiv,
např. `dist/demo-0.1-cp35-cp35m-linux_x86_64.whl`. Tento archiv jde nahrát na PyPI a následně
nainstalovat, ovšem jen na architektuře a verzi Pythonu, pro které byl vytvořen.

Wheels jdou vytvářet i pro moduly tvořené jen Pythoním kódem.
Nejsou pak vázané na verzi a architekturu.
Jejich výhoda oproti `sdist` archivům spočívá v tom, že se rychleji instalují.

Alternativa k instalaci, alespoň pro lokální vývoj, je rozšíření jen přeložit a dát do
aktuálního adresáře (nebo jakéhokoli jiného adresáře, odkud se importují moduly).
K tomu slouží příkaz `python setup.py build_ext --inplace`.
Pozor na to, že po každé změně zdrojového kódu je potřeba rozříření znovu přeložit.

Příkaz `python setup.py develop` bude fungovat jako dřív (používá `build_ext --inplace`),
jen je opět potřeba příkaz po každé změně znovu spustit.


PyObject
--------

Podívejme se teď na základní mechanismy interpretu CPython.

Základní datová struktura, která reprezentuje jakýkoli objekt Pythonu, je PyObject
([dokumentace](https://docs.python.org/3/c-api/structures.html#c.PyObject), 
[definice](https://github.com/python/cpython/blob/3.5/Include/object.h#L106)).
Skládá se ze dvou prvků:

    typedef struct _object {
        Py_ssize_t ob_refcnt;
        struct _typeobject *ob_type;

     } PyObject;


První je počet referencí (*reference count*), který se dá popsat jako počet míst,
ze kterých je možné k tomuto objektu přistoupit.
Když objekt uložíme do proměnné nebo do seznamu, zvýší se počet referencí o 1.
Když seznam nebo proměnná zanikne (nebo náš objekt přepíšeme jiným),
počet referencí se zase sníží.
Když počet referencí dosáhne nuly, znamená to, že se k objektu už nedá dostat, a Python ho
uvolní z paměti.

Druhý prvek struktury PyObject je ukazatel na typ.
Typ je Pythoní objekt (`class`), který definuje chování třídy objektů: operátory,
atributy a metody, které ten který objekt má.

Struktura PyObject slouží jako hlavička, za kterou pak následují data interpretovaná podle
typu daného objektu.
Například Pythoní [objekt typu `float`][float] vypadá následovně:
    
    typedef struct {
        PyObject ob_base;
        double ob_fval;
    } PyFloatObject;

tedy struktura PyObject, za kterou je v paměti číselná hodnota.

[Seznamy][list] obsahují za hlavičkou např. velikost a (ukazatel na) pole ukazatelů na jednotlivé
prvky.
Podobně [objekty typu `int`][int] (které mají v Pythonu neomezený rozsah) mají délku a pole
jednotlivých 30-bitových "číslic".
NumPy matice mají metadata (velikost, typ, druh rozložení v paměti) a ukazatel na pole hodnot.

[float]: https://github.com/python/cpython/blob/3.5/Include/floatobject.h#L15
[list]: https://github.com/python/cpython/blob/3.5/Include/listobject.h#L23
[int]: https://github.com/python/cpython/blob/3.5/Include/longintrepr.h#L89

To základní, co potřebujeme vědět, je že na úrovni C je každý Pythoní objekt reprezentován
jako struktura počtu referencí, ukazatele na typ, a dat specifických pro daný typ.



Reference counting
------------------

Tak jako v C je důležité správně alokovat a dealokovat paměť, při tvorbě rozšíření do CPythonu
je třeba správně pracovat s referencemi: ke kažému [Py_INCREF] (přičtení 1 k počtu referencí)
je potřeba později zavolat [Py_DECREF] (odečtení 1, a případné uvolnění objektu).
Jakákoli práce s objektem se smí provádět jen mezi INCREF a příslušným DECREF.

Platí konvence, že argumenty funkcí se předávají jako tzv. *borrowed reference*: o počitadlo
se stará volající, a v průběhu volané funkce se objekt dá používat.
Pokud bychom ale argument potřebovali i po skončení volané funkce (např. si ho uložíme
do globální proměnné), je potřeba mu počitadlo zvýšit (a po skončení proáce zase snížit).

V našem modulu `demo` přebíráme nako parametr n-tici.
Zodpovědnost zavolat na tuto n-tici Py_DECREF má ale volající, ne my.
Zavoláním funkce PyArg_ParseTuple získáme `char*`, který ale můžeme používat jen v rámci naší
funkce: po jejím skončení může volající argumenty funkce uvolnit, a tím řetězec zrušit.

Funkce, které vracejí Pythoní objekty, předpokládají že volající provede příslušný DECREF.
V modulu `demo` voláme funkci [PyLong_FromLong], která vytvoří nové Pythoní číslo.
Za vzniklou referenci naše funkce přebírá zodpovědnost, je tedy na nás, abychom se postarali
o zavolání Py_DECREF.
Vrácením výsledku tuto zodpovědnost ale předáváme na funkci, která volá tu naši.

[`Py_INCREF`]: https://docs.python.org/3/c-api/refcounting.html#c.Py_INCREF
[`Py_DECREF`]: https://docs.python.org/3/c-api/refcounting.html#c.Py_DECREF
[PyLong_FromLong]: https://docs.python.org/3/c-api/long.html#c.PyLong_FromLong


Hodnoty a výjimky
-----------------

Další konvence, kterou většina funkcí v C API dodržují, je způsob vracení výjimek.

Funkce, které vrací Pythoní objekty, na úrovni C vrací `PyObject*`.
Nastane-li výjimka, objekt výjimky se zaznamená se do globální (přesněji, *thread-local*)
proměnné, a funkce vrátí NULL.

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
Toto vlákno drží globální zámek, který čas od času odemče a znovu se pokusí zamknout,
aby mohly běžet i ostatní vlákna.

Díky GIL je vícevláknové programování v Pythonu relativně bezpečné: nemůže např. nastat souběh
(*race condition*), kdy by se nastavilo počitadlo referencí na špatnou hodnotu.
Na druhou stranu tento zámek ale omezuje paralelismus, a tedy i rychlost programu.

Globální zámek se dá odemčít v situacích, kdy nepracujeme s `PyObject*` a nevoláme Pythoní kód.
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

Cython je jazyk podobný Pythonu, který ale lze přeložit na C, a dále optimalizovat.

Cython si nainstalujte pomocí příkazu:

    python -m pip install cython


Kompilace Pythonu
-----------------

Když chceme převést modul z Pythonu do Cythonu, nejjednodušší začátek je přejmenovat soubor `.py`
na `.pyx`, aby bylo jasné, že jde o jiný jazyk, který nepůjde naimportovat přímo.

Jako příklad můžete použít tuto naivní implementaci celočíselného a maticového násobení:

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

Výsledek můžeme převést na C pomocí příkazu `cython -3 soubor.pyx`, čímž vznikne `soubor.c`, který
můžeme přeložit výše uvedeným způsobem.

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
    install_requires=[
        'Cython',
        'NumPy',
    ],
)
```

Po zadání `python setup.py develop` nebo `python setup_matmul.py build_ext --inplace` atp.
se modul `matmul.pyx` zkompiluje s použitím nainstalovaného NumPy a bude připraven na použití.

Jazyky Python a Cython nejsou 100% kompatibilní, ale zvláště u kódu, který pracuje hlavně s
čísly, se nekompatibilita neprojeví.
Vývojáři Cythonu považují každou odchylku od specifikace jazyka za chybu, kterou je nutno opravit.


Anotace
-------

Kód, který takto vznikne, není o moc rychlejší než původní Python.
Je to tím, že sekvence příkazů ve funkci je sice převedená do C a přeložená do strojového kódu,
ale každá operace pracuje s generickými Pythoními objekty, takže musí pro každé číslo
číslo z matice zkonstruovat Pythoní objekt, vyhledat implementaci sečítání pro dvě celá čísla,
a výsledek převést zpět na `int64` a uložit do matice.

Na situaci se můžeme podívat pomocí přepínače `--annotate`:
    
    cython -3 --annotate matmul.pyx

To vygeneruje soubor `matmul.html`, kde jsou potencionálně pomalé operace vysvíceny žlutě.
Ke každému řádku se navíc dá kliknutím ukázat odpovídající kód v C (který bývá docela složitý,
protože řeší věci jako zpětnou kompatibilitu a ošetřování chyb, a navíc používá hodně pomocných
maker).

Obecně nebývá problém mít "žluté" řádky na úrovni funkce, kde se provádí pouze jednou.
Ale v cyklech, zvláště těch třikrát zanořených, se autor rozšíření typicky snaží žlutým řádkům
vyhnout.
Nejjednoduší způsob, jak toho docílit, je doplnění statických informací o typech.


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

Další věc, kterou můžeme udělat, je změnit příkaz `def` na `cpdef`, a doplnit typ návratové
hodnoty:
    
```python
cpdef int intmul(int a, int b):
    cdef int result
    result = a * b
    return result
```

Tím se zbavíme nákladného převodu výsledku na PyObject.
Bohužel ale toto zrychlení pocíte jen kdycz takovou funkci zavoláme z jiné funkce napsané v
Cythonu.


Používání numpy
---------------

Pro funkci `matmul` můžeme nadefinovat číselné proměnné (`n`, `m`, `p`, `i`, `j`, `k`, `x`, `y`)
jako `int`, ale tím si moc nepomůžeme: většinu času program stráví vybíráním a ukládáním hodnot
z/do matic, a protože Cython nemá informace o tom, že jsou to NumPy matice, používá obecný
protokol pro Pythoní kontejnery, takže se každá hodnota převede na Pythoní objekt.

Je tedy potřeba říct Cythonu, že používáme NumPy matice.
Naštěstí v NumPy existuje integrace s Cythonem, takže můžeme na úrovni C "naimportovat"
rozšíření pro NumPy:

```python
cimport numpy
```

... a potom použít typ "dvourozměrná matice celých čísel", který se v Cythonu jmenuje
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
    

     ctypedef numpy.int64_t DATATYPE


... a pak používat tento alias.
Na maticové typy bohužel typedef zatím nefunguje.


Vypínání kontrol
----------------

XXX


pyximport a %%cython
--------------------

XXX


Úkol
====

Vaším úkolem za 5 bodů je zrychlit pomocí Cythonu úkol z předchozího cvičení tak, aby zvládal řešit i bludiště o rozměrech v řádech XXX × XXX na moderním počítači (srovnatelném s těmi ve školní učebně) v průměrném čase maximálně 1 sekundu. Úkol musí formálně splňovat všechny náležitosti z minulého týdne + podmínku na čas (která platí pro volání funkce `analyze()` i metody `.path()`).

Odevzdávajte s tagem v0.2. Následující příkazy musí po instalaci závislostí z `requirements.txt` fungovat:

```
python setup.py build_ext -i  # sestaví modul napsaný v Cythonu
python -m pytest  # pustí testy
python -c 'from maze import analyze; analyze(...)'  # lze importovat a použitít z Pythonu
```
 

