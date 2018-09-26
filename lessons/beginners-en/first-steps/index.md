## First commands in Python

Let's see if we installed Python successfully!

First check if your virtual environment is active. (You should see `(myenv)`
in the beginning of your command line.)

If it's there, we can now start Python (specifically, the Python console).
To do that, just write `python`:


``` plain
(myenv)$ python
Python 3.4.0 (default, Jan 26 2014, 18:15:05)
[GCC 4.8.2 20131212 (Red Hat 4.8.2-7)] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>>
```

This command will print some information.
in the first line, it shows which version of Python you have 
(you should have Python 3).
The command line starts with three "greater than" signs.
This way Python prompts (asks) you for instructions.
This is the same as the standard command line, but instead of commands
like `cd` or `mkdir`, you write Python commands.

The simplest command is a number. Try it:

```pycon
>>> 1
1
>>> 42
42
>>> -8.3    # (Python uses period as decimal point)
-8.3
```

> [note]
> Python prints the greater-than signs `>>>` and the answer by itself!
> You just write number and press Enter.

Python can also add up numbers, like this:

```pycon
>>> 8 + 2
10
```

Notice that commands from the standard command line do not work here,
although the window looks the same:

```pycon
>>> whoami
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
NameError: name 'whoami' is not defined
```

This is an *error message* which appears every time when you
do anything wrong.
You will see a lot of them during the course,
so look at it carefully so you recognise it later.

If you got this far, congratulations!
You have installed Python and it works.
You can now quit the Python console and close the command prompt.
To quit, just type `quit()` with empty parentheses. 


<div class="highlight"><pre>
<span class="gp">&gt;&gt;&gt;</span> quit()
<span class="gp">(myenv)$</span>
</pre></div>

The greater-than signs `>>>` change back to `(myenv)` 
followed by `$` or `>`.
Now commands like `whoami` and `cd` work again, but Python
commands like `1 + 2` don't wotk, until you enter the Python console  
with `python` again.

To quit the virtual environment, type `deactivate` or `source deactivate` 
(for Linux and Mac) -- this time without parentheses.

```console
(myenv)$ deactivate
```

The command prompt (terminal) can be closed by typing `exit`.

```console
$ exit
```

As an exercise, try to run the Python console again -- open the command prompt 
(the terminal), then activate the virtual environment, and finally run Python.

