# Přepisování proměnných

Už víš, že hodnota proměnné se může v čase měnit:
když přiřadíš do už existující proměnné, stará hodnota se zahodí
a použije se nová.

```python
oblibena_barva = 'modrá'
print(oblibena_barva)

oblibena_barva = 'žlutá'
print(oblibena_barva)

# Na tomhle místě programu už se k řetězci 'modrá' nedostaneš...
```

Trošku zajímavější (nebo složitější?) je situace, kdy hodnotu proměnné
přepíšeš výrazem, který používá tu stejnou proměnnou.
Zkus si to:


```python
oblibene_cislo = 7
print(oblibene_cislo)

oblibene_cislo = oblibene_cislo * 6
print(oblibene_cislo)
```

Co se tady děje?
Python vyhodnotí výraz za `=` se *starou* hodnotou proměnné, a teprve když
zná výsledek, přiřadí ho (a na starou hodnotu zapomene).
V našem příkladu postupuje takhle:

```python
oblibene_cislo = oblibene_cislo * 6
#                ╰──────────┬─╯
oblibene_cislo =            7   * 6
#                           ╰─┬───╯
oblibene_cislo =             42
#         ▲                  |
#         ╰──────────────────╯
```



## Přepisování v cyklu

Ještě „zajímavější“ je použít podobné přepisování v cyklu.

Zopakuj si, že `for` cyklus jako:

```python
print("Tady je pár čísel:")

for cislo in 8, 45, 9, 21:
    print(cislo)
```

opakuje *přiřazení do proměnné* a *tělo cyklu*; můžeš si ho rozepsat jako:

```python
print("Tady je pár čísel:")

cislo = 8
print(cislo)

cislo = 45
print(cislo)

cislo = 9
print(cislo)

cislo = 21
print(cislo)
```

Zkus podobně rozepsat cyklus v následujícím programu
a popsat, co se děje:

```python
celkem = 0

for delka_trasy in 8, 45, 9, 21:
    print('Jdu', delka_trasy, 'km do další vesnice.')
    celkem = celkem + delka_trasy

print('Celkem jsem ušla', celkem, 'km')
```


{% filter solution %}
```python
celkem = 0

delka_trasy = 8
print('Jdu', delka_trasy, 'km do další vesnice.')
celkem = celkem + delka_trasy

delka_trasy = 45
print('Jdu', delka_trasy, 'km do další vesnice.')
celkem = celkem + delka_trasy

delka_trasy = 9
print('Jdu', delka_trasy, 'km do další vesnice.')
celkem = celkem + delka_trasy

delka_trasy = 21
print('Jdu', delka_trasy, 'km do další vesnice.')
celkem = celkem + delka_trasy

print('Celkem jsem ušla', celkem, 'km')
```

Příkaz `celkem = celkem + delka_trasy` vypočítá hodnotu
`celkem + delka_trasy`, tedy přičte aktuální číslo k součtu.
Výsledek uloží opět do proměnné `celkem`.
Nová hodnota `celkem` se pak použije v dalším průchodu cyklem.

Na začátku je `celkem` 0 a na konci se celkový součet všech čísel vypíše.
{% endfilter %}
