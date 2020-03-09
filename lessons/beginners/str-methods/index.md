# Řetězcové funkce a metody

Řetězce umí všelijaké triky.
Funkcí `len()` můžeš zjistit, jak je řetězec dlouhý;
operátorem `in` pak jestli v sobě obsahuje daný podřetězec.

<table class="table">
    <tr>
        <th>Zápis</th>
        <th>Popis</th>
        <th>Příklad</th>
    </tr>
    <tr>
        <td><code>len(r)</code></td>
        <td>Délka řetězce</td>
        <td><code>len('čokoláda')</code></td>
    </tr>
    <tr>
        <td><code>x&nbsp;in&nbsp;r</code></td>
        <td>True pokud je řetězec <code>x</code> obsažen v <code>r</code></td>
        <td><code>'oko' in 'čokoláda'</code></td>
    </tr>
    <tr>
        <td><code>x&nbsp;not&nbsp;in&nbsp;r</code></td>
        <td>Opak <code>x in r</code></td>
        <td><code>'dub' not in 'čokoláda</code></td>
    </tr>
</table>

Řetězce vždy berou v potaz velikost písmen,
takže např. `'ČOKO' in 'čokoláda'` je `False`.
Kdybys chtěl{{a}} porovnávat bez ohledu na velikost písmen,
musel{{a}} bys oba řetězce převést třeba na malá písmena
a pak je porovnat.

A jak se převádí na malá písmena?
K tomu budeme potřebovat další novou vlastnost Pythonu: metody.

## Metody

*Metoda* (angl. *method*) je jako funkce – něco, co se dá zavolat.
Na rozdíl od funkce je svázaná s nějakým *objektem* (hodnotou).
Volá se tak, že se za objekt napíše tečka,
za ní jméno metody a za to celé se, jako u funkcí, připojí závorky
s případnými argumenty.

Řetězcové metody `upper()` a `lower()`
převádí text na velká, respektive malá písmena.
Zkus si to!

```python
retezec = 'Ahoj'
print(retezec.upper())
print(retezec.lower())
print(retezec)
```

> [note]
> Všimni si, že původní řetězec se nemění; metoda vrátí nový řetězec, ten
> starý zůstává.
>
> To je obecná vlastnost řetězců v Pythonu: jednou existující řetězec se už
> nedá změnit, dá se jen vytvořit nějaký odvozený.


### Iniciály

Pro procvičení metod a vybírání znaků si zkus napsat program,
který se zeptá na jméno, pak na příjmení
a pak vypíše iniciály – první písmena zadaných jmen.

Iniciály jsou vždycky velkými písmeny
(i kdyby byl uživatel líný mačkat Shift).

{% filter solution %}
```python
jmeno = input('Zadej jméno: ')
prijmeni = input('Zadej příjmení ')
inicialy = jmeno[0] + prijmeni[0]
print('Iniciály:', inicialy.upper())
```

Způsobů, jak takový program napsat, je více.
Lze například zavolat `upper()` dvakrát – zvlášť na jméno a zvlášť na příjmení.

Nebo to jde zapsat i takto –
metoda se dá volat na výsledku jakéhokoli výrazu:

```python
jmeno = input('Zadej jméno: ')
prijmeni = input('Zadej příjmení ')
print('Iniciály:', (jmeno[0] + prijmeni[0]).upper())
```

Doporučuji spíš první způsob, ten se smysluplnými názvy proměnných.
Je sice delší, ale mnohem přehlednější.
{% endfilter %}

Řetězcových metod je celá řada.
Nejužitečnější z nich najdeš v [taháku](https://pyvec.github.io/cheatsheets/strings/strings-cs.pdf), který si můžeš stáhnout či vytisknout.

A úplně všechny řetězcové metody jsou popsány v [dokumentaci Pythonu](https://docs.python.org/3/library/stdtypes.html#string-methods) (anglicky; plné věcí, které ještě neznáš).

Všimni si, že `len` není metoda, ale funkce; píše se `len(r)`, ne `r.len()`.
Proč tomu tak je, to za nějakou dobu poznáš.


## Cvičení: Záměna znaku

Zkus napsat kód, který v daném slově zamění znak na dané pozici za jiný:
například ze slova *ba**ň**ka* udělá záměnou znaku číslo 2 na „*j*“ slovo
*ba**j**ka*:

```python
# Zaměň znak číslo 2 ve slově "baňka" na "j"
slovo = 'baňka'
pozice = 2
novy_znak = 'j'

... # dopiš kód, co vypíše "bajka"
```

Stejný kód by měl fungovat i když změníš počáteční proměnné:

```python
slovo = 'kočka'
pozice = 1
novy_znak = 'a'

# → kačka
```

```python
slovo = 'slůně'
pozice = 1
novy_znak = 't'

# → stůně
```

```python
slovo = 'kapka'
pozice = 0
novy_znak = 'l'

# → lapka
```


Pozor na to, že řetězce v Pythonu nelze měnit.
Musíš vytvořit nový řetězec poskládaný z částí toho starého.

{% filter solution %}
```python
slovo = 'baňka'
pozice = 2
novy_znak = 'j'

zacatek = slovo[:pozice]
konec = slovo[pozice + 1:]
nove_slovo = zacatek + novy_znak + konec

print(nove_slovo)
```

Nebo jednodušeji:

```python
nove_slovo = slovo[:pozice] + novy_znak + slovo[pozice + 1:]
```

{% endfilter %}

