# Výjimky

O [chybových výpisech]({{ lesson_url('beginners/print') }}) už v tomto
kurzu byla zmínka: Python si postěžuje, řekne, kde je chyba, a ukončí program.
O chybách se toho ale dá říct mnohem víc.


## Výpisy chyb

Na začátku si ukážeme (nebo zopakujeme), jak Python vypíše chybu, která
nastane v zanořené funkci:

```python
def vnejsi_funkce():
    return vnitrni_funkce(0)

def vnitrni_funkce(delitel):
    return 1 / delitel

print(vnejsi_funkce())
```

<!-- XXX: Highlight the line numbers -->

```pycon
Traceback (most recent call last):          
  File "/tmp/ukazka.py", line 7, in <module>
    print(vnejsi_funkce())
  File "/tmp/ukazka.py", line 2, in vnejsi_funkce
    return vnitrni_funkce(0)
  File "/tmp/ukazka.py", line 5, in vnitrni_funkce
    return 1 / delitel
ZeroDivisionError: division by zero
```

Všimni si, že každá funkce, jejíž volání vedlo k chybě, je uvedena ve výpisu.
Skutečná chyba (tedy místo, které musíme opravit)
je pravděpodobně poblíž některého z těchto volání.
V našem případě bychom asi neměl{{gnd('i', 'y', both='i')}} volat
`vnitrni_funkce` s argumentem `0`.
A nebo by `vnitrni_funkce` měla být na nulu
připravená a dělat v tomto případě něco jiného.

Python nemůže vědět, na kterém místě by se chyba měla opravit, a tak ukáže vše.
Ve složitějších programech se to bude hodit.


## Vyvolání chyby

Chybu neboli *výjimku* (angl. *exception*) můžeš vyvolat i {{gnd('sám', 'sama')}},
pomocí příkazu `raise`.
Za příkaz dáš jméno výjimky a pak do závorek nějaký popis toho, co je špatně.

```python
VELIKOST_POLE = 20

def over_cislo(cislo):
    if 0 <= cislo < VELIKOST_POLE:
        print('OK!')
    else:
        raise ValueError('Čislo {n} není v poli!'.format(n=cislo))
```

Všechny typy výjimek, které jsou zabudované
v Pythonu, jsou popsané [v dokumentaci](https://docs.python.org/3.2/library/exceptions.html#exception-hierarchy).

Pro nás jsou (nebo budou) důležité tyto:

```plain
BaseException
 ├── SystemExit                     vyvolána funkcí exit()
 ├── KeyboardInterrupt              vyvolána po stisknutí Ctrl+C
 ╰── Exception
      ├── ArithmeticError
      │    ╰── ZeroDivisionError    dělení nulou
      ├── AssertionError            nepovedený příkaz `assert`
      ├── AttributeError            neexistující atribut, např. 'abc'.len
      ├── ImportError               nepovedený import
      ├── LookupError
      │    ╰── IndexError           neexistující index, např. 'abc'[999]
      ├── NameError                 použití neexistujícího jména proměnné
      │    ╰── UnboundLocalError    použití proměnné, která ještě nebyla nastavená
      ├── SyntaxError               špatná syntaxe – program je nečitelný/nepoužitelný
      │    ╰── IndentationError     špatné odsazení
      │         ╰── TabError        kombinování mezer a tabulátorů
      ├── TypeError                 špatný typ, např. len(9)
      ╰── ValueError                špatná hodnota, např. int('xyz')
```


## Ošetření chyby

A proč jich je tolik druhů?
Abys je mohl{{a}} chytat!
Následující funkce je připravená na to, že
funkce `int` může selhat, pokud uživatel nezadá číslo:

```python
def nacti_cislo():
    odpoved = input('Zadej číslo: ')
    try:
        cislo = int(odpoved)
    except ValueError:
        print('To nebylo číslo! Pokračuji s nulou.')
        cislo = 0
    return cislo
```

Jak to funguje?
Příkazy v bloku uvozeném příkazem `try` se normálně provádějí, ale když
nastane uvedená výjimka, Python místo ukončení programu provede
všechno v bloku `except`.
Když výjimka nenastane, blok `except` se přeskočí.

Když odchytáváš obecnou výjimku,
chytnou se i všechny podřízené typy výjimek –
například `except ArithmeticError:` zachytí i `ZeroDivisionError`.
A `except Exception:` zachytí všechny
výjimky, které běžně chceš zachytit.


## Nechytej je všechny!

Většinu chyb ale není potřeba ošetřovat.

Nastane-li nečekaná situace, je téměř vždy
*mnohem* lepší program ukončit, než se snažit
pokračovat dál počítat se špatnými hodnotami.
Navíc chybový výstup, který Python standardně
připraví, může hodně ulehčit hledání chyby.

„Ošetřování” chyb jako `KeyboardInterrupt`
je ještě horší: může způsobit, že program nepůjde
ukončit, když bude potřeba.

Příkaz `try/except` proto používej
jen v situacích, kdy výjimku očekáváš – víš přesně, která chyba může
nastat a proč, a máš možnost ji opravit.
Pro nás to typicky bude načítání vstupu od uživatele.
Po špatném pokusu o zadání je dobré se ptát znovu, dokud uživatel nezadá
něco smysluplného:

```python
def nacti_cislo():
    while True:
        odpoved = input('Zadej číslo: ')
        try:
            return int(odpoved)
        except ValueError:
            print('To nebylo číslo! Zkus to znovu.')
```


## Další přílohy k `try`

Kromě `except` existují dva jiné bloky,
které můžeš „přilepit“ k `try`, a to `else` a `finally`.
První se provede, když v `try` bloku
žádná chyba nenastane; druhý se provede vždy – ať
už chyba nastala nebo ne.

Můžeš taky použít více bloků `except`. Provede se vždy maximálně jeden:
ten první, který danou chybu umí ošetřit.

```python
try:
    neco_udelej()
except ValueError:
    print('Tohle se provede, pokud nastane ValueError')
except NameError:
    print('Tohle se provede, pokud nastane NameError')
except Exception:
    print('Tohle se provede, pokud nastane jiná chyba')
    # (kromě SystemExit a KeyboardInterrupt, ty chytat nechceme)
except TypeError:
    print('Tohle se neprovede nikdy')
    # ("except Exception" výše ošetřuje i TypeError; sem se Python nedostane)
else:
    print('Tohle se provede, pokud chyba nenastane')
finally:
    print('Tohle se provede vždycky; i pokud v `try` bloku byl např. `return`')
```


## Úkol

Doplň do geometrické kalkulačky (nebo 1-D piškvorek, máš-li je) ošetření chyby,
která nastane když uživatel nezadá číslo.

{% filter solution %}

Možné řešení pro geometrickou kalkulačku:

```python

while True:
    try:
        strana = float(input('Zadej stranu čtverce v centimetrech: '))
    except ValueError:
        print('To nebylo číslo!')
    else:
        if strana <= 0:
            print('To nedává smysl!')
        else:
            break

print('Obvod čtverce se stranou', strana, 'je', 4 * strana, 'cm')
print('Obsah čtverce se stranou', strana, 'je', strana * strana, 'cm2')

```

Možné řešení pro 1-D piškvorky:

```python
def tah_hrace(pole):
    while True:
        try:
            pozice = int(input('Kam chceš hrát? (0..19) '))
        except ValueError:
            print('To není číslo!')
        else:
            if pozice < 0 or pozice >= len(pole):
                print('Nemůžeš hrát venku z pole!')
            elif pole[pozice] != '-':
                print('Tam není volno!')
            else:
                break

    pole = pole[:pozice] + 'o' + pole[pozice + 1:]
    return pole


print(tah_hrace('-x----'))
```
{% endfilter %}
