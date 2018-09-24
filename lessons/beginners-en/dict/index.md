# Dictionaries

Another basic data type which we will instroduce is
*dictionary*, abbr. `dict`.

Similar to lists dictionaries contains values inside.
Opposite to lists where all elements are in specific order, there are two types
of elements in dictionaries: *key* and *value*. There exists
exactly one value to every key (I don't want to confuse you right at the beginning
but so you know - empty list can be also value to the key).

You can use dictionary when you have some data each can be somehow named but you want 
to work with them as one variable.

There is a dictionary with 3 keys and each one of them has value:

```pycon
>>> me = {'name': 'Marketa', 'city': 'Prague', 'numbers': [20, 8]}
```

{# XXX - Only visible on Python 3.5 and below. How to teach this?
When you print the dictionary you will probably find out
that keys with values are in different order.
Dictionaries doesn't have order of elements they are just 
assigning values to the keys.
#}

You can get values from the dictionary similar was as
from lists but instead of index you have to use the key. 

```pycon
>>> me['name']
'Marketa'
```

If you would want to work with non-existent key Python won't like it:

```pycon
>>> me['age']
Traceback (most recent call last):
  File "<stdin>", line 1, in &lt;module&gt;
KeyError: 'age'
```

You can also change values with keys.

```pycon
>>> me['numbers'] = [3, 7, 42]
>>> me
{'name': 'Marketa', 'city': 'Prague', 'numbers': [20, 8, 42]}
```

... or add:

```pycon
>>> me['language'] = 'Python'
>>> me
{'name': 'Marketa', 'city': 'Prague', 'numbers': [20, 8, 42], 'language': 'Python'}
```

... or delete wit `del` command (also same as lists):

```pycon
>>> del me['numbers']
>>> me
{'name': 'Marketa', 'city': 'Prague', 'language': 'Python'}
```

## Lookup table

Another use of dictionaries than data clustering is
so-called *lookup table*.
There are values of same type.

This is useful for example with phone book.
For every name there is one phone number.
Or other example is dictionary with words translations.


```python
phones = {
    'Mary': '153 85283',
    'Theresa': '237 26505',
    'Paul': '385 11223',
    'Michael': '491 88047',
}

colours = {
    'pear': 'green',
    'apple': 'red',
    'melon': 'green',
    'plum': 'purple',
    'radish': 'red',
    'cabbage': 'green',
    'carrot': 'orange',
}
```

## Iteration

When you put dictionary into `for` cycle you will get only keys:

```pycon
>>> func_descript = {'len': 'length', 'str': 'string', 'dict': 'dictionary'}
>>> for key in func_descript:
...     print(key)
str
dict
len
```

But when you want to know the values you will have to use the method `values`:

```pycon
>>> for value in func_descript.values():
...     print(value)
string
dictionary
length
```

But mostly you will need both - keys and values.
For this purpose dictionaries have method `items`. 

```pycon
>>> for key, value func_descript.items():
...     print('{}: {}'.format(key, value))
str: string
dict: dictionary
len: length
```

> [note]
> There is also method `keys()` which return just keys.
>
> `keys()`, `values()` and `items()` return special objects
> which can be used in `for` cycle (that's called that those objects are iterable)
> and they behave as set.
> In [documentation](https://docs.python.org/3.0/library/stdtypes.html#dictionary-view-objects)
> is everything well written.

In `for` cycle you can't add keys to dictionary nor delete them:

```pycon
>>> for key in func_descript:
...     del func_descript[key]
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
RuntimeError: dictionary changed size during iteration
```

But you can change values for already existing keys.


## How to create dictionary

Dictionary can be created in two ways.
First way uses square bracket `[]`.
The other way is by using keyword `dict`.
This works similar to `strings`, `integer` or `list`, so it will
convert some specific objects to a dictionary.

Dictionary has very specific structure -
numbers or simple lists can't be converted into dictionary.
But we can convert dictionary into *another dictionary*.
This new dictionary won't be anyhow connected to the
old one.

```python
colour_riped = dict(colours)
for key in colour_riped:
    colour_riped[key] = 'blackish-brownish-' + colour_riped[key]
print(colours['apple'])
print(colour_riped['apple'])
```

We can also convert list which contains tuples with *pairs* (works as key/value) 
into dictionary:

```python
data = [(1, 'one'), (2, 'two'), (3, 'three')]
number_names = dict(data)
```

And that's all what we can convert into a dictionary.

As a bonus function `dict` can also work with named arguments.
Each argument's name will be key and argument itself will be value:


```python
func_descript = dict(len='length', str='string', dict='dictionary')
print(func_descript['len'])
```

> [note]
> Be aware of that in this case keys have to have "pythonic" names – 
> should follow same rules as other Python's variables.
> For example these can't be keys: `"def"`or `"propan-butan"`


## And that's all for now

If you would like to know all the tricks
about dictionaries you can look at (and also print) this [cheatsheet](https://github.com/ehmatthes/pcc/releases/download/v1.0.0/beginners_python_cheat_sheet_pcc_dictionaries.pdf).

Complete description can be foind there in
Python's [documentation](https://docs.python.org/3.0/library/stdtypes.html#mapping-types-dict).

