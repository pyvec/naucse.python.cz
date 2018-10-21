# Modules

Module je v Pythonu něco, z čeho můžeme importovat.
For example you can import function `sqrt` from module `math`:

```python
from math import sqrt

print(sqrt(2))
```

You can also import whole module. You can get to module's
functions through period - same as you get to strings methods
(`'Hello'.upper*()`).

For example:

```python
import turtle

turtle.left(90)
turtle.color('red')
turtle.forward(100)
turtle.exitonclick()
```

```python
import math

print(math.cos(math.pi))
```

> [note] We don't want asterisks
>
> You could see in documentation or in another course command
> import with asterisk (`*`).
> In this course we won't use it, import the whole module instead.
> When you will write more difficult programs it will simplify
> your work.


## Custom modules

You can also create your own module simply by
creating Python file. Functions and variables
you will create there will be available
in programs where you will import this module.

Try it!
Create file `meadow.py` and write:

```python
meadow_colour = 'green'
number_of_kitties = 28

def description():
    return 'Meadow is {colour}. There are {number} kitties.'.format(
        colour=meadow_colour, number=number_of_kitties)
```

And then write in another file (`write.py`):

```python
import meadow

print(meadow.description())
```

and run:

```console
$ python write.py
```

Command `import` looks for files in the same folder
where is the file where you imported the module - in our
case `write.py`. So both of the files should be in the 
same folder.

## Side effects

What exactly is doing the command `import meadow`?

Python will look for relevant file (`meadow.py`) and run all the commands
there from the top to the bottom, like it was normal program.
It will give all the global variables (including defined functions) to the
program that imported that module.

When you import the same module for second time, it doesn't
run everything again - it will just use what it already has.

Try it - write in the end of `meadow.py`:

```python
print('Meadow is green!')
```

And then run `python` in command line (if you already have interactive
Python on, close it and run again) and enter:

```pycon
>>> print('First import:')
>>> import meadow
>>> print('Second import:')
>>> import meadow
```

The print we wrote to the end of the module file
will appear only once.

When module is "doing something" (prints something, asks user, 
writes something into a file)
- it is called that it has *side effect*.
We are trying to avoid such modules that have side effects:
because the purpose of a module is to give us *functions*, that we
will use to do something, not to do it instead of us.
For example when we write `import turtle` the window is not shown but it will 
be when we write `turtle.forward()`.

So you better delete `print` from our module.


## Directory for every project

From now on we will work on bigger projects that contains
more files. So it will be better if you will create folder for each
one of them.
