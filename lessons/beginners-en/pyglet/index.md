# Graphics

Today we will learn how to write graphical applications in Python.

We will use library that is not built-in Python (similar to pytest
which we used for testing). So we have to install it first. open 
your virtual environment and then use `pip` - specifically command -
`python -m pip install pyglet`.
It looks like this:


```console
(venv)$ python -m pip install pyglet
Collecting pyglet
  Downloading pyglet-1.2.4-py3-none-any.whl (964kB)
Installing collected packages: pyglet
Successfully installed pyglet-1.2.4
```

If you installed pygled successfully try to run
following program. There should appear
black window.

```python
import pyglet
window = pyglet.window.Window()
pyglet.app.run()
print('Done!')
```

> [note]
> If your window is black but there is some rubbish
> don't mind it now. Before we will start to draw 
> in the window we will clean it.


Done? Let's explain what is exactly happening.


## Interactive programs

Let's have a look how program for 1D tic tac toe looks like.
You can see in the comments what every line of code is
doing.


```python
def tictactoe1d():
    field = '-' * 20                # Game preparation
    while True:                     # Repetition:
        field = player_move(field)  # 1. Ask player about their move
        if evaluate(field) != '-':  # 2. Evaluate move
            break
        print(field)                # 3. Print how game looks like

                                    # And again:
        field = ai_move(field)      # 1. Ask computer about its move
        if evaluate(field) != '-':  # 2. Evaluate move
            break
        print(field)                # 3. Print how game looks like
```

We have two types of actions/events in this program, which alternate regularly.
When action is called, it's then evaluated and printed.

We already had similar structure of reactions, for example:
rock, paper, scissors.

* Some preparation
* Until program finishes
    * Read some input
    * Evaluate the input
    * Print result

And similarly works a lot of different programs which
somehow respond to input or other actions/events.

Web server is waiting for *request* about webpage. When it
gets some, it will proccess for example page that is saved on
disk and as output it sends some response.

More complex programs are responding to a lot
of sorts of actions/events, not only to "request"
or "player move"/"computer move". What happens after
input evaluation depends on type of the action.

Your web browser is waiting for a mouse click or a keystroke
and it will behave by the type of key you press or where you
clicked - maybe it sends request to the remote server.
And then it's waiting for another action. There may come a response from
server and then the web browser renders the page
to the screen. Or the user can press "STOP"
and the request is canceled.

The text editor waits for different input from the keyboard
or mouse and it has to evaluate every input.


So a similar program structure - loop that reads the input, 
processes it and produces output - it is very useful.
It is called *event loop* and programs built on it
are *event-driven*.

When there is something useful for more programs it is
not usuall that each programmer will write it all over from the beginning
but some people write it once, pack it as a *library* and then everytone 
is using it.

## Pyglet 🐷

One of such libraries is Pyglet.
It contains event loop and some functions for
2D graphics(with help of another library - OpenGL)
and also retrieving keyboard and mouse events.

Let's go back to the program that opens a window:

```python
import pyglet
window = pyglet.window.Window()
pyglet.app.run()
print('Done!')
```

The whole event loop is hidden in function `pyglet.app.run()`.
Loading of an input (e.g. from keyboard) is Pyglet doing
itself but evaluation and drawing the result is for each program
different so you will have to program it by yourself. 

Currently Pyglet is proccessing only two events:
closing of the window (by "x" button which is added by 
operating system) and pressing <kbd>Esc</kbd> key,
which also closes the window.
After the window is closed event loop (function `pyglet.app.run()`)
ends and program continues to the next line of code.


## Text

<kbd>Esc</kbd> key is not interesting
so let's have a look on another keys.

In Pyglet when you want respond to some event you have to
write a function and then you *register* it - you tell
Pyglet to call this function in the right time.
Event that happens when user is writing something
on keyboard is called `on_text` in Pyglet and it's
processed this way:

{# XXX - highlight "process_text" and "window.push_handlers" blocks #}
```python
import pyglet
window = pyglet.window.Window()

def process_text(text):
    print(text)

window.push_handlers(on_text=process_text)

pyglet.app.run()
```

What is it doing? `window.push_handlers(on_text=process_text)`
tells Pyglet that when user writes something into our
window Pyglet have to call function `process_text`. This
function gets one argument with what user wrote.

Notice that when we are registering our function
we are __not__ writing brackets although we 
[once]({{ lesson_url('beginners/functions') }}) said
that functions have to be called that way.
Do you remember this example? Maybe you found it wird back then.

```python
from math import sin
print(sin(1))
print(sin)
print(sin + 1)
```

Now when we know apart from numbers, strings, `True/False` also
files, lists, tuples and others we can say that function
in Python is value like every other.
Numbers can be multiplied, strings can be written into a file,
we can read from files and functions are only different by that
that they can be called.
But before we call function we can store the function
into some variable:

```python
write = print
write("Hello world!")
```

or we can pass a function to another function as an argument:

```python
print(print)
```

And function `window.push_handlers` was directly writen to
process a function. Why? Pyglet doesn't need one result
of function `process_text` - it is useless for it.
And we also can't call the function cause we don't have
usefull `text` as an argument.
That's why we give to Pyglet the function itself and it
will be called everytime user press some key.

## Time ⏲

Before we move to the real graphics we will have a look
on another type of event.

It's a *clock tick*). That's an event, which is happening
regularly after some time.

Registration of function for ticks is done differently than `on_text`:
Funkce pro tiky se registruje trochu jinak než `on_text`:

{# XXX - highlight "tick" and "schedule_interval" blocks #}
```python
import pyglet
window = pyglet.window.Window()

def tick(t):
    print(t)

pyglet.clock.schedule_interval(tick, 1/30)

def process_text(text):
    print(text)

window.push_handlers(on_text=process_text)

pyglet.app.run()
```

What is it doing? `pyglet.clock.schedule_interval(tick, 1/30)`
tells Pyglet that it should cal the function `tick` every
`1/30` of a second.

Function `tick` gets only one argument - 
how much time has elapsed since the last call.
Mostly it is not exactly 1/30 of a second, it's a bit
more. Computer has also another things to do, so it
doesn't get to our program immediately and it also
takes some time for Python to call our function.

> [note]
> And why 1/30 of a second? Because we will
> create animation later. When 30 images per second 
> are replaced in front of our eyes, 
> the brain connects them to create an illusion of smooth motion.
> <br>
> Most of the movies are using only 24 pictures per second and
> realistic 3D game has up to 60.

## Vykreslování 🖌

<img src="{{ static('had.png') }}" alt="" style="display:block;float:right;">

Program, který vypisuje na terminál spoustu čísel,
není asi zas tak zajímavý.
Téma téhle stránky je ale grafika, tak se začněme od
terminálu odpoutávat. Pojďme kreslit.

Najdi si na Internetu nějaký obrázek. Ne moc velký,
tak 3cm, ať je kolem něj v našem černém okýnku dost
místa, a nejlépe ve formátu PNG. Začni třeba na
[téhle stránce](https://www.google.cz/search?tbs=ift:png&tbm=isch&q=snake+icon).
Ale nevybírej obrázek, který je celý černý, protože by v našem černém okně
nebyl vidět.
Ulož si ho do adresáře, odkud spouštíš svůj pythonní
program. Já mám třeba obrázek hada v souboru `had.png`.

Pak obrázek vykresli (použij jméno souboru se svým obrázkem):

{# XXX: Highlight "obrazek =", "had =", "vykresli", "on_draw=vykresli" blocks #}
{# XXX: Highlight 'had.png' strongly #}
```python
import pyglet
window = pyglet.window.Window()

def tik(t):
    print(t)

pyglet.clock.schedule_interval(tik, 1/30)

def zpracuj_text(text):
    print(text)

obrazek = pyglet.image.load('had.png')
had = pyglet.sprite.Sprite(obrazek)

def vykresli():
    window.clear()
    had.draw()

window.push_handlers(
    on_text=zpracuj_text,
    on_draw=vykresli,
)

pyglet.app.run()
```

Povedlo se?

Vysvětleme si, co se tady děje:

* `obrazek = pyglet.image.load('had.png')` načte ze souboru obrázek
* `had = pyglet.sprite.Sprite(obrazek)`
  vytvoří speciální objekt [Sprite](https://cs.wikipedia.org/wiki/Sprite_%28po%C4%8D%C3%ADta%C4%8Dov%C3%A1_grafika%29),
  který určuje, že tento obrázek chceme „posadit“
  na určité místo v černém okýnku.
  Když neuděláme nic dalšího, bude obrázek čekat v levém rohu.
* Funkce `vykresli()` se stará o vykreslení okna – výstup našeho programu.
  Volá se vždycky, když je potřeba okno překreslit –
  například když okno minimalizuješ a pak vrátíš
  nebo přesuneš částečně ven z obrazovky a pak dáš zase zpět.
  A nebo když budeme něco animovat.

> [note]
> Některé operační systémy si pamatují i obsah oken,
> které nejsou vidět, ale není radno na to spoléhat.

* `window.clear()` vyčistí okno – natře ho černou barvou a smaže
  všechno, co v něm bylo předtím.

> [note]
> Na spoustě počítačů tohle není potřeba.
> Ale je lepší psát programy tak, aby
> běžely správně kdekoli.

* `had.draw()` nakreslí obrázek pomocí předpřipraveného *spritu* `had`.
* `window.push_handlers(on_draw=vykresli)` zaregistruje funkci `vykresli` –
  řekne Pygletu, aby ji volal vždy, když je třeba.
  <br>
  Když potřebuješ zaregistrovat pro jedno okno
  víc funkcí na obsluhu událostí,
  dají se dát funkci `push_handlers`
  takhle najednou.

Jakékoli kreslení se *musí* dělat v rámci kreslící funkce,
kterou Pyglet volá z `on_draw`.
Jinde funkce jako `clear` a `draw` nebudou fungovat správně.

## Animace

Pojď si teď se Spritem trochu pohrát.

Do funkce `zpracuj_text` dej místo printu tento příkaz:

```python
def zpracuj_text(text):
    had.x = 150
```


Náš Sprite má *atribut* (angl. *attribute*)
`x`, který určuje jeho <var>x</var>-ovou souřadnici –
jak moc je vpravo od okraje okna.
Tenhle atribut se dá nastavit, jak budeš chtít – nejčastěji
v reakci na nějakou událost, ale často se nastavuje
i na začátku programu.

Zajímavé je zkusit k `x` něco přičíst při každém tiknutí hodin.
Dokážeš předpovědět, co udělá tenhle kód?

```python
def tik(t):
    had.x = had.x + t * 20
```


Nebojíš-li se matematiky, naimportuj `math`
a nech obrázek, ať se pohybuje podle nějaké funkce:

```python
def tik(t):
    had.x = had.x + t * 20
    had.y = 20 + 20 * math.sin(had.x / 5)
```


Co se stane, když začneš měnit ta čísla?

Co se stane, když zkusíš podobně nastavovat atribut `rotation`?

## Zavolej později

<img src="{{ static('had2.png') }}" alt="" style="display:block;float:right;">

Pyglet umí kromě opakovaného „tikání“ zavolat funkci
jednorázově, za určitou dobu.

Stáhni si (nebo vytvoř) druhý obrázek. Já mám druhého
hada, tentokrát s trochu natočenou hlavou a ocasem.

Až budeš mít obrázek v adresáři s programem,
přidej těsně před `pyglet.app.run()` tenhle kus kódu:

{# XXX: Highlight 'had2.png' strongly #}
```python
obrazek2 = pyglet.image.load('had2.png')

def zmen(t):
    had.image = obrazek2

pyglet.clock.schedule_once(zmen, 1)
```

Volání `schedule_once(zmen, 1)` říká Pygletu,
že za jednu vteřinu má zavolat funkci `zmen`.
A funkce změní obrázek – stejně jako se předtím měnily
souřadnice.

`schedule_once` se dá volat i v rámci obsluhy jiné události. Zkus funkci `zmen`
nahradit tímhle:

```python
def zmen(t):
    had.image = obrazek2
    pyglet.clock.schedule_once(zmen_zpatky, 0.2)

def zmen_zpatky(t):
    had.image = obrazek
    pyglet.clock.schedule_once(zmen, 0.2)
```

## Klik 🐭

Poslední věc, na kterou se tady naučíme reagovat, je klikání.
Těsně před `window.push_handlers` napiš funkci:

```python
def klik(x, y, tlacitko, mod):
    had.x = x
    had.y = y
```

… a pak v `push_handlers` ji zaregistruj
pomocí řádku `on_mouse_press=klik,`.

Co znamená který argument, to zkus zjistit sama.

> [note] Nápověda
> * Dokud příkazovou řádku neopustíš úplně, bude fungovat `print`!
>   Kdykoliv budeš chtít zjistit nějakou hodnotu, prostě si ji vypiš.
> * Kolik má myš tlačítek?
> * Jak se projeví <kbd>Shift</kbd>+klik?


## Pokračování příště

Koukám že kódu už je dnes tak akorát na ukončení lekce:

```python
import math

import pyglet

window = pyglet.window.Window()

def tik(t):
    had.x = had.x + t * 20

pyglet.clock.schedule_interval(tik, 1/30)

def zpracuj_text(text):
    had.x = 150
    had.rotation = had.rotation + 10

obrazek = pyglet.image.load('had.png')
had = pyglet.sprite.Sprite(obrazek, x=10, y=10)

def vykresli():
    window.clear()
    had.draw()

def klik(x, y, tlacitko, mod):
    print(tlacitko, mod)
    had.x = x
    had.y = y

window.push_handlers(
    on_text=zpracuj_text,
    on_draw=vykresli,
    on_mouse_press=klik,
)

obrazek2 = pyglet.image.load('had2.png')

def zmen(t):
    had.image = obrazek2
    pyglet.clock.schedule_once(zmen_zpatky, 0.2)

def zmen_zpatky(t):
    had.image = obrazek
    pyglet.clock.schedule_once(zmen, 0.2)

pyglet.clock.schedule_once(zmen, 0.2)

pyglet.app.run()
```

Se vstupem z klávesnice a myši, časováním a vykreslováním
Spritu si vystačíš u leckteré hry nebo grafické aplikace.

Až budeš nějakou hru dělat, zkus udržovat
stav aplikace v seznamech a <var>n</var>-ticích (případně
slovnících a třídách, které se naučíme později).
Jedna funkce by měla umět takový stav vykreslit a
jiné s ním pak budou manipulovat.
Tyhle dvě sady funkcí můžeš mít i v jiných souborech,
aby se nezapletly dohromady.

Zajímá-li tě toto téma, zkus si zahrát přiloženou hru
[Pong](static/pong.py),
která ukazuje některé další
možnosti Pygletu: psaní textu, kreslení obdélníků
a obsluhu jednotlivých kláves (např. šipek).
Na první pohled může její kód vypadat složitě,
ale zkus si k němu sednout a s pomocí komentářů ho pochopit.
Kdyby komentáře nestačily, jsou k Pongu připravené
i [podrobné materiály]({{ lesson_url('projects/pong') }}).

To, co jsme tu probral{{gnd('i', 'y', both='i')}} a pár věcí navíc,
je shrnuto v [taháku na Pyglet](https://pyvec.github.io/cheatsheets/pyglet/pyglet-basics-cs.pdf),
který si můžeš stáhnout a vytisknout.

A chceš-li se do Pygletu ponořit hlouběji,
existuje pro něj [dokumentace](http://pyglet.readthedocs.org/en/latest/index.html).
Nebude-li ti v ní něco jasné, zeptej se!