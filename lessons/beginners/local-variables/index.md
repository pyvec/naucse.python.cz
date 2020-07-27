# Lokální proměnné

Už umíš definovat vlastní funkce.
Zbývá ale ještě dovysvětlit, jak v nich fungují proměnné.

Funkce může používat proměnné „zvnějšku“.
Následující program přiřadí do proměnné `pi` a všechny další funkce
mají k `pi` přístup:

```python
pi = 3.1415926

def obsah_kruhu(polomer):
    return pi * polomer ** 2

print(obsah_kruhu(100))
```

Jinak je tomu ale v případě, kdy proměnnou nastavíš *uvnitř* funkce.

Všechny parametry a všechny proměnné, do kterých funkce přiřazuje,
jsou *úplně nové* proměnné, které nemají nic
společného s tím, co je „venku“ kolem funkce.

Těmto proměnným se říká *lokální proměnné* (angl. *local variables*),
protože existují jen místně, v rámci volání jedné jediné funkce.

Proměnné, které nejsou lokální, jsou *globální* – ty existují v celém programu.

Pro příklad:

```python
def nastav_x(hodnota):
    x = hodnota  # Přiřazení do lokální proměnné!

nastav_x(40)
print('x =', x)
```

Program skončí s chybou!
Funkce `nastav_x` si hraje na vlastním písečku; proměnná `x` je jen
pro ni.
Když funkce `nastav_x` skončí, proměnná `x` přestane existovat.


## Skrývání detailů

Podobně skončí s chybou i složitější program:

```python
def zamen(slovo, pozice, novy_znak):
    """V daném slově zamění znak na dané pozici za daný nový znak"""
    zacatek = slovo[:pozice]
    konec = slovo[pozice + 1:]
    nove_slovo = zacatek + novy_znak + konec
    return nove_slovo

print(zamen('kočka', 1, 'a'))
print(zamen('kačka', 2, 'p'))

print(zacatek)  # NameError
```

Funkce `zamen` jsi napsal{{a}} proto, abys nemusel{{a}} pořád opakovat detaily
záměny písmenka.
Jakmile je jednu nadefinovaná, stačí ji zavolat. Důležité jsou jen jméno
funkce, parametry a návratová hodnota; na detaily kódu uvnitř můžeš zapomenout.
A to i díky lokálním proměnným, které detaily ve vnitřku funkce trochu líp
izolují od zbytku programu.

Ještě lépe je to vidět u funkcí, které jsi nenapsal{{a}} {{gnd('sám', 'sama')}}.
Jak divné by bylo, kdyby po každém zavolání `print` byla najednou nastavená
proměnná `i`, kterou `print` náhodou používá při procházení svých parametrů!


## Přiřazení

To, co dělá lokální proměnnou, je *přiřazení*.
Porovnej `nastav_x` s příkladem na `obsah_kruhu` výše: rozdíl mezi `pi` a `x`
je v tom, že do `x` se v rámci funkce přiřazuje.

Co je to přiřazení? Všechno, co *nastavuje* nějakou proměnnou. Například:
* Klasika je přiřazovat pomocí `=`, např. `a = 3`.
* Parametry funkce: funkce `def nastav_x(hodnota)` přiřadí do `hodnota`,
* Cyklus `for x in ...:` přiřazuje do proměnné `x`.
* Pro úplnost, příkazy `def x(...):`, `import x` a `from ... import x` taky
  přiřazují do `x` – ale ve funkcích se moc nepoužívají.

> [note] A další
> K těmto materiálům se možná budeš vracet, tak pro úplnost přidám další
> způsoby, které postupně poznáš. Není jich mnoho:
> * Příkazy `with ... as x`, `del x`, `except ... as x` přiřazují do `x`.
> * Přiřazují i speciální přiřazovací operátory jako `+=`, `*=`, `:=`.


## Zakrývání jména

Jak to funguje, když ve funkci přiřadíš do proměnné, která existuje i globálně?
Pak tu máme problém.

Vytvoří se *úplně nová* lokální proměnná, která má stejné jméno jako
ta globální.
Jméno označuje lokální proměnnou, a ta globální pak „není vidět“.

Tento příklad tedy nebude fungovat tak, jak se zdá:

```python
x = 0

def nastav_x(hodnota):
    x = hodnota  # Přiřazení do lokální proměnné!
    print('Ve funkci nastav_x: x =', x)

nastav_x(40)
print('Venku: x =', x)
```

V tomto programu existují *dvě* proměnné jménem `x`.
Jedna je globální. Jedna je lokální pro funkci `nastav_x`.
Jmenují se stejně, ale jsou to dvě různé proměnné.


## Lokální nebo globální?

Pojďme si to ukázat.
Než spustíš tenhle program, zkus předpovědět co bude dělat.
Pak ho pusť, a pokud dělal něco jiného, zkus vysvětlit proč.
Pozor na chytáky!

```python
from math import pi
obsah = 0
a = 30

def obsah_elipsy(a, b):
    obsah = pi * a * b  # Přiřazení do `obsah`
    a = a + 3  # Přiřazení do `a`
    return obsah

print(obsah_elipsy(a, 20))
print(obsah)
print(a)
```

Zkus odpovědět na tyto otázky:

* Je proměnná `pi` lokální, nebo globální?
* Je proměnná `obsah` lokální, nebo globální?
* Je proměnná `a` lokální, nebo globální?
* Je proměnná `b` lokální, nebo globální?
* Je proměnná `obsah_elipsy` lokální, nebo globální?

{% filter solution %}
* `pi` je globální – nepřiřazuje se do ní ve funkci;
  je „vidět“ v celém programu.
* Proměnné `obsah` jsou v programu dvě – jedna globální,
  a jedna je lokální pro funkci `obsah_elipsy`,
  protože do ní tahle funkce přiřazuje.
* Proměnné `a` jsou taky dvě, podobně jako `obsah`.
  Tady byl chyták: příkaz `a = a + 3` nemá žádný smysl;
  do `a` se sice uloží větší číslo, ale vzápětí funkce `obsah_elipsy` skončí
  a její lokální proměnná `a` přestane existovat.
* Proměnná `b` je jenom lokální – jako parametr funkce `obsah_elipsy`.
* Proměnná `obsah_elipsy` je globální (a je v ní funkce).

> [note] A pro úplnost
>
> * Klíčová slova `from`, `import`, `def`, `return` neoznačují proměnné.
> * Jméno modulu `math` taky neoznačuje proměnnou.
> * Proměnná `print` se dá považovat za globální.
>   (Ve skutečnosti existuje zvláštní kategorie *zabudovaných* (angl. *builtin*)
>   proměnných – ty jsou „ještě globálnější“.)

{% endfilter %}


## Rada na závěr

Pravidla pro lokální proměnné jsou pro začátečníky jednou z nejzvláštnějších
věcí v Pythonu.
Jsou ale přínosná – umožňují některé užitečné techniky, např. rekurzi.

Jestli ti to celé připadá složité, dá se tomu zatím vyhnout dodržováním jednoho
pravidla:
*nepřiřazuj ve funkcích do proměnných, které existují i vně funkce.*
(Parametr funkce se počítá jako přiřazení.)
