
# ![Python](static/python.png) ![Turtle](static/turtle.png)

In this lesson we will be drawing with *turtle* module.

Run Python in *interactive mode* (after you activate Conda write Python in command line).

```pycon
$ python

>>>
```

> [note]
> Characters `>` and `$` are written by compouter, not you.
> On Windows there will be `>` instead of `$` and
> before`$`or `> ` there can be something else.

Then write:

```python
from turtle import forward

forward(50)
```

Now a popup window will appear, don't close it.
Place it somewhere where you will be able to see it and
your command line, too.

## Where is the turtle?

Now the turtle is disguised as an arrow.
There is a way how to unmask it:

```python
from turtle import shape

shape('turtle')
```


## Rotation

Turtle can rotate and crawl on "paper".
It has brush on its tail which is drawing a line.

```python
from turtle import left, right

forward(50)
left(60)
forward(50)
right(60)
forward(50)
```

Now give turtle some commands.
If you won't like the drawing you can close
the window or import and use functionv`clear()`.


## Turtle program

Interactive mode is good for trying new stuff
but we will now go back to our editors
and write some program in file.

Create a file <code>~/pyladies/03/drawing.py</code>.

> [note]
> Directory <code>~/pyladies</code> can have a different name on your laptop
> – see [Python installation]({{ lesson_url('beginners/install') }}).

You can have a different name for your file
but don't use `turtle.py`.

Write commands for drawing into the
file and in the end call function `exitonclick`
(imported from module `turtle`).

> [note] Question
> What is doing function <code>exitonclick</code>?

After you are done we can start with drawing pictures:

### Square

Draw a square.

![Turtle square](static/turtle-square.png)

Square has 4 equal straight sides
and 4 90° angles.

{% filter solution %}
```python
from turtle import forward, left, exitonclick

forward(50)
left(90)
forward(50)
left(90)
forward(50)
left(90)
forward(50)
left(90)

exitonclick()
```
{% endfilter %}

### Rectangle

Draw rectangle.

Try to make it that turtle will "look" to the right in the end (like it was in the beginning).

![Turtle rectangle](static/turtle-rect.png)

{% filter solution %}
```python
from turtle import forward, left, exitonclick

forward(100)
left(90)
forward(50)
left(90)
forward(100)
left(90)
forward(50)
left(90)

exitonclick()
```
{% endfilter %}

### Three squares

Now draw three sqares, each rotated by 20°.

![Three turtle squares](static/turtle-squares.png)

{% filter solution %}
```python
from turtle import forward, left, exitonclick

forward(50)
left(90)
forward(50)
left(90)
forward(50)
left(90)
forward(50)
left(90)

left(20)

forward(50)
left(90)
forward(50)
left(90)
forward(50)
left(90)
forward(50)
left(90)

left(20)

forward(50)
left(90)
forward(50)
left(90)
forward(50)
left(90)
forward(50)
left(90)

exitonclick()
```
{% endfilter %}

### Can we write it better?

So much code! There have to be a way how to simplify it.

There is.
Now we will learn command `for`.

## Repetition

What is following code doing?
Save it as
<code>~/pyladies/03/loop.py</code>

```python
for number in range(5):
    print(number)

for greeting in 'Ahoj', 'Hello', 'Hola', 'Hei', 'SYN':
    print(greeting + '!')
```

What is command `for` doing?

{% filter solution %}
Command `for` is repeating part of a program.
It repeats command that are intended after `for`.
It's same as with `if` - it's applied only for
commands that are intended below.

Command `for x in range(n):` repeats commands bellow <var>n</var> times
and it sets variable `x` gradually from 0 to n-1.

Command `for x in a, b, c, d, ...:` repeates commands bellow;
it sets variable `x` gradually to <var>a</var>, <var>b</var>,
<var>c</var> <var>d</var>, ...
{% endfilter %}

### Overwriting variables

What is following program doing?

```python
sum = 0

for number in 8, 45, 9, 21:
    sum = sum + number

print(sum)
```

{% filter solution %}
Command `sum = sum + number` calculates the value of
`sum + cislo`, adds up current number to sum
and stores the result into variable `sum`.
New value of `sum` will be used in the next loop.

In the beginning the sum is 0 and in the end the sum of
our numbers will be printed.
{% endfilter %}

### Square

Back to drawing! This time we will use loops.

Draw a square.

Use `forward` only twice, once in import
and once as function.

![Turtle square](static/turtle-square.png)

{% filter solution %}
```python
from turtle import forward, left, exitonclick

for i in range(4):
    forward(50)
    left(90)

exitonclick()
```
{% endfilter %}

### Discontinuous line

Functions `penup` and `pendown` from `turtle`
module tell the turtle to stop/start with drawing.

Try to draw discontinuous line.

![Turtle and discontinuous line](static/turtle-dashed.png)

{% filter solution %}
```python
from turtle import forward, penup, pendown, exitonclick

for i in range(10):
    forward(10)
    penup()
    forward(5)
    pendown()

exitonclick()
```
{% endfilter %}

Now try to make it that lines that are drawn were
gradually bigger.

![Turtle and discontinuous line]](static/turtle-dashed2.png)

> [note] Help
>
> What exactly is command `for` doing?
> Can we use variable that it sets up?

{% filter solution %}
```python
from turtle import forward, penup, pendown, left, exitonclick

for i in range(20):
    forward(i)
    penup()
    forward(5)
    pendown()

exitonclick()
```
{% endfilter %}

### Three squares

In the end draw 3 squares, each rotated by 20°.
Now you know how to write it simple: repeat the code
by using `for`, do not copy the code. 

![Three turtle squares](static/turtle-squares.png)

{% filter solution %}
```python
from turtle import forward, left, right, speed, exitonclick

for i in range(3):
    for j in range(4):
        forward(50)
        left(90)
    left(20)

exitonclick()
```
{% endfilter %}


## Extra tasks

If you are done try to draw a stairs:

![Turtle stairs](static/turtle-stairs.png)

If you are also done with stairs try to draw 7 hexagons:

![Želví plástev](static/turtle-hexagons.png)
