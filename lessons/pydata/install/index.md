# Instalace

Instalace všeho potřebného není složitá a zabere jen chvíli. Pokud se během ní
přeci jen něco pokazí, popros na Slacku nebo někoho zkušenějšího o radu.

Další kroky počítají s tím, že máš nainstalovaný a funkční Python 3.6, 3.7 nebo 3.8.
Pokud ne, obecný návod na instalaci máme k dispozici [v začátečnickém kurzu](https://naucse.python.cz/course/pyladies/sessions/install/).

Tip č. 1: Máš-li aktualizované Windows 10, úplně nejjednodušší je použít instalaci z [Microsoft Store](https://www.microsoft.com/store/productId/9MSSZTT1N39L).

Tip č. 2: Pokud chceš, můžeš použít distribucí [miniconda](https://docs.conda.io/en/latest/miniconda.html), s ní by také neměly být problémy. Lidé z oblasti data science (včetně některých autorů těchto materiálů) ji rádi používají - sice se tak připravují o práci s "čistým" Pythonem, ale zjednodušují si instalaci některých (zejména výpočetních) knihoven, které závisejí na externích binárních balíčcích.

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
(venv)$ python -m pip install jupyter pandas matplotlib requests seaborn scipy scikit-learn sqlalchemy plotly xlrd openpyxl
```

Tímto příkazem se do virtuálního prostředí nainstalovaly následující knihovny (a některé další jejich závislosti):

* Jupyter - webové rozhraní pro interaktivní a reprodukovatelnou práci s Pythonem
* Matplotlib - jedna z nejznámějších knihoven pro tvorbu grafů
* Openpyxl - knihovna pro načítání a zápis souborů .xlsx
* Pandas - pro práci s tabulkovými daty
* Plotly - knihovna pro vytváření interaktivních grafů
* Requests - knihovna pro práci s HTTP (webovými a API) požadavky
* Scikit-learn - sbírka nejznámějších algoritmů pro strojové učení
* SciPy - švýcarský nůž pro vědecké výpočty a pokročilou matematiku
* Seaborn - rozšíření pro Matplotlib, které umí vytvořit pokročilejší grafy
* Sqlalchemy - knihovna pro sjednocený, vysokoúrovňový přístup k databázím
* Xlrd - knihovna pro načítání souborů .xls/.xlsx

V následující kapitole se podíváme na to, jak Jupyter spustit a jak s ním pracovat.
