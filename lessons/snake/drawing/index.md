# Nakresli mi hada

Většina videoher má celý herní svět uložený jako spoustu čísel, textů, seznamů
a jiných datových objektů, které popisují všechno, co ve hře je.
Tenhle stav se časem mění, ať už automaticky nebo podle akcí hráče.
A docela často – většinou zhruba šedesátkrát za vteřinu – se stav hry převede
na obrázek, který se hráčovi ukáže.

Abys mohl{{a}} zobrazit hada, budeš napřed muset definovat stav hry – zadat
to, co se má vykreslovat.

Zkus se zamyslet, co všechno bude ten stav obsahovat: co všechno si počítač
musí o hře „pamatovat“, aby mohl aktuální stav zobrazit?

Bude potřebovat například aktuální polohu všech částí hada: kde má začátek?
Kroutí se doprava nebo doleva? Jak je dlouhý?
Naopak barvu hada ve stavu uložit nepotřebuješ – každý had v téhle hře bude
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
My za onen „počátek“ zvolíme roh okýnka, ve kterém se bude náš had plazit.

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
Dvojice čísel je perfektní způsob, jak uložit souřadnice kousku hada.

Had má ale kousků víc, a jinak dlouzí hadi jich budou mít různý počet.
Na to je dobré použít seznam. Seznam souřadnic.
A protože souřadnice pro nás budou dvojice čísel,
seznam souřadnic bude seznam dvojic čísel.

Had z obrázku výše bude v Pythonu vypadat takto:

```python
snake = [(1, 2), (2, 2), (3, 2), (3, 3), (3, 4), (3, 5), (4, 5)]
```

Tohle je reprezentace hada – to, co je z hlediska hry potřeba o konkrétním
hadovi vědět.

Počítačům (a programátorům?) to takhle stačí.
My si to ale zkusme zobrazit barevně, ať hadovi rozumí i hráč naší budoucí hry.


## Logické a zobrazovací souřadnice

U vykreslování hada musíme vyřešit jeden základní problém:
převod *logických souřadnic* na souřadnice *obrazovky*.

Displeje počítačů fungují podobně jako naše souřadnicová „šachovnice“:
jsou to čtvercové mřížky plné políček.
Každému políčku – *pixelu* – lze nastavit barvu.
Hlavní rozdíl proti šachovnici je v tom, že pixelů na obrazovce je mnohem,
mnohem víc.

Kdyby byl každý „herní“ čtvereček 10×10 pixelů velký,
tak hlava hada z ukázky, která má „herní“ souřadnice (4, 5),
se na obrazovku bude vykreslovat na čtverečku, který začíná na (40, 50):

{{ figure(
    img=static('coords-px.svg'),
    alt="Had na „šachovnici“ se souřadnicemi obrazovky",
) }}

A ocas s „herními“ (*logickými*) souřadnicemi (1, 2) se vykreslí na čtvereček
se souřadnicemi (10, 20).


## Sázení čtverečku

Na to, abychom hada vykreslili, použijeme okýnko z Pygletu.
Tady je základní kostra Pygletí aplikace, které už bys měl{{a}} rozumět:

```python
import pyglet

window = pyglet.window.Window()

@window.event
def on_draw():
    window.clear()

pyglet.app.run()
```

V editoru si otevři nový soubor, ulož ho jako `had.py` a kostru programu
do něj zkopíruj.
Budeme ji dál rozvíjet.

<img src="{{ static('green.png') }}" alt="" style="display:block; float:right; margin: 2px; border: 1px solid #ccc; border-radius: 1px;">
Stáhni si soubor [green.png]({{ static('green.png') }}) – zelený čtvereček –
a dej ho do adresáře, kam píšeš kód.

Pod `import pyglet` přidej řádek, který tento obrázek načte.

```python
green_image = pyglet.image.load('green.png')
```

Potom zkus dovnitř do funkce `on_draw` přidat vykreslení obrázku na souřadnice
(40, 50), velikosti 10.

```python
    green_image.blit(40, 50, width=10, height=10)
```

Program spusť (`cd` do nového adresáře; `python had.py`). Funguje?
(Je docela důležité, aby fungoval – nevidíš-li zelený čtvereček,
nečti dál a program radši oprav.)

Jak vidíš, čtvereček je docela malý.
Budeme radši používat čtverečky větší, řekněme 64 pixelů.

To číslo je „střelené od boku“.
V programu ho použijeme několikrát, a možná ho později budeš chtít upravit.
Uložíme si ho proto do *konstanty* (proměnné, kterou nebudeme měnit).
Konstanty se tradičně pojmenovávají velkými písmeny a píšou se hned za řádek
`import` (i když to není technicky nutné).
Přidej tedy za `import` řádek:

```python
TILE_SIZE = 64
```

… a ve volání `green.blit` velikost čtverečku zohledni:

```python
    green_image.blit(4 * TILE_SIZE, 5 * TILE_SIZE,
                     width=TILE_SIZE, height=TILE_SIZE)
```

Povedlo se? Máš čtvereček?
Jestli ne, zkus si program celý, řádek po řádce, projít a zkontrolovat.
Nebo ho porovnej se vzorovým řešením (což je rychlejší varianta, ale míň
se naučíš).

{% filter solution %}
```python
import pyglet

TILE_SIZE = 64
green_image = pyglet.image.load('green.png')

window = pyglet.window.Window()

@window.event
def on_draw():
    window.clear()
    green_image.blit(4 * TILE_SIZE, 5 * TILE_SIZE,
                     width=TILE_SIZE, height=TILE_SIZE)

pyglet.app.run()
```
{% endfilter %}


## Sázení hada

Zkus teď na začátek programu – těsně pod `import` a konstantu – přidat
definici hada:

```python
snake = [(1, 2), (2, 2), (3, 2), (3, 3), (3, 4), (3, 5), (4, 5)]
```

A ve funkci `draw` vykresli všechny čtverečky hada.
Vzpomeň si, že seznam dvojic můžeš „projít“ pomocí cyklu `for` a „rozbalení“
<var>n</var>-tice:

```python
for x, y in snake:
    ...
```

Funguje to? Vidíš v tom – aspoň zhruba – hada poskládaného ze čtverečků?

{{ figure(
    img=static('coords-blocks.svg'),
    alt="Had na „šachovnici“ a ukázka programu",
) }}

Jestli ne, nezoufej, zkontroluj si to znovu, poptej se na radu.
Ukázkové řešení využij až jako krajní možnost, jak pokračovat dál.
Nebo pro kontrolu.

{% filter solution %}
```python
import pyglet

TILE_SIZE = 64

snake = [(1, 2), (2, 2), (3, 2), (3, 3), (3, 4), (3, 5), (4, 5)]

green_image = pyglet.image.load('green.png')

window = pyglet.window.Window()

@window.event
def on_draw():
    window.clear()
    for x, y in snake:
        green_image.blit(x * TILE_SIZE, y * TILE_SIZE,
                         width=TILE_SIZE, height=TILE_SIZE)

pyglet.app.run()
```
{% endfilter %}


## Krmení

<img src="{{ static('apple.png') }}" alt="" style="display:block; float:right; margin: 2px; border: 1px solid #ccc; border-radius: 1px;">
Aby bylo ve hře co dělat, budeme potřebovat pro hada krmení.
Stáhni si do adresáře s projektem obrázek
[apple.png]({{ static('apple.png') }}) a zkus vykreslit
jablíčka na následující souřadnice:

```python
food = [(2, 0), (5, 1), (1, 4)]
```

{% filter solution %}
```python
import pyglet

TILE_SIZE = 64

snake = [(1, 2), (2, 2), (3, 2), (3, 3), (3, 4), (3, 5), (4, 5)]
food = [(2, 0), (5, 1), (1, 4)]

red_image = pyglet.image.load('apple.png')
green_image = pyglet.image.load('green.png')

window = pyglet.window.Window()

@window.event
def on_draw():
    window.clear()
    for x, y in snake:
        green_image.blit(x * TILE_SIZE, y * TILE_SIZE,
                         width=TILE_SIZE, height=TILE_SIZE)
    for x, y in food:
        red_image.blit(x * TILE_SIZE, y * TILE_SIZE,
                       width=TILE_SIZE, height=TILE_SIZE)

pyglet.app.run()
```
{% endfilter %}

Možná si všimneš, že obrázek má ve hře trošičku „zubaté“ hrany.
To je dáno způsobem, jakým v Pygletu vykreslujeme.
Úplné vysvětlení by se do tohoto návodu nevešlo, potřebuje trochu hlubší
znalosti počítačové grafiky.
Proto uvedu jen řešení.
Do funkce `on_draw`, hned za `clear`, dej následující tři řádky:

```python
    # Lepší vykreslování (pro nás zatím kouzelné zaříkadlo)
    pyglet.gl.glEnable(pyglet.gl.GL_BLEND)
    pyglet.gl.glBlendFunc(pyglet.gl.GL_SRC_ALPHA, pyglet.gl.GL_ONE_MINUS_SRC_ALPHA)
```


## Načítání kousků hada

Teď, když umíš kreslit hada ze čtverců, zkusíme ho udělat hezčího.
Stáhni si archiv [snake-tiles.zip]({{ static('snake-tiles.zip') }})
a rozbal si ho tak, aby adresář `snake-tiles` s obrázky byl na stejné úrovni
jako program s hrou.
Struktura adresáře by měla vypadat takhle:

{{ figure(
    img=static('screenshot-dir.png'),
    alt="Adresářová struktura",
) }}

V archivuje spousta „kousků“ hada, které můžeme vykreslovat místo zelených
čtverečků.
Kousky vypadají následovně.
Všimni si pojmenování – každý kousek hada buď spojuje dvě strany obrázku,
nebo stranu obrázku s hlavou či ocasem.
Obrázek se jmenuje <var>odkud</var>-<var>kam</var>.png.

{{ figure(
    img=static('snake-tiles.png'),
    alt="Kousky hada",
) }}

> [note]
> Co jsou taková ta divná „hadí vajíčka”?
> <img src="{{ static('snake-tiles/end-end.png') }}" alt="" style="display:block; float:left; margin: 2px; border: 1px solid #ccc; border-radius: 1px;">
> To je pro případ, že by had byl jen jedno políčko dlouhý – a tedy měl hlavu
> i ocas na stejném políčku.
> V dodělané hře se do takového stavu nedostaneme (had bude začínat s délkou 2),
> ale než hru dokončíme, budou tyhle obrázky užitečné.

Pojďme si teď tyhle obrázky *načíst*.
Šlo by to dělat postupně, třeba takhle:

```python
bottom_left = pyglet.image.load('snake-tiles/bottom-left.png')
bottom_right = pyglet.image.load('snake-tiles/bottom-right.png')
bottom_top = pyglet.image.load('snake-tiles/bottom-top.png')
...
```

Ale obrázků je spousta, tímhle způsobem by to bylo zdlouhavé a nejspíš bys
na některý zapomněl{{a}}.

Proto si obrázky načteme automaticky, v cyklu, a dáme je do slovníku.

Program bude vypadat takhle:

* Začni s prázdným slovníkem.
* Pro každý *začátek* (`bottom`, `end`, `left`, `right`, `top`):
  * Pro každý *konec* (`bottom`, `end`, `left`, `right`, `top`, `dead`, `tongue`):
    * Budeme načítat obrázek „<var>začátek</var>-<var>konec</var>“; tento
      <var>klíč</var> si dej do proměnné
    * Načti obrázek <var>klíč</var>.png
    * Ulož obrázek do slovníku pod <var>klíč</var>.

```python
snake_tiles = {}
for start in ['bottom', 'end', 'left', 'right', 'top']:
    for end in ['bottom', 'end', 'left', 'right', 'top', 'dead', 'tongue']:
        key = start + '-' + end
        image = pyglet.image.load('snake-tiles/' + key + '.png')
        snake_tiles[key] = image
```

Pak celý slovník vypiš.
Výpis vypadat asi takhle:

```
{'right-tongue': <ImageData 64x64>, 'top-tongue': <ImageData 64x64>,
 'right-top': <ImageData 64x64>, 'left-bottom': <ImageData 64x64>,
 'end-left': <ImageData 64x64>, 'bottom-tongue': <ImageData 64x64>,
 'left-top': <ImageData 64x64>, 'bottom-bottom': <ImageData 64x64>,
 ...
```


## Housenka

A teď zkus načtení obrázků začlenit do programu s hadem!

Všechny importy patří nahoru, konstanty pod ně, a dál pak zbytek kódu.
Vypisovat načtený slovník ve hře nemusíš.
Zato ve vykreslovací funkci použij místo `green_image`
třeba `snake_tiles['end-end']`.

Místo čtverečků se teď objeví kuličky – místo hada budeš mít „housenku“.

{{ figure(
    img=static('caterpillar.png'),
    alt="Housenka",
) }}

{% filter solution %}
```python
from pathlib import Path

import pyglet

TILE_SIZE = 64
TILES_DIRECTORY = Path('snake-tiles')

snake = [(1, 2), (2, 2), (3, 2), (3, 3), (3, 4), (3, 5), (4, 5)]
food = [(2, 0), (5, 1), (1, 4)]

red_image = pyglet.image.load('apple.png')
snake_tiles = {}
for path in TILES_DIRECTORY.glob('*.png'):
    snake_tiles[path.stem] = pyglet.image.load(path)

window = pyglet.window.Window()

@window.event
def on_draw():
    window.clear()
    pyglet.gl.glEnable(pyglet.gl.GL_BLEND)
    pyglet.gl.glBlendFunc(pyglet.gl.GL_SRC_ALPHA, pyglet.gl.GL_ONE_MINUS_SRC_ALPHA)
    for x, y in snake:
        snake_tiles['end-end'].blit(
            x * TILE_SIZE, y * TILE_SIZE, width=TILE_SIZE, height=TILE_SIZE)
    for x, y in food:
        red_image.blit(
            x * TILE_SIZE, y * TILE_SIZE, width=TILE_SIZE, height=TILE_SIZE)

pyglet.app.run()
```
{% endfilter %}


## Jak vybrat čtverečky?

Místo toho, aby byl všude stejný kousek hada,
ale budeme chtít vybrat vždycky ten správný.

Jak na to?
Podle čeho ho vybrat?

Pojďme si to vyzkoušet vedle.
Vytvoř soubor `smery.py` a napiš do něj:

```python
snake = [(1, 2), (2, 2), (3, 2), (3, 3), (3, 4), (3, 5), (4, 5)]

for x, y in snake:
    print(x, y)
```

Tenhle kód vypisuje souřadnice:

```
1 2
2 2
3 2
3 3
3 4
3 5
4 5
```

Zkus vymyslet, jak by se tenhle kód dal změnit, aby vypisoval ke každé
souřadnici *směr* k předchozímu a následujícímu políčku – tedy odkud a kam
každý kousek hada „vede“.
Takhle:

{#
snake = [(1, 2), (2, 2), (3, 2), (3, 3), (3, 4), (3, 5), (4, 5)]

def direction(a, b):
    if a is None:
        return 'end'
    if b is None:
        return 'end'
    x1, y1 = a
    x2, y2 = b
    if x1 == x2 - 1:
        return 'left'
    elif x1 == x2 + 1:
        return 'right'
    elif y1 == y2 - 1:
        return 'bottom'
    elif y1 == y2 + 1:
        return 'top'
    return 'end'

for a, b, c in zip([None] + snake, snake, snake[1:] + [None]):
    x, y = b
    u = direction(a, b)
    v = direction(c, b)
    print(x, y, u, v)
#}


```
1 2 end right
2 2 left right
3 2 left top
3 3 bottom top
3 4 bottom top
3 5 bottom right
4 5 left end
```

Toto je **těžký úkol**.
Nepředpokládám, že ho zvládneš vyřešit hned, i když všechny potřebné informace
a nástroje k tomu znáš.
Zkus nad tím ale přemýšlet, nech si to rozležet v hlavě třeba přes noc,
vrať se k materiálům k předchozím lekcím (hlavně k úvodu do Pythonu),
zkoušej a objevuj… A časem na to přijdeš.

Až se to stane, zkus své řešení co nejvíc *zjednodušit* a pak ho zakomponovat
do vykreslovací funkce místo existujícího cyklu `for x, y in snake`.

```python
    for ... in ...:
        ...
        x = ...
        y = ...
        odkud = ...
        kam = ...
        ...

        snake_tiles[odkud + '-' + kam].blit(
            x * TILE_SIZE, y * TILE_SIZE, width=TILE_SIZE, height=TILE_SIZE)
```

Soubor `smery.py` po vyřešení nemaž, bude se ti pak hodit.

Odměnou za vyřešení tohoto úkolu ti bude had místo housenky.

Než na to přijdeš, zbytek programu ti neuteče.
Housenka je úplně stejně hratelná jako had, jen jinak vypadá.
Klidně přejdi na další část – logiku hry – s housenkou.
