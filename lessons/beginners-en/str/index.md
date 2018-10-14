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
        <th>Code</th>
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
        <td>Opposite to <code>x in r</code></td>
        <td><code>'eye' not in 'PyLadies</code></td>
    </tr>
</table>

Python is case sensitive so `ladies in Pyladies`
is `False`. If you would like do it case insensitive
you would have to change case of both strings (lower or upper) and then
do `x in y`.

And how to change case of our string?
To do that we will need another Python feature: methods.

## Methods

*Methods* are like functions - we can call something with them.
Unlike a function, method is tied to some *object* (value).
It is called by writing colon and method's name just after the object.
And then, of course, brackets, which may contain arguments.

String methods `upper()` and `lower()` change the case.

```python
string = 'Hello'
print(string.upper())
print(string.lower())
print(string)
```

> [note]
> Notice that the original string is not changing.
> Methods return new string and the older string stays
> like it was.
>
> That is Python's standard behavior: already existing string can't be changed,
> we can only create new one - derived from the old one.


### Initials

For practicing methods and subscripting try to write a program,
which will ask user about their name, then their surname
and then it will print their initials - first letters of
name and surname.

Initials are always upper case (even if the
user won't write it that way).

{% filter solution %}
```python
name = input('Enter your name: ')
surname = input('Enter your surname: ')
initials = name[0] + surname[0]
print('Initials:', initials.upper())
```

There are more ways how to write such program.
You can call `upper()` twice - on name and surname separately.

Or like this:

```python
name = input('Enter your name: ')
surname = input('Enter your surname: ')
print('Initials:', (name[0] + surname[0]).upper())
```

I recommend the first option. It is longer but way more clear.
{% endfilter %}

There are many more string methods. You can find the most
useful in our [cheatsheet](https://github.com/muzikovam/cheatsheets/blob/master/strings/strings-en.pdf).

All methods are in [Python documentation](https://docs.python.org/3/library/stdtypes.html#string-methods).

Notice that `len` isn't method but function. It's
written `len(s)` not `r.len()`.
You will find out why it is like that in a minute.


## Formatting

Especially useful is `format` method, which replaces
pair of curly brackets in string for whatever it
gets as an argument.

```python
write = '{}×{} je {}'.format(3, 4, 3 * 4)
print(write)
```

String `'{}×{} je {}'` is something like *template*.
Imagine it as form, where are highlighted fields where Python
fills in values.

If you want to fill values in different order or you want
the template to be clearer, you can write variables into
curly braces:

```python
write = 'Hi {name}! The result is {number}.'.format(number=7, name='Mary')
print(write)
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
