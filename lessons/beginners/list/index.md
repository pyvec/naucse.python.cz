Encyklopedické informace z této stránky shrnuje
[Tahák na seznamy](https://github.com/pyvec/cheatsheets/blob/master/lists/lists-cs.pdf),
který si můžeš vytisknout.

# Seznamy

Dnes si ukážeme, jak pracovat se *seznamy* (angl. *lists*).
Zapisují se hranatými závorkami:

```python
zviratka = ['pes', 'kočka', 'králík']
print(zviratka)
```

> [note]
> Nemůžeš najít hranaté závorky?
> Na české klávesnici zkus pravý <kbd>Alt</kbd> + <kbd>F</kbd> a <kbd>G</kbd>.

Seznam je hodnota, která může obsahovat spoustu dalších hodnot.
Tak jako řetězec obsahuje sekvenci znaků,
seznam obsahuje sekvenci... čehokoliv. Třeba slov (řetězců).
A tak jako můžeme pomocí cyklu `for`
procházet řetězec po znacích,
seznam můžeme procházet po jednotlivých prvcích:

```python
for zviratko in zviratka:
    print(zviratko)
```

Seznamy se v programech vyskytují velice často:
soubor se dá načíst jako seznam řetězců
s jednotlivými řádky,
seznam řetězců jako `'7♥'`
a `'K♣'` může posloužit jako balíček karet,
matematika je plná číselných řad,
každá online služba má seznam uživatelů.


Hodnoty v seznamu můžou být jakéhokoli typu.
Dokonce můžeme různé typy míchat v jednom seznamu
(i když s takovými namixovanými seznamy se
příliš často nesetkáme – více se různé typy hodnot
používají v <var>n</var>-ticích, o kterých si povíme později):

```python
seznam = [1, 'abc', True, None, range(10), len]
print(seznam)
```

## Neměnitelné hodnoty

Důležitá vlastnost seznamů je, že se dají *měnit*.

Než vysvětlíme o co jde, připomeňme si jak fungují hodnoty, které se měnit
nedají – např. čísla, řetězce, `True`/`False`/`None`.

Vyzkoušej si následující kousek kódu. Co je na něm „špatně“?

```python
kamaradka = 'Žaneta'
print(kamaradka)
kamaradka.upper()
print(kamaradka)
```

Proměnná `kamaradka` obsahuje řetězec `'Žaneta'` (který se už nedá změnit).
Metoda `upper()` vytvoří a vrátí *nový* řetězec.
Výsledná hodnota se ale v našem programu nevyužije – Python ji vypočítá,
ale pak na ni „zapomene“.

Oprava je snadná: výsledek uložit do proměnné.
Často budeš chtít takový výsledek uložit do původní proměnné:

```python
kamaradka = kamaradka.upper()
```

Tímto přiřazením Python „zapomene“ na původní hodnotu,
a od tohoto příkazu dál bude proměnná `kamaradka` označovat nový řetězec.

Podobně by se dala proměnná přenastavit na jakoukoli jinou hodnotu:

```python
kamaradka = 'Žaneta'
print(kamaradka)
kamaradka = 'Alexandra'
print(kamaradka)
```


## Měnění seznamů

A jak jsou na tom seznamy?
Ty se měnit dají.

Základní způsob, jak změnit seznam, je přidání
prvku na konec pomocí metody `append`.
Ta *nic nevrací* (resp. vrací `None`), ale „na místě” (angl. *in place*) změní
seznam, na kterém pracuje. Vyzkoušej si to:

```pycon
>>> zviratka = ['pes', 'kočka', 'králík']
>>> print(zviratka)
['pes', 'kočka', 'králík']
>>> zviratka.append('morče')
>>> print(zviratka)
['pes', 'kočka', 'králík', 'morče']
```

Všimni si, že proměnná `zviratka` se nastavuje jen na začátku.
V celém programu výše jen jeden seznam – na začátku má tři prvky, pak
mu jeden přibude, ale stále je to jeden a ten samý seznam.

Takové měnění může být občas překvapující,
protože stejná hodnota může být přiřazená ve více proměnných.
Protože se mění hodnota samotná, může to vypadat,
že se „mění proměnná, aniž na ni sáhneme”:

```python
a = [1, 2, 3]   # Vytvoření seznamu
b = a           # Tady se nový seznam nevytváří!

# seznam vytvořený v prvním řádku má teď dvě jména: "a" a "b",
# ale stále pracujeme jenom s jedním seznamem

print(b)
a.append(4)
print(b)
```

## Další způsoby, jak měnit seznamy

Kromě metody `append`, která přidává jediný prvek na konec, existuje
spousta metod, které mění seznamy.
Všechny udělají přímo v daném seznamu, a (kromě `pop`) vrací `None`:

* `extend()` přidá více prvků najednou,
* `insert()` přidá prvek na danou pozici,
* `pop()` odebere *a vrátí* poslední prvek,
* `remove()` odstraní první výskyt daného prvku,
* `sort()` seznam seřadí (řetězce “podle abecedy”, čísla vzestupně),
* `reverse()` obrátí pořadí prvků,
* `clear()` odstraní všechny prvky.

{{ figure(img=static('methods.svg'), alt="Tahák") }}

Například:

```python
zviratka = ['pes', 'kočka', 'králík']
zviratka.append('morče')      # ['pes', 'kočka', 'králík', 'morče']
zviratka.insert(2, 'had')     # ['pes', 'kočka', 'had', 'králík', 'morče']
zviratka.pop()                # ['pes', 'kočka', 'had', 'králík'], vrátí 'morče'
zviratka.remove('had')        # ['pes', 'kočka', 'králík']
zviratka.sort()               # ['kočka', 'králík', 'pes']
zviratka.reverse()            # ['pes', 'králík', 'kočka']
zviratka.clear()              # []
```

## Vybírání ze seznamů

Často budeš ze seznamu chtít vybrat prvek na určité pozici.
To funguje jako u řetězců: do hranatých závorek dáš číslo prvku.
Stejně jako u řetězců se čísluje od nuly a záporná čísla označují prvky
od konce.

```python
zviratka = ['pes', 'kočka', 'králík']
print(zviratka[2])
```

Hranatými závorkami můžeš získat i podseznam.
[Diagram z materiálů k řetězcům]({{ lesson_url('beginners/str')}}#slicing-diagram)
ukazuje, jak u takového „sekání” číslovat:
funguje to stejně, jen místo menšího řetězce
dostaneš menší seznam.

```python
print(zviratka[2:-3])
```

„Sekáním“ vzniká nový seznam – když pak ten původní změníš, v podseznamu se
to neprojeví.


### Měnění prvků

Na rozdíl od řetězců (které se nedají měnit) můžeš u existujících seznamů
nastavovat konkrétní prvky – a to tak, že do prvku přiřadíš jako by to byla
proměnná:

```python
zviratka = ['pes', 'kočka', 'králík']
zviratka[1] = 'koťátko'
print(zviratka)
```

Přiřazovat se dá i do podseznamu – v tomto případě
se podseznam nahradí jednotlivými prvky z toho,
co přiřadíš.

```python
zviratka = ['pes', 'kočka', 'králík', 'had', 'andulka']
print([1:-1])
zviratka[1:-1] = ['koťátko', 'králíček', 'hádě']
print(zviratka)
```

### Mazání prvků

Přiřazením do podseznamu se dá i změnit délka
seznamu, nebo některé prvky úplně odstranit:

```python
zviratka = ['pes', 'kočka', 'králík']
zviratka[1:-1] = ['had', 'ještěrka', 'drak']
print(zviratka)
cisla[1:-1] = []
print(zviratka)
```

Tenhle zápis pro mazání prvků je ale docela
nepřehledný, a proto na to máme zvláštní příkaz jménem `del`.
Jak už jeho název (z angl. *delete*, smazat)
napovídá, smaže, co mu přijde pod ruku – jednotlivé
prvky seznamů, podseznamy, … a dokonce i proměnné!

```python
zviratka = ['pes', 'kočka', 'králík', 'had', 'ještěrka', 'andulka']

print(zviratka[-1])
del zviratka[-1]
print(zviratka)

print(zviratka[1:-1])
del zviratka[1:-1]
print(zviratka)

del zviratka
print(zviratka)
```

Nebo můžeš použít mazací metody zmíněné výše:
* `pop`, která odstraní *a vrátí* poslední prvek v seznamu,
* `remove`, která najde v seznamu první výskyt daného prvku a odstraní ho,
* `clear`, která vyprázdní celý seznam.

```python
balicek = ['eso', 'sedma', 'svršek', 'sedma', 'král']
liznuta_karta = karty.pop()
print(liznuta_karta)
print(balicek)

balicek.remove('sedma')
print(balicek)

balicek.clear()
print(balicek)
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
Funkce `list` vytvoří z řetězce seznam znaků.
Když chceme dostat seznam slov, použijeme
na řetězci metodu `split` (angl. *rozdělit*):

```python
slova = 'Tato věta je složitá, rozdělme ji na slova!'.split()
print(slova)
```

Metoda `split` umí brát i argument.
Pokud ho předáme, místo mezer (a nových řádků)
se řetězec „rozseká” daným oddělovačem.
Takže když máš nějaká data oddělená čárkami,
použíj `split` s čárkou:

```python
zaznamy = '3A,8B,2E,9D'.split(',')
print(zaznamy)
```

Chceš-li spojit seznam řetězců zase dohromady
do jediného řetězce, použij metodu `join` (angl. *spojit*).
Pozor, tahle metoda se volá na *oddělovači*,
tedy řetězci, kterým se jednotlivé kousky „slepí”
dohromady; a jako argument bere seznam jednotlivých
řetězců.

```python
veta = ' '.join(slova)
print(veta)
```

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
S použitím seznamu tak můžeš třeba jednoduše vybrat tah pro hru
kámen/nůžky/papír:

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
