#!/usr/bin/env python3
"""Hra typu Pong

Graficka hra pro dva hrace. Kazdy hrac ovlada "palku" na sve strane hriste,
a snazi se odpalit micek na protivnikovu stranu.

Ovladani:
Hrac 1: klavesy W a S
Hrac 2: sipky Nahoru a Dolu
Konec: Esc


Hra pouziva gravickou knihovnu Pyglet, coz je Pythonova nadstavba nad OpenGL.

Souradny system okynka je nasledujici::

        y ^
          |
    VYSKA +---------------------------------------+
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
          0               SIRKA/2               SIRKA

Pozor pokud mate zkusenosti s nekterymi grafickymi programy, nebo 2D
knihovnami. OpenGL pouziva matematicky souradny system, nula je vlevo *dole*.

"""

# Prvni radek (#!/usr/bin/env python3) je takzvany "shebang": na systemech
# zalozenych na Unixu (Linux, OS X) umoznuje spustit tenhle soubor jednoduse
# pomoci prikazu: ./pong.py

# A ted uz k samotne hre: napred naimportujeme potrebne veci z knihovny pyglet

import random

import pyglet
from pyglet import gl
from pyglet.window import key


# Nejake konstanty:

# Velikost okna (v pixelech)
SIRKA = 900
VYSKA = 600

VELIKOST_MICE = 20
TLOUSTKA_PALKY = 10
DELKA_PALKY = 100
RYCHLOST = 200  # v pixelech za sekundu
RYCHLOST_PALKY = RYCHLOST * 1.5  # taky v pixelech za sekundu

DELKA_PULICI_CARKY = 20
VELIKOST_FONTU = 42
ODSAZENI_TEXTU = 30


# Stav hry si budeme pamatovat v globalnich promennych.
# Profesionalni programator se nad tim zhrozi, ale pro nas je to tak zatim
# jednodussi.
# Jen nezapomente ze prikaz jako:
#     pozice_mice = [0, 0]
# ve funkci by vytvoril novou lokalni promennou, ktera by s globalni
# `pozice_mice` nemela nic spolecneho. Oproti tomu prikaz jako:
#     pozice_mice[0] = 0
# nastavi prvni prvek globalni `pozice_mice`.

pozice_palek = [VYSKA // 2, VYSKA // 2]  # vertikalni pozice dvou palek
pozice_mice = [0, 0]  # x, y souradnice micku -- nastavene v reset()
rychlost_mice = [0, 0]  # x, y slozky rychlosti micku -- nastavene v reset()
stisknute_klavesy = set()  # sada stisknutych klaves
skore = [0, 0]  # skore dvou hracu

# Pozice palek a micku vzdy bude urcovat stred daneho obdelnicku.


def reset():
    """Nastav pocatecni stav

    Tahle funkce se bude volat na zacatku programu, a taky potom co nektery
    z hracu prohraje.
    Funkce da micek doprostred obrazovky a da mu nahodnou rychlost.

    N.B. Neresetujeme tady skore ani pozici palek; ty zustavaji do dalsiho kola
    """
    pozice_mice[0] = SIRKA // 2
    pozice_mice[1] = VYSKA // 2

    # x-ova rychlost - bud vpravo, nebo vlevo
    if random.randint(0, 1):
        rychlost_mice[0] = RYCHLOST
    else:
        rychlost_mice[0] = -RYCHLOST
    # y-ova rychlost - uplne nahodna
    rychlost_mice[1] = random.uniform(-1, 1) * RYCHLOST


def obnov_stav(dt):
    """Spocitej novy stav hry

    Tahle funkce se vola mockrat za sekundu. V parametru ``dt`` dostane cas
    v sekundach od posledniho zavolani. Pocitac je rychly, proto to
    vetsinou bude velice male cislo - kolem sedesatiny sekundy (0.0167).
    """
    # Jak zname z fyziky, micek s rychlosti `v` se za cas `t` pohne o `v*t`.
    # Tenhle vyraz muzeme rozlozit pro slozky x, y.
    pozice_mice[0] += rychlost_mice[0] * dt
    pozice_mice[1] += rychlost_mice[1] * dt

    # odraz od spodni hrany
    # Kdyz je micek prilis "nizko", odrazi se, a zacne se pohybovat nahoru.
    # To znamena ze bude mit kladnou y-ovou slozku rychlosti.
    # x-ova slozka (vpravo/vlevo) se nezmeni.
    if pozice_mice[1] < VELIKOST_MICE // 2:
        rychlost_mice[1] = abs(rychlost_mice[1])

    # odraz od vrchni hrany
    # To same, ale micek je moc vysoko a musi se zacit pohybovat dolu.
    if pozice_mice[1] > VYSKA - VELIKOST_MICE // 2:
        rychlost_mice[1] = -abs(rychlost_mice[1])

    # pohyb palek - cyklus se projde dvkrat; jednou pro kazdou palku
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

    # odrazeni micku
    # Pokud je micek prilis vlevo, muze se budto odrazit od leve palky, anebo
    # tam palka neni a levy hrac prohral. Podobne pro pravou stranu.
    # Doporucuju si to nakreslit na papir :)

    # nejdriv si poznamename minimalni a maximalni pozici, kde musi byt palka
    # (t.j. stred palky), aby odrazila micek.
    palka_min = pozice_mice[1] - VELIKOST_MICE/2 - DELKA_PALKY/2
    palka_max = pozice_mice[1] + VELIKOST_MICE/2 + DELKA_PALKY/2

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


def nakresli_obdelnik(x1, y1, x2, y2):
    """Nakresli obdelnik na dane souradnice

    Nazorny diagram::

         y2 - +-----+
              |/////|
         y1 - +-----+
              :     :
             x1    x2
    """
    # Tady pouzivam volani OpenGL, ktere je pro nas zatim asi nejjednodussi
    # na pouziti
    gl.glBegin(gl.GL_TRIANGLE_FAN)   # zacni kreslit spojene trojuhelniky
    gl.glVertex2f(int(x1), int(y1))  # souradnice A
    gl.glVertex2f(int(x1), int(y2))  # souradnice B
    gl.glVertex2f(int(x2), int(y2))  # souradnice C, nakresli trojuhelnik ABC
    gl.glVertex2f(int(x2), int(y1))  # souradnice D, nakresli trojuhelnik BCD
    # dalsi souradnice E by nakreslila trojuhelnik CDE, atd.
    gl.glEnd()  # ukonci kresleni trojuhelniku


def nakresli_text(text, x, y, pozice_x):
    """Nakresli dany text na danou pozici

    Argument ``pozice_x`` muse byt "left" nebo "right", udava na kterou stranu
    bude text zarovnany
    """
    # Texty umi vypisovat Pyglet, a to tak, ze vytvorime objekt "napis"
    # a pak ho nakreslime.
    # (Normalne bychom tenhle objekt udelali jednou, a pak v nem jen menili
    # text a vykreslovali ho, ale pro jednoduchost si ho vytvorime tady:)
    napis = pyglet.text.Label(
        text,
        font_name='League Gothic',
        font_size=VELIKOST_FONTU,
        x=x, y=y, anchor_x=pozice_x)
    napis.draw()


def vykresli():
    """Vykresli stav hry"""
    gl.glClear(gl.GL_COLOR_BUFFER_BIT)  # smaz obsah okna (vybarvi na cerno)
    gl.glColor3f(1, 1, 1)  # nastav barvu kresleni na bilou

    # micek
    nakresli_obdelnik(
        pozice_mice[0] - VELIKOST_MICE // 2,
        pozice_mice[1] - VELIKOST_MICE // 2,
        pozice_mice[0] + VELIKOST_MICE // 2,
        pozice_mice[1] + VELIKOST_MICE // 2)

    # palky - udelame si seznam souradnic palek, a pro kazdou dvojici souradnic
    # v tom seznamu palku vykreslime
    for x, y in [(0, pozice_palek[0]), (SIRKA, pozice_palek[1])] :
        nakresli_obdelnik(
            x - TLOUSTKA_PALKY,
            y - DELKA_PALKY // 2,
            x + TLOUSTKA_PALKY,
            y + DELKA_PALKY // 2)

    # prerusovana pulici cara - slozena ze spousty malych obdelnicku
    for y in range(DELKA_PULICI_CARKY // 2, VYSKA, DELKA_PULICI_CARKY * 2):
        nakresli_obdelnik(
            SIRKA // 2 - 1,
            y,
            SIRKA // 2 + 1,
            y + DELKA_PULICI_CARKY)

    # A nakonec vypiseme skore obou hracu
    nakresli_text(str(skore[0]),
                  x=ODSAZENI_TEXTU,
                  y=VYSKA - ODSAZENI_TEXTU - VELIKOST_FONTU,
                  pozice_x='left')

    nakresli_text(str(skore[1]),
                  x=SIRKA - ODSAZENI_TEXTU,
                  y=VYSKA - ODSAZENI_TEXTU - VELIKOST_FONTU,
                  pozice_x='right')


def stisk_klavesy(symbol, modifikatory):
    """Osetri stisknuti klavesy

    Kdyz hrac stiskne spravnou klavesu, do mnoziny ``stisknute_klavesy`` se
    prida dvojice (n-tice) tvaru (smer, cislo palky).
    Program pak muze pohybovat palkou podle toho, co je v mnozine.
    """
    if symbol == key.W:
        stisknute_klavesy.add(('nahoru', 0))
    if symbol == key.S:
        stisknute_klavesy.add(('dolu', 0))
    if symbol == key.UP:
        stisknute_klavesy.add(('nahoru', 1))
    if symbol == key.DOWN:
        stisknute_klavesy.add(('dolu', 1))
    # N.B. klavesu ESC Pyglet osetri sam: zavre okno a ukonci funkci run()


def pusteni_klavesy(symbol, modifikatory):
    """Osetri pusteni klavesy

    Opak funkce ``stisk_klavesy`` -- podle argumentu vynda prislusnou
    dvojici z mnoziny.
    """
    # Vsimnete si pouziti funkce ``discard``: na rozdil od ``remove``
    # nezpusobi chybu, kdyz prvek v mnozine neni. Takze program nespadne,
    # kdyz napr. uzivatel zmackne klavesu, pak se prepne do naseho okna,
    # a pak teprve klavesu pusti.
    if symbol == key.W:
        stisknute_klavesy.discard(('nahoru', 0))
    if symbol == key.S:
        stisknute_klavesy.discard(('dolu', 0))
    if symbol == key.UP:
        stisknute_klavesy.discard(('nahoru', 1))
    if symbol == key.DOWN:
        stisknute_klavesy.discard(('dolu', 1))
    # Mimochodem, funkce pusteni_klavesy a stisk_klavesy by se daly hodne
    # zjednodusit pomoci slovniku. Zkusite to?

# Nastavime prvotni stav
reset()

# Vytvorime okno, do ktereho budeme kreslit
window = pyglet.window.Window(width=SIRKA, height=VYSKA)

# Oknu priradime par funkci, ktere budou reagovat na udalosti.
# Kdyz napr. uzivatel zmackne klavesu na klavesnici,
# Pyglet zavola funkci, kterou tady zaregistrujeme pod `on_key_press`,
# a preda ji prislusne argumenty.
# Jake vsechny udalosti muzou nastat, a jake argumenty se predaji prislusne
# funkci, se doctete v dokumentaci Pygletu,
# nebo pomoci `help(pyglet.window.event)`.
window.push_handlers(
    on_draw=vykresli,  # na vykresleni okna pouzij funkci `vykresli`
    on_key_press=stisk_klavesy,  # po stisknuti klavesy zavolej `stisk_klavesy`
    on_key_release=pusteni_klavesy,  # a mame i funkci na  pusteni klavesy
    )

# Jeste mame jednu podobnou funkci, kterou ale neprirazujeme primo
# oknu. Misto toho chceme aby ji Pyglet zavolal vzdycky kdyz "tiknou hodiny"
pyglet.clock.schedule(obnov_stav)

pyglet.app.run()  # vse je nastaveno, at zacne hra
# (funkce run() bude porad dokola volat obnov_stav, vykresli, a kdyz se mezitim
# neco stane, zavola navic funkci kterou jsme nastavili jako reakci na
# danou udalost)
