# Strings

Now we will learn about strings.
You already know how to write them in Python code.

```python
'This is string'
"And this is also string"
```

Sometimes you will need a string that is multiple lines long.
But you can write strings only on one line in Python
(you can actually write on more lines but the text would
appear on just one).

In your text, you can use a special character that means
new line `\n`:

```python
print('Hello word\nHow are you?')
```
A backslash allows us to write characters which we can't easily
write on the keyboard.
The backslash also allows us to use both types of quotes in one piece of text. 

```python
print('"Don\'t do it", said dad.')
print("\"Don't do it\", said dad.")
```

Backward slashes can also insert exotic characters 
that you do not have on the keyboard.
Fancy characters can be written as `\N` and a character 
name in compound ("curly") braces.
Try for example the following characters
(some might not work for your system):

```python
print('--\N{LATIN SMALL LETTER L WITH STROKE}--')
print('--\N{SECTION SIGN}--')
print('--\N{PER MILLE SIGN}--')
print('--\N{BLACK STAR}--')
print('--\N{SNOWMAN}--')
print('--\N{KATAKANA LETTER TU}--')
```

If you want to write a backslash character in your text
you have to write it twice (for example, in a path to a
file in Windows).
So the sequence `\\` means one backslash.

```python
print('C:\\PyLadies\\New Folder')
```

But back to multi-line strings. There is also another way how to write them
in Python. You just have to wrap them in *three* single
or *three* double quotes:

```python
basen = '''Hello World!
How are you?'''
```

Programmers also use three quotes to document their functions.

```python
def multiply(a, b):
    """ This function multiplies two arguments and returns the result.

    Both arguments should be numbers.
    """

    return a * b
```


Now we will have a look at how to work with strings.


## Subscripting

You already know how to concatenate strings by addition and multiplication.

```python
concatenated_string = 'a' + 'b'
long_string = 'o' * 100
```
Now we will learn how we can get part of a string.
We will start with single characters.
This is done by *subscripting*. The Syntax looks similar
to calling a function but with square brackets.

```python
fifth_character = 'PyLadies'[5]

print(fifth_character)
```

Does it work? Did you really get the fifth character?

{% filter solution %}
You didn't – you got the *sixth* character.
{% endfilter %}

As you may have already noticed, programmers start counting from zero.
First comes 0, then 1, and so on.

It's the same with strings - the first character is on position zero.

Why is it like that?
You would have to know about pointers and arrays
to fully understand, so now let's just assume
that programmers are weird. Or that they just like
weird numbers.


```plain
   [0] [1] [2] [3] [4] [5] [6] [7]

  ╭───┬───┬───┬───┬───┬───┬───┬───╮
  │ P │ y │ L │ a │ d │ i │ e │ s │
  ╰───┴───┴───┴───┴───┴───┴───┴───╯
```


What happens if you pick characters with negative numbers?


{% filter solution %}
```python
print('PyLadies'[-1])  # → s
print('PyLadies'[-2])  # → e
print('PyLadies'[-3])  # → i
print('PyLadies'[-4])  # → d
```

Negative numbers pick characters from the end.

```plain
   [0] [1] [2] [3] [4] [5] [6] [7]
   [-8][-7][-6][-5][-4][-3][-2][-1]
  ╭───┬───┬───┬───┬───┬───┬───┬───╮
  │ P │ y │ L │ a │ d │ i │ e │ s │
  ╰───┴───┴───┴───┴───┴───┴───┴───╯
```
{% endfilter %}

Strings can do more tricks.
You can find out how long the string is,
or if it contains a certain substring.

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
        <td>True if the string <code>x</code> is in the string <code>r</code></td>
        <td><code>'Ladies' in 'PyLadies'</code></td>
    </tr>
    <tr>
        <td><code>x&nbsp;not&nbsp;in&nbsp;r</code></td>
        <td>The opposite of <code>x in r</code></td>
        <td><code>'eye' not in 'PyLadies</code></td>
    </tr>
</table>

Python is case sensitive, so `ladies in PyLadies`
is `False`. If you want to do a case insensitive test,
you would have to change the case of both strings 
(both to lower, or both to upper) and then do `x in y`.

And how to change the case of our string?
To do that, we will need another Python feature: methods.

## Methods

*Methods* are like functions - we can call something with them.
Unlike a function, a method is tied to some *object* (value).
It is called by writing a colon and a method name just after the object.
And then, of course, parentheses, which may contain arguments.

The String methods `upper()` and `lower()` change the case.

```python
string = 'Hello'
print(string.upper())
print(string.lower())
print(string)
```

> [note]
> Notice that the original string has not changed.
> Methods return a new string and the old string stays
> as it was.
>
> That is Python's standard behavior: already existing string can't be changed,
> we can only create a new one - derived from the old one.


### Initials

For practicing methods and subscripting, try to write a program,
which will ask the user for their name, then their surname
and then it will print their initials - the first letters of
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

There are more ways how to write such a program.
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
useful ones in our [cheatsheet](https://github.com/muzikovam/cheatsheets/blob/master/strings/strings-en.pdf).

All methods are in the [Python documentation](https://docs.python.org/3/library/stdtypes.html#string-methods).

Notice that `len` isn't a method but a function. It's
written `len(s)` not `r.len()`.
You will find out why it is like that in a minute.


## Formatting

Especially useful is the `format` method, which replaces
a pair of curly braces in string for whatever it
gets as an argument.

```python
write = '{}×{} equals {}'.format(3, 4, 3 * 4)
print(write)
```

The String `'{}×{} equals {}'` is something like a *template*.
Imagine it as form, where we have highlighted fields where Python
fills in values.

If you want to fill values in a different order, or you want
the template to be clearer, you can write variables into your
curly braces:

```python
write = 'Hi {name}! The result is {number}.'.format(number=7, name='Mary')
print(write)
```
Formatting is used when you need to include a variable value in
the string.

```python
number = 3 + 4
name = "Mary"
write = 'Hi {}! The result is {}.'.format(name, number)
print(write)
```

It is almost the same as the old fashioned `%s`, but instead of `.format`
you write `%`. If you want to use just one variable, you don't
need parenthesis, just make sure that there is one space after the `%`.

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
`string[5:]` will print the *substring* from the fifth character to the end.
{% endfilter %}

We can also use `string[:5]`, which will select all characters
up to the fifth character, which is not included.
So `string[:5] + string[5:] == string`.


What does `string[2:5]` do?

And what about `string[-4:]`?

```python
string = 'PyLadies'
print(string[:4])
print(string[2:5])
print(string[-4:])
```

You have to think about which number, which *index*, you want to use.

It is better to think of these numbers as being on the borderlines 
between characters, it makes it easier to understand:

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

This function returns a string which inserts the given character into the given
position. The rest is the same as the original `string`.
For example:

```python
change('doctor', 2, 'g') == 'dogtor'
change('slice', 1, 'p') == 'spice'
```

Keep in mind that you can't change a string.
You can only create a new one and put together
pieces from the old one.

{% filter solution %}
```python
def change(string, position, character):
    """This function inserts the given character into the given position.
    
    Returns a new string which has the given character in the given
    position. The rest is the same as the original string.
    """

    return string[:position] + character + string[position + 1:]
```
{% endfilter %}
