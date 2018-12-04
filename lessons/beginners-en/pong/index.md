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

Když už jsme dokázali zpracovat vstup od uživatele,
můžeme podle něj pohnout s pálkami.
Pohyb předmětů budeme provádět ve funkci `obnov_stav(dt)`,
která bude registrována na tik hodin v Pygletu.
Argument `dt` je čas od posledního zavolání funkce Pygletem.

```python
def obnov_stav(dt):
    for cislo_palky in (0, 1):
        # pohyb podle klaves (viz funkce `stisk_klavesy`)
        if ('nahoru', cislo_palky) in stisknute_klavesy:
            pozice_palek[cislo_palky] += RYCHLOST_PALKY * dt
        if ('dolu', cislo_palky) in stisknute_klavesy:
            pozice_palek[cislo_palky] -= RYCHLOST_PALKY * dt

        # dolni zarazka - kdyz je palka prilis dole, nastavime ji na minimum
        if pozice_palek[cislo_palky] < DELKA_PALKY / 2:
            pozice_palek[cislo_palky] = DELKA_PALKY / 2
        # horni zarazka - kdyz je palka prilis nahore, nastavime ji na maximum
        if pozice_palek[cislo_palky] > VYSKA - DELKA_PALKY / 2:
            pozice_palek[cislo_palky] = VYSKA - DELKA_PALKY / 2
```

Podívejme se na tento kus kódu. Procházíme
v cyklu obě pálky a ptáme se, zda je v množině
stisknutých kláves <var>n</var>-tice reprezentující
pohyb dané pálky nahoru nebo dolů.
Když ano, *pohneme pálkou* v daném směru
(přičteme nebo odečteme od vertikální polohy pálky
změnu polohy, což je čas od posledního zavolání,
který známe, vynásobený rychlostí pálky nastavené
v konstantě).

V druhé části musíme zajistit, aby pálka *nevyjela*
z hracího pole. Z minulých hrátek s hadem víme,
že to se může stát velmi snadno. Pálku malujeme kolem
jejího středu, což znamená, že když se pálka přiblíží na
na <var>y</var>-ovou pozici `DELKA_PALKY / 2`, začíná
překračovat dolní hranici hracího pole. V tom případě
její pozici zafixujeme na nejnižší možné souřadnici.
Analogicky to provedeme, když se blíží hornímu okraji.

Zaregistruj vytvořenou funkci na tik hodin jako

```python
...
pyglet.clock.schedule(obnov_stav)
pyglet.app.run()
```

a podívej se na výsledek.


### Rozehrání

Než začneme míček odrážet od stěn, musíme ho nejprve
uvést do pohybu. Vystřelíme ho ze středu hrací plochy
do náhodného směru. Toto se také stane v momentě, kdy
jeden z hráčů skóruje a hra se rozehrává znovu.
Proto tohle rozehrání zabalíme do funkce `reset()`.
Zavolejte ji, než se spustí hra.

Jak bude tato funkce vypadat?
Nejprve přesuň míček do středu hrací plochy nastavením
proměnné `pozice_mice`. Potom je třeba
simulovat hod mincí pomocí volání funkce
`random.randint(0, 1)`. Tím rozhodneme, zda
se míček rozletí doprava nebo doleva.
Míček rozpohybujeme horizontálním směrem přičtením
požadované rychlosti k `rychlost_mice[0]`.
Ve vertikálním směru `rychlost_mice[1]`
se bude míček pohybovat zcela náhodně přičtením
náhodné rychlosti.

{% filter solution %}
```python
import random
...
def reset():
    pozice_mice[0] = SIRKA // 2
    pozice_mice[1] = VYSKA // 2

    # x-ova rychlost - bud vpravo, nebo vlevo
    if random.randint(0, 1):
        rychlost_mice[0] = RYCHLOST
    else:
        rychlost_mice[0] = -RYCHLOST
    # y-ova rychlost - uplne nahodna
    rychlost_mice[1] = random.uniform(-1, 1) * RYCHLOST

# nastavit vychozi stav pro start hry
reset()
```
{% endfilter %}


Nic se zatím ale nestane, protože funkce
`obnov_stav(dt)` zatím nepracuje
se změnou rychlosti. Musíme v ní tedy nastavit proměnnou
`poloha_micku` podle současné rychlosti míčku
a času uplynulého od posledního zavolání funkce podle
fyzikálního vztahu <var>s</var> = <var>v</var> <var>t</var>, tedy že dráha
je rovna rychlosti vynásobené časem. Přidej tedy do
funkce `obnov_stav(dt)` následující kód:

```python
def obnov_stav(dt):
    ...
    # POHYB MICKU
    pozice_mice[0] += rychlost_mice[0] * dt
    pozice_mice[1] += rychlost_mice[1] * dt
```

Zkus, co se teď stane při spuštění hry.
Míček by měl vyletět pokaždé do jiného směru.

### Odrážení míčku

Míček nám teď nekontrolovaně vyletí z hřiště.
Musíme tedy zařídit, aby se odrážel od stěn.
Jelikož úhel dopadu se rovná úhlu odrazu,
stačí otočit znaménko <var>y</var>-ové složky rychlosti.
Do funkce `obnov_stav(dt)` musíme
přidat kontroly na polohu míčku a případně
změnit jeho směr, pokud je moc nízko nebo moc vysoko.

```python
def obnov_stav(dt):
    ...
    # Odraz micku od sten
    if pozice_mice[1] < VELIKOST_MICE // 2:
        rychlost_mice[1] = abs(rychlost_mice[1])
    if pozice_mice[1] > VYSKA - VELIKOST_MICE // 2:
        rychlost_mice[1] = -abs(rychlost_mice[1])
```


Teď nám zbývá odraz od pálky, případně resetování
hry, pokud míček padne mimo pálku jednoho hráče a
ten druhý tak získá bod. Opět tedy budeme přidávat
kód do funkce `obnov_stav(dt)`.

Prvním krokem je poznamenání mezí na <var>y</var>-ové ose,
kde se musí míček nacházet, aby byl úspěšně odražen –
to je mezi horním a dolním koncem pálky:

```python
def obnov_stav(dt):
    ...
    palka_min = pozice_mice[1] - VELIKOST_MICE / 2 - DELKA_PALKY / 2
    palka_max = pozice_mice[1] + VELIKOST_MICE / 2 + DELKA_PALKY / 2
```

Nyní když míček narazí do pravé nebo levé stěny
se umíme zeptat, zda je pálka na správné pozici
a my máme `odrazit` míček nebo zda hráč
prohrál kolo a my máme přičíst jeho soupeři bod a
`restartovat hru`.

```python
def obnov_stav(dt):
    ...
    # odrazeni vlevo
    if pozice_mice[0] < TLOUSTKA_PALKY + VELIKOST_MICE / 2:
        if palka_min < pozice_palek[0] < palka_max:
            # palka je na spravnem miste, odrazime micek
            rychlost_mice[0] = abs(rychlost_mice[0])
        else:
            # palka je jinde nez ma byt, hrac prohral
            skore[1] += 1
            reset()

    # odrazeni vpravo
    if pozice_mice[0] > SIRKA - (TLOUSTKA_PALKY + VELIKOST_MICE / 2):
        if palka_min < pozice_palek[1] < palka_max:
            rychlost_mice[0] = -abs(rychlost_mice[0])
        else:
            skore[0] += 1
            reset()
```

## Závěr

Hurá, prokousali jsme se k zdárnému konci Pongu!
Máš teď plně funkční interaktivní grafickou
hru zakládající se na reálné předloze. :)