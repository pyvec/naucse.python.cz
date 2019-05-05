# To-Do List

## Co je cílem tohoto cvičení?

Na tomto příkladu si vyzkoušíme použít knihovnu SQLAlchemy na práci s databází.
Napíšeme si jednoduchý program pro evidenci úkolů. Také si procvičíme práci s
knihovnou Click.


## Předpoklady

Předpokládáme základní znalost Pythonu. Měli byste mít počítač s nainstalovaným
interpretem jazyka Python ve verzi aspoň 3.6. Pro začátek si také vytvořte nové
virtuální prostředí.

Do tohoto prostředí si nainstalujte knihovny `sqlalchemy` a `click`.


## Krok 1 – připojení k databázi


Pro zjednodušení začneme čtením dat z databáze. Můžete si stáhnout
<a href="{{ static("ukoly.sqlite") }}">připravená data</a>. Stáhněte si ho do
stejného adresáře, ve kterém budete mít samotný program.

Do souboru `ukoly.py` si stáhněte tuto základní kostru.


```python
# ukoly.py
from sqlalchemy import create_engine


db = create_engine("sqlite:///ukoly.sqlite")
```

Funkce `create_engine` vytváří spojení s databází `ukoly.sqlite`, která je
uložená v aktuálním adresáři. Knihovna `sqlalchemy` umí pracovat i s jinými
typy databází než je `SQLite`. Ta je ale nejjednodušší, a velice vhodná na
uložení dat, se kterými budeme pracovat.

Momentálně program nic nedělá. Nejprve musíme nadefinovat, jak vlastně naše
data vypadají.


## Krok 2 – první dotaz

Samotnou databází si můžeme přestavit jako několik tabulek, které mají nějak
pojmenované sloupce. V našem příkladu budeme potřebovat jedinou tabulku, ale
klidně by jich mohlo být víc.

Pro každou tabulku budeme potřebovat třídu (`class`), jejíž instance budou
reprezentovat jednotlivé řádky v ní.

Metodu `__repr__` používá Python, když potřebuje zobrazit instanci této třídy.
Není určená na výpis pro uživatele, ale pro ladění programu.

```python
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.exc.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


db = create_engine("sqlite:///ukoly.sqlite")
Base = declarative_base()


class Ukol(Base):
    # Název tabulky v databází.
    __tablename__ = "ukoly"

    # Číselný identifikátor úkolu, toto číslo bude jedinečné.
    id = Column(Integer, primary_key=True)
    # Text úkolu.
    text = Column(String)
    # Datum a čas zadání úkolu.
    zadano = Column(DateTime)
    # Datum a čas vyřešení úkolu. Prázdná hodnota znamená nehotový úkol.
    vyreseno = Column(DateTime)

    def __repr__(self):
        return f"<Ukol(text='{self.text}', zadano={self.zadano}, vyreseno={self.vyreseno})>"
```

Přidejte jeden import a na konec souboru ještě několik řádků. Pokud chceme z
databáze vytahovat data, nebo je ukládat, potřebujeme vytvořit ještě jeden
objekt. Takzvané sezení (anglicky *session*) využije dříve vytvořené spojení a
umožňuje nám použít všechny nadefinované třídy.

```python
from sqlalchemy.orm import sessionmaker

...

Session = sessionmaker(bind=db)
sezeni = Session()

dotaz = sezeni.query(Ukol)
print(dotaz.all())
```

Metoda `query` vytvoří dotaz, který bude vracet instance třídy `Ukol`. Nezadáme
žádné omezení, takže chceme všechny úkoly. Metoda `all` na tomto dotazu potom
vrací seznam všech řádků v tabulce, které odpovídají dotazu.

Tento program už půjde spustit a bude vypisovat všechny úkoly. Tento výpis ale
není úplně pěkný. Upravte program tak, aby každý úkol byl na samostatném řádku,
a v hezky čitelném formátu. Jednotlivé objekty mají atributy `id` a `text`,
které můžeme použít.

{% filter solution %}
```python
...

ukoly = dotaz.all()
for ukol in ukoly:
    symbol = "[x]" if ukol.vyreseno else "[ ]"
    print(f"{symbol} {ukol.id}. {ukol.text}")
```
{% endfilter %}


## Krok 3 – uživatelské rozhraní

Teď program upravíme tak, abychom ho mohli postupně rozšiřovat dalšími příkazy.

Ve finále chceme, aby program fungoval takto:

```console
$ python ukoly.py vypis
[x] 1. dej si čaj
[x] 2. bež do kina
$ python ukoly.py pridej
Nový úkol: Udělej si úkoly
Zadán úkol 3
$ python ukoly.py vyres 3
$ python ukoly.py vypis
[x] 1. dej si čaj
[x] 2. bež do kina
[x] 3. Udělej si úkoly
```

Nejprve musíme naimportovat knihovnu `click`.

Následně označíme hlavní funkci dekorátorem `@click.group()`. Tím řekneme, že
to vlastně není příkaz sám o sobě, ale bude to skupina dalších příkazů. Hned si
jeden vytvoříme a necháme ho vypisovat úkoly.

```python
Session = sessionmaker(bind=db)
sezeni = Session()


@click.group()
def ukolnik():
    pass


@ukolnik.command()
def vypis():
    dotaz = sezeni.query(Ukol)
    ukoly = dotaz.all()
    for ukol in ukoly:
        symbol = "[x]" if ukol.vyreseno else "[ ]"
        print(f"{symbol} {ukol.id}. {ukol.text}")


if __name__ == "__main__":
    ukolnik()
```

Výpis by měl pořád vypadat stejně, akorát ho budeme volat trochu jinak.


## Krok 4 – přidávání úkolů

Přidejte do programu další příkaz. Bude se jmenovat `pridej`, a vždy od
uživatele dostane text úkolu, který hned vypíše.

{% filter solution %}
```python
@ukolnik.command()
@click.option("--zadani", prompt="Nový úkol")
def pridej(zadani):
    print(f"OK: {zadani}")
```
{% endfilter %}

Teď můžeme metodu upravit tak, aby úkol opravdu vytvořila a uložila.

Nejprve musíme vytvořit instanci třídy `Ukol`. Tu potom přidáme do našeho
sezení a řekneme databázi, že ji chceme uložit. Aktuální čas dostaneme ze
standardní knihovny, takže nezapomeňte na začátek programu přidat `from
datetime import datetime`.

{% filter solution %}
```python
@ukolnik.command()
@click.option("--zadani", prompt="Nový úkol")
def pridej(zadani):
    ukol = Ukol(text=zadani, zadano=datetime.now())
    sezeni.add(ukol)
    sezeni.commit()
```
{% endfilter %}

Pokud bychom vytvářeli několik úkolů, můžeme je všechny přidat a teprve potom
jednou zavolat `commit`. Pokud bychom na toto poslední volání zapomněli,
záznamy budou časem uloženy taky, ale nebude úplně přímočaré poznat, kde k tomu
dojde. Je lepší najít vhodné místo a `commit` zavolat.


## Krok 5 – vytvoření databáze

Momentálně program funguje celkem dobře, ale vždycky potřebuje, aby na disku
existoval soubor s databází. Bylo by hezké, kdyby si dokázal vytvořit prázdnou
databázi.

Nejprve přesuneme vytváření sezení do samostatné funkce, kterou zavoláme v
každém příkazu. Toto nebude mít vliv na výsledné chování, ale program bude
trošku čitelnější a jednodušší na orientaci.

Vytvořte funkci `pripoj_se`, která nebude mít žádné argumenty a bude vracet
nové sezení.


{% filter solution %}
```python
...

def pripoj_se():
    Session = sessionmaker(bind=db)
    return Session()


@click.group()
def ukolnik():
    pass


@ukolnik.command()
def vypis():
    sezeni = pripoj_se()
    ...


@ukolnik.command()
@click.option("--zadani", prompt="Nový úkol")
def pridej(zadani):
    sezeni = pripoj_se()
    ...
```
{% endfilter %}

K vytvoření prázdné databáze stačí do funkce `pripoj_se` přidat jeden řádek:

```python
def pripoj_se():
    Base.metadata.create_all(db)
    Session = sessionmaker(bind=db)
    return Session()
```

Třída `Base` je společný předek všech našich tříd reprezentujících data. My
máme pouze jednu, ale to není na závadu. Nově přidané volání se podívá, jestli
pro každou třídu existuje odpovídající tabulka, a případně ji vytvoří.

Tato funkce není úplně všemocná. Pokud například budeme měnit existující
tabulku, s největší pravděpodobností dostaneme chybovou hlášku. Na obecné
migrace dat je lepší použít něco sofistikovanějšího, jako třeba knihovnu
[alembic].

[alembic]: https://pypi.org/project/alembic/


## Krok 6 – řešení úkolů

Pojďme přidat poslední chybějící část: označování úkolů za vyřešené. Začneme
zase přidáním kostry příkazu, která dostane číslo úkolu a vypíše ho na výstup.

{% filter solution %}
```python
@ukolnik.command()
@click.argument("cislo_ukolu", type=click.INT)
def vyres(cislo_ukolu):
    print(f"Značím {cislo_ukolu} jako vyřešené")
```
{% endfilter %}

Postup pro vyřešení úkolu bude následovný: najdeme úkol podle čísla, nastavíme
mu čas vyřešení a uložíme ho.

Metodu `query` pro vytvoření dotazu už známe. Tentokrát ovšem místo všech úkolů
chceme najít jeden konkrétní. K tomu použijeme `filter_by`, která přes
pojmenované argumenty umí vyfiltrovat pouze některé řádky.

Pro vykonání dotazu existuje kromě nám už známé `all()` několik metod:

 * `all` vrací všechny výsledky jako seznam
 * `first` vrací první výsledek, další ignoruje
 * `one` zkontroluje, že máme právě jeden výsledek, a vrátí ho. Pokud by jich
   byl jiný počet, vyhodí výjimku.
 * `one_or_none` se chová podobně, ale místo výjimky vrací `None`
 * `scalar` očekává ve výsledku jeden řádek s jediným sloupcem, a vrací přímo
   hodnotu z tohoto jediného pole

```python
@ukolnik.command()
@click.argument("cislo_ukolu", type=click.INT)
def vyres(cislo_ukolu):
    sezeni = pripoj_se()
    dotaz = sezeni.query(Ukol)
    ukol = dotaz.filter_by(id=cislo_ukolu).one()
    ukol.vyreseno = datetime.now()
    sezeni.add(ukol)
    sezeni.commit()
```

> [note]
> Mohli bychom použít metodu `get(cislo_ukolu)`, která najde úkol podle klíče.
> To bychom si ale neprocvičili filtrování výsledků dotazu.


## Krok 7 – výpis jen nedokončených úkolů

Filtrování můžeme aplikovat i pro výpis úkolů. Například bychom mohli vypisovat
jenom úkoly, které ještě nejsou dokončené.

Na to se nám může hodit metoda `filter`, která umožňuje více porovnání než
známá `filter_by`.

```python
@ukolnik.command()
@click.option("--jen-nehotove", default=False, is_flag=True)
def vypis(jen_nehotove):
    sezeni = pripoj_se()
    dotaz = sezeni.query(Ukol)

    if jen_nehotove:
        dotaz = dotaz.filter(Ukol.vyreseno == None)

    ukoly = dotaz.all()
    for ukol in ukoly:
        symbol = "[x]" if ukol.vyreseno else "[ ]"
        print(f"{symbol} {ukol.id}. {ukol.text}")  
```


## Další vylepšení

Tady je několik tipů, co by se v tomto programu dalo vylepšit:

* Ošetření chyb: momentálně program spadne, pokud se pokusíme vyřešit
  neexistující úkol.
* Řazení výpisu: teď jsou úkoly vypsané od nejstaršího. Možná bychom je chtěli
  řadit v opačném pořadí. Dotaz má metodu `order_by()`, které můžeme zadat
  sloupec, podle kterého se bude řadit. Také můžeme řadit v opačném pořadí,
  třeba pomocí `Ukol.zadano.desc()`.
* Mohli bychom přidat další příkaz, který smaže některé úkoly (třeba ty, které
  jsou vyřešené, nebo starší než nějaký limit). Dotaz s aplikovanými filtry má
  metodu `delete()`, která smaže všechny odpovídající záznamy.
