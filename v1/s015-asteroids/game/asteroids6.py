import math
import random

import pyglet
from pyglet import gl

WIDTH = 1024
HEIGHT = 768
ROTATION_SPEED = 200
ACCELERATION = 300
SPACESHIP_RADIUS = 40
START_LIVES = 3
SHOOT_DELAY = 0.3
LASER_SPEED = 500
LASER_RADIUS = 5
UFO_RADIUS = 45
UFO_SPEED = 50
UFO_ROTATION_SPEED = 4000
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
space_img = load_image('assets/Backgrounds/blue.png')
life_img = load_image('assets/PNG/UI/playerLife2_red.png')
ufo_img = load_image('assets/PNG/ufoGreen.png')
ufo_laser_img = load_image('assets/PNG/Lasers/laserGreen13.png')
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

life_sprite = pyglet.sprite.Sprite(life_img)

exhaust_images = []
for i in range(25):
    name = 'assets2/PNG/White puff/whitePuff{:02}.png'.format(i)
    exhaust_images.append(load_image(name))

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
main_batch = pyglet.graphics.Batch()
exhaust_batch = pyglet.graphics.Batch()
ufo_batch = pyglet.graphics.Batch()

pyglet.font.add_file('assets/Bonus/kenvector_future_thin.ttf')
level_label = pyglet.text.Label('Loading...', x=10, y=10,
                                font_name='Kenvector Future Thin',
                               )

class SpaceObject:
    kind = None

    def __init__(self, window, image, x, y, radius, rotation=0,
                 x_speed=0, y_speed=0, batch=main_batch):
        self.x = x
        self.y = y
        self.x_speed = x_speed
        self.y_speed = y_speed
        self.rotation = rotation
        self.radius = radius
        self.sprite = pyglet.sprite.Sprite(image, batch=batch)
        self.window = window

    def tick(self, dt, wrap_x=True, wrap_y=True):
        self.x += dt * self.x_speed
        self.y += dt * self.y_speed

        if wrap_x:
            if self.x < 0:
                self.x += self.window.width
            if self.x > self.window.width:
                self.x -= self.window.width
        if wrap_y:
            if self.y < 0:
                self.y += self.window.height
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

    def explode(self, explosion_size):
        for i in range(explosion_size):
            t = random.uniform(0, math.pi*2)
            rx = random.uniform(0, 100) * math.cos(t)
            ry = random.uniform(0, 100) * math.sin(t)
            debris = Debris(self.window, x=self.x, y=self.y,
                            x_speed=self.x_speed + rx * 3,
                            y_speed=self.y_speed + ry * 3,
                            time_to_live=4,
                           )
            objects.append(debris)
            explosion = Exhaust(self.window, x=self.x, y=self.y,
                                x_speed=self.x_speed + rx * 2,
                                y_speed=self.y_speed + ry * 2,
                                die_speed=1,
                               )
            objects.append(explosion)

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
        self.lives = START_LIVES - 1
        self.invincibility_timer = 0
        self.size = 5
        self.level = 0

    def tick(self, dt):
        if pyglet.window.key.LEFT in pressed_keys:
            self.rotation += dt * ROTATION_SPEED
            objects.append(make_exhaust(self, -1))
        if pyglet.window.key.RIGHT in pressed_keys:
            self.rotation -= dt * ROTATION_SPEED
            objects.append(make_exhaust(self, 1))
        if pyglet.window.key.UP in pressed_keys:
            rotation_radians = math.radians(self.rotation)
            self.x_speed += dt * ACCELERATION * math.cos(rotation_radians)
            self.y_speed += dt * ACCELERATION * math.sin(rotation_radians)
            objects.append(make_exhaust(self))
        if pyglet.window.key.SPACE in pressed_keys:
            if self.shoot_timer < 0:
                self.shoot()
                self.shoot_timer = SHOOT_DELAY

        super().tick(dt)

        self.shoot_timer -= dt

        self.invincibility_timer -= dt
        if self.invincibility_timer < 0:
            self.sprite.opacity = 255
            for obj in list(objects):
                if overlaps(self, obj):
                    obj.hit_by_spaceship(self)
        else:
            self.sprite.opacity = 255 * (
                abs(math.sin(self.invincibility_timer * 5)) *
                max(0, min(2.5 - self.invincibility_timer, 1))
            )

    def shoot(self):
        laser = ShipLaser(self.window, rotation=self.rotation,
                          x=self.x, y=self.y,
                          ship_x_speed=self.x_speed, ship_y_speed=self.y_speed,
                         )
        objects.append(laser)

    def destroy(self, asteroid):
        if self.invincibility_timer > 0:
            return

        self.explode(50)

        self.lives -= 1
        if self.lives < 0:
            self.delete()
            pyglet.text.Label('Game over', anchor_x='center',
                              x=window.width/2, y=window.height/2,
                              font_name='Kenvector Future Thin',
                              font_size=50,
                              batch=main_batch,
                             )
        else:
            self.invincibility_timer = 3
            self.x = self.window.width / 2
            self.y = self.window.height / 2
            self.x_speed = 0
            self.y_speed = 0
            pressed_keys.clear()


class Ufo(SpaceObject):
    def __init__(self, window):
        super().__init__(window=window,
                         image=ufo_img,
                         x=-UFO_RADIUS,
                         y=random.uniform(UFO_RADIUS, window.height-UFO_RADIUS),
                         x_speed=random.uniform(UFO_SPEED/2, UFO_SPEED*2),
                         y_speed=UFO_SPEED,
                         rotation=0,
                         radius=UFO_RADIUS,
                         batch=ufo_batch,
                        )
        self.shoot_timer = 0
        self.rotation_speed = random.choice([-0.1, 0.1])

    def tick(self, dt):
        self.rotation += self.rotation_speed * dt
        self.rotation_speed *= 1.105
        if abs(self.rotation_speed) > UFO_ROTATION_SPEED:
            self.rotation_speed = random.choice([-1, 1])
            laser = UfoLaser(self, ship)
            objects.append(laser)
            self.x_speed = random.uniform(0, UFO_SPEED)
            self.y_speed = random.uniform(-UFO_SPEED, UFO_SPEED)
        super().tick(dt, wrap_x=False)
        if self.x > self.window.width+UFO_RADIUS:
            self.delete()

    def hit_by_laser(self, laser):
        self.explode(30)
        self.delete()

class Asteroid(SpaceObject):
    kind = 'asteroid'

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
        spaceship.destroy(self)

    def hit_by_laser(self, laser):
        split_x_speed = -laser.y_speed * COLLISION_SPEED_FACTOR
        split_y_speed = laser.x_speed * COLLISION_SPEED_FACTOR

        for i in range(2):
            if self.size > 1:
                asteroid = Asteroid(self.window, self.size-1)
                asteroid.x = self.x
                asteroid.y = self.y
                asteroid.x_speed = self.x_speed + split_x_speed
                asteroid.y_speed = self.y_speed + split_y_speed
                objects.append(asteroid)

            for j in range(self.size):
                x_rand_speed = random.uniform(-40, 40)
                y_rand_speed = random.uniform(-40, 40)
                debris = Debris(self.window, x=self.x, y=self.y,
                                x_speed=self.x_speed - split_y_speed + x_rand_speed,
                                y_speed=self.y_speed + split_x_speed + y_rand_speed,
                                time_to_live=self.size,
                                )
                objects.append(debris)

            split_x_speed = -split_x_speed
            split_y_speed = -split_y_speed

        laser.delete()
        self.delete()

        for obj in objects:
            if obj.kind == 'asteroid':
                return

        # No asteroids!
        start_level()


class Laser(SpaceObject):
    def __init__(self, window, x, y, ship_x_speed, ship_y_speed, rotation, image=laser_img):
        rotation_radians = math.radians(rotation)
        x_speed = ship_x_speed + LASER_SPEED * math.cos(rotation_radians)
        y_speed = ship_y_speed + LASER_SPEED * math.sin(rotation_radians)
        super().__init__(window,
                         x=x + math.cos(rotation_radians),
                         y=y + math.sin(rotation_radians),
                         x_speed=x_speed,
                         y_speed=y_speed,
                         rotation=rotation,
                         image=image,
                         radius=LASER_RADIUS,
                        )
        self.time_to_live = max(window.width, window.height) / LASER_SPEED

    def tick(self, dt):
        super().tick(dt)

        self.time_to_live -= dt
        if self.time_to_live < 0:
            self.delete()

class ShipLaser(Laser):
    def tick(self, dt):
        super().tick(dt)

        for obj in list(objects):
            if overlaps(self, obj):
                obj.hit_by_laser(self)

class UfoLaser(Laser):
    def __init__(self, ufo, ship):
        super().__init__(ufo.window,
                         x=ufo.x,
                         y=ufo.y,
                         ship_x_speed=0,
                         ship_y_speed=0,
                         rotation=math.degrees(math.atan2(ship.y-ufo.y, ship.x-ufo.x)),
                         image=ufo_laser_img,
                        )

    def hit_by_spaceship(self, spaceship):
        spaceship.destroy(self)

def make_exhaust(spaceship, side=0):
    rotation_radians = math.radians(spaceship.rotation + side * 15)
    x_unit = -math.cos(rotation_radians)
    y_unit = -math.sin(rotation_radians)
    start_radians = math.radians(spaceship.rotation - side * 48)
    x_start = -math.cos(start_radians)
    y_start = -math.sin(start_radians)
    if side:
        speed = 100
        die_speed = 4
    else:
        speed = 200
        die_speed = 3
    x_rand_speed = random.uniform(-20,20)
    y_rand_speed = random.uniform(-20,20)
    return Exhaust(spaceship.window,
                    x=spaceship.x + x_start * 43,
                    y=spaceship.y + y_start * 43,
                    x_speed=spaceship.x_speed + x_unit*speed + x_rand_speed,
                    y_speed=spaceship.y_speed + y_unit*speed + y_rand_speed,
                    die_speed=die_speed,
                    small=side,
                   )

class Exhaust(SpaceObject):
    def __init__(self, window, x, y, x_speed, y_speed, die_speed, small=False):
        super().__init__(window,
                         x=x, y=y, x_speed=x_speed, y_speed=y_speed,
                         image=random.choice(exhaust_images),
                         radius=0,
                         batch=exhaust_batch,
                        )
        self.time_to_live = 2
        self.die_speed = die_speed
        if small:
            self.sprite.scale = 1/30
        else:
            self.sprite.scale = 1/10

    def tick(self, dt):
        super().tick(dt)

        self.time_to_live -= dt * self.die_speed
        if self.time_to_live > 1:
            t = self.time_to_live - 1
            self.sprite.color = (255, 255 * t, 0)
        elif self.time_to_live > 0:
            t = self.time_to_live
            self.sprite.color = (255 * t, 0, 0)
            self.sprite.opacity = 255 * t
        else:
            self.delete()

class Debris(SpaceObject):
    def __init__(self, window, x, y, x_speed, y_speed, time_to_live):
        super().__init__(window, x=x, y=y, x_speed=x_speed, y_speed=y_speed,
                         image=random.choice(asteroid_images[1]),
                         radius=0,
                         batch=exhaust_batch,
                        )
        self.time_to_live = time_to_live
        self.die_speed = 3
        self.sprite.color = 0, 0, 0
        self.sprite.scale = 1/2
        self.rotation_speed = random.uniform(-20, 20)

    def tick(self, dt):
        self.rotation += self.rotation_speed * dt
        super().tick(dt)

        self.time_to_live -= dt * self.die_speed
        if self.time_to_live > 1:
            self.sprite.opacity = 255
        elif self.time_to_live > 0:
            self.sprite.opacity = 255 * self.time_to_live
        else:
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

    if random.uniform(0, 600) < dt * ship.level:
        objects.append(Ufo(window))

def draw():
    window.clear()

    for x in range(0, window.width+space_img.width, space_img.width):
        for y in range(0, window.height+space_img.height, space_img.height):
            space_img.blit(x=x, y=y)

    exhaust_batch.draw()
    for y_offset in (-window.height, 0, window.height):
        gl.glPushMatrix()
        gl.glTranslatef(0, y_offset, 0)
        ufo_batch.draw()
        gl.glPopMatrix()
    for x_offset in (-window.width, 0, window.width):
        for y_offset in (-window.height, 0, window.height):
            gl.glPushMatrix()
            gl.glTranslatef(x_offset, y_offset, 0)
            main_batch.draw()
            gl.glPopMatrix()

    for i in range(ship.lives):
        life_sprite.y = 40
        life_sprite.x = 30 + 40 * i
        life_sprite.draw()

    level_label.draw()

def key_pressed(key, mod):
    pressed_keys.add(key)
    if key == pyglet.window.key.S:
        pyglet.image.get_buffer_manager().get_color_buffer().save('screenshot.png')

def key_released(key, mod):
    pressed_keys.discard(key)

def start_level():
    ship.level += 1
    ship.lives += 1
    for i in range(ship.level):
        objects.append(Asteroid(window, 4))
    level_label.text = 'Level {}'.format(ship.level)

window = pyglet.window.Window(width=WIDTH, height=HEIGHT)

window.push_handlers(
    on_draw=draw,
    on_key_press=key_pressed,
    on_key_release=key_released,
    on_resize=lambda w, h: print(w, h),
)

pyglet.clock.schedule(tick)

ship = Spaceship(window)
objects.append(ship)
start_level()

pyglet.app.run()
