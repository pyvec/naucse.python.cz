import math
import random

import pyglet
from pyglet import gl

WIDTH = 800
HEIGHT = 600
ROTATION_SPEED = 200
ACCELERATION = 300
SPACESHIP_RADIUS = 40
SHOOT_DELAY = 0.3
LASER_SPEED = 500
LASER_RADIUS = 5
COLLISION_SPEED_FACTOR = 0.2
ASTEROID_SPEED = 100
ASTEROID_ROTATION_SPEED = 3
ASTEROID_RADIUSES = {
    1: 8,
    2: 15,
    3: 20,
    4: 42,
}

def load_image(filename):
    image = pyglet.image.load(filename)
    image.anchor_x = image.width // 2
    image.anchor_y = image.height // 2
    return image

# Images from www.kenney.nl, thank you!
# Public Domain (Creative Commons CC-0)
spaceship_img = load_image('assets/PNG/playerShip2_red.png')
laser_img = load_image('assets/PNG/Lasers/laserBlue06.png')
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

def circle(x, y, radius):
    iterations = 20
    s = math.sin(2*math.pi / iterations)
    c = math.cos(2*math.pi / iterations)

    dx, dy = radius, 0

    gl.glBegin(gl.GL_LINE_STRIP)
    for i in range(iterations+1):
        gl.glVertex2f(x+dx, y+dy)
        dx, dy = (dx*c - dy*s), (dy*c + dx*s)
    gl.glEnd()

pressed_keys = set()
objects = []
batch = pyglet.graphics.Batch()

class SpaceObject:
    def __init__(self, window, image, x, y, radius, rotation=0, x_speed=0, y_speed=0):
        self.x = x
        self.y = y
        self.x_speed = x_speed
        self.y_speed = y_speed
        self.rotation = rotation
        self.radius = radius
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

    def hit_by_spaceship(self, spaceship):
        return

    def hit_by_laser(self, laser):
        return

    def delete(self):
        if self in objects:
            objects.remove(self)
            self.sprite.delete()

class Spaceship(SpaceObject):
    def __init__(self, window, rotation=0):
        super().__init__(window=window,
                         image=spaceship_img,
                         x=window.width / 2,
                         y=window.height / 2,
                         rotation=rotation,
                         radius=SPACESHIP_RADIUS,
                        )
        self.shoot_timer = 0

    def tick(self, dt):
        if pyglet.window.key.LEFT in pressed_keys:
            self.rotation += dt * ROTATION_SPEED
        if pyglet.window.key.RIGHT in pressed_keys:
            self.rotation -= dt * ROTATION_SPEED
        if pyglet.window.key.UP in pressed_keys:
            rotation_radians = math.radians(self.rotation)
            self.x_speed += dt * ACCELERATION * math.cos(rotation_radians)
            self.y_speed += dt * ACCELERATION * math.sin(rotation_radians)
        if pyglet.window.key.SPACE in pressed_keys:
            if self.shoot_timer < 0:
                self.shoot()
                self.shoot_timer = SHOOT_DELAY

        super().tick(dt)

        self.shoot_timer -= dt

        for obj in list(objects):
            if overlaps(self, obj):
                obj.hit_by_spaceship(self)

    def shoot(self):
        laser = Laser(self.window, rotation=self.rotation,
                      x=self.x, y=self.y,
                      ship_x_speed=self.x_speed, ship_y_speed=self.y_speed,
                     )
        objects.append(laser)


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
                         radius=ASTEROID_RADIUSES[size],
                        )
        self.size = size
        self.rotation_speed = random.uniform(-ASTEROID_ROTATION_SPEED,
                                             ASTEROID_ROTATION_SPEED)

    def tick(self, dt):
        self.rotation += self.rotation_speed
        super().tick(dt)

    def hit_by_spaceship(self, spaceship):
        spaceship.delete()

    def hit_by_laser(self, laser):
        split_x_speed = -laser.y_speed * COLLISION_SPEED_FACTOR
        split_y_speed = laser.x_speed * COLLISION_SPEED_FACTOR

        if self.size > 1:
            for i in range(2):
                asteroid = Asteroid(self.window, self.size-1)
                asteroid.x = self.x
                asteroid.y = self.y
                asteroid.x_speed = self.x_speed + split_x_speed
                asteroid.y_speed = self.y_speed + split_y_speed
                objects.append(asteroid)

                split_x_speed = -split_x_speed
                split_y_speed = -split_y_speed

        laser.delete()
        self.delete()


class Laser(SpaceObject):
    def __init__(self, window, x, y, ship_x_speed, ship_y_speed, rotation):
        rotation_radians = math.radians(rotation)
        x_speed = ship_x_speed + LASER_SPEED * math.cos(rotation_radians)
        y_speed = ship_y_speed + LASER_SPEED * math.sin(rotation_radians)
        super().__init__(window,
                         x=x + math.cos(rotation_radians),
                         y=y + math.sin(rotation_radians),
                         x_speed=x_speed,
                         y_speed=y_speed,
                         rotation=rotation,
                         image=laser_img,
                         radius=LASER_RADIUS,
                        )
        self.time_to_live = max(window.width, window.height) / LASER_SPEED

    def tick(self, dt):
        super().tick(dt)

        for obj in list(objects):
            if overlaps(self, obj):
                obj.hit_by_laser(self)

        self.time_to_live -= dt
        if self.time_to_live < 0:
            self.delete()

def distance(a, b, wrap_size):
    result = abs(a - b)
    if result > wrap_size / 2:
        result = wrap_size - result
    return result

def overlaps(a, b):
    distance_squared = (distance(a.x, b.x, window.width) ** 2 +
                        distance(a.y, b.y, window.height) ** 2)
    max_distance_squared = (a.radius + b.radius) ** 2
    return distance_squared < max_distance_squared

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
for i in range(1):
    objects.append(Asteroid(window, 4))
for i in range(1, 4):
    objects.append(Asteroid(window, i))

pyglet.app.run()
