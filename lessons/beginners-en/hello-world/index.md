# My First Program

```pycon
>>> 3 + 4
7
```

You can issue commands in the _Python interactive console_. 
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

Then save the file as <code><span class="pythondir">~/{{ rootname }}</span>/02/hello.py</code>.
You need to replace <code class="pythondir">~/{{ rootname }}</code> with the name of the directory that you create in the past when you have 
[installed Python](../../beginners-en/install/).
You have to create the subdirectory named `02` in it.
Then you can store the file as `hello.py` into it.

If you can choose the _encoding_ in your editor, you should use `UTF-8`.
If you can choose the file type, use `.py` or `All Formats`.

Some operating systems or editors hide extensions or add their own extensions.
You can check the real name using the command line.

Open your command line and change your current directory using the `cd` command to
<code><span class="pythondir">~/{{ rootname }}</span>/02</code>.
List what is in the directory using command `ls` (Mac or Linux) or `dir` (Windows) and check that the filename is really `hello.py` and not, for example, `hello.py.txt`.


## Executing Your Program

Open the command line and activate the virtual environment.
Change to the <code><span class="pythondir">~/{{ rootname }}</span>/02</code> directory and issue following command:

```console
$ python hello.py
```

> [note]
> You have learned the command line in 
> a [previous lesson](../../beginners-en/cmdline/) that shows how to change the current directory using the `cd` command.
> You know how to activate the virtual environment since the lesson about
> [Python installation](../../beginners-en/install/).

Do you see the greeting? If you do you just wrote your first Python program!

If it does not work, make sure that:

* You have activated the virtual environment.
  (You should the <code>(venv)</code> in your command line prompt. If you do not see it, 
  use the `activate` command that you have used in a [previous lession]({{ lesson_url('beginners-en/install') }}).)
* You are the correct directory: <code><span class="pythondir">~/{{ rootname }}</span>/02</code>
  (you need to replace <span class="pythondir">~/{{ rootname }}</span> with the directory that you have created previously).
* The `hello.py` file contains the correct command, including quotes and parentheses.
* Do not type `$` characters – it just denotes that there is a command line prompt.
  It is the end of the prompt that is printed by the operating system.
  You type only: `python hello.py`.

If it still does not work ask 
{% if var('coach-present') -%}
your teacher.
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
