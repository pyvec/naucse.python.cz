This chapter is full of new things. Hang in there! 
If anything doesn't make sense now, don't worry:
What we explain now will teach you important
things we will use in another lesson.

Try each example in this lesson;
what Python prints is an important part of the lesson.

# Lists

Today we will show you how to work with *lists*.
We will use square brackets a lot because that's how lists are created:

```python
numbers = [1, 1, 2, 3, 5, 8, 13]
print(numbers)
```


A list is a value that can contain many other values.
Just like a string contains a sequence of characters,
a list contains a sequence of anything. Numbers, for example.
And just as we can use the `for` loop
to print strings character by character,
we can loop over list elements:

```python
for number in numbers:
    print(number)
```

Lists in programs are very common:
A file can be retrieved as a list of strings
line by line.
A list of strings like `7 ♥`
and `K ♣` can be used as a deck of cards.
Math is full of numerical lists and
each online service has a list of users.


The values ​​in a list can be of any type,
we can even mix different types in one list
(even though we won't meet such mixed lists
very often - they are more used in tuples,
which we will tell you about later):

```python
list = [1, 'abc', True, None, range(10), len]
print(list)
```

## Selection from lists

Yo already know the most basic operation with lists, 
the `for` loop.
The second most important operation is picking
individual elements.
This works the same way as in strings: square brackets and
the element number. List elements are numbered from zero, 
just as characters in strings; negative numbers indicate elements from the end.

```python
print(numbers[2])
```

We use square brackets to access subsets.
[Strings Chart] ({{lesson_url ('beginners-en/str')}} # slicing-diagram)
shows you how to write the numbers when you want parts of the list:

```python
print(numbers[2:-3])
```

## Changing lists

An important feature of lists, that neither numbers nor strings
(nor `True`/`False`/`None`) have, is
that lists can be changed.

Numbers can't be changed - if you have `a = 3` and
you write `a = a + 1`, the number `3` will not change.
A new number `4` will be calculated, and the variable `a`
will be set to this new number.

By contrast, lists can be changed without setting a variable to a new value.
The most basic way to change a list is to add elements
to its end, using the `append` method.
Doing this doesn't return *anything* (actually it returns `None`)
but it changes the list we are working on *in place*  (`append` means 
add to *the end* of the list). Try it:

```python
prime_numbers = [2, 3, 5, 7, 11, 13, 17]
print(prime_numbers)
prime_numbers.append(19)
print(prime_numbers)
```

Such a value change can sometimes be surprising,
because multiple variables can have the same value.
Because the value itself changes, it may seem
that the variable "changes without us touching it":

```python
a = [1, 2, 3] # creates a list 'a'
b = a         # no new list is created, 'b' just points to 'a'

# the list created in the first row now has two variable names: "a" and "b",
# but we are still working with just one and the same list:

print(b)
a.append(4)
print(b)
```

## More ways to edit lists

Apart from the `append` method that adds
only one element, there is also the `extend` method,
which can add more elements.
The elements to be added here are in the form of a list:

```python
more_prime_nr = [23, 29, 31]
prime_numbers.extend(more_prime_nr)
print(primary)
```

The `extend` method can work with other
types of variables - it can work with anything on which
we can use a `for` loop: For example,
individual strings, rows of files, or numbers from `range()`.

```python
listA = []
listA.extend('abcdef')
listA.extend(range(10))
print(listA)
```

## Changing elements

But enough adding.
You can change individual elements of lists,
simply by assigning a value to the element,
as if it were a variable:

```python
numbers = [1, 0, 3, 4]
numbers[1] = 2
print(numbers)
```

You can also assign new values to a sublist - in this case
the subset is replaced by the individual values we write.
Like with `extend`, you can replace the elements with anything 
that works with `for` loops - list, string, `range()`, etc.

```python
numbers = [1, 2, 3, 4]
numbers[1:-1] = [6, 5]
print(numbers)
```

## Deleting elements

We can also change the length of the
list by replacing a sublist with fewer elements,
or by removing some of the elements completely:

```python
numbers = [1, 2, 3, 4]
numbers[1:-1] = [0, 0, 0, 0, 0]
print(numbers)
numbers[1:-1] = []
print(numbers)
```

This form of deleting elements is quite obscure,
therefore we have a special command named `del`.
It deletes everything that we tell it to - individual
elements, sublists and even variables!

```python
numbers = [1, 2, 3, 4, 5, 6]
del numbers[-1]
print(numbers)
del numbers[3:5]
print(numbers)
del numbers
print(numbers)
```

Other deleting methods are:
* `pop`, which removes *and returns* the last element in the list - for example, if
  I have a list of cards in a deck, `pop` is like "drawing a card".
* `remove`, which finds the element in the list and removes it,
* `clear`, which clears the entire list.

```python
numbers = [1, 2, 3, 'abc', 4, 5, 6, 12]
last = numbers.pop()
print(last)
print(numbers)

numbers.remove('abc')
print(numbers)

numbers.clear()
print(numbers)
```

## Sorting

And we also have a `sort` method that sorts list elements.

```python
listA = [4, 7, 8, 3, 5, 2, 4, 8, 5]
listA.sort()
print(listA)
```

In order to be sorted, the elements of the list must be
*comparable* - we have to be able to use the `<` operator with them.
A mixed list of numbers and strings cannot be sorted.
The operator `<` defines how exactly the elements will
be sorted (e.g., numbers by size; strings according to the special "alphabet"
where upper case is smaller than lower case, etc.).

The `sort` method has a `reverse` argument. 
If you set it to *True*, it will sort the elements in backwards order.
The default value is *False*, so if you want the elements to be
sorted from smaller to larger, you don't have to specify this argument.

```python
listA = [4, 7, 8, 3, 5, 2, 4, 8, 5]
listA.sort(reverse=True)
print(listA)
```

## Other methods

Lots of what we can do with strings, we can also do with lists.
For example adding and multiplying:

```python
melody = ['C', 'E', 'G'] * 2 + ['E', 'E', 'D', 'E', 'F', 'D'] * 2 + ['E', 'D', 'C']
print(melody)
```

As with strings, the list can be added only to other lists
- not to a string or to a number.

Other known methods are `len`, `count`, and` index`,
and the `in` operator.

```python
print(len(melody)) # Length of the list
print(melody.count('E')) # How many 'E's are in the list?
print(melodie.index('E')) # Position of the first 'E'
print('E' in melody) # Is 'E' in the list?
```

The last three methods work a little bit differently:
for strings they are work on *substrings*,
for lists they work on *individual* elements.
So although our melody contains the elements
`D` and ` E` next to each other, `DE` is not in the list:

```python
print('DE' in melody)
print(melody.count('DE'))
print(melody.index('DE'))
```

## A list as a condition

A list can be used in an `if` (or` while`) statement
which is true while there is something in that list.
In other words, `list` is an 'abbreviation' for `len(list) > 0`.

```python
if list:
    print ('There is something in the list!')
else:
    print ('The list is empty!')
```

Strings can be used similarly.
And even numbers - the condition is *True* if they are not zero.

## Creating lists

Just like the `int` function converts values to
integers and `str` converts values to strings,
the `list` function converts values to a list.
As an argument, we can give it any value,
which can be processed by a `for` loop.
A string will turn into a list of characters, a file
will turn into a list of rows, a `range` will turn 
into a list of numbers.

```python
alphabet = list('abcdefghijklmnopqrstuvwxyz')
numbers = list(range(100))
print(alphabet)
print(numbers)
```

The `list` function can also create a list from a list.
It may sound useless, but it isn't - it creates a *new* list that
is not dependent on the old list.
It will contain the same elements in the same order,
but it will not be the same list:
You can change it independently of the old one.

```python
a = [1, 2, 3]
b = list(a)

print(b)
a.append(4)
print(b)
```

Another way to create lists
(especially more complex lists) is to first make an empty
list, and then fill it up using the `append` function.
For example, if you want a list with numbers that are
powers of two, pass the numbers into a `for` loop, and 
for each number, add the appropriate power to the list:

```python
power_of_two = []
for number in range (10):
    power_of_two.append (2 ** number)
print(power_of_two)
```

If you want a list that represents a deck of cards,
call `append` for all combinations of color and value.

```python
deck = []
for color in '♠', '♥', '♦', '♣': # (Use text names on Windows)
    for value in list(range(2, 11)) + ['J', 'Q', 'K', 'A']:
        deck.append(str(value) + color)
print(deck)
```

## Lists and Strings

Lists and strings are types of "sequences",
so it is not surprising that they can be converted
from one type to another.
The `list` function creates a list of characters from a string.
If we want to get a list of words, we use the `split` method on a sentence:

```python
words = 'This sentence is complex, split it into words!'.split()
print(words)
```

The `split` method can also take an argument.
If we pass it a separator character, the string is "cut" 
at this given separator, instead of at spaces (and new lines).
So, when we have some data separated by commas,
there is nothing easier than using `split` with a comma argument:

```python
records = '3A, 8B, 2E, 9D'.split(',')
print(records)
```

If we want to join a list of strings into
a single string, we use the method `join`.
Note that this method is called on the *delimiter* character that we want to use
between the elements of a list, and as an argument, it takes the list.

```python
sentence = ' '.join(words)
print(sentence)
```

## Task

Imagine that users enter their names and surnames, and you store them in
a list for future use, for instance, student records. 
Not all users are careful when entering their names,
so the names can appear with incorrectly capitalized letters.
For example:

```python
records = ['john doe', 'John Smith', 'Stuart little', 'petr File']
```

Your task is:

* Write a function that selects only those correctly entered entries where
the first letters of the first name and last name are capitalized.
* Write a function that selects only the incorrectly entered records.
* *(Optional)* - Write a function that returns a list with corrected records.

The result should look like this:

```python
records = ['john doe', 'John Smith', 'Stuart little', 'petr File']

error_entries = select_errors(records)
print(error_entries) # → ['john doe', 'Stuart little', 'petr File']

ok_entries = select_correct(records)
print(ok_entries) # → ['John Smith']

corected_entries = correct_entries(records)
print(corected_entries) # → ['John Doe', 'John Smith', 'Stuart Little', 'Petr File']
```

> [note]
> An easy way to find out if the string is written in lower case,
> is the `islower()` method, which returns True if the string contains only lower
> case letters, otherwise it returns False. For example, `'abc'.islower() == True` but
> `'aBc'.islower() == False`.
>
> The easiest way to convert first letters to upper case is `capitalize()`:
> `'abc'.capitalize() == 'Abc'`

{% filter solution%}
```python
def select_errors(listA):
    result = []
    for record in listA:
        name_surname = record.split(' ')
        name = name_surname[0]
        surname = name_surname[1]
        if name[0].islower() or surname[0].islower():
            result.append(record)
    return result

def select_correct(listA):
    result = []
    for record in listA:
        name_surname = record.split(' ')
        name = name_surname[0]
        surname = name_surname[1]
        if not name[0].islower() and not surname[0].islower():
            result.append(record)
    return result

def correct_entries(listA):
    result = []
    for record in listA:
        name_surname = record.split(' ')
        name = name_surname[0]
        surname = name_surname[1]
        result.append(name.capitalize() + ' ' + surname.capitalize())
    return result
```
{% endfilter%}

## Lists and random

The `random` module contains two functions that can be used with lists.

First, the `shuffle` function shuffles elements - all elements are left in a random order.
Just like `sort`, `shuffle` does not return anything.

```python
import random

deck = []
for color in '♠', '♥', '♦', '♣':
    for value in list(range(2, 11)) + ['J', 'Q', 'K', 'A']:
        deck.append(str(value) + color)
print(deck)

random.shuffle(deck)
print(deck)
```

The second one is the `choice` function that selects a random element from the list.
Using a list, it's much easier to implement rock/paper/scissors:

```python
import random
possibilities = ['rock', 'scissors', 'paper']
pc_choice = random.choice(possibilities)
```

## Nested lists

In the beginning of this lesson we said that a list
can contain any type of value.
A list can even contain other lists:

```python
list_of_lists = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
```

Such a list behaves as expected - we can choose
elements (which are, of course, lists):

```python
first_list = list_of_lista[0]
print(first_list)
```

And since elements are themselves lists,
we can talk about elements like "the first element of the second list":

```python
second_list = list_of_lists[1]
first_element_of_second_list = second_list[0]
print(first_element_of_second_list)
```

And because `list_of_lists[1]`
indicates the list, we can take the elements directly from it:

```python
first_element_of_second_list = (list_of_list[1])[0]
```

Or:

```python
first_element_of_second_list = list_of_list[1][0]
```

This approach is quite useful.
Same as nested `for` loops
allowed us to list a table, nested lists
allow us to store a table.

```python
def create_tab(size=11):
    row_list = []
    for a in range(size):
        row = []
        for b in range(size):
            row.append(a * b)
        row_list.append(row)
    return row_list

multiplication_tab = create_tab()

print(multiplication_tab[2][3]) # two times three
print(multiplication_tab[5][2]) # five times two
print(multiplication_tab[8][7]) # eight times seven

# List the entire table
for row in multiplication_tab:
    for number in row:
        print(number, end = '')
    print()
```

What can we do with such a stored table? For example,
you can save the positions of figures on a chessboard, 
or of the crosses and circles in a *2D* tictactoe.
