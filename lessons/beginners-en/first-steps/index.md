## First commands in Python

Let's see if we installed Python successfully!

First check if your virtual environment is active. You should see `(myenv)`
in the beginning of your command line. If you don't see it, try doing `conda activate <your virtuale environment name>`

If it's there, we can now start Python (specifically, the Python console).
To do that, just write `python`:


``` plain
(myenv)$ python
Python 3.8.1 (default, Dec 24 2019, 17:02:07) 
[GCC 9.2.1 20191008] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>>
```

This command will print some information. In the first line, it shows which version of Python you have (you should have Python 3+). The command line starts with a `>>>` symbol. This way Python prompts (asks) you for instructions. This is the same as the standard command line, but instead of commands like `cd` or `mkdir`, you write Python commands.

## Quick task 

If you have the terminal ready don't waste time! Type `print("Hello, world!")` in the Python terminal! 

{% filter solution %}

What happened? Python "printed out" `Hello, world!` for you. It's an old programming tradition, going back to ~1970s. It is a traditional first command executed by people who are learning a given programming language, which illustrates the basic syntax of the language. In python one can simply execute `print("Hello, world!")`. In other programming languages it might not be that simple! Feel free to search for examples of a "Hello world" code in C++, Java, HTML, JavaScript or other languages.  

{% endfilter %}

## Python basics

Python can work as a simple calculator:

```pycon
>>> 1
1
>>> 42 + 3
45
>>> -1.1 + 12
10.9
>>> 2/3
0.6666666666666666
>>> 3*5
15
>>> 2**4
16
>>> 1e3 + 222
1222.0
>>> -8.3 + 2
-6.300000000000001
>>> 15%4
3
>>> 10_000 + 155
10155
>>> 17//3
5
>>> 2 + 3 * 4
14
>>> (2+3) * 4
20
```

> [note]
> Python prints the greater-than signs `>>>` and the answer by itself!
> You just write number and press Enter.

Notice that commands from the standard command line do not work here, although the window looks similar:

```pycon
>>> whoami
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
NameError: name 'whoami' is not defined
```

This is an *error message* which appears every time when you do anything wrong. You will see a lot of them during the course, so look at it carefully so you recognise it later.

If you got this far, congratulations! You have installed Python and it works. You can now quit the Python console and close the command prompt. To quit, just type `exit()` with empty parentheses. 


<div class="highlight"><pre>
<span class="gp">&gt;&gt;&gt;</span> exit()
<span class="gp">(myenv)$</span>
</pre></div>

The greater-than signs `>>>` change back to `(myenv)` followed by `$` or `>`. This tells you that you're back on the system prompt. Now commands like `whoami` and `cd` work again, but Python commands like `1 + 2` won't work. You can re-activate the Python prompt anytime you want by simply typing `python` - as long as you have the virtual environment active! 

To quit the virtual environment, type `deactivate` or `source deactivate`  (for Linux and Mac) -- this time without parentheses.

```console
(myenv)$ deactivate
```

The terminal can be closed by typing `exit`.

```console
$ exit
```

As an exercise, try to run the Python console again - open the command prompt 
(the terminal), then activate the virtual environment, and finally run Python.
