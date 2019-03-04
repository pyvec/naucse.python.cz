# While

Kromě cyklu `for` máme ještě druhý typ cyklu uvozený příkazem `while`
(angl. *dokud*).
Na rozdíl od `for`, kde *předem známe počet opakování*,
se while používá, když cyklus závisí na nějaké podmínce.
Tělo cyklu se opakuje, dokud je podmínka splněna. Například:

```python
odpoved = input('Řekni Ááá! ')
while odpoved != 'Ááá':
    print('Špatně, zkus to znovu')
    odpoved = input('Řekni Ááá! ')
```

Ale pozor! Je velice jednoduché napsat cyklus,
jehož podmínka bude splněna vždycky.
Takový cyklus se bude opakovat donekonečna.

```python
from random import randrange

while True:
    print('Číslo je', randrange(10000))
    print('(Počkej, než se počítač unaví...)')
```

Program se dá přerušit zmáčknutím
<kbd>Ctrl</kbd>+<kbd>C</kbd>.

> [note]
> Tahle klávesová zkratka vyvolá v programu chybu
> a program se – jako po každé chybě – ukončí.

A nakonec, existuje příkaz `break`, který z cyklu „vyskočí“:
začnou se hned vykonávat příkazy za cyklem.

```python
while True:
    odpoved = input('Řekni Ááá! ')
    if odpoved == 'Ááá':
        print('Bééé')
        break
    print('Špatně, zkus to znovu')

print('Hotovo, ani to nebolelo.')
```

Příkaz `break` se dá použít jenom v cyklu (`while` nebo `for`)
a pokud máme víc cyklů zanořených v sobě, vyskočí jen z toho vnitřního.

```python
for i in range(10):  # Vnější cyklus
    for j in range(10):  # Vnitřní cyklus
        print(j * i, end=' ')
        if i <= j:
            break
    print()
```
