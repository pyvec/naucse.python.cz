# Řetězce

Teď se podíváme na zoubek řetězcům (angl. *strings*).
Už víš, jak je zapisovat:

```python
'tohle je řetězec'
"tohle taky"
```

Někdy potřebuješ řetězce, které obsahují více řádků.
Pythonní řetězce ale můžeš normálně napsat jen na jeden řádek.
Jinak by koncová uvozovka mohla být kdekoli
a špatně by se hledala, kdybys na ni zapomněl{{a}}.

Můžeš ale do řetězce znak pro nový řádek vložit pomocí speciálního
zápisu `\n`:

```python
print('Haló haló!\nCo se stalo?')
```

Obecně zpětné lomítko umožňuje zapsat znaky, které by se špatně zadávaly.
Třeba uvozovka se dá zapsat jako `\"` a „apostrof“ jako `\'`.
To se dá použít, když potřebuješ mít v jednom
řetězci uvozovku i apostrof:

```python
print("Vtom vnuk křik': \"Hleď!\"")
print('"Jen ho nech," řek\' děd. "Kdo zná líp kraj?"')
```

Zpětným lomítkem se dají přidávat i
exotické znaky, které nemáš na klávesnici.
Ty se dají zapsat jako `\N` a jméno znaku
v složených („kudrnatých“) závorkách.
Třeba následující znaky.
(Do konzole na Windows bohužel nemusí jít všechny
vypsat, ale aspoň první by jít měl):

```python
print('--\N{LATIN SMALL LETTER L WITH STROKE}--')
print('--\N{SECTION SIGN}--')
print('--\N{PER MILLE SIGN}--')
print('--\N{BLACK STAR}--')
print('--\N{SNOWMAN}--')
print('--\N{KATAKANA LETTER TU}--')
```

Tahle vychytávka má jeden, někdy nepříjemný,
důsledek: pokud chceš použít zpětné lomítko
(třeba ve jménech souborů na Windows),
musíš ho ve zdrojovém kódu zdvojit.
Sekvence `\\` znamená „jedno zpětné lomítko“.

```python
print('C:\\PyLadies\\Nový adresář')
```

Ale zpátky k řetězcům na více řádků. Kromě `\n` je i druhý způsob, jak takový
řetězec zadat: ohraničit ho *třemi* uvozovkami (jednoduchými nebo dvojitými)
na každé straně:

```python
basen = '''Haló haló!
Co se stalo?
Prase kozu potrkalo!'''
```

Takové dlouhé texty nachází uplatnění třeba v dokumentačních řetězcích
u funkcí.

```python
def vynasob(a, b):
    """Vynásobí argumenty a vrátí výsledek.

    Oba argumenty by měly být čísla.
    """

    return a * b
```

Jen pozor na to, že pokud je tenhle řetězec
v odsazeném kódu, každý jeho řádek bude začínat
několika mezerami.
(V dokumentačních řetězcích to nevadí, tam se s odsazením počítá.)

Tolik k zápisu řetězců.
Teď se podíváme, jak se zadanými řetězci pracovat.


## Výběr znaků

Už umíš spojovat dohromady kratší řetězce:

```python
spojeny_retezec = 'a' + 'b'
dlouhy_retezec = 'ó' * 100
```
Teď se podíváme na opačný proces: jak z dlouhého
řetězce dostat kratší součásti.
Začneme jednotlivými znaky.
Dělá se to operací *vybrání prvku* (angl. *subscripting*),
která se píše podobně jako volání funkce, jen s hranatými závorkami:

```python
pate_pismeno = 'čokoláda'[5]

print(pate_pismeno)
```

Funguje to? Dostal{{a}} jsi opravdu páté písmeno?

{% filter solution %}
Nedostal{{a}} – dostal{{a}} jsi *šesté* písmeno.
{% endfilter %}

Jak sis možná už všiml{{a}}, programátoři počítají od nuly.
„První“ prvek má vždy číslo nula, druhý číslo jedna a tak dál.

Stejně je to i s písmeny v řetězcích: první písmeno má číslo nula,
druhé jedna, ... a osmé písmeno má číslo sedm.

Proč je tomu tak?
K úplnému pochopení důvodů by ses potřeboval{{a}}
naučit něco o ukazatelích a polích,
což nebude hned, takže pro teď nám bude
stačit vědět,
že programátoři jsou prostě divní.

A nebo že mají rádi divná čísla jako nulu.

```plain
   [0] [1] [2] [3] [4] [5] [6] [7]

  ╭───┬───┬───┬───┬───┬───┬───┬───╮
  │ Č │ o │ k │ o │ l │ á │ d │ a │
  ╰───┴───┴───┴───┴───┴───┴───┴───╯
```


A když už jsme u divných čísel,
co se asi stane, když budu chtít vybírat písmena
pomocí záporných čísel?

{% filter solution %}
```python
print('Čokoláda'[-1])  # → a
print('Čokoláda'[-2])  # → d
print('Čokoláda'[-3])  # → á
print('Čokoláda'[-4])  # → l
```

Záporná čísla vybírají písmenka od konce.

```plain
   [0] [1] [2] [3] [4] [5] [6] [7]
   [-8][-7][-6][-5][-4][-3][-2][-1]
  ╭───┬───┬───┬───┬───┬───┬───┬───╮
  │ Č │ o │ k │ o │ l │ á │ d │ a │
  ╰───┴───┴───┴───┴───┴───┴───┴───╯
```
{% endfilter %}

Řetězce umí i jiné triky.
Třeba můžeš zjistit, jak je řetězec dlouhý
nebo jestli v sobě obsahuje daný menší řetězec.

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


## Sekání řetězců

Teď se vrátíme k vybírání kousků řetězců.
Zkus, co dělá tenhle program:

```python
retezec = 'čokoláda'
kousek = retezec[5:]
print(kousek)
```

{% filter solution %}
Zápis `retezec[5:]` vybere *podřetězec* od znaku číslo 5 dál.
{% endfilter %}


Dá se použít i `retezec[:5]`,
který vybere všechno *až po* znak číslo 5.
Ale ne znak 5 samotný, takže `retezec[:5] + retezec[5:] == retezec`.


Co asi udělá `retezec[2:5]`?

A co `retezec[-4:]`?

```python
retezec = 'čokoláda'
print(retezec[:4])
print(retezec[2:5])
print(retezec[-4:])
```

Určování vhodných čísel, *indexů*, občas vyžaduje trochu zamyšlení.

U podobného „sekání“ (angl. *string slicing*)
je lepší si číslovat „hranice“ mezi znaky.
Člověk tomu pak lépe rozumí:

{{ anchor('slicing-diagram') }}
```plain
  ╭───┬───┬───┬───┬───┬───┬───┬───╮
  │ Č │ o │ k │ o │ l │ á │ d │ a │
  ├───┼───┼───┼───┼───┼───┼───┼───┤
  │   │   │   │   │   │   │   │   │
  0   1   2   3   4   5   6   7   8
 -8  -7  -6  -5  -4  -3  -2  -1

  ╰───────────────╯
  'čokoláda'[:4] == 'čoko'

          ╰───────────────╯
        'čokoláda'[2:6] == 'kolá'

                      ╰───────────╯
                      'čokoláda'[-3:] == 'áda'
```


## Cvičení

Zkus napsat funkci `zamen(retezec, pozice, znak)`.

Tato funkce vrátí řetězec, který má na dané pozici
daný znak; jinak je stejný jako původní `retezec`. Např:

```python
zamen('palec', 0, 'v') == 'valec'
zamen('valec', 2, 'j') == 'vajec'
```

Pozor na to, že řetězce v Pythonu nelze měnit.
Musíš vytvořit nový řetězec poskládaný z částí toho starého.

{% filter solution %}
```python
def zamen(retezec, pozice, znak):
    """Zamění znak na dané pozici

    Vrátí řetězec, který má na dané pozici daný znak;
    jinak je stejný jako vstupní retezec
    """

    return retezec[:pozice] + znak + retezec[pozice + 1:]
```
{% endfilter %}
