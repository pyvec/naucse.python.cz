# Iterátory n-tic

Některé hodnoty v Pythonu jsou *iterovatelné* (angl. *iterable*):
obsahují sekvenci jiných hodnot a lze je „projít“ (iterovat) cyklem `for` nebo
je převést na seznam.
Už jich známe několik:

```pycon
>>> list(range(10))                 # sekvence čísel
>>> list('ahoj')                    # řetězec
>>> list(['Ahoj', 'Hello', 'Hei'])  # seznam
>>> list((12, 'Sr', True))          # n-tice
```

Spousta těchto typů umí něco navíc: zjistit jestli obsahují nějaký prvek
(`4 in range(10)`), zjistit délku (`len([1, 2, 3])`), převést na velká písmena
(`'abc'.upper()`).
Nic z toho ale není potřeba, aby byl objekt iterovatelný.

Podívejme se na dva dalších iterovatelné objekty: `enumerate` a `zip`.


## Enumerate: očíslování sekvence

Funkce `enumerate` vezme nějakou existující sekvenci a *očísluje ji*:
ve vrácené sekvenci budou dvojice (index, původní hodnota).

Řekněme že máš tento seznam:

```python
trpaslici = ['Prófa', 'Stydlín', 'Dřímal', 'Kejchal', 'Štístko',
             'Šmudla', 'Rejpal']
```

Když na něj použiješ `enumerate`, dostaneš objekt `enumerate`,
který podobně jako `range()` neukáže svůj obsah „rovnou“,
ale můžeš se „do něj“ podívat převedením na seznam.
Uvidíš tak seznam dvojic (číslo, trpaslík):

```pycon
>>> enumerate(trpaslici)
<enumerate object at 0x7f0db61b29d8>
>>> list(enumerate(trpaslici))
[(0, 'Prófa'), (1, 'Stydlín'), (2, 'Dřímal'), (3, 'Kejchal'), (4, 'Štístko'), (5, 'Šmudla'), (6, 'Rejpal')]
```

Místo převedení na seznam můžeš přes objekt `enumerate` iterovat cyklem `for`
a pro každou dvojici něco udělat.
Třeba ji hezky vypsat:

```python
for dvojice in enumerate(trpaslici):
    # Rozbalení dvojice
    index, trpaslik = dvojice
    # Vypsání
    print(f'Na pozici {index} je {trpaslik}!')
```

Objekt, který funkce `enumerate` vrací, je *iterátor dvojic* – sekvence,
jejíž prvky jsou dvojice.

## Rozbalování v cyklu for

„Trpasličí“ cyklus se dá rozepsat takto:

```python
dvojice = 0, 'Prófa'    # toto dělá `for`
index, trpaslik = dvojice
print(f'Na pozici {index} je {trpaslik}!')

dvojice = 1, 'Stydlín'  # toto dělá `for`
index, trpaslik = dvojice
print(f'Na pozici {index} je {trpaslik}!')

dvojice = 2, 'Dřímal'  # toto dělá `for`
index, trpaslik = dvojice
print(f'Na pozici {index} je {trpaslik}!')

# A tak dále
```

Kdybys to psal{{a}} ručně, lze to zjednodušit – přiřadit do dvou proměnných
najedno, bez pomocné `dvojice`:

```python
index, trpaslik = 0, 'Prófa'    # toto by mohl dělat `for`
print(f'Na pozici {index} je {trpaslik}!')

index, trpaslik = 1, 'Stydlín'  # toto by mohl dělat `for`
print(f'Na pozici {index} je {trpaslik}!')

index, trpaslik = 2, 'Dřímal'  # toto by mohl dělat `for`
print(f'Na pozici {index} je {trpaslik}!')

# A tak dále
```

A `for` tohle ve skutečnosti umí: místo do proměnné `dvojice` může přiřadit
rovnou do dvou proměnných `index, trpaslik`:

```python
for index, trpaslik in enumerate(trpaslici):
    print(f'Na pozici {index} je {trpaslik}!')
```

Tohle je docela častẙ způsob práce s *iterátorem n-tic* – máš-li sekvenci,
jejíž prvky jsou <var>n</var>-tice, můžeš jednotlivé součásti <var>n</var>-tice
rozbalit přímo v hlavičce `for` cyklu.

Zkus si to! Zkopíruj si tento seznam:

```python
dny = ['Po', 'Út', 'St', 'Čt', 'Pá', 'So', 'Ne']
```

… a zkus vypsat:

```plain
1. Po
2. Út
3. St
4. Čt
5. Pá
6. So
7. Ne
```

{% filter solution %}

```python
dny = ['Po', 'Út', 'St', 'Čt', 'Pá', 'So', 'Ne']
for index, den in enumerate(dny):
    cislo = index + 1
    print(f'{cislo}. {den}')
```

To je trošku kostrbaté, ale dá se to zjednodušit: funkce `enumerate` zná
pojmenovaný argument `start`, pomocí kterého umí sama
počítat od jiného začátku než od nuly:

```python
dny = ['Po', 'Út', 'St', 'Čt', 'Pá', 'So', 'Ne']
for index, den in enumerate(dny, start=1):
    print(f'{index}. {den}')
```

{% endfilter %}


## Zip: Víc iterací najednou

Další iterátor <var>n</var>-tic je funkce `zip`, která umí projít dvě sekvence
naráz.
Řekněme že máš seznam věcí a k nim příslušných barev:

``` python
veci = ['tráva', 'slunce', 'mrkev', 'řeka']
barvy = ['zelená', 'žluté', 'oranžová', 'modrá']
```

Kdtyž tyto dva seznamy dáš funkci `zip`, dostaneš iterátor který příslušné
hodnoty spáruje.
Bude tedy obsahovat:

* Dvojici prvních prvků obou seznamů
* Dvojici druhých prvků obou seznamů
* Dvojici třetích prvků obou seznamů
* ...

``` python
for vec, barva in zip(veci, barvy):
    print(f"{vec} je {barva}")
```

Funguje to i pro více sekvencí.
V následujícím případě je výsledný `zip` iterátor čtveřic (věc, barva,
místo, číslo):

```python
veci = ['tráva', 'slunce', 'mrkev', 'řeka']
barvy = ['zelená', 'žluté', 'oranžová', 'modrá']
mista = ['na zemi', 'nahoře', 'na talíři', 'za zídkou']
cisla = range(4)

for vec, barva, misto, cislo in zip(veci, barvy, mista, cisla):
    print(f"{cislo}. {barva} {vec} je {misto}")
```

Když si ale vypíšeš samotný objekt `zip`, zjistíš že o sobě nic moc neřekne
– podobně jako `enumerate`:

```pycon
>>> zip(veci, barvy, mista, cisla)
<zip object at 0x7f0db61b1f48>
```


## Zip Longest: Pro ty co chtějí všechno

Jak se `zip` chová, když dostane seznamy různých délek?

```python
veci = ['tráva', 'slunce', 'mrkev', 'řeka', 'myšlenka', 'spravedlnost']
barvy = ['zelená', 'žluté', 'oranžová', 'modrá']
for vec, barva in zip(veci, barvy):
    print(f"{vec} je {barva}")
```

{% filter solution %}
Výsledek `zip` skončí hned když „dojde“ nejkratší sekvence.
{% endfilter %}

Občas je potřeba projít všechny záznamy.
Na to slouží funkce `zip_longest` z modulu `itertools`:

```python
from itertools import zip_longest
for vec, barva in zip_longest(veci, barvy, fillvalue='(nevím)'):
    print(f"{vec} je {barva}")
```

Argument `fillvalue` říká, co se doplní za chybějící hodnoty.
Když ho nezadáš, doplní se `None` („nic“, hodnota kterou např. vrací procedury).
To se často používá, když je pro chybějící hodnoty potřeba nějaká
složitější logika:

```python
from itertools import zip_longest
for vec, barva in zip_longest(veci, barvy):
    if vec == None:
        vec = 'nějaká věc'
    if barva == None:
        barva = 'bez barvy'
    print(f"{vec} je {barva}")
```

