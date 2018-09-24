

If you would try to do some calculations with the number π (pi), how would you write it?
3.14159265 ?

However, Python has a lot of built-in features, so you don’t have to rewrite them
you just have to know where to look.<br>
We can access *π* by importing the `math` module.


```python
from math import pi

print(pi)
```

As you can see, π is a bit hidden. Comparing to `print` or `if` which everyone needs, 
not everyone needs `math`. Let's stick with this module for a bit longer.


## Expressions

In mathematics we have a lot of different operations that are implemented as 
symbols, like + or -. The same symbols are used in Python.

* 3 + 4
* <var>a</var> - <var>b</var>

It's a bit difficult with multiplying and dividing
because you can't write the usual mathematical expression
on keyboard:

* 3 · 4
* ¾

Mathematicians were inventing more and more complex symbols 
that cannot be just as easily replicated by programmers:


* <var>x</var>²
* <var>x</var> ≤ <var>y</var>
* sin θ
* Γ(<var>x</var>)
* ∫<var>x</var>
* ⌊<var>x</var>⌋
* <var>a</var> ★ <var>b</var>
* <var>a</var> ⨁ <var>b</var>

There are also programming languages that needs
special keyboard. But their programs can't be easily 
written and they aren't readable.

> [note]
> For example this is program written in language APL:
>
> <!--z http://catpad.net/michael/apl/ -->
>
>     ⍎’⎕’,∈Nρ⊂S←’←⎕←(3=T)∨M∧2=T←⊃+/(V⌽”⊂M),(V⊖”⊂M),(V,⌽V)⌽”(V,V←1¯1)⊖”⊂M’


There are relatively a few operators in Python.
And we already know almost half of them!
Some operators are words.
There are all of them:

<div>
    <code>==</code> <code>!=</code>
    <code>&lt;</code> <code>&gt;</code>
    <code>&lt;=</code> <code>&gt;=</code>
    <code class="text-muted">|</code> <code class="text-muted">^</code>
    <code class="text-muted">&amp;</code>
    <code class="text-muted">&lt;&lt;</code> <code class="muted">&gt;&gt;</code>
    <code>+</code> <code>-</code>
    <code>*</code> <code class="text-muted">@</code> <code>/</code>
    <code>//</code> <code>%</code>
    <code class="text-muted">~</code>
    <code>**</code>
    <code class="text-muted">[ ]</code> <code class="text-muted">( )</code>
    <code class="text-muted">{ }</code>
    <code class="text-muted">.</code>
</div>

<div>
    <code class="muted">lambda</code>
    <code class="muted">if else</code>
    <code>or</code> <code>and</code> <code>not</code>
    <code class="muted">in</code> <code class="muted">not in</code>
    <code class="muted">is</code> <code class="muted">is not</code>
</div>

It is clear now that some operations that we want to do in the program 
cannot be expressed by the operators.


How to deal with that?

One of the way which we already mentioned is to define operation in words.

* <var>x</var> = sin <var>a</var>

And we can write that on our keyboards!
We just have to add parentheses (some editors will do it for us) to make it 
clear to whom the operation applies:

```python
x = sin(a)
```

But first of all you have to *import* `sin`,
same way as you already imported `pi`.
So the whole program will look like this:

```python
from math import sin

x = sin(1)  # (in radian)
print(x)
```

> [warning] Import and files names
> When we want to import some module we have to pay extra attention
> when we are naming our files with programs.
> If you are importing in your program module `math` your file can't
> have name `math.py`.
>
> Why? Because if you are importing some module Python will look firstly
> into the folder from which you are running the program.
> It will find the `math.py` and will try to import `sin` function from there.
> And of course it won't find it.


## Call functions

We call the function by its *name*.

The name looks like a variable – actually it *is* a variable, 
only difference is that instead of a number or a string, we have a function stored inside.

After the name of the function we have parentheses where we enclose the *argument* 
(or *input*) for the function. This is the information which our function will work with.
In our example, `sin()` will calculate the <em>sine</em>

The *return value* of a function is value that can be
signed to a variable.


```
        function name
                 │
                ╭┴╮
            x = sin(1)
            ▲      ╰┬╯
            │     argument
            │
            ╰── return value 
```

Or we can use it in other operations:

```python
a = sin(1) + cos(2)
```

Or we can use it in an `if` condition:

```python
if sin(1) < 3:
```

Or even use it as an input for a different function:

```python
print(sin(1))
```

… etc.


### Arguments

To some functions we can pass multiple arguments. For example, `print`, 
which prints all its arguments consecutively. We separate the arguments by comma:

```python
print(1, 2, 3)
```

```python
print("One plus two equals", 1 + 2)
```
Some functions do not need any argument. 
It can be also `print`, but we still have to write the parentheses, even if they are empty.
Guess what `print` without arguments will do?

```python
print()
```

{% filter solution %}
Function `print` without arguments will print empty line.

It's exactly by the definition - function `print` will write all
its argument on a line.
{% endfilter %}

### Functions have to be called

Be careful to write the parentheses, otherwise, the function is not called. 
You will not get the return value, but the function itself! Let’s try the following examples:

```python
from math import sin
print(sin(1))
print(sin)
print(sin + 1)
```

### Named arguments

Some functions can also work with *named* arguments. 
They are written similarly to the assignment of a variable, with an equal, 
but inside the parentheses:

For example function `print` ends with printing new line at the end of a line by default,
but we can rewrtite it by named argument `end` and print something else.

> [note]
> We have to write this into .py file because we won't
> be able to see it properly in the interactive console.

```python
print('1 + 2', end=' ')
print('=', end=' ')
print(1 + 2, end='!')
print()
```

## Useful functions

In the end we will look at some basic functions which are built-in.
You can also download 
<a href="https://github.com/muzikovam/cheatsheets/blob/master/basic-functions/basic-functions-en.pdf">cheatsheet</a>.


### Input and output

We already know these functions.
`print` writes non-named arguments separated by space into the output.
It will  write named argument `end` in the end of a line (default is newline).
And another named argument `sep` defines what will be written between each argument (default is space).


> [note]
> We recommend to run following example
> from the file, not from Python console.

```python
print(1, "two", False)
print(1, end=" ")
print(2, 3, 4, sep=", ")
```

Basic function for input is obviously `input`.
It will print the question (or whatever you type in)
and collect the input from the user and return it
as a string.

```python
input('Enter input: ')
```

### Type conversion (type casting)

In case we don’t want to work just with strings, here is a group of 
functions that can convert strings to numbers and back.
But what to do when we don't won't to work with a string but for example with a number?
With that will help a group of functions that can convert strings to numbers and back.
Each from three <em>types</em> of variables that we currently know
has function which takes some value (as an argument) and returns it as a
value its own type. 
For *integers* there is function `int()`, for *floating points* there is
`float` and for *strings* there is `str()`.


```python
int(x)              # conversion to integer
float(x)            # conversion to real number
str(x)              # conversion to string
```

Examples:

```python
3 == int('3') == int(3.0) == int(3.141) == int(3)
8.12 == float('8.12') == float(8.12)
8.0 == float(8) == float('8') == float(8.0)
'3' == str(3) == str('3')
'3.141' == str(3.141) == str('3.141')
```
But not all conversions are possible:

```python
int('blablabla')    # error!
float('blablabla')  # error!
int('8.9')          # error!
```

We will tell you how to deal with errors some other time.


### Mathematical functions

Maths is sometimes useful so let's have a look how to work 
with numbers in Python :)

There is one mathematical function which is always available:

```python
round(number)    # rounding
```

Lots of others are imported from the `math` module:

```python
from math import sin, cos, tan, sqrt, floor, ceil

sin(angle)       # sine
cos(angle)       # cosine
tan(angle)       # tangent
sqrt(number)     # square root

floor(angle)    # rounding down
ceil(angle)     # zaokrouhlení nahoru
```

### Help

There are some more functions that are helping programmers:
You can get help regarding a specific function from program 
itself (or Python console) by using the help function.
It's sometimes usual even for beginners, but if
not - use Google.

Help will be shown, regarding operating system,
either in browser or right in terminal.
If the help is too long for the terminal you can move pages there by
 (<kbd>↑</kbd>, <kbd>↓</kbd>,
<kbd>PgUp</kbd>, <kbd>PgDn</kbd>) and you can get "out" with
key <kbd>Q</kbd> (like *Quit*).

You can get help for <code>print</code> like that:

```python
help(print)
```

You can also get help to the whole module:.

```python
import math

help(math)
```

### Random

Last but not least we will look on two functions from
`random` which are very useful for games.

```python
from random import randrange, uniform

randrange(a, b)   # random integer from a to b-1
uniform(a, b)     # random float from a to b
```

Beware that the <code>randrange(a, b)</code> never returns <code>b</code>. 
If we need to randomly choose between 3 options, use <code>randrange(0,3)</code> 
which returns <code>0</code>, <code>1</code>, nebo
<code>2</code>:


```python
from random import randrange

number = randrange(0, 3)  # number - 0, 1, or 2
if number == 0:
    print('Circle')
elif number == 1:
    print('Square')
else:  # 2
    print('Triangle')
```

> [note]
> Remember that when you are importing `random` module you can't 
> name your file `random.py`.


### And more...
There are a lot more functions within Python itself,
although you probably won't understand them from the beginning.
All of them are in Python documentation, e.g.:
<a href="https://docs.python.org/3/library/functions.html">built-in</a>,
<a href="https://docs.python.org/3/library/math.html">maths</a>.
