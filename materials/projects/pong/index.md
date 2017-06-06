# Pong

<div style="text-align:center;">
    <img src="{{ static('pong.png') }}" alt="">
</div>

Dnes si prohloubíme znalosti programování grafických aplikací,
které jsme získali na [lekci o Pygletu]({{ lesson_url('intro/pyglet') }}),
na reálném problému.

Naprogramujeme si s pomocí knihovny Pyglet
jednu z prvních videoher, [Pong](https://en.wikipedia.org/wiki/Pong).
Pong vydala společnost [Atari](https://en.wikipedia.org/wiki/Atari,_Inc.)
jako svůj první titul v roce 1972 a odstartovala tak boom herního průmyslu.

Na Youtube se můžeš podívat na
[video, které ukazuje jak se Pong hraje](https://www.youtube.com/watch?v=fiShX2pTz9A).


## Konstanty a stav hry

Hra Pong má jednoduchá pravidla. Musíme je ale umět
vyjádřit v Pythonu a to není úplně jednoduché.
Pojdmě si srovnat v hlavě, co ve hře máme.

* Hrací pole ve tvaru obdélníku s půlící čárou.
* Míček létající určitou rychlostí po hracím poli.
* Dvě pálky pohybující se vertikálně na krajích pole.
* Dvě počítadla skóre.

Hra bude pro 2 hráče, nebudeme programovat chování počítače.
Každý z hráčů může ovládat svou pálku stiskem kláves.
Jeden hráč šipkou nahoru a šipkou dolů a druhý hráč klávesami <kbd>W</kbd>
a <kbd>S</kbd>.

Stav hry dokážeme v Pythonu vyjádřit pomocí proměnných
a konstant. To dává smysl, protože některé
věci se ve hře mění (poloha pálek, poloha míčku, rychlost míčku, skóre)
a některé ne (velikost hrací plochy, velikost pálek a
míčku, poloha a velikost počítadel skóre).
Ze složitějších datových struktur použijeme seznam
(list, ten už známe) a množinu (set), která je velmi podobná
matematické množině. Zjednodušeně je to seznam, který se
nestará o pořadí a stejné prvky v něm mohou být právě jednou.

Možná přemýšlíš nad tím, v jakých jednotkách můžeme měřit
vzdálenost a rychlost v takovéto hře na počítači.
Na obrazovce je nešikovné měřit vzdálenost např.
v centimetrech. Nicméně každá obrazovka se skládá
z jednotlivých svítících bodů tzn. *pixelů*.
V grafické aplikaci jako je Pong můžeme tedy měřit
vzdálenost dvou míst na obrazovce jako počet pixelů
mezi těmito dvěma místy. Souřadný systém Pygletu
je založený právě na pixelech, přičemž pixel se
souřadnicemi [0, 0] je na obrazovce vlevo dole.
Rychlost můžeme jednoduše měřit v pixelech za sekundu.

Založte si nový skript. Společně nadefinujeme *konstanty*, které
budeme v tvorbě hry potřebovat. Normálně bychom
definovali konstanty postupně, až bychom je potřebovali,
ale pro jednoduchost to udělejme společně a najednou.
Ukážeme si na tom, jak začít převádět problém z reálného
světa do Pythonu.

```python
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
```

Nyní nadefinujeme *proměnné* potřebné v naší hře: poloha míčku, poloha pálek,
rychlost míče, stisknuté klávesy a skóre obou hráčů.
Budou to globální proměnné, za což by nás profesionální
programátor pokáral, ale nám to v tuhle chvíli ulehčí
práci.

```python
pozice_palek = [VYSKA // 2, VYSKA // 2]  # vertikalni pozice dvou palek
pozice_mice = [0, 0]  # x, y souradnice micku -- nastavene v reset()
rychlost_mice = [0, 0]  # x, y slozky rychlosti micku -- nastavene v reset()
stisknute_klavesy = set()  # sada stisknutych klaves
skore = [0, 0]  # skore dvou hracu
```

## Vykreslení hrací plochy

Nejprve si v Pygletu otevřeme okno velikosti hrací plochy.

```python
import pyglet
...
window = pyglet.window.Window(width=SIRKA, height=VYSKA)
pyglet.app.run()  # vse je nastaveno, at zacne hra
```

Než začneme dělat interaktivní část hry reagující na vstupy
od uživatele, je třeba umět vůbec vykreslit prvky na hrací
ploše. Podobně jako jsme v lekci o Pygletu měli funkci
`vykresli()`, která vykreslila hada, budeme mít
v Pongu funkci stejného jména, která vykreslí prvky na hrací
ploše.

Většina z tvarů jsou obdélníky, takže nejprve
navrhněme funkci `nakresli_obdelnik`, která
dostane čtveřici souřadnic a pomocí modulu `gl`
z Pygletu vykreslí čtverec pomocí 2 trojúhelníků.

```python
from pyglet import gl
...
def nakresli_obdelnik(x1, y1, x2, y2):
    """Nakresli obdelnik na dane souradnice

    Nazorny diagram::

         y2 - +-----+
              |/////|
         y1 - +-----+
              :     :
             x1    x2
    """
    # Tady pouzijeme volani OpenGL, ktere je pro nas zatim asi nejjednodussi
    # na pouziti
    gl.glBegin(gl.GL_TRIANGLE_FAN)   # zacni kreslit spojene trojuhelniky
    gl.glVertex2f(int(x1), int(y1))  # vrchol A
    gl.glVertex2f(int(x1), int(y2))  # vrchol B
    gl.glVertex2f(int(x2), int(y2))  # vrchol C, nakresli trojuhelnik ABC
    gl.glVertex2f(int(x2), int(y1))  # vrchol D, nakresli trojuhelnik BCD
    # dalsi souradnice E by nakreslila trojuhelnik CDE, atd.
    gl.glEnd()  # ukonci kresleni trojuhelniku
```


Teď začneme pracovat na funkci `vykresli()`
Nejprve ji vytvoř prázdnou a zaregistruj ji
v Pygletu na událost `on_draw`, jak jsme to
dělali v lekci o Pygletu. To znamená, že se tato funkce
zavolá pokaždé, když Pyglet překreslí okno. Pokud se
mezitím např. změnila poloha míčku, funkce ho vykreslí
o kousek jinde. Tím vlastně vytváříme dynamiku hry.
Analogicky jsme to dělali s hadem, tady máme jen víc
grafických prvků.

```python
...
def vykresli():
    """Vykresli stav hry"""
    gl.glClear(gl.GL_COLOR_BUFFER_BIT)  # smaz obsah okna (vybarvi na cerno)
    gl.glColor3f(1, 1, 1)  # nastav barvu kresleni na bilou

window = pyglet.window.Window(width=SIRKA, height=VYSKA)
window.push_handlers(
    on_draw=vykresli,  # na vykresleni okna pouzij funkci `vykresli`
)
pyglet.app.run()  # vse je nastaveno, at zacne hra
```

Zatím máme v těle funkce jen volání, která vyčistí
plochu, do které kreslíme a nastaví barvu kreslení na bílou.

Teď zkus {{gnd('sám', 'sama')}} do funkce `vykresli()` přidat
vykreslení `míčku` na správné pozici,
kterou získáš z příslušné globální proměnné. Míček je
v našem případě jen malý čtvereček jehož velikost
máme uloženou v konstantě.

{% filter solution %}
```python
def vykresli():
    ...
    # Vykresleni micku
    nakresli_obdelnik(
        pozice_mice[0] - VELIKOST_MICE // 2,
        pozice_mice[1] - VELIKOST_MICE // 2,
        pozice_mice[0] + VELIKOST_MICE // 2,
        pozice_mice[1] + VELIKOST_MICE // 2,
    )
```
{% endfilter %}


Po míčku zkus vykreslit obě *pálky*.
V proměnné `pozice_palek` máme vertikální
polohu první a druhé pálky, ale horizontální poloha je
konstantní. Jaké souřadnice musíš předat funkci
`nakresli_obdelnik`, aby se pálka vykreslila
správně a na správném místě? Princip určení souřadnic
je podobný jako u vykreslení míčku.

{% filter solution %}
```python
def vykresli():
    ...
    # palky - udelame si seznam souradnic palek a pro kazdou dvojici souradnic
    # v tom seznamu palku vykreslime
    for x, y in [(0, pozice_palek[0]), (SIRKA, pozice_palek[1])]:
        nakresli_obdelnik(
            x - TLOUSTKA_PALKY,
            y - DELKA_PALKY // 2,
            x + TLOUSTKA_PALKY,
            y + DELKA_PALKY // 2,
        )
```
{% endfilter %}

Přehlednosti hry pomůže *půlící čára*
uprostřed. Jak ji ale namalovat?
Nebudeme vymýšlet zbytečné složitosti.
Namalujme ji jako sérii obdélníčků táhnoucích se odshora
dolů. Chce to jen vygenerovat seznam souřadnic,
které budou mít dostatečné rozestupy, a na každé
z nich vykreslit obdélníček. Kterou funkci z Pythonu
bys použila na získání tohoto seznamu souřadnic?

{% filter solution %}
```python
def vykresli():
    ...
    # prerusovana pulici cara - slozena ze spousty malych obdelnicku
    for y in range(DELKA_PULICI_CARKY // 2, VYSKA, DELKA_PULICI_CARKY * 2):
        nakresli_obdelnik(
            SIRKA // 2 - 1,
            y,
            SIRKA // 2 + 1,
            y + DELKA_PULICI_CARKY
        )
```
{% endfilter %}

Co nám ještě chybí? *Počítadlo skóre* pro oba hráče.
K tomu se musíme naučit vykreslovat v Pygletu text.
V Pygletu je modul `text`, který obsahuje
objekt `Label` (Nápis). Ten se hodí k vykreslení hodnoty
skóre. Objekt musíme nejdřív vytvořit. To uděláme
kulatými závorkami za jménem objektu, jako bychom
volali funkci, a uložíme si ho do proměnné:
`napis = Label()`. Normálně bychom objekt
vytvořili jen jednou a pak měnili jeho hodnotu, ale
pro jednoduchost vytvoříme vždy nový a celé to zabalíme
do funkce. V jejím závěru musíme na nadpisu zavolat
metodu `draw()`, jinak se nápis nevykreslí.

```python
def nakresli_text(text, x, y, pozice_x):
    """Nakresli dany text na danou pozici

    Argument ``pozice_x`` muze byt "left" nebo "right", udava na kterou stranu
    bude text zarovnany
    """
    napis = pyglet.text.Label(
        text,
        font_size=VELIKOST_FONTU,
        x=x, y=y, anchor_x=pozice_x
    )
    napis.draw()
```

Teď zkus tuto funkci použít ve funkci `vykresli()`
k nakreslení skóre. K určení pozice textu použij
konstanty SIRKA, VYSKA, ODSAZENI_TEXTU a VELIKOST_FONTU.

{% filter solution %}
```python
def vykresli():
    ...
    # A nakonec vypiseme skore obou hracu
    nakresli_text(
        str(skore[0]),
        x=ODSAZENI_TEXTU,
        y=VYSKA - ODSAZENI_TEXTU - VELIKOST_FONTU,
        pozice_x='left',
    )

    nakresli_text(
        str(skore[1]),
        x=SIRKA - ODSAZENI_TEXTU,
        y=VYSKA - ODSAZENI_TEXTU - VELIKOST_FONTU,
        pozice_x='right',
    )

```
{% endfilter %}



Hurá, teď už máme vykreslené hrací pole. Pojďme ho rozhýbat.
## Dynamika hry

Teď to začne být zajímavé. Nejdřív rozhýbeme pálky,
protože je to jednodušší, pak míček.

### Vstup od uživatele

Potřebujeme pohybovat s pálkami podle vstupu od uživatele.
Dokud bude uživatel držet např. klávesu <kbd>S</kbd>, levá pálka
pojede dolů.
V Pygletu jsme se naučili pracovat s událostí
`on_text`, ta nám ale v tomto případě nebude stačit.
K realizaci pohybu pálek budeme potřebovat 2 typy událostí,
které ještě neznáme - `on_key_press` a `on_key_release`.

Pyglet zavolá funkci registrovanou na událost `on_key_press`
stejně jako při vykreslování okna zavolal funkci `vykresli()`,
zaregistrovanou na události `on_draw`.
Přidáme právě stisknutou klávesu do množiny stisknutých
kláves v globální proměnné `stisknute_klavesy`
jako <var>n</var>-tici `(směr, číslo pálky)`, např. tedy
`('nahoru', 0)`, což bude vyjadřovat, že levá pálka má jet nahoru.
Při události `on_key_release` odebereme právě
stisknutou klávesu z množiny `stisknute_klavesy`.
Tím zajistíme, že v daný okamžik bude množina `stisknute_klavesy`
obsahovat všechny klávesy, které uživatel drží, a budeme
podle toho moct pohnout s pálkami.

Troufneš si napsat funkce `stisk_klavesy(symbol, modifikatory)`
a `pusteni_klavesy(symbol, modifikatory)`?
Poznamenejme, že do množiny `stisknute_klavesy`
můžeš přidat prvek metodou `add(prvek)` a pak
odebrat metodou `discard(prvek)`. Obě berou jako
argument prvek, který se má přidat nebo odstranit,
v našem případě konkrétní <var>n</var>-tici.

Budeš potřebovat zjistit, kterou klávesu uživatel stisknul.
Kód stisknuté klávesy předá Pyglet našim funkcím
v argumentu `symbol`. Je to ale nic neříkající
číslo. Z `pyglet.window` můžeš naimportovat
modul `key`, který obsahuje konstanty jednotlivých
kláves. Můžeš pak porovnat, zda symbol odpovídá např.
klávese <kbd>↑</kbd> jako `symbol == key.UP`.

{% filter solution %}
```python
from pyglet.window import key
...
def stisk_klavesy(symbol, modifikatory):
    if symbol == key.W:
        stisknute_klavesy.add(('nahoru', 0))
    if symbol == key.S:
        stisknute_klavesy.add(('dolu', 0))
    if symbol == key.UP:
        stisknute_klavesy.add(('nahoru', 1))
    if symbol == key.DOWN:
        stisknute_klavesy.add(('dolu', 1))


def pusteni_klavesy(symbol, modifikatory):
    if symbol == key.W:
        stisknute_klavesy.discard(('nahoru', 0))
    if symbol == key.S:
        stisknute_klavesy.discard(('dolu', 0))
    if symbol == key.UP:
        stisknute_klavesy.discard(('nahoru', 1))
    if symbol == key.DOWN:
        stisknute_klavesy.discard(('dolu', 1))
...
```
{% endfilter %}

> [note]
> Proč vlastně používáme k odebrání <var>n</var>-tice metodu
> `discard()` místo metody `remove()`,
> kterou známe ze seznamů a množiny ji také mají?
> Nezpůsobí totiž chybu, když se pokusíme odebrat
> prvek, který v množině není. To by se mohlo stát,
> kdyby uživatel stiskl jednu z funkčních kláves
> a teprve pak se přepnul do našeho okna a pak jí
> pustil.


Zaregistruj si obě funkce na příslušné události:

```python
...
window = pyglet.window.Window(width=SIRKA, height=VYSKA)
window.push_handlers(
    on_draw=vykresli,  # na vykresleni okna pouzij funkci `vykresli`
    on_key_press=stisk_klavesy,
    on_key_release=pusteni_klavesy,
)
pyglet.app.run()
```

### Pohyb pálek

Když už jsme dokázali zpracovat vstup od uživatele,
můžeme podle něj pohnout s pálkami.
Pohyb předmětů budeme provádět ve funkci `obnov_stav(dt)`,
která bude registrována na tik hodin v Pygletu.
Argument `dt` je čas od posledního zavolání funkce Pygletem.

```python
def obnov_stav(dt):
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
```

Podívejme se na tento kus kódu. Procházíme
v cyklu obě pálky a ptáme se, zda je v množině
stisknutých kláves <var>n</var>-tice reprezentující
pohyb dané pálky nahoru nebo dolů.
Když ano, *pohneme pálkou* v daném směru
(přičteme nebo odečteme od vertikální polohy pálky
změnu polohy, což je čas od posledního zavolání,
který známe, vynásobený rychlostí pálky nastavené
v konstantě).

V druhé části musíme zajistit, aby pálka *nevyjela*
z hracího pole. Z minulých hrátek s hadem víme,
že to se může stát velmi snadno. Pálku malujeme kolem
jejího středu, což znamená, že když se pálka přiblíží na
na <var>y</var>-ovou pozici `DELKA_PALKY / 2`, začíná
překračovat dolní hranici hracího pole. V tom případě
její pozici zafixujeme na nejnižší možné souřadnici.
Analogicky to provedeme, když se blíží hornímu okraji.

Zaregistruj vytvořenou funkci na tik hodin jako

```python
...
pyglet.clock.schedule(obnov_stav)
pyglet.app.run()
```

a podívej se na výsledek.


### Rozehrání

Než začneme míček odrážet od stěn, musíme ho nejprve
uvést do pohybu. Vystřelíme ho ze středu hrací plochy
do náhodného směru. Toto se také stane v momentě, kdy
jeden z hráčů skóruje a hra se rozehrává znovu.
Proto tohle rozehrání zabalíme do funkce `reset()`.
Zavolejte ji, než se spustí hra.

Jak bude tato funkce vypadat?
Nejprve přesuň míček do středu hrací plochy nastavením
proměnné `pozice_mice`. Potom je třeba
simulovat hod mincí pomocí volání funkce
`random.randint(0, 1)`. Tím rozhodneme, zda
se míček rozletí doprava nebo doleva.
Míček rozpohybujeme horizontálním směrem přičtením
požadované rychlosti k `rychlost_mice[0]`.
Ve vertikálním směru `rychlost_mice[1]`
se bude míček pohybovat zcela náhodně přičtením
náhodné rychlosti.

{% filter solution %}
```python
import random
...
def reset():
    pozice_mice[0] = SIRKA // 2
    pozice_mice[1] = VYSKA // 2

    # x-ova rychlost - bud vpravo, nebo vlevo
    if random.randint(0, 1):
        rychlost_mice[0] = RYCHLOST
    else:
        rychlost_mice[0] = -RYCHLOST
    # y-ova rychlost - uplne nahodna
    rychlost_mice[1] = random.uniform(-1, 1) * RYCHLOST

# nastavit vychozi stav pro start hry
reset()
```
{% endfilter %}


Nic se zatím ale nestane, protože funkce
`obnov_stav(dt)` zatím nepracuje
se změnou rychlosti. Musíme v ní tedy nastavit proměnnou
`poloha_micku` podle současné rychlosti míčku
a času uplynulého od posledního zavolání funkce podle
fyzikálního vztahu <var>s</var> = <var>v</var> <var>t</var>, tedy že dráha
je rovna rychlosti vynásobené časem. Přidej tedy do
funkce `obnov_stav(dt)` následující kód:

```python
def obnov_stav(dt):
    ...
    # POHYB MICKU
    pozice_mice[0] += rychlost_mice[0] * dt
    pozice_mice[1] += rychlost_mice[1] * dt
```

Zkus, co se teď stane při spuštění hry.
Míček by měl vyletět pokaždé do jiného směru.

### Odrážení míčku

Míček nám teď nekontrolovaně vyletí z hřiště.
Musíme tedy zařídit, aby se odrážel od stěn.
Jelikož úhel dopadu se rovná úhlu odrazu,
stačí otočit znaménko <var>y</var>-ové složky rychlosti.
Do funkce `obnov_stav(dt)` musíme
přidat kontroly na polohu míčku a případně
změnit jeho směr, pokud je moc nízko nebo moc vysoko.

```python
def obnov_stav(dt):
    ...
    # Odraz micku od sten
    if pozice_mice[1] < VELIKOST_MICE // 2:
        rychlost_mice[1] = abs(rychlost_mice[1])
    if pozice_mice[1] > VYSKA - VELIKOST_MICE // 2:
        rychlost_mice[1] = -abs(rychlost_mice[1])
```


Teď nám zbývá odraz od pálky, případně resetování
hry, pokud míček padne mimo pálku jednoho hráče a
ten druhý tak získá bod. Opět tedy budeme přidávat
kód do funkce `obnov_stav(dt)`.

Prvním krokem je poznamenání mezí na <var>y</var>-ové ose,
kde se musí míček nacházet, aby byl úspěšně odražen –
to je mezi horním a dolním koncem pálky:

```python
def obnov_stav(dt):
    ...
    palka_min = pozice_mice[1] - VELIKOST_MICE / 2 - DELKA_PALKY / 2
    palka_max = pozice_mice[1] + VELIKOST_MICE / 2 + DELKA_PALKY / 2
```

Nyní když míček narazí do pravé nebo levé stěny
se umíme zeptat, zda je pálka na správné pozici
a my máme `odrazit` míček nebo zda hráč
prohrál kolo a my máme přičíst jeho soupeři bod a
`restartovat hru`.

```python
def obnov_stav(dt):
    ...
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
```

## Závěr

Hurá, prokousali jsme se k zdárnému konci Pongu!
Máš teď plně funkční interaktivní grafickou
hru zakládající se na reálné předloze. :)
