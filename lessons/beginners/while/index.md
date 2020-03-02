# While

Kromě cyklu `for` máme ještě druhý typ cyklu: `while` (angl. *dokud*).
Na rozdíl od `for`, kde *předem známe počet opakování*,
se while používá když cyklus závisí na nějaké podmínce.
Tělo cyklu se opakuje, dokud je podmínka splněna.
Zkus si naprogramovat následující postup pro zubaře:

* Řekni, aby pacient řekl „Ááá“ a počkej na odpověď
* Dokud pacient *ne*řekl „Ááá“:
  * Vynadej pacientovi
  * Znovu počkej na odpověď

```python
odpoved = input('Řekni Ááá! ')
while odpoved != 'Ááá':
    print('Špatně, zkus to znovu')
    odpoved = input('Řekni Ááá! ')
```

Ale pozor! Je velice jednoduché napsat cyklus,
jehož podmínka bude splněna vždycky.
Takový cyklus se bude opakovat donekonečna.

* Dokud je pravda pravdivá:
  * Napiš náhodné číslo
  * Napiš hlášku

```python
from random import randrange

while True:
    print('Číslo je', randrange(10000))
    print('(Počkej, než se počítač unaví...)')
```

Program se dá přerušit zmáčknutím
<kbd>Ctrl</kbd>+<kbd>C</kbd>.
Tahle klávesová zkratka vyvolá v programu chybu
a program se – jako po každé chybě – ukončí.

> [note] Pro macOS
> I na Macu je to opravdu <kbd>Ctrl</kbd>+<kbd>C</kbd>, nikoli
> <kbd>⌘ Cmd</kbd>+<kbd>C</kbd>.

> [note] Pro ostatní systémy
> <kbd>Ctrl</kbd>+<kbd>C</kbd> je velice stará zkratka, zavedená ještě před
> grafickými programy které ji začaly používat pro kopírování.
> Když dnes používáš textové programy v okýnku,
> musíš pro kopírování použít složitější zkratky:
>
> * Kopírovat:
>   <kbd>Shift</kbd>+<kbd>Ctrl</kbd>+<kbd>C</kbd> nebo
>   <kbd>Ctrl</kbd>+<kbd>Insert</kbd>
>
> * Vložit:
>   <kbd>Shift</kbd>+<kbd>Ctrl</kbd>+<kbd>V</kbd> nebo
>   <kbd>Shift</kbd>+<kbd>Insert</kbd>
>
> Případně můžeš najít příslušné operace v menu.
> Na Windows se menu skrývá pod ikonkou v levém horním rohu okýnka;
> funkce pro kopírování jsou v podmenu Edit.
> Na starších Windows tam najdeš i *Mark*, způsob jak označit text.
>
> A na Linuxu jde jen označit text a pak ho (bez <kbd>Ctrl</kbd>+<kbd>C</kbd>)
> vložit prostředním tlačítkem myši.

## Break

A nakonec, existuje příkaz `break`, který z cyklu „vyskočí“:
začnou se hned vykonávat příkazy za cyklem.

Cyklus `while` se dívá na podmínku jen na začátku každého průchodu cyklem.
Občas ale chceš podmínku uprostřed nebo na konci.
Třeba „zubařský“ program výše by se dal napsat i takto:

* Opakuj:
  * Zeptej se na odpověd
  * Je-li odpověď „Ááá“, zavtipkuj a ukonči cyklus
  * Vynadej uživateli. (Sem se program dostane jen při špatné odpovědi.)
* Dokonči operaci

V překladu do Pythonu využiješ kombinace `if` a `break`:

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
a pokud máš víc cyklů zanořených v sobě, vyskočí jen z toho vnitřního.

```python
for i in range(10):  # Vnější cyklus
    for j in range(10):  # Vnitřní cyklus
        print(j * i, end=' ')
        if i <= j:
            break
    print()
```
