# Nakresli mi hada

Většina videoher má vlastní svět – spoustu čísel, textů, seznamů a jiných
datových objektů, které popisují všechno, co ve hře je – celý *stav* hry.
Tenhle stav se časem mění, ať už automaticky nebo podle akcí hráče.
A docela často – většinou zhruba šedesátkrát za vteřinu – se stav hry převede
na obrázek, který se hráčovi ukáže.

Abys mohl{{a}} zobrazit hada, budeš napřed muset definovat stav hry – zadat
to, co se má vykreslovat.

Zkus se zamyslet, co všechno bude ten stav obsahovat: co všechno si počítač
musí o hře „pamatovat“, aby mohl aktuální stav zobrazit?

Bude potřebovat například aktuální polohu všech částí hada: kde má začátek?
Kroutí se doprava nebo doleva? Jak je dlouhý?
Naopak barvu hada se stavu ukložit nepotřebuješ – každý had v téhle hře bude
stejný.

Napadne tě, jak polohu hada zapsat pomocí čísel, seznamů a dalších základních
datových typů?


## Reprezentace hada

Asi nejjednodušší způsob, jak si v počítači „zapamatovat“ herního hada,
je pomocí seznamu souřadnic.

Pamatuješ si ze školy na kartézské souřadnice?
To je taková ta část matematiky, co možná vypadala že nemá praktické využití.
Pro počítačovou grafiku jsou ale souřadnice to co pro češtinu písmenka.
Pojďme si je osvěžit.

Každý bod v rovině (třeba na obrazovce!)
je možné popsat dvěmi čísly: <var>x</var>-ovou a <var>y</var>-ovou souřadnicí.
Ta <var>x</var>-ová říká, jak moc vlevo je bod od nějakého počátku,
ta <var>y</var>-ová udává jak moc je nahoře.
My za onen „počátek“ zvolíme roh okýnka, ve kterém se bude plazit náš had.

Na rozdíl od školní geometrie se had bude plazit po čtverečkové mřížce.
Je to jako na šachovnici – když jde pěšec na D5, D značí, jak moc je to
políčko vlevo od okraje a 5 jak moc „nahoře“.

Tady je had, který začíná na souřadnicích (1, 2) a hlavu má na (4, 5):

{{ figure(
    img=static('coords.svg'),
    alt="Had na „šachovnici“ se souřadnicemi",
) }}

Možná si všimneš, že matematický zápis souřadnic – (1, 2) – odpovídá
způsobu, jak se v Pythonu píšou <var>n</var>-tice.
To není náhoda!
Dvojice čísel je perfektní způsob, jak uložit souřdadnice kousku hada.

Had má ale kousků víc, a jinak dlouzí hadi jich budou mít různý počet.
Na to je dobré použít seznam. Seznam souřadnic.
A protože souřadnice pro nás budou dvojice čísel,
seznam souřadnic bude dvojice čísel.

Had z obrázku výše bude v Pythonu vypadat takto:

```python
had = [(1, 2), (2, 2), (3, 2), (3, 3), (3, 4), (3, 5), (4, 5)]
```

Tohle je reprezentace hada – to, co je z hlediska hry potřeba o konkrétním
hadovi vědět.

Počítačům (a programátorům?) to takhle stačí.
My si to ale zkusme zobrazit barevně, ať hadovi rozumí i hráč naší budoucí hry.


## Vykreslení hada

Na to, abychom hada vykreslili, použijeme okýnko z Pygletu.
Tady je základní kostra programu Pyglet, které už bys měl{{a}} rozumět.
Zkopíruj si ji do souboru `ui.py`; budeme ji dál rozvíjet.

```python
import pyglet

had = [(1, 2), (2, 2), (3, 2), (3, 3), (3, 4), (3, 5), (4, 5)]

window = pyglet.window.Window()

@window.event
def on_draw():
    window.clear()

@pyglet.clock.schedule
def sched(dt):
    print(dt)

pyglet.app.run()
```

U vykreslování hada musíme vyřešit jeden základní problém:
převod *logických souřadnic* na souřadnice *obrazovky*.

Displeje počítačů fungují podobně jako naše souřadnicová „šachovnice“:
jsou to čtvercové mřížky plné políček.
Každému políčku – *pixelu* – lze nastavit barvu.
Hlavní rozdíl proti šachovnici je v tom, že pixelů na obrazovce je mnohem,
mnohem víc.


{{ figure(
    img=static('coords-px.svg'),
    alt="Had na „šachovnici“ se souřadnicemi",
) }}


