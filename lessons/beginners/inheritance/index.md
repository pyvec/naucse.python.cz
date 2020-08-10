# Dědičnost

Minule jsme probrali třídy.
Jako příklad jsme si ukázali třídu pro koťátka:

```python
class Kotatko:
    def __init__(self, jmeno):
        self.jmeno = jmeno

    def snez(self, jidlo):
        print(f"{self.jmeno}: {jidlo} mi chutná!")

    def zamnoukej(self):
        print(f"{self.jmeno}: Mňau!")
```

Zkus si udělat podobnou třídu pro štěňátka:

```python
class Stenatko:
    def __init__(self, jmeno):
        self.jmeno = jmeno

    def snez(self, jidlo):
        print(f"{self.jmeno}: {jidlo} mi chutná!")

    def zastekej(self):
        print(f"{self.jmeno}: Haf!")
```

Většina kódu je stejná!
Kdybys měla napsat i třídu pro kuřátka, kůzlátka,
slůňátka a háďátka, bez <kbd>Ctrl</kbd>+<kbd>C</kbd> by to bylo docela nudné.
A protože jsou programátoři líní psát stejný kód
několikrát (a hlavně ho potom udržovat), vymysleli
mechanismus, jak se toho vyvarovat.

Koťátka i štěňátka jsou zvířátka.
Můžeš si vytvořit třídu společnou pro všechna
zvířátka a do ní napsat všechno, co je společné.
Ve třídách pro jednotlivé druhy zvířat pak zbude jen to, co se liší.
V Pythonu se to dělá takto:

```python
class Zviratko:
    def __init__(self, jmeno):
        self.jmeno = jmeno

    def snez(self, jidlo):
        print(f"{self.jmeno}: {jidlo} mi chutná!")


class Kotatko(Zviratko):
    def zamnoukej(self):
        print(f"{self.jmeno}: Mňau!")


class Stenatko(Zviratko):
    def zastekej(self):
        print(f"{self.jmeno}: Haf!")


micka = Kotatko('Micka')
azorek = Stenatko('Azorek')
micka.zamnoukej()
azorek.zastekej()
micka.snez('myš')
azorek.snez('kost')
```

Jak to funguje?
Příkazem `class Kotatko(Zviratko):`
říkáš Pythonu, že třída `Kotatko`
*dědí* ze třídy `Zviratko`
(angl. *inherits* from `Zviratko`).
Případně se můžeš setkat s jinými termíny:
„je odvozená” ze třídy `Zviratko`,
(angl. *derived from*),
nebo ji “rozšiřuje” (angl. *extends*).
A když už jsme u terminologie, odvozeným třídám se
říká taky *podtřídy* (angl. *subclasses*)
a `Zviratko` je tu *nadtřída*
(angl. *superclass*).

Když potom Python hledá nějakou metodu
(nebo jiný atribut), třeba `micka.snez`,
a nenajde ji přímo ve třídě daného objektu (u nás
`Kotatko`), podívá se do nadtřídy.
Takže všechno, co je definované pro
`Zviratko`, platí i pro koťátka – dokud to výslovně nezměníš.


## Přepisování metod a `super()`

Když se ti nebude líbit chování některé metody
v nadtřídě, stačí dát metodu stejného jména do
podtřídy:

```python
class Kotatko(Zviratko):
    def snez(self, jidlo):
        print(f"{self.jmeno}: {jidlo} mi vůbec nechutná!")


micka = Kotatko('Micka')
micka.snez('granule')
```

> [note]
> Je to podobné jako když jsme minule přepisoval{{gnd('i', 'y', both='i')}}
> atribut pomocí `micka.zamnoukej = 12345`.
> Python atributy hledá napřed na samotném objektu,
> potom na třídě toho objektu a pak na nadtřídě
> (a případně dalších nadtřídách té nadtřídy).

Občas se může stát, že v takovéto přepsané metodě budeš
potřebovat použít původní funkčnost, jen budeš chtít udělat ještě něco navíc.
To umí zařídit speciální funkce `super()`,
která umožňuje volat metody z nadtřídy.
Třeba takhle:

```python
class Kotatko(Zviratko):
    def snez(self, jidlo):
        print(f"({self.jmeno} na {jidlo} chvíli fascinovaně kouká)")
        super().snez(jidlo)


micka = Kotatko('Micka')
micka.snez('granule')
```

Pozor na to, že takhle volané metodě musíš dát všechny
argumenty, které potřebuje (kromě `self`,
který se jako obvykle doplní automaticky).
Toho se dá i využít – můžeš použít i jiné argumenty
než dostala původní funkce:

```python
class Hadatko(Zviratko):
    def __init__(self, jmeno):
        jmeno = jmeno.replace('s', 'sss')
        jmeno = jmeno.replace('S', 'Sss')
        super().__init__(jmeno)


standa = Hadatko('Stanislav')
standa.snez('myš')
```

Jak je vidět, `super()` se dá bez problémů
kombinovat se speciálními metodami jako `__init__`.
Dokonce se to dělá poměrně často!


## Polymorfismus

Programátoři nezavedli dědičnost jen proto, že jsou
líní a nechtějí psát dvakrát stejný kód.
To je sice dobrý důvod, ale nadtřídy mají jednu
důležitější vlastnost. Když víš, že každé
`Kotatko` nebo `Stenatko`
nebo jakákoli jiná podtřída je zvířátko,
můžeš si udělat seznam zvířátek s tím,
že pak bude jedno, jaká přesně zvířátka to jsou:

```python
{# XXX: perhaps put these definitions back, but highlight the 4 lines below?
class Zviratko:
    def __init__(self, jmeno):
        self.jmeno = jmeno

    def snez(self, jidlo):
        print(f"{self.jmeno}: {jidlo} mi chutná!")


class Kotatko(Zviratko):
    def zamnoukej(self):
        print(f"{self.jmeno}: Mňau!")


class Stenatko(Zviratko):
    def zastekej(self):
        print(f"{self.jmeno}: Haf!")
#}
zviratka = [Kotatko('Micka'), Stenatko('Azorek')]

for zviratko in zviratka:
    zviratko.snez('flákota')
```

Tohle je docela důležitá vlastnost podtříd:
když máš nějaké `Kotatko`, můžeš ho použít
kdekoliv kde program očekává `Zviratko`,
protože každé koťátko *je* zvířátko.

> [note]
> Tohle je docela dobrá pomůcka pro případy, kdy nebudeš vědět
> kterou třídu podědit z které.
> Každé *koťátko* nebo *štěňátko*
> je *zvířátko*, každá *chata*
> nebo *panelák* je *stavení*.
> V takových případech dává dědičnost smysl.
>
> Někdy se ale stane, že tuhle pomůcku zkusíš použít a vyjde ti
> nesmysl jako „každé auto je volant”.
> V takovém případě dědičnost nepoužívej.
> I když jak auto tak volant se dají „otočit doprava”,
> u každého to znamená něco jiného – a určitě nejde auto
> použít kdekoli, kde bys chtěl{{a}} použít volant.
> Takže v tomto případě je lepší si říct „každé auto
> *má* volant”, stejně jako „každé kotě
> *má* jméno”, udělat dvě nezávislé třídy a napsat něco jako:
>
> ```python
> class Auto:
>     def __init__(self):
>         self.volant = Volant()
> ```
>
> (A až bude někdy nějaký vystudovaný informatik nespokojený
> s tím, že porušuješ
> [Liskovové substituční princip](https://en.wikipedia.org/wiki/Liskov_substitution_principle),
> jde o právě tento problém.)

## Generalizace

Když se teď podíváš na funkce `zamnoukej`
a `zastekej`, možná tě napadne, že by se
daly pojmenovat lépe, aby se daly použít pro všechna
zvířata, podobně jako `snez`.
Bude nejlepší je přejmenovat:


{# XXX: Every instance of "udelej_zvuk" should be highlighted #}
```python
class Zviratko:
    def __init__(self, jmeno):
        self.jmeno = jmeno

    def snez(self, jidlo):
        print(f"{self.jmeno}: {jidlo} mi chutná!")


class Kotatko(Zviratko):
    def udelej_zvuk(self):
        print(f"{self.jmeno}: Mňau!")


class Stenatko(Zviratko):
    def udelej_zvuk(self):
        print(f"{self.jmeno}: Haf!")


zviratka = [Kotatko('Micka'), Stenatko('Azorek')]

for zviratko in zviratka:
    zviratko.udelej_zvuk()
    zviratko.snez('flákota')
```

Jak tenhle příklad naznačuje, psát nadtřídy ze kterých se dobře dědí
není jednoduché. Zvlášť to platí, kdyby se z nich mělo dědit v jiném
programu, než kde je nadtřída.
I z toho důvodu je dobré dědičnost používat hlavně v rámci svého kódu:
nedoporučuji dědit od tříd, které napsali ostatní (jako `bool` nebo
`pyglet.sprite.Sprite`), pokud autor nadtřídy výslovně nezmíní, že (a jak) se
z ní dědit má.

A to je zatím o třídách vše. Už toho víš dost na to,
aby sis napsal{{a}} vlastní zoo :)
