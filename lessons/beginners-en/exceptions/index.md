# Exceptions

We were already talking about [error messages]({{ lesson_url('beginners/print') }}) : 
Python complains, tells us where is the error (line) and terminates the program.
But there are lot more what we can learn about error messages (a.k.a *exceptions*).


## Printing errors:

In the beginning we will repeat how Python prints error which is in nested function.


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

You can notice that every function calling that led to error is written there.
The actuall error is probably somewhere around that function calling.
In our case it's easy. We should't call `in_func` with argument `0`.
Or this `in_function` should be prepared that the divisor can be `0`
and it should do something else than try to devide by zero.

Python can't know where is the error that should repaired so it shows
you everything in error message.
It will be very useful in more difficult programs.


## Raising error

Error or more precisely *exception* could be also invoked by command `raise`.
After that command there have to be the name of the exception and then you write some 
information about what went wrong into brackets.


```python
LIST_SIZE = 20

def verify_number(number):
    if 0 <= number < LIST_SIZE:
        print('OK!')
    else:
        raise ValueError('The number {n} is not in the list!'.format(n=number))
```

All types of built-in exceptions are
[here](https://docs.python.org/3/library/exceptions.html) including their hierarchy.

Those are important to us now:

```plain
BaseException
 ├── SystemExit                     raised by function exit()
 ├── KeyboardInterrupt              raised after pressind Ctrl+C
 ╰── Exception
      ├── ArithmeticError
      │    ╰── ZeroDivisionError    zero division
      ├── AssertionError            command `assert` failed
      ├── AttributeError            non-existing attribute, e.g. 'abc'.len
      ├── ImportError               failed import
      ├── LookupError
      │    ╰── IndexError           non-existing index, e.g. 'abc'[999]
      ├── NameError                 used non-existing name of variable
      │    ╰── UnboundLocalError    used variable, which wasn't initiated
      ├── SyntaxError               wrong syntax – program is unreadable/unusable
      │    ╰── IndentationError     wrong indentation
      │         ╰── TabError        combination of tabs and spaces
      ├── TypeError                 wrong type, e.g. len(9)
      ╰── ValueError                wrong value, e.g. int('xyz')
```


## Handling Exceptions

And why are there so many?
So you can catch them! :)
In the following function the `int` function can 
fail when there is something else than
number given to it. So it needs to be prepared for
that kind of situation with `try/except` block (you can also
see this named `try/catch` block - mostly in different
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

So how does that work?
Commands within the block `try` will be run but when there is error
which you named after `except` Python won't terminate the program it will
run all the commands in the exception block.
When there won't be any error the except block will be skipped.

When you are catching a general exception there will be
catched also exceptions that are related to it (in the diagram they are underneath) - 
e.g. `except ArithmeticError:` will catch also `ZeroDivisionError`.
And `except Exception:` will catch all ussual exceptions.


## Don't catch'em all!

There is no need to catch most of the errors.

If any error, that you don't expect, happens 
it's always *much* better to terminate the program
than continue with wrong values.
In addition Python's standard error output will
really easy you to find the error.

For example catching exception `KeyboardInterrupt`
could cause that program couldn't be terminated if we would need it
(with shortcut <kbd>Ctrl</kbd>+<kbd>C</kbd>).

Use command `try/except`only in situations when you
expect some exception - you know exactly what could happen
and why and you have the option to correct it - in
except block.
Typical example with input from user. When user will 
enter some gibberish it is better to ask again until
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


## Another clauses

Apart from `except` there are two more clauses - blocks that can 
be used with `try` and those are `else` and `finally`.
The first one will be run if exception in `try` block won't happen.
And `finally` will run every time.

You can also have more `except` block. There will be triggered only one - 
the first one that can handle the raised exception. 


```python
try:
    do_something()
except ValueError:
    print('This will be printed when there will be ValueError.')
except NameError:
    print('This will be printed when there will be NameError.')
except Exception:
    print('This will be printed when there will be some other exception.')
    # (apart from SystemExit a KeyboardInterrupt, we don't want to catch those)
except TypeError:
    print('This will never be printed')
    # ("except Exception" above already caught TypeError)
else:
    print('This will be printed when there will not be any error in try block')
finally:
    print('This will be printed always; even if there would be e.g. `return` in the `try` block.')
```


## Task

Add to our calculator (or to 1-D ticktactoe if you have it) exception 
handeling if user won't enter number in the input.


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
                print('You can not play out of field!')
            elif field[position] != '-':
                print('That position is not free!')
            else:
                break

    field = field[:position] + 'o' + field[position + 1:]
    return field


print(player_move('-x----'))
```
{% endfilter %}
