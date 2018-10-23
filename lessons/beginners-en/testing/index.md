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
The main benefit is that you can change the code in future
and let the tests verify that the existing is not broken by the change.


## Installing the pytest library

We have used only the modules that are installed with Python. 
For example with modules as `math` or `turtle`.
There is a lot of other *libraries* that are not included in Python
but you can install them to your Python environment and use them.

The is a library for testing in Python called `unittest`.
It is quite difficult to use this library so we will use a better one.
We will install library `pytest` that is easy to use and very popular.

You install libraries to your active virtual environment.
We have learned how to create and activate a virtual environment
in the lesson about [Python installation]({{ lesson_url('beginners/install') }}).
Make sure that you have activated a virtual environment.

Submit the following command.
(It is a command-line command, 
as `cd` or `mkdir`; do not submit it in Python.)

```console
(venv)$ python -m pip install pytest
```

> [note] What it does?
> `python -m pip` calls Python and tells it to execute the
> `pip` module. This module can install and uninstall libraries. 
> (When you were creating a virtual environment, you have used 
> command `python -m venv` – the `venv` module can create virtual environments.)
> And the arguments `install pytest` tell Pip to install `pytest`.
>
> You can display the help for the Pip using command
> `python -m pip --help`.

> [warning] For Windows users
> If you use Windows, it is important to run Python programs using
> `python program.py`, and not just `program.py`.
> Although we always show `python` in our lessons, 
> it could work without it so far.
> If you do not use command `python` at the beginning, the program can start
> in different Python and different virtual environment 
> and the `pytest` module can be missing there.


## Writing tests

We will show testing on a very simple example.
There is a function `add` that can add two numbers.
There is another function that tests if the 
`add` gives correct results for specific numbers.

Make a copy of the code to a file named `test_addition.py`
in a new empty directory.

The naming of files with and test functions is important for `pytest` (with default settings). So it is important for names of the files with tests and test functions
to start with `test_`.

```python
def add(a, b):
    return a + b

def test_add():
    assert add(1, 2) == 3
```

What the test function does?

The `assert` statement evaluates the expression that follows it.
If the result is not true then it raises an exception 
and it makes the test fail.
You can imagine that `assert a == b` does following:

```python
if a != b:
    raise AssertionError('Test failed!')
```

> [note]
> Do not use `assert` outside of test functions in this moment.
> For "regular" code, the  `assert` has functionality that
> we will not explain now.


## Running tests

Tests can be executed by command
`python -m pytest -v` that is followed by name of the file with tests.
By using this command you are telling: <strong>Python</strong>, execute
<strong>m</strong>odule named <strong>pytest</strong>,
in a <strong>v</strong>erbose mode for the given file.

```ansi
$ python -m pytest -v test_addition.py
␛[1m============= test session starts =============␛[0m
platform darwin -- Python 3.6.5, pytest-3.9.1, py-1.7.0, pluggy-0.8.0 -- 
rootdir: learn, inifile: 
␛[1mcollecting ...␛[0m collected 1 items

test_addition.py::test_add ␛[32mPASSED␛[0m

␛[32m============= 1 passed in 0.01 seconds =============␛[0m
```

This command scans the given file and calls all function that starts
with `test_` and it checks that do not raise any exception, 
for example, an exception raised by `assert`.
If an exception occurs, `pytest` shows it by a red message with
additional details that can help you to find the bug and fix it.

> [note]
> You can omit the argument with the filename: `python -m pytest -v`
> In this case, `pytest` scans the current directory and start tests
> in all files whose names start with `test_`. You can use a path to 
> a directory and `pytest` finds tests in it.

Try to change the `add` function (or its test) and see what happens
if a test fails.


## Test modules

You do not usually write tests in the same file with the regular code.
It is typical to write tests to another file.
It is more understandable this way and it is possible to distribute 
only code without the tests to someone who needs only to execute the program.

Split the `test_addition.py` file: the `add` function move to new module `addition.py`,
and in the `test_addition.py` file keep only the test.
To the `test_addition.py` file add `from addition import add` to the top
so the test can call the tested function.

The test should pass again.


## Executable modules

Automated tests have to run "unattended".
They are usually executed automatically and the failures are reported
automatically (e.g. by email) and the code that passes all tests can
be automatically released (installed to a system where it runs 
or made available to customers).

What does it mean to us?
The `input` function does not work in tests. There is not anyone who can reply.

This can make the work harder sometimes. Let's see it on a more complex project: 1D (one-dimensional) tic-tac-toe.

> [note]
{% if var('coach-present') -%}
> If you do not have program with 1D tic-tac-toe, the following sections are only theoretical.
{% endif -%}
> If you study at home, you can complete 1D tic-tac-toe before continuing.
> The homework assignment is in [PyLadies projects](http://pyladies.cz/v1/s004-strings/handout/handout4.pdf)
> on page 2 (the English translation is at [one-dimensional tic-tac-toe](tic_tac_toe.md)).

The structure of the 1D tic-tac-toe code can look like this:

```python
import random  # (eventually other import statements that are needed)

def move(board, space_number, mark):
    """Returns the board with the specified mark placed on specified space"""
    ...

def player_move(board):
    """Asks the player what move should be done and returns the board
    with the move played
    """
    ...
    input('What is your move? ')
    ...

def tic_tac_toe_1d():
    """Starts the game

    It creates an empty board and runs player_move and computer_move alternately
    until the game is finished
    """
    while ...:
        ...
        player_move(...)
        ...

# Start the game:
tic_tac_toe_1d()
```

If you import this module, the Python executes all commands 
in it from the top to the bottom.

The first command, `import`, makes some functions and variables available.
There is not usually any side-effect.

The definitions of functions (`def` statements and everything in them) 
just define the functions (but they do not execute the functions).

But calling the `tic_tac_toe_1d` function starts the game.
The `tic_tac_toe_1d` call the `player_move()` function and that calls `input()`.

If you import this module from tests, the `input` fails 
and the module is not imported.

> [note]
> If you want to import such module from elsewhere – for example, you would like
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

A test for the original module can look like this:

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
But you can test what your program does if there unexpected conditions.

The tests that check the behavior in case of "invalid" input
are called *negative tests*.
They can check a specific negative result (for example that call like `is_number_even(7)` returns `False`), or that a "reasonable" exception is raised. 

For example, the `computer_move` function should raise an error 
(for example `ValueError`) when the board is full.

> [note]
> It is much better to raise an exception than do nothing 
> and silently make the program stuck.
> You can such function in a more complex program 
> and be sure that you will get an understandable error
> when it is called under bad conditions. 
> Then you can easily fix it.

Use the `with` statement and the `raises` function 
to test that your code raises expected exception.
The `raises` function is imported from the `pytest` module.
We will explain the `with` statement later.
You just need to know that it checks that the block of the code below 
raises the specified exception:

```python
import pytest

import tic_tac_toe

def test_move_failure():
    with pytest.raises(ValueError):
        tic_tac_toe.computer_move('oxoxoxoxoxoxoxoxoxox')
```