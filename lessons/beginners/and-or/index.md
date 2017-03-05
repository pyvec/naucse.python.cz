{% if var('bonus') %}
!!! note ""
    Na tuto stránku odkazuje domácí projekt.
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
        <td><code>True and False</code></td>
        <td>„a zároveň“</td>
    </tr>
    <tr>
        <td><code>or</code></td>
        <td><code>True or False</code></td>
        <td>„a nebo“</td>
    </tr>
    <tr>
        <td><code>not</code></td>
        <td><code>not False</code></td>
        <td>„ne“</td>
    </tr>
</table>

Pro příklad použijeme `and` v tomto programu.
Zkus si ho projít a okomentovat části, které nejsou na první pohled jasné.

```python
# Tento program rozdává naivní rady do života.

print('Odpovídej "ano" nebo "ne".')
stastna_retezec = input('Jsi šťastná? ')
if stastna_retezec == 'ano':
    stastna = True
elif stastna_retezec == 'ne':
    stastna = False
else:
    print('Nerozumím!')

bohata_retezec = input('Jsi bohatá? ')
if bohata_retezec == 'ano':
    bohata = True
elif bohata_retezec == 'ne':
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

!!! note ""
    Všimni si co se stane když zadáš něco jiného než „ano“ nebo „ne“.

    Proměnná `stastna` nebo `bohata` se nenastaví, a když je ji potom
    potřeba použít, program skončí s chybou.
    
    O tom, jak se vypořádat s chybami, si povíme [později]({{ lesson_url('beginners/exceptions') }}).
