# Print and errors


Now create file <code>~/pyladies/02/printing.py</code> (in editor)
and write there following commands:


```python
print(1)
print(1, 2, 3)
print(1 + 1)
print(3 * 8)
print(10 - 2.2)
print(3 + (4 + 6) * 8 / 2 - 1)
print('*' * 80)
print("Hello" + " " + "PyLadies!")
print("Sum of numbers 3 and 8 is", 3 + 8)
print('Twinkle, twinkle, little star')
print(How I wonder what you are.)
```

Now run the program. Does it work?

## How to read error messages

You will often find out that the code you wrote isn't working on its first run.
It's because computer isn't that smart so you have to write commands in exact way
according to the Python rules. Don't worry it happens even to experienced programmers.
Important is to know how to find what is wrong. The error messages will help you with
that. For example after run our program will print this:


<pre>
  File "<span class="plhome">~/pyladies</span>/02/printing.py", line <span class="err-lineno">11</span>
    print(How I wonder what you are.)
               ^
<span class="err-exctype">SyntaxError</span>: invalid syntax
</pre>

First Python prints name of the file and <span class="err-lineno">line number</span>,
where the error is.
Then it prints the whole line with the mistake.
And finally <span class="err-exctype">error type</span>
(in our case it's "syntax error") and eventually some more info.

> [note] How is this error different from the one that happens when you
> try to add up number and text? Or when you try to divide by zero?

Error messages can be hard to understand from the beginning, but 
you will get used to them with practice.
For now the important thing for you will be the line number.
When you know that the mistake is on line <span class="err-lineno">11</span>,
you can look on that line and try to find it.

When you won't find it there, it can also be few lines above or bellow.
Python sometimes doesn't share human views where the mistake actually *is*
and it shows you where it *noticed* the mistake.

In our case the mistake is that we don't have quotations around
the string. So add them there and run the program again.
If it works, congratulations!
If not try to correct the program and repeat it until it will work :)

## How program works

Now when our program works we can look closely on what is happening
when it's running.
It's quite simple now: commands are performed one after anoter
from the top to the bottom.
Program is like cooking recipe: instructions what to do.

Soon your programs will more look like sorcerer potions 
(*wait for the full moon and if Mars in in conjunction with
Jupiter then stir up three times*) but the principle is still
the same: computer reads commands from the top to the bottom
and performs one after another.

## Print and expressions

And from what instructions are in our "recipe"?

That `print` which we are using is *function*. We will talk
about functions later, now all you need to know is that
if you type `print` and after that into brackets some
*expressions* separated by comma values of that
expressions will be printed.

And what are those expressions?
You have some examples in our code:
expression can be number, string or some (e.g. mathematical)
operation composed of multiple expressions.
For example expression `3 + 8` will add up `3` and `8`.

We will focus on expressions and theur values more in 
lesson about [variables]({{ lesson_url('beginners/variables') }}).

> [style-note] Typography
>
> Notice that there are no spaces around
> the brackets:
> ```python
> print("Hello!")
> ```
>
> But we can write space after comma but not before:
> ```python
> print(1, 2, 3)
> ```
>
> We can also write spaces around mathematics operators:
> ```python
> print(2 + 8)
> print("One and a half is ", 1 + 1/2)
> ```