import math
import random

import pyglet
from pyglet import gl

WIDTH = 800
HEIGHT = 600
ROTATION_SPEED = 200
ACCELERATION = 300
ASTEROID_SPEED = 100
ASTEROID_ROTATION_SPEED = 3

def load_image(filename):
    image = pyglet.image.load(filename)
    image.anchor_x = image.width // 2
    image.anchor_y = image.height // 2
    return image

# Images from www.kenney.nl, thank you!
# Public Domain (Creative Commons CC-0)
spaceship_img = load_image('assets/PNG/playerShip2_red.png')
asteroid_images = {
    1: [load_image('assets/PNG/Meteors/meteorGrey_tiny1.png'),
        load_image('assets/PNG/Meteors/meteorGrey_tiny2.png'),
       ],
    2: [load_image('assets/PNG/Meteors/meteorGrey_small1.png'),
        load_image('assets/PNG/Meteors/meteorGrey_small2.png'),
       ],
    3: [load_image('assets/PNG/Meteors/meteorGrey_med1.png'),
        load_image('assets/PNG/Meteors/meteorGrey_med2.png'),
       ],
    4: [load_image('assets/PNG/Meteors/meteorGrey_big1.png'),
        load_image('assets/PNG/Meteors/meteorGrey_big3.png'),
        load_image('assets/PNG/Meteors/meteorGrey_big4.png'),
       ],
}

pressed_keys = set()
objects = []
batch = pyglet.graphics.Batch()

class SpaceObject:
    def __init__(self, window, image, x, y, rotation=0, x_speed=0, y_speed=0):
        self.x = x
        self.y = y
        self.x_speed = x_speed
        self.y_speed = y_speed
        self.rotation = rotation
        self.sprite = pyglet.sprite.Sprite(image, batch=batch)
        self.window = window

    def tick(self, dt):
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

class Spaceship(SpaceObject):
    def __init__(self, window, rotation=0):
        super().__init__(window=window,
                         image=spaceship_img,
                         x=window.width / 2,
                         y=window.height / 2,
                         rotation=rotation,
                        )

    def tick(self, dt):
        if pyglet.window.key.LEFT in pressed_keys:
            self.rotation += dt * ROTATION_SPEED
        if pyglet.window.key.RIGHT in pressed_keys:
            self.rotation -= dt * ROTATION_SPEED
        if pyglet.window.key.UP in pressed_keys:
            rotation_radians = math.radians(self.rotation)
            self.x_speed += dt * ACCELERATION * math.cos(rotation_radians)
            self.y_speed += dt * ACCELERATION * math.sin(rotation_radians)

        super().tick(dt)

class Asteroid(SpaceObject):
    def __init__(self, window, size):
        # Asteroids start at edges of the screen, so they don't
        # initially collide with the ship
        edge = random.choice(['horizontal', 'vertical'])
        if edge == 'vertical':
            x = 0
            y = random.randrange(window.height)
        else:
            x = random.randrange(window.width)
            y = 0
        super().__init__(window=window,
                         image=random.choice(asteroid_images[size]),
                         x=x, y=y,
                         x_speed=random.uniform(-ASTEROID_SPEED, ASTEROID_SPEED),
                         y_speed=random.uniform(-ASTEROID_SPEED, ASTEROID_SPEED),
                         rotation=random.uniform(0, 360),
                        )
        self.rotation_speed = random.uniform(-ASTEROID_ROTATION_SPEED,
                                             ASTEROID_ROTATION_SPEED)

    def tick(self, dt):
        self.rotation += self.rotation_speed
        super().tick(dt)


def tick(dt):
    for obj in objects:
        obj.tick(dt)

def draw():
    window.clear()

    for x_offset in (-window.width, 0, window.width):
        for y_offset in (-window.height, 0, window.height):
            gl.glPushMatrix()
            gl.glTranslatef(x_offset, y_offset, 0)
            batch.draw()
            gl.glPopMatrix()

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
for i in range(3):
    objects.append(Asteroid(window, 4))
for i in range(1, 4):
    objects.append(Asteroid(window, i))

pyglet.app.run()
