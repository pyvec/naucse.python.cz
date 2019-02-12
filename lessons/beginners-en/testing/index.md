# Testing

Programming is not just about writing code. 
It is important to verify that the code does what it should 
(and about fixing it if needed).
The process of verification that the program works as expected is called *testing*.

You have probably tested your programs by trying to execute them, 
entered some input data and looked if the results are correct.
It is harder to do it for bigger programs. 
Bigger programs have more possibilities what to do and it is harder 
to verify that all possibilities do what they should.

That is why developers write code that verifies their program 
instead of testing their programs manually.

*Automated tests* are functions that check that the program works correctly.
You can execute the tests anytime and verify that the code works.
The main benefit is that you can change the code in the future
and let the tests verify that the change does not break existing functionalitye.


## Installing the pytest library

Up to now, we have used only the modules that come installed with Python, 
for example, modules such as `math` or `turtle`.
There are many more *libraries* that are not included in Python
but you can install them to your Python environment and use them.

The library for testing in Python is called `unittest`.
It is quite difficult to use this library so we will use a better one.
We will install the library `pytest` which is easy to use and very popular.

You install libraries into your active virtual environment.
We have learned how to create and activate a virtual environment
in the lesson about [Python installation]({{ lesson_url('beginners/install') }}).
Make sure that you have activated a virtual environment.

Submit the following command. (It is a command-line command, 
just as `cd` or `mkdir`; do not enter it into the Python console.)

```console
(venv)$ python -m pip install pytest
```

> [note] What does Pip do?
> `python -m pip` calls Python and tells it to execute the
> `pip` module. This module can install and uninstall libraries. 
> (Similarly, when you created a virtual environment, you used the
> command `python -m venv` – the `venv` module can create virtual environments.)
> And the arguments `install pytest` tell Pip to install `pytest`.
>
> You can display the help for the Pip module using the command
> `python -m pip --help`.

> [warning] For Windows users
> If you use Windows, it is important to run Python programs using
> `python program.py`, and not just `program.py`.
> Although we always show `python` in our lessons, 
> it could work without it so far.
> If you do not use the command `python` in the beginning, the program 
> could start in a different Python and different virtual environment, 
> where the `pytest` module might not have been installed.


## Writing tests

We will show testing thtough a very simple example.
There is a function `add` that can add two numbers.
There is another function that tests if the 
`add` function returns correct results for specific numbers.

Make a copy of the code into a file named `test_addition.py`
in a new empty directory.

The naming of files and test functions is important for `pytest` (with default settings). 
It is important for names of files containing tests and test functions
to start with `test_`.

```python
def add(a, b):
    return a + b

def test_add():
    assert add(1, 2) == 3
```

What does the test function do?

The `assert` statement evaluates the expression that follows it.
If the result is not true then it raises an exception 
and it makes the test fail.
You can imagine that `assert a == b` does following:

```python
if a != b:
    raise AssertionError('Test failed!')
```

> [note]
> Do not use `assert` outside of test functions for now.
> For "regular" code, the  `assert` has functionality that
> we will not explain now.


## Running tests

You execute tests with the command `python -m pytest -v`, 
followed by the name of the file containing the tests.
By using this command you are telling: <strong>Python</strong>: 
Execute the <strong>m</strong>odule named <strong>pytest</strong>,
in <strong>v</strong>erbose mode, for the given file.

```ansi
$ python -m pytest -v test_addition.py
␛[1m============= test session starts =============␛[0m
platform darwin -- Python 3.6.5, pytest-3.9.1, py-1.7.0, pluggy-0.8.0 -- 
rootdir: learn, inifile: 
␛[1mcollecting ...␛[0m collected 1 items

test_addition.py::test_add ␛[32mPASSED␛[0m

␛[32m============= 1 passed in 0.01 seconds =============␛[0m
```

This command scans the given file and calls all functions that start
with `test_`. It checks that they do not raise any exceptions, 
for example, an exception raised by `assert`.
If an exception occurs, `pytest` shows a red message with
additional details that can help you find the bug and fix it.

> [note]
> You can omit the argument with the filename: `python -m pytest -v`
> In this case, `pytest` scans the current directory and runs tests
> in all files whose names start with `test_`. You can use a path to 
> a directory and `pytest` finds tests in it.

Try to change the `add` function (or its test) and see what happens
if a test fails.


## Test modules

You do not usually write tests in the same file with the regular code.
Typically, you write tests in another file.
This way, your code is easier to read, and it makes it possible to distribute 
only the code, without the tests, to someone who is interested only in executing the program.

Split the `test_addition.py` file: Move the `add` function to a new module `addition.py`.
In the `test_addition.py` file, keep only the test.
To the `test_addition.py` file, add `from addition import add` to the top
so the test can call the tested function.

The test should pass again.


## Executable modules

Automated tests have to run "unattended".
They are usually executed automatically and the failures are reported
automatically (e.g. by email) and the code that passes all tests can
be automatically released (installed to a system where it runs 
or is made available to customers).

What does this mean to us?
The `input` function will not work in tests. There is no-one who can reply.

This can make your work harder sometimes. Let's look at a more complex project: 1D (one-dimensional) tic-tac-toe.

> [note]
{% if var('coach-present') -%}
> If you do not have the 1D tic-tac-toe program, the following sections are only theoretical.
{% endif -%}
> If you study at home, complete the 1D tic-tac-toe lesson before continuing.
> The homework assignment is in [PyLadies projects](http://pyladies.cz/v1/s004-strings/handout/handout4.pdf)
> on page 2.  (the English translation is at [one-dimensional tic-tac-toe](../tictactoe))..

The structure of your 1D tic-tac-toe code could look like this:

```python
import random  # (and possibly other import statements that are needed)

def move(board, space_number, mark):
    """Returns the board with the specified mark placed in the specified position"""
    ...

def player_move(board):
    """Asks the player what move should be done and returns the board
    with the move played.
    """
    ...
    input('What is your move? ')
    ...

def tic_tac_toe_1d():
    """Starts the game

    It creates an empty board and runs player_move and computer_move alternately
    until the game is finished.
    """
    while ...:
        ...
        player_move(...)
        ...

# Start the game:
tic_tac_toe_1d()
```

If you import this module, Python executes all commands in it 
from top to bottom.

The first command, `import`, makes some functions and variables available.
Imports do not usually have any side-effects.

The definitions of functions (`def` statements and everything in them) 
just define the functions (but they do not execute the functions).

Calling the `tic_tac_toe_1d` function starts the game.
The `tic_tac_toe_1d` calls the `player_move()` function which calls `input()`.

If you import this module from tests, the `input` fails 
and the module is not imported.

> [note]
> If you want to import such a module from elsewhere – for example, you would like
> to use `move` in another game – the import of the module requires the user to 
> play 1D tic-tac-toe!

The calling of `tic_tac_toe_1d` is a side-effect and we need to remove it.
Yeah but you cannot start the game without it! What about it?

You can create a new module.
Name it `game.py` and put just this call into it:

```python
import tic_tac_toe

tic_tac_toe.tic_tac_toe_1d()
```

You cannot test this module because it calls `input` indirectly.
But you can execute it if you want to play.
Since you do not have tests for this module, it should be very simple: 
one import and one statement.

You can import the original module from tests or other modules.

A test for the original module could look like this:

```python
import tic_tac_toe

def test_move_to_empty_space():
    board = tic_tac_toe.computer_move('--------------------')
    assert len(board) == 20
    assert board.count('x') == 1
    assert board.count('-') == 19
```

## Positive and negative tests

The tests that verify that the program works correctly 
under correct conditions are called *positive tests*.
But you can test what your program does under unexpected conditions.

The tests that check the behavior in case of "invalid" input
are called *negative tests*.
They can check for a specific negative result (for example 
that a call like `is_number_even(7)` returns `False`), 
or that a "reasonable" exception is raised. 

For example, the `computer_move` function should raise an error 
(for example `ValueError`) when the board is full.

> [note]
> It is much better to raise an exception than doing nothing 
> and silently letting the program get stuck.
> You can use such function in a more complex program 
> and be sure that you will get an understandable error
> when it is called under bad conditions. 
> Then you can easily fix it.

Use the `with` statement and the `raises` function 
to test that your code raises the expected exception.
The `raises` function is imported from the `pytest` module.
We will explain the `with` statement later.
You just need to know that it checks that the block of code below 
raises the specified exception:

```python
import pytest

import tic_tac_toe

def test_move_failure():
    with pytest.raises(ValueError):
        tic_tac_toe.computer_move('oxoxoxoxoxoxoxoxoxox')
```
