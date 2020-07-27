# Výběr z řetězců


Už umíš spojovat dohromady kratší řetězce:

```python
spojeny_retezec = 'a' + 'b'
dlouhy_retezec = 'ó' * 100
```
Teď se podíváme na opačný proces: jak z dlouhého
řetězce dostat kratší součásti.
Začneme jednotlivými znaky.


## Výběr znaku

Konkrétní znak na dané pozici se z řetězce dá vybrat operací *vybrání prvku*
(angl. *subscripting*),
která se píše podobně jako volání funkce, jen s hranatými závorkami.
Třeba takhle se dá vybrat znak na páté pozici:

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

Stejně je to i se znaky v řetězcích. První písmeno má číslo nula,
druhé jedna, ... a osmé písmeno má číslo sedm.

Proč je tomu tak?
K úplnému pochopení důvodů by ses potřeboval{{a}}
naučit něco o ukazatelích a polích,
což nebude hned, takže pro teď nám bude
stačit vědět,
že programátoři jsou prostě divní.

Nebo aspoň že mají rádi divná čísla – jako nulu.

```plain
   [0] [1] [2] [3] [4] [5] [6] [7]

  ╭───┬───┬───┬───┬───┬───┬───┬───╮
  │ Č │ o │ k │ o │ l │ á │ d │ a │
  ╰───┴───┴───┴───┴───┴───┴───┴───╯
```


A když už jsme u divných čísel,
co se asi stane, když budu vybírat písmena pomocí záporných čísel?

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



## Sekání řetězců

Kromě jednotlivých znaků můžeme vybírat i delší části – odborně
*podřetězce* (angl. *substrings*).

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
Ne však znak 5 samotný, což je možná trochu zarážející,
ale je potřeba s tím počítat.
Poslední prvek není ve výběru obsažen, podobně jako `range(5)` neobsahuje
číslo 5.

Ačkoli je tohle chování divné, má hezké důsledky.
Všimni si třeba, že `retezec[:5] + retezec[5:]` ti dá zpět původní `retezec`.

Podobnému vybírání podřetězců se říká „sekání“ řetězců
(angl. *string slicing*).

Sekání „od“ a „do“ se dá kombinovat.
Zkus si to: co asi udělají následující příkazy?

```python
retezec = 'čokoláda'
print(retezec[:4])
print(retezec[2:6])
print(retezec[-3:])
print(retezec[:])
```

{% filter solution %}
Zápis `retezec[od:do]` vybere *podřetězec* od pozice `od` do pozice `do`.
Když jednu z hodnot vynecháš, vybírá se od začádku, resp. do konce.

```python
retezec = 'čokoláda'
print(retezec[:4])      # → čoko
print(retezec[2:6])     # → kolá
print(retezec[-3:])     # → áda
print(retezec[:])       # → čokoláda
```
{% endfilter %}

Určování vhodných čísel, *indexů*, občas vyžaduje trochu zamyšlení.

U sekání (s `:`) pomáhá očíslovat si „hranice“ mezi znaky,
abys v tom měl{{a}} lepší přehled:

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

Zkus napsat program `zamen.py`, který umí zaměnit jedno písmeno ve slově za
jiné. Například:

```python
slovo = input('Slovo: ')
pozice = int(input('Které písmeno zaměnit (od nuly)? '))
novy_znak = input('Nové písmeno: ')

... # sem doplň kód

print(nove_slovo)
```

Příklad použití:

<pre>
Slovo: <strong>čokoláda</strong>
Které písmeno zaměnit (od nuly)? <strong>3</strong>
Nové písmeno: <strong>u</strong>
<strong>čokuláda</strong>
</pre>

<pre>
Slovo: <strong>kočka</strong>
Které písmeno zaměnit (od nuly)? <strong>1</strong>
Nové písmeno: <strong>a</strong>
<strong>kačka</strong>
</pre>

Pozor na to, že řetězce v Pythonu nelze měnit.
Nemůžeš v existujícím řetězci zaměnit jeden znak za jiný;
musíš vytvořit nový řetězec poskládaný z částí toho starého.

{% filter solution %}
```python
slovo = input('Slovo: ')
pozice = int(input('Které písmeno zaměnit (od nuly)? '))
novy_znak = input('Nové písmeno: ')

zacatek_slova = slovo[:pozice]
konec_slova = slovo[pozice + 1:]
nove_slovo = zacatek_slova + novy_znak + konec_slova

print(nove_slovo)
```
{% endfilter %}
