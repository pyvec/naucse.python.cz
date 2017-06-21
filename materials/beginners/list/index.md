Tahle kapitola je plná nových věcí.
Doufám, že vydržíš až do konce. A kdyby něco
zatím nedávalo úplně smysl, nevěš hlavu:
věci, které si teď vysvětlíme, se opravdu naučíš
až v dalších lekcích, kde je budeme využívat
prakticky.

Encyklopedické informace z této stránky shrnuje
[Tahák na seznamy](https://github.com/pyvec/cheatsheets/blob/master/lists/lists-cs.pdf),
který si doporučuji vytisknout.

Každý příklad v tomto textu si vyzkoušej;
to, co Python vypíše, je důležitá součást lekce,
i když v materiálech není přímo napsaná.

# Seznamy

Dnes si ukážeme, jak pracovat se *seznamy* (angl. *lists*).
Doufám, že víš, kde máš na klávesnici hranaté
závorky, protože právě těmi se seznamy vytváří:

```python
cisla = [1, 1, 2, 3, 5, 8, 13]
print(cisla)
```

> [note]
> Nemůžeš najít hranaté závorky?
> Na české klávesnici zkus pravý <kbd>Alt</kbd> + <kbd>F</kbd> a <kbd>G</kbd>.

Seznam je hodnota, která může obsahovat spoustu dalších hodnot.
Tak jako řetězec obsahuje sekvenci znaků,
seznam obsahuje sekvenci... čehokoliv. Třeba čísel.
A tak jako můžeme pomocí cyklu `for`
procházet řetězec po znacích,
seznam můžeme procházet po jednotlivých prvcích:

```python
for cislo in cisla:
    print(cislo)
```

Seznamy se v programech vyskytují velice často:
soubor se dá načíst jako seznam řetězců
s jednotlivými řádky,
seznam řetězců jako `'7♥'`
a `'K♣'` může posloužit jako balíček karet,
matematika je plná číselných řad,
každá online služba má seznam uživatelů.


Hodnoty v seznamu můžou být jakéhokoli typu,
dokonce můžeme různé typy míchat v jednom seznamu
(i když s takovými namixovanými seznamy se
příliš často nesetkáme – více se používají v
<var>n</var>-ticích, o kterých si povíme později):

```python
seznam = [1, 'abc', True, None, range(10), len]
print(seznam)
```

## Vybírání ze seznamů

Nejzákladnější operaci se seznamy,
cyklus `for`, už jsme si ukázal{{gnd('i', 'y', both='i')}}.
Druhá nejdůležitější operace je vybírání
jednotlivých prvků.
To funguje jako u řetězců: do hranatých závorek
se dá číslo prvku. Čísluje se, jako u řetězců,
od nuly; záporná čísla označují prvky od konce.

```python
print(cisla[2])
```

Hranatými závorkami můžeme získávat podseznamy.
[Diagram z materiálů k řetězcům]({{ lesson_url('beginners/str')}}#slicing-diagram)
ukazuje, jak u takového „sekání” číslovat:
funguje to stejně, jen místo menšího řetězce
dostaneme menší seznam.

```python
print(cisla[2:-3])
```

## Měnění seznamů

Důležitá vlastnost seznamů, kterou nemají ani čísla, ani řetězce
(a `True`/`False`/`None` už vůbec ne), je,
že seznamy se dají měnit.

Čísla měnit nejdou – máš-li `a = 3` a
napíšeš `a = a + 1`, číslo `3` se nezmění.
Vypočítá se nové číslo `4` a proměnná `a`
se nastaví na toto nové číslo.

Oproti tomu seznamy se dají měnit bez nastavování proměnné.
Základní způsob, jak změnit seznam, je přidání
prvku na konec pomocí metody `append`.
Ta *nic nevrací* (resp. vrací `None`),
ale „na místě” (angl. *in place*) změní
seznam, na kterém pracuje. Vyzkoušej si to:

```python
prvocisla = [2, 3, 5, 7, 11, 13, 17]
print(prvocisla)
prvocisla.append(19)
print(prvocisla)
```

Takové měnění hodnoty může být občas překvapující,
protože stejnou hodnotu může mít více proměnných.
Protože se mění hodnota samotná, může to vypadat,
že se proměnná „mění aniž na ni sáhneme”:

```python
a = [1, 2, 3]   # vytvoření seznamu
b = a           # tady se nový seznam nevytváří

# seznam vytvořený v prvním řádku má teď dvě jména: "a" a "b",
# ale stále pracujeme jenom s jedním seznamem

print(b)
a.append(4)
print(b)
```

## Další způsoby, jak měnit seznamy

Kromě metody `append`, která přidává
jediný prvek, existuje metoda `extend`,
která umí přidávat prvků víc.
Prvky k přidání jí předáme ve formě seznamu:

```python
dalsi_prvocisla = [23, 29, 31]
prvocisla.extend(dalsi_prvocisla)
print(prvocisla)
```

Metoda `extend` umí pracovat i s jinými
typy než se seznamy – ráda zpracuje cokoli, přes
co umí cyklit `for`: např.
jednotlivé znaky řetězců, řádky souborů, nebo čísla z `range()`.

```python
seznam = []
seznam.extend('abcdef')
seznam.extend(range(10))
print(seznam)
```

## Měnění prvků

Ale dost přidávání.
Seznamům se dají i měnit jednotlivé prvky
a to jednoduše tak, že do prvku přiřadíme,
jako by to byla proměnná:

```python
cisla = [1, 0, 3, 4]
cisla[1] = 2
print(cisla)
```

Přiřazovat se dá i do podseznamu – v tomto případě
se podseznam nahradí jednotlivými prvky z toho,
co přiřazujeme.
Jako u `extend` můžeš do podseznamu opět přiřadit cokoli, co umí
zpracovat `for` – seznam, řetězec, `range()` apod.

```python
cisla = [1, 2, 3, 4]
cisla[1:-1] = [6, 5]
print(cisla)
```

## Mazání prvků

Přiřazením do podseznamu se dá i změnit délka
seznamu, nebo některé prvky úplně odstranit:

```python
cisla = [1, 2, 3, 4]
cisla[1:-1] = [0, 0, 0, 0, 0, 0]
print(cisla)
cisla[1:-1] = []
print(cisla)
```

Tenhle zápis pro mazání prvků je ale docela
nepřehledný, a proto na to máme zvláštní příkaz
jménem `del`.
Jak už jeho název (z angl. *delete*, smazat)
napovídá, smaže, co mu přijde pod ruku – jednotlivé
prvky seznamů, podseznamy, … a dokonce i proměnné!

```python
cisla = [1, 2, 3, 4, 5, 6]
del cisla[-1]
print(cisla)
del cisla[3:5]
print(cisla)
del cisla
print(cisla)
```

Další mazací metody jsou:
* `pop`, která odstraní *a vrátí* poslední prvek v seznamu – například pokud
  mám seznam karet v balíčku, jde takhle jednoduše „líznout” kartu,
* `remove`, která najde v seznamu daný prvek a odstraní ho,
* `clear`, která vyprázdní celý seznam.

```python
cisla = [1, 2, 3, 'abc', 4, 5, 6, 12]
posledni = cisla.pop()
print(posledni)
print(cisla)

cisla.remove('abc')
print(cisla)

cisla.clear()
print(cisla)
```

## Řazení

A taky tu máme metodu `sort`, která prvky seznamu seřadí.

```python
seznam = [4, 7, 8, 3, 5, 2, 4, 8, 5]
seznam.sort()
print(seznam)
```

Aby se daly seřadit, musí být prvky seznamu vzájemně
*porovnatelné* – konktrétně na ně musí fungovat
operátor `<`.
Seznam s mixem čísel a řetězců tedy seřadit nepůjde.
Operátor `<` definuje i
jak přesně se řadí (např. čísla podle velikosti;
řetězce podle speciální „abecedy” která řadí
velká písmena za malá, česká až za anglická, atd.).

Metoda `sort` zná pojmenovaný argument
`reverse`. Pokud ho nastavíš na *True*, řadí se „naopak”.

```python
seznam = [4, 7, 8, 3, 5, 2, 4, 8, 5]
seznam.sort(reverse=True)
print(seznam)
```

## Známé operace se seznamy

Spousta toho, co můžeme dělat s řetězci, má stejný
účinek i u seznamů.
Třeba sečítání a násobení číslem:

```python
melodie = ['C', 'E', 'G'] * 2 + ['E', 'E', 'D', 'E', 'F', 'D'] * 2 + ['E', 'D', 'C']
print(melodie)
```

Stejně jako u řetězců, sečítat jde jen seznam
se seznamem – ne třeba seznam s řetězcem.

Další staří známí jsou funkce `len`,
metody `count` a `index`, a operátor `in`.

```python
print(len(melodie))         # Délka seznamu
print(melodie.count('D'))   # Počet 'D' v seznamu
print(melodie.index('D'))   # Číslo prvního 'D'
print('D' in melodie)       # Je 'D' v seznamu?
```

Poslední tři se ale přece jen chovají kapku jinak:
u řetězců pracují s *podřetězci*,
u seznamů jen s *jednotlivými* prvky.
Takže ačkoliv naše melodie obsahuje prvky
`'D'` a `'E'` vedle sebe, `'DE'` v seznamu není:

```python
print('DE' in melodie)
print(melodie.count('DE'))
print(melodie.index('DE'))
```

## Seznam jako podmínka

Seznam se dá použít v příkazu `if` (nebo `while`) jako podmínka,
která platí, když v tom seznamu něco je.
Jinými slovy, `seznam` je tu „zkratka“ pro `len(seznam) > 0`.

```python
if seznam:
    print('V seznamu něco je!')
else:
    print('Seznam je prázdný!')
```

Podobně se dají v podmínce použít i řetězce.
A dokonce i čísla – ta jako podmínka platí, pokud jsou nenulová.

## Tvoření seznamů

Tak jako funkce `int` převádí na
celá čísla a `str` na řetězce,
funkce `list` (angl. *seznam*) převádí na seznam.
Jako argument jí předáme jakoukoli hodnotu,
kterou umí zpracovat příkaz `for`.
Z řetězců udělá seznam znaků, z otevřeného souboru
udělá seznam řádků, z `range` udělá
seznam čísel.

```python
abeceda = list('abcdefghijklmnopqrstuvwxyz')
cisla = list(range(100))
print(abeceda)
print(cisla)
```

I ze seznamu udělá funkce `list` seznam.
To může znít zbytečně, ale není – vytvoří se
totiž *nový* seznam.
Bude mít sice stejné prvky ve stejném pořadí,
ale nebude to ten samý seznam:
měnit se bude nezávisle na tom starém.

```python
a = [1, 2, 3]
b = list(a)

print(b)
a.append(4)
print(b)
```

Další způsob, jak tvořit seznamy
(zvláště složitější), je nejdřív udělat prázdný
seznam a pak ho postupně naplnit pomocí funkce `append`.
Třeba pokud z nějakého důvodu chceš seznam
mocnin dvou, projdi čísla, kterými chceme mocnit,
cyklem `for` a pro každé z nich
do seznamu přidej příslušnou mocninu:

```python
mocniny_dvou = []
for cislo in range(10):
    mocniny_dvou.append(2 ** cislo)
print(mocniny_dvou)
```

Chceš-li seznam, který reprezentuje balíček karet,
zavolej `append` pro všechny kombinace barev a hodnot.

```python
balicek = []
for barva in '♠', '♥', '♦', '♣':  # (Na Windows použij textová jména)
    for hodnota in list(range(2, 11)) + ['J', 'Q', 'K', 'A']:
        balicek.append(str(hodnota) + barva)
print(balicek)
```

## Seznamy a řetězce

Seznamy a řetězce jsou druhy „sekvencí”,
takže snad nepřekvapí, že se dá různě převádět
z jednoho typu na druhý.
Funkce `list` vytvoří z řetězce
seznam znaků.
Když chceme dostat seznam slov, použijeme
na řetězci metodu `split` (angl. *rozdělit*):

```python
slova = 'Tato věta je složitá, rozdělme ji na slova!'.split()
print(slova)
```

Metoda `split` umí brát i argument.
Pokud ho předáme, místo mezer (a nových řádků)
se řetězec „rozseká” daným oddělovačem.
Takže když máme nějaká data oddělená čárkami,
není nic jednoduššího než použít `split` s čárkou:

```python
zaznamy = '3A,8B,2E,9D'.split(',')
print(zaznamy)
```

Chceme-li spojit seznam řetězců zase dohromady
do jediného řetězce, použijeme metodu
`join` (angl. *spojit*).
Pozor, tahle metoda se volá na *oddělovači*,
tedy řetězci, kterým se jednotlivé kousky „slepí”
dohromady; a jako argument bere seznam jednotlivých
řetězců.

```python
veta = ' '.join(slova)
print(veta)
```

## Úkol

Představ si, že ti uživatelé zadávají jména a příjmení a ty si je ukládáš do
seznamu pro další použití např. v evidenci studentů. Ne všichni jsou ale pořádní,
a tak se v seznamu sem tam objeví i jméno s nesprávně zadanými velkými písmeny.
Například:

```python
zaznamy = ['pepa novák', 'Jiří Sládek', 'Ivo navrátil', 'jan Poledník']
```

Úkolem je:

* Napsat funkci, která vybere jen ty správně zadané záznamy, které mají správně
jméno i příjmení s velkým počátečním písmenem.
* Napsat funkci, která vybere naopak jen ty nesprávně zadané záznamy.
* *(Nepovinný)* – Napsat funkci, která vrátí seznam s opravenými záznamy.

Výsledné funkce by měly fungovat takto:

```python
zaznamy = ['pepa novák', 'Jiří Sládek', 'Ivo navrátil', 'jan Poledník']

chybne_zaznamy = vyber_chybne(zaznamy)
print(chybne_zaznamy) # → ['pepa novák', 'Ivo navrátil', 'jan Poledník']

spravne_zaznamy = vyber_spravne(zaznamy)
print(spravne_zaznamy) # → ['Jiří Sládek']

opravene_zaznamy = oprav_zaznamy(zaznamy)
print(opravene_zaznamy) # → ['Pepa Novák', 'Jiří Sládek', 'Ivo Navrátil', 'Jan Poledník']
```

> [note]
> Snadný způsob jak zjistit, zda je řetězec složen jen z malých písmen,
> je metoda `islower()`, která vrací True, pokud řetězec obsahuje jen malá
> písmena, jinak vrací False. Například `'abc'.islower() == True` ale
> `'aBc'.islower() == False`.
>
> Snadný způsob jak převést první písmenko na velké je metoda `capitalize()`:
> např. `'abc'.capitalize() == 'Abc'`

{% filter solution %}
```python
def vyber_chybne(seznam):
    vysledek = []
    for zaznam in seznam:
        jmeno_a_prijmeni = zaznam.split(' ')
        jmeno = jmeno_a_prijmeni[0]
        prijmeni = jmeno_a_prijmeni[1]
        if jmeno[0].islower() or prijmeni[0].islower():
            vysledek.append(zaznam)
    return vysledek

def vyber_spravne(seznam):
    vysledek = []
    for zaznam in seznam:
        jmeno_a_prijmeni = zaznam.split(' ')
        jmeno = jmeno_a_prijmeni[0]
        prijmeni = jmeno_a_prijmeni[1]
        if not jmeno[0].islower() and not prijmeni[0].islower():
            vysledek.append(zaznam)
    return vysledek

def oprav_zaznamy(seznam):
    vysledek = []
    for zaznam in seznam:
        jmeno_a_prijmeni = zaznam.split(' ')
        jmeno = jmeno_a_prijmeni[0]
        prijmeni = jmeno_a_prijmeni[1]
        vysledek.append(jmeno.capitalize() + ' ' + prijmeni.capitalize())
    return vysledek
```
{% endfilter %}

## Seznamy a náhoda

Modul `random` obsahuje dvě funkce, které se hodí k seznamům.
Jako `random.randrange`, obě mají něco
společného s náhodou.

Funkce `shuffle` seznam „zamíchá” – všechny prvky náhodně popřehází.
Jako metoda `sort` i funkce `shuffle` nic nevrací.

```python
import random

balicek = []
for barva in '♠', '♥', '♦', '♣':
    for hodnota in list(range(2, 11)) + ['J', 'Q', 'K', 'A']:
        balicek.append(str(hodnota) + barva)
print(balicek)

random.shuffle(balicek)
print(balicek)
```

A funkce `choice` ze seznamu vybere jeden náhodný prvek.
S použitím seznamu tak můžeme výrazně zjednodušit
úvodní část naší staré hry kámen/nůžky/papír:

```python
import random
mozne_tahy = ['kámen', 'nůžky', 'papír']
tah_pocitace = random.choice(mozne_tahy)
```

## Vnořené seznamy

A perlička na konec!
Na začátku tohoto textu je napsáno, že seznam
může obsahovat jakýkoli typ hodnot.
Může třeba obsahovat i další seznamy:

```python
seznam_seznamu = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
```

Takový seznam se chová docela normálně – jdou
z něj třeba brát jednotlivé prvky
(které jsou ovšem taky seznamy):

```python
prvni_seznam = seznam_seznamu[0]
print(prvni_seznam)
```

A protože jsou prvky samy seznamy,
můžeme mluvit o věcech jako „první prvek druhého seznamu”:

```python
druhy_seznam = seznam_seznamu[1]
prvni_prvek_druheho_seznamu = druhy_seznam[0]
print(prvni_prvek_druheho_seznamu)
```

A protože výraz `seznam_seznamu[1]`
označuje seznam, můžeme brát prvky přímo z něj:

```python
prvni_prvek_druheho_seznamu = (seznam_seznamu[1])[0]
```

Neboli:

```python
prvni_prvek_druheho_seznamu = seznam_seznamu[1][0]
```

A má tahle věc nějaké použití, ptáš se?
Stejně jako vnořené cykly `for`
nám umožnily vypsat tabulku, vnořené seznamy
nám umožní si tabulku „zapamatovat”.

```python
def vytvor_tabulku(velikost=11):
    seznam_radku = []
    for a in range(velikost):
        radek = []
        for b in range(velikost):
            radek.append(a * b)
        seznam_radku.append(radek)
    return seznam_radku

nasobilka = vytvor_tabulku()

print(nasobilka[2][3])  # dva krát tři
print(nasobilka[5][2])  # pět krát dva
print(nasobilka[8][7])  # osm krát sedm

# Vypsání celé tabulky
for radek in nasobilka:
    for cislo in radek:
        print(cislo, end=' ')
    print()
```

Co s takovou „zapamatovanou” tabulkou?
Můžeš si do ní uložit třeba pozice
figurek na šachovnici nebo křížků a koleček
ve *2D* piškvorkách.
