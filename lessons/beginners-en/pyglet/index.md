# Graphics

Today we will learn how to write graphical applications in Python.

We will use library that is not built-in Python (similar to pytest
which we used for testing). So we have to install it first. open 
your virtual environment and then use `pip` - specifically command -
`python -m pip install pyglet`.
It looks like this:


```console
(venv)$ python -m pip install pyglet
Collecting pyglet
  Downloading pyglet-1.2.4-py3-none-any.whl (964kB)
Installing collected packages: pyglet
Successfully installed pyglet-1.2.4
```

If you installed Pyglet successfully try to run
following program. There should appear
black window.

```python
import pyglet
window = pyglet.window.Window()
pyglet.app.run()
print('Done!')
```

> [note]
> If your window is black but there is some rubbish
> don't mind it now. Before we will start to draw 
> in the window we will clean it.


Done? Let's explain what is exactly happening.


## Interactive programs

Let's have a look how program for 1D tic tac toe looks like.
You can see in the comments what every line of code is
doing.


```python
def tictactoe1d():
    field = '-' * 20                # Game preparation
    while True:                     # Repetition:
        field = player_move(field)  # 1. Ask player about their move
        if evaluate(field) != '-':  # 2. Evaluate move
            break
        print(field)                # 3. Print how game looks like

                                    # And again:
        field = ai_move(field)      # 1. Ask computer about its move
        if evaluate(field) != '-':  # 2. Evaluate move
            break
        print(field)                # 3. Print how game looks like
```

We have two types of actions/events in this program, which alternate regularly.
When action is called, it's then evaluated and printed.

We already had similar structure of reactions, for example:
rock, paper, scissors.

* Some preparation
* Until program finishes
    * Read some input
    * Evaluate the input
    * Print result

And similarly works a lot of different programs which
somehow respond to input or other actions/events.

Web server is waiting for *request* about web page. When it
gets some, it will process for example page that is saved on
disk and as output it sends some response.

More complex programs are responding to a lot
of sorts of actions/events, not only to "request"
or "player move"/"computer move". What happens after
input evaluation depends on type of the action.

Your web browser is waiting for a mouse click or a keystroke
and it will behave by the type of key you press or where you
clicked - maybe it sends request to the remote server.
And then it's waiting for another action. There may come a response from
server and then the web browser renders the page
to the screen. Or the user can press "STOP"
and the request is canceled.

The text editor waits for different input from the keyboard
or mouse and it has to evaluate every input.


So a similar program structure - loop that reads the input, 
processes it and produces output - it is very useful.
It is called *event loop* and programs built on it
are *event-driven*.

When there is something useful for more programs it is
not usual that each programmer will write it all over from the beginning
but some people write it once, pack it as a *library* and then everyone 
can use it.

## Pyglet 🐷

One of such libraries is Pyglet.
It contains event loop and some functions for
2D graphics(with help of another library - OpenGL)
and also retrieving keyboard and mouse events.

Let's go back to the program that opens a window:

```python
import pyglet
window = pyglet.window.Window()
pyglet.app.run()
print('Done!')
```

The whole event loop is hidden in function `pyglet.app.run()`.
Loading of an input (e.g. from keyboard) is Pyglet doing
itself but evaluation and drawing the result is for each program
different so you will have to program it by yourself. 

Currently Pyglet is processing only two events:
closing of the window (by "x" button which is added by 
operating system) and pressing <kbd>Esc</kbd> key,
which also closes the window.
After the window is closed event loop (function `pyglet.app.run()`)
ends and program continues to the next line of code.


## Text

<kbd>Esc</kbd> key is not interesting
so let's have a look on another keys.

In Pyglet when you want respond to some event you have to
write a function and then you *register* it - you tell
Pyglet to call this function in the right time.
Event that happens when user is writing something
on keyboard is called `on_text` in Pyglet and it's
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

What is it doing? `window.push_handlers(on_text=process_text)`
tells Pyglet that when user writes something into our
window Pyglet have to call function `process_text`. This
function gets one argument with what user wrote.

Notice that when we are registering our function
we are __not__ writing brackets although we 
[once]({{ lesson_url('beginners/functions') }}) said
that functions have to be called that way.
Do you remember this example? Maybe you found it weird back then.

```python
from math import sin
print(sin(1))
print(sin)
print(sin + 1)
```

Now when we know apart from numbers, strings, `True/False` also
files, lists, tuples and others we can say that function
in Python is value like every other.
Numbers can be multiplied, strings can be written into a file,
we can read from files and functions are only different by that
that they can be called.
But before we call function we can store the function
into some variable:

```python
write = print
write("Hello world!")
```

or we can pass a function to another function as an argument:

```python
print(print)
```

And function `window.push_handlers` was directly writen to
process a function. Why? Pyglet doesn't need one result
of function `process_text` - it is useless for it.
And we also can't call the function cause we don't have
useful `text` as an argument.
That's why we give to Pyglet the function itself and it
will be called everytime user press some key.

## Time ⏲

Before we move to the real graphics we will have a look
on another type of event.

It's a *clock tick*). That's an event, which is happening
regularly after some time.

Registration of function for ticks is done differently than `on_text`:

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

What is it doing? `pyglet.clock.schedule_interval(tick, 1/30)`
tells Pyglet that it should cal the function `tick` every
`1/30` of a second.

Function `tick` gets only one argument - 
how much time has elapsed since the last call.
Mostly it is not exactly 1/30 of a second, it's a bit
more. Computer has also another things to do, so it
doesn't get to our program immediately and it also
takes some time for Python to call our function.

> [note]
> And why 1/30 of a second? Because we will
> create animation later. When 30 images per second 
> are replaced in front of our eyes, 
> the brain connects them to create an illusion of smooth motion.
> <br>
> Most of the movies are using only 24 pictures per second and
> realistic 3D game has up to 60.

## Drawing 🖌

<img src="{{ static('snake.png') }}" alt="" style="display:block;float:right;">

Program that prints a lot of number to a command line
is not really interesting. But today's topic is
graphics so we will slowly get rid off the command line.
Let's draw! :)

Find some picture on the internet. Not too big so we still have
some room in our window. And PNG format would be the best.
You can start for example [here](https://www.google.cz/search?tbs=ift:png&tbm=isch&q=snake+icon).
And don't pick any dark picture because you might not
see it in your dark window.
Save it to the same folder where you have your program. For
example I have the picture saved as `snake.png`.

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

* `image = pyglet.image.load('snake.png')` loads picture from file
* `snake = pyglet.sprite.Sprite(image)`
  creates special object [Sprite](https://en.wikipedia.org/wiki/Sprite_(computer_graphics)),
  which specifies that we want to "put" our image to a specific
  place in the window. If we wouldn't do anything else the image
  will wait in the left corner.
* Our function `draw()` takes care of rendering(drawing into) the window.
  It is called everytime when a window needs to be redrawn - e. g. when you
  minimize the window and then you open it again or when you move the window
  out of the screen and then you move it back in. Or when we will animate
  something.

> [note]
> Some operating systems remembers content of windows
> that are not visible but you shouldn't count on it.

* `window.clear()` cleans the window - "paints the window black" and
  deletes everything what was there before.

> [note]
> It's not needed on a lot of computers but it's
> better to write programs so they run correctly
> everywhere.

* `snake.draw()` draws a picture with prepared `snake` *sprite*.
* `window.push_handlers(on_draw=draw)` registers function `draw` –
  tells Pyglet to call it everytime it is needed.
  <br>
  When you need to register more functions to handle events
  you can add them to `push_handlers` function like that ↑.

Any drawing *must* be done within the drawing function that
Pyglet calls from `on_draw`. Functions like `clear` and `draw`
won't work anywhere else.

## Animation

Let's play with Sprite a bit.

Write to function `process_text` following:

```python
def process_text(text):
    snake.x = 150
```

Our Sprite has *attribute* `x` which determines its 
<var>x</var> coordinate - how far to the right it is
from the window edge.
You can set this attribute how you would want - mostly as
reaction to some event but it can be also set in the beginning.

Try to add something to `x` everytime the clock ticks.
Are you able to guess how this piece of code will behave?

```python
def tick(t):
    snake.x = snake.x + t * 20
```

If you are not scared of maths import `math`
and let the picture move regarding to some function:

```python
def tick(t):
    snake.x = snake.x + t * 20
    snake.y = 20 + 20 * math.sin(snake.x / 5)
```

What will happen when you change those numbers?

What will happen when you try to set `rotation` attribute similar way?

## Call later

<img src="{{ static('snake2.png') }}" alt="" style="display:block;float:right;">

Pyglet also can call a function after some time.

Download another picture. I have another snake which
is a bit different then the first one.

Once you have the picture in the folder with your
program add this piece of code right before `pyglet.app.run()`:

{# XXX: Highlight 'snake2.png' strongly #}
```python
image2 = pyglet.image.load('snake2.png')

def change(t):
    snake.image =image2

pyglet.clock.schedule_once(change, 1)
```

Calling `schedule_once(change, 1)` tells Pyglet that it
should call the function `change` after one second.
And this function changes the image - similar way as we were
changing the coordinates.

`schedule_once` can be also called when you are handling another
event. Try to replace function `change` like that:

```python
def change(t):
    snake.image = image2
    pyglet.clock.schedule_once(change_back, 0.2)

def change_back(t):
    snake.image = image
    pyglet.clock.schedule_once(change, 0.2)
```

## Click 🐭

Last event we will learn to handle is clicking.
Write this function right before the `window.push_handlers`:

```python
def click(x, y, button, mode):
    snake.x = x
    snake.y = y
```

… and then register it in `push_handlers` by `on_mouse_press=click,`.

Try to find out what each argument means by yourself.

> [note] Help
> * If you don't get rid of the command line completely
> you can use `print`. So everytime you want to find out some
> value, use print.
> * How many buttons does mouse have?
> * What will happen after <kbd>Shift</kbd>+click?


## To be continued

We wrote enough code so we can end this lesson:

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

With keystroke and mouse input, timing and rendering Sprite, 
you can create a simple game or graphics application.

When you will write some game try to keep the state of the
application (basically how the window should look like)
in lists and tuples (eventually in dictionaries or classes).
One function should draw this state and other function
should manipulate (change) it.
To avoid confusion you can also have those two functions 
in different files.

If you are interested in this topic you can try to play and examine
[Pong](static/pong.py) code, which shows more Pyglet options: writing text, 
drawing rectangles and handling specific keys (e. g. arrows).
It can look difficult but look into the comments(currently with A LOT of grammar
errors) and try to understand it. If the comments are not enough for you
 to understand we will also translate more detailed 
 materials for [it]({{ lesson_url('beginners-en/pong') }}) 

You can find things that we've learned today (and some more) in
[Pyglet cheatsheet](https://github.com/muzikovam/cheatsheets/blob/master/pyglet/pyglet-basics-en.pdf),
which you can download and print out.

And if you want to dive deeper into Pyglet there is also
[documentation](http://pyglet.readthedocs.org/en/latest/index.html).
If anything in there won't be clear just ask!