# Strings

Now we will learn something about strings.
You already know how to write them into Python code.

```python
'This is string'
"And this is also string"
```

Sometimes you will need string that is multipleline.
But you can write string only on one line in Python
(you can actually write on more lines but the text would
appear just on one).

You can write into your text special character that means
new line `\n`:

```python
print('Hello word\nHow are you?')
```
Backslash allows us to write characters which we can't easily
on keyboard.
It also allows us to write both types of quotes into the text. 

```python
print('"Don\'t do it", said dad.')
print("\"Don't do it\", said dad.")
```

Backward slashes can also add exotic characters 
that you do not have on the keyboard.
Fancy characters can be written as `\N` and a character 
name in compound ("curly") brackets.
For example following characters
(some might not work for your system):

```python
print('--\N{LATIN SMALL LETTER L WITH STROKE}--')
print('--\N{SECTION SIGN}--')
print('--\N{PER MILLE SIGN}--')
print('--\N{BLACK STAR}--')
print('--\N{SNOWMAN}--')
print('--\N{KATAKANA LETTER TU}--')
```

If you want to write in text backslash you have to
write it twice (for example path to some
file in Windows).
So sequence `\\` means one backslash.

```python
print('C:\\PyLadies\\Nový adresář')
```

But back to multipleline strings. There is also another way how to write them
in Python. You just have to write them in *three* single
or double quotes:

```python
basen = '''Hello World!
How are you?'''
```

Programmers also use three quotes for documentation of functions.

```python
def multiply(a, b):
    """ This function multiplies two arguments and returns the result.

    Both arguments should be numbers.
    """

    return a * b
```


Now we will have a look on how to work with them.


## Subscripting

You already know how to concatenate string by addition.

```python
concatenated_string = 'a' + 'b'
long_string = 'o' * 100
```
Now we will learn how we can get a part from a string.
We will start with single characters.
It is done by *subscripting*, which is written similarly
as calling a functin but with square brackets.

```python
fifth_character = 'PyLadies'[5]

print(fifth_character)
```

Does it work? Did you get really the fifth character?

{% filter solution %}
You didn't – you got the *sixth* character.
{% endfilter %}

As you may already noticed programmers counts from zero.
First is 0, then 1 and so on.

It's the same with strings - first character is on zero position.

Why is it like that?
You would have to know about pointers and arrays
to fully understand so now we can just think
that programmers are weird. Or that they just like
weird numbers.


```plain
   [0] [1] [2] [3] [4] [5] [6] [7]

  ╭───┬───┬───┬───┬───┬───┬───┬───╮
  │ P │ y │ L │ a │ d │ i │ e │ s │
  ╰───┴───┴───┴───┴───┴───┴───┴───╯
```


But what will happen if you would like
to pick character with negative numbers?


{% filter solution %}
```python
print('PyLadies'[-1])  # → s
print('PyLadies'[-2])  # → e
print('PyLadies'[-3])  # → i
print('PyLadies'[-4])  # → d
```

Negative numbers picks characters from the end.

```plain
   [0] [1] [2] [3] [4] [5] [6] [7]
   [-8][-7][-6][-5][-4][-3][-2][-1]
  ╭───┬───┬───┬───┬───┬───┬───┬───╮
  │ P │ y │ L │ a │ d │ i │ e │ s │
  ╰───┴───┴───┴───┴───┴───┴───┴───╯
```
{% endfilter %}

Strings can do more tricks.
You can find out how long is the string
or if it contains some substring.

<table class="table">
    <tr>
        <th>Zápis</th>
        <th>Description</th>
        <th>Example</th>
    </tr>
    <tr>
        <td><code>len(r)</code></td>
        <td>Length of string</td>
        <td><code>len('PyLadies')</code></td>
    </tr>
    <tr>
        <td><code>x&nbsp;in&nbsp;r</code></td>
        <td>True if sttring <code>x</code> is in string <code>r</code></td>
        <td><code>'Ladies' in 'PyLadies'</code></td>
    </tr>
    <tr>
        <td><code>x&nbsp;not&nbsp;in&nbsp;r</code></td>
        <td>Opposite <code>x in r</code></td>
        <td><code>'eye' not in 'PyLadies</code></td>
    </tr>
</table>

Řetězce vždy berou v potaz velikost písmen,
takže např. `'ČOKO' in 'PyLadies'` je `False`.
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


## Formátování

Obzvláště užitečná je metoda `format`,
která v rámci řetězce nahradí dvojice „kudrnatých“ závorek
za to, co dostane v argumentech:

```python
vypis = '{}×{} je {}'.format(3, 4, 3 * 4)
print(vypis)
```

Řetězec `'{}×{} je {}'` tady funguje jako *šablona* (angl. *template*).
Představ si to jako jako formulář, do kterého Python na vyznačená místa
vpisuje hodnoty.

Pokud chceš nahradit hodnoty v jiném pořadí, nebo když chceš aby šablona
byla čitelnější, můžeš do „kudrnatých“ závorek napsat jména:

```python
vypis = 'Ahoj {jmeno}! Výsledek je {cislo}.'.format(cislo=7, jmeno='Elvíro')
print(vypis)
```

Formátování se používá skoro všude, kde je
potřeba „hezky“ vypsat nějakou hodnotu.


## Sekání řetězců

Teď se vrátíme k vybírání kousků řetězců.
Zkus, co dělá tenhle program:

```python
retezec = 'PyLadies'
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
retezec = 'PyLadies'
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
  'PyLadies'[:4] == 'čoko'

          ╰───────────────╯
        'PyLadies'[2:6] == 'kolá'

                      ╰───────────╯
                      'PyLadies'[-3:] == 'áda'
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
