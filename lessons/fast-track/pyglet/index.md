# Grafika

Teď si ukážeme, jak napsat grafickou aplikaci.

Python obsahuje nástroje na kreslení obrázků,
ale pro tvorbu her nejsou příliš vhodné.
Použijeme proto *knihovnu* (nadstavbu) jménem Pyglet, která je přímo stavěná
na interaktivní grafiku.

Musíme si ji ale nejdřív zvlášť nainstalovat.
Nejjistější je do příkazové řádky se zapnutým virtuálním prostředím
zadat následující dva příkazy.
(Existují i jednodušší způsoby, které ovšem vyžadují „správně“
nastavený systém.)

* Aktualizace nástroje `pip`, který umí instalovat knihovny pro Python:
  ``` console
  (venv)$ python -m pip install --upgrade pip
  ```
  (V překladu: **Python**e, spusť **m**odul **pip** a řekni mu,
  ať na**instal**uje a kdyžtak aktualizuje (*upgrade*) knihovnu **pip**.)
* Samotné nainstalování Pygletu:
  ``` console
  (venv)$ python -m pip install pyglet
  ```
  (V překladu: **Python**e, spusť **m**odul **pip** a řekni mu,
  ať na**instal**uje knihovnu **pyglet**.)

U mě vypadá instalace nějak takto:

```console
(venv)$ python -m pip install --upgrade pip
Requirement already satisfied: pip in ./venv/lib/python3.6/site-packages (18.0)
(venv)$ python -m pip install pyglet
Collecting pyglet
  Downloading pyglet-1.2.4-py3-none-any.whl (964kB)
Installing collected packages: pyglet
Successfully installed pyglet-1.2.4
```

Důležité je `Successfully installed`, resp. `Requirement already satisfied`
na konci.
To znamená že je knihovna připravená k použití!


## Kostra programu

Teď zkus v editoru vytvořit nový soubor, uložit ho jako `grafika.py`
a napsat do něj následující program:

```python
import pyglet
window = pyglet.window.Window()
pyglet.app.run()
print('Hotovo!')
```

Spusť ho. Mělo by se objevit černé okýnko.

> [note] Okýnko není černé?
> Na některých počítačích (často s macOS a některými druhy Linuxu) se stává,
> že okýnko není černé, ale je v něm nějaký „nepořádek“.
> To nevadí.
> Než do okýnka začneme kreslit, nepořádek uklidíme.

> [note] AttributeError?
> Jestli dostaneš chybu
> `AttributeError: module 'pyglet' has no attribute 'window'`, zkontroluj si,
> zě jsi soubor pojmenoval{{a}} `grafika.py` a ne `pyglet.py`.
> Soubor v editoru ulož jako `grafika.py`, případný soubor `pyglet.py` smaž,
> a zkus to znovu.

Hotovo? Pojďme si vysvětlit, co se v tomhle programu děje.

Příkaz `import pyglet` ti zpřístupní grafickou knihovnu, tak jako třeba
`import random` ti zpřístupní funkce okolo náhodných čísel.

Zavolání `pyglet.window.Window()` vytvoří nové *okýnko* na obrazovce.
Vrátí objekt, kterým pak tohle okýnko můžeš ovládat; ten si uložíme
do proměnné `window`.

Zavolání `pyglet.app.run()` pak spustí aplikaci.
Co to znamená?

Jednoduché programy, které jsi zatím psal{{a}}, jsou popisy procesu – podobně
jako třeba recepty k vaření.
Sled kroků, které Python postupně vykoná od prvního po poslední.
Občas se něco opakuje a některé kroky se dají „zabalit“ do funkce,
ale vždycky jsme zatím popisovali jeden postup od začátku po konec.

Programy pro složitější aplikace spíš než jako recept vypadají jako příručka
automechanika.
Popisují, co se má stát v jaké situaci.
Třeba program pro textový editor by mohl vypadat takhle:

* Když uživatel zmáčkne písmenko na klávesnici, přidej ho do dokumentu.
* <p>Když uživatel zmáčkne <kbd>⌫ Backspace</kbd>, poslední písmenko umaž.</p>
* Když uživatel zmáčkne tlačítko Uložit, zapiš soubor na disk.

I takový program se dá napsat i jako „recept“ – ale ten recept je pro všechny
aplikace stejný:

* Pořád dokola:
  * Počkej, než se něco zajímavého stane
  * Zareaguj na nastalou situaci

A to je přesně to, co dělá `pyglet.app.run()`.
Zpracovává *události*, situace na které je potřeba zareagovat.
V tvém programu reaguje zavírací tlačítko okýnka a na klávesu <kbd>Esc</kbd>
tím, že okno zavře a ukončí se.

Tvůj úkol teď bude popsat, jaké další události jsou zajímavé
a jak na ně reagovat.


## Obsluha událostí

Nejjednodušší událost, kterou můžeme obsloužit, je psaní textu na klávesnici.

Zkus do programu těsně nad řádek `pyglet.app.run()` dát následující kód:

``` python
@window.event
def on_text(text):
    print(text)
```

Co to je?
Je to definice funkce, ale na začátku má *dekorátor* – tu řádku začínající
zavináčem.

Dekorátor `window.event` je způsob, jak Pygletu říct, že má tuto funkci
spustit, když se něco zajímavého stane.

Co zajímavého?
To Pyglet zjistí podle jména funkce: `on_text` reaguje na text.
Vždycky, když uživatel zmáčkne klávesu, Pyglet zavolá tvoji funkci!

A co udělá tvoje funkce? Zavolá `print`. To už znáš.
Zadaný text se vypíše na konzoli, ze které program spouštíš.
To, že je otevřené okýnko, neznamená že `print` začne automaticky psát do něj!


## Kreslení

Jak psát do okýnka?
To je trochu složitější než do konzole.
Text tu může mít různé barvy, velikosti, druhy písma,
může být všelijak posunutý nebo natočený…

Všechny tyhle *atributy* písma můžeme (i se samotným textem) uložit do objektu 
`Label` („popisek“).
Zkus to – dej následující kód pod řádek s `window = `:

```python
label = pyglet.text.Label("Ahoj!", x=10, y=20)
```

V proměnné `label` teď budeš mít máš popisek s textem `"Ahoj"`, který patří
na pozici (10, 20) – 10 bodů od pravého okraje okna, 20 od spodního.

Popisek se ale sám nevypíše.
Podobně jako pro vypsání textu do konzole je potřeba zavolat `print`,
pro nakreslení textu je potřeba reagovat na událost
*vykreslení okna* – `on_draw`.

Dej pod funkci `on_text` tento kód:

```python
@window.event
def on_draw():
    window.clear()
    label.draw()
```

Tuhle funkci Pyglet zavolá vždycky, když je potřeba nakreslit obsah okýnka.
U animací (filmů nebo her) to často bývá třeba 60× za sekundu
(„[60 FPS](https://cs.wikipedia.org/wiki/Sn%C3%ADmkov%C3%A1_frekvence)“).

Funkce dělá dvě věci:
* Smaže celé okýnko (nabarví ho na černo)
* Vykreslí text

V okně teď bude vidět pozdrav!


Zkus ještě změnit `on_text` tak, aby se zadaný text místo na konzoli
ukázal v okýnku.
To se dělá přiřazením do *atributu* `label.text`:

```python
@window.event
def on_text(text):
    print('Starý text:', label.text)
    label.text = text
    print('Nový text:', label.text)
```

Zvládneš v této funkci nový text přidat ke starému,
aby program fungoval jako jednoduchý textový editor?

{% filter solution %}
```python
@window.event
def on_text(text):
    label.text = label.text + text
```
{% endfilter %}


## Další událostí

Na jaké další události se dá reagovat?
Všechny jsou popsané v [dokumentaci Pygletu](https://pyglet.readthedocs.io/en/latest/modules/window.html#pyglet.window.Window.on_activate).
Tady uvádím pár zajímavých.

### Stisk klávesy

Klávesy, které nezadávají text (šipky, <kbd>Backspace</kbd> nebo
<kbd>Enter</kbd>, atp.) se dají rozpoznat v události `on_key_press`.

Funkce `on_key_press` má dva argumenty: první je kód klávesy,
který můžeš porovnat s konstantou z [pyglet.window.key](https://pyglet.readthedocs.io/en/latest/modules/window_key.html#key-constants).
Druhý určuje stisknuté modifikátory jako <kbd>Shift</kbd> nebo <kbd>Ctrl</kbd>.

``` python
@window.event
def on_key_press(key_code, modifier):
    if key_code == pyglet.window.key.BACKSPACE:
        label.text = label.text[:-1]

    if key_code == pyglet.window.key.ENTER:
        print('Zadaná zpráva:', label.text)
        window.close()
```

Na macOS budeš možná muset zaměňit `BACKSPACE` za `DELETE`. {# XXX: je to tak? #}
(Nebo si doma nastuduj [způsob](https://pyglet.readthedocs.io/en/latest/programming_guide/keyboard.html#motion-events), jak to dělat automaticky a správně.)


### Kliknutí myši

Při obsluze události `on_mouse_press` dostaneš informace o pozici
kliknutí (<var>x</var>-ovou a <var>x</var>-ovou souřadnici)
a navíc informaci o stisknutém tlačítku myši a modifikátoru.

Takhle se třeba popisek přesune na místo kliknutí:

```python
@window.event
def on_mouse_press(x, y, button, modifier):
    label.x = x
    label.y = y
```


## Celý program

Pro případ, že by ses ztratil{{a}} nebo nevěděla,
kam který kousek kódu patří, uvádím výsledný ukázkový program.

```python
import pyglet
window = pyglet.window.Window()
label = pyglet.text.Label("Ahoj!", x=10, y=20)


@window.event
def on_draw():
    window.clear()
    label.draw()


@window.event
def on_text(text):
    label.text = label.text + text


@window.event
def on_key_press(key_code, modifier):
    if key_code == pyglet.window.key.BACKSPACE:
        label.text = label.text[:-1]

    if key_code == pyglet.window.key.ENTER:
        print('Zadaná zpráva:', label.text)
        window.close()


@window.event
def on_mouse_press(x, y, button, modifier):
    label.x = x
    label.y = y


pyglet.app.run()
```

