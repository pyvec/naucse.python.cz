{% if var('bonus') %}
> [note]
> Na tuto stránku odkazuje domácí projekt.
{% endif %}

# *Nebo* anebo *a*

Vzpomínáš na tabulku operátorů
z [lekce o Porovnávání]( {{ lesson_url('beginners/comparisons')}} )?
Nyní si ji doplníme o další tři operátory,
které se hodí do podmínek:

<table class="table">
    <tr>
        <th>Symbol</th>
        <th>Příklad</th>
        <th>Popis</th>
    </tr>
    <tr>
        <td><code>and</code></td>
        <td><code>True and False</code><br><code>2 < 3 and 5 < 3</code></td>
        <td>„a zároveň“</td>
    </tr>
    <tr>
        <td><code>or</code></td>
        <td><code>True or False</code><br><code>2 < 3 or 5 < 3</code></td>
        <td>„a nebo“</td>
    </tr>
    <tr>
        <td><code>not</code></td>
        <td><code>not False</code><br><code>not 5 < 3</code</td>
        <td>„ne“</td>
    </tr>
</table>

Například, chceš-li zjistit, jestli je kterékoli z dvou čísel záporné,
můžeš napsat:

```python
a = float(input("Zadej první stranu obdélníka: "))
b = float(input("Zadej druhou stranu obdélníka: "))

if a <= 0 or b <= 0:
    print("Délka nemůže být záporná!")
```

> [warning] Falešní kamarádi
>
> Pozor na to, že `and` a `or` nejsou anglická slovíčka, ale operátory,
> které spojují logické výrazy.
> Na *obě* strany `and` i `or` patří výraz, jehož hodnota je `True`/`False`
> (například porovnání).
>
> ```python
> if a <= 0 or b <= 0:
> ```
>
> Může se zdát, že by se to dalo zkrátit a napsat `if a or b <= 0:` – „pokud
> je A nebo B menší než 0“.
> Ale to si Python přeloží na:
>
> ```python
> if (a) or (b <= 0):
> ```
>
> ... tedy  „pokud platí A, a nebo je B menší než 0“.
> A to moc smyslu nedává.
> (Kdy „platí“ celé číslo?)


## Šťastná/Bohatá

Pro příklad použijeme `and` ve vylepšeném programu, který rozdává nejapné rady
do života.
Zkus si ho projít a okomentovat části, které nejsou na první pohled jasné.

```python
# Tento program rozdává nejapné rady do života.

print('Odpovídej "ano" nebo "ne".')
stastna_retezec = input('Jsi šťastná? ')
if stastna_retezec == 'ano' or stastna_retezec == 'Ano':
    stastna = True
elif stastna_retezec == 'ne' or stastna_retezec == 'Ne':
    stastna = False
else:
    print('Nerozumím!')

bohata_retezec = input('Jsi bohatá? ')
if bohata_retezec == 'ano' or bohata_retezec == 'Ano':
    bohata = True
elif bohata_retezec == 'ne' or bohata_retezec == 'Ne':
    bohata = False
else:
    print('Nerozumím!')

if bohata and stastna:
    # Je bohatá a zároveň štǎstná, ta se má.
    print('Gratuluji!')
elif bohata:
    # Je bohatá, ale není „bohatá a zároveň šťastná“,
    # takže musí být jen bohatá.
    print('Zkus se víc usmívat.')
elif stastna:
    # Tady musí být jen šťastná.
    print('Zkus míň utrácet.')
else:
    # A tady víme, že není ani šťastná, ani bohatá.
    print('To je mi líto.')
```

> [note]
> Všimni si co se stane, když zadáš něco jiného než „ano“ nebo „ne“.
>
> Proměnná `stastna` nebo `bohata` se nenastaví, a když je ji potom
> potřeba použít, program skončí s chybou.
>
> O tom, jak se vypořádat s chybami, si povíme [později]({{ lesson_url('beginners/exceptions') }}).
