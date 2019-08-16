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

snake = [(1, 2), (2, 2), (3, 2), (3, 3), (3, 4), (3, 5), (4, 5)]
food = [(2, 0), (5, 1), (1, 4)]

red_image = pyglet.image.load('apple.png')
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
    pyglet.gl.glEnable(pyglet.gl.GL_BLEND)
    pyglet.gl.glBlendFunc(pyglet.gl.GL_SRC_ALPHA, pyglet.gl.GL_ONE_MINUS_SRC_ALPHA)
    for x, y in snake:
        before = 'end'     # (Tady případně je nějaké
        after = 'end'      #  složitější vybírání políčka)
        snake_tiles[before + '-' + after].blit(
            x * TILE_SIZE, y * TILE_SIZE, width=TILE_SIZE, height=TILE_SIZE)
    for x, y in food:
        red_image.blit(
            x * TILE_SIZE, y * TILE_SIZE, width=TILE_SIZE, height=TILE_SIZE)

pyglet.app.run()
```

Zkus těsně nad řádek `pyglet.app.run` doplnit funkci,
která se bude volat každou šestinu vteřiny
a přidá hadovi políčko navíc:

``` python
def move(dt):
    x, y = snake[-1]
    new_x = x + 1
    new_y = y
    new_head = new_x, new_y
    snake.append(new_head)

pyglet.clock.schedule_interval(move, 1/6)
```

Funguje?
Tak do téhle funkce ještě přidej `del snake[0]`, aby had nerostl donekonečna.
Víš co tenhle příkaz dělá? Jestli ne, koukni znovu na poznámky k seznamům!

Zvládneš funkci upravit tak, aby had lezl nahoru?

Jestli ano, gratuluji!
Zvývá směr hada ovládat šipkami na klávesnici, a většina hry bude hotová!


## Třída pro stav

Než ale uděláme interaktivního hada, zkusíme trošku uklidit.
Program se nám rozrůstá a za chvíli bude složité se v něm vyznat.

Stav hry máme zatím ve dvou seznamech: `snake` a `food`.
Časem ale bude podobných proměnných víc.

Abychom je měli všechny pohromadě, vytvoříme pro stav hry *třídu*.

{# XXX: More about classes #}

Na všechno, co se ve hře může stát, nadefinujeme *metody*.
Zatím budou dvě: začátek hry a pohyb hada.

Na začátku hry se zavolá metoda `__init__`.
Má trochu divné jméno se dvěma podtržítkama na každé straně.
Podle toho Python ví, že tahle metoda je speciální a se má volat
při vytvoření objektu.

Metoda `__init__` nastaví celý stav hry jako *atributy*.
Stav hry je všechno, co potřebujeme o hře vědět a může se to časem měnit.
V našem případě to zatím budou souřadnice hada a jídla.

Metoda `move`, kterou budeme volat při každém „tahu“ hry, je bude tyhle
atributy měnit.

Pro funkčnost, kterou zatím náš had umí, bude třída se stavem vypadat
následovně.
Přidej ji do programu hned za nastavení konstant.

```python
class State:
    def __init__(self):
        self.food = [(2, 0), (5, 1), (1, 4)]
        self.snake = [(0, 0), (1, 0)]

    def move(self):
        old_x, old_y = self.snake[-1]
        new_x = old_x + 1
        new_y = old_y
        new_head = new_x, new_y
        self.snake.append(new_head)
        del self.snake[0]
```

> [note]
> Použij prosím pro třídu jméno `State` a i atributy pojmenuj podle
> materiálů (`snake`, `food`, a později i další).
> Bude se ti to hodit.

Všimni si, že metody berou argument `self`.
To označuje konkrétní objekt, stav hry se kterým metoda pracuje nebo
který mění.
Ke všem atributům přistupují pomocí tečky –
<code>self.<var>jméno_atributu</var></code>.

Tak, máme třídu se stavem.
No jo, ale jak ji teď použít?

Na to potřebuješ ještě několik změn:

* Nastavování seznamů `snake` a `food` (mimo třídu) zruš; místo nich nastav
  jedinou proměnnou `state` na nový stav:

  ```python
  state = State()
  ```

* Místo `snake` a `food` ve funkci `on_draw` použij `state.snake`
  a `state.food` – atributy našeho stavu.

  Všimni si že tady se nepoužívá `self`, což je jméno které používají jen
  *metody* v rámci třídy.
  Jinde musíš pojmenovat konkrétní objekt, se kterým pracujeme.

* Funkci `move` přepiš tak, aby jen volala metodu `state.move`:

  ```python
  def move(dt):
      state.move()
  ```

  Všimni si že ani tady se nepoužívá `self`.

* Vykreslování hada z funkce `on_draw` přesuň do nové metody
  `draw`:

  ```python
  class State:
    ...

    def draw(self):
        for x, y in state.snake:
            ...
        for x, y in state.food:
            ...
  ...

  @window.event
  def on_draw():
      window.clear()
      pyglet.gl.glEnable(pyglet.gl.GL_BLEND)
      pyglet.gl.glBlendFunc(pyglet.gl.GL_SRC_ALPHA, pyglet.gl.GL_ONE_MINUS_SRC_ALPHA)
      state.draw()
  ```

  Všimni si že ani tady se nepoužívá `self`.

Povedlo se? Funguje to jako předtím?
Pro kontrolu můžeš svůj program porovnat s mým (ale nejde o jediné správné
řešení):

{% filter solution %}
```python
import pyglet

TILE_SIZE = 64

class State:
    def __init__(self):
        self.food = [(2, 0), (5, 1), (1, 4)]
        self.snake = [(0, 0), (1, 0)]

    def move(self):
        old_x, old_y = self.snake[-1]
        new_x = old_x + 1
        new_y = old_y
        new_head = new_x, new_y
        self.snake.append(new_head)
        del self.snake[0]

    def draw(self):
        for x, y in state.snake:
            before = 'end'     # (Tady případně je nějaké
            after = 'end'      #  složitější vybírání políčka)
            snake_tiles[before + '-' + after].blit(
                x * TILE_SIZE, y * TILE_SIZE, width=TILE_SIZE, height=TILE_SIZE)
        for x, y in state.food:
            red_image.blit(
                x * TILE_SIZE, y * TILE_SIZE, width=TILE_SIZE, height=TILE_SIZE)

red_image = pyglet.image.load('apple.png')
snake_tiles = {}
for start in ['bottom', 'end', 'left', 'right', 'top']:
    for end in ['bottom', 'end', 'left', 'right', 'top', 'dead', 'tongue']:
        key = start + '-' + end
        image = pyglet.image.load('snake-tiles/' + key + '.png')
        snake_tiles[key] = image

window = pyglet.window.Window()

state = State()

@window.event
def on_draw():
    window.clear()
    pyglet.gl.glEnable(pyglet.gl.GL_BLEND)
    pyglet.gl.glBlendFunc(pyglet.gl.GL_SRC_ALPHA, pyglet.gl.GL_ONE_MINUS_SRC_ALPHA)
    state.draw()

def move(dt):
    state.move()

pyglet.clock.schedule_interval(move, 1/6)

pyglet.app.run()
```
{% endfilter %}


## Ovládání

Nyní k onomu slíbenému ovládání. Respektive nejdřív k změnám směru.

Had ze hry se plazí stále stejným směrem, dokud hráč nezmáckne klávesu.
Had z naší ukázky se plazí doprava.
Jestli jsi to ještě neudělal{{a}}, zkus zařídit, aby se místo toho
plazil nahoru.

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

* `(1, 0)` = doprava (o jedno políčko v kladném <var>x</var>-ovém směru;
   v <var>y</var>-ovém neposouvat)
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

Druhý parametr nebude v naší hře potřeba, ale v hlavičce funkce musí být.

Podle prvního ale nastav aktuální směr hada.
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

[key-constants]: https://pyglet.readthedocs.io/en/pyglet-1.3-maintenance/modules/window_key.html#key-constants

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
Jen místo chybového výpisu ukáže daný text.

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
Pro začátek nějakou velikost – třeba 10×10 – nastav v `__init__`:

```python
        self.width = 10
        self.height = 10
```

A pak zařiď, aby po nárazu na neviditelnou stěnu kolem hřiště velkého
10×10 políček hra skončila.
Pořádně vyzkoušej všechny varianty – severní, jižní, východní i západní zeď.
Had je virtuální, nemusíš se bát že mu z toho vyroste boule.

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

A pak v souboru se hrou hned po tom co vytvoříš stav (`state = State()`)
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
Na to můžeme použít funkci `random.randrange`.
Vzpomeň si, že volání `randrage(N)` vrátí náhodné celé číslo od
0 do <var>N</var> - 1.

Jaký rozsah čísel potřebujeme pro hadí jídlo?

Až na to přijdeš, zkus přidat náhodu do programu: jídlo by se mělo objevit
na *úplně náhjodném* políčku na herní ploše.

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
V metodě `__init__` se dá místo nastavení `self.food` na seznam s pozicemi
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
Zaříď teď, aby hra skončila i když narazí sám do sebe.

Jak na to?
Do metody `move`, vedle kontrola vylezení z hrací plochy,
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
Když had narazí, nastaví se na `False`, a od té doby se už nebude pohybovat.
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
* „Prvotní nastavení atributu“ do metody `__init__`.
* „Zastaveni hada“ místo všech výskytů `raise("Game Over")`.
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
(A nedívej se sem dokud hada nenaprogramuješ {{gnd('sám', 'sama')}},
Chybami a neustálým zkoušením se člověk učí – a programátor zvlášť.
Čtením už vyřešeného se učí hůř.)


{% filter solution %}

```python
import random
from pathlib import Path

import pyglet

TILE_SIZE = 64

class State:
    def __init__(self):
        self.snake = [(0, 0), (1, 0)]
        self.snake_direction = 0, 1
        self.width = 10
        self.height = 10
        self.food = []
        self.add_food()
        self.add_food()
        self.alive = True

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

red_image = pyglet.image.load('apple.png')
snake_tiles = {}
for start in ['bottom', 'end', 'left', 'right', 'top']:
    for end in ['bottom', 'end', 'left', 'right', 'top', 'dead', 'tongue']:
        key = start + '-' + end
        image = pyglet.image.load('snake-tiles/' + key + '.png')
        snake_tiles[key] = image

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
        before = 'end'     # (Tady případně je nějaké
        after = 'end'      #  složitější vybírání políčka)
        if after == 'end' and not state.alive:
            after = 'dead'
        snake_tiles[before + '-' + after].blit(
            x * TILE_SIZE, y * TILE_SIZE, width=TILE_SIZE, height=TILE_SIZE)
    for x, y in state.food:
        red_image.blit(
            x * TILE_SIZE, y * TILE_SIZE, width=TILE_SIZE, height=TILE_SIZE)


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

* Hra se bude postupně zrychlovat.<br>
  *(Na to je nejlepší předělat funkci `move`, aby *sama*
  naplánovala, kdy se má příště zavolat. Volání `schedule_interval` tak už
  nebude potřeba.)*

* Když had vyleze ven z okýnka, místo konce hry se objeví na druhé straně.
  (Viz [návod](../toroid).)

* Hadi budou dva; druhý se ovládá klávesami
  <kbd>W</kbd> <kbd>A</kbd> <kbd>S</kbd> <kbd>D</kbd>.<br>
  *(Na to je nejlepší udělat novou třídu, `Snake`, a všechen stav hada
  přesunout ze `State` do ní. Ve `State` pak měj seznam hadů.
  Téhle změně je potřeba přizpůsobit celý zytek programu.)*
