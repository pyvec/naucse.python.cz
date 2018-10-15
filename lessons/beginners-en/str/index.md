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
as calling a function but with square brackets.

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
  │  P │ y │ L │ a │ d │ i │ e │ s │
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
  │  P │ y │ L │ a │ d │ i │ e │ s │
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
Formatting is used when you need to include variables value into
the string.

```python
number = 3 + 4
name = "Mary"
write = 'Hi {}! The result is {}.'.format(name, number)
print(write)
```

It is almost the same with old fashioned `%s`, but instead of `.format`
you write `%`. If you want are using just one variable you don't
need brackets, just make sure that there is one space after `%`.

```python
number = 3 + 4
name = "Mary"
write = 'Hi %s! The result is %s.' % (name, number)
print(write)
```
## Substrings

Now we will go back to subscripting.
Try to find out what the following program does:

```python
string = 'PyLadies'
substring = string[5:]
print(substring)
```

> [warning]
> Keep in mind that we are still counting from 0!

{% filter solution %}
`string[5:]` will print *substring* from the fifth character to the end.
{% endfilter %}

We can also use `string[:5]`, which will select all to the
fifth character, which is not included.
So`string[:5] + string[5:] == string`.


What is doing `string[2:5]`?

And what about `string[-4:]`?

```python
string = 'PyLadies'
print(string[:4])
print(string[2:5])
print(string[-4:])
```

You have to think about what number, *index*, you want to use.

It is better to put numbers on borderlines between
every character, it is better to understand:

{{ anchor('slicing-diagram') }}
```plain
 ╭───┬───┬───┬───┬───┬───┬───┬───╮
  │ P │ y │ L │ a │ d │ i │ e │ s │
  ├───┼───┼───┼───┼───┼───┼───┼───┤
  │   │   │   │   │   │   │   │   │
  0   1   2   3   4   5   6   7   8
 -8  -7  -6  -5  -4  -3  -2  -1

  ╰───────────────╯
  'PyLadies'[:4] == 'PyLa'

          ╰───────────────╯
        'PyLadies'[2:6] == 'Ladi'

                      ╰───────────╯
                      'PyLadies'[-3:] == 'ies'
```


## Exercise 

Try to write a function `change(string, position, character)`.

This function returns string which has given character on given
position. The rest is the same as the original `string`.
For example:

```python
change('doctor', 2, 'g') == 'dogtor'
change('slice', 1, 'p') == 'spice'
```

Keep in mind that you can't change a string.
You can only create new one and put together
some pieces from the old one.

{% filter solution %}
```python
def change(string, position, character):
    """This function changes given character on given position.
    
    Returns new string which has given character on given
    position. The rest is the same as the original string.
    """

    return string[:position] + character + string[position + 1:]
```
{% endfilter %}
