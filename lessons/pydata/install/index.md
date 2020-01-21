# Instalace

Instalace všeho potřebného není složitá a zabere jen chvíli. Pokud se během ní
přeci jen něco pokazí, popros na Slacku nebo někoho zkušenějšího o radu.

> Další kroky počítají s tím, že máš nainstalovaný a funkční Python 3.6 nebo 3.7.
Pokud ne, návod na instalaci máme k dispozici [v začátečnickém kurzu](https://naucse.python.cz/course/pyladies/sessions/install/).

> **Upozornění:**
Na základě povšimnutí jedné z vás jsme zjistili, že jsou problémy hned se dvěma způsoby instalace Pythonu
ve Windows. Prosím, neinstaluj Python z Windows Store
a neinstaluj Python 3.8, v obou případech není jednoduché zprovoznit Jupyter Notebook. Doporučujeme nainstalovat
Python 3.7.6 [odtud](https://www.python.org/downloads/release/python-376/) (vyber "executable installer", ideálně verzi `x86-64`).
Nezapomeň v první obrazovce instalátoru zaškrtnout, že chceš přidat Python do proměnné `PATH`. Pokud chceš (a navíc víš proč), 
s distribucí [miniconda](https://docs.conda.io/en/latest/miniconda.html) by také neměly být problémy
(někteří z autorů ji používají).

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
(venv)$ python -m pip install jupyter pandas matplotlib requests seaborn scipy scikit-learn plotly xlrd openpyxl
```

Tímto příkazem se do virtuálního prostředí nainstalovaly následující knihovny (a některé další jejich závislosti):

* Jupyter - webové rozhraní pro interaktivní a reprodukovatelnou práci s Pythonem
* Pandas - pro práci s tabulkovými daty
* Matplotlib - jedna z nejznámějších knihoven pro tvorbu grafů
* Seaborn - rozšíření pro Matplotlib, které umí vytvořit pokročilejší grafy
* SciPy - švýcarský nůž pro věděcké výpočty a pokročilou matematiku
* Scikit-learn - sbírka nejznámějších algoritmů pro strojové učení
* Requests - knihovna pro práci s HTTP (webovými a API) požadavky
* Plotly - knihovna pro vytváření interaktivních grafů
* Xlrd - knihovna pro načítání souborů .xls/.xlsx
* Openpyxl - knihovna pro načítání a zápis souborů .xlsx

V následující kapitole se podíváme na to, jak Jupyter spustit a jak s ním pracovat.
