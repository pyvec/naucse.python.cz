# Podmínky

Spoustu věcí v kódu chceme provádět, jen pokud jsou splněny určité podmínky.
Proto má Python *podmíněné příkazy*.

Zkusíme napsat program, který ověřuje tajné heslo.
Tenhle program napíše `True`, když zadáš slovo `čokoláda`:

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

Anglicky se „když“ řekne *if*. A to je i jméno Pythoního příkazu.
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
```

``` console
(venv) $ python python_intro.py
Zadej heslo: sezam
```

## Jinak

V předchozím příkladu byl kód proveden pouze v případě, že podmínka byla splněna.
Ještě lepší program by ale:

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

## Více možností

Občas se stane, že se program musí rozhodnout mezi více možnostmi.
K tomu slouží příkaz `elif`, zkratka znglického *else if* – „jinak, pokud“.

Napišme program, který okomentuje hlasitost hudby:

* Zeptá se na hlasitost, a odpověď uloží jako číslo.
* Když je hlasitost do 20:
    * vypíše „Je to dost potichu.“
* Jinak, když je hlasitost do 40:
    * vypíše „Jako hudba v pozadí dobré.“
* Jinak, když je hlasitost do 60:
    * vypíše „Skvělé, slyším všechny detaily.“
* Jinak, když je hlasitost do 80:
    * vypíše „Dobré na párty.“
* Jinak, když je hlasitost do 100:
    * vypíše „Trochu moc nahlas!“
* Jinak:
    * vypíše „Krvácí mi uši!“

V Pythonu:

```python
hlasitost = int(input('Jaká je nastavená hlasitost rádia? '))
if hlasitost < 20:
     print("Je to dost potichu.")
elif hlasitost < 40:
     print("Jako hudba v pozadí dobré.")
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
příslušnou hlášku a další možnosti přeskočí.


## Shrnutí

Co jsi viděl{{a}} v této lekci?

*   Příkazy **if** (pokud), **elif** (jinak, pokud) a **else** (jinak)
    podmiňují jiné příkazy.
*   **Odsazení** se používá pro podmíněné příkazy, které následují po
    `if` apod..
