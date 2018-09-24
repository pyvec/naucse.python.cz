## First commands in Python

Let's try if we installed Python successfully!

First check if you have your virtual environment active (there is `(venv)`
in the beginning of your command line).

If it's there we can now start Python (precisely Python console).
To do that just write `python`:


``` plain
(venv)$ python
Python 3.4.0 (default, Jan 26 2014, 18:15:05)
[GCC 4.8.2 20131212 (Red Hat 4.8.2-7)] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>>
```

That commnd will write out some information.
On the first line there is which version of Python you have (so 
you should have there Python 3).
Now the command line starts with three "greater than" signs.
This way Python asks for instructions.
It's same as standard command line but instead of commands
like `cd` or `mkdir` you have to write there Python commands.

The simplest command is number. Try it:

```pycon
>>> 1
1
>>> 42
42
>>> -8.3    # (Python uses period as decimal point)
-8.3
```

> [note]
> Greater than signs `>>>` and the answer is printing Python by itself!
> You just have to write number and press Enter.

Python can also add up numbers, like that:

```pycon
>>> 8 + 2
10
```

Notice that commands from standard command line are not working there
although window looks the same:

```pycon
>>> whoami
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
NameError: name 'whoami' is not defined
```

This is *error message* which appears always when you
do anything wrong.
You will see a lot of them during the course
so look at it carefully so you can recognise it later.

If you got into this point congratulation!
You have installed Python and it works.
Now you can quit Python console and close command prompt.
To quit just type `quit()` with empty brackets. 


<div class="highlight"><pre>
<span class="gp">&gt;&gt;&gt;</span> quit()
<span class="gp">(venv)$</span>
</pre></div>

Greater than signs `>>>` changed back to `(venv)` with `$` or
`>` in the end.
Now commands like `whoami` and `cd` are working but Python's
commands like `1 + 2` don't until you enter Python console with 
`python` again.

To quit virtual environment type `deactivate` -
now without brackets.

```console
(venv)$ deactivate
```

Command prompt (terminal) can be closed by typing `exit`.

```console
$ exit
```

For practicing try run Python console again - open command prompt/terminal
then activate virtual environment and finally fun Python.

