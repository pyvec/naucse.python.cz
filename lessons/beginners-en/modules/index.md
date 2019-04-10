# Modules

A module is something like a package. We can import it into our code.
Or we can import functions from the module into our code.
For example, you can import the function `sqrt` from the module `math`:

```python
from math import sqrt

print(sqrt(2))
```

You can also import a whole module. You can access a module's
functions through a period - the same way as you access string methods
(`'Hello'.upper()`).

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
> In documentation or in another course, you have maybe seen 
> an import with an asterisk (`*`).
> In this course, we won't use it, we always import the whole module instead.
> When you write more difficult programs in the future, this will make
> your work easier.


## Custom modules

You can also create your own module simply by
creating a Python file. Functions and variables
that you create there will be available
in programs where you import this module.

Try it!
Create file `meadow.py` and write:

```python
meadow_colour = 'green'
number_of_kitties = 28

def description():
    return 'The meadow is {colour}. There are {number} kitties.'.format(
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

The command `import` looks for files in the same folder
of the file where you imported the module - in our
case `write.py`. So place both of the files into the 
same folder.

## Side effects

What exactly does the command `import meadow` do?

Python will look for a matching file (`meadow.py`) and run all the commands
there from top to bottom, like it was a normal program.
It will give all the global variables (including defined functions) to the
program that imported that module.

When you import the same module a second time, it doesn't
run everything again - it will just use what it already has.

Try it - write in the end of `meadow.py`:

```python
print('The meadow is green!')
```

And then run `python` in the command line (if you already have an interactive
Python open, close it, and run again) and enter:

```pycon
>>> print('First import:')
>>> import meadow
>>> print('Second import:')
>>> import meadow
```

The print we wrote in the end of the module file
will appear only once.

When the module is "doing something" (it prints something, asks the user, 
writes something into a file) - we say that it has a *side effect*.
We try to avoid writing modules that have side effects:
because the purpose of a module is to give us *functions*, that we
will use to do something, not to do it instead of us.
For example, when we write `import turtle`, no window opens. It opens
only when we write `turtle.forward()`.

So you better delete `print` from our module.


## One directory for every project

From now on, we will work on bigger projects that contain
more files. We recommend that you create a folder for each
of them.


You can find more info about [import and modules here](https://chrisyeh96.github.io/2017/08/08/definitive-guide-python-imports.html#basics-of-the-python-import-and-syspath).
