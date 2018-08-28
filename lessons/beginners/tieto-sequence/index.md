## Sekvence (Sequence)

Jednou ze základních *datových struktur* v Pythonu je posloupnost (sekvence). Každému elementu v sekvenci je přiřazeno číslo, jeho index (pozice). První číslo je nula, druhé je jednička atd.

Dnes si povíme něco o sekvencích a také, jaké operace s nimi můžeme dělat. Popíšeme si některé operace, které můžeme dělat nad všemi sekvencemi, včetně seznamů a n-tic. Tyto operace fungují také s řetězci, o těch bude ale až příští lekce.

### Přehled sekvencí

Python má několik základních typů sekvencí. Mezi nejpoužívanější patří seznamy a n-tice.

Rozdíl mezi seznamy a n-ticemi je v tom, že seznamy lze měnit, zatímco n-tice ne. Proto se seznamy a n-tice používají pro jiné účely. Zatímco seznamy se používají tam, kde je vhodné nebo nutné měnit obsah nebo počet prvků v datové struktuře, n-tice se používá tam, kde je nopak žádoucí takové chování znemožnot.

Sekvence se používají tam, kde potřebujete vytvořit seznam hodnot. Můžete například vytvořit sekvenci, která obsahuje osobu v databázi, jako je na následujícím příkladu:

```
>>> john_doe = ['John Doe', 40]
>>> peter_smith = ['Peter Smith', 50]
>>> database = [john_doe, peter_smith]
>>> database
[['John Doe', 40], ['Peter Smith', 50]]
```

### Operace nad sekvencemi

Některé operace můžete provádět nad všemi sekvencemi. Mezi tyto operace patří *indexing*, *slicing*, *adding*, *multiplying* a kontrola členství. Python také má vestavěné funkce pro zjištění délky sekvence a nalezení největšího a nejmenšího prvku.

#### Indexování (Indexing)

Pamatujete, že řetězce jsou také sekvencemi? Můžeme použít příklad s řetězcem a ukázat si na něm indexování v praxi:

```
>>> greeting = 'Hello'
>>> greeting[0]
'H'
```

Jak vidíte, řetězec je jen sekvence znaků. Můžete přistupovat k jednotlivým prvkům pole pomocí indexu, který začíná nulou a končí *-1*. Přistoupit k poslední pozici v sekvenci proto můžeme takto:

```
>>> greeting[-1]
'o'
```

> [note]
> Vyzkoušejte přistoupit k prvku přímo, bez použití proměnné
> 
> ```
> >>> 'Hello'[1]
> 'e'
> ```

Také, pokud funkce vrací sekvenci, můžete přistoupit k hodnotě přímo:

```
>>> fourth = input('Year: ')[3]
Year: 2005
>>> fourth
'5'
```

#### Řez (Slicing)


Kromě toho, že můžete přistupovat k jednotlivým prvkům sekvence, můžete použít řez seznamem (slicing) a získat podmnožinu prvků. Abyste toho docílili, musíte použít místo jednoho dva indexy oddělené dvojtečkou.


```
>>> tag = '<a href="http://www.python.org">Python web site</a>'
>>> tag[9:30]
'http://www.python.org'
>>> tag[32:-4]
'Python web site'
```

První index je číslo indexu prvního prvku, který chcete zahrnout. Ale druhý index je číslo prvku v sekvenci *za* vaším řezem.

```
>>> numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
>>> numbers[3:6]
[4, 5, 6]
>>> numbers[0:1]
[1]
```

Další příklady:

```
>>> numbers[7:10]
[8, 9, 10]
```

Index č.10 (jedenáctý prvek pole) odkazuje na neexistující prvek pole. Proto můžem místo toho použít následující zápis pomocí negativní notace:

```
>>> numbers[-3:-1]
[8, 9]
```

Pokud zkusíme toto, nebude to fungovat, tak jak očekáváme:

```
>>> numbers[-3:0]
[]
```

Proto místo toho musíme použít tento zápis:

```
>>> numbers[-3:]
[8, 9, 10]
```

Totéž můžeme udělat v opačném směru:

```
>>> numbers[:3]
[1, 2, 3]
```

A pomocí následující syntaxe můžeme *zkopírovat* celou sekvenci (**její hodnoty**), například do jiné proměnné:

```
>>> numbers[:]
[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
```

> [note]
> Prosím vyzkoušejte si, jaký je rozdíl mezí následujícími příklady:
> 
> ```
> numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
> copy_numbers_variable = numbers
> slicing_numbers = numbers[:]
> ```
> Příjdete na to?
> 

Další možná ukázka slicingu je másledující:

```
url = input('Please enter the URL:')
domain = url[11:-4]

print("Domain name: " + domain)
```

```
Please enter the URL: http://www.python.org
Domain name: python
```

#### Řez po krocích

Jako volitelný parametr můžete použít délku kroku, kterým chcete řez vytvořit:

```
>>> numbers[0:10:1]
[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
```

```
>>> numbers[0:10:2]
[1, 3, 5, 7, 9]
```

#### Slučování sekvencí

Sekvence mohou být slučovány pomocí znaku plus.

```
>>> [1, 2, 3] + [4, 5,  6]
[1, 2, 3, 4, 5, 6]
>>> 'Hello,' + 'world!'
'Hello, world!'
```

#### Multiplikační operátor

```
>>> z = [3, 1] * 2
>>> z
[3, 1, 3, 1]
```

Pokud byste chtěli vytvořit prázdný seznam s místem pro tři prvky, můžete to udělat takto:

```
>>> s = [None] * 3
>>> s
[None, None, None]
```

#### Zjištění prvku v sekvenci (Membership)

Abychom zjistili, zda je nějaký prvek prkem sekvence, použijeme operátor *in*. Tento operátor ověřuje, zda je něco pravdivé nebo ne a podle toho vrací návratovou hodnotu *True/False*. 

>[note]
>True a False jsou tzv. logické operátory

```
>>> 3 in [1, 2, 3, 4, 5]
True
>>> 3 not in [1, 2, 3, 4, 5]
False
```

```
>>> 'P' in 'Python'
True
```

#### Délka sekvence, nalezení minima a maxima

```
>>> numbers = [100, 34, 678]
>>> len(numbers)
3
>>> max(numbers)
678
>>> min(numbers)
34
>>> max(2, 3)
3
>>> min(9, 3, 2, 5)
2
```

