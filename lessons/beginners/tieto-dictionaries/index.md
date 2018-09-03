## Dictionaries

Dictionaries is data structure, in which each value has it§s own name. This type of structure is called a mapping.

Dictionaries are constructed to be easilly searchable based on it's key.

A dictionary is more appropriate than a list in some situations.


* Storing file modification times, with file names as keys

* Address book

For example list of people:

```
>>> names = ['Alice', 'Beth', 'Cecil', 'Dee-Dee', 'Earl']     
```

In case that you would like to store telephone number of users using list, you would have to create second list with numbers under same index as user name:

```
>>> numbers = ['2341', '9102', '3158', '0142', '5551']              
```

And lookup for user phone like this:

```
>>> numbers[names.index('Alice')]
'2341'
```

As you can see, it's not straightforward. You can use dictionay instead in such case.

```
phonebook = {'Alice': '2341', 'Beth': '9102', 'Cecil': '3258'}
```

Dictionaries consist of pairs of keys and their corresponding values.

You can create empty dictionary like this:

```
new_dictionary = {}
```

> [note]
> Keys are unique within a dictionary!


### The dict() function

You can use dict function() to construct dictionary from other sequences like this:

```
>>> items = [('name', 'Gumby'), ('age', 42)]                
>>> d = dict(items)                
>>> d                
{'age': 42, 'name': 'Gumby'}                
>>> d['name']                
'Gumby'                
```

You can also use *keywoard argument*:

```
>>> d = dict(name='Gumby', age=42)                
>>> d                
{'age': 42, 'name': 'Gumby'}
```

### Basic dictionary operations

* **len(d)** - returns the number of items (key-value pairs)
* **d[k]** - returns the value associated with the key k
* **d[k] = v**  - associates the value v with the key k
* **del d[k]** - deletes the item with key k
* **k in d** - checks whether there is an item in d that has the key k

```
# A simple database

# A dictionary with person names as keys. Each person is represented as
# another dictionary with the keys 'phone' and 'addr' referring to their phone
# number and address, respectively.
people = {

    'Alice': {
        'phone': '2341',
        'addr': 'Foo drive 23'
    },

    'Beth': {
        'phone': '9102',
        'addr': 'Bar street 42'
    },

    'Cecil': {
        'phone': '3158',
        'addr': 'Baz avenue 90'
    }

}

# Descriptive labels for the phone number and address. These will be used
# when printing the output.
labels = {
    'phone': 'phone number',
    'addr': 'address'
}

name = input('Name: ')

# Are we looking for a phone number or an address?
request = input('Phone number (p) or address (a)? ')

# Use the correct key:
if request == 'p': key = 'phone'
if request == 'a': key = 'addr'

# Only try to print information if the name is a valid key in                                                
# our dictionary:
if name in people: print("{}'s {} is {}.".format(name, labels[key], people[name][key]))
```

### String formatting with dictionaries

The dictionary may contain all kinds of information, and your format string will only pick out whatever it needs.

```
>>> phonebook
{'Beth': '9102', 'Alice': '2341', 'Cecil': '3258'}
>>> "Cecil's phone number is {Cecil}.".format_map(phonebook)
"Cecil's phone number is 3258."
```
Another example:

```
>>> template = '''<html>
... <head><title>{title}</title></head>
... <body>
... <h1>{title}</h1>
... <p>{text}</p>
... </body>'''
>>> data = {'title': 'My Home Page', 'text': 'Welcome to my home page!'}
>>> print(template.format_map(data))
<html>
<head><title>My Home Page</title></head>
<body>
<h1>My Home Page</h1>
<p>Welcome to my home page!</p>
</body>
```

### Dictionary methods

**clear()**

The clear method removes all items from the dictionary. This is an in-place operation.

```
>>> d = {}
>>> d['name'] = 'Gumby'
>>> d['age'] = 42
>>> d
{'age': 42, 'name': 'Gumby'}
>>> returned_value = d.clear()
>>> d
{}
>>> print(returned_value)
None
```

Why don't erase dictionary simply like this?

```
>>> x = {}
>>> x[1] = 'one'
>>> x
{1: 'one'}
>>>
>>> x = {}
>>> x
{}
```

Sometimes you want also delete all referenced objects values as well:

```
>>> x = {}
>>> y = x
>>> x['key'] = 'value'
>>> y
{'key': 'value'}
>>> x = {}
>>> x = {}
{'key': 'value'}
```

vs.

```
>>> x = {}
>>> y = x
>>> x['key'] = 'value'
>>> y
{'key': 'value'}
>>> x.clear()
>>> y
{}
```

**copy()**

The copy method returns a new dictionary with the same key-value pairs (shallow copy).

```
>>> x = {'username': 'admin', 'machines': ['foo', 'bar', 'baz']}
>>> y = x.copy()
>>> y['username'] = 'mlh'
>>> y['machines'].remove('bar')
>>> y
{'username': 'mlh', 'machines': ['foo', 'baz']}
>>> x
{'username': 'admin', 'machines': ['foo', 'baz']}
```

**deepcopy()**

```
>>> from copy import deepcopy
>>> d = {}
>>> d['names'] = ['Alfred', 'Bertrand']
>>> c = d.copy()
>>> dc = deepcopy(d)
>>> d['names'].append('Clive')
>>> c
{'names': ['Alfred', 'Bertrand', 'Clive']}
>>> dc
{'names': ['Alfred', 'Bertrand']}
```

**get()**

 Ordinarily, when you try to access an item that is not present in the dictionary, things go very wrong .
 
```
>>> d = {}
>>> print(d['name'])
Traceback (most recent call last):
  File "<stdin>", line 1, in ?
KeyError: 'name'
```

Get, on the other side:

```
>>> print(d.get('name'))
None
```

**items()**

The items method returns all the items of the dictionary as a list of items in which each item is of the form (key, value).

```
>>> d = {'title': 'Python Web Site', 'url': 'http://www.python.org', 'spam': 0}
>>> d.items()
dict_items([('url', 'http://www.python.org'), ('spam', 0), ('title', 'Python Web Site')])
```

**keys()**

The keys method returns a dictionary view of the keys in the dictionary .

**pop()**

The pop method can be used to get the value corresponding to a given key and then to remove the key-value pair from the dictionary .

```
>>> d = {'x': 1, 'y': 2}
>>> d.pop('x')
1
>>> d
{'y': 2}
```

**values()**

The values method returns a dictionary view of the values in the dictionary. Unlike keys, the view returned by values may contain duplicates .

```
>>> d = {}
>>> d[1] = 1
>>> d[2] = 2
>>> d[3] = 3
>>> d[4] = 1
>>> d.values()
dict_values([1, 2, 3, 1])
```