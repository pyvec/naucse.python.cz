GUI v Pythonu: PyQt5
====================

Instalace
---------

Na tomto cvičení budete potřebovat balíček PyQt5 a aplikaci Qt5 Designer.
Pokud budete používat svůj počítač, prosíme vás o instalaci již předem, na cvičení toho bude opravdu hodně a nemůžeme si dovolit plýtvat časem.

### PyQt5

Pokud máte Python 3.5 a jednu z platforem, pro které je připraven [wheel na PyPI](https://pypi.python.org/pypi/PyQt5), stačí udělat:

    python -m pip install PyQt5

Pro starší verzi Pythonu nebo 32bitový Linux to ale nebude fungovat.
V takovém případě můžete PyQt5 zkusit najít v balíčkovacím systému vaší distribuce (např. balíček `python3-qt5` ve Fedoře nebo `python3-pyqt5` v Debianu).
Virtualenv pak může vytvořit s přepínačem `--system-site-packages`, který zajistí, že i z virtualenvu uvidíte PyQt5 nainstalované z distribučního balíčku.

Pokud nic z toho nepomůže, můžete zkusit přeložit PyQt5 ze [zdrojových souborů](https://www.riverbankcomputing.com/software/pyqt/download5)
([návod](http://pyqt.sourceforge.net/Docs/PyQt5/installation.html#building-and-installing-from-source)).

Pokud narazíte na chybu `Could not find or load the Qt platform plugin "xcb"`, podívejte se do [naší issue](https://github.com/cvut/MI-PYT/issues/57).

### Qt5 Designer

Na Linuxu najdete Qt5 Designer v balíčkách, třeba `qt5-designer` na Fedoře.

Na Windows (i na Macu) si můžete [stáhnout] instalátor Qt 5, který (doufáme) nainstaluje i Designer.

[stáhnout]: https://www.qt.io/download-open-source/#section-2

Pokud používáte na Macu `homebrew`, můžete to udělat i takto:

    brew install qt5
    brew linkapps qt5
