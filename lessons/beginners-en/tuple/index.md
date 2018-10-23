# Tuples

Once we know the list, let's look at its sibling: the so-called
*tuples*.

Tuples, like the list,
may contain <var>n</var> elements.
Tuple with two elements is a *pair*; with three
elements it's a *3-tuple* and with four elements
it's a *4-tuple*, etc.

> [note]
> There are tuples with one element
> and with null elements (*empty tuple*),
> but we will not deal with them at the beginning.

Tuples are created as lists, they do not have square brackets around them.
Just the commas between the elements are enough.

They behave almost like lists, but they can not change.
They doesn't have methods like `append`
and `pop` and can not be assigned to elements.
But they can be used in `for` cycle
and they can read individual elements.

```python
people = 'mom', 'aunt', 'grandmother'
for person in people:
    print(person)
print('First is {}'.format(people[0]))
```

> [note]
> Does it look familiar?
> We have already used tuples in
> `for greeting in 'Ahoj', 'Hello', 'Hola', 'Hei', 'SYN'`


If you want to pass a tuple to a function there will be a problem 
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
in fact, only one tuple returns.

```python
def floor_and_remainder(a, b):
    return a//b, a%b
```

> [note]
> This function is in Python by default: it's called
> `divmod` and is always available
> (you don't have to import it).

Python can do another trick: if you want to assign values
into several variables at one time, you can just separate variables (left side)
by a comma and the right side can be some "compound" value - for example
a tuple.

```python
floor_number, remainder = floor_and_remainder(12, 5)
```

A tuple is the best for this purpose, but
it works with all the values ​​that can be used with `for`:

```python
x, o = 'xo'
one, two, three = [1, 2, 3]
```

## Functions returning tuples

`zip` is an interesting function.
It is used in `for` cycles, just like the`range` function that is passing numbers.

When `zip` gets two lists
(or other things applicable in `for`),
it gives back a pairs, the first element of the first list is paired with
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

When `zip` gets three lists it will create triplets and so on.

The other function that returns pairs is `enumerate`.
As an argument, it takes a list (or other thing applicable
with `for`) and always combines the index (order in the list) with the appropriate element.
So the first element will be (0, *first element of the ogiven list*), then
(1, *second element*), (2, *third element*) and so on.

```python
prime_numbers = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]

for i, prime_number in enumerate(prime_numbers):
    print('Prime number on position {} is {}'.format(i, prime_number))
```

## Small tuples

How to create a tuple with none or one element? Like this:

```python
empty_tuple = ()
one_elem_tuple = ('a',)
```


The second example works also without brackets - `one_el_tuple = 'a',`
but it looks like a forgotten comma.
When you *really* need a single-element tuple, 
you'd better encapsulate it for clarity.


## When to use the list and when the tuple?

Lists are used when you do not know in advance
how many values you will have,
or when there are a lot of values.
For example, a list of words in a sentence,
list of contest participants, list of moves in the game
or a list of cards in the package.
On the other hand in `for greeting in 'Ahoj', 'Hello', 'Hola', 'Hei', 'SYN'`
we are using the tuple.

Tuples are often used for values
of different types where each "position"
in tuple has different meaning.
For example, you can use a list for alphabet letters,
but pairs of index-value from `enumerate` will be a tuple.

Empty tuple and one element tuple are a little but strange but they can appear:
for example, a list of playing cards in hand or
list of people currently enrolled in the competition
may occasionally be empty.

Lists and tuples also have technical limits:
tuples can not be changed and when we will learn to work with dictionaries,
we find that lists can't be used as keys.

Often, it is not entirely clear which type to use
- in that case, it probably doesn't really matter.
Follow your instinct. :)