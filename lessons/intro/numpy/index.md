NumPy
=====

Materiály jsou opět [na Githubu](https://github.com/cvut/MI-PYT/blob/master/tutorials/07-numpy/numpy-intro.ipynb).

Na příklady budete potřebovat následující soubory:


* [matrixdemo.py](https://raw.githubusercontent.com/cvut/MI-PYT/master/tutorials/07-numpy/matrixdemo.py)
* [python.jpg](https://raw.githubusercontent.com/cvut/MI-PYT/master/tutorials/07-numpy/python.jpg)
* [sample.wav](https://github.com/cvut/MI-PYT/raw/master/tutorials/07-numpy/sample.wav)
* [secret.png](https://raw.githubusercontent.com/cvut/MI-PYT/master/tutorials/07-numpy/secret.png)
* [python-logo-template.svg](https://raw.githubusercontent.com/cvut/MI-PYT/master/tutorials/07-numpy/python-logo-template.svg)

---

Vaším úkolem je vytvořit funkci `analyze(maze)`

Na vstupu bude bludiště uložené v matici, kde:

* záporné honoty představují zeď (kterou nejde projít)
* nezáporné hodnoty předstvaují průchozí prostor
* 1 představuje cíl

V bludišti se lze pohybovat pouze horizontálně nebo veritkálně. Hranice matice jsou neprůchozí.

Funkce vrátí objekt, který má:

* atribut `distances`: matice, kde pro každé políčko, ze kterého se dá dostat do cíle, bude délka nejkratší cesty k cíli, jinak -1
* atribut `directions`, matice, kde je pro každé takové políčko směr, kterým se odtud dá nejrychleji dostat do cíle, jako ASCII byte `^`, `v`, `<` nebo `>`; pro nedostupná políčka mezeru, pro cíl `X` a pro zeď `#`
* atribut `is_reachable`: `True` pokud se dá z každého políčka, kde není zeď, dostat do cíle, jinak `False`
* metodu `path(x, y)`: vrátí souřadnice nejkratší cesty z políčka `(x, y)` jako seznam dvojic včetně cíle a startu (pro souřadnice zdí a nedostupných políček vyhodí výjimku)

K funkci napiště testy pomocí pytestu, hezká bludiště na testování můžete získat
[generátorem](https://en.wikipedia.org/wiki/Maze_generation_algorithm).

Odevzdávání:

* vytvořte si nový privátní git repozitář (do něj nás pozvěte)
* na tuto úlohu budou navazovat další, všechny se budou tématicky věnovat bludišti
* v repozitáři odevzdávejte pomocí tagu `v0.1`
* všechny závislosti (včetně `numpy` a `pytest`) uveďte v souboru `requirements.txt` (nemusí být s konkrétní verzí)
* příkaz `python -m pytest` musí po instalaci závislostí spouštět testy
