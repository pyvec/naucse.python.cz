## <var>N</var>-tice

Když už známe seznam, podívejme se na jeho sestřičku: takzvanou
<var>n</var>-tici (angl. *tuple*).

<var>N</var>-tice může, podobně jako seznam, obsahovat <var>n</var> prvků. 
<var>N</var>-tice se dvěma prvky je *dvojice*
neboli *pár* (angl. *pair*); se třemi
prvky *trojice* (angl. *3-tuple*),
se čtyřmi *čtveřice* (angl. *4-tuple*), atd.

> [note]
> Pro úplnost: existují i <var>n</var>-tice s jedním prvkem (hmm… „jednice”?)
> a s nula prvky (prázdné <var>n</var>-tice, angl. *empty tuple*),
> ale ty se v praxi tolik nepoužívají.

<var>N</var>-tice se tvoří jako seznamy, jen kolem sebe nemají hranaté závorky.
Stačí čárky mezi prvky:

```python
dvojice = 'Pat', 'Mat'
print(dvojice)
```

Chovají se skoro stejně jako seznamy, jen nejdou měnit.
Nemají tedy metody jako `append` a `pop` a nedá se jim přiřazovat do prvků
(např. `ntice[1] = 2`).
Dají se ale použít v cyklu `for` a dají se z nich číst jednotlivé prvky
(např. `print(ntice[1])`).

```python
osoby = 'máma', 'teta', 'babička'
for osoba in osoby:
    print(osoba)

prvni = osoby[0]
print(f'První je {prvni}')
```

> [note]
> Vypadá to povědomě? Aby ne!
> <var>N</var>-tice jsme už použil{{gnd('i', 'y', both='i')}} dříve:
> `for pozdrav in 'Ahoj', 'Hello', 'Ciao':`
> ve skutečnosti používá <var>n</var>-tici.

Když chceš <var>n</var>-tici předat do funkce,
narazíš na problém, že čárka odděluje jednotlivé
argumenty funkce.
V podobných případech musíš <var>n</var>-tici
uzavřít do závorek, aby bylo jasné, že jde o jednu
hodnotu (byť složenou).

```python
print('osoby:', ('máma', 'teta', 'babička'))
```

```python
seznam_dvojic = []
for i in range(10):
    # `append` bere jen jeden argument; dáme mu jednu dvojici
    seznam_dvojic.append((i, i**2))
print(seznam_dvojic)
```

<var>N</var>-tice se hodí, pokud chceš z funkce vrátit
víc než jednu hodnotu.
Když u příkazu `return` použiješ několik hodnot oddělených čárkou,
vypadá to, že vracíš několik hodnot, ale
ve skutečnosti se vrací jen jedna <var>n</var>-tice.

```python
def podil_a_zbytek(a, b):
    return a // b, a % b
```

> [note]
> Funkce „podíl a zbytek“ je mimochodem k dispozici přímo v Pythonu
> pod jménem `divmod`.

Python umí ještě jeden trik, takzvané „rozbalení“ (angl. *unpacking*).
Když chceš přiřadit do několika proměnných najednou, stačí je na levé
straně rovnítka oddělit čárkou a na pravou stranu
dát nějakou „složenou” hodnotu – třeba právě <var>n</var>-tici.

```python
podil, zbytek = podil_a_zbytek(12, 5)
```

> [note]
> <var>N</var>-tice se k „rozbalování“ hodí nejvíc, protože mají
> daný počet prvků.
> Jde to ale použít se všemi hodnotami, které jdou použít ve `for`:
>
> ```python
> ix, ocko = 'xo'
> jedna, dva, tri = [1, 2, 3]
> ```


## Malé <var>n</var>-tice

Jak vytvořit <var>n</var>-tici s žádným nebo jedním prvkem? Takhle:

```python
prazdna_ntice = ()
jednoprvkova_ntice = ('a', )
```

Druhý příklad jde i bez závorek –
`jednoprvkova_ntice = 'a',` –
ale to vypadá jako zapomenutá čárka.
Když budeš *opravdu* potřebovat jednoprvkovou
<var>n</var>-tici, radši ji pro přehlednost ozávorkuj.


## Kdy použít seznam a kdy <var>n</var>-tici?

Seznamy se používají, když předem nevíš,
kolik v nich přesně bude hodnot,
nebo když je hodnot mnoho.
Například seznam slov ve větě,
seznam účastníků soutěže, seznam tahů ve hře
nebo seznam karet v balíčku.
Oproti tomu `for pozdrav in 'Ahoj', 'Hello', 'Hola', 'Hei', 'SYN':`
používá <var>n</var>-tici.

Když se počet prvků může v průběhu programu měnit, určitě sáhni po seznamu.
Příklad budiž seznam přihlášených uživatelů, nevyřešených požadavků,
karet v ruce nebo položek v inventáři.

<var>N</var>-tice se často používají na hodnoty
různých typů, kdy má každá „pozice”
v <var>n</var>-tici úplně jiný význam.
Například seznam můžeš použít na písmena abecedy,
ale dvojice „podíl a zbytek“ je <var>n</var>-tice.

Prázdné <var>n</var>-tice a <var>n</var>-tice s jedním
prvkem se zapisují trochu divně a má to své důvody:
může-li nastat situace, kdy takovou sekvenci budeš
potřebovat, většinou je lepší sáhnout po seznamu.
Například seznam hracích karet v ruce nebo
seznam lidí aktuálně sledujících video může být občas prázdný.

Seznamy i n-tice mají i technické limity:
<var>n</var>-tice nejdou měnit a až se naučíš pracovat se slovníky,
zjistíš že seznamy tam nepůjdou použít jako klíče.
V takových případech je potřeba použít ten druhý typ sekvence.

Často není úplně jasné, který typ použít.
V takovém případě je to pravděpodobně jedno.
