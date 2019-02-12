# Graphics

Today we will learn how to write graphical applications in Python.

We will use a library that is not built into Python (similar to pytest
which we used for testing). So we have to install it first. Open 
your virtual environment and then use `pip` - specifically the command
`python -m pip install pyglet`.
It looks like this:


```console
(venv)$ python -m pip install pyglet
Collecting pyglet
  Downloading pyglet-1.2.4-py3-none-any.whl (964kB)
Installing collected packages: pyglet
Successfully installed pyglet-1.2.4
```

If you have installed Pyglet successfully, try to run the
following program. A black window should appear.

```python
import pyglet
window = pyglet.window.Window()
pyglet.app.run()
print('Done!')
```

> [note]
> If your window is black but there is some rubbish
> don't mind it now. Before we will start to draw 
> in the window, we will clean it.


Done? Let's explain what is exactly happening.


## Interactive programs

Let's have a look what the program for 1D tic tac toe looks like.
You can see in the comments what every line of code does.


```python
def tictactoe1d():
    field = '-' * 20                # Game preparation
    while True:                     # Loop:
        field = player_move(field)  # 1. Ask player for their move
        if evaluate(field) != '-':  # 2. Evaluate move
            break
        print(field)                # 3. Print what the game looks like now

                                    # And again:
        field = ai_move(field)      # 1. Ask computer for its move
        if evaluate(field) != '-':  # 2. Evaluate move
            break
        print(field)                # 3. Print what the game looks like now
```

We have two types of actions/events in this program, which alternate regularly.
When an action is called, it's then evaluated and printed.

We already had a similar structure of reactions, for example:
rock, paper, scissors.

* Some preparation
* Until program finishes
    * Read some input
    * Evaluate the input
    * Print result

A lot of different programs work similarly, they
respond to input or other actions/events.

A web server is waiting for a *request* for a web page. When it
gets a request, it processes for example a page that is saved on
the disk, and as output, it sends some response.

More complex programs are responding to many 
different actions/events, not only to a "request"
or "player move"/"computer move". What happens after the
input evaluation depends on the type of the action.

For example your web browser is waiting for a mouse click or a keystroke
and it will behave depending on the type of key you press or where you
clicked - maybe it sends a request to the remote server.
And then it's waiting for another action. A response may come from the 
server and then the web browser renders the page
to the screen. Or the user can press "STOP"
and the request is canceled.

Or, a text editor waits for different kidns of input from the keyboard
or mouse, and it has to evaluate every input.

So a similar program structure - a loop that reads the input, 
processes it, and produces output - it is very useful.
It is called *event loop* and programs built on it
are called *event-driven*.

When there is something useful for more programs it is
not usual that each programmer will write it all over from the beginning
but some people write it once, pack it as a *library* and then everyone 
can use it.

## Pyglet 🐷

One of these libraries is Pyglet.
It contains an event loop and some functions for
2D graphics (with help from another library - OpenGL)
and also for retrieving keyboard and mouse events.

Let's go back to the program that opens a window:

```python
import pyglet
window = pyglet.window.Window()
pyglet.app.run()
print('Done!')
```

The whole event loop is hidden in the function `pyglet.app.run()`.
Detecting input (e.g. from keyboard) is something that Pyglet can do
by itself, but the evaluation and drawing of the result is different 
for each program, so you will have to program it by yourself. 

Currently Pyglet is processing only two events:
Closing the window (by pressing the "x" button which is added by the 
operating system) and pressing the <kbd>Esc</kbd> key,
which also closes the window.
After the window is closed, the event loop (function `pyglet.app.run()`)
ends and the program continues to the next line of code.


## Text

The <kbd>Esc</kbd> key is not interesting
so let's have a look at the other keys.

In Pyglet when you want to respond to some event, you have to
write a function and then you *register* it - you tell
Pyglet to call this function at the right time.
An event that happens when the user is writing something
on the keyboard is called `on_text` in Pyglet and it's
processed this way:

{# XXX - highlight "process_text" and "window.push_handlers" blocks #}
```python
import pyglet
window = pyglet.window.Window()

def process_text(text):
    print(text)

window.push_handlers(on_text=process_text)

pyglet.app.run()
```

What does it do? `window.push_handlers(on_text=process_text)`
tells Pyglet that when the user writes something into our
window, Pyglet has to call a function `process_text`. This
function gets one argument containing what the user wrote.

Notice that when we register our function
we are __not__ writing parentheses, although we 
[once]({{ lesson_url('beginners/functions') }}) said
that functions have to be called that way.
Do you remember this example? Maybe you found it weird back then.

```python
from math import sin
print(sin(1))
print(sin)
print(sin + 1)
```

Apart from numbers, strings, `True/False`, we now also know
files, lists, tuples and others. And we can say that a function
in Python is a value like any other.
Numbers can be multiplied, strings can be written into a file,
we can read from files, and functions are only different in that
that they can be called.
But before we call a function, we can store the function
in a variable:

```python
write = print
write("Hello world!")
```

Or we can pass the function to another function as an argument:

```python
print(print)
```

And the function `window.push_handlers` was directly writen to
process a function. Why? Pyglet doesn't need the result
of the function `process_text` - it is useless for it.
And we also can't call the function cause we don't have
useful `text` as an argument.
That's why we give the function itself to Pyglet, and it
is called everytime the user press some key.

## Time ⏲

Before we move to the real graphics, we will have a look
at another type of event.

It's a *clock tick*. That's an event, which is happening
regularly after some time.

Registering a function for ticks is done differently than `on_text`:

{# XXX - highlight "tick" and "schedule_interval" blocks #}
```python
import pyglet
window = pyglet.window.Window()

def tick(t):
    print(t)

pyglet.clock.schedule_interval(tick, 1/30)

def process_text(text):
    print(text)

window.push_handlers(on_text=process_text)

pyglet.app.run()
```

What does it do? `pyglet.clock.schedule_interval(tick, 1/30)`
tells Pyglet that it should call the function `tick` every
`1/30` of a second.

The function `tick` gets only one argument - 
how much time has elapsed since the last call.
Mostly it is not exactly 1/30 of a second, it's a bit
more. Our computer has also other things to do, so it
doesn't get to our program immediately, and it also
takes some time for Python to call our function.

> [note]
> And why 1/30 of a second? Because we will
> create an animation later. When 30 images per second 
> are displayed in front of our eyes, 
> the brain connects them to create an illusion of smooth motion.
> <br>
> Most of the movies are using only 24 pictures per second and
> realistic 3D games have up to 60.

## Drawing 🖌

<img src="{{ static('snake.png') }}" alt="" style="display:block;float:right;">

A program that prints a lot of numbers to the command line
is not really interesting. But today's topic is
graphics so we will slowly get rid off the command line.
Let's draw! :)

Find some picture on the internet. Not too big so we still have
some room in our window. And PNG format would be the best.
You can start for example [here](https://www.google.cz/search?tbs=ift:png&tbm=isch&q=snake+icon).
And don't pick any dark picture because you might not
see it in your dark window.
Save it to the same folder where you have your program. For
example I have saved the picture as `snake.png`.

Then draw the picture (use the name of your image):

{# XXX: Highlight "image =", "snake =", "draw", "on_draw=draw" blocks #}
{# XXX: Highlight 'snake.png' strongly #}
```python
import pyglet
window = pyglet.window.Window()

def tick(t):
    print(t)

pyglet.clock.schedule_interval(tick, 1/30)

def process_text(text):
    print(text)

image = pyglet.image.load('snake.png')
snake = pyglet.sprite.Sprite(image)

def draw():
    window.clear()
    snake.draw()

window.push_handlers(
    on_text=process_text,
    on_draw=draw,
)

pyglet.app.run()
```

Success?

Let's explain what is happening:

* `image = pyglet.image.load('snake.png')` loads the picture from a file
* `snake = pyglet.sprite.Sprite(image)`
  creates a special object, a [Sprite](https://en.wikipedia.org/wiki/Sprite_(computer_graphics)),
  which specifies that we want to "place" our image at a specific
  place in the window. If we didn't do anything else, the image
  would sit in the left corner.
* Our function `draw()` takes care of rendering (drawing into) the window.
  It is called everytime when the window needs to be redrawn - e.g. when you
  minimize the window and then you open it again, or when you move the window
  out of the screen and then you move it back in. Or when we animate
  something.

> [note]
> Some operating systems remember the contents of windows
> that are not visible, but you shouldn't count on it.

* `window.clear()` cleans the window - "paints the window black" and
  deletes everything that was there before.

> [note]
> This is not needed on a lot of computers but it's
> better to write programs so they run correctly
> everywhere.

* `snake.draw()` draws a picture with our prepared `snake` *sprite*.
* `window.push_handlers(on_draw=draw)` registers the function `draw` –
  and tells Pyglet to call it everytime it is needed.
  <br>
  When you need to register more functions to handle events
  you can also add them to the `push_handlers` function like that ↑.

Any drawing *must* be done within the drawing function that
Pyglet calls from `on_draw`. Functions like `clear` and `draw`
won't work anywhere else.

## Animation

Let's play with the Sprite a bit.

Write the following in the function `process_text`:

```python
def process_text(text):
    snake.x = 150
```

Our Sprite has an *attribute* `x` which determines its 
<var>x</var> coordinate - how far to the right it is
from the window edge.
You can set this attribute how ever you want - mostly as
reaction to some event, but it can be also set in the beginning.

Try to add something to `x` everytime the clock ticks.
Are you able to guess how this piece of code will behave?

```python
def tick(t):
    snake.x = snake.x + t * 20
```

If you are not scared of maths, import `math`,
and let the picture move according to some function:

```python
def tick(t):
    snake.x = snake.x + t * 20
    snake.y = 20 + 20 * math.sin(snake.x / 5)
```

What will happen when you change those numbers?

What will happen when you try to set a `rotation` attribute in a similar way?

## Call later

<img src="{{ static('snake2.png') }}" alt="" style="display:block;float:right;">

Pyglet also can call a function after some time.

Download another picture. I have another snake which
is a bit different than the first one.

Once you have the picture in the folder with your
program, add this piece of code right before `pyglet.app.run()`:

{# XXX: Highlight 'snake2.png' strongly #}
```python
image2 = pyglet.image.load('snake2.png')

def change(t):
    snake.image =image2

pyglet.clock.schedule_once(change, 1)
```

Calling `schedule_once(change, 1)` tells Pyglet that it
should call the function `change` after one second.
And this function changes the image - in a similar way as we were
changing the coordinates.

`schedule_once` can be also called when you are handling another
event. Try to replace the function `change` like that:

```python
def change(t):
    snake.image = image2
    pyglet.clock.schedule_once(change_back, 0.2)

def change_back(t):
    snake.image = image
    pyglet.clock.schedule_once(change, 0.2)
```

## Click 🐭

The last event we will learn to handle is clicking.
Write this function right before the `window.push_handlers`:

```python
def click(x, y, button, mode):
    snake.x = x
    snake.y = y
```

… and then register it in the `push_handlers` as `on_mouse_press=click,`.

Try to find out what each argument means by yourself.

> [note] Help
> * If you don't get rid of the command line completely
> you can use `print`. So everytime you want to find out some
> value, use print.
> * How many buttons does a mouse have?
> * What happens when the user <kbd>Shift</kbd>+clicks?


## To be continued

We wrote enough code, so we can end this lesson:

```python
import math

import pyglet

window = pyglet.window.Window()

def tick(t):
    snake.x = snake.x + t * 20

pyglet.clock.schedule_interval(tick, 1/30)

def process_text(text):
    snake.x = 150
    snake.rotation = snake.rotation + 10

image = pyglet.image.load(snake.png)
snake = pyglet.sprite.Sprite(image, x=10, y=10)

def draw():
    window.clear()
    snake.draw()

def click(x, y, button, mode):
    print(button, mode)
    snake.x = x
    snake.y = y

window.push_handlers(
    on_text=process_text,
    on_draw=draw,
    on_mouse_press=click,
)

image2 = pyglet.image.load('snake2.png')

def change(t):
    snake.image = image2
    pyglet.clock.schedule_once(change_back, 0.2)

def change_back(t):
    snake.image = image
    pyglet.clock.schedule_once(change, 0.2)

pyglet.clock.schedule_once(change, 0.2)

pyglet.app.run()
```

With keystroke and mouse input, timing, and rendering of Sprites, 
you can create a simple game or graphics application.

When you write some game, try to keep the state of the
application (basically how the window should look)
in lists and tuples (or in dictionaries or classes).
One function should draw this state, and another function
should manipulate (change) it.
To avoid confusion, you can also have those two functions 
in different files.

If you are interested in this topic, you can try to play and examine this
[Pong](static/pong.py) code, which shows more Pyglet options: writing text, 
drawing rectangles and handling specific keys (e.g. arrows).
It may seem difficult, but just look at the comments (currently with A LOT of grammar
errors) and try to understand it. If the comments are not enough for you
to understand, we will also translate [the more detailed 
materials for it]({{ lesson_url('beginners-en/pong') }}) 

You can find the things that we've learned today (and some more) in the
[Pyglet cheatsheet](https://github.com/muzikovam/cheatsheets/blob/master/pyglet/pyglet-basics-en.pdf),
which you can download and print out.

And if you want to dive deeper into Pyglet, there is also
[documentation](http://pyglet.readthedocs.org/en/latest/index.html).
If anything in there isn't clear, just ask!
