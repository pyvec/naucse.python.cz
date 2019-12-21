# Instalace

Instalace všeho potřebného není složitá a zabere jen chvíli. Pokud se během ní
přeci jen něco pokazí, popros na Slacku nebo někoho zkušenějšího o radu.

> Další kroky počítají s tím, že máš nainstalovaný a funkční Python 3.
Pokud ne, návod na instalaci máme k dispozici [v začátečnickém kurzu](https://naucse.python.cz/course/pyladies/sessions/install/).

## Adresář, vytvoření a aktivace virtuálního prostředí

Nejprve si připrav adresář pro ukládání souborů (třeba `pydata`) a v něm si vytvoř
virtuální prostředí.

Pokud nevíš jak na to, kompletní návod je stejně jako pro instalaci Pythonu k dispozici
v [materiálech k začátečnickému kurzu](https://naucse.python.cz/2019/pyladies-ostrava-podzim/beginners/venv-setup/).

Po každém spuštění příkazové řádky bude potřeba aktivovat virtuální prostředí, abychom
mohli pracovat s knihovnami a nástroji v něm nainstalovanými.

## Instalace

Do příkazové řádky s aktivním virtuálním prostředím zadej následující příkaz:

```shell
(venv)$ python -m pip install jupyter pandas matplotlib seaborn scipy scikit-learn
```

Tímto příkazem se do virtuálního prostředí nainstalovaly následující knihovny:

* Jupyter - webové rozhraní pro interaktivní a reprodukovatelnou práci s Pythonem
* Pandas - pro práci s tabulkovými daty
* Matplotlib - jedna z nejznámějších knihoven pro tvorbu grafů
* Seaborn - rozšíření pro Matplotlib, které umí vytvořit pokročilejší grafy
* SciPy - švýcarský nůž pro věděcké výpočty a pokročilou matematiku
* Scikit-learn - sbírka nejznámějších algoritmů pro strojové učení

V následující kapitole se podíváme na to, jak Jupyter spustit a jak s ním pracovat.
