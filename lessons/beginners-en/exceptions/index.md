# Exceptions

We have already talked about [error messages]({{ lesson_url('beginners/print') }}): 
Python complains, tells us where the error (line) is, and terminates the program.
But there is much more that we can learn about error messages (a.k.a *exceptions*).


## Printing errors:

In the beginning we will repeat how Python prints an error which is in a nested function.


```python
def out_func():
    return in_func(0)

def in_func(divisor):
    return 1 / divisor

print(out_func())
```

<!-- XXX: Highlight the line numbers -->

```pycon
Traceback (most recent call last):          
  File "/tmp/example.py", line 7, in <module>
    print(out_func())
  File "/tmp/example.py", line 2, in out_func
    return in_func(0)
  File "/tmp/example.py", line 5, in in_func
    return 1 / divisor
ZeroDivisionError: division by zero
```

You notice that every function call that led to the error is listed here.
The actuall error is probably somewhere near that function call.
In our case it's easy. We shouldn't call `in_func` with argument `0`.
Or, the `in_function` must be written to handle the case that the divisor can be `0`
and it should do something else than try to devide by zero.

Python can't know where the error is that needs to be fixed, so it shows
you everything in the error message.
This will be very useful in more complex programs.


## Raising an error

An error, or more precisely an *exception*, can be also invoked by the command `raise`.
After that command, write the name of the exception and some
information about what went wrong in parentheses.


```python
LIST_SIZE = 20

def verify_number(number):
    if 0 <= number < LIST_SIZE:
        print('OK!')
    else:
        raise ValueError('The number {n} is not in the list!'.format(n=number))
```

All types of built-in exceptions are
[here](https://docs.python.org/3/library/exceptions.html), including their hierarchy.

These exceptions are important to us now:

```plain
BaseException
 ├── SystemExit                     raised by function exit()
 ├── KeyboardInterrupt              raised after pressing Ctrl+C
 ╰── Exception
      ├── ArithmeticError
      │    ╰── ZeroDivisionError    zero division
      ├── AssertionError            command `assert` failed
      ├── AttributeError            non-existing attribute, e.g. 'abc'.len
      ├── ImportError               failed import
      ├── LookupError
      │    ╰── IndexError           non-existing index, e.g. 'abc'[999]
      ├── NameError                 used a non-existing variable name
      │    ╰── UnboundLocalError    used a variable that wasn't initiated
      ├── SyntaxError               wrong syntax – program is unreadable/unusable
      │    ╰── IndentationError     wrong indentation
      │         ╰── TabError        combination of tabs and spaces
      ├── TypeError                 wrong type, e.g. len(9)
      ╰── ValueError                wrong value, e.g. int('xyz')
```


## Handling Exceptions

And why are there so many?
So you can catch them! :)
In the following function, the `int` function can 
fail when something other than a
number is given to it. It needs to be prepared for
that kind of situation with a `try/except` block. (You also
commonly hear this called a `try/catch` block -- mostly in other
programming languages).

```python
def load_number():
    answer = input('Enter some number: ')
    try:
        number = int(answer)
    except ValueError:
        print('That was not a number! I will continue with 0')
        number = 0
    return number
```

So how does this work?
Python runs the commands within the `try` block, but if the error occurs
that you mentioned after `except`, Python won't terminate the program, instead, it will
run all the commands in the exception block.
If there's no error, the except block will be skipped.

When you catch a general exception, Python also catches
exceptions that are related to it (in the diagram, they are listed as child entries) -- 
e.g. `except ArithmeticError:` will also catch `ZeroDivisionError`.
And `except Exception:` will catch all usual exceptions.


## Don't catch'em all!

There is no need to catch most of the errors.

If any unexpected error happens 
it's always *much* better to terminate the program
than to continue with wrong values.
In addition, Python's standard error output will make it
really easy for you to find the error.

For example, catching the exception `KeyboardInterrupt`
could have the side effect that the program couldn't be terminated if we needed to
(with shortcut <kbd>Ctrl</kbd>+<kbd>C</kbd>).

Use the command `try/except` only in situations when you
expect some exception -- when you know exactly what could happen
and why, and you have the option to correct it -- in the
except block.
A typical example would be reading input from a user. If the user 
enters gibberish, it's better to ask again until the
user enters something meaningful:


```pycon
>>> def retrieve_number():
...     while True:
...             answer = input("Type a number: ")
...             try:
...                     return int(answer)
...             except ValueError:
...                     print("This is not a number. Try again")

>>> print(retrieve_number())
Type a number: twenty
This is not a number. Try again
Type a number: 20
20

```


## Other clauses

Additionally to `except`, there are two more clauses - blocks that can 
be used with `try`, and these are `else` and `finally`.
The first one will be run if exception in the `try` block didn't happen.
And `finally` runs every time.

You can also have several `except` blocks. Only one of them will be triggered -- 
the first one that can handle the raised exception. 


```python
try:
    do_something()
except ValueError:
    print("This will be printed if there's a ValueError.")
except NameError:
    print("This will be printed if there's a NameError.")
except Exception:
    print("This will be printed if there's some other exception.")
    # (apart from SystemExit a KeyboardInterrupt, we don't want to catch those)
except TypeError:
    print("This will never be printed")
    # ("except Exception" above already caught the TypeError)
else:
    print("This will be printed if there's no error in try block")
finally:
    print("This will always be printed; even if there's e.g. a 'return' in the 'try' block.")
```


## Task

Let's add exception handling to our calculator (or to 1-D ticktactoe, if you have it)  
if the user doesn't enter a number in the input.


{% filter solution %}

Possible solution for the calculator:

```python

while True:
    try:
        side = float(input('Enter the side of a square in centimeters: '))
    except ValueError:
        print('That was not a number!')
    else:
        if side <= 0:
            print('That does not make sense!')
        else:
            break

print("The perimeter of a square with a side of", side,"cm is ", side * 4,"cm.")
print("The area of a square with a side of", side,"cm is", side * side, "cm2.")

```

Possible solution for 1-D ticktactoe:

```python
def load_number(field):
    while True:
        try:
            position = int(input('Which position do you want to fill? (0..19) '))
        except ValueError:
            print('This is not a number!')
        else:
            if position < 0 or position >= len(field):
                print('You can not play outside the field!')
            elif field[position] != '-':
                print('That position is not free!')
            else:
                break

    field = field[:position] + 'o' + field[position + 1:]
    return field


print(player_move('-x----'))
```

{% endfilter %}
