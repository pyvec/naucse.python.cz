# Logika hry

Už umíš vykreslit hada ze seznamu souřadnic.
Hadí videohra ale nebude jen „fotka“.
Seznam se bude měnit a had se bude hýbat!


<!--
# Ukládání revizí

XXX - Nestíhám dopsat, omlouvám se
-->

# Rozhýbejme hada

Tvůj program teď, doufám, vypadá nějak takhle:

```python
import pyglet

TILE_SIZE = 64

class GameState:
    def initialize(self):
        self.snake = [(1, 2), (2, 2), (3, 2), (3, 3), (3, 4), (3, 5), (4, 5)]
        self.food = [(2, 0), (5, 1), (1, 4)]

    def draw(self):
        for x, y in self.snake:
            before = 'end'     # (Tady případně je nějaké
            after = 'end'      #  složitější vybírání políčka)
            key = before + '-' + after
            snake_tiles[key].blit(x * TILE_SIZE, y * TILE_SIZE,
                                  width=TILE_SIZE, height=TILE_SIZE)
        for x, y in self.food:
            apple_image.blit(x * TILE_SIZE, y * TILE_SIZE,
                             width=TILE_SIZE, height=TILE_SIZE)

state = GameState()
state.initialize()

apple_image = pyglet.image.load('apple.png')
green_image = pyglet.image.load('green.png')
snake_tiles = {}
for start in ['bottom', 'end', 'left', 'right', 'top']:
    for end in ['bottom', 'end', 'left', 'right', 'top', 'dead', 'tongue']:
        key = start + '-' + end
        image = pyglet.image.load('snake-tiles/' + key + '.png')
        snake_tiles[key] = image

window = pyglet.window.Window()

@window.event
def on_draw():
    window.clear()
    # Lepší vykreslování (pro nás zatím kouzelné zaříkadlo)
    pyglet.gl.glEnable(pyglet.gl.GL_BLEND)
    pyglet.gl.glBlendFunc(pyglet.gl.GL_SRC_ALPHA, pyglet.gl.GL_ONE_MINUS_SRC_ALPHA)

    state.draw()

pyglet.app.run()
```

Zkus teď doplnit do třídy `GameState` metodu, která
přidá hadovi políčko navíc:

``` python
    def move(self, dt):
        x, y = snake[-1]
        new_x = x + 1
        new_y = y
        new_head = new_x, new_y
        snake.append(new_head)
```

A těsně nad řádek `pyglet.app.run` říct Pygletu, aby tuto funkci volal
každou šestinu vteřiny:

```python
pyglet.clock.schedule_interval(state.move, 1/6)
```

Funguje?
Tak do té metody ještě přidej `del snake[0]`, aby had nerostl donekonečna.
Víš co tenhle příkaz dělá? Jestli ne, koukni znovu na poznámky k seznamům!

Zvládneš funkci upravit tak, aby se had plazil nahoru? Nebo dolů?

Jestli ano, gratuluji!
Zbývá směr hada ovládat šipkami na klávesnici, a většina hry bude hotová!

Pro kontrolu přikládám svoje řešení:

{% filter solution %}
V metodě `move` je potřeba jinak nastavit proměnné `new_x` a `new_y`:

Pro pohyb nahoru:

```python
        new_x = old_x
        new_y = old_y + 1
```

A dolů:

```python
        new_x = old_x
        new_y = old_y - 1
```
{% endfilter %}


## Ovládání

Nyní k onomu slíbenému ovládání. Respektive nejdřív k změnám směru.

Had ze hry se plazí stále stejným směrem, dokud hráč nezmáčkne klávesu
a směr nezmění.

Aby si had „pamatoval“ kam se zrovna plazí, je potřeba mít směr jako součást
stavu hry.
Uložme ho tedy do atrubutu jménem `snake_direction`.

Co tam ale přesně uložit?
Jak reprezentovat směr v Pythonu – pomocí čísel, <var>n</var>-tic a tak?

{{ figure(
    img=static('coord-vectors.svg'),
    alt="Mřížka s X a Y souřadnicemi",
) }}

Asi nejpříhodnější řešení je uložit si o kolik políček se had má posunout,
a to zvlášť v <var>x</var>-ovém a zvlášť v <var>y</var>-ovém směru.
Čili jako dvojici:

* (`1, 0`) = doprava (o jedno políčko v kladném <var>x</var>-ovém směru;
   v <var>y</var>-ovém neposouvat)
* (`-1, 0`) = doleva (o jedno políčko v záporném <var>x</var>-ovém směru)
* (`0, 1`) = nahoru (+<var>y</var>, ale v <var>x</var> neposouvat)
* (`0, -1`) = dolů (-<var>y</var>)

Nový atribut přidej do metody `initialize`:

```python
        self.snake_direction = 0, 1
```

A v metodě `move` změň nastavování `new_x` a `new_y` podle nového atributu:

```python
        dir_x, dir_y = self.snake_direction
        new_x = old_x + dir_x
        new_y = old_y + dir_y
```

Směr hada teď můžeš měnit změnou `snake_direction` v `initialize`.
Funguje to? (Jestli ne, oprav to – a jestli to nejde, zavolej někoho na pomoc!)

Nyní zbývá atribut `snake_direction` měnit, když uživatel něco stiskne na
klávesnici.
To už je doména Pygletu.

Je potřeba přidat funkci, která reaguje na stisk klávesy.
Aby Pyglet tuhle funkci našel a uměl zavolat, musí se jmenovat `on_key_press`,
musí mít dekorátor `@window.event`, a musí brát dva parametry:
číslo klávesy, která byla zmáčknutá a informace o modifikátorech
jako <kbd>Shift</kbd> nebo <kbd>Ctrl</kbd>:

```python
@window.event
def on_key_press(key_code, modifier):
    ...
```

Důležitý je ten první parametr. Podle něho nastavíš aktuální směr hada.
Čísla kláves jsou definována v modulu [`pyglet.window.key`][key-constants]
jako konstanty se jmény `LEFT`, `ENTER`, `Q` či `AMPERSAND` .
My použijeme šipky – `LEFT`, `RIGHT`, `UP ` a `DOWN`:

```python
@window.event
def on_key_press(key_code, modifier):
    if key_code == pyglet.window.key.LEFT:
        state.snake_direction = -1, 0
    if key_code == pyglet.window.key.RIGHT:
        state.snake_direction = 1, 0
    if key_code == pyglet.window.key.DOWN:
        state.snake_direction = 0, -1
    if key_code == pyglet.window.key.UP:
        state.snake_direction = 0, 1
```

Druhý parametr nebude v naší hře potřeba, ale v hlavičce funkce musí být.

[key-constants]: https://pyglet.readthedocs.io/en/pyglet-1.3-maintenance/modules/window_key.html#key-constants

Funkci `on_key_press je potřeba dát někam za nastavení `window` (aby byl
k dispozici `window.event`) a před `pyglet.app.run()` (protože nastavovat
ovládání až potom, co hra proběhne, je zbytečné).
Nejlepší je ji dát vedle jiné funkce s dekorátorem `@window.event`,
aby byly pěkně pohromadě.

Funguje to?
Můžeš ovládat směr hada?
To je skvělé!
Určitě ale při zkoušení narazíš na pár věcí, které je potřeba dodělat:

* Had by neměl mít možnost vylézt ven z okýnka.
* Had by měl jíst jídlo a růst.
* Hra by měla skončit, když had narazí sám do sebe nebo do okraje okna.

Pojďme je vyřešit, jednu po druhé.


## Zatím dobrý, teď ale narazíme

„Hadí“ hry jako ta naše mají dvě varianty: buď je kolem hřiště „zeď“
a hráč při nárazu do okraje prohraje, nebo je hřiště „nekonečné“ – had okrajem
proleze a objeví se na druhé straně.
My naprogramujeme tu první variantu – zeď.

Abys zjistil{{a}}, jestli had „vylezl“ z levého okraje okna ven,
je potřeba zkontrolovat, jestli <var>x</var>-ová souřadnice hlavy
je menší než 0.
To je dobré udělat hned poté, co nové souřadnice hlavy získáš – konkrétně
hned za řádkem `new_head = new_x, new_y` v metodě `move`.

A co při takovém nárazu udělat?
Pro začátek bude nejjednodušší ukončit hru.
Na to má Python funkci `exit()`, která funguje podobně jako když v programu
nastane chyba.
Jen místo dlouhého chybového výpisu ukáže daný text.

Ukončení programu není příliš příjemný způsob, jak říct hráčovi že prohrál.
Za chvíli ale tuhle část předěláme, tak prozatím tenhle jednoduchý způsob postačí.

```python
    def move(self):
        old_x, old_y = self.snake[-1]
        dir_x, dir_y = self.snake_direction
        new_x = old_x + dir_x
        new_y = old_y + dir_y
        new_head = new_x, new_y

        # Nový kód – kontrola vylezení z hrací plochy
        if new_x < 0:
            exit('GAME OVER')

        self.snake.append(new_head)
        del self.snake[0]
```

Věřím, že zvládneš udělat stejnou kontrolu pro vylezení ze spodního okraje.

Jak ale ošetřit ty zbylé okraje – pravý a horní?
Na to je potřeba znát velikost okýnka.
A tu zná Pyglet; třída se stavem by k okýnku neměla mít přístup!

Na velikosti herní plochy závisí chování hry.
Tahle informace tedy bude tedy muset být součást stavu.
Pro začátek nějakou velikost – třeba 10×10 – nastav v `initialize`:

```python
        self.width = 10
        self.height = 10
```

A pak zařiď, aby po nárazu na neviditelnou stěnu kolem hřiště velkého
10×10 políček hra skončila.
Pořádně vyzkoušej všechny varianty – severní, jižní, východní i západní zeď.
Had je virtuální, nemusíš se bát že mu z narážení do zdí vyroste boule.

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

A pak v souboru se hrou hned po tom co vytvoříš stav (`state = GameState()`)
a okýnko (`window`) nastav *opravdovou* velikost.
Použij celočíselné dělení, aby počet políček byl v celých číslech:

```python
state.width = window.width // TILE_SIZE
state.height = window.height // TILE_SIZE
```


## Krmení

Tak. Had je v kleci, už nemůže vylézt.
Co dál?

Teď se musíš o hada postarat: pravidelně ho krmit.
Ale ještě předtím je potřeba ho naučit, jak se vůbec jí – na naši potravu
ještě není zvyklý.
Když to zvládneš, poroste jako z vody!

Konkrétně musíš hlavně zajistit aby, když se had připlazí na políčko
s jídlem, jídlo zmizelo.
K tomu se dá použít:
* operátor `in`, který zjišťuje jestli něco (třeba
  souřadnice) je v nějakém seznamu (třeba seznamu souřadnic jídla), a
* metoda `remove`, která ze seznamu odstraní daný prvek (podle *hodnoty* prvku
  – na rozdíl od `del`, který maže podle pozice).

Za kontrolu vylezení z hrací plochy potřebuješ dát kód,
který dělá následující:

* Pokud je nová pozice hlavy v seznamu souřadnic jídla:
  * Odeber tuhle pozici ze seznamu souřadnic jídla

Zvládneš ho napsat?

{% filter solution %}
```python
        if new_head in self.food:
            self.food.remove(new_head)
```
{% endfilter %}

Vyzkoušej, jestli to funguje. Had by měl jíst jídlo.

Ještě ale zbývá zařídit, aby po každém soustu trochu povyrostl.
Ale jak? Kterým směrem má růst?

Tady je dobré se podívat na existující kód a uvědomit si, co dělá.

Náš had se plazí tak, že napřed vepředu povyroste (pomocí `append`)
a potom se vzadu zmenší (pomocí `del self.snake[0]`).

Aby tedy po snězení jídla vyrostl, stačí *přeskočit* ono zmenšování!
A tím *přeskočit* myslím podmínit pomocí `if`.
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
Běda ale těm, kdo opisují kód aniž by se mu snažili porozumět!

{% filter solution %}
```python
    def move(self):
        old_x, old_y = self.snake[-1]
        dir_x, dir_y = self.snake_direction
        new_x = old_x + dir_x
        new_y = old_y + dir_y
        new_head = new_x, new_y

        # Kontrola vylezení z hrací plochy
        if new_x < 0:
            exit('GAME OVER')
        if new_y < 0:
            exit('GAME OVER')
        if new_x >= self.width:
            exit('GAME OVER')
        if new_y >= self.height:
            exit('GAME OVER')

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

Přidej do třídy `GameState` následující novou metodu, která umí přidat jídlo:

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
To je dobré tak akorát na… no, na to, aby sis ověřil{{a}} že se jídlo do
seznamu opravdu přidává.
Bylo by fajn, kdyby se nové jídlo objevilo vždycky jinde,
na náhodném místě.
Na to můžeš použít funkci `random.randrange`.
Vzpomeň si, že volání `randrage(N)` vrátí náhodné celé číslo od
0 do <var>N</var> - 1.

Jaký rozsah čísel potřebuješ pro hadí jídlo?

Až na to přijdeš, zkus přidat náhodu do programu: jídlo by se mělo objevit
na *úplně náhodném* políčku na herní ploše.

Nezapomeň na `import random` – to patří na úplný začátek souboru.
Další změny ale už dělej jen v metodě `add_food`.

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
vzdáme to. Jídla už je nejspíš dost.

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
V metodě `initialize` se dá místo nastavení `self.food` na seznam s pozicemi
jídla napsat:
```python
        self.food = []
        self.add_food()
        self.add_food()
```
Pak budou na začátku hry na hada čekat dvě náhodná jídla.
{% endfilter %}


## Konec

Had teď může narůst do obrovských rozměrů – a lze prohrát jen tím, že
narazí do stěny.
Zaříď, aby hra skončila i když narazí sám do sebe.

Jak na to?
Do metody `move`, vedle kontroly vylezení z hrací plochy,
dej kód který udělá následující:

* Pokud jsou souřadnice nové hlavy už součást hada:
  * Ukonči hru (podobně jako po nárazu do stěny).

Dokážeš to převést do Pythonu?

{% filter solution %}
```python
        # Kontrola, jestli had narazil
        if new_head in self.snake:
            exit('GAME OVER')
```
{% endfilter %}

Hotovo!

### Pauza

Není ale dobré při konci hry ukončit celý program a zavřít okýnko.

Lepší je hru „zapauzovat“ a ukázat hráči situaci, do které nešťastného hada
dostal, aby se z ní mohl pro příště poučit.

Aby to bylo možné, dáme do stavu hry další atribut: `alive`.
Ten bude nastavený na `True`, dokud bude had žít.
Když had narazí, nastaví se `alive` na `False`, a od té doby se už had nebude 
pohybovat.
Je dobré i graficky ukázat, že hadovi není dobře – hráč pak spíš bude
zpytovat svědomí.

Zkus zapřemýšlet, kam v kódu patří následující
kousky kódu, které prohru implementují:

```python
        # Prvotní nastavení atributu
        self.alive = True
```

```python
        # Zastavení hada
        self.alive = False
```

```python
        # Zabránění pohybu
        if not self.alive:
            return
```

```python
        # Grafická indikace
        if after == 'end' and not state.alive:
            after = 'dead'
```

{% filter solution %}
* „Prvotní nastavení atributu“ do metody `initialize`.
* „Zastavení hada“ místo *všech* výskytů `raise("Game Over")`.
* „Zabránění pohybu“ na úplný začátek metody `move` (příkaz `return`
  okamžitě ukončí provádění metody).
* „Grafická indikace“ za sekci pro vybírání obrázku pro kousek
  hada.
{% endfilter %}


## A to je vše?

Gratuluji, máš funkční a hratelnou hru!
Doufám že jsi na sebe hrd{{gnd('ý', 'á')}}!

Dej si něco sladkého, zasloužíš si to.

---

Tady je moje řešení.
To se touhle dobou od toho tvého může dost lišit – to je úplně normální.

(Nedívej se sem dokud hada nenaprogramuješ {{gnd('sám', 'sama')}}.
Chybami a neustálým zkoušením se člověk učí – a programátor zvlášť.
Čtením už vyřešeného se učí hůř.)


{% filter solution %}

```python
import random
import pyglet

TILE_SIZE = 64

class GameState:
    def initialize(self):
        self.snake = [(0, 0), (1, 0)]
        self.snake_direction = 0, 1
        self.width = 10
        self.height = 10
        self.food = []
        self.add_food()
        self.add_food()
        self.alive = True

    def draw(self):
        for x, y in self.snake:
            before = 'end'     # (Tady případně je nějaké
            after = 'end'      #  složitější vybírání políčka)
            if after == 'end' and not state.alive:
                after = 'dead'
            key = before + '-' + after
            snake_tiles[key].blit(x * TILE_SIZE, y * TILE_SIZE,
                                  width=TILE_SIZE, height=TILE_SIZE)
        for x, y in self.food:
            apple_image.blit(
                x * TILE_SIZE, y * TILE_SIZE, width=TILE_SIZE, height=TILE_SIZE)

    def move(self):
        if not self.alive:
            return

        old_x, old_y = self.snake[-1]
        dir_x, dir_y = self.snake_direction
        new_x = old_x + dir_x
        new_y = old_y + dir_y

        # Kontrola vylezení z hrací plochy
        if new_x < 0:
            self.alive = False
        if new_y < 0:
            self.alive = False
        if new_x >= self.width:
            self.alive = False
        if new_y >= self.height:
            self.alive = False

        new_head = new_x, new_y
        if new_head in self.snake:
            self.alive = False
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

apple_image = pyglet.image.load('apple.png')
snake_tiles = {}
for start in ['bottom', 'end', 'left', 'right', 'top']:
    for end in ['bottom', 'end', 'left', 'right', 'top', 'dead', 'tongue']:
        key = start + '-' + end
        image = pyglet.image.load('snake-tiles/' + key + '.png')
        snake_tiles[key] = image

window = pyglet.window.Window()

state = GameState()
state.initialize()
state.width = window.width // TILE_SIZE
state.height = window.height // TILE_SIZE


@window.event
def on_draw():
    window.clear()
    pyglet.gl.glEnable(pyglet.gl.GL_BLEND)
    pyglet.gl.glBlendFunc(pyglet.gl.GL_SRC_ALPHA, pyglet.gl.GL_ONE_MINUS_SRC_ALPHA)
    state.draw()


@window.event
def on_key_press(key_code, modifier):
    if key_code == pyglet.window.key.LEFT:
        state.snake_direction = -1, 0
    if key_code == pyglet.window.key.RIGHT:
        state.snake_direction = 1, 0
    if key_code == pyglet.window.key.DOWN:
        state.snake_direction = 0, -1
    if key_code == pyglet.window.key.UP:
        state.snake_direction = 0, 1


def move(dt):
    state.move()


pyglet.clock.schedule_interval(move, 1/6)

pyglet.app.run()
```
{% endfilter %}

## Co dál?

Najdeš ještě nějaké další vylepšení, které by se dalo udělat?

Zkus třeba následující rozšíření. Jsou seřazené zhruba podle složitosti:

* Vylepši ovládání (a hratelnost!) podle [návodu](../handling).

* Každých 30 vteřin hry přibude samo od sebe nové jídlo,
  takže jich pak bude na hrací ploše víc.

* Když had vyleze ven z okýnka, místo konce hry se objeví na druhé straně.
  (Viz [návod](../toroid).)

* Hadi budou dva; druhý se ovládá klávesami
  <kbd>W</kbd> <kbd>A</kbd> <kbd>S</kbd> <kbd>D</kbd>.<br>
  *(Na to je nejlepší udělat novou třídu, `Snake`, a všechen stav hada
  přesunout ze `GameState` do ní. Ve `GameState` pak měj seznam hadů.
  Téhle změně je potřeba přizpůsobit celý zytek programu.)*

* Hra se bude postupně zrychlovat.<br>
  *(Na to je nejlepší předělat funkci `move`, aby *sama*
  naplánovala, kdy se má příště zavolat. Volání `schedule_interval` tak už
  nebude potřeba.)*
