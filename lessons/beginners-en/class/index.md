# Objects and values

Before we start with classes, we will learn about objects.

What does *object* mean for programmers?

It's actually easy with Python - every value (that's something you can "store"
into a variable) is an object.
Some programming languages (e.g. JavaScript, C++, Java) also have 
values other than objects. And for example C doesn't have objects at all.
But in Python there is no difference between value and object, so
it's a little bit difficult to understand. On the other hand, you don't have
to know the details.

The basic attribute of objects is that they contain data (information) and *behaviour* -
instructions and/or methods how to work with data.
For example, strings contain information (a sequence of characters) as well as
useful methods such as `upper` and `count`.
If strings were not objects, Python would have to have a lot more
functions, such as `str_upper` and `str_count`.
Objects connect data and functionality together.


> [note]
> You will maybe say that, for example, `len` is a function, and you will be correct.
> Python is not 100% an object oriented language.
> But the function `len` also works on objects which do not have anything in common with strings.


# Classes

The data of each object is specific for each concrete object
(e.g. `"abc"` contains different characters than `"def"`),
but the functionality - the methods - are the same for all objects of the same 
type (class). For example, the string method `count()` could be
written like this:


```python
def count(string, character):
    sum = 0
    for c in string:
        if c == character:
            sum = sum + 1
    return sum
```

And although a different string will return a different value,
the method itself is same for all strings.

This common behaviour is defined by the *type* or *class* of the object. 


> [note]
> In previous versions of Python there was a difference between "type"
> and "class", but now they are synonyms.

You can find out type of an object by using the function `type`:


```pycon
>>> type(0)
<class 'int'>
>>> type(True)
<class 'bool'>
>>> type("abc")
<class 'str'>
>>> with open('file.txt') as f:
...     type(f)
... 
<class '_io.TextIOWrapper'>
```

The function `type` returns some classes.
What is a class? It's a description how every object of the same type
behaves.

Most of the classes in Python are callable as if they were functions. 
This following code will create an object of the class we called:

```pycon
>>> string_class = type("abc")
>>> string_class(8)
'8'
>>> string_class([1, 2, 3])
'[1, 2, 3]'
```

So it's behaving as the function `str`! Isn't it strange?

Now I have to apologise:
[materials for functions](../functions/)
lied a bit. Functions `str`, `int`, `float`, etc., are actually classes.

```pycon
>>> str
<class 'str'>
>>> type('abcdefgh')
<class 'str'>
>>> type('abcdefgh') == str
True
```

But we can call them as if they were functions.
So classes contain not only the "description" how object of the class
will behave, but they can also create objects.


## Custom classes

Now we will try to create our own class.

Writing custom classes is useful when you want to use different objects 
with similar behaviour in your program.
For example, a card game could have Card class, a web application could 
have a User class, and a spreadsheet application could have Row class.

Let's write a program that handles animals.
First, you create a Kittie class which can meow:


```python
class Kittie:
    def meow(self):
        print("Meow!")
```

Just as a function is defined by the `def` keyword, classes are
defined by the `class` keyword. Then of course you have to continue with a colon
and indentation of the class body.
Similar as `def` creates a function, `class` creates a class and assigns it to the 
name of the class (in our example to `Kittie`).

It's a convention that classes are named with an uppercase first letter so they
are not easily confused with "normal" variables.


> [note]
> Basic classes (`str`, `int`, etc.)
> don't start with an uppercase letter because of historic
> reasons – originally they were really functions.

In the class body, you define methods, which looks like functions.
The difference is that class methods have `self` as the first argument,
which we will explain later - meowing comes first:

```python
# Creation of the object
kittie = Kittie()

# Calling the method
kittie.meow()
```

In this case you have to be really careful about uppercase letters:
`Kittie` (with uppercase K) is the class - the description how kitties behave.
`kittie` (lowercase k) is the object (an *instance*) of the Kittie class:
a variable that represents a Kittie.
That object is created by calling the class (same as we
can create a string by calling `str()`).

Meow!

## Attributes 

Objects that are created from custom classes have one feature that
classes like `str` don't allow: The ability to define class *attributes* -
information that is stored by the instance of the class.
You can recognise attributes by the period between class instance and the name of its attribute.


```python
smokey = Kittie()
smokey.name = 'Smokey'

misty = Kittie()
misty.name = 'Misty'

print(smokey.name)
print(misty.name)
```

In the beginning we said that objects are connecting behaviour with data.
Behaviour is defined in the class, data is stored in attributes.
We can differentiate Kitties, for example, by their names because of the attributes.

> [note]
> By using a period after a class object, you can access the class methods 
> as well as its attributes.
> What happens if an attribute has the same name as method?
> Try it!
>
> ```python
> misty = Kittie()
> misty.meow = 12345
> misty.meow()
> ```

## Parameter `self`

Now we will briefly go back to methods, to be specific, we will go back
to the parameter `self`.

Each method has access to any specific object that it's working on just because of
parameter `self`.
Now after you have named your kitties, you can use the `self` parameter to add the name to meowing.


```python
class Kittie:
    def meow(self):
        print("{}: Meow!".format(self.name))

smokey = Kittie()
smokey.name = 'Smokey'

misty = Kittie()
misty.name = 'Misty'

smokey.meow()
misty.meow()
```

What just happened? The command `smokey.meow` called a *method* which when it's called assigns the object
`smokey` as first argument to the function `meow`.

> [note]
> This is how a *method* is different from a *function*:
> A method "remembers" the object it is working on.

And that first argument which contains a specific object of the just created class is
usually called `self`.
You can of course call it differently, but other programmers will not like you. :)

Can such a method take more that one argument?
It can - in that case, `self` will be substituted as the first argument,
and the rest of the arguments will be taken from how you called the method.
For example:

```python
class Kittie:
    def meow(self):
        print("{}: Meow!".format(self.name))

    def eat(self, food):
        print("{}: Meow meow! I like {} very much!".format(self.name, food))

smokey = Kittie()
smokey.name = 'Smokey'
smokey.eat('fish')
```

## Method `__init__`

There is another place where you can pass arguments to the class:
when you create a new object (calling the class).
You can easily solve the problem that you might see in the previous code:
After the kittie object is created, you must add a name so the method
`meow` can work.

You can also create classes by passing parameters when you are calling it:

```python
smokey = Kittie(name='Smokey')
```
Python uses the `__init__` method (2 underscores, `init`, 2 underscores) for this option.
Those underscores indicate that this method name is somehow special. The method `__init__`
is actually called right when the object is being created, or in other words - when it's
being initialized (`init` stands for *initialization*).
So you can write it like this:

```python
class Kittie:
    def __init__(self, name):
        self.name = name

    def meow(self):
        print("{}: Meow!".format(self.name))

    def eat(self, food):
        print("{}: Meow meow! I like {} very much!".format(self.name, food))

smokey = Kittie('Smokey')
smokey.meow()
```

And now there is no possibility to create a kittie without a name,
and `meow` will work all the time.

There are many more methods with underscores, e.g. the `__str__`
method is called when you need to convert the object into a string:

```python
class Kittie:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return '<Kittie named {}>'.format(self.name)

    def meow(self):
        print("{}: Meow!".format(self.name))

    def eat(self, food):
        print("{}: Meow meow! I like {} very much!".format(self.name, food))

smokey = Kittie('Smokey')
print(smokey)
```

## Exercise: Cat

Now that you know how to create the kittie class, try to make a class for cats.

- The Cat can meow with the `meow` method.
- The Cat has 9 lives when she's created (she can't have more than 9 and less than 0 lives). 
- The Cat can say if she is alive (has more than 0 lives) with the `alive` method.
- The Cat can lose lives (method `takeoff_life`).
- The Cat can be fed with the `eat` method that takes exactly 1 argument - a specific food (string).
 If the food is `fish`, the Cat will gain one life (if she is not already dead or
 doesn't have maximum lives).

{% filter solution %}
```python
class Cat:
    def __init__(self):         # Init function does not have to take number of lives
        self.lives_number = 9   # as parameter 'cause that number is always the same.

    def meow(self):
        print("Meow, meow, meeeoooow!")

    def alive(self):
        return self.lives_number > 0

    def takeoff_life(self):
        if not self.alive():
            print("You can't kill a cat that is already dead, you monster!")
        else:
            self.lives_number -= 1

    def eat(self, food):
        if not self.alive():
            print("It's pointless to give food to dead cat!")
            return
        if food == "fish" and self.lives_number < 9:
            self.lives_number += 1
            print("The cat ate a fish and gained 1 life!")
        else:
            print("The cat is eating.")
```
{% endfilter %}

And that's now everything about classes.
[Next time](../inheritance/) we will learn about inheritance.
And also about doggies. :)
