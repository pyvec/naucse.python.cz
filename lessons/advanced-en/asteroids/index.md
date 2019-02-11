# Asteroids game

Our final project is going to use everything what we know: 
classes, graphics, lists... I hope that you will like it!

We will try to make a clone of the game [Asteroids](https://en.wikipedia.org/wiki/Asteroids_%28video_game%29) 
that has been released in 1979.

Our version will look like this:

{{ figure(
    img=static('screenshot.png'),
    alt="Asteroids-like game screenshot"
) }}

The project is quite complex. It is using few things that were
not covered by [the beginner's course](https://naucse.python.cz/2018/pyladies-en-prague/). 
I know that you will be able to look them up.

> [note]
> If you go through the project alone, it is possible that you
> will be stuck at some problem. 
> If it happens to you, let us know.
> We will be happy to help you!

## Spaceship

{# XXX: (asteroids1.py) #}

The first step is to program a spaceship that you can control by keyboard.

* Instance of class `Spaceship` represents the spaceship.
* Every spaceship has two attributes `x` a `y` (position),
  `x_speed` a `y_speed`, `rotation`, and
  `sprite` (2D object in Pyglet wiht position, speed, rotation, and image).
* Spaceship has a method called `tick` that handles the spaceship mechanics – movement,
  rotation, and control.
* All objects that are in the game are stored in a global list `objects`.
  It should contain only the spaceship for now.
* All pressed keys should be stored in a *set* (keyword `set`).
  It is a datatype list but without order. It members can be in
  only once. (Sets are like dictionaries without values.)
  You can use [sets cheatsheet](https://github.com/pyvec/cheatsheets/blob/master/sets/sets-en.pdf)
  and the official Python documentation contains
  [a tutorial](https://docs.python.org/3/tutorial/datastructures.html#sets)
  and [the reference](https://docs.python.org/3/library/stdtypes.html#set-types-set-frozenset).
  The spaceship using the set as part of the processing in its `tick` method.
* You can use [the image set](http://opengameart.org/content/space-shooter-redux),
  created by [Kenney Vleugels](http://kenney.nl). He made them public and free. You can draw your own if you want!
* In the game, we will use a large number of `Sprite`s and draw them one by one would take quite a long time.
  So add all the `Sprite`s to the (pyglet.graphics.Batch)[https://pythonhosted.org/pyglet/api/pyglet.graphics.Batch-class.html] collection, which Pyglet can efficiently draw at once. Add arguments to "batch" by using `Sprite()` to create a `sprite.delete()`. For example:
    ```python
    batch = pyglet.graphics.Batch()
    sprite1 = pyglet.sprite.Sprite(image, batch=batch)
    sprite2 = pyglet.sprite.Sprite(image, batch=batch)

    # and then you can draw all of them at once: 
    batch.draw()
    ```
    You should have the `batch` collection, as well as the `objects`, kept globally.
* To move and rotate the objects according to their center, it is good to set the
  "anchor" of the image to its center (otherwise, the anchor is in the lower left corner):
    ```python
    image = pyglet.image.load(...)
    image.anchor_x = image.width // 2
    image.anchor_y = image.height // 2 
    self.sprite = pyglet.sprite.Sprite(image, batch=batch)
    ```
* You can use the arrow keys to move left, right, and straight with the rocket.
  The arrows to the sides spin the rocket, the arrow forward accelerates the movement
  in the direction the rocket is turned.
    * The basic motion of the rocket is simple: the x-coordinate is added to the x-velocity
    times the elapsed time and the same with the y-coordinate as for the rotation angle:
        ```python
        self.x = self.x + dt * self.x_speed
        self.y = self.y + dt * self.y_speed
        self.rotation = self.rotation + dt * rotation_speed
        ```
        The speed of rotation depends on the arrows (left or right). In one case, it is 
        negative, in the other positive. Choose the appropriate value by experimenting 
        - starting at 4 radians per second. All similar "magical values" should be defined 
        as constants - i.e. variables that you set at the beginning and never change. It is 
        a convention to name them in capital letters and put them at the beginning of the file, 
        right after the import:
        ```python
        ROTATION_SPEED  =  4   # radians per second
        ```
    * Acceleration is a little more complicated: the x-axis speed is added to the cosine 
    angle of rotation times elapsed time. The sinus is used with the y-axis.
        ```python
        self.x_speed += dt * ACCELERATION * math.cos(self.rotation)
        self.y_speed += dt * ACCELERATION * math.sin(self.rotation)
        ```
        Notice the ACCELERATION constant example. Choose it again at your discretion.
    * If you have the `self.x`, `self.y` and `self.rotation` values counted, do not forget 
    to project them into `self.sprite`, otherwise nothing interesting will happen.

        Beware that the `math.sin` and `math.cos` functions use radians, whereas the `pyglet` 
        uses `Sprite.rotation` degrees. (And this is extra 0° elsewhere, and it rotates 
        on the opposite side.) For sprite, therefore, the angle needs to be converted:
        ```python
        self.sprite.rotation = 90 - math.degrees(self.rotation)
        self.sprite.x = self.x
        self.sprite.y = self.y
        ```
    * When the rocket breaks out of the window, go back to the game on the other side of 
    the screen. (Check that it works on all four sides.)
* **Bonus 1:** Try to add a few rakets, each with a slightly different angle.
    Each individual `Spaceship` object maintains its own state, so it should not be difficult 
    to create more (and to control all at once).
* **Bonus 2 :** You may have noticed a "jump" when a rocket escapes from the window and 
    returns to the other side. This can be avoided by rendering the whole screen once more 
    to the left, right, up and down.

    Pyglet has a special low-level feature that can tell "now draw everything moved by 
    the X pixels to the left". Full explanation would be long, so just copy the code:
    ```python
    from pyglet import gl

    def draw():
        window.clear()

        for x_offset in (-window.width, 0, window.width):
            for y_offset in (-window.height, 0, window.height):
                # Remember the current state 
                gl.glPushMatrix () 
                # Move everything drawn from now on by (x_offset, y_offset, 0)
                gl.glTranslatef(x_offset, y_offset, 0)

                # Draw 
                batch.draw()

                # Restore remembered state (this cancels the glTranslatef) 
                gl.glPopMatrix()
    ```
    For an overview, the documentation for the functions used here is: 
    [glPushMatrix](https://www.khronos.org/registry/OpenGL-Refpages/gl2.1/xhtml/glPushMatrix.xml), 
    [glPopMatrix](https://www.khronos.org/registry/OpenGL-Refpages/gl2.1/xhtml/glPushMatrix.xml), 
    [glTranslatef](https://www.khronos.org/registry/OpenGL-Refpages/gl2.1/xhtml/glTranslate.xml).

Succeeded? Can you fly the universe?

## Asteroids
{# XXX: (asteroids2.py) #}

Add a second type of space object: `Asteroid`.

* Asteroids and spaceships have many things in common: every space object will have its 
position, speed, rotation, and rules how it moves. So create `SpaceObject` class, where will be 
everything they have in common, and `Spaceship` class, that inherits from `SpaceObject`, in which the spaceship-specific 
code remains (i.e., keyboard control, ship image, start from the middle of the screen).
* The part of the code for motion will be common to all space objects (e.g. code for the 
acceleration); part will be specific to the rocket only (keypad control). Take advantage 
of the `super()` function (more in [inheritance lesson](../../beginners-en/inheritance/)).
* Write the `Asteroid` class, which is also inherited from `SpaceObject`, but has its own 
behavior: it starts either at the left or bottom of the screen with random speed, and each 
asteroid have randomly assigned image. (In the Asteroids, the left and right edges 
are essentially the same, and the top and bottom too.)
* And then add some asteroids of different sizes to the game.

Succeeded? Do you have two types of objects?


## Collisions

Our asteroids are pretty harmless yet. Let's change it.

* In this section, your task will be to find out when the ship is hit by an asteroid. For 
simplicity, we replace each object with a circle and count when the circles collide. 
Each object will need to have a radius - `radius` attribute.
* In order to see what game "thinks" about objects, draw a circle above each object. 
The best thing to do is to use [pyglet.gl](https://pyglet.readthedocs.io/en/latest/programming_guide/gl.html) 
and a little math; for now just copy the `draw_circle` function and call it for each object. 
When everything will work, you can give it away.
    ```python
    def draw_circle(x, y, radius):
      iterations = 20
      s = math.sin(2 * math.pi / iterations)
      c = math.cos(2 * math.pi / iterations)

      dx, dy = radius, 0

      gl.glBegin(gl.GL_LINE_STRIP)
      for i in range(iterations + 1):
        gl.glVertex2f(x + dx, y + dy)
        dx, dy = (dx * c - dy * s), (dy * c + dx * s)
      gl.glEnd()
    ```
* When the asteroid crashes into the ship, the ship will explode and disappear. We'll leave the 
explosion for later, it's important to remove the object from the game. Put it in the 
`SpaceObject.delete` method, because any object can be removed from the game. In this 
method, you must remove the object from the list of `objects` and then delete its `Sprite` 
so that it does not render within the `batch`.
* And how do you do that collision? Within the `Spaceship.tick`, go through each object to 
see if the distance between the ship and the other object is less than the sum of their radiuses 
(they hit each other), and if so, call the object's `hit_by_spaceship` method.

    Finding a distance in a game where the [objects that fly out of the screen returns on the other side](https://en.wikipedia.org/wiki/Wraparound_%28video_games%29) 
    is not entirely straightforward, so copy the code for now:
    ```python
    def distance(a, b, wrap_size):
        """Distance in one direction (x or y)"""
        result = abs(a - b)
        if result > wrap_size / 2:
            result = wrap_size - result
        return result

    def overlaps(a, b):
        """Returns true if and only if two objects overlap space"""
        distance_squared = (distance(a.x, b.x, window.width) ** 2 +
                            distance(a.s, b.y, window.height) ** 2)
        max_distance_squared = (a.radius +b.radius) ** 2
        return distance_squared < max_distance_squared
    ```

    Most objects in a completed game (such as fire from the rocket, missile) will not do anything 
    when the collision will happen, so the `SpaceObject.hit_by_spaceship` should do nothing 
    (it only needs to exist). Just the asteroid will break the rocket, so redefine `Asteroid.hit_by_spaceship` 
    to call `delete` ship.

    Because there could be more rockets in our game in general, the asteroid needs to know which rocket it broke. 
    The `hit_by_spaceship` method should, therefore, have an argument.


Succeeded? Can you lose now?

## Attack
Now try to break the asteroids.
 
* The missile can fire a laser in 0.3 seconds. For each rocket save a number (as an attribute)
which is set, after each fire, to 0.3 and then let this number drop by 1 per second in the 
`tick` method. If the number is negative user can fire again.
* When a player holds a space bar and there is possibility to fire, then the ship should fire.
This will be reflected in the game by adding an object of a new `Laser` class. It starts at 
rocket's coordinates, with rocket's rotation and rocket speed plus something extra in the 
direction of rotation.
* Each `Laser` object will "remember" how long it is in the game. In the beginning, 
it's set to a number so the laser can fly little bit more than one screen. When the time 
comes, the `Laser` disappears.
* In its `tick` method the laser go thru all objects and when its position overlaps with some
of these object it calls `hit_by_laser` method. For most objects, this method does nothing, 
only the asteroids will break.
* When the laser touches the asteroid, the asteroid divides into two smaller ones (or, if it's
too small, it disappears completely).

  You can set the speeds of new asteroids how you want - it is important that every smaller 
  asteroid flew elsewhere. Usually, new asteroids are faster than the original ones.

* And that's all! You have a functional game!

Succeeded? Can you also win?


## Completion and extension
If you want to continue in the game, here are some ideas. You can do it in any order - or 
you can invent your own extension!

* Is the game too difficult?

    You can add lives: there are three at the beginning, and as long as there's one left, 
    the rocket will appear again in the middle of the screen with zero speed after the 
    asteroid hit it. 
    The game should also ignore the keys that were held until the player press them again 
    (preferably use `pressed_keys.clear ()`).

    You can show the number of ships (lives) that are left with icons at the bottom of the screen.

    **Bonus**: A few seconds after the "restart", the rocket can be indestructible to have 
    time to fly when the is an asteroid in the middle of the screen.

* Is the game too easy?

    Add Levels: When the player shoots all the asteroids, they move to the next level where 
    are more the asteroids than in the the previous lever.

    You can display the level number using [pyglet.text.Label](https://pyglet.readthedocs.io/en/latest/programming_guide/text.html).

* Is the background too black?

    In the set of pictures in the `Backgrounds` directory choose one background and paint 
    the whole universe with it.

* Is the game too austere?

    Add fire and explosion! Like the `Laser`, they just don't destroy anything, they just 
    change a colour depending on how long they are in the game.

    You can use the ["Smoke particle assets"](http://opengameart.org/content/smoke-particle-assets) 
    images drawn by [Kenney Vleugels](https://kenney.nl/) again. I recommend "White Puff" 
    that you can shrink (e.g. `sprite.scale = 1/10`), change colour (e.g. `sprite.color = 255, 100, 0`) 
    or make them partially transparent (e.g. `sprite.opacity = 100`).

    I recommend to make a new `batch` for the effects and draw it before the main one so the 
    effects can't overlap the game objects.

* Don't you know whether you lost or won?

    In the end, you can draw the big GAME OVER or WINNER sign.

* Are you bored?

    In the original game UFOs sometimes appear and sometimes they shoot at the rocket, 
    so if the rocket is still in one spot and it is just spinning around, the UFO will 
    destroy it. You can try to complete the `Ufo` class and you can create `ShipLaser` and 
    `UfoLaser` that inherit from the `Laser` class.

Succeeded? Does it look and behave professionally?