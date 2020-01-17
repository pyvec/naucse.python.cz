# Podmínky

Spoustu věcí v kódu budeš chtít provádět,
jen pokud jsou splněny určité podmínky.
Na to má Python *podmíněné příkazy*.

Zkusíme teď postupně napsat program, který ověřuje tajné heslo.

Pro začátek napiš program, který vypíše `True`, když zadáš slovo `čokoláda`.
Když bude zadané heslo jiné, napíše `False`:

```python
heslo = input('Zadej heslo: ')
print(heslo == 'čokoláda')
```

## Když – tak

Vypsání `True` ale není moc zajímavé.
Lepší program by dělal tohle:

* Zeptá se na tajné heslo
* Když je heslo správné:
    * Pustí uživatele dovnitř

Anglicky se „když“ řekne *if*. A to je i jméno Pythonního příkazu.
Používá se takhle:

```python
heslo = input('Zadej heslo: ')
if heslo == 'čokoláda':
    print('Správně! Račte vstoupit.')
```

Podmíněný příkaz začíná `if`, pokračuje podmínkou (třeba porovnáním)
a končí dvojtečkou.

Po řádkem s `if` je příkaz *odsazený* – na začátku řádku jsou 4 mezery.
Podle toho Python pozná, že tuhle část programu má provést,
jen když je podmínka pravdivá.

Ulož a spusť:

``` console
(venv) $ python python_intro.py
Zadej heslo: čokoláda
Správně! Můžeš vstoupit.
(venv) $ python python_intro.py
Zadej heslo: sezam
```

### Odsazování

To, že jsou na začátku řádku potřeba čtyři mezery, neznamená že musíš
4× zmáčknout mezerník.
Některé editory odsazují automaticky (pokud napíšeš řádek s `if` správně).
Ve všech správně nastavených editorech ale lze odsadit pomocí klávesy
<kbd>↹ Tab</kbd> a kombinace <kbd>⇧ Shift</kbd>+<kbd>↹ Tab</kbd> vrátí řádek o jednu úroveň odsazení zpátky.


## Jinak

V předchozím příkladu byl kód proveden pouze v případě, že podmínka byla splněna.
Ještě lepší program by ale byl tenhle:

* Zeptá se na tajné heslo
* Když je heslo správné:
    * Pustí uživatele dovnitř
* Jinak <small>(tedy pokud heslo nebylo správné)</small>:
    * Spustí alarm

K tomu má Python příkaz `else` – „jinak“:

```python
heslo = input('Zadej heslo: ')
if heslo == 'čokoláda':
    print('Správně! Račte vstoupit.')
else:
    print('POZOR! POZOR!')
    print('NEOPRÁVNĚNÝ VSTUP!')
```

Funuje to?

``` console
(venv) $ python python_intro.py
Zadej heslo: čokoláda
Správně! Můžeš vstoupit.
(venv) $ python python_intro.py
Zadej heslo: sezam
POZOR! POZOR!
NEOPRÁVNĚNÝ VSTUP!
```


## Více možností

Občas se stane, že se program musí rozhodnout mezi více možnostmi.
K tomu slouží příkaz `elif` (zkratka znglického *else if* – „jinak, pokud“).

Třeba takovýmhle postupem se dá okomentovat hlasitost hudby:

* Zeptej se na hlasitost, zapamatuj si číselnou odpověď.
* Když je hlasitost do 20:
    * vypíše „Je to dost potichu.“
* Jinak, když je hlasitost do 40:
    * vypíše „Jako hudba na pozadí dobré.“
* Jinak, když je hlasitost do 60:
    * vypíše „Skvělé, slyším všechny detaily.“
* Jinak, když je hlasitost do 80:
    * vypíše „Dobré na párty.“
* Jinak, když je hlasitost do 100:
    * vypíše „Trochu moc nahlas!“
* Jinak:
    * vypíše „Krvácí mi uši!“

V Pythonu by se to zapsalo takto:

```python
hlasitost = int(input('Jaká je nastavená hlasitost rádia? '))
if hlasitost < 20:
     print("Je to dost potichu.")
elif hlasitost < 40:
     print("Jako hudba na pozadí dobré.")
elif hlasitost < 60:
     print("Skvělé, slyším všechny detaily.")
elif hlasitost < 80:
     print("Dobré na party.")
elif hlasitost < 100:
     print("Trochu moc nahlas!")
else:
    print("Krvácí mi uši!")
```

``` console
(venv) $ python python_intro.py
Jaká je nastavená hlasitost rádia? 28
Jako hudba v pozadí dobré.
```

Všimni si, že se vybere vždycky jedna alternativa.
Když zadáš `28`, Python se dostane k `hlasitost < 40`, vypíše
příslušnou hlášku a všechny další možnosti přeskočí.


## Shrnutí

Co jsi viděl{{a}} v této lekci?

*   Příkazy **if** (pokud), **elif** (jinak, pokud) a **else** (jinak)
    podmiňují jiné příkazy.
*   **Odsazení** se používá pro podmíněné příkazy, které následují po
    `if` apod..
