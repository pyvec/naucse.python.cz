GUI v Pythonu: PyQt5
====================

Způsobů, jak dělat v Pythonu aplikace s GUI, je mnoho. Dá se použít zabudovaný, ale ošklivý Tkinter, nebo nějaký externí framework.

V tomto cvičení budeme používat framework Qt, protože je multiplatformní, používá se i v jiných oblastech, než je Python,
je dostatečně robustní a (například na rozdíl od GTK3) nemění API téměř s každou vydanou verzí.

Pomocí aplikace Qt Designer se dá navíc základní kostra GUI poměrně jednoduše *naklikat*, takže není nutné psát layout aplikace v kódu.

Instalace
---------

Na tomto cvičení budete potřebovat balíček PyQt5 a aplikaci Qt5 Designer.
Pokud budete používat svůj počítač, prosíme vás o instalaci již předem, na cvičení toho bude opravdu hodně a nemůžeme si dovolit plýtvat časem.

### PyQt5

Pokud máte Python 3.5 a jednu z platforem, pro které je připraven [wheel na PyPI](https://pypi.python.org/pypi/PyQt5), stačí udělat:

    python -m pip install --upgrade pip
    python -m pip install PyQt5

Pro starší verzi Pythonu nebo 32bitový Linux to ale nebude fungovat.
V takovém případě můžete PyQt5 zkusit najít v balíčkovacím systému vaší distribuce (např. balíček `python3-qt5` ve Fedoře nebo `python3-pyqt5` v Debianu).
Virtualenv pak může vytvořit s přepínačem `--system-site-packages`, který zajistí, že i z virtualenvu uvidíte PyQt5 nainstalované z distribučního balíčku.

Pokud nic z toho nepomůže, můžete zkusit přeložit PyQt5 ze [zdrojových souborů](https://www.riverbankcomputing.com/software/pyqt/download5)
([návod](http://pyqt.sourceforge.net/Docs/PyQt5/installation.html#building-and-installing-from-source)).

*První aplikace* níže by vám měla fungovat.

Pokud narazíte na chybu `Could not find or load the Qt platform plugin "xcb"`, podívejte se do [naší issue](https://github.com/cvut/MI-PYT/issues/57).

### Qt5 Designer

Na Linuxu najdete Qt5 Designer v balíčkách, třeba `qt5-designer` na Fedoře nebo `qttools5-dev-tools` na Debianu.

Na Windows (i na Macu) si můžete [stáhnout] instalátor Qt 5, který (doufáme) nainstaluje i Designer.

[stáhnout]: https://www.qt.io/download-open-source/#section-2

Pokud používáte na Macu `homebrew`, můžete to udělat i takto:

    brew install qt5
    brew linkapps qt5

### Numpy

Do virtuálního prostředí s PyQt5 si nainstalujte in NumPy:

    python -m pip install numpy


První aplikace
--------------

Napište si první aplikaci, ať vidíte jak kód v PyQt vypadá.
Detaily toho, jak to funguje, si ukážeme později.

```python
from PyQt5 import QtWidgets

app = QtWidgets.QApplication([])

button = QtWidgets.QPushButton("Click to Exit")
button.setWindowTitle("Goodbye World")
button.clicked.connect(app.quit)

button.show()

app.exec()
```


O Qt, PyQT a PySide
-------------------

[Qt](https://www.qt.io/) je aplikační framework napsaný v C++, který zjednodušuje psaní multiplatformních aplikací (od počítačů s Linuxem, Mac OS či Windows po různá vestavěná zařízení).

[PyQt](https://riverbankcomputing.com/software/pyqt) je knihovna, která umožňuje použít Qt z Pythonu.
Na rozdíl od samotného Qt je licencovaná pod [GNU GPL v3](https://www.gnu.org/licenses/gpl-3.0.en.html), která (stručně řečeno) vyžaduje, že programy napsané s použitím PyQt byly šířeny pod stejnou licencí a se zdrojovým kódem.
Tedy: kdokoliv, kdo dostane kopii programu, musí mít možnost dostat odpovídající zdrojový kód, a má možnost tento kód dál šířit pod stejnou licencí.

Pokud by se vám tato licence nelíbila, je možnost použít [PySide](https://wiki.qt.io/PySide), které má permisivnější licenci a téměř stejné API jako PyQt, ale není tak stabilní.

### Moduly Qt

Qt je rozděleno na několik tzv. [modulů](http://doc.qt.io/qt-5/qtmodules.html).
Pro grafická uživatelská rozhraní (GUI), kterými se budeme zabývat, použijeme hlavně [QtGui] a [QtWidgets].

Dále je tu modul [QtCore], který obsahuje mj. základní datové typy jako QString a QList (které PyQt
automaticky převádí na pythonní ekvivalenty a zpět), nebo třeba [QRect](http://doc.qt.io/qt-5/qrect.html) – abstraktní obdélník.

Další moduly jsou nadstavby od [vykreslování SVG][QtSVG] nebo [práci s multimédii][QtMultimedia] (které se můžou hodit) po
třeba práci s [SQL][QtSQL] a [XML][QtXML] nebo [síťovou komunikaci][QtNetwork], kde je pro Python pohodlnější použít jiné knihovny.

[QtGui]: http://doc.qt.io/qt-5/qtgui-index.html
[QtWidgets]: http://doc.qt.io/qt-5/qtwidgets-index.html
[QtCore]: http://doc.qt.io/qt-5/qtcore-index.html
[QtSVG]: http://doc.qt.io/qt-5/qtsvg-index.html
[QtMultimedia]: http://doc.qt.io/qt-5/qtmultimedia-index.html
[QtSQL]: http://doc.qt.io/qt-5/qtsql-index.html
[QtXML]: http://doc.qt.io/qt-5/qtxml-index.html
[QtNetwork]: http://doc.qt.io/qt-5/qtnetwork-index.html


Specifika PyQt
--------------

Ačkoli se Qt dá použít z Pythonu, bohužel zjistíte, že ne všechno funguje a vypadá tak, jako kdyby to byla knihovna od základů napsaná pro Python.
Tady jsou některé zvláštnosti, na které se můžete připravit.

### Jména a dokumentace

Qt pojmenovává funkce, metody a atributy konvencí `camelCase`, místo pythonistického `snake_case`.
PyQt tuto konvenci nemění: je užitečnější používat identická jména, a kromě toho knihovna PyQt vznikla ještě před PEP 8.

Hledáte-li dokumentaci, doporučuji zadat do vyhledávače "qt5 <hledaný objekt>".
Dostanete se tak na dokumentaci pro C++ (např. [QObject](http://doc.qt.io/qt-5/qobject.html)).
Hledáte-li "pyqt5 <hledaný objekt>", dostanete se k dokumentaci pro Python, která ale většinou jen odkazuje
na verzi pro C++ (např. [pro QObject](http://pyqt.sourceforge.net/Docs/PyQt5/api/qobject.html)).

Rozdíly mezi C a pythonní verzí jsou většinou intuitivní (např. None místo NULL), ale jsou popsány
v [dokumentaci PyQt](http://pyqt.sourceforge.net/Docs/PyQt5/index.html).

### Atributy

Qt zásadně používá pro přístup k atributům objektů funkce.
Funkce pro čtení se typicky jmenuje podle atributu, funkce pro nastavení má předponu `set`.
Namísto pythonního `c = obj.color` a `obj.color = ...` tedy použijeme `c = obj.color()` a `obj.setColor(...)`.

### Správa paměti

Python a C++/Qt mají, bohužel, rozdílný přístup ke správě paměti.
Python používá *reference counting* a *garbage collection*.
C++ má objekty s destruktory, což Qt zjednodušuje (alespoň pro C++) *stromem vlastnictví*.

Základní třída v Qt, ze které dědí téměř všechny ostatní, je QObject.
Ten má seznam potomků (children), o které se „stará“, a když uvolníme rodiče, uvolní se rekurzivně i všichni potomci.
Z Pythonu pak můžeme dostat chybu `wrapped C/C++ object has been deleted`.
Jinak ale kombinace QObject a pythonních objektů funguje dobře.

Větší problémy můžou nastat s pomocnými objekty, které nedědí z QObject, a nemají potřebné „dynamické“ vlastnosti.
Takový objekt doporučujeme používat jen v rámci jedné funkce (t.j. neukládat si ho jinde), pokud si nejste jistí že
ho „nevlastníte“ i ve smyslu C++/Qt.

Občase se stane, že program spadne pro chybu jako nepovolený přístup do paměti.
Bez hlubší znalosti Qt a PyQt se taková chyba odstraňuje poměrně těžko, ale vaše znalosti C++ (z jiných kurzů)
a CPython C API (z minula) vám v tom pomůžou.
Doporučujeme dělat malé commity a psát jednoduchý kód.

### Smyčka událostí, signály a sloty

Qt funguje na principu smyčky událostí (event loop).
Metoda `QApplication.exec` obsahuje v podstatě nekonečnou smyčku, která čeká na externí události (klik myši,
žádost OS o vykreslení okna, atd.), a na jejich základě volá příslušné funkce – ať už interní
nebo námi definované.

Pro komunikaci mezi objekty v rámci aplikace pak Qt používá mechanismus *signálů a slotů* (variantu *observer pattern*).
Signál je vyslán (*emitted*) při události jako kliknutí na tlačítko, výběr položky z menu, zavření okna atp.
K signálu může být připojeno několik slotů, což jsou funkce, které se po vyslání signálu zavolají.
Kód který vysílá signál obecně neví o tom, kolik slotů je připojeno (a jsou-li nějaké).

V C++ jsou signály a sloty vždy staticky nadefinované na nějaké třídě, která dědí z `QObject`.
V PyQt takto musí být nadefinovány jen signály; za slot poslouží jakákoli pythonní funkce.

V příkladu výše jsme připojili signál `clicked` tlačítka na slot `quit` aplikace.
Stejně bychom mohli připojit jakoukoli funkci/metodu, která bere správný počet argumentů – v následujícím případě nula:

```python
    button.clicked.connect(lambda: print('Exiting program'))
```

V C++ je časté přetěžování funkcí (včetně signálů), což Pythonistům občas ztěžuje život.
PyQt většinou automaticky vybere variantu signálu podle připojené funkce, ale ne vždy je to možné.

Ukažme si to na následujícím kódu, který napojuje funkci `print` na dvě varianty signálu [QComboBox.activated].
Ten se vyšle při výběru položky ze seznamu buď jako `QComboBox.activated[int]`, kdy předává index vybrané položky,
nebo jako `QComboBox.activated[str]`, kdy předává text položky:

```python
from PyQt5 import QtWidgets

app = QtWidgets.QApplication([])

# QComboBox - políčko pro výběr z několika možností
box = QtWidgets.QComboBox()
box.addItem('First Option')
box.addItem('Second Option')

# Základní varianta napojí na activated[int]
box.activated.connect(print)

# Výběr varianty signálu pomocí hranatých závorek
box.activated[str].connect(print)
box.activated[int].connect(print)

box.show()

app.exec()
```

[QComboBox.activated]: http://doc.qt.io/qt-5/qcombobox.html#activated


Skládání GUI
------------

Základní způsob, jak v Qt vytvářet grafické rozhraní, je skládání funkčních prvků (*widgets*) do
hierarchie oken, skupin a panelů.

Základní třída pro funkční prvky, [QWidget], dědí z už zmíněného `QObject`.
Každý QObject může obsahovat potomky (children), a v případě QWidget se potomci vykreslují
jako součást svého rodiče.
Navíc může mít každý widget tzv. *layout*, který určuje pozici a velikost widgetů, které jsou
do něj přidané.

Ukažme to v kódu:

```python
from PyQt5 import QtWidgets

app = QtWidgets.QApplication([])

# Hlavní okno
main = QtWidgets.QWidget()
main.setWindowTitle('Hello Qt')

# Layout pro hlavní okno
layout = QtWidgets.QHBoxLayout()
main.setLayout(layout)

# Nápis
label = QtWidgets.QLabel('Click the button to change me')
# Přidáním do layoutu se nápis automaticky stane potomkem hlavního okna
layout.addWidget(label)

# Tlačítko
button = QtWidgets.QPushButton('Click me')
layout.addWidget(button)

# Funkcionalita
def change_label():
    label.setText('Good job. +100 points.')

button.clicked.connect(change_label)

# Spuštění
main.show()
app.exec()
```

Zabudovaných [layoutů][layout-gallery] i [widgetů][widget-gallery] existuje spousta, jednodušší
programy stačí „poskládat“ z nich a napojit je na logiku.
Pro složitější programy jsou pak možnosti, jak si widgety přizpůsobit.

[QWidget]: http://doc.qt.io/qt-5/qwidget.html
[layout-gallery]: http://doc.qt.io/qt-5/layout.html#horizontal-vertical-grid-and-form-layouts
[widget-gallery]: http://doc.qt.io/qt-5/gallery-fusion.html


Qt Designer
-----------

Vytvářet GUI v kódu je poměrně neefektivní, a tak existuje nástroj, kde si okna můžeme „naklikat“.
Jmenuje se Qt Designer, a měli byste ho mít nainstalovaný.
Na školních počítačích se spouští příkazem `designer -qt=5`.

Spustíme Designer a vytvoříme v něm nové *Main Window*.
Do něj si z palety přidáme *Scroll Area* a doprava vedle něj *List Widget*.
Poté aplikujeme layout: na volnou plochu okna klikneme pravým tlačítkem a vybereme *Lay Out ‣ Horizontally*.
(Dá se to udělat i tlačítkem v liště.)

Pomocí <kbd>Ctrl</kbd>+<kbd>R</kbd> lze zkontrolovat, jak okno vypadá a jak reaguje na změny velikosti.

Potom přidáme položku do menu: místo *Type Here* napíšeme *Map*, a pod něj podobně přidáme položky *New* a *Quit*.

V panelu *Property Editor* jde měnit vlastnosti jednotlivých prvků.
U skrolovacího okna nastavíme *objectName* na *scrollArea*.
U *ListWidget* nastavíme *objectName* na *palette* a *sizePolicy ‣ Horizontal* na *Preferred*.
V panelu *ActionEditor* najdeme položky pro *New* a *Quit* a nastavíme jim *objectName* na *actionNew*, resp. *actionQuit*.

Potom přes pravé tlačítko na nevyužité ploše okna přidáme lištu nástrojů (*Add Toolbar*) a z panelu
*Action Editor* do něj akci *actionQuit* přetáhnéme.

Pomocí <kbd>Ctrl</kbd>+<kbd>R</kbd> opět zkontrolujeme, jak okno vypadá, a jak po nastavení *sizePolicy* reaguje na změny velikosti .

V Designeru jde i napojovat signály. V panelu *Signal/Slot Editor* přidáme tento řádek:

    Sender: actionQuit
    Signal: triggered()
    Receiver: MainWindow
    Slot: close()

Pomocí <kbd>Ctrl</kbd>+<kbd>R</kbd> jde ověřit, že zavírání okna funguje.

Návrh okna uložíme do souboru `mainwindow.ui`.

Soubor s návrhem jde převést na pythonní zdrojový soubor pomocí programu `pyuic5`, nebo
ho vždy načíst přímo z programu.
My použijeme druhou variantu, je však dobré o `pyuic5` vědět, kdybyste někdy potřebovali
základ pro vytváření UI v kódu (např. na vytvoření sady několika podobných tlačítek v cyklu).

Načíst `.ui` soubor z programu do předpřipraveného okna `QMainWindow` lze pomocí funkce [uic.loadUi]:


```python
from PyQt5 import QtWidgets, uic

def main():
    app = QtWidgets.QApplication([])

    window = QtWidgets.QMainWindow()

    with open('mainwindow.ui') as f:
        uic.loadUi(f, window)

    window.show()

    return app.exec()

main()
```

[uic.loadUi]: http://pyqt.sourceforge.net/Docs/PyQt5/designer.html#the-uic-module


Vlastní widget - Grid
---------------------

Nejprve si vyrobíme vlastní *widget*, který bude sloužit k vizualizaci bludiště.
Zde na cvičení bude zobrazovat jen trávu a stěny, pro splnění úkolu toho ale musí umět víc.

Velikost widgetu se zadává v pixelech. Musíme ho udělat dostatečně velký, aby se do něj vešla všechna políčka bludiště.
Velikost jednoho políčka v pixelech zvolíme pro jednoduchost konstantou.

Souřadnice v Qt jsou v pixelech ve formě `(x, y)` – klasicky jak jsme zvyklí, `x` je horizontální souřadnice –
kdežto matice je uložená jako po políčkách `(řádek, sloupec)`.
Abychom se v tom neztratili, je dobré hned ze začátku udělat funkce pro převod mezi souřadnými systémy,
a důsledně rozlišovat `(x, y)` vs. `(row, column)`.

```python
CELL_SIZE = 32


def pixels_to_logical(x, y):
    return y // CELL_SIZE, x // CELL_SIZE


def logical_to_pixels(row, column):
    return column * CELL_SIZE, row * CELL_SIZE


class GridWidget(QtWidgets.QWidget):
    def __init__(self, array):
        super().__init__()  # musíme zavolat konstruktor předka
        self.array = array
        # nastavíme velikost podle velikosti matice, jinak je náš widget příliš malý
        size = logical_to_pixels(*array.shape)
        self.setMinimumSize(*size)
        self.setMaximumSize(*size)
        self.resize(*size)
```

`GridWidget` vložíme do `QScrollArea`, kterou jsme si vytvořili v Qt Designeru:

```python
import numpy

    ...

    # bludiště zatím nadefinované rovnou v kódu
    array = numpy.zeros((15, 20), dtype=numpy.int8)
    array[:, 5] = -1  # nějaká zeď

    # získáme oblast s posuvníky z Qt Designeru
    scroll_area = window.findChild(QtWidgets.QScrollArea, 'scrollArea')

    # dáme do ní náš grid
    grid = GridWidget(array)
    scroll_area.setWidget(grid)

    ...
```

Po spuštění aplikace zatím nic nového neuvidíte, maximálně se trochu změní posuvníky.
Potřebujeme ještě zařídit, aby se data z matice vykreslovala do gridu.
Nejlepší je vykreslovat, kdykoliv nás OS (nebo Qt) vyzve, že potřebuje kus okna překreslit:
při prvním zobrazení, odminimalizování okna, ukázání nové části bludiště přes scrollování.
Také je zbytečně vykreslovat obrázky mimo oblast, která je vidět na obrazovce.

K tomuto účelu nám poslouží událost (*event*).
Jak bylo řečeno v úvodu, na rozdíl od signálů a slotů, které zajišťují komunikaci v rámci aplikace,
události vznikají mimo aplikaci.
Jde například o kliknutí myší ([mouse*Event][mouseEvent]), vstup z klávesnice ([key*Event][keyEvent]),
nebo právě žádost OS o překreslení okna ([paintEvent]).
Na poslední jmenovanou událost, `paintEvent`, teď budeme reagovat.

Události se obsluhují předefinováním příslušné metody, která jako argument bere objekt popisující
danou událost.

V rámci reakce na událost `paintEvent` můžeme používat [QPainter], objekt, který generalizuje kreslení
na různé „povrchy“ jako widgety, obrázky, nebo i instrukce pro tiskárnu.

```python
from PyQt5 import QtWidgets, QtGui, QtCore, uic


class GridWidget(QtWidgets.QWidget):

    ...

    def paintEvent(self, event):
        rect = event.rect()  # získáme informace o překreslované oblasti

        # zjistíme, jakou oblast naší matice to představuje
        # nesmíme se přitom dostat z matice ven
        row_min, col_min = pixels_to_logical(rect.left(), rect.top())
        row_min = max(row_min, 0)
        col_min = max(col_min, 0)
        row_max, col_max = pixels_to_logical(rect.right(), rect.bottom())
        row_max = min(row_max + 1, self.array.shape[0])
        col_max = min(col_max + 1, self.array.shape[1])

        painter = QtGui.QPainter(self)  # budeme kreslit

        for row in range(row_min, row_max):
            for column in range(col_min, col_max):
                # získáme čtvereček, který budeme vybarvovat
                x, y = logical_to_pixels(row, column)
                rect = QtCore.QRectF(x, y, CELL_SIZE, CELL_SIZE)

                # šedá pro zdi, zelená pro trávu
                if self.array[row, column] < 0:
                    color = QtGui.QColor(115, 115, 115)
                else:
                    color = QtGui.QColor(0, 255, 0)

                # vyplníme čtvereček barvou
                painter.fillRect(rect, QtGui.QBrush(color))

```


[mouseEvent]: http://doc.qt.io/qt-5/qwidget.html#mousePressEvent
[keyEvent]: http://doc.qt.io/qt-5/qwidget.html#keyPressEvent
[paintEvent]: http://doc.qt.io/qt-5/qwidget.html#paintEvent
[QPainter]: http://doc.qt.io/qt-5/qpainter.html

Nyní by již bludiště mělo být v okně vidět barevně.

### Obrázky

Protože barvičky jsou příliš nudné, přidáme do bludiště obrázky.

Veškerou ke cvičení i k úkolu potřebnou grafiku najdete na [GitHubu](https://github.com/cvut/MI-PYT/tree/master/tutorials/09-qt/pics).
Je k dispozici pod public domain (tj. „dělej si s tím, co chceš“), pochází ze studia [Kenney],
a je (společně se další volně licencovanou grafikou) ke stažení z [OpenGameArt.org].

[Kenney]: http://kenney.nl/
[OpenGameArt.org]: http://opengameart.org/users/kenney

Nejprve si načteme SVG soubory jako objekty `QSvgRenderer`:

```python
from PyQt5 import QtWidgets, QtCore, QtGui, QtSvg, uic

SVG_GRASS = QtSvg.QSvgRenderer('grass.svg')
SVG_WALL = QtSvg.QSvgRenderer('wall.svg')
```

A poté je na správných místech vyrendrujeme:

```python
                ...
                rect = QtCore.QRectF(x, y, CELL_SIZE, CELL_SIZE)

                # podkladová barva pod poloprůhledné obrázky
                white = QtGui.QColor(255, 255, 255)
                painter.fillRect(rect, QtGui.QBrush(white))

                # trávu dáme všude, protože i zdi stojí na trávě
                SVG_GRASS.render(painter, rect)

                # zdi dáme jen tam, kam patří
                if self.array[row, column] < 0:
                    SVG_WALL.render(painter, rect)
```

* [grass.svg](https://raw.githubusercontent.com/cvut/MI-PYT/master/tutorials/09-qt/pics/grass.svg)
* [wall.svg](https://raw.githubusercontent.com/cvut/MI-PYT/master/tutorials/09-qt/pics/wall.svg)


Model/View
----------

Nyní trochu odbočíme a povíme si krátce o dalším podsystmému Qt: o modelech.

Qt obsahuje framework, který mapuje informace do podoby tabulek, seznamů, nebo obecných stromů.
Vzniklé modely se potom dají zobrazit ve specializovaných widgetech.

Samotná data můžou být uložena kdekoli – v paměti, SQL databázi, souborech a podobně.
Dokonce nemusí být všechna dostupná: existuje vestavěný model pro souborový systém,
který se dá zobrazit aniž by se procházely všechny soubory.
Když je informace potřeba, model se postará o její načtení.

Pomocí modelů a modelových widgetů lze informace i měnit, a pokud je model
zobrazen ve více widgetech zároveň, změny se projeví ve všech.

Obecné modely je bohužel relativně obtížné implementovat v Pythonu, protože používají třídy,
které nedědí z QObject, takže je potřeba sledovat, jestli je „vlastní“ Python nebo C++.

Naštěstí ale existují widgety se zabudovanými modely, které obsahují i samotná data.
Tyto modely je složitější napojit na existující aplikační logiku, ale pro většinu účelů postačí.

O obecných modelech si můzete přečíst v [dokumentaci](http://doc.qt.io/qt-5/model-view-programming.html).


QListWidget - Paleta
--------------------

Jeden z widgetů se zabudovaným modelem je `QListWidget`, který umí spravovat a zobrazovat
nějaký seznam.
My jsme si v Qt Designeru připravili `QListWidget` s názvem `palette`, který použijeme
jako paletu jednotlivých dílků, které budeme moci vkládat do bludiště.
Položky se do tohoto modelu přidávají následovně:

```python
def main():
    ...

    # získáme paletu vytvořenou v Qt Designeru
    palette = window.findChild(QtWidgets.QListWidget, 'palette')

    item = QtWidgets.QListWidgetItem('Grass')  # vytvoříme položku
    icon = QtGui.QIcon('grass.svg')  # ikonu
    item.setIcon(icon)  # přiřadíme ikonu položce
    palette.addItem(item)  # přidáme položku do palety
```

Stejným způsobem lze do palety přidat další položky: kromě trávy budeme na toto
cvičení potřebovat i stěnu.
Protože v úkolu bude položek více, je lepší si na to vytvořit funkci či metodu.
To necháme na vás.

Zatím jsme vytvořili paletu, ve které uživatel může položky vybírat.
Výběr položky aktivuje signál `itemSelectionChanged`, na který můžeme
navázat volání funkce.
(Pokud bychom měli pod kontrolou třídu widgetu, jako tomu je u třídy `Grid`,
mohli bychom místo toho i předefinovat metodu `itemSelectionChanged()`.)

```python
def main():
    ...

    def item_activated():
        """Tato funkce se zavolá, když uživatel zvolí položku"""

        # Položek může obecně být vybráno víc, ale v našem seznamu je to
        # zakázáno (v Designeru selectionMode=SingleSelection).
        # Projdeme "všechny vybrané položky", i když víme že bude max. jedna
        for item in palette.selectedItems():
            row_num = palette.indexFromItem(item).row()
            print(row_num)

    palette.itemSelectionChanged.connect(item_activated)

```

Nyní, když uživatel zvolí položku, vypíše se do konzole její pořadí.
Nás by ale spíš zajímalo, jak bude tato položka reprezentována v matici s bludištěm.
K položce v paletě můžeme uložit informace pomocí `item.setData(<role>, <data>)`.
Rolí pro informace je [spousta][roles], a několik z nich Qt používá pro vykreslování.
Pro vlastní data můžeme použít `QtCore.Qt.UserRole`.
V případě potřeby ukládat více dat můžeme dále zvolit `QtCore.Qt.UserRole + 1` atd.
Pro případ, že budeme potřebovat rolí víc, je dobré si je vhodně pojmenovat.

[roles]: http://doc.qt.io/qt-5/qt.html#ItemDataRole-enum

```python

VALUE_ROLE = QtCore.Qt.UserRole

def main():
    ...
    self.palette.addItem(item)  # přidáme položku do palety
    item.setData(VALUE_ROLE, -1)  # přiřadíme jí data
    ...

    def item_activated():
        for item in palette.selectedItems():
            print(item.data(VALUE_ROLE))  # čteme data stejné role z položky
```

Nyní byste měli mít v paletě trávu a stěnu s patřičnými čísly (`0` a `-1`), které se vypisují do konzole při zvolení položky.

Nakonec si číslo místo vypisování uložíme do gridu, abychom ho mohli později použít.

```python
    def item_activated():
        for item in palette.selectedItems():
            grid.selected = item.data(QtCore.Qt.UserRole)
```

Klikání do gridu
----------------

Nyní nezbývá nic jiného, než pomocí klikání nanášet zvolené dílky do bludiště.
K tomu opět použijeme událost, tentokrát událost kliknutí, tedy `mousePressEvent`.

```python
class GridWidget(QtWidgets.QWidget):
    ...

    def mousePressEvent(self, event):
        # převedeme klik na souřadnice matice
        row, column = pixels_to_logical(event.x(), event.y())

        # Pokud jsme v matici, aktualizujeme data
        if 0 <= row < self.array.shape[0] and 0 <= column < self.array.shape[1]:
            self.array[row, column] = self.selected

            # tímto zajistíme překreslení widgetu v místě změny:
            # (pro Python 3.4 a nižší volejte jen self.update() bez argumentů)
            self.update(*logical_to_pixels(row, column), CELL_SIZE, CELL_SIZE)
```

Poznámka: Zde víme, že kliknutí může změnit vykreslené bludiště pouze v místě kliknutí.
V úkolu ale bude možné, že kliknutí někam změní vykreslení bludiště někde jinde,
proto bude lepší zavolat `self.update()` bez argumentů, a říct tak systému že se má překreslit celý widget.

Protože po spuštění aplikace není zvolena žádná položka a `self.selected` není definován, je rozumné prostě nějakou položku zvolit:

```python
# Za přidáním položek do palety a napojení signálu
palette.setCurrentRow(1)
```

### Více tlačítek myši

Můžete si vyzkoušet, že bludiště se mění při použití jakéhokoliv tlačítka myši.
Je to proto, že `mousePressEvent` se stane, kdykoli na widgetu stiskneme libovolné tlačítko.
Pokud bychom chtěli řešit pouze levé (primární) tlačítko, můžeme zjistit, které tlačítko událost vyvolalo:

```python
            if event.button() == QtCore.Qt.LeftButton:
                self.array[row, column] = self.selected
            else:
                return
            self.update(*logical_to_pixels(row, column), CELL_SIZE, CELL_SIZE)
```

Na pravé tlačítko myši můžeme namapovat funkci mazání:

```python
            elif event.button() == QtCore.Qt.RightButton:
                self.array[row, column] = 0
```

### Tažení myši

Pro splnění úkolu bude stačit objekty mazat a klást pomocí klikání na jednotlivá políčka.
Pokud však chcete poskytnout uživateli větší komfort, prozkoumejte další [události]
a můžete políčka nanášet/mazat i při kliknutí a táhnutí.
(Možná tu narazíte na problém, kdy se při příliš rychlém pohybu myši generují události
pro body příliš daleko od sebe.
Když program nestíhá, OS nebo Qt spojuje víc událostí pohybu myši dohromady a posílá
jen jednu poslední.
Jednotlivé body můžete spojit čárou pomocí knihovny [bresenham].)

[události]: http://doc.qt.io/qt-5/qwidget.html
[bresenham]: https://pypi.python.org/pypi/bresenham

Menu a modální dialog
---------------------

Naše aplikace bude umět vytvořit nové, prázdné bludiště.
Ukážeme si, jak vytvořit modální dialog pro volby (šířka a výška nového bludiště).
„Modální dialog“ znamená okno, které musí uživatel zavřít, než může pracovat se zbytkem aplikace.

Layout okna nejprve naklikáme v Qt Designeru:

 1. Po spuštění zvolíme *Dialog with Buttons Bottom* a *Create*.
 2. Přes pravé tlačítko pro dialog zvolíme *Lay Out ‣ Vertically*.
 3. Nad tlačítka *Cancel* a *OK* přetáhneme z *Widet Box* *Form Layout* (layouty lze takto přímo vnořovat).
 4. Do něj přetáhneme postupně dvakrát *Label* a *Spin Box*, abychom vytvořili formulář.
 5. Přejmenujeme v panelu *Property Editor* jednotlivé přidané položky tak, aby dávaly v kódu smysl (`widthBox`, `heightBox`).
 6. Poklikáním na *Labely* změníme jejich text.
 7. Nastavíme v panelu *Property Editor* rozumné limity a výchozí hodnoty pro *Spin Boxy*.
 8. Okno případně zmenšíme, aby nebylo zbytečně velké.
 9. V menu zvolíme *Edit ‣ Edit Buddies* a táhnutím z *Labelu* na *Spin Box* nastavíme, ke kterému prvku se *Label* vztahuje.
 10. V menu zvolíme *Edit ‣ Edit Tab Order* a zkontrolujeme, že pořadí ve kterém bude prvky vybírat klávesa `Tab` je rozumné.
 11. Můžeme se vrátit zpět na *Edit ‣ Edit Widgets*.
 12. Dialog uložíme jako `newmaze.ui`.

Poté připravíme funkci pro zobrazení dialogu a pro jeho vyhodnocení:

```python
def new_dialog(window, grid):
    # Vytvoříme nový dialog.
    # V dokumentaci mají dialogy jako argument `this`;
    # jde o "nadřazené" okno
    dialog = QtWidgets.QDialog(window)

    # Načteme layout z Qt Designeru
    with open('newmaze.ui') as f:
        uic.loadUi(f, dialog)

    # Zobrazíme dialog.
    # Funkce exec zajistí modalitu (tj.  tzn. nejde ovládat zbytek aplikace,
    # dokud je dialog zobrazen), a vrátí se až potom, co uživatel dialog zavře.
    result = dialog.exec()

    # Výsledná hodnota odpovídá tlačítku/způsobu, kterým uživatel dialog zavřel.
    if result == QtWidgets.QDialog.Rejected:
        # Dialog uživatel zavřel nebo klikl na Cancel
        return

    # Načtení hodnot ze SpinBoxů
    w = dialog.findChild(QtWidgets.QSpinBox, 'widthBox').value()
    h = dialog.findChild(QtWidgets.QSpinBox, 'heightBox').value()

    # Vytvoření nového bludiště
    grid.array = numpy.zeros((h, w), dtype=numpy.int8)

    # Bludiště může být jinak velké, tak musíme změnit velikost Gridu;
    # (tento kód používáme i jinde, měli bychom si na to udělat funkci!)
    size = logical_to_pixels(h, w)
    grid.setMinimumSize(*size)
    grid.setMaximumSize(*size)
    grid.resize(*size)

    # Překreslení celého Gridu
    grid.update()


def main():
    ...


     # Napojení signálu actionNew.triggered

    action = window.findChild(QtWidgets.QAction, 'actionNew')
    action.triggered.connect(lambda: new_dialog(window, grid))
```

Další dialogy, které budeme potřebovat, jsou tak rozšířené (a mezi jednotlivými platformami tak různé),
že je Qt má předpřipravené.
Jsou to dialogy pro ukázání hlášky, výběr souboru, barvy nebo fontu, nebo pro nastavení tisku.

Tyto předpřipravené dialogy mají typicky statické metody, které dialog vytvoří a přímo zavolají
`exec()` a vrátí výsledek.

Pro splnění úkolu (dalších položek v menu) se vám můžou hodit tyto dialogy:

 * [QtWidgets.QFileDialog.getOpenFileName](http://doc.qt.io/qt-5/qfiledialog.html#getOpenFileName)
 * [QtWidgets.QFileDialog.getSaveFileName](http://doc.qt.io/qt-5/qfiledialog.html#getSaveFileName)
 * [QtWidgets.QMessageBox.critical](http://doc.qt.io/qt-5/qmessagebox.html#critical)
 * [QtWidgets.QMessageBox.about](http://doc.qt.io/qt-5/qmessagebox.html#about)
   * Tip: Do *QMessageBoxu* jde dávat i HTML (ale v řetězci s ním nesmí být zalomeny řádky, jinak to nefunguje)
   * Tip: Když hlavnímu oknu aplikace nastavíte ikonu (`setWindowIcon(icon)`), v *About* dialogu bude automaticky vidět


Třída pro GUI aplikace
----------------------

Funkce `main` se nám pomalu rozrůstá, a další funkce, které volá, musí být buď definované v ní (jako `item_activated`)
nebo musí brát relativně hodně argumentů (jako `new_dialog`).
Abychom si zjednodušili práci, můžeme logiku místo do funkce dát do třídy, ve které si důležité prvky
uložíme do atributů (`self.grid`, `self.window`, `self.app`, atd.).
Doporučujeme udělat přípravu v `__init__`, a volání `window.show()` a `return app.exec()` dát do metody `run`.


Úkol
====

Vaším úkolem za 5 bodů je vytvořit pomocí PyQt5 grafické uživatelské rozhraní,
které umožní vizualizovat a editovat bludiště.
Můžete samozřejmě vyjít z práce na cvičení, ale zbývá toho poměrně dost dodělat.
Rozhraní umožní:

* vytvářet nové bludiště zadaných rozměrů (prázdné, náhodně generované apod., jak chcete)
    * generování náhodného bludiště však musí trvat snesitelně dlouho, v případě nutnosti si vypomožte Cythonem
* ukládat a načítat bludiště ve formě NumPy matic do/ze souborů dle volby uživatele
    * pokud se to nepovede, musí aplikace zobrazit chybové hlášení v grafické podobě (tj. ne jen do konzole)
    * formát souborů viz níže
* prohlížet bludiště v grafické podobě
    * včetně všech objektů v něm a vizualizace cest (viz níže)
    * pokud se bludiště celé nevejde do okna, musí mít posuvníky (jako na cvičení)
    * zoom (např. <kbd>Ctrl</kbd> + kolečko myši) není nutný, ale je příjemný
* klást do bludiště objekty (zdi, cíle, postavy) a odebírat je (tyto změny se projeví v paměti na úrovni NumPy matice)
* automaticky zobrazovat cesty mezi postavami a cílem
* nabídka *Help ‣ About* vyvolá okno s informacemi o aplikaci:
    * název
    * stručný popis
    * autor/autoři (vy, případně i my, pokud používáte náš kód)
    * odkaz na repozitář
    * informace o licenci
    * pokud používáte public domain grafiku z [OpenGameArt.org], nemáte právní povinnost zdroj zmínit, ale považujeme to za slušnost

Veškerou potřebnou grafiku najdete výše v materiálech.

Objekty a jejich reprezentace v matici
--------------------------------------

* vystačíte si s jedním typem zdi (-1)
    * pokud to chcete mít později zajímavější, vytvořte si typy dva (-1 a -2)
* jako cíl (1) můžete použít obrázek hradu
* postavy jsou průchozí a je jich 5 různých druhů (2 až 6)
* pokud vaše algoritmy dokáží pracovat jen s jedním cílem, zabraňte vzniku bludiště s více cíli
    * buďto přidání druhého cíle nebude možné
    * nebo se tím odstraní předchozí cíl
* podobně pokud vaše algoritmy neumí pracovat s bludištěm bez cíle, zabraňte vzniku této situace

Formát souboru s bludištěm
--------------------------

Ukládejte a načítejte bludiště takto, umožní nám to jednodušší kontrolu:

```python
numpy.savetxt(path, array)
array = numpy.loadtxt(path, dtype=numpy.int8)
```

Zobrazování cesty
-----------------

* nejkratší cesty od všech postav k cíli zobrazte pomocí obrázků čar z materiálů
* výpočet cesty pro jednu postavu máte připraven z minulých úkolů
* musíte si zvolit vhodný způsob, jaky více cest od více postav složit do jedné tak, abyste mohli použít křižovatky apod.
    * *tip:* názvy souborů s čarami nejsou náhodné
    * *tip:* jelikož cesta vede přes políčka, na kterých může být postava nebo cíl, nemůžete cestu ukládat do matice s bludištěm
* výpočet nových cest musíte provést po každé změně bludiště (vytvoření, načtení, přidání/odebrání objektu)
    * kód spojující cesty by měl proto být relativně rychlý (v případě nutnosti si vypomožte Cythonem, ale při vhodně zvoleném algoritmu to není nutné)
* na cestě musí být znázorněny šipky směrem k cíli
    * matici šipek máte opět z úloh z minula, stačí je zobrazit pouze tam, kde jsou čáry
* od některých postav logicky cesta k cíli nemusí existovat, od nich tedy žádnou nevykreslujte (aplikace s takovou situací musí počítat a nesmí spadnout)

![Obrázek bludiště](https://raw.githubusercontent.com/cvut/MI-PYT/master/tutorials/09-qt/mazepic.png)

Odevzdání
---------

Jako obvykle. Tag `v0.3`, termín příští středu v 11:00. Pokud teprve začínáte, můžete použít naše [řešení] minulé úlohy (pozor na licenci\*), a nezapomeňte nás pozvat do repozitáře `maze`.

[řešení]: https://github.com/encukou/maze

\* Licence našeho řešení je (zatím) MIT. Při použití PyQt5 ale musíte použít GPL. Což jde, ale někam musíte napsat, že části vašeho programu mají MIT licenci, a přiložit kopii této licence. Abyste to měli jednodušší, dáváme vám souhlas, abyste naše řešení šířili pod stejnou licencí, jako má GPL varianta PyQt5. V takovém případě nás však nezapomeňte uvést jako autory.

Uvítáme, pokud přidáte další testy k nově implementované logice, ale není to nutné.

Aplikace musí jít spustit ve virtualenvu (na systému, pro který jsou PyQt5 wheels na PyPI, a na kterém je nainstalovaný překladač C a hlavičkové soubory Pythonu) takto:

```
python -m pip install -r requirements.txt
python setup.py develop
python -m maze
```

Doporučujeme si sekvenci těchto příkazů vyzkoušet v novém virtualenvu, ať nedochází ke zbytečným chybám.

Aplikace nesmí při žádné akci uživatele zhavarovat (tím nemyslíme, když uživatel udělá z terminálu <kbd>Ctrl</kbd>+<kbd>C</kbd>, ale když např. klikne někam, kde jste to nečekali, nebo zruší dialog pro výběr jména souboru).
Pokud se vám zdá v zadání něco nelogické, prosím, zeptejte se.

