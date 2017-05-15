import math

import pyglet
from pyglet import gl

WIDTH = 800
HEIGHT = 600
ROTATION_SPEED = 200
ACCELERATION = 300

def load_image(filename):
    image = pyglet.image.load(filename)
    image.anchor_x = image.width // 2
    image.anchor_y = image.height // 2
    return image

# Images from www.kenney.nl, thank you!
# Public Domain (Creative Commons CC-0)
spaceship_img = load_image('assets/PNG/playerShip2_red.png')

pressed_keys = set()
objects = []
batch = pyglet.graphics.Batch()

class Spaceship:
    def __init__(self, window, rotation=0):
        self.x = window.width / 2
        self.y = window.height / 2
        self.x_speed = 0
        self.y_speed = 0
        self.rotation = rotation
        self.sprite = pyglet.sprite.Sprite(spaceship_img, batch=batch)
        self.window = window

    def tick(self, dt):
        if pyglet.window.key.LEFT in pressed_keys:
            self.rotation += dt * ROTATION_SPEED
        if pyglet.window.key.RIGHT in pressed_keys:
            self.rotation -= dt * ROTATION_SPEED
        if pyglet.window.key.UP in pressed_keys:
            rotation_radians = math.radians(self.rotation)
            self.x_speed += dt * ACCELERATION * math.cos(rotation_radians)
            self.y_speed += dt * ACCELERATION * math.sin(rotation_radians)

        self.x += dt * self.x_speed
        self.y += dt * self.y_speed

        if self.x < 0:
            self.x += self.window.width
        if self.y < 0:
            self.y += self.window.height
        if self.x > self.window.width:
            self.x -= self.window.width
        if self.y > self.window.height:
            self.y -= self.window.height

        self.sprite.rotation = 90 - self.rotation
        self.sprite.x = self.x
        self.sprite.y = self.y


def tick(dt):
    for obj in objects:
        obj.tick(dt)

def draw():
    window.clear()
    batch.draw()

    ## Advanced: Correct drawing at the edges of the screen
    ## Instead of batch.draw, do:
    # for x_offset in (-window.width, 0, window.width):
        # for y_offset in (-window.height, 0, window.height):
            # gl.glPushMatrix()
            # gl.glTranslatef(x_offset, y_offset, 0)
            # batch.draw()
            # gl.glPopMatrix()

def key_pressed(key, mod):
    pressed_keys.add(key)

def key_released(key, mod):
    pressed_keys.discard(key)

window = pyglet.window.Window(width=WIDTH, height=HEIGHT)

window.push_handlers(
    on_draw=draw,
    on_key_press=key_pressed,
    on_key_release=key_released,
)

pyglet.clock.schedule(tick)

objects.append(Spaceship(window))

## For fun, also try:
# for i in range(0, 360, 10):
#      objects.append(Spaceship(window, rotation=i))

pyglet.app.run()
