Encyklopedické informace z této stránky shrnuje
[Tahák na seznamy](https://github.com/pyvec/cheatsheets/blob/master/lists/lists-cs.pdf),
který si můžeš vytisknout.

# Seznamy

Dnes si ukážeme, jak pracovat se *seznamy* (angl. *lists*).

Začneme prakticky.
Vytvoř si seznam pomocí následujícího kódu:

```python
zviratka = ['pes', 'kočka', 'králík']
print(zviratka)
```

> [note]
> Nemůžeš najít hranaté závorky?
> Na české klávesnici zkus pravý <kbd>Alt</kbd> + <kbd>F</kbd> a <kbd>G</kbd>.

Seznam je hodnota, která může obsahovat spoustu dalších hodnot.
Tak jako řetězec obsahuje sekvenci znaků,
seznam obsahuje sekvenci jakýchkoli hodnot.
V našem případě obsahuje sekvenci řetězců.

A tak jako můžeš pomocí cyklu `for` procházet řetězec po znacích,
seznam můžeš procházet po jednotlivých prvcích:

```python
for zviratko in zviratka:
    print(zviratko)
```

Seznamy se v programech vyskytují často:
soubor se dá načíst jako seznam řetězců s jednotlivými řádky,
seznam řetězců jako `'7♥'` a `'K♣'` může posloužit jako balíček karet,
matematika je plná číselných řad, e-shopy pracují se seznamy zboží.

Hodnoty v seznamu můžou být jakéhokoli typu:

```python
prvni_prvocisla = [2, 3, 5, 7, 11]
```

Dokonce můžeš různé typy míchat v jednom seznamu.
(S takovými namixovanými seznamy se ovšem příliš často nesetkáš.
Různé typy hodnot se používají spíš v <var>n</var>-ticích, o kterých si povíme
později):

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
Metoda `upper()` vytvoří a vrátí *nový* řetězec `'ŽANETA'`.
Výsledná hodnota se ale v našem programu nevyužije – Python ji vypočítá,
ale pak ji „zahodí“.

Oprava je snadná: výsledek si ulož do proměnné.
Často budeš chtít takový výsledek uložit zpátky do původní proměnné:

```python
kamaradka = kamaradka.upper()
```

Tímto přiřazením Python „zahodí“ původní hodnotu,
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
seznam, se kterým pracuje. Vyzkoušej si to:

```pycon
>>> zviratka = ['pes', 'kočka', 'králík']
>>> print(zviratka)
['pes', 'kočka', 'králík']
>>> zviratka.append('morče')
>>> print(zviratka)
['pes', 'kočka', 'králík', 'morče']
```

Všimni si, že proměnná `zviratka` se nastavuje jen na začátku.
V rámci celého běhu programu výše existuje jen jeden seznam.
Na začátku má tři prvky, pak mu jeden přibude, ale stále je to jeden a ten
samý seznam.

Takové měnění může být občas překvapující,
protože stejná hodnota může být přiřazená ve více proměnných.
Protože se mění hodnota samotná, může to vypadat,
že se „mění proměnná, aniž na ni sáhneš”:

```python
a = [1, 2, 3]   # Vytvoření seznamu
b = a           # Tady se nový seznam nevytváří!

# seznam vytvořený v prvním řádku má teď dvě jména: "a" a "b",
# ale stále pracuješ jenom s jedním seznamem

print(b)
a.append(4)
print(b)
```


## Další způsoby, jak měnit seznamy

Kromě metody `append`, která přidává jediný prvek na konec, existuje
spousta dalších metod, které seznamy mění.
Všechny udělají změny přímo v daném seznamu a (kromě `pop`) vrací `None`:

* `extend()` přidá více prvků najednou,
* `insert()` přidá prvek na danou pozici,
* `pop()` odebere poslední prvek a *vrátí ho* (jako návratovou hodnotu),
* `remove()` odstraní první výskyt daného prvku,
* `sort()` seznam seřadí (řetězce podle “abecedy”, čísla vzestupně),
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
Stejně jako u řetězců se čísluje od nuly a záporná čísla číslují od konce.

```python
zviratka = ['pes', 'kočka', 'králík']
print(zviratka[2])
```

Hranatými závorkami můžeš získat i podseznam.
[Diagram z materiálů k řetězcům]({{ lesson_url('beginners/str-index-slice')}}#slicing-diagram)
ukazuje, jak u takového „sekání” číslovat:
funguje to stejně, jen místo menšího řetězce dostaneš menší seznam.

```python
print(zviratka[2:-3])
```

„Sekáním“ vzniká nový seznam – když pak ten původní změníš, v novém menším seznamu se
to neprojeví.


### Měnění prvků

Na rozdíl od řetězců (které se měnit nedají) můžeš u existujících seznamů
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
print(zviratka[1:-1])
zviratka[1:-1] = ['koťátko', 'králíček', 'hádě']
print(zviratka)
```

### Mazání prvků

Přiřazením do podseznamu můžeš i změnit délku
seznamu nebo některé prvky úplně odstranit:

```python
zviratka = ['pes', 'kočka', 'králík']
zviratka[1:-1] = ['had', 'ještěrka', 'drak']
print(zviratka)
zviratka[1:-1] = []
print(zviratka)
```

Tenhle zápis pro mazání prvků je ale docela nepřehledný.
Proto na to existuje zvláštní příkaz jménem `del`.
Jak už jeho název (z angl. *delete*, smazat)
napovídá, smaže, co mu přijde pod ruku – jednotlivé
prvky seznamů, podseznamy, … a dokonce i proměnné!
Zkus si:

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

Na mazání prvků můžeš použít i metody zmíněné výše:
* `pop` odstraní poslední prvek v seznamu a *vrátí* ho,
* `remove` najde v seznamu první výskyt daného prvku a odstraní ho,
* `clear` vyprázdní celý seznam.

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

Metoda `sort` seřadí prvky seznamu.

```python
seznam = [4, 7, 8, 3, 5, 2, 4, 8, 5]
seznam.sort()
print(seznam)
```

Aby se daly seřadit, musí být prvky seznamu vzájemně
*porovnatelné* – konktrétně na ně musí fungovat operátor `<`.
Seznam s mixem čísel a řetězců tedy seřadit nepůjde.
Operátor `<` definuje i jak přesně `sort` řadí: čísla vzestupně podle
velikosti; řetězce podle speciální „abecedy” která řadí
velká písmena za malá, česká až za anglická, atd.

Metoda `sort` zná pojmenovaný argument `reverse`.
Pokud ho nastavíš na *True*, řadí se naopak – od největšího prvku po nejmenší.

```python
seznam = [4, 7, 8, 3, 5, 2, 4, 8, 5]
seznam.sort(reverse=True)
print(seznam)
```

## Známé operace se seznamy

Spousta toho, co můžeš dělat s řetězci, má stejný
účinek i u seznamů.
Třeba sečítání a násobení číslem:

```python
melodie = ['C', 'E', 'G'] * 2 + ['E', 'E', 'D', 'E', 'F', 'D'] * 2 + ['E', 'D', 'C']
print(melodie)
```

Stejně jako u řetězců jde sečítat jen seznam
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
Takže ačkoliv melodie výše obsahuje prvky
`'D'` a `'E'` vedle sebe, `'DE'` ani `['D', 'E']` v seznamu není:

```python
print('DE' in melodie)
print(melodie.count('DE'))
print(melodie.index('DE'))
```

## Seznam jako podmínka

Seznam můžeš použít v příkazu `if` (nebo `while`) jako podmínku,
která platí, když v tom seznamu něco je.
Jinými slovy, `seznam` je tu „zkratka“ pro `len(seznam) > 0`.

```python
if seznam:
    print('V seznamu něco je!')
else:
    print('Seznam je prázdný!')
```

Podobně můžeš v podmínce použít i řetězce.
A dokonce i čísla – ta jako podmínka platí, pokud jsou nenulová.

## Tvoření seznamů

Tak jako funkce `int` převádí na
celá čísla a `str` na řetězce,
funkce `list` převádí na seznam.
Jako argument jí můžeš předat jakoukoli hodnotu,
kterou umí zpracovat příkaz `for`.
Z řetězce udělá seznam znaků, z `range` udělá seznam čísel.

```python
abeceda = list('abcdefghijklmnopqrstuvwxyz')
cisla = list(range(100))
print(abeceda)
print(cisla)
```

I ze seznamu udělá funkce `list` seznam.
To může znít zbytečně, ale není – vytvoří se totiž *nový* seznam.
Bude mít sice stejné prvky ve stejném pořadí,
ale nebude to ten samý seznam:
měnit se bude nezávisle na tom starém.

```python
a = [1, 2, 3]
b = list(a)

print(b)
a.append(4)
print(b)
print(a)
```

Další způsob, jak tvořit seznamy
(zvláště složitější), je nejdřív udělat prázdný
seznam a pak ho postupně naplnit pomocí funkce `append`.
Třeba pokud z nějakého důvodu chceš seznam
mocnin dvou, projdi čísla, kterými chceš mocnit,
cyklem `for` a pro každé z nich
do seznamu přidej příslušnou mocninu:

```python
mocniny_dvou = []
for cislo in range(10):
    mocniny_dvou.append(2 ** cislo)
print(mocniny_dvou)
```

Podobným způsobem získáš seznam seznam `matka`, `babička`, `prababička`,
`praprababička`, atd.:

```python
predkove = ['matka']
for pocet_pra in range(10):
    predkove.append(('pra' * pocet_pra) + 'babička')
print(predkove)
```

Chceš-li seznam, který reprezentuje balíček karet,
zavolej `append` pro všechny kombinace barev a hodnot:

```python
balicek = []
for barva in '♠', '♥', '♦', '♣':
    for hodnota in ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']:
        balicek.append(hodnota + barva)
print(balicek)
```

> [note] Jde to líp?
> Psát do programu výčet po sobě jdoucích čísel,
> `'2', '3', '4', '5', '6', '7', '8', '9', '10'`,
> není ideální – na takovou otročinu přece máme počítače!
> Zkus čísla dostat pomocí `range`.
> Ale pozor, není to úplně přímočaré:
>
> * Jaké argumenty dáš funkci `range`, abys dostal{{a}} čísla od 2 do 10?
> * Funkce `range` vrací sekvenci, která ale není seznam.
>   Abys ji mohl{{a}} spojit se seznamem `['J', 'Q', 'K', 'A']`, budeš ji muset
>   na seznam převést: `list(range(...))`
> * Abys mohl{{a}} čísla z `range` připojit k řetězci jako `♠`, budeš muset
>   každou hodnotu před použitím převést na řetězec: `str(hodnota)`.
>
> Bonus: Jaký je nejkratší zápis, kterým můžeš zadat seznam
> `['J', 'Q', 'K', 'A']`?
>
> Řešení najdeš v textu o kousek níže.


## Seznamy a řetězce

Seznamy a řetězce jsou druhy *sekvencí*.
Můžeš různě převádět z jednoho typu na druhý.

Funkce `list` vytvoří z řetězce seznam znaků.
Když chceš dostat seznam slov, použij
na řetězci metodu `split` (angl. *rozdělit*):

```python
slova = 'Tato věta je složitá, rozdělme ji na slova!'.split()
print(slova)
```

Metoda `split` umí brát i argument.
Pokud ho předáš, řetězec „rozseká” daným oddělovačem
(místo mezer a nových řádků).
Takže když máš nějaká data oddělená čárkami,
použíj `split` s čárkou:

```python
zaznamy = '3A,8B,2E,9D'.split(',')
print(zaznamy)
```

Chceš-li spojit seznam řetězců zase dohromady
do jediného řetězce, použij metodu `join` (angl. *spojit*).
Pozor, tahle metoda se volá na *oddělovači*,
tedy na řetězci, kterým se jednotlivé kousky „slepí” dohromady.
Seznam jednotlivých řetězců bere jako argument.

```python
veta = ' '.join(slova)
print(veta)
```

## Seznamy a náhoda

Modul `random` obsahuje funkce, které mají něco společného s náhodou:
třeba nám už známou `random.randrange`.
Podívejme se na dvě další, které se hodí k seznamům.

Funkce `shuffle` seznam „zamíchá” – všechny prvky náhodně popřehází.
Seznam změní „na místě“ a nic nevrací (podobně jako metoda `sort`).

```python
import random

ciselne_hodnoty = list(range(2, 11))
pismenne_hodnoty = list('JQKA')

balicek = []
for barva in '♠', '♥', '♦', '♣':
    for hodnota in ciselne_hodnoty + pismenne_hodnoty:
        balicek.append(str(hodnota) + barva)
print(balicek)

random.shuffle(balicek)
print(balicek)
```

A funkce `choice` ze seznamu vybere jeden náhodný prvek.
S použitím seznamu tak můžeš třeba jednoduše vybrat tah pro hru
kámen/nůžky/papír:

```python
import random
mozne_tahy = ['kámen', 'nůžky', 'papír']
tah_pocitace = random.choice(mozne_tahy)
print(tah_pocitace)
```
