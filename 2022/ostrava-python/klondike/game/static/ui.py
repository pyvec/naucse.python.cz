from pathlib import Path
import traceback

import pyglet

from klondike import udelej_hru, udelej_tah


WINDOW_CAPTION = 'Klondike Solitaire'

SUIT_NAMES = 'Kr', 'Ka', 'Pi', 'Sr'

KEYS = {
    pyglet.window.key.A: 'A',
    pyglet.window.key.B: 'B',
    pyglet.window.key.C: 'C',
    pyglet.window.key.D: 'D',
    pyglet.window.key.E: 'E',
    pyglet.window.key.F: 'F',
    pyglet.window.key.G: 'G',
    pyglet.window.key.U: 'U',
    pyglet.window.key.V: 'V',
    pyglet.window.key.W: 'W',
    pyglet.window.key.X: 'X',
    pyglet.window.key.Y: 'Y',
    pyglet.window.key.Z: 'Z',
}


image = pyglet.image.load('cards.png')
card_width = image.width // 14
card_height = image.height // 4

card_pictures = {}
for suit_number, suit_name in enumerate(SUIT_NAMES):
    for value in range(1, 14):
        card_pictures[value, suit_name] = image.get_region(
            card_width * value, card_height * suit_number,
            card_width, card_height,
        )

card_back_picture = image.get_region(0, card_height, card_width, card_height)
empty_slot_picture = image.get_region(0, 0, card_width, card_height)

label = pyglet.text.Label('x', color=(0, 200, 100, 255),
                          anchor_x='center', anchor_y='center')

window = pyglet.window.Window(resizable=True, caption=WINDOW_CAPTION)
press_queue = []


def get_dimensions():
    card_width = window.width / (7*6+1) * 5
    card_height = card_width * 19/14
    margin_x = card_width / 5
    margin_y = margin_x * 2
    offset_y = margin_x
    return card_width, card_height, margin_x, margin_y, offset_y


def draw_card(card, x, y, x_offset=0, y_offset=0, active=False):
    card_width, card_height, margin_x, margin_y, offset_y = get_dimensions()

    if card == None:
        pyglet.gl.glColor4f(0.5, 0.5, 0.5, 0.5)
        picture = empty_slot_picture
    else:
        if active:
            pyglet.gl.glColor4f(0.75, 0.75, 1, 1)
        else:
            pyglet.gl.glColor4f(1, 1, 1, 1)
        value, suit, is_face_up = card
        if is_face_up:
            picture = card_pictures[value, suit]
        else:
            picture = card_back_picture

    picture.blit(
        margin_x + (card_width + margin_x) * x + (x_offset * margin_x / 60),
        window.height - (margin_y + card_height) * (y+1) - offset_y * y_offset,
        width=card_width, height=card_height)


def draw_label(text, x, y, active):
    card_width, card_height, margin_x, margin_y, offset_y = get_dimensions()

    label.x = x * (card_width + margin_x) + margin_x + card_width / 2
    label.y = window.height - y * (card_height + margin_y) - margin_y / 2
    label.text = text
    if active:
        label.color = 200, 200, 255, 255
    else:
        label.color = 0, 200, 100, 255
    label.draw()


def draw_deck(letter, deck, x, y, x_offset=0, y_offset=0):
    active = (letter in press_queue)
    draw_label(letter, x, y, active)
    draw_card(None, x, y)
    for i, card in enumerate(deck):
        draw_card(card, x, y, x_offset*i, y_offset*i, active)


@window.event
def on_draw():
    # Enable transparency for images
    pyglet.gl.glEnable(pyglet.gl.GL_BLEND)
    pyglet.gl.glBlendFunc(pyglet.gl.GL_SRC_ALPHA, pyglet.gl.GL_ONE_MINUS_SRC_ALPHA)

    # Green background
    pyglet.gl.glClearColor(0, 0.25, 0.05, 1)
    window.clear()

    # Get dimensions
    card_width, card_height, margin_x, margin_y, offset_y = get_dimensions()
    label.font_size = margin_y / 2

    # Draw all the cards in the various decks
    for x, letter in enumerate('UV'):
        draw_deck(letter, game[letter], x, 0, x_offset=1)

    for x, letter in enumerate('WXYZ'):
        draw_deck(letter, game[letter], x + 3, 0, x_offset=1)

    for x, letter in enumerate('ABCDEFG'):
        draw_deck(letter, game[letter], x, 1, y_offset=1)


@window.event
def on_key_press(symbol, mod):
    if symbol in KEYS:
        press_queue.append(KEYS[symbol])
    handle_press_queue()


@window.event
def on_mouse_press(x, y, symbol, mod):
    card_width, card_height, margin_x, margin_y, offset_y = get_dimensions()
    if y > window.height - card_height - margin_y:
        deck_names = 'UV WXYZ'
    else:
        deck_names = 'ABCDEFG'
    deck_name = deck_names[int(x - margin_x/2) // int(card_width + margin_x)]
    if deck_name.strip():
        press_queue.append(deck_name)
    handle_press_queue()


def handle_press_queue():
    if press_queue == ['U']:
        press_queue.append('V')
    if len(press_queue) >= 2:
        source = press_queue[0]
        destination = press_queue[1]
        press_queue.clear()

        try:
            result = udelej_tah(game, source, destination)
        except ValueError as e:
            # Print *just* the error message
            msg = f'{source}→{destination}: {e}'
            window.set_caption(msg)
            print(msg)
        except Exception:
            # Print the error message, but ignore the error (so the
            # game can continue)
            traceback.print_exc()
        else:
            print(f'{source}→{destination}: {result}')
            window.set_caption(WINDOW_CAPTION)


game = udelej_hru()

pyglet.app.run()
