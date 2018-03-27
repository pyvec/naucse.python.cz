# Logika hry

Už umíš vykreslit „fotku“ hada.
Hadí videohra ale nebude jen statický obrázek.
Had se bude hýbat!


<!--
# Ukládání revizí

XXX - Nestíhám dopsat, omlouvám se
-->

# Rozhýbejme hada

Tak, ale teď už k samotné hře!

Tvůj program teď, doufám, vypadá nějak takhle:

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
        source = 'tail'     # (Tady případně je nějaké
        dest = 'head'       #  složitější vybírání políčka)
        snake_tiles[source + '-' + dest].blit(
            x * TILE_SIZE, y * TILE_SIZE, width=TILE_SIZE, height=TILE_SIZE)
    for x, y in food:
        red_image.blit(
            x * TILE_SIZE, y * TILE_SIZE, width=TILE_SIZE, height=TILE_SIZE)

pyglet.app.run()
```

Zkus těsně nad řádek `pyglet.app.run` doplnit funkci,
která se bude volat každou šestinu vteřiny,
a přidá hadovi políčko navíc:

```
def move(dt):
    x, y = snake[-1]
    new_head = x+1, y
    snake.append(new_head)

pyglet.clock.schedule_interval(move, 1/6)
```

Funguje?
Tak do téhle funkce ještě přidej `del snake[0]`, aby had nerostl donekonečna.
Víš co tenhle příkaz dělá? Jestli ne, koukni znovu na poznámky k seznamům!

A had se hýbe… Jen ho ještě nejde ovládat.


## Ven se stavem

Než uděláme interaktivního hada, zkusíme trošku uklidit.
Program se nám rozrůstá, a za chvíli bude složité se v něm vyznat.
Můžeme tomu trochu pomoct tím, že ho rozdělíme do dvou souborů:
jeden pro *logiku hry* a druhý na *vykreslování* (a později ovládání)
přes Pyglet.

Udělej si nový soubor pojmenovaný `had.py`.
V něm budeme mít *třídu*, která spravuje (a obsahuje) celý stav hry.

Všechno, co je potřeba o hře vědět – v našem případně zatím souřadnice hada
a jídla – bude tato třída obsahovat jako *atributy*.

Třída bude obsahovat dvě *metody* – funkce, které se dají zavolat na objekty
této třídy.
Speciální metoda `__init__` (která se automaticky volá při vytvoření objektu
této třídy) bude tyto atributy nastavovat.
Metoda `move`, kterou budeme volat při každém „tahu“ hry, je pak bude
měnit.

Pro funkčnost, kterou zatím náš had umí, bude `had.py` vypadat takto:

```python
class State:
    def __init__(self):
        self.food = [(2, 0), (5, 1), (1, 4)]
        self.snake = [(0, 0), (1, 0)]  # (kratší než v kódu na vykreslování)

    def move(self):
        old_x, old_y = self.snake[-1]
        new_x = old_x + 1
        new_y = old_y
        new_head = new_x, new_y
        self.snake.append(new_head)
        del self.snake[0]
```

> [note]
> Pužij prosím pro třídu jméno `State` a i atributy pojmenuj podle
> materiálů – `snake`, `food`, a později i další, které budeme přidávat.
> Bude se ti to hodit.

Všimni si, že metody berou argument `self`.
To označuje konkrétní objekt, stav hry se kterým metoda pracuje nebo
který mění.
Ke všem atributúm přistupují pomocí tečky –
<code>self.<var>jméno_atributu</var></code>.

Tak, máme třídu se stavem.
No jo, ale jak ji teď použít?
Je v jiném souboru než naše hra (`ui.py`).

Pythonní soubory (ty s příponou `.py`) jsou zároveň *moduly*, které se dají
importovat.
Na začátku `ui.py` tak můžeš napsat:

```python
from had import State
```

… a třída se stavem bude k dispozici!

Pak potřebuješ ještě několik změn:

* Nastavování seznamů `snake` a `food` zruš; místo nich nastav jedinou
  proměnnou `state` na nový stav:

  ```python
  state = State()
  ```

* Místo `snake` a `food` ve funkci `on_draw` použij `state.snake`
  a `state.food` – atributy našeho stavu.

  Všimni si že tady nepoužíváme `self` – tohle jméno je pro *metody* v rámci
  třídy. Jinde musíme pojmenovat konkrétní objekt, se kterým pracujeme.

* Funkci `move` přepiš tak, aby jen volala metodu `state.move`:

  ```python
  def move(dt):
      state.move()
  ```

  Všimni si že ani tady nepoužíváme `self`.
  Ten se doplní automaticky – jde o objekt, jehož metodu voláme.

Povedlo se? Funguje to jako předtím?
Pro kontrolu můžeš svůj program porovnat s mým (ale nejde o jediné správné
řešení):

{% filter solution %}
```python
from pathlib import Path

import pyglet

from had import State

TILE_SIZE = 64
TILES_DIRECTORY = Path('snake-tiles')

red_image = pyglet.image.load('apple.png')
snake_tiles = {}
for path in TILES_DIRECTORY.glob('*.png'):
    snake_tiles[path.stem] = pyglet.image.load(path)

window = pyglet.window.Window()

state = State()

@window.event
def on_draw():
    window.clear()
    pyglet.gl.glEnable(pyglet.gl.GL_BLEND)
    pyglet.gl.glBlendFunc(pyglet.gl.GL_SRC_ALPHA, pyglet.gl.GL_ONE_MINUS_SRC_ALPHA)
    for x, y in state.snake:
        source = 'tail'     # (Tady případně je nějaké
        dest = 'head'       #  složitější vybírání políčka)
        snake_tiles[source + '-' + dest].blit(
            x * TILE_SIZE, y * TILE_SIZE, width=TILE_SIZE, height=TILE_SIZE)
    for x, y in state.food:
        red_image.blit(
            x * TILE_SIZE, y * TILE_SIZE, width=TILE_SIZE, height=TILE_SIZE)

def move(dt):
    state.move()

pyglet.clock.schedule_interval(move, 1/6)

pyglet.app.run()
```
{% endfilter %}


## Ovládání

Nyní k onomu slíbenému ovládání. Respektive nejdřív k změnám směru.

Had ze hry se plazí stále stejným směrem, dokud hráč nezmáckne klávesu.
Had z naší ukázky se plazí doprava; dokážeš zařídit, aby se místo toho
plazil nahoru?

{% filter solution %}
Ve funkci `move` je potřeba jinak nastavit proměnné `new_x` a `new_y`:
```python
        new_x = old_x
        new_y = old_y + 1
```
{% endfilter %}

A co dolů?

{% filter solution %}
```python
        new_x = old_x
        new_y = old_y - 1
```
{% endfilter %}

Aby si had „pamatoval“ kam se zrovna plazí, je potřeba mít směr součástí stavu
hry.
Uložme ho tedy do atrubutu jménem `snake_direction`.

Co tam ale přesně uložit?
Jak reprezentovat směr v Pythonu – pomocít čísel, <var>n</var>-tic a tak?

Asi nejpříhodnější řešení je uložit si o kolik políček se had posune,
a to zvlášť v <var>x</var>-ovém a zvlášť v <var>y</var>-ovém směru.
Čili jako dvojici:

* `(1, 0)` = doprava (o jedno políčko v kladném <var>x</var>-ovém směru)
* `(-1, 0)` = doleva (o jedno políčko v záporném <var>x</var>-ovém směru)
* `(0, 1)` = nahoru (+<var>y</var>)
* `(0, -1)` = dolů (-<var>y</var>)

Nový atribut přidej do metody `__init__` ve stavu:

```python
        self.snake_direction = 0, 1
```

A v metodě `move` změň nastavování `new_x` a `new_y` podle nového atributu:

```python
        dir_x, dir_y = self.snake_direction
        new_x = old_x + dir_x
        new_y = old_y + dir_y
```

Směr hada teď můžeš měnit změnou `snake_direction` v `__init__`.
Funguje to? (Jestli ne, oprav to – a jestli to nejde, zavolej někoho na pomoc!)

Nyní zbývá jen atribut `snake_direction` měnit, když uživatel něco stiskne na
klávesnici.
To už je doména Pygletu.
Opusť na chvíli abstraktní stav v `had.py` a koukni na hru v `ui.py`.
Sem je potřeba přidat funkci, která reaguje na stisk klávesy.

Aby Pyglet tuhle funkci našel a uměl zavolat, musí se jmenovat `on_key_press`,
musí mít dekorátor `@window.event`, a musí brát dva argumenty:
číslo klávesy, která byla zmáčknutá, a informace o modifikátorech
(Shift, Ctrl, a tak podobně):

```python
@window.event
def on_key_press(symbol, mod):
    ...
```

Druhý argument nepoužijeme.
Podle prvního ale nastav aktuální směr hada.
Čísla kláves jsou definována v modulu `pyglet.window.key` jako konstanty se
jmény `LEFT`, `ENTER`, `Q` či `AMPERSAND` .
My použijeme šipky:

```python
@window.event
def on_key_press(symbol, mod):
    if symbol == pyglet.window.key.LEFT:
        state.snake_direction = -1, 0
    if symbol == pyglet.window.key.RIGHT:
        state.snake_direction = 1, 0
    if symbol == pyglet.window.key.DOWN:
        state.snake_direction = 0, -1
    if symbol == pyglet.window.key.UP:
        state.snake_direction = 0, 1
```

Tuhle funkci je potřeba dát někam za nastavení `window` (aby byl k dispozici
`window.event`) a před `pyglet.app.run()` (protože nastavovat ovládání až
potom, co hra proběhne, je zbytečné).
Nejlepší je ji dát vedle jiné funkce s dekorátorem `@window.event`,
aby byly pěkně pohromadě.

Funguje to?
Můžeš ovládat směr hada?
To je skvělé!
Určitě ale při zkoušení narazíš na pár věcí, které je potřeba dodělat:

* Had by neměl mít možnost vylézt ven z okýnka.
* Had by měl jíst jídlo a růst.
* Hra by měla skončit, když had narazí sám do sebe.

Pojďme je vyřešit, jednu po druhé.


## Zatím dobrý, teď ale narazíme

„Hadí“ hry jako ta naše mají dvě varianty: buď je kolem hřiště „zeď“
a hráč při nárazu do okraje prohraje, nebo je hřiště „nekonečné“ – had okrajem
proleze a objeví se na druhé straně.

My nakonec naprogramujeme druhou variantu, která je zajímavější.
Začneme ale s tou první, která je jednodušší.

Vrať se k souboru se stavem – `had.py`.
Budeme pracovat na chování, na logice hry; ne na vykreslování a ovládání.

Abys zjistil{{a}}, jestli had „vylezl“ z levého okraje okna ven,
je potřeba zkontrolovat, jestli <var>x</var>-ová souřadnice hlavy
je menší než 0.
To je dobré udělat hned poté, co nové souřadnice hlavy získáš – konkrétně
hned před řádkem `new_head = new_x, new_y` v metodě `move`.

A co při takovém nárazu udělat?
Nejjednodušší bude hru ukončit.
Na to má Python funkci `exit()`, která funguje podobně jako když v programu
nastane chyba.
Jen místo chybového výpisu ukáže daný text.

Ukončení programu není příliš příjemný způsob, jak říct hráčovi že prohrál.
Za chvíli ale tuhle část předěláme, tak prozatím tenhle jednoduchý způsob postačí.

```python
    def move(self):
        old_x, old_y = self.snake[-1]
        dir_x, dir_y = self.snake_direction
        new_x = old_x + dir_x
        new_y = old_y + dir_y

        # Nový kód – kontrola vylezení z hrací plochy
        if new_x < 0:
            exit('GAME OVER')

        new_head = new_x, new_y
        self.snake.append(new_head)
        del self.snake[0]
```

Věřím, že zvládneš udělat stejnou kontrolu pro vylezení ze spodního okraje.

Jak ale ošetřit ty zbylé okraje – pravý a horní?
Na to je potřeba znát velikost okýnka.
A tu zná Pyglet; třída se stavem k okýnku nemá přístup!

Na velikosti herní plochy závisí chování hry.
Tahle informace tedy bude tedy muset být součást stavu.
Pro začátek nějakou velikost – třeba 10×10 – nastav v `__init__`:

```python
        self.width = 10
        self.height = 10
```

A pak zařiď, aby po nárazu na neviditelnou stěnu kolem hřiště velkého
10×10 políček hra skončila.
Vyzkoušej všechny varianty – severní, jižní, východní i západní zeď.
(Had je virtuální, nemusíš se bát že mu z toho vyroste boule.)

{% filter solution %}
```python
    def move(self):
        old_x, old_y = self.snake[-1]
        dir_x, dir_y = self.snake_direction
        new_x = old_x + dir_x
        new_y = old_y + dir_y

        # Kontrola vylezení z hrací plochy
        if new_x < 0:
            exit('GAME OVER')
        if new_y < 0:
            exit('GAME OVER')
        if new_x >= self.width:
            exit('GAME OVER')
        if new_y >= self.height:
            exit('GAME OVER')

        new_head = new_x, new_y
        self.snake.append(new_head)
        del self.snake[0]
```
{% endfilter %}

A pak nastav *opravdovou* velikost herní plochy. Jak?
V souboru se hrou (`ui.py`), hned po tom co vytvoříš stav (`state`)
a okýnko (`window`) velikost nastav.
Použij celočíselné dělení (se zbytkem), aby velikost byla v celých číslech:

```python
state.width = window.width // TILE_SIZE
state.height = window.height // TILE_SIZE
```

## Nekonečná magická klec

Teď místo konce hry při naražení necháme hada „projít“ a objevit se na druhé
straně.

Nemělo by to být tak složité udělat – stačí místo `exit()` vždy správně
nastavit příslušnou hodnotu.
Je ale potřeba si dát pozor kde použít `new_x` a kde `new_y`, kde `width` a kde
`height`, a kde přičíst nebo odečíst jedničku, aby při číslování od nuly
všechno sedělo.
Zkus to!


> [note]
> Jestli už vykresluješ hada místo housenky, možná teď narazíš na problém
> s vybíráním správných dílků – okraj herní plochy hada vizuálně rozdělí
> na dva menší.
> Zatím to ignoruj, ale ve volné chvilce se pokus problém opravit.
> Doporučuji se vrátit k „abstraktní“ funkci, která jen vypisuje souřadnice
> a směry:
>
> ```
> 1 2 tail right
> 2 2 left right
> 3 2 left top
> 3 3 bottom top
> 3 4 bottom top
> 3 5 bottom right
> 4 5 left head
> ```
> Jdeš-li podle návodu, tuhle funkci máš uloženou v souboru `smery.py`
> Oprav nejdřív tu, a řešení „transplantuj“ do hry.

{% filter solution %}
```python
        # Kontrola vylezení z hrací plochy
        if new_x < 0:
            new_x = self.width - 1
        if new_y < 0:
            new_y = self.height - 1
        if new_x >= self.width:
            new_x = 0
        if new_y >= self.height:
            new_y = 0
```
{% endfilter %}

Jde to jednodušeji? Jde!
Matematikové vymysleli operaci, která se jmenuje *zbytek po dělení*.
Ta dělá přesně to, co potřebujeme – zbytek po dělení nové souřadnice velikostí
hřiště dá souřadnici, která leží v hřišti.
Když byla předchozí souřadnice o jedna větší než maximum,
zbytek po dělení bude nula; když byla -1, dostaneme maximum.

Celý kód pro kontrolu a ošetření vylézání z hrací plochy tak jde
nahradit tímhle:

```python
        new_x = new_x % self.width
        new_y = new_y % self.height
```

Podobné matematické „zkratky“ umí programátorům často usnadnit život – ale
přijít na ně nebývá jednoduché.
Ale nevěš hlavu: neláká-li tě studovat informatiku na škole, věz, že to jde
i bez „zkratek“. Jen občas trochu krkoloměji.

> [note]
> Ale jestli tě matematika baví, je tu poznámka pro tebe!
>
> To, že existuje přesně operace kterou potřebujeme, není až tak úplně náhoda.
> Ona matematická jednoduchost je spíš  *důvod*, proč se hrací plocha
> u spousty starých her chová právě takhle.
> Odborně se tomu „takhle“ říká
> [toroidální topologie](https://en.wikipedia.org/wiki/Torus#Topology).
> 
> Zkušení matematici si teď možná stěžují na nutnost definovat zbytek po
> dělení záporných čísel. Proto dodám, že ho Python schválně
> [definuje](https://docs.python.org/3/reference/expressions.html#binary-arithmetic-operations)
> *vhodně* pro tento účel; `a % b` má vždy stejné znaménko jako `b`.


## Krmení

Tak. Had je v pasti, už nemůže vylézt.
Co dál?

Teď se musíme o hada postarat: pravidelně ho krmit.
Ale ještě předtím je potřeba ho naučit, jak se vůbec jí – na naši potravu
ještě není zvyklý.
Když to zvládneme, poroste jako z vody!

Konkrétně musíme hlavně zajistit, aby když se had připlazí na políčko
s jídlem, tak jídlo zmizelo.
K tomu se dá použít operátor `in`, který zjišťuje jestli něco (třeba
souřadnice) je v nějakém seznamu (třeba seznamu souřadnic jídla),
a metoda `remove`, která ze seznamu odstraní daný prvek (podle hodnoty prvku,
na rozdíl od `del`, který maže podle pozice).

Nebudu napínat, kód je následující.
Rozumíš mu?
Víš, kam je ho potřeba dát?

```python
        if new_head in self.food:
            self.food.remove(new_head)
```

{% filter solution %}
Do metody `move`, kamkoli za řádek který nastavuje `new_head`.
{% endfilter %}

Vyzkoušej, jestli to funguje. Had by měl jíst jídlo.

Ještě ale zbývá zařídit, aby po každém soustu trochu povyrostl.
Ale jak? Kterým směrem má růst?

Tady je dobré se podívat na existující kód a uvědomit si, co dělá.

Náš had se plazí tak, že napřed vepředu povyroste (pomocí `append`)
a potom se vzadu zmenší (pomocí `del self.snake[0]`).

Aby tedy po snězení jídla vyrostl, stačí *přeskočit* ono zmenšování!
Ono *přeskočit* znamená podmínit, pomocí `if`.
Logika jezení a zmenšování hada tedy bude:

* Když had sní jídlo, jídlo zmizí. Had se nezmenší.
* Jinak (tedy když had *nesní* jídlo) se had zmenší (a tudíž neroste).

Neboli přeloženo do Pythonu:

```python
        if new_head in self.food:
            self.food.remove(new_head)
        else:
            del self.snake[0]
```

Pro ty, co se začínají ztrácet, dám k dispozici celou metodu `move`.
Běda ale těm, kdo opisují kód bez toho aby mu rozuměli!

{% filter solution %}
```python
    def move(self):
        old_x, old_y = self.snake[-1]
        dir_x, dir_y = self.snake_direction
        new_x = old_x + dir_x
        new_y = old_y + dir_y

        # Kontrola vylezení z hrací plochy
        new_x = new_x % self.width
        new_y = new_y % self.height

        new_head = new_x, new_y
        self.snake.append(new_head)
        if new_head in self.food:
            self.food.remove(new_head)
        else:
            del self.snake[0]
```
{% endfilter %}


### Nové jídlo

Když už had umí jíst, je potřeba mu zajistit pravidelný přísun jídla.
Nejlépe tak, že se každé snězené jídlo nahradí novým.

Přidej do třídy `State` následující novou metodu, která umí přidat jídlo:

```python
    def add_food(self):
        x = 0
        y = 0
        position = x, y
        self.food.append(position)
```

Pak tuhle metodu zavolej – najdi v programu kód, který se provádí když
je potřeba přidat nové jídlo, a přidej tam následující řádek:

```python
            self.add_food()
```

Tahle metoda přidává jídlo na pozici (0, 0), tedy stále do stejného rohu.
Bylo by ale fajn, kdyby se nové jídlo objevilo vždycky jinde,
na náhodném místě.
Na to můžeme použít funkci `random.randrange`, která vrací náhodná celá čísla.
Vyzkoušej si ji (z jiného souboru, třeba ``experiment.py`):

```python
import random

print('Na kostce padlo:', random.randrange(6))
```

Čím se liší `random.randrange` od klasické hrací kostky?
Uměl{{a}} bys program upravit tak, aby padalo 1 až 6?

Je tahle změna užitečná pro naši hru? Jaký rozsah čísel potřebujeme pro hadí jídlo?

Až na to přijdeš, zkus přidat náhodu do programu: jídlo by se mělo objevit
na *úplně náhjodném* políčku na herní ploše.
Nezapomeň na `import random` – to patří na úplný začátek souboru.
Další změny už dělej v metodě `add_food`.

{% filter solution %}
```python
    def add_food(self):
        x = random.randrange(self.width)
        y = random.randrange(self.height)
        position = x, y
        self.food.append(position)
```
{% endfilter %}

Až to budeš testovat, asi zjistíš, že *úplně náhodné* políčko není ideální.
Občas se  totiž jídlo objeví na políčku s hadem, nebo dokonce na jiném jídle.
Je proto dobré tuhle situaci zkontrolovat, a když volba padne na plné políčko,
jídlo nepřidávat:

```python
        if (position not in self.snake) and (position not in self.food):
            self.food.append(position)
```

Když ale zkusíš *tohle*, zjistíš, že občas se nové jídlo vůbec nepřidá.
To taky není vhodná varianta – had by tak měl hlad.
Co s tím?

Překvapivě dobré (i když ne *úplně* ideální) řešení je zkusit políčko vybrat
několikrát.
Když padne prázdné políčko, šup tam s jídlem; když padne plné, tak to
prostě zkusit znovu.

Je ale potřeba počet pokusů omezit, aby v situaci, kdy je pole *úplně* plné,
počítač nevybíral donekonečna.
Řekněme že když se na 100 pokusů nepodaří prázdné políčko vybrat,
vzdáme to.

Metoda `add_food` po všech úpravách bude vypadat takhle:

```python
    def add_food(self):
        for try_number in range(100):
            x = random.randrange(self.width)
            y = random.randrange(self.height)
            position = x, y
            if (position not in self.snake) and (position not in self.food):
                self.food.append(position)
                # Ukončení funkce ("vyskočí" i z cyklu for)
                return
```

Jestli ti to funguje, ještě zařiď, aby na začátku hry bylo jídlo na náhodných
pozicích.

{% filter solution %}
V metodě `__init__` se dá místo nastavení `self.food` na seznam s pozicemi
jídla napsat:
```python
        self.food = []
        self.add_food()
        self.add_food()
```
Pak budou na začátku hry na hada čekat dvě náhodné jídla.
{% endfilter %}


## Konec

Had teď může narůst do obrovských rozměrů – a hru stále nelze prohrát.
Zařídíme tedy, aby hra skončila, když had narazí sám do sebe.

Na rozdíl od `0/1`, které jsme použili výše, buďme trochu opatrnější.
Není dobré ukončit celý program; to by se hráčům moc nelíbilo.
Ostatně, zkus si, jak to působí – následující kód dej na správné místo
a zkus, jak se hra hraje, když skončí hned po nárazu:

```python
        # Kontrola, jestli had narazil
        if new_head in self.snake:
            exit('GAME OVER')
```

{% filter solution %}
Kód patří do metody `move`, hned za nastavení proměnné `new_head`.
{% endfilter %}

Lepší je hru „zapauzovat“ – ukázat hráči situaci, do které nešťastného hada
dostal, aby se z ní mohl pro příště poučit.

Aby to bylo možné, dáme do stavu hry další atribut: `snake_alive`.
Ten bude nastavený na `True`, dokud bude had žít.
Když had narazí, nastaví se na `False`, a od té doby se už nebude pohybovat.
Je dobré i graficky ukázat, že hadovi není dobře – hráč pak spíš bude
zpytovat svědomí.

Zkus zapřemýšlet, kam v kódu (a i do kterých souborů) patří následující
kousky kódu, které prohru implementují:

```python
        # Prvotní nastavení atributu
        self.snake_alive = True
```

```python
        # Kontrola, jestli had narazil
        if new_head in self.snake:
            self.snake_alive = False
```

```python
        # Zabránění pohybu
        if not self.snake_alive:
            return
```

```python
        # Grafická indikace
        if dest == 'head' and not state.snake_alive:
            dest = 'dead'
```

{% filter solution %}
* „Prvotní nastavení atributu“ do metody `__init__`.
* „Kontrola, jestli had narazil“ do `move` místo původní kontroly,
  kdy se hra ukončila pomocí `exit()`.
* „Zabránění pohybu“ na úplný začátek metody `move` (příkaz `return`
  okamžitě ukončí provádění metody).
* „Grafická indikace“ do `ui.py`, za sekci pro vybírání obrázku pro kousek
  hada.

{% endfilter %}


## Vylepšení ovládání

Poslední úprava kódu!

Možná si všimneš – zvlášť jestli jsi už nějakou verzi hada hrál{{a}},
že ovládání tvé nové hry je trošku frustrující.
A možná není úplně jednoduché přijít na to, proč.

Můžou za to (hlavně) dva důvody.

První problém: když zmáčkneš dvě šipky rychle za sebou, v dalším „tahu“
hada se projeví jen ta druhá.
Z pohledu programu je to chování (snad) jasné – po stisknutí šipky se uloží
její směr, a při „tahu“ hada se použije poslední uložený směr.
S tímhle chováním je ale složité hada rychle otáčet: hráč se musí „trefovat“
do tahů hada.
Lepší by bylo, kdyby se ukládaly *všechny* stisknuté klávesy, a had by
v každém tahu reagoval maximálně jednu – další by si „schoval“ na další tahy.

Takovou „frontu“ stisků kláves lze uchovávat v seznamu.
Přidej si na to do stavu hry seznam (v metodě `__init__`):

```python
        self.queued_directions = []
```

Tuhle frontu plň v `ui.py` po každém stisku klávesy, metodou `append`.
Je potřeba změnit většinu funkce `on_key_press`:

```python
@window.event
def on_key_press(symbol, mod):
    if symbol == pyglet.window.key.LEFT:
        new_direction = -1, 0
    if symbol == pyglet.window.key.RIGHT:
        new_direction = 1, 0
    if symbol == pyglet.window.key.DOWN:
        new_direction = 0, -1
    if symbol == pyglet.window.key.UP:
        new_direction = 0, 1
    state.queued_directions.append(new_direction)
```

A zpátky k logice, v `had.py` v metodě `move` místo
`dir_x, dir_y = self.snake_direction` z fronty vyber první nepoužitý prvek
(a nezapomeň ho z fronty smazat, ať se dostane i na další!):

```python
        if self.queued_directions:
            new_direction = self.queued_directions[0]
            del self.queued_directions[0]
            self.snake_direction = new_direction
```

Zkontroluj, že to funguje.

Druhý problém: když se had plazí doleva a hráč zmáčkne šipku doprava,
had se otočí a hlavou si narazí do krku.
Z pohledu programu to dává smysl: políčko napravo od hlavy je plné,
hra tedy končí.
Z pohledu hry (a biologie už vůbec!) ale narážení do krku moc smyslu nedává.
Lepší by bylo obrácení směru úplně ignorovat.

A jak poznat opačný směr?
Když se had plazí doprava – (1, 0) – tak je opačný směr doleva – (-1, 0).
Když se plazí dolů – (0, -1) – tak naopak je nahoru – (0, 1).
Obecně, k (<var>x</var>, <var>y</var>) je opačný směr
(-<var>x</var>, -<var>y</var>).

Zatím ale pracujeme s celými <var>n</var>-ticemi, je potřeba obě
na <var>x</var> a <var>y</var> „rozbalit“.
Kód tedy bude vypadat takto:

```python
            old_x, old_y = self.snake_direction
            new_x, new_y = new_direction
            if (old_x, old_y) != (-new_x, -new_y):
                self.snake_direction = new_direction
```


## A to je vše?

Gratuluji, máš funkční a hratelnou hru!
Doufám že jsi na sebe hrd{{gnd('ý', 'á')}}!

Dej si něco sladkého, zasloužíš si to.

---

Tady je moje řešení.
To se touhle dobou od toho tvého může dost lišit – to je úplně normální.
(A nedívej se sem dokud hada nenaprogramuješ {{gnd('sám', 'sama')}},
Chybami (a neustálým zkoušením) se člověk učí – a programátor zvlášť.
Čtením už vyřešeného se učí hůř.)


{% filter solution %}

`had.py`:

```python
import random

class State:
    def __init__(self):
        self.food = []
        self.add_food()
        self.add_food()
        self.snake = [(0, 0), (1, 0)]
        self.snake_direction = 0, 1
        self.width = 10
        self.height = 10
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

        new_x = new_x % self.width
        new_y = new_y % self.height

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
```

`ui.py`:

```python
from pathlib import Path

import pyglet

from had import State

TILE_SIZE = 64
TILES_DIRECTORY = Path('snake-tiles')

red_image = pyglet.image.load('apple.png')
snake_tiles = {}
for path in TILES_DIRECTORY.glob('*.png'):
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
    for x, y in state.snake:
        source = 'tail'     # (Tady případně je nějaké
        dest = 'head'       #  složitější vybírání políčka)
        if dest == 'head' and not state.snake_alive:
            dest = 'dead'
        snake_tiles[source + '-' + dest].blit(
            x * TILE_SIZE, y * TILE_SIZE, width=TILE_SIZE, height=TILE_SIZE)
    for x, y in state.food:
        red_image.blit(
            x * TILE_SIZE, y * TILE_SIZE, width=TILE_SIZE, height=TILE_SIZE)


@window.event
def on_key_press(symbol, mod):
    if symbol == pyglet.window.key.LEFT:
        new_direction = -1, 0
    if symbol == pyglet.window.key.RIGHT:
        new_direction = 1, 0
    if symbol == pyglet.window.key.DOWN:
        new_direction = 0, -1
    if symbol == pyglet.window.key.UP:
        new_direction = 0, 1
    state.queued_directions.append(new_direction)


def move(dt):
    state.move()


pyglet.clock.schedule_interval(move, 1/6)

pyglet.app.run()
```
{% endfilter %}


Najdeš ještě nějaké další vylepšení, které by se dalo udělat?

Zkus třeba následující rozšíření:

* Každých 30 vteřin hry přibude samo od sebe nové jídlo,
  takže jich pak bude na hrací ploše víc.

* Hra se bude postupně zrychlovat.<br>
  *(Na to je nejlepší předělat funkci `move` v `ui.py`, aby *sama*
  naplánovala, kdy se má příště zavolat. Volání `schedule_interval` tak už
  nebude potřeba.)*

* Hadi budou dva; druhý se ovládá klávesami
  <kbd>W</kbd> <kbd>A</kbd> <kbd>S</kbd> <kbd>D</kbd>.<br>
  *(Na to je nejlepší udělat novou třídu, `Snake`, a všechen stav hada
  přesunout ze `State` do ní. Ve `State` pak měj seznam hadů.
  Téhle změně je potřeba přizpůsobit celý zytek programu.)*
