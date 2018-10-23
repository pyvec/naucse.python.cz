
This chapter is full of new things.
I hope you can hold on to the end. And if anything
doesn't make sense now, don't lose your head:
the things we will explain now will really teach you
things we will use in another lesson.

Try each example in this lesson;
what Python prints is an important part of the lesson.

# Lists

Today we will show you how to work with *lists*.
We will use square brackets a lot because that's how are lists created:

`` `python
numbers = [1, 1, 2, 3, 5, 8, 13]
print (numbers)
`` `


The list is a value that can contain many other values.
As the string contains a sequence of characters,
the list contains a sequence of anything. Numbers, for example.
And just as we can use the `for` cycle
to print strings after the characters,
we can go through the following elements:

`` `python
for number in numbers:
    print (number)
`` `

Lists in programs are very common:
the file can be retrieved as a list of strings
with single lines.
A list of strings like `7 ♥`
and `K ♣` can be used as a pack of cards.
Math is full of numerical lists and
each online service has a list of users.


The values ​​in the list can be of any type,
we can even mix different types in one list
(even though we won't meet such mixed lists
very often - they are more used in tuples
,which we'll tell you later):

`` `python
list = [1, 'abc', True, None, range(10), len]
print(list)
`` `

## Selection from lists

The most basic operation with lists,the `for`
cycle, we have already learned.
The second most important operation is picking
of individual elements.
This works like in strings: square brackets and
the element number. It is numbered, as with strings,
from zero; negative numbers indicate the elements from the end.

`` `python
print(numbers[2])
`` `

We can get subsections with square brackets.
[Strings Chart] ({{lesson_url ('beginners-en/str')}} # slicing-diagram)
shows how to write numbers when we want smaller list:

`` `python
print(numbers[2:-3])
`` `

## Changing lists

An important feature of lists that neither numbers nor strings
(nor `True`/`False`/`None`) doesn't have is
that lists can be changed.

Numbers can't be changed - if you have `a = 3` and
you write `a = a + 1`, the number `3` will not change.
There will be calculated new number `4` and the variable` a`
will be set to this new number.

By contrast, lists can be changed without setting a variable to new value.
The basic way to change a list is to add
to the end using the `append` method.
That doesn't return *anything* (actually it returns `None`)
but it changes the list *in place* we are working on (`append` is changing the list
in *the last place*). Try it:

`` `python
prime_numbers = [2, 3, 5, 7, 11, 13, 17]
print(prime_numbers)
prime_numbers.append(19)
print(prime_numbers)
`` `

Such a change of value can sometimes be surprising,
because multiple variables can have the same value.
Because the value itself changes, it may seem,
that the variable "changes without we touching it":

```python
a = [1, 2, 3] # creates a list
b = a         # here the new list is not created, it just points to 'a' list

# the list created in the first row now has two variable names: "a" and "b",
# but we are still working with just one list

print(b)
a.append(4)
print(b)
```

## More ways to edit lists

Except for the `append` method that adds
only one element, there is the `extend` method,
which can add more elements.
The elements to be added here are in the form of a list:

`` `python
more_prime_nr = [23, 29, 31]
prime_numbers.extend(more_prime_nr)
print(primary)
`` `

The `extend` method can work with other
types of variables - it can work with anything where
we can use `for` cycle: eg.
individual strings, rows of files, or numbers from `range()`.

```python
listA = []
listA.extend('abcdef')
listA.extend(range(10))
print(listA)
```

## Changing elements

But enough adding.
Lists can also be used to change individual elements
simply by assigning a value to the element,
as if it was a variable:

```python
numbers = [1, 0, 3, 4]
numbers[1] = 2
print(numbers)
```

You can also assign new values to the sublist - in this case
the subsection is replaced by the individual values we write.
Like with `extend`, you can replace the elements with anything 
that works with `for` cycles - list, string,`range()`, etc.

```python
numbers = [1, 2, 3, 4]
numbers[1:-1] = [6, 5]
print(numbers)
```

## Deleting elements

We can also change the length of the
list by replacing sublist with less elements
or remove some of the elements completely:

```python
numbers = [1, 2, 3, 4]
numbers[1:-1] = [0, 0, 0, 0, 0]
print(numbers)
numbers[1:-1] = []
print(numbers)
```

This form of deleting the elements is quite
unclear, and therefore we have a special command
named `del`.
It deletes everything that we tell him to - individual
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
  I have a list of cards in the pack, it's like a "draw"
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

And we also have the `sort` method that sorts the list elements.

```python
listA = [4, 7, 8, 3, 5, 2, 4, 8, 5]
listA.sort()
print(listA)
```

In order to sort, the elements of the list must be
*comparable* - we have to be able to put between them the operator `<`.
The mixed list of numbers and strings can not be sorted.
The operator `<` defines how exactly the elements will
be sorted (e.g. numbers by size; string according to the special "alphabet"
where are upper case smaller than lower case, etc.).

The `sort` method has an argument
`reverse`. If you set it to *True*, it will sort elements "vice versa".
The default value is *False* so if you want the elements to be
sorted from smaller you don't have to specify this argument.

```python
listA = [4, 7, 8, 3, 5, 2, 4, 8, 5]
listA.sort(reverse=True)
print(listA)
```

## Other methods

Lots of what we can do with strings we can also do with lists.
For example adding and multiplying:

```python
melody = ['C', 'E', 'G'] * 2 + ['E', 'E', 'D', 'E', 'F', 'D'] * 2 + ['E', 'D', 'C']
print(melody)
```

As with strings, the list can be added only to another lists
- not to a string or a number.

Other known methods are `len`,
`count` and` index` and `in` operator.

```python
print(len(melody)) # Length of the list
print(melody.count('E')) # How many 'E's are in the list
print(melodie.index('E')) # Number of the first 'E'
print('E' in melody) # Is 'E' in the list?
```

The last three methods are working bit differently:
for strings they are working with *substrings*,
for lists  they are working with *individual* elements.
So although our melody contains elements
`D` and ` E` next to each other, `DE` is not in the list:

```python
print('DE' in melody)
print(melody.count('DE'))
print(melody.index('DE'))
```

## A list as a condition

The list can be used in the `if` (or` while`) statement
which is true when there is something in that list.
In other words, `list` is an 'abbreviation' for `len (list)> 0`.

```python
if list:
    print ('There is something in the list!')
else:
    print ('The list is empty!')
```

Strings can be used similarly.
And even numbers - the condition is *True* if they are nonzero.

## Creating lists

Just like the `int` function converts to
integers and `str` to strings,
the `list` function converts to a list.
As an argument, we can give it any value,
which can be processed by `for` loop.
A string will make a list of characters, a file
will make a list of rows, a `range` will make a
list of numbers.

```python
alphabet = list('abcdefghijklmnopqrstuvwxyz')
numbers = list(range(100))
print(alphabet)
print(numbers)
```

The `list` function can also create a list from a list.
It may sound useless, but it is not - it creates a *new* list with value that
is not dependent on the old list.
It will have the same elements in the same order,
but it will not be the same list:
it will change independently to the old one.

```python
a = [1, 2, 3]
b = list(a)

print(b)
a.append(4)
print(b)
```

Another way to create lists
(especially more complex) is first made empty
list and then fill it up with the `append` function.
For example if you want a list with numbers that are
powered to two, pass the numbers in `for` cycle and for each of them
add the appropriate power to the list:

```python
power_of_two = []
for number in range (10):
    power_of_two.append (2 ** number)
print(power_of_two)
```

If you want a list that represents a package of cards,
call `append` for all combinations of color and value.

```python
package = []
for color in '♠', '♥', '♦', '♣': # (Use text names on Windows)
    for value in list(range(2, 11)) + ['J', 'Q', 'K', 'A']:
        package.append(str(value) + color)
print(package)
```

## Lists and Strings

Lists and strings are types of "sequences"
so it is not surprising that it can be converted
from one type to another.
The `list` function creates a list of characters from a string.
If we want to get a list of words, we'll use `split` method on sentence:

```python
words = 'This sentence is complex, split it into words!'.split()
print(words)
```

The `split` method can also take an argument.
If we pass it, instead of spaces (and new lines)
the string is "cuted" by the given separator.
So when we have some data separated by commas,
there is nothing easier than using `split` with a comma argument:

```python
records = '3A, 8B, 2E, 9D'.split(',')
print(records)
```

If we want to join a list of strings into
a single string, we use the method `join`.
Note that this method is called on *delimiter* we want to use
between the elements of a list, and as an argument it takes the list.

```python
sentence = ' '.join(words)
print(sentence)
```

## Task

Imagine that users enter their names and surnames for you and you store them in
the list for future use, e.g. student records. Not all are careful about what they are entering their names,
so the names can appear with incorrectly capitalized letters.
For example:

```python
records = ['john doe', 'John Smith', 'Stuart little', 'petr File']
```

The task is:

* Write a function that selects only those correctly entered entries that has
first name and last name with first letter capitalized.
* Write a function that selects only the incorrectly entered records.
* *(Optional)* - Write a function that returns a list of corrected records.

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
> The easy way to convert the first letter to upper case is `capitalize()`:
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

The `random` module contains two functions that can be used with the lists.

First the `shuffle` function shuffles elements - all elements are randomly discarded.
As `sort`, `shuffle` does not return anything.

```python
import random

package = []
for color in '♠', '♥', '♦', '♣':
    for value in list(range(2, 11)) + ['J', 'Q', 'K', 'A']:
        package.append(str(value) + color)
print(package)

random.shuffle(package)
print(package)
```

Second is the `choice` function that selects a random element from the list.
By using the list, we can make rock/paper/scissors much easier:

```python
import random
possibilities = ['rock', 'scissors', 'paper']
pc_choise = random.choice(possibilities)
```

## Nested lists

In the beginning of this lesson we said that list
can contain any type of value.
It can contain also another lists.

```python
list_of_lists = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
```

Such a list behaves quite usually - we can choose
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

This approach also has some use.
Same as nested `for` cycles
allowed us to list a table, nested lists
will allow us to "remember" the table.

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

What to do with such "memorized" table?
You can save positions of figures on a chessboard 
or crosses and circles in *2D* tictactoes.
