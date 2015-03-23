import math
import random

import pyglet
from pyglet import gl

window = pyglet.window.Window()

class Had:
    def __init__(self, rychlost_x, rychlost_y=10):
        self.x = 0
        self.y = 0
        self.rychlost_x = rychlost_x
        self.rychlost_y = rychlost_y
        self.obrazek = pyglet.resource.image('had.png')

    def vykresli(self):
        self.obrazek.blit(self.x, self.y)

    def posun(self, dt):
        self.x = self.x + dt * self.rychlost_x
        self.y = self.y + dt * self.rychlost_y
        if self.x < 0 or self.x > window.width - self.obrazek.width:
            self.rychlost_x = -self.rychlost_x
        if self.y < 0 or self.y > window.height - self.obrazek.height:
            self.rychlost_y = -self.rychlost_y

class TociciHad:
    def __init__(self, rychlost):
        self.uhel = 0
        self.rychlost = rychlost
        self.obrazek = pyglet.resource.image('had.png')

    def vykresli(self):
        gl.glRotatef(self.uhel, 0, 0, 1)
        self.obrazek.blit(0, 0)
        gl.glRotatef(-self.uhel, 0, 0, 1)

    def posun(self, dt):
        self.uhel = self.uhel + dt * self.rychlost


# Vykreslování

hadi = [Had(20), Had(200), Had(10, 10), TociciHad(100)]
for i in range(20):
    hadi.append(Had(random.uniform(-400, 400),
                    random.uniform(-400, 400)))

def vykresli():
    gl.glClear(gl.GL_COLOR_BUFFER_BIT)

    for had in hadi:
        had.vykresli()

window.push_handlers(on_draw=vykresli)

# Obnovování

def obnov(cas_od_posledniho_volani):
    for had in hadi:
        had.posun(cas_od_posledniho_volani)

pyglet.clock.schedule(obnov)

pyglet.app.run()
