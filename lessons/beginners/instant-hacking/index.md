## Interaktivní příkazová řádka Pythonu

Zkontroluj si, že máš aktivované virtuální prostředí (na začátku příkazové
řádky ti svítí `(venv)`).

Je-li tomu tak, nezbývá než – konečně – pustit Python.
K tomu použij příkaz `python`:

``` plain
(venv)$ python
Python 3.4.0 (default, Jan 26 2014, 18:15:05)
[GCC 4.8.2 20131212 (Red Hat 4.8.2-7)] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>>
```

Zkus napsat do příkazového řádku příkaz:

```
>>> print("Hello, world!")
```

Když stiskneš Enter, měl by se ti objevit nýsledující výstup:

```
Hello, world!
>>>
```

Pokud jste zvyklí z jiných programovacícj jazyků, že řádka musí být ukončena středníkem, pak v Pythonu to není zapotřebí.

Toto značí příkazový řádek:

```
>>>
```

Pokud do něj napíšeš řetězec v uvozovkách:

```
>>> "Hello world!"
```

dostaneš následující výstup:

```
'Hello world!'
>>>
```

Pokud ale zkusíš napsat podobný příkaz:

```
>>> Have fun!
  File "<stdin>", line 1
    Have fun!
           ^
SyntaxError: invalid syntax
>>>
```

Obdržíš chybové hlášení, že Python interpret nerozumí příkazu.

### Čísla a výrazy

Zkus následující příkazy:

```
>>> 2 + 2
4
```

Výsledkem sčítání je celé číslo. Pokud budeme dělit, výsledkem bude číslo s pohyblivou čárkou (floating-point number).


```
>>> 1 / 2
0.5
>>> 1 / 1
1.0
```


