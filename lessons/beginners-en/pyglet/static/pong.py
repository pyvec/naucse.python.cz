#!/usr/bin/env python3
"""Pong game

Graphics game for two players. Every player controls the "bat" on their side,
and tries to fire the ball on the opponent's side.

Control:
Hrac 1: Keys W and S
Hrac 2: arrows Up and Down
End: Esc


The game uses the Pyglet gravitational library, which is Python's superstructure over OpenGL.

The Coordinate System is following:


        y ^
          |
    HEIGHT +---------------------------------------+
          |                   :                   |
          |                   :                   |
          |                   :                   |
          |                   ;     []            |
          |]                  ;                  [|
          |]                  ;                  [|
          |]                  ;                  [|
          |]                  ;                  [|
          |                   ;                   |
          |                   :                   |
          |                   ;                   |
          |                   ;                   |
        0 +---------------------------------------+------> x
          :                   :                   :
          0               WIDTH/2               WIDTH

Be careful if you have experience with some graphics programs or 2D
libraries. OpenGL uses the mathematical coordinate system, zero is left *down*.

"""

# First line (#!/usr/bin/env python3) is the so-called "shebang": on
# Unix base operating systems (Linux, OS X) allows you to run this file simply by using the command: ./pong.py

# And now to the game itself: first you have to import the necessary methods from the pyglet library

import random

import pyglet
from pyglet import gl
from pyglet.window import key


# Some constants:

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

# We will remember the state of the game in global variables.
# Professional programmer would get mad but it is
# now simpler for us.
# Just don't forget that command like:
#     ball_coordinates = [0, 0]
# in function would've create only local variable, which wouldn't have
# anything in common with global `ball_coordinates` variable.
# And command like:
#     ball_coordinates[0] = 0
# sets first element in global variable `ball_coordinates`.

bat_coordinates = [HEIGHT // 2, HEIGHT // 2]  # vertical position of two bats
ball_coordinates = [0, 0]  # x, y ball coordinates -- set in reset()
ball_speed = [0, 0]  # x, y components of ball speed -- set in reset()
keys_pressed = set()  # set of pressed keys
score = [0, 0]  # score for 2 players

# The position of the bats and the ball will always be determined by the center of the rectangle.


def reset():
    """set initial state

    This function will be call in the beginning and also after some of
    the players loses the game.
    Function will place the ball to the centre of the window and will give
    it random speed.

    We are not resetting score and bats position here, those will stay to the next round.
    """
    ball_coordinates[0] = WIDTH // 2
    ball_coordinates[1] = HEIGHT // 2

    # x speed - right or left
    if random.randint(0, 1):
        ball_speed[0] = SPEED
    else:
        ball_speed[0] = -SPEED
    # y speed - completely random
    ball_speed[1] = random.uniform(-1, 1) * SPEED


def revive(dt):
    """Count new game state

    This function is called many times per second. It will get time
    in seconds that has passed from the last call by `dt` argument.
    The computer is very quick so the number will be usually small.
    """
    # As we know from physics, ball with speed `v` move in time `t` about
    # `v*t` length.
    # We can expand this expression for x and y components.
    ball_coordinates[0] += ball_speed[0] * dt
    ball_coordinates[1] += ball_speed[1] * dt

    # bounce from the bottom edge
    # When the ball is too "low" it should bounce back and start to move up
    # That means that it will have y speed component above 0
    # x component won't change
    if ball_coordinates[1] < BALL_SIZE // 2:
        ball_speed[1] = abs(ball_speed[1])

    # bounce from top edge
    # The same but ball is too high and it has to move down.
    if ball_coordinates[1] > HEIGHT - BALL_SIZE // 2:
        ball_speed[1] = -abs(ball_speed[1])

    # bat movement - loop has to run twice - once for each bat
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

    # ball bounce
    # If the ball is "too left" it could be bounced from the left bat
    # or there isn't any bat and player on the left lost. It's
    # similar for the right side.
    # I recommend to draw it on a piece of paper :)

    # first I will write down minimal and maximal position where the bat have to be
    # (centre of the bat) to bounce back the ball
    bat_min = ball_coordinates[1] - BALL_SIZE/2 - BAT_LENGTH/2
    bat_max = ball_coordinates[1] + BALL_SIZE/2 + BAT_LENGTH/2

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


def draw_text(text, x, y, x_position):
    """Draw given text on the given coordinates

    Argument `x_position` can be "left" or "right" - sets where the text will be aligned
    """
    # Pyglet can print text and we will create object "write" and then we will draw it.
    # (Usually we would create this object once and then we would just change its text and
    # redraw it but we will do it this way cause it's easier)
    write = pyglet.text.Label(
        text,
        font_name='League Gothic',
        font_size=FONT_SIZE,
        x=x, y=y, anchor_x=x_position)
    write.draw()


def render():
    """Render(draw) state of the game"""
    gl.glClear(gl.GL_COLOR_BUFFER_BIT)  # clear the window (paint the window black)
    gl.glColor3f(1, 1, 1)  # set the paint to white

    # ball
    draw_rectangle(
        ball_coordinates[0] - BALL_SIZE // 2,
        ball_coordinates[1] - BALL_SIZE // 2,
        ball_coordinates[0] + BALL_SIZE // 2,
        ball_coordinates[1] + BALL_SIZE // 2)

    # bats - we will create list of bats coordinates and for each pair of coordinates
    # in this list we will draw the bat
    for x, y in [(0, bat_coordinates[0]), (WIDTH, bat_coordinates[1])] :
        draw_rectangle(
            x - BAT_THICKNESS,
            y - BAT_LENGTH // 2,
            x + BAT_THICKNESS,
            y + BAT_LENGTH // 2)

    # midfield line (as net) - composed from couple of small rectangles
    for y in range(NET_LENGTH // 2, HEIGHT, NET_LENGTH * 2):
        draw_rectangle(
            WIDTH // 2 - 1,
            y,
            WIDTH // 2 + 1,
            y + NET_LENGTH)

    # And finally we will draw the score of both players
    draw_text(str(score[0]),
                  x=TEXT_ALIGN,
                  y=HEIGHT - TEXT_ALIGN - FONT_SIZE,
                  x_position='left')

    draw_text(str(score[1]),
                  x=WIDTH - TEXT_ALIGN,
                  y=HEIGHT - TEXT_ALIGN - FONT_SIZE,
                  x_position='right')


def key_press(symbol, modifiers):
    """Handles key press

    When player presses some key there will be added a tuple (direction, bat number) to `keys_pressed` set.
    So the program can move with the bats according to what's in the set.
    """
    if symbol == key.W:
        keys_pressed.add(('up', 0))
    if symbol == key.S:
        keys_pressed.add(('down', 0))
    if symbol == key.UP:
        keys_pressed.add(('up', 1))
    if symbol == key.DOWN:
        keys_pressed.add(('down', 1))
    # Pyglet handles ESC key by itself: it closes the window and exits the run() function


def key_release(symbol, modifiers):
    """Handles when key is released

    The opposite to the `key_press` function -- regarding the arguments
    it will remove the tuple of direction and bat number from the set.
    """
    # Notice the usage of function `discard`: unlike `remove` it won't
    # raise an error when the element is not in the set. So the program
    # won't end when user press some key elsewhere and then switch back to our
    # window and after then they will release the key.
    if symbol == key.W:
        keys_pressed.discard(('up', 0))
    if symbol == key.S:
        keys_pressed.discard(('down', 0))
    if symbol == key.UP:
        keys_pressed.discard(('up', 1))
    if symbol == key.DOWN:
        keys_pressed.discard(('down', 1))
    # By the way, functions key_release and key_press could be simplified by
    # using dictionaries. Will you try that?

# We will set the initial state.
reset()

# We will create the window where we will draw.
window = pyglet.window.Window(width=WIDTH, height=HEIGHT)

# We will add some functions to the window which will react to some events.
# For example when the user will press some key, Pyglet will call
# a function that we will register with `on_key_press`, and it will pass specific
# key to the function. You can find the list of all the events that can happen
# and what exactly Pyglet passes as an argument in Pyglet documentation or with
# `help(pyglet.window.event)` function.
window.push_handlers(
    on_draw=render,  # for drawing into the window use function `render`
    on_key_press=key_press,  # when key is pressed call function `key_press`
    on_key_release=key_release,  # when key is released call `key_release`
    )

# We also have another function but we don't want to assign it to any window event.
# We want to call it everytime the clock "ticks".
pyglet.clock.schedule(revive)

pyglet.app.run()  # everything is set, let the game begin
# Function run() will be calling in a loop revive, render and if some event will appear it will also
# call the function we assign to it.
