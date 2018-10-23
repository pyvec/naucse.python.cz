# Tuples

Now that we know about lists, let's look at their sibling: the so-called
*tuples*.

Tuples, just like lists, can contain <var>n</var> elements.
A Tuple with two elements is a *pair*; with three
elements it's a *3-tuple* and with four elements
it's a *4-tuple*, etc.

> [note]
> There are tuples with one element
> and with null elements (*empty tuple*),
> but we will not deal with them at the beginning.

Tuples are created as lists, they do not have square brackets around them.
Just the commas between the elements are enough.

They behave almost like lists, but they cannot change.
They don't have methods like `append`
and `pop`, and cannot be assigned to elements.
But they can be used in `for` loops
and they can read individual elements.

```python
people = 'mom', 'aunt', 'grandmother'
for person in people:
    print(person)
print('First is {}'.format(people[0]))
```

> [note]
> Does this look familiar?
> We have already used tuples in
> `for greeting in 'Ahoj', 'Hello', 'Hola', 'Hei', 'SYN'`


If you want to pass a tuple to a function, there will be a problem 
that a comma separates the individual arguments.
In similar cases, you have to encapsulate the tuple into
brackets to make it clear that it is one value.

```python
list_of_pairs = []
for i in range(10):
    #`append` takes only one argument; we'll give it one pair
    list_of_pairs.append ((i, i ** 2))
print(list_of_pairs)
```

Tuples are useful if you want to return 
more than one value from the function.
You simply declare the return values with a comma between them.
It looks like you're returning a few values, but
in fact, only one tuple is returned.

```python
def floor_and_remainder(a, b):
    return a//b, a%b
```

> [note]
> Such a floor_and_remainder function already exists 
> in Python: it's called `divmod` and it's always 
> available (you don't have to import it).

Python can do another trick: if you want to assign values
into several variables at once, you can just separate the variables 
(the left side) by a comma, and the right side can be some 
"compound" value - for example a tuple.

```python
floor_number, remainder = floor_and_remainder(12, 5)
```

A tuple is the best for this purpose, but
it works with all the values ​​that can be used with a `for` loop:

```python
x, o = 'xo'
one, two, three = [1, 2, 3]
```

## Functions returning tuples

`zip` is an interesting function.
It is used in `for` loops, just like the `range` function that returns numbers.

When `zip` gets two lists (or other values that can be used in a `for` loop),
it returns pairs -- the first element of the first list is paired with
the first element of the second list,
then the second element with the second, the third element with the third and so on.

It is useful when you have two lists with the same
structure - the relevant elements "belong" together
and you want to process them together:

```python
people = 'mom', 'aunt', 'grandmother', 'assassin'
properties = 'good', 'nice', 'kind', 'insidious'
for person, property in zip(people, properties):
    print ('{} is {}'.format(person, property))
```

When `zip` gets three lists it will return triplets, and so on.

The other function that returns pairs is `enumerate`.
As an argument, it takes a list (or other values that can be used in a `for` loop)
and it pairs up the element's index (its order in the list) with the respective element.
So the first element will be (0, *first element of the given list*), then
(1, *second element*), (2, *third element*) and so on.

```python
prime_numbers = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]

for i, prime_number in enumerate(prime_numbers):
    print('Prime number on position {} is {}'.format(i, prime_number))
```

## Small tuples

How to create a tuple with no or one element? Like this:

```python
empty_tuple = ()
one_elem_tuple = ('a',)
```


The second example works also without brackets - `one_el_tuple = 'a',`
but it looks like a forgotten comma.
When you *really* need a single-element tuple, 
you should better encapsulate it for clarity.


## When to use the list and when the tuple?

Lists are used when you do not know in advance
how many values you will have,
or when there are a lot of values.
For example, a list of words in a sentence,
a list of contest participants, a list of moves in a game,
or a list of cards in a deck.
In contrast, in `for greeting in 'Ahoj', 'Hello', 'Hola', 'Hei', 'SYN'`
we are using a tuple.

Tuples are often used for values
of different types where each "position"
inside the tuple has a different meaning.
For example, you can use a list for the letters of the alphabet,
but for pairs of index-value from `enumerate`, you'd use a tuple.

The empty tuple and one-element tuple are a little strange, but they exist:
For example, the list of playing cards in your hand, or the
list of people currently enrolled in the competition
may occasionally be empty.

Lists and tuples also have technical limits:
Tuples cannot be changed, and when we will learn how to work with dictionaries,
we will find that lists cannot be used as dictionary keys.

Often, it is not entirely obvious which type to use
-- in that case, it probably doesn't really matter.
Follow your instinct. :)
