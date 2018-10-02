# My First Program

```pycon
>>> 3 + 4
7
```

You can issue commands in the *Python interactive console*. 
But it has a disadvantage:
the program that you type is lost when the session ends.
It is good for trying simple commands. 
But you need to save more complex program somewhere. 

Open your editor
(You should have an editor installed. If not, follow the instructions in 
[previous lesson]({{ lesson_url('beginners-en/install-editor')}}).)

Create a new file in your editor and type following code:

```python
print("Hello world!")
```

{% if var('pyladies') -%}
{% set rootname = 'pyladies' %}
{%- else -%}
{% set rootname = 'naucse-python' %}
{%- endif %}

Then save the file as `hello.py`.
* You have to create the subdirectory named `02` in the `pyladies`
(or whatever name of folder you've created last lecture) directory.
* Then you can store the file as `hello.py` into it.

If you can choose the *encoding* in your editor, you should use `UTF-8`.
If you can choose the file type, use `.py` or `All Formats`.

Some operating systems or editors hide extensions or add their own extensions.
You can check the real name using the command line.
Open your command line and change your current directory using the `cd` command to
~/pyladies/02.
List what is in the directory using command `ls` (Mac or Linux) or `dir` (Windows) 
and check that the filename is really `hello.py` and not, for example, `hello.py.txt`.


## Executing Your Program

Open the command line and activate the virtual environment.
Change to the `~/pyladies/02` directory and issue following command:

```console
$ python hello.py
```

> [note]
> You have learned the command line in 
> a [previous lesson](../../beginners-en/cmdline/) which shows how to change the current directory 
> using the `cd` command.
> You know how to activate the virtual environment since the lesson about
> [Python installation](../../beginners-en/install/).

Do you see the greeting? If you do you just wrote your first Python program!

If it does not work, make sure that:

* You have activated the virtual environment.
  (You should the `(venv)` in your command line prompt. If you do not see it, 
  use the `activate` or `source activate` command that you have used in a [previous lession]({{ lesson_url('beginners-en/install') }}).)
* You are in the correct directory: `~/pyladies/02`
  (you need to replace `~/pyladies` with the directory that you have created previously).
* The `hello.py` file contains the correct command, including quotes and parentheses.
* Do not type `$` or `>` characters in the command line – it is there for recognition that it is a command line.
  It is is printed by the operating system after any program had finished.
  You type only: `python hello.py`.

If it still does not work ask 
{% if var('coach-present') -%}
your coach.
{%- else -%}
another developer. <!-- XXX: where to direct people? -->
{% endif %}


> [style-note] Note about code style
>
> It does not usually matter where you use space in Python inside a command. 
> The command `print("Hello world!")` has the same effect as:
>
> ```python
> print      (   "Hello world!"     )
> ```
>
> It is a good practice to follow some typical guidelines.
> In English, we do not write a space after an opening parenthesis.
> In Python, we do not write a space even between `print` and `(`.
> The recommended style is:
>
> ```python
> print("Hello world!")
> ```
>
> The spaces between the quotes have their meaning: if you type
> `"    Hello      world!"`, the extra spaces are printed.
