# Vlastní funkce

Pamatuješ na funkce `len()`, `print()` nebo `randrange()` z modulu `random`?
Jsou jako kouzelná zaříkadla z knihy vázané v kůži: když víš jak se jmenují
a umíš je správně {# XXX: <s>vyslovit</s> #}napsat, něco pro tebe udělají.

Teď postoupíme na další úroveň: vymyslíme si vlastní zaříkadla!
Jak? Budeme kombinovat příkazy, které už známe.

Třeba funkce, která tě pozdraví, by mohla:

* Vypsat „ahoj!“
* Vypsat „jak se máš?“

Definice funkce v Pythonu začíná klíčovým slovem `def`,
dále je uveden název a následují závorky (zatím prázdné).
Pak je jako po `if` dvojtečka a odsazené příkazy – tentokrát
příkazy, které má funkce provést.
Napiš to do programu:

```python
def pozdrav():
    print('Ahoj!')
    print('Jak se máš?')
```

Tvoje první funkce je připravena!

Když ale tenhle program spustíš, nic neudělá.
To proto, že tohle je jen *definice* funkce.
Python teď ví jak pozdravit – ale neřeklo se, že to má udělat!

Na konec programu přidej volání.
To už *není součást funkce*, ale pokračování samotného programu.
Proto nesmí být odsazené:

```python
def pozdrav():
    print('Ahoj!')
    print('Jak se máš?')

pozdrav()
```

Co se stane, když funkci zavoláš několikrát po sobě?

```python
def pozdrav():
    print('Ahoj!')
    print('Jak se máš?')

pozdrav()
pozdrav()
pozdrav()
```

{% filter solution %}
Každé volání spustí tělo funkce znovu.

``` console
(venv) $ python python_intro.py
Ahoj!
Jak se máš?
Ahoj!
Jak se máš?
Ahoj!
Jak se máš?
```
{% endfilter %}

Co se stane, když volání dáš *nad* definici funkce, místo na konec programu?

```python
pozdrav()

def pozdrav():
    print('Ahoj!')
    print('Jak se máš?')
```

{% filter solution %}
``` pycon
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
NameError: name 'pozdrav' is not defined
```

Python si postěžuje na `NameError` – nezná nic jménem `pozdrav`.

Python totiž program čte odzhora dolů.
Až příkazem `def` se „naučí" jak zdravit.
Předtím, než se k příkazu `def` dostane, funkce neexistuje.
{% endfilter %}

## Parametry

Tvoje funkce se dá volat jen jako `pozdrav()`.
Funkce ale jako `len('slovo')` a `print(1 + 2)` umí navíc pracovat s hodnotou.

Poďme teraz napisať funkciu, ktorá ťa pozdraví menom.
(Uľahčíme si to použitím jazyka, ktorý nepoužíva piaty pád.)

```python
def pozdrav(meno):
    print('Vítam ťa,', meno)

pozdrav('Ola')
pozdrav('Soňa')
pozdrav('Hubert')
pozdrav('Anička')
```

Jak to funguje?
V definici funkce uvedeš závorkách *parametr* – jméno proměnné se kterou bude
funkce pracovat.
Hodnotu pro tenhle parametr pak zadáš při volání funkce.

Zvládneš napsat program, který se zeptá na jméno a pak tě pozdraví?

{% filter solution %}
```python
def pozdrav(meno):
    print('Vitam ťa,', meno)

pozdrav(input('Ako sa voláš? '))
```
{% endfilter %}

Co se stane, když funkci zavoláš bez hodnoty pro parametr?

{% filter solution %}
``` python
def pozdrav(meno):
    print('Vitam ťa,', meno)

pozdrav()
```
``` pycon
Traceback (most recent call last):
  File "<stdin>", line 9, in <module>
TypeError: pozdrav() missing 1 required positional argument: 'meno'
```

Python si stěžuje na `TypeError` – funkce `pozdrav` nedostala povinný
argument `meno`.
{% endfilter %}

Funkce může obsahovat jakýkoli kód.
Třeba podmíněný příkaz, `if`.
Příkazy po `if` je pak potřeba odsatit o *další* čtyři mezery:

```python
def pozdrav(meno):
    print('Vitam ťa,', meno)
    if meno == 'Ola':
        print('Ty umíš programovať!')

pozdrav('Hubert')
pozdrav('Ola')
pozdrav('Soňa')
```


## Vracení

Další věc, kterou funkce jako `len` umí, je *vrátit* výsledek:

``` python
delka = len('Ola')
print(delka)        # napíše: 3
```

Jak na to, kdybys takovou funkci chtěl{{a}} napsat?
V definici funkce můžeš použít příkaz `return`.
Ten funkci okamžitě ukončí a vrátí danou hodnotu:

```python
def dvojnasobek(x):
    return x * 2

print(dvojnasobek(42))
```

Zkus se zamyslet, jak napsat funkci, která vrátí pátý pád nějakého jména. Třeba:

* `paty_pad('Ola')` → 'Olo'
* `paty_pad('Soňa')` → 'Soňo'
* `paty_pad('Hubert')` → 'Huberte'

Tohle je velice složitý úkol, tak si ho trochu zjednodušíme.
Funkce by měla dělat tohle:

* Pokud jméno je „Hubert“:
    * vrátí `Huberte`
* Pokud jméno končí na `a`:
    * vrátí jméno s `o` místo posledního písmenka
* Jinak:
    * Vrátí původní jméno. (Uživatel si toho snad nevšimne.)

``` python
def paty_pad(jmeno):
    if jmeno == 'Hubert':
        return 'Huberte'
    elif jmeno[-1] == 'a':
        return jmeno[:-1] + 'o'
    else:
        return jmeno
```

Dokážeš změnit funkci `pozdrav`, aby zdravila v češtině?
Můžeš na to použít funkci `paty_pad`.

{% filter solution %}
``` python
def paty_pad(jmeno):
    if jmeno == 'Hubert':
        return 'Huberte'
    elif jmeno[-1] == 'a':
        return jmeno[:-1] + 'o'
    else:
        return jmeno

def pozdrav(jmeno):
    print('Vítam tě,', paty_pad(jmeno))

pozdrav('Hubert')
pozdrav('Ola')
pozdrav('Soňa')
```
{% endfilter %}


## Shrnutí

Co bylo nového tentokrát?

* **Funkce** umožňuje pojmenovat nějkolik příkazů, a pak je zavolat najednou.
* **Parametry** funkce, hodnoty se kterými funkce pracuje,
  se zadávají v závorkách.
* `return` ukončí funkci a vrátí hodnotu
