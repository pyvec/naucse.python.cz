# Inheritance

We already know what are classes and we have shown the class for kitties
as an example:

```python
class Kittie:
    def __init__(self, name):
        self.name = name

    def meow(self):
        print("{}: Meow!".format(self.name))

    def eat(self, food):
        print("{}: Meow meow! I like {} very much!".format(self.name, food))
```

Now create similar class for dogs:

```python
class Doggie:
    def __init__(self, name):
        self.name = name

    def woof(self):
        print("{}: Woof!".format(self.name))

    def eat(self, food):
        print("{}: Woof woof! I like {} very much!".format(self.name, food))
```

Most of the code is the same!
If you would have to write class for chicks, ducks and rabbits, 
it would be quite boring without Ctrl+C.
And because programmers are lazy to write the same piece of
code multiple times (and mostly maintain it) they created
mechanism how to avoid it. How?

Kitties and doggies are animals.
So you can create class for all animals and write
there everything that applies to all animals.
And to classes about each animal you will just
write the specifics.
That's how it's done in Python:

```python
class Animal:
    def __init__(self, name):
        self.name = name

    def eat(self, food):
        print("{}: I like {} very much!".format(self.name, food))


class Kittie(Animal):
    def meow(self):
        print("{}: Meow!".format(self.name))


class Doggie(Animal):
    def woof(self):
        print("{}: Woof!".format(self.name))


smokey = Kittie('Smokey')
doggo = Doggie('Doggo')
smokey.meow()
doggo.woof()
smokey.eat('mouse')
doggo.eat('bone')
```

How does it work?
With command `class Kittie(Animal)` you are
telling Python that class `Kittie` *inherits*
behaviour from class `Animal`.
Or you can see in different programming languages 
that `Kittie` is *derived from* `Animal` 
or it *extends* `Animal`.
Derived classes are called *subclasses* and the main one
is *superclass*

When Python searches for some method/function (or other attribute),
for example `smokey(eat)`, and it doesn't find it in the class itself
it will look into the superclass. So everything that has been
defined for Animal can be applied for Kittie (if you won't
tell Python otherwise).


## Overwriting methods and `super()`

If you don't like some behaviour of superclass you can
define method with the same name into subclass:

```python
class Kittie(Animal):
    def eat(self, food):
        print("{}: I don't like {} at all!".format(self.name, food))


smokey = Kittie('Smokey')
smokey.eat('dry food')
```

> [python]
> It's similar to what we did in the previous lesson with
> `misty.meow = 12345`. Python searches for the attributes in the object,
> then the class and then the superclass (and then in superclass' superclass).

It can happen that sometimes you will need in the overwritten
method some behaviour from the original method, you will only need to do
something extra there. You can do it with special function `super()`,
which allows calling methods from superclass.

```python
class Kittie(Animal):
    def eat(self, food):
        print("({} is looking at {} for a while)".format(self.name, food))
        super().eat(food)

smokey = Kittie('Smokey')
smokey.eat('dry food')
```

Keep in mind that you have to pass everything that this `super()` method
needs (apart from `self`, which is passed automatically).
You can use this - you can pass different values
than the original function received (in this case `snake` class will
receive name `Stanley` but you want to change it to `Ssstanley`):

```python
class snake(Animal):
    def __init__(self, name):
        name = name.replace('s', 'sss')
        name = name.replace('S', 'Sss')
        super().__init__(name)


stanley = snake('Stanley')
stanley.eat('mouse')
```

As you can see, you can use `super()` even with special methods
like `__init__`.


## Polymorphism

Programmer didn't create inheritance only because they are lazy
to write the same code multiple times. It is, of course,
good reason but superclasses have also another
important feature: when we know that `Kittie` and `Doggie`
and any other similar class are animals we can create a list
of animals but we don't care what animals they are 
specifically:

{# XXX: last 4 lines are new and should be highlighted #}
```python
class Animal:
    def __init__(self, name):
        self.name = name

    def eat(self, food):
        print("{}: I like {} very much!".format(self.name, food))


class Kittie(Animal):
    def meow(self):
        print("{}: Meow!".format(self.name))


class Doggie(Animal):
    def woof(self):
        print("{}: Woof!".format(self.name))

animals = [Kittie('Smokey'), Doggie('Doggo')]

for animal in animals:
    animal.eat('meat')
```

This is quite important behaviour of subclasses:
when you have some `Kittie` you can use it anywhere
where program expects `Animal` because each kittie
*is* animal.

> [note]
> This is good help when you won't know which class should be
> inherited in which class.
> Each *kittie* or *doggie* is *animal*,
> each *cabin* or *house* is *building*.
> In those examples heredity makes sense.
>
> But sometimes our help fails - for example if we would say
> each *car* is *steering wheel*, then we will know that
> we shouldn't use inheritance.
> Even if we can "rotate" car and steering wheel it means different thing, 
> and we definitely can't use car everywhere where we would want to
> use steering wheel. So in this case we should say to ourselves:
> each kittie *has* name and each car *has* steering wheel so we
> should create two different classes and in car class 
> use steering wheel as default variable:
>
> ```python
> class Car:
>     def __init__(self):
>         self.wheel = Wheel()
> ```
>
> (And when some programmer will be mad at you that you
> are breaking [Liskov_substitution_principle](https://en.wikipedia.org/wiki/Liskov_substitution_principle)
> it's because of this problem.)

## Generalization

When you look back to functions `meow` and `woof` you will maybe find out
that they can be named better so they can be used for each animal, similarly
as `eat`.

{# XXX: Every instance of "speak" should be highlighted #}
```python
class Animal:
    def __init__(self, name):
        self.name = name

    def eat(self, food):
        print("{}: I like {} very much!".format(self.name, food))


class Kittie(Animal):
    def speak(self):
        print("{}: Meow!".format(self.name))


class Doggie(Animal):
    def speak(self):
        print("{}: Woof!".format(self.name))

animals = [Kittie('Smokey'), Doggie('Doggo')]

for animal in animals:
    animal.speak()
    animal.eat('meat')
```

As this example shows writing superclasses from which we can easily inherit
methods is not easy. It is definitely not easy when we want to create
subclass in different program than where is superclass.
So that's why you should inherit classes within your code:
we do not recommend to inherit classes that someone else wrote,
unless the author of the superclass explicitly mentions that you can (and
mainly how) inherit from their class.

And that's all about classes. Now you know enough to create
your own zoo :)