# Pong

<div style="text-align:center;">
    <img src="{{ static('pong.png') }}" alt="">
</div>

Now we will deepen the knowledge of programming graphics applications
which we got in the last [lecture about Pyglet]({{ lesson_url('intro/pyglet') }}),
by creating real program.

We will program one of the first video game ever, [Pong](https://en.wikipedia.org/wiki/Pong).
Pong was released by [Atari](https://en.wikipedia.org/wiki/Atari,_Inc.)
as their first game of year 1972 and it started the gaming industry revolution.

You can have a look on 
[video, which shows how Pong is played](https://www.youtube.com/watch?v=fiShX2pTz9A).


## Constants and state of the game

The Pong game has simple rules. But we have to know how
to express them in Python, and it is not that easy.
Let's take a look at what have to be in the game.

* Game board in rectangle shape with a net in the middle.
* A ball flying at a certain speed over the game field.
* Two bats moving vertically by the edges of the field.
* Two score counters.

The game will be for 2 players, we will not program the behavior of the computer.
Each player can control their bat by pressing the exact key.
One player can control the bat by up and down arrows and the other one by
<kbd>W</kbd> and <kbd>S</kbd> keys.

We can express the state of the game in Python using variables and
constants. Which makes sense because some things change in the game 
(bats position, ball position, ball speed, score) and some do not 
(size of the playing area, size of the bats and
ball, position and size of score counters).
From the complex data structures we will use list (which we already know)
and set, which is similar to set in maths. It's similar to list but
it doesn't care about the order and there can't be any two or more 
same elements.

You might be wondering in what units we can measure
distance and speed in such game on a computer.
On the screen, it is not practical to measure the distance
in centimeters. However, each screen is composed
from individual luminous points, ie. *pixels*.
In a graphical application such as Pong, we can measure the
distance of two places on the screen as the number of pixels
between these two places. Coordinate system of Pyglet
is based on pixels, where the pixel with the [0, 0] 
coordinates is on the bottom left of the screen.
The speed can be measured in in pixels per second.

Create a new file. Together we will define *constants*, which
we will need during the game creation. Usually, we would define the 
constants when we need them, but for simplicity let's do it together 
and all at once. We'll show you how to start translating the real 
world problem into Python.


```python
# Window size (in pixels)
WIDTH = 900
HEIGHT = 600

BALL_SIZE = 20
BAT_THICKNESS = 10
BAT_LENGTH = 100
SPEED = 200  # pixels per second
BAT_SPEED = SPEED * 1.5  # also pixels per second

NET_LENGTH = 20
FONT_SIZE = 42
TEXT_ALIGN = 30
```

We will now define *variables* that we will need: ball coordinates,
bat coordinates, pressed keys and score of two players.
Those variables will be global which would made any programmer 
furious but it will ease our work for now.

```python
bat_coordinates = [HEIGHT // 2, HEIGHT // 2]  # vertical position of two bats
ball_coordinates = [0, 0]  # x, y ball coordinates -- set in reset()
ball_speed = [0, 0]  # x, y components of ball speed -- set in reset()
keys_pressed = set()  # set of pressed keys
score = [0, 0]  # score for 2 players
```

## Rendering the game board

First, we open the window with the same size as the game board.

```python
import pyglet
...
window = pyglet.window.Window(width=WIDTH, height=HEIGHT)
pyglet.app.run()  # everything is set, let the game begin
```

Before we start to make an interactive part of the game responding to inputs
from the user we have to be able to draw everything that should be on the game
board. Just like in the Pyglet lesson where we had function `draw()` which
rendered the python we will have similar function in the Pong which will
render all elements on the board.

Most of the shapes are rectangles so let's create
a function `draw_rectangle` which will get 4 coordinates
and which will draw rectangle with the help of module `gl`
by drawing two triangles.

```python
from pyglet import gl
...
def draw_rectangle(x1, y1, x2, y2):
    """Draw the rectangle to the given coordinates

    How it should look like::

         y2 - +-----+
              |/////|
         y1 - +-----+
              :     :
             x1    x2
    """
    # I am calling OpenGL here which is the easiest to use for us at the moment
    gl.glBegin(gl.GL_TRIANGLE_FAN)   # draw connected triangles
    gl.glVertex2f(int(x1), int(y1))  # coordinate A
    gl.glVertex2f(int(x1), int(y2))  # coordinate B
    gl.glVertex2f(int(x2), int(y2))  # coordinate C, draw triangle ABC
    gl.glVertex2f(int(x2), int(y1))  # coordinate D, draw triangle BCD
    # another coordinate E would draw triangle CDE and so on
    gl.glEnd()  # stop drawing the triangles
```

We can now start to work on `render()` function.
First create it empty and register it with `on_draw` event.
That means that it will be called everytime when Pyglet redraws 
the window. If, for example, the position of the ball has changed the
function will draw it a bit elsewhere. By this we are creating
the game dynamics. We also did it with the python, but now we have more 
graphical elements. 

```python
...
def render():
    """Render(draw) state of the game"""
    gl.glClear(gl.GL_COLOR_BUFFER_BIT)  # clear the window (paint the window black)
    gl.glColor3f(1, 1, 1)  # set the paint to white

window = pyglet.window.Window(width=WIDTH, height=HEIGHT)
window.push_handlers(
    on_draw=render,  # for drawing into the window use function `render`
)
pyglet.app.run()  # everything is set, let the game begin
```

For now we only have cleaning of the window and setting the drawing
colour to white in the body of our function.

Try to add to the `render()` function rendering of the ball in the 
right position which you will get from the relevant global variable.
Size of the ball is in our case just small square which size is
stored in one of the constants.

{% filter solution %}
```python
def render():
    ...
    # ball
    draw_rectangle(
    ball_coordinates[0] - BALL_SIZE // 2,
    ball_coordinates[1] - BALL_SIZE // 2,
    ball_coordinates[0] + BALL_SIZE // 2,
    ball_coordinates[1] + BALL_SIZE // 2)
```
{% endfilter %}


After that try to draw both *bats*.
We have the vertical position of one bat stored in the 
`bat_position` variable. Horizontal position is a constant.
What coordinates do you have to pass to `draw_rectangle` so the bat
is rendered correctly and on the right position? It is similar to
drawing the ball.

{% filter solution %}
```python
def render():
    ...
    # bats - we will create list of bats coordinates and for each pair of coordinates
    # in this list we will draw the bat
    for x, y in [(0, bat_coordinates[0]), (WIDTH, bat_coordinates[1])] :
        draw_rectangle(
            x - BAT_THICKNESS,
            y - BAT_LENGTH // 2,
            x + BAT_THICKNESS,
            y + BAT_LENGTH // 2)
        )
```
{% endfilter %}

The *midfield line*(also the *net*) will help the game clarity.
But how to draw it? We don't have to think about anything 
difficult. We will just draw it as a series of rectangles from top to bottom.
This just needs to generate a list of coordinates,
which will have enough distance, and render a rectangle on each coordinate.
Which Python function would you use to obtain this list?

{% filter solution %}
```python
def render():
    ...
    # midfield line (as net) - composed from couple of small rectangles
    for y in range(NET_LENGTH // 2, HEIGHT, NET_LENGTH * 2):
        draw_rectangle(
            WIDTH // 2 - 1,
            y,
            WIDTH // 2 + 1,
            y + NET_LENGTH)
```
{% endfilter %}

So what's missing? *Score counter* for both players.
For that we will have to learn how to draw text with Pyglet.
There is already `text` module which contains `Label` object.
And that's exactly what we need for drawing the score.
First we have to create `Label` object. We will do that by brackets
after the name of the object, similar to when we are calling a function:
`write = Label()`. Usually we would create this object once and then 
we would just change its text and redraw it but we will do it this way 
cause it's easier. Finally we have to call `draw()` method or the
text won't be rendered.

```python
def draw_text(text, x, y, x_position):
    """Draw given text on the given coordinates

    Argument `x_position` can be "left" or "right" - sets where the text will be aligned
    """
    write = pyglet.text.Label(
        text,
        font_name='League Gothic',
        font_size=FONT_SIZE,
        x=x, y=y, anchor_x=x_position)
    write.draw()
```

Now try to use this function in `render()` function for
rendering the score. Use constants WIDTH, HEIGHT, TEXT_ALIGN
and TEXT_SIZE for setting the score coordinates.

{% filter solution %}
```python
def render():
    ...
     # And finally we will draw the score of both players
    draw_text(str(score[0]),
                  x=TEXT_ALIGN,
                  y=HEIGHT - TEXT_ALIGN - FONT_SIZE,
                  x_position='left')

    draw_text(str(score[1]),
                  x=WIDTH - TEXT_ALIGN,
                  y=HEIGHT - TEXT_ALIGN - FONT_SIZE,
                  x_position='right')

```
{% endfilter %}


Yay, now we have the whole game board rendered. Let's put it in motion!


## Game dynamics

Now it will start to be interesting. Let's move with bats first,
because it's easier, and then with the ball.

### User's input

We need to move with the bats regarding to user input.
As long as they will hold for example key <kbd>S</kbd>, left
bat will be moving down.
In previous lesson we learned how to work with event `on_text`,
but this one won't be enough. We will need 2 types of events
which we don't know yet - `on_key_press` and `on_key_release`.

Pyglet calls a function registered to event `on_key_press`
the same way it calls function `render()` registered to
event `on_draw`.
We will add pressed key to the global variable `keys_pressed`
as tuple with direction and bat's number, e. g. `('up',0)`,
which means that left bat have to go up.
We will remove the tuple from the `keys_pressed` set 
when `on_key_release` happens. This will ensure that the set `keys_pressed`
includes all the keys the user holds and we will be able to move
the bats according to that.

Will you try to code `key_press(symbol, modifiers)` and
`key_release(symbol, modifiers)` functions by yourself?
You can add element to any set by method `add(element)`
and delete by `discard(element)`. Both take an element which we
want to add or discard as an argument, in our case it will
be the tuple.

You will have to find out which key was pressed. Pyglet will
pass the code of pressed key to our function as first argument
so in our case it will be a `symbol`. It will be a number unless
you import `key` from `puglet.window`, which contains constants
of each key. So you will be able to compare if the key is
for example up arrow <kbd>↑</kbd> as `symbol == key.UP`.

{% filter solution %}
```python
from pyglet.window import key
...
def key_press(symbol, modifiers):
    if symbol == key.W:
        keys_pressed.add(('up', 0))
    if symbol == key.S:
        keys_pressed.add(('down', 0))
    if symbol == key.UP:
        keys_pressed.add(('up', 1))
    if symbol == key.DOWN:
        keys_pressed.add(('down', 1))
...

def key_release(symbol, modifiers):
    if symbol == key.W:
        keys_pressed.discard(('up', 0))
    if symbol == key.S:
        keys_pressed.discard(('down', 0))
    if symbol == key.UP:
        keys_pressed.discard(('up', 1))
    if symbol == key.DOWN:
        keys_pressed.discard(('down', 1))
...
```
{% endfilter %}

> [note]
> Why are we using `dicard()` method and not `remove()`(which
> we already know from lists and sets also have it)? Because
> it won't raise an error when the element is not in the set. So the program
> won't cause an error when user press some of the defined key
> elsewhere and then switch back to our
> window and just after that they will release the key.


Register both functions to events:

```python
...
window = pyglet.window.Window(width=WIDTH, height=HEIGHT)
window.push_handlers(
    on_draw=render,  # for drawing into the window use function `render`
    on_key_press=key_press,  # when key is pressed call function `key_press`
    on_key_release=key_release,  # when key is released call `key_release`
    )
pyglet.app.run()
```

### Bat movement

Once we were able to process input from the user,
we can move with bats regarding that.
We will move the objects in the function `revive(dt)`,
which will be registered to the clock. Argument `dt`
is time that passed from the last call.

```python
def revive(dt):
    for bat_number in (0, 1):
        # movement according to pressed keys (function `key_press`)
        if ('up', bat_number) in keys_pressed:
            bat_coordinates[bat_number] += BAT_SPEED * dt
        if ('down', bat_number) in keys_pressed:
            bat_coordinates[bat_number] -= BAT_SPEED * dt

        # bottom stop - when bat is down bellow we will set it to the minimum
        if bat_coordinates[bat_number] < BAT_LENGTH / 2:
            bat_coordinates[bat_number] = BAT_LENGTH / 2
        # top stop - when bat is too high we will set it to the maximum
        if bat_coordinates[bat_number] > HEIGHT - BAT_LENGTH / 2:
            bat_coordinates[bat_number] = HEIGHT - BAT_LENGTH / 2
```

Let's have a look at this piece of code.
We are going through both bats in a loop 
and we ask if there is the tuple of direction
and number of bat in the set `keys_pressed`.
If yes we *move* with the bat regarding to
the direction(we add to or deduct from the vertical
position of the bat the change which is time from
the last call multiplied by bat speed which we have
in constants).

In the second part we have to make sure that bat doesn't
appear *outside* of the game board. We know from the last
lesson when we were playing with the python image that it
can happen very easily. We are drawing bat from the 
middle, which means that if the bat `y` coordinate is lower than 
`BAT_LENGTH / 2` it is going outside of the board. 
In that case we will fix the position to the lowest possible coordinate.
It is done also for the top edge accordingly.

Register created function to the clock:

```python
...
pyglet.clock.schedule(revive)
pyglet.app.run()
```

and look at the result.


### Kick off

Before we start to bounce the ball from the walls we
have put it into motion first. We shoot it from the centre 
of the board to the random direction. This should also
happen when one player scores and game is starting again.
That's why we encapsulate this into `reset()` function.
Call it before you run the app.

How will this function look like?
First you have to move the ball to the centre of the
board by setting `ball_coordinates` variable. Then
we have to randomly select if the ball should go to the
left or to the right by calling `random.randint(0, 1)`.
We have to move the ball in the horizontal direction by adding
required speed to the `ball_speed[0]`. The speed in vertical
`ball_speed[1]` direction will be random.


{% filter solution %}
```python
import random
...
def reset():
    ball_coordinates[0] = WIDTH // 2
    ball_coordinates[1] = HEIGHT // 2

    # x speed - right or left
    if random.randint(0, 1):
        ball_speed[0] = SPEED
    else:
        ball_speed[0] = -SPEED
    # y speed - completely random
    ball_speed[1] = random.uniform(-1, 1) * SPEED
...
# We will set the initial state.
reset()
```
{% endfilter %}

Nothing is happening right now because function
`revive(dt)` is not working with the time yet.
We have to set there `ball_coordinates`. It will be
based on current coordinates and time from the last call
regarding to physics equation <var>d</var> = <var>v</var> <var>t</var>,
which means that the final distance equals to speed
multiplied by time. So add the following to the
`revive(dt)` function:

```python
def obnov_stav(dt):
    ...
    # BALL MOVEMENT
    ball_coordinates[0] += ball_speed[0] * dt
    ball_coordinates[1] += ball_speed[1] * dt
```

Now let's have a look at what happens when you run
the game. The ball should fly into different direction
each time.

### Ball bounce

The ball is flying uncontrollably out of the field now.
So we have to make sure that it will bounce back from the walls.
Because in our case angle of incidence equals angle of deflection
we will just switch the signs of y part of the speed.
So we have to add some checks of the ball position and 
eventually change its direction if it is too low or too high to the
`revive(dt)` function.

```python
def revive(dt):
    ...
    if ball_coordinates[1] < BALL_SIZE // 2:
        ball_speed[1] = abs(ball_speed[1])

    if ball_coordinates[1] > HEIGHT - BALL_SIZE // 2:
        ball_speed[1] = -abs(ball_speed[1])
```

Now we have to code the bounce from the bat, or a 
game reset if the ball is not hit by one of the player's
bat(that means that the other one gets a point).
We will be adding something to our `revive(dt)`
function again.

First step is to set bounds on y axis where the ball can be to be
successfully hit with a bat - between upper and lower
edge of a bat:

```python
def revive(dt):
    ...
    bat_min = ball_coordinates[1] - BALL_SIZE/2 - BAT_LENGTH/2
    bat_max = ball_coordinates[1] + BALL_SIZE/2 + BAT_LENGTH/2
```

Now when the ball hits the left or the right wall we can ask
if the bat it on the right spot so we can `bounce` ball back or
if it isn't so one player lost and the other one gets point and
we can `reset` the game.

```python
def obnov_stav(dt):
    ...
    # bounce to the left
    if ball_coordinates[0] < BAT_THICKNESS + BALL_SIZE / 2:
        if bat_min < bat_coordinates[0] < bat_max:
            # bat is at the right spot we can bounce the ball back
            ball_speed[0] = abs(ball_speed[0])
        else:
            # bat is not at the right place the player lost
            score[1] += 1
            reset()

    # bounce to the right
    if ball_coordinates[0] > WIDTH - (BAT_THICKNESS + BALL_SIZE / 2):
        if bat_min < bat_coordinates[1] < bat_max:
            ball_speed[0] = -abs(ball_speed[0])
        else:
            score[0] += 1
            reset()
    
```

## The end

Hooray, we finished the Pong! Now you have fully
functioning interactive graphical game based
on real game :)