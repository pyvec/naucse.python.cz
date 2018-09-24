{%- macro sidebyside(titles=['Unix', 'Windows']) -%}
    <div class="row side-by-side-commands">
        {%- for title in titles -%}
            <div class="col">
                <h4>{{ title }}</h4>
{%- filter markdown() -%}
```{%- if title.lower().startswith('win') -%}dosvenv{%- else -%}console{%- endif -%}
{{ caller() | extract_part(loop.index0, '---') | dedent }}
```
{%- endfilter -%}
            </div>
        {%- endfor -%}
    </div>
{%- endmacro -%}

{%- if var('pyladies') -%}
{% set purpose = 'PyLadies' %}
{% set dirname = 'pyladies' %}
{%- else -%}
{% set purpose = 'Python' %}
{% set dirname = 'naucse-python' %}
{%- endif -%}


# Command line

The following steps will show you how to use the black window all 
hackers use. It might look a bit scary at first but really it's 
just a prompt waiting for commands from you.

What is the command line?
The window, which is usually called the *command line* or *command-line interface*, 
is a text-based application for viewing, handling, and manipulating files on your computer. 
It’s much like Windows Explorer or Finder (Mac), but without the graphical interface. 
Other names for the command line are:
*cmd*, *CLI*, *prompt*, *console* or *terminal*.

How can I open it?

* Windows (English): Start → write "cmd" → Command prompt
* Windows (older versions): Start menu → All programs → Accessories → Command prompt
* macOS (English): Applications → Utilities → Terminal
* Linux (KDE): Main Menu → search for Console
* Linux (GNOME): Super → search for Terminal

If you don't know what to do, you can try Google, ask the coach,
or you can e-mail us.


When you open the command line, you should see a white or black window that is waiting for your command.
Each command will be prepended by the sign `$` or `>` (depending on your operating system) 
and one space, but you don’t have to type this prompt. 
Your computer will do it for you.


{% call sidebyside(titles=['Unix (Linux, macOS)', 'Windows']) %}
$
---
>
{% endcall %}

Each operating system has slightly different set of commands for the command line, 
so make sure to follow the instructions for your operating system.


> [note] Font size (Windows)
> If your font is too small you can click on the small window icon in the up right corner.
> Then choose Properties and find the Font tab where you can set a different font size.
>
> {{ figure( img=static('windows-cmd-properties.png'), alt='Screenshot of command line window', ) }}
>
> In other operating systems, you can try:
> <kbd>Ctrl</kbd>+<kbd>+</kbd> and
> <kbd>Ctrl</kbd>+<kbd>-</kbd> (+ Shift).


## First command

We will start with a very easy command.
Write `whoami` (*who am I?*)
and press <kbd>Enter</kbd>.
Your user ID will be shown. For example on Alex' computer, it looks like this:

{% call sidebyside() %}
$ whoami
Alex
---
> whoami
PCname\Alex
{% endcall %}

## Working directory

The command line always works from a *directory* (also *folder*).
We can print our working directory (also called current directory) by using the command `pwd` (Linux, MacOS)
or `cd` (Windows). `pwd` means *print working directory* and `cd` stands for *current directory*

{% call sidebyside() %}
$ pwd
/home/Alex/
---
> cd
C:\Users\Alex
{% endcall %}

The current directory is often also displayed before `$` or `>`, but it's
good to know this command in case that you get lost or if you have to
work on a computer that is set to display something different before `$`.


## So what's in that directory?

Command `ls` or `dir` (*list* or *directory*)
will show us what's in the current directory: all files and
subfolders.

{% call sidebyside() %}
$ ls
Applications
Desktop
Downloads
Music
…
---
> dir
 Directory of C:\Users\Alex
05/08/2014 07:28 PM <DIR>  Applications
05/08/2014 07:28 PM <DIR>  Desktop
05/08/2014 07:28 PM <DIR>  Downloads
05/08/2014 07:28 PM <DIR>  Music
…
{% endcall %}


## Change current directory

You can chnage your current directory by using the command `cd` (*change directory*) -
for all OSs (in Windows, if you don't specify anything after `cd`, command 
prints the *current directory* as we said earlier)
So after `cd` we have to write the folder's name where we want to go.
Don't forget to check if you were successful.

If you have Linux or macOS, be careful - those systems are case sensitive,
so `Desktop` and `desktop` are two different folders!


{% call sidebyside() %}
$ cd Desktop
$ pwd
/home/Alex/Desktop
---
> cd Desktop
> cd
C:\Users\Alex\Desktop
{% endcall %}

> [note] Note for Windows users
> If you change directories to a different disk (to `D:` from `C:`)
> you have to enter the disk's name (`D:`) as a special command before
> you enter `cd`.

## Create directory

How about creating a practice directory on your Desktop? You can do this by using the
command `mkdir` (*make directory*).
After that command, write the name of the folder that you want to create -
in our case `practice`.


{% call sidebyside() %}
$ mkdir practice
---
> mkdir practice
{% endcall %}

Now, look on your Desktop or into some other graphical program
for browsing folders, and check if the folder was created!

## Task
In your new `practice` directory, try to create a subfolder `test` and check
if it was created.

The commands `cd`, `mkdir` and `ls` or `dir` might help you.

{% filter solution %}
{% call sidebyside() %}
$ cd practice
$ mkdir test
$ ls
test
---
> cd practice
> mkdir test
> dir
05/08/2014 07:28 PM <DIR>  test
{% endcall %}
{% endfilter %}


## Cleaning

We don't want to leave a mess, so let's remove everything we did until that point.

But you can't delete the folder in which you currently are.
First, we need to get back to the Desktop. We can't use `cd Desctop` because in the current
folder, there is no Desktop.
So we have to go to the *parent directory* which contains the folder that you are
currently in.
Two dots stand for the parent directory.

{% call sidebyside() %}
$ pwd
/home/Alex/Desktop/practice
$ cd ..
$ pwd
/home/Alex/Desktop
---
> cd
C:\Users\Alex\Desktop\practice
> cd ..
> cd
C:\Users\Alex\Desktop
{% endcall %}

Now it's time to delete the `practice` directory.
For that purpose, use `rm` or `rmdir`
(*remove* or *remove directory*).

> [warning] Warning!
> The command line does not have a Recycle Bin! Everything will be deleted for good.
> Every time, make sure that you are deleting the right folder.

In Unix, you have to write `rmdir -rv` (minus,`r`, `v`). The parameter deletes everything
(`r` - *recursive*) inside the folder, and it prints info telling you (`v` - *verbose*) 
what the command is doing.

In Windows, you also have to add a switch to the `rm` command to delete everything inside a
directory. Here, the switch is `/S` (forward slash, `S`).

{% call sidebyside() %}
$ pwd
/home/Alex/Desktop
$ rm -rv practice
removed directory: ‘practice’
---
> cd
C:\Users\Alex\Desktop
> rmdir /S practice
practice, Are you sure <Y/N>? Y
{% endcall %}


## Summary

There is a table of basic commands:

<table class="table">
    <tr>
        <th>Unix</th>
        <th>Windows</th>
        <th>Description</th>
        <th>Example</th>
    </tr>
    <tr>
        <td><code>cd</code></td>
        <td><code>cd</code></td>
        <td>change directory</td>
        <td><code>cd test</code></td>
    </tr>
    <tr>
        <td><code>pwd</code></td>
        <td><code>cd</code></td>
        <td>show the current directory</td>
        <td><code>pwd</code><br><code>cd</code></td>
    </tr>
    <tr>
        <td><code>ls</code></td>
        <td><code>dir</code></td>
        <td>list directories/files</td>
        <td><code>ls</code><br><code>dir</code></td>
    </tr>
    <tr>
        <td><code>cp</code></td>
        <td><code>copy</code></td>
        <td>copy a file</td>
        <td>
            <code>cp original.txt copy.txt</code>
            <br>
            <code>copy cp original.txt copy.txt</code>
        </td>
    </tr>
    <tr>
        <td><code>mv</code></td>
        <td><code>move</code></td>
        <td>move a file</td>
        <td>
            <code>mv old.txt new.txt</code>
            <br>
            <code>move old.txt new.txt</code>
        </td>
    </tr>
    <tr>
        <td><code>mkdir</code></td>
        <td><code>mkdir</code></td>
        <td>create a new directory</td>
        <td><code>mkdir test</code></td>
    </tr>
    <tr>
        <td><code>rm</code></td>
        <td><code>del</code></td>
        <td>delete a file</td>
        <td><code>rm test.txt</code><br><code>del test.txt</code></td>
    </tr>
    <tr>
        <td><code>rmdir /S</code></td>
        <td><code>rm -rv</code></td>
        <td>delete a directory</td>
        <td><code>rm -rv testdir</code></td>
    </tr>
    <tr>
        <td><code>exit</code></td>
        <td><code>exit</code></td>
        <td>close the window</td>
        <td><code>exit</code></td>
    </tr>
</table>

There are of course a lot more commands.
All the programs that you have installed on your laptop can be
run from the command line - usually by typing their names.
Try for example - `firefox`, `notepad`, `safari`, or `gedit`.
{% if var('coach-present') -%}
If it's not working, ask your coach and they might help you to find an example command that works.
{%- endif %}

We will use commands/programs like `python` and `git` a lot. We will install them
in a while.
<!--- XXX: this assumes installation is after intro to cmdline -->


## Exit

Now you can try one more command - the one that closes the command line window - `exit`.
It works the same in all operating systems.


```console
$ exit
```
We will be using `$` to indicate Linux/macOS (in fact, for Unix based OS) commands
and `>` to indicate Windows commands for the rest of our course.
This is the convention in most materials and tutorials you will find.


