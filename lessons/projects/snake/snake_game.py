import random
from pathlib import Path

import pyglet

TILE_SIZE = 64
TILES_DIRECTORY = Path('static/snake-tiles')

class State:
    def __init__(self):
        self.snake = [(0, 0), (1, 0)]
        self.snake_direction = 0, 1
        self.width = 10
        self.height = 10
        self.food = []
        self.add_food()
        self.add_food()
        self.snake_alive = True
        self.queued_directions = []

    def move(self):
        if self.queued_directions:
            new_direction = self.queued_directions[0]
            del self.queued_directions[0]
            old_x, old_y = self.snake_direction
            new_x, new_y = new_direction
            if (old_x, old_y) != (-new_x, -new_y):
                self.snake_direction = new_direction

        if not self.snake_alive:
            return

        old_x, old_y = self.snake[-1]
        dir_x, dir_y = self.snake_direction
        new_x = old_x + dir_x
        new_y = old_y + dir_y

        # Kontrola vylezení z hrací plochy
        if new_x < 0:
            self.snake_alive = False
        if new_y < 0:
            self.snake_alive = False
        if new_x >= self.width:
            self.snake_alive = False
        if new_y >= self.height:
            self.snake_alive = False

        new_head = new_x, new_y
        if new_head in self.snake:
            self.snake_alive = False
        self.snake.append(new_head)

        if new_head in self.food:
            self.food.remove(new_head)
            self.add_food()
        else:
            del self.snake[0]

    def add_food(self):
        for try_number in range(100):
            x = random.randrange(self.width)
            y = random.randrange(self.height)
            position = x, y
            if (position not in self.snake) and (position not in self.food):
                self.food.append(position)
                return

    def image_name(self, index):
        return ("tail", "head")
        image_name = []
        x, y = self.snake[index]

        for index in (index-1, index+1):

            if index < 0:
                image_name.append('tail')
                continue
            if index > len(self.snake) - 1:
                image_name.append('head')
                continue

            x1, y1 = self.snake[index]
            if x1 < x:
                image_name.append('left')
            elif x1 > x:
                image_name.append('right')
            elif y1 < y:
                image_name.append('bottom')
            elif y1 > y:
                image_name.append('top')

        return image_name


red_image = pyglet.image.load('static/apple.png')
snake_tiles = {}
for path in TILES_DIRECTORY.glob('*.png'):
    print(f'loading {path}')
    snake_tiles[path.stem] = pyglet.image.load(path)

window = pyglet.window.Window()

state = State()
state.width = window.width // TILE_SIZE
state.height = window.height // TILE_SIZE


@window.event
def on_draw():
    window.clear()
    pyglet.gl.glEnable(pyglet.gl.GL_BLEND)
    pyglet.gl.glBlendFunc(pyglet.gl.GL_SRC_ALPHA, pyglet.gl.GL_ONE_MINUS_SRC_ALPHA)
    for i, (x, y) in enumerate(state.snake):
        source, dest = state.image_name(i)
        if dest == 'end' and not state.snake_alive:
            dest = 'dead'
        snake_tiles[source + '-' + dest].blit(
            x * TILE_SIZE, y * TILE_SIZE, width=TILE_SIZE, height=TILE_SIZE)
    for x, y in state.food:
        red_image.blit(
            x * TILE_SIZE, y * TILE_SIZE, width=TILE_SIZE, height=TILE_SIZE)


@window.event
def on_key_press(key_code, modifier):
    if key_code == pyglet.window.key.LEFT:
        new_direction = -1, 0
    if key_code == pyglet.window.key.RIGHT:
        new_direction = 1, 0
    if key_code == pyglet.window.key.DOWN:
        new_direction = 0, -1
    if key_code == pyglet.window.key.UP:
        new_direction = 0, 1
    state.queued_directions.append(new_direction)


def move(dt):
    state.move()


pyglet.clock.schedule_interval(move, 1/6)

pyglet.app.run()