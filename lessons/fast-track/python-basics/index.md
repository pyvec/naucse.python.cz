# Úvod do Pythonu

> Tento text je založen na materiálech [Django Girls](https://tutorial.djangogirls.org/cs/python_introduction/) a [Geek Girls Carrots](https://github.com/ggcarrots/django-carrots).

Pojď napsat nějaký kód!

## Interaktivní režim Pythonu

Chceš-li si začít hrát s Pythonem, otevři *příkazový řádek* a aktivuj virtuální prostředí.  Zkontroluj si, že na začátku příkazové řádky ti svítí `(venv)`.

Je-li tomu tak, nezbývá než – konečně – pustit Python. K tomu použij příkaz `python`:

``` console
$ python3
Python 3.6.6 (...)
Type "help", "copyright", "credits" or "license" for more information.
>>>
```

Příkaz vypíše několik informací. Z prvního řádku se můžeš ujistit, že používáš Python 3. (Vidíš-li číslo jako `2.7.11`, něco je špatně – popros o radu kouče.)

Třemi „zobáčky“ ``>>>` pak Python poprosí o instrukce. Je to jako v příkazové řádce, ale místo příkazů jako `cd` a `mkdir` sem budeš psát příkazy Pythonu.

Jako první instrukci použijeme Pythonu jako kalkulačku.
Za tři zobáčky napiš třeba `2 + 3` a zmáčkni <kbd>Enter</kbd>.

``` pycon
>>> 2 + 3
5
```

Zobrazila se ti správná odpověď?
Pokud ano, gratuluji! První příkaz v Pythonu máš za sebou.

Zkusíš i odečítání?

A jak je to s násobením?
{# XXX: Jak zapsat násobení? `4 x 5` `4 . 5` `4 × 5` `4 * 5` -#}
Na kalkulačce bys zadala `4 × 5`, což se na klávesnici píše špatně.
Python proto používá symbol `*` a pro dělení `/`.
Tyhle symboly se odborně nazývají *operátory*.

``` pycon
>>> 4 * 5
20
>>> 5 / 2
2.5
```

> [note]
> V tomto úvodu budeme zadávat jen celá čísla.
> Dělením ale může vzniknout třeba dva a půl
> (tedy `2.5` – Python používá desetinnou *tečku*).
> Z důvodů, do kterých teď nebudeme zabíhat, se desetinné pozice po dělení
> objeví i když vyjde celé číslo:
> ``` pycon
> >>> 4 / 2
> 2.0
> ```

{# XXX:
Kolik je
<math mode="display" style="display:inline-box;" xmlns="http://www.w3.org/1998/Math/MathML"><mfrac><mrow><mn>123</mn> + <mn>456</mn></mrow><mrow><mn>789</mn></mrow></mfrac></math>?
#}

> [style-note]
> Mezery mezi čísly a znamínkem nejsou nutné: `4*5` i `4       * 5` dělá
> to samé co `4 * 5`.
> Je ale zvykem psát kolem operátoru jednu mezeru z každé strany – tak jako
> v těchto materiálech.
> Kód je pak čitelnější.


## Řetězce

Čísla jsou pro počítače dost užitečná (ostatně slovo *počítač* to naznačuje),
ale Python umí pracovat i s jinými druhy informací.
Třeba s textem.

Zkus si to: zadej své jméno do uvozovek, jak vidíš níže:

``` pycon
>>> 'Ola'
'Ola'
```

Nyní jsi vytvořil{{a}} svůj první *řetězec*!
Řetězec je programátorský termín pro *text* – posloupnost znaků (písmenek), které mohou být zpracovány počítačem.

Když řetězec zadáváš, musíš ho vždy uzavřít do uvozovek (apostrofů).
Jinak by Python nepoznal, co je text a co jsou instrukce.

{# XXX: Assessment here: adding strings together #}

Řetězce se dají spojovat – „sečítat“ – pomocí `+`. Zkus toto:

``` pycon
>>> 'Já jsem ' + 'Ola'
'Já jsem Ola'
```

> [note]
> Pozor na mezeru! Když zadáš `'Já jsem'+'Ola'`, spojí se ti dvě slova
> dohromady.
> Počítač považuje i mezeru za *znak*; chová se k ní stejně jako k jakémukoli
> písmenku.
> Když nedáš mezeru do uvozovek, nebude součástí řetězce.
>
> Zkus si:
>
> ``` pycon
> >>> 'Já jsem' + ' ' + 'Ola'
> 'Já jsem Ola'
> ```

Také můžeš řetězce opakovat – násobit číslem:

``` pycon
>>> 'Ola' * 3
'OlaOlaOla'
```

### Uvozování

A co když budeš chtít dát dovnitř do svého řetězce apostrof?
Můžeš kolem řetězce použít dvojité uvozovky:

``` pycon
>>> "To bych řek', že jsou pořádně praštěný!"
"To bych řek', že jsou pořádně praštěný!"
```

Pythonu je jedno, se kterým druhem uvozovek řetězec zadáš.
Podstatná jsou jen písmenka uvnitř.
Když Python řetězec vypisuje, může si vybrat jiný druh uvozovek
než jsi použil{{a}} ty:

``` pycon
>>> "Ola"
'Ola'
```

### Funkce a metody

Už umíš řetězce „sčítat“ pomocí `+` (`'Ahoj ' + 'Olo!'`)
a „násobit“ pomocí `*` (`'la' * 3`).
Na všechny ostatní věci, které se s textem dají dělat,
ale na klávesnici není dost symbolů.
Proto jsou některé operace pojmenované slovně – třeba takzvané *funkce*.

Chceš-li znát počet písmen ve svém jméně, zavolej funkci `len`.
Napiš `len` (bez uvozovek), pak kulaté závorky, a do těch závorek
své jméno (jako řetězec – v uvozovkách):

``` pycon
>>> len('Ola')
3
```

{# XXX: Existuje funkce `type`. Jak bych ji zavolal? #}

Kromě funkcí existují *metody*, které se zapisují trochu jinak.

Chceš-li vidět své jméno velkými písmeny, zavolej metody `upper`.
Napiš řetězec, pak tečku, jméno metody `upper` (bez uvozovek) a prázdné
závorky:

``` pycon
>>> 'Ola'.upper()
'OLA'
```

Zkus si zavolat metodu `lower`.

{# XXX: Existuje funkce `type`. Jak bych ji zavolal? #}

Co je metoda (které voláš s `.`, jako `'Ola'.upper()`) a co je funkce
(kde vložíš informaci do závorek jako (`len('Ola')`)

### Shrnutí

OK, dost bylo řetězců. Co ses zatím naučil{{a}}:

*   **Interaktivní režim Pythonu** umožňuje zadávat příkazy (kód) pro
    Python a zobrazuje výsledky/odpovědi.
*   **Čísla a řetězce** se používají na matematiku a práci s textem.
*   **Operátor** jako `+` a `*` kombinuje hodnoty a vytvoří výsledek.
*   **Funkce** a **metody** jako `len()` a `upper()` provádí na hodnotách
    nějaké akce.

Čísla, řetězce a operátory a funkce jsou základy většiny programovacích jazyků.

Připraven{{a}} na něco dalšího? Vsadíme se, že ano!


## Skládání

Volání funkce nebo metody můžeš použít jako jinou hodnotu.

Nech Python spočítat matematický výraz `(1 + 3) / 2`:

```pycon
>>> (1 + 3) / 2
2.0
```

Python napřed sečte `1 + 3` a vyjde mu 4.
Čtverku doplní místo `1 + 3` do původního příkladu, a dostane `4 / 2`.
To vydělí a dostane `2`.

Neboli: `(1 + 3) / 2` = `4 / 2` = `2`

Zkus se zamyslet, jak Python zpracuje tyto výrazy:

```pycon
>>> len('Ola') + 1
4
```

```pycon
>>> 'Já jsem ' + 'Ola'.upper()
'Já jsem OLA'
```

```pycon
>>> len('Ola'.upper())
4
```

```pycon
>>> len('Ola' * 3)
9
```

{% filter solution() %}
`'Já jsem ' + 'Ola'.upper()` → `'Já jsem ' + 'OLA'` → `'Já jsem OLA'`

`len('Ola') + 1` → `3 + 1` → `4`

`len('Ola'.upper())` → `len('OLA')` → `3`

`len('Ola' * 3)` → `len('OlaOlaOla')` → `9`
{% endfilter %}


Podobné skládání je v programování velice časté.
Většinu základních stavebních bloků se začátečník naučí za pár
týdnů – a pak je po celou svou progrmátorskou kariéru skládá do
složitějších a složitějších konstrukcí.


## Chyby

Pojď zkusit něco nového: zjistit délku čísla stejným způsobem,
jakým jsme zjišťovali délku našeho jména.
Zadej `len(304023)` a stiskni <kbd>Enter</kbd>:

``` pycon
>>> len(304023)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: object of type 'int' has no len()
```

{# XXX: tohle nebude první chyba... #}
Zobrazila se ti naše první chyba!
Ta říká, že objekty typu `int` (zkratka anglického *integer*, celé číslo)
nemají délku.
Tak co můžeme udělat teď?
Možná můžeme zkusit napsat naše číslo jako řetězec?
Řetězce mají délky, že?

```pycon
>>> len("304023")
6
```

Existuje i funkce, která *převede* číslo na řetězec. Jmenuje se `str`:

```pycon
>>> str(304023)
"304023"
>>> len(str(304023))
6
```

Podobně funkce `int` převádí věci na celá čísla:

```pycon
>>> int("304023")
```

Můžeš převést čísla na text, ale nemůžeš jen tak převést text na čísla.
Co by se stalo, kdyby ses pokusil{{a}} na číslo převést řetězec, ve kterém
nejsou číslice?

{% filter solution() %}
``` pycon
>>> int('hello')
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
ValueError: invalid literal for int() with base 10: 'ahoj'
```
{% endfilter %}

## Proměnné

Důležitým konceptem v programování jsou *proměnné*.
Proměnná není nic jiného než *pojmenování* něčeho,
co budeme chtít použít později.
Programátoři proměnné používají k ukládání dat,
aby byl jejich kód čitelnější a nemuseli si pamatovat konkrétní hodnoty.

Řekněme, že chceš vytvořit novou proměnnou s názvem `jmeno`.
To se zapíše takto:

``` pycon
>>> jmeno = 'Ola'
```

Proměnná `jmeno` teď bude mít hodnotu `'Ola'`.

Jak sis mohl{{a}} všimnout, tenhle příkaz nic nevrátil – Python nevypsal
žádný výslede.
Jak tedy víme, že proměnná skutečně existuje?

Zadej samotné jméno proměnné (tedy `jmeno`) a stiskni <kbd>Enter</kbd>:

``` pycon
>>> jmeno
'Ola'
```

Zkus si nastavit i jinou proměnnou – třeba svoji oblíbenou barvu:

``` pycon
>>> barva = 'modrá'
>>> barva
'modrá'
```

Kdykoli můžeš do proměnné přiřadit znovu, a změnit tak co se pod
daným jménem skrývá:

``` pycon
>>> jmeno
'Ola'
>>> jmeno = "Soňa"
>>> jmeno
'Soňa'
```

Můžeš ji také použít ve funkcích:

``` pycon
>>> len(jmeno)
4
```

Super, ne?
Proměnná může obsahovat cokoliv, například také čísla!
Zkus tohle:

``` pycon
>>> sirka = 4
>>> delka = 6
>>> sirka * delka
24
```

Ale co když použiješ nesprávné jméno? Dokážeš odhadnout, co se stane?

{% filter solution %}
``` pycon
>>> mesto = "Tokyo"
>>> mmesto
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
NameError: name 'mmesto' is not defined
```
{% endfilter %}

Chyba!

Python má různé typy chyb. Tato se nazývá `NameError`.
Python ti vrátí tuto chybu, pokud se pokusíš použít proměnnou,
která dosud nebyla nastavena.
Pokud někdy dojde k této chybě, zkontroluj svůj kód, abys zjistil{{a}},
jestli jsi někde neudělal{{a}} překlep.

> [note] Jména proměnných
> Profesionální programátoři pojmenovávají proměnné anglicky,
> aby jim rozuměli co nejvíc kolegů po celém světě.
> Ze začátku ale doporučujeme češtinu – je tak jasnější, která jména
> si můžeš zvolit {{gnd('sám', 'sama')}} (např. `barva`) a která jsou
> z Pythonu (např. `upper`).
>
> Je ovšem dobré se nepoužívat diakritiku a vyhnout se velkým pímenům:
> místo `Jméno` použij jen `jmeno`.

## Seznamy

Vedle řetězců a celých čísel má Python další druhy hodnot.

Teď se podíváme na jeden, který se nazývá *seznam* (anglicky *list*).
To je hodnota, která v sobě obsahuje jiné hodnoty.

{# Anglické termíny všude! #}

Seznamy se zadávají tak, že dáš několik hodnot, oddělených čárkami,
do hranatých závorek.
Zkus si vytvořit třeba seznam čísel z loterie:

``` pycon
>>> [3, 42, 12, 19, 30, 59]
[3, 42, 12, 19, 30, 59]
```

Abys s takovým seznamem mohl{{a}} pracovat,
ulož si ho do proměnné:

``` pycon
>>> loterie = [3, 42, 12, 19, 30, 59]
```

Dobrá, máme seznam! Co s ním můžeme dělat?
Podíváme se, kolik čísel v seznamu je.
Dá se na to použít funkce, kterou už znáš.
Tipneš si, která to je?

{% filter solution %}
``` pycon
>>> len(loterie)
6
```

Funkce `len()` umí zjistit nejen délku řetězce, ale i délku seznamu – tedy
počet jeho prvků.
{% endfilter %}

Teď si zkus seznam seřadit. Na to existuje metoda `sort`:

``` pycon
>>> loterie.sort()
```

Tato funkce nic nevrátí, jen změní pořadí čísel v seznamu.
Znovu si ho vypiš, ať vidíš co se stalo:

``` pycon
>>> loterie
[3, 12, 19, 30, 42, 59]
```

Čísla v seznamu jsou nyní seřazena od nejnižší k nejvyšší hodnotě.

Podobně funguje metoda `reverse`, která obrátí pořadí prvků.
Vyzkoušej si ji!

``` pycon
>>> loterie.reverse()
>>> loterie
[59, 42, 30, 19, 12, 3]
```

Pokud chceš do svého něco přidat seznamu, můžeš to provést pomocí metody
`append`.
Ale pozor! Tahle metoda potřebuje vědět co má do seznamu přidat
Nová hodnota se zadává do závorek:

``` pycon
>>> loterie.append(199)
```

Metoda opět nic nevrací, takže je potřeba seznam pro kontrolu vypsat:

``` pycon
>>> loterie
[59, 42, 30, 19, 12, 3, 199]
```

### Vybírání prvků

Když se budeš chtít na jednu věc ze seznamu podívat podrobněji,
přijde vhod možnost vybrat si konkrétní prvek.
Na to se v Pythonu používají hranaté závorky.

{# XXX: MCQ #}

Chceš-li vybrat prvek, zadej jméno seznamu a hned za ním hranaté závorky
s pořadovým číslem prvku, který chceš:

``` pycon
>>> loterie[1]
```

Dostaneš první prvek?

{% filter solution %}
``` pycon
>>> loterie
[59, 42, 30, 19, 12, 3, 199]
>>> loterie[1]
42
```

Ne, dostaneš druhý prvek.

Programátoři počítají od nuly.
Chceš li tedy první prvek, popros Python o prvek číslo nula:

``` pycon
>>> loterie[0]
42
```

Je to zpočátku divné, ale dá se na to zvyknout.
{% endfilter %}

Číslu prvku se také říká *index* a procesu vybírání prvků *indexování*.

Zkus si indexování s dalšími indexy: 3, 100, 7, -1, -2, -6 nebo -100.
Pokus se předpovědět výsledek před zadáním příkazu.
Jak ti to půjde?

{% filter solution %}
``` pycon
>>> loterie
[59, 42, 30, 19, 12, 3, 199]

>>> loterie[3]
19
```
Index 3 označuje čtvrtý prvek.

``` pycon
>>> loterie[7]
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
IndexError: list index out of range

```
Prvek s indexem 100 v seznamu není – nastane chyba.

``` pycon
>>> loterie[1000]
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
IndexError: list index out of range
```
Prvek s indexem 7 v seznamu taky není.

``` pycon
>>> loterie[-1]
199
```
Index -1 označuje *poslední* prvek.

``` pycon
>>> loterie[-2]
3
```
Index -2 označuje předposlední prvek.

``` pycon
>>> loterie[-6]
42
```
Index -6 označuje šestý prvek od konce.

``` pycon
>>> loterie[-100]
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
IndexError: list index out of range
```
Stý prvek od konce v seznamu není. Nastane chyba.
{% endfilter %}

### Řezání

XXX Slicing

### Odstraňování

Chceš-li ze seznamu něco odstranit, můžeš opět použít indexy.
Tentokrát s příkazem `del`.
Následující kód odstraní počáteční číslo seznamu, tedy prvek číslo 0:

``` pycon
>>> del loterie[0]
```

Pak si seznam opět vypiš. Kousek chybí!

``` pycon
>>> loterie
[42, 30, 19, 12, 3, 199]
```

Zkusíš odstranit poslední prvek?

{% filter solution %}
``` pycon
>>> del loterie[-1]
>>> loterie
[42, 30, 19, 12, 3]
```
{% endfilter %}

A co prostřední tři?
Zkus si nejdřív vypsat, které to jsou, a pak teprve použít `del`.

{% filter solution %}
``` pycon
>>> loterie
[42, 30, 19, 12, 3]
>>> loterie[1:-1]
[30, 19, 12]
>>> del loterie[1:-1]
>>> loterie
[42, 3]
```
{% endfilter %}


## Slovníky

Jiný typ hodnot, které v sobě mohou obsahovat další hodnoty, je *slovník*.
Pro příklad si představ překladový slovník, třeba česko-anglický:

* **Jablko**: Apple
* **Knoflík**: Button
* **Myš**: Mouse

Slovník v Pythonu obsahuje záznamy, a každý záznam přiřazuje
nějakému *klíči* nějakou *hodnotu*.
V našem příkladu je klíči *Jablko* přiřazena hodnota *Apple*,
klíči *Knoflík* náleží hodnota *Button*
a klič *Myš* ukazuje na *Mouse*.

V Pythonu by se takový slovník napsal následovně:

``` pycon
>>> slovnik = {'Jablko': 'Apple', 'Knoflík': 'Button', 'Myš': 'Mouse'}
```

Naše klíče a hodnoty jsou slova – krátké texty, tedy řetězce,
které je potřeba dát do uvozovek.
Klíč a hodnota jsou oddělené dvojtečkou,
jednotlivé dvojice se od sebe oddělují čárkou,
a celý slovník je uzavřený ve složených závorkách.

Když budeš chtít v takovém slovníku něco najít, potřebuješ vědět, co hledat.
Konkrétně *klíč*.
Pomocí hranatých závorek můžeš zjistit hodnotu, která odpovídá danému klíči:


``` pycon
>>> slovnik['Jablko']
'Apple'
```

Je to podobné jako u seznamů, jen v hranatých závorkách není pořadí prvku,
ale klíč.
{# XXX: Slicing taky nejde #}

> [note]
> Naopak to nejde – slovník neumožňuje podle hodnoty přímo zjistit klíč.
> Na překlad z angličtiny do češtiny bys potřeboval{{a}} druhý slovník.

### Měnění slovníků

Co se stane, když klíč ve slovníku není?

``` pycon
>>> slovnik['Pes']
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
KeyError: 'Pes'
```

Python si postěžuje na `KeyError` – chybu klíče.

Podobně jako seznamy se ale slovníky dají měnit.
Nový záznam vytvoříš takhle:

``` pycon
>>> slovnik['Pes'] = 'Dog'
>>> slovnik
{'Jablko': 'Apple', 'Knoflík': 'Button', 'Myš': 'Mouse', 'Pes': 'Dog'}
```

> [note]
> Na rozdíl od překladového slovníku nemusí být Pythonní slovník seřazený
> podle abecedy.
> Není to potřeba, počítač umí rychle vyhledávat i bez seřazení.

Kdybys potřebovala{{a}} změnit už existující záznam, použij stejný příkaz.
K jednomu klíči může patřit jen jedna hodnota.

``` pycon
>>> slovnik['Pes'] = 'Extension cord'
>>> slovnik
{'Jablko': 'Apple', 'Knoflík': 'Button', 'Myš': 'Mouse', 'Pes': 'Extension cord'}
```

{# XXX: Zmínit se o nehomogenních slovnících? #}

Chceš-li ze zlovníku nějaký záznam smazat, dělá se to podobně jako
u seznamů příkazem `del`:

``` pycon
>>> del slovnik['Pes']
>>> slovnik
{'Jablko': 'Apple', 'Knoflík': 'Button', 'Myš': 'Mouse'}
```

A když budeš chtít zjistit, kolik je ve slovníku záznamů,
zeptáš se podobně jako na počet znaků řetězce nebo prvků seznamu.
Použiješ funkci `len()`.

``` pycon
>>> len(slovnik)
3
```

{# XXX

* Kontakty
* Když číslo není číslo
* Více čísel

### K zamyšlení

Ke každému klíči může patřit jen jedna hodnota.
Jak bys zařídil{{a}}, aby hodnot víc?

Zkus do Pythonní proměnné uložit tyto kontakty:

* Katka:
    * 4925219
* Jirka:
    * 7477058
    * 3251156
* Verča:
    * 1019103

{% filter solution %}
Více hodnot se dá uložit do seznamu.
Hodnoty budou seznamy čísel:

```pycon
>>> kontakty = {'Katka': ['4925219'], 'Jirka': ['7477058', '3251156'], 'Verča': ['1019103']}
```
{% endfilter %}

Verča se přestěhovala do zahraničí a má nové číslo: `+897 3788509`.

#}

### Shrnutí

Skvělé! Nyní víš o programování hodně. V této poslední části jsi poznal{{a}}:

*   **chyby** - hlášky které Python zobrazí když nerozumí příkazu který jsi zadal{{a}} nebo ho neumí splnit
*   **proměnné** - názvy pro objekty, které umožňují psát čitelnější kód
*   **seznam** - sekvence objektů uložených v určitém pořadí
*   **slovník** - sbírka záznamů klíč–hodnota

Jsi připraven{{a}} na další část?

## Porovnávání věcí

Programátoři často porovnávají různé hodnoty. Pojďme se podívat, jak na to.

``` pycon
>>> 5 > 2
True
>>> 5 > 8
False
>>> 5 < 8
True
```

Když se Pythonu zeptáš, jestli je jedno číslo větší než druhé, odpoví ti
`True` (pravda) nebo `False` (nepravda).

Funguje to i se složitějšími výrazy:

``` pycon
>>> 5 > 2 * 2
True
```

„Větší než“ a „menší než“ používají značky známé z matematiky.
Chceš-li se ale zeptat, jestli jsou dvě čísla stejná, je to trochu jiné:

``` pycon
>>> 1 == 1
True
```

Jedno rovnítko `=` používáme pro přiřazení hodnoty do proměnné.
Když chceš zkontrolovat, jestli se věci navzájem rovnají, vždy, **vždy** musíš dát dvě rovnítka `==`.

Další možnosti porovnávání jsou nerovnost (≠), větší než (≤) a meší než (≥).
Většina lidí tyhle symboly nemá na klávesnici, a tak se používá `!=`, `<=`
a `>=`.

``` pycon
>>> 5 != 2
True
>>> 3 <= 2
False
>>> 6 >= 12 / 2
True
```

### Logika

Chceš zkusit ještě něco? Zkus tohle:

``` pycon
>>> 6 > 2 and 2 < 3
True
>>> 3 > 2 and 2 < 1
False
>>> 3 > 2 or 2 < 1
True
```

V Pythonu můžeš zkombinovat několik porovnání do jednoho!

*   Pokud použiješ operátor `and`, obě strany musí být pravdivé, aby byl celý výraz pravdivý.
*   Pokud použiješ operátor `or`, stačí aby jen jedna strana z porovnání byla pravdivá.

Už jsi někdy slyšel{{a}} výraz „srovnávat jablka a hrušky“? Zkusme v Pythonu ekvivalent:

``` pycon
>>> 1 > 'krajta'
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: '>' not supported between instances of 'int' and 'str'
```

Stejně jako nelze srovnávat „jablka a hrušky“,
Python není schopen porovnávat řetězce (`str`) a čísla (`int`).
Místo toho zobrazí `TypeError` a říká nám, že tyto dva typy nelze porovnat.


### Logické hodnoty

Mimochodem právě ses dozvěděl{{a}} o novém typu objektu v Pythonu.
Říká se mu *pravdivostní hodnota*, nebo častěji anglicky *boolean*.

Může mít jednu z dvou hodnot: `True` a `False`.

Aby Python pochopil, že se jedná o tento typ,
je potřeba dávat pozor na velikost písmen.
`true`, `TRUE`, `tRUE` nebude fungovat – jedině `True` je správně.

Jako kažtou hodnotu, i pravdivostní hodnotu můžeš uložit do proměnné:

``` pycon
>>> a = True
>>> a
True
```

Stejně tak můžeš uložit i výsledek porovnání:

```
>>> a = 2 > 5
>>> a
False
```

# Ulož to!

Zatím jsi psal{{a}} všechny programy v konzoli v interaktivním režimu Pythonu,
který nás omezuje na jeden řádek kódu.
Když Python opustíš (nebo vypneš počítač),
všechno co jsi zatím naprogramoval{{a}}, se ztratí.

Větší programy jsou trvanlivější: ukládají se do souborů a dají se kdykoli
spustit znovu.

Vyzkoušejme si to. Budeme potřebovat:

*   Ukončit interaktivní režim Pythonu
*   Otevřít editor kódu
*   Uložit kód do nového souboru
*   Spustit ho!

Zkus vypnout Python. Existuje na to funkce `exit()`:

``` pycon
>>> exit()
```

Tak se dostaneš zpět do příkazové řádky.
Budou tu fungovat příkazy jako `cd` a `mkdir`,
ale ne příkazy Pythonu, jako `1 + 1`.

Chceš-li opustit interaktivní režim Pythonu, který jsme dosud používaly, jednoduše zadejte ~ ~ ~ exit() ~ ~ ~ funkci:


{# (((((((( XXX )))))))) #}
> [Note]
> Pokud budeš chtít Python konzoli ukončit, zadej `exit()` nebo použíj
> zkratku `Ctrl + D` (pro Mac/Linux) nebo `Ctrl + Z` (na Windows).
> Pak již neuvidíš `>>>`.


Tak se dostaneš zpět do příkazové řádky.

Doufám, že máš nainstalovaný textový editor.
Ten teď otevři a napiš do nového souboru tento příkaz:

```python
print('Hello, PyLadies!')
```

Teď vytvořený soubor ulož pod nějakým popisným názvem.
Pojďme ho nazvat `python_intro.py` a ulož si jej na plochu.
Soubor můžeš pojmenovat jakkoliv chceš, ale jméno musí končit na `.py`
Tahle přípona říká editoru nebo i operačnímu systému,
že jde o program v Pythonu a Python ho může spustit.

> [note] Obarvování
> Po uložení by se text měl obarvit.
> V interaktivním režimu Pythonu mělo vše stejnou barvu,
> ale nyní bys měla vidět, že jméno funkce `print` je jinou barvou než
> řetězec v závorkách.
> Barvy nevolíš {{gnd('sám', 'sama')}}, vybírá je editor na základě toho,
> jak potom Python kódu porozumí.
>
> Nazývá se to "zvýrazňování syntaxe" a je to užitečná funkce.
> Chce to trochu praxe, ale barvy můžou napovědět
> že ti chybí uvozovka za řetězcem
> nebo máš překlep v klíčovém slovu jako `del`.
> To je jeden z důvodů, proč používáme editory kódu :)

Pokud máš soubor uložen, je čas jej spustit!
Pomocí dovedností, které jsi se naučil{{a}} v sekci příkazová řádka,
*změň adresář* terminálu na plochu.

Na Macu bude příkaz vypadat přibližně takto:

``` console
(venv) $ cd ~/Desktop
```

Na Linuxu to bude vypadat takto (slovo "Desktop" (Plocha) může být
přeloženo třeba do češtiny):

``` console
(venv) $ cd ~/Desktop
```

A na Windows to bude vypadat takto:

``` doscon
(venv) > cd Desktop
```

Pokud nevíš jak dál, požádej o pomoc kouče.

Nyní pomocí Pythonu spusť kód v souboru:

``` console
(venv) $ python python_intro.py
Hello, PyLadies!
```

Funguje? Vidíš text?
Jesli ano, právě jsi spustil{{a}} svůj první opravdový program v Pythonu!
Cítíš se úžasně?

### Vstup a výstup

Funkce `print()`, kterou jsi použila, umí něco *vypsat* na obrazovku.
V konzoli se hodnoty výrazů vypisovaly automaticky, abys je mohl{{a}}
průběžně kontrolovat, ale programy v souborech bývají složitější a výpis
každého kroku by byl nepřehledný.
Proto na vypsání potřebuješ `print()`.
Zkus si to:

``` python
jmeno = 'Ola'

'Já jsem ' + jmeno  # Tohle Python nevypíše

print(jmeno * 8)    # Tohle jo!
```

Do závorek funkce `print()` můěš dát i víc hodnot oddělených čárkami.

``` python
jmeno = 'Amálka'
vek = 5
print('Já jsem', jmeno, 'a je mi', vek)

print('Za rok mi bude', vek + 1)
```

Další užitečná funkce je `input()`, která se umí zeptat na otázku.
Odpověď pak vrátí jako řetězec, který si můžeš uložit do proměnné:

``` python
jmeno = input('Jak se jmenuješ? ')
print(jmeno, 'umí programovat!')
```

A co když budeš chtít spíš číslo než text?
Pamatuješ si na funkci, která umí převést řetězec na číslo?

``` python
letopocet = int(input('Jaký je letos rok? '))
print('Loni byl rok', letopocet - 1)
```


## Když – tak

Spoustu věcí v kódu chceme provádět, jen pokud jsou splněny určité podmínky.
Proto má Python *podmíněné příkazy*.

Zkusíme napsat program, který ověřuje tajné heslo.
Tenhle program napíše `True`, když zadáš slovo `čokoláda`:

```python
heslo = input('Zadej heslo: ')
print(heslo == 'čokoláda')
```

Vypsání `True` ale není moc zajímavé.
Lepší program by dělal tohle:

* Zeptá se na tajné heslo
* Když je heslo správné:
    * Pustí uživatele dovnitř

Anglicky se „když“ řekne *if*. A to je i jméno Pythoního příkazu.
Používá se takhle:

```python
heslo = input('Zadej heslo: ')
if heslo == 'čokoláda':
    print('Správně! Račte vstoupit.')
```

Podmíněný příkaz začíná `if`, pokračuje podmínkou (třeba porovnáním)
a končí dvojtečkou.

Po řádkem s `if` je příkaz *odsazený* – na začátku řádku jsou 4 mezery.

Podle toho Python pozná, že tuhle část programu má provést,
jen když je podmínka pravdivá.

Ulož a spusť:

``` console
(venv) $ python python_intro.py
Zadej heslo: čokoláda
Správně! Můžeš vstoupit.
```

``` console
(venv) $ python python_intro.py
Zadej heslo: sezam
```

### Jinak

V předchozím příkladu byl kód proveden pouze v případě, že podmínka byla splněna.
Ještě lepší program by ale:

* Zeptá se na tajné heslo
* Když je heslo správné:
    * Pustí uživatele dovnitř
* Jinak:
    * Spustí alarm

K tomu má Python příkaz `else` – „jinak“:

```python
heslo = input('Zadej heslo: ')
if heslo == 'čokoláda':
    print('Správně! Račte vstoupit.')
else:
    print('POZOR! POZOR!')
    print('NEOPRÁVNĚNÝ VSTUP!')
```

Funuje to?

### Více možností

Občas se stane, že se program musí rozhodnout mezi více možnostmi.
K tomu slouží příkaz `elif`, zkratka znglického *else if* – „jinak, pokud“.

Napišme program, který okomentuje hlasitost hudby:

* Zeptá se na hlasitost, a odpověď uloží jako číslo.
* Když je hlasitost do 20:
    * vypíše „Je to dost potichu.“
* Jinak, když je hlasitost do 40:
    * vypíše „Jako hudba v pozadí dobré.“
* Jinak, když je hlasitost do 60:
    * vypíše „Skvělé, slyším všechny detaily.“
* Jinak, když je hlasitost do 80:
    * vypíše „Dobré na párty.“
* Jinak, když je hlasitost do 100:
    * vypíše „Trochu moc nahlas!“
* Jinak:
    * vypíše „Krvácí mi uši!“

V Pythonu:

```python
hlasitost = int(input('Jaká je nastavená hlasitost rádia? '))
if hlasitost < 20:
     print("Je to dost potichu.")
elif hlasitost < 40:
     print("Jako hudba v pozadí dobré.")
elif hlasitost < 60:
     print("Skvělé, slyším všechny detaily.")
elif hlasitost < 80:
     print("Dobré na party.")
elif hlasitost < 100:
     print("Trochu moc nahlas!")
else:
    print("Krvácí mi uši!")
```

``` console
(venv) $ python python_intro.py
Jaká je nastavená hlasitost rádia? 28
Jako hudba v pozadí dobré.
```

Všimni si, že se vybere vždycky jedna alternativa.
Když zadáš `28`, Python se dostane k `hlasitost < 40`, vypíše
příslušnou hlášku a další možnosti přeskočí.


### Shrnutí

V posledních třech cvičeních ses dozvěděla o:

*   **Porovnání věcí** - v Pythonu můžeš porovnávat věci pomocí operátorů `>`, `>=`, `==` `<=`, `<`, `!=` a `and`, `or`
*   **Pravdivostní hodnoty / Boolean** - typ, který může mít pouze jednu ze dvou hodnot: `True` nebo `False`
*   **Ukládání do souborů** - pokud uložíš kód do souboru, můžeš spouštět větší programy
*   **if – elif – else** - příkazy, které umožňují spouštět kód pouze v případě, kdy jsou splněny určité podmínky.

Čas na předposlední část této kapitoly!


## Vlastní funkce

Pamatuješ na funkce `len()` a `print()`?
Jsou jako kouzelná zaříkadla z knihy vázané v kůži: když víš jak se jmenují
a umíš je správně {# XXX: <s>vyslovit</s> #}napsat, něco pro tebe udělají.

Teď postoupíme na další úroveň: vymyslíme si vlastní zaříkadla!
Jak? Budeme kombinovat příkazy, které už známe.

Třeba funkce, která tě pozdraví, by měla:

* Vypsat „ahoj!“
* Vypsat „jak se máš?“

Definice funkce v Pythonu začíná klíčovým slovem `def`,
dále je uveden název a závorky (zatím prázdné).
Pak jako po `if` dvojtečka, a odsazené příkazy,
které má funkce provést.

```python
def pozdrav():
    print('Ahoj!')
    print('Jak se máš?')
```

Naše první funkce je připravena!

Když ale tenhle program spustíš, nic neudělá.
To proto, že tohle je jen *definice* funkce.
Python teď ví jak pozdravit – ale neřeklo se, že to má udělat!

Na konec programu přidej volání.
To už není součást funkce, ale pokračování samotného programu.
Proto nesmí být odsazené:

```python
def pozdrav():
    print('Ahoj!')
    print('Jak se máš?')

pozdrav()
```

Co se stane, když funkci zavoláš několikrát po sobě?

```python
def pozdrav():
    print('Ahoj!')
    print('Jak se máš?')

pozdrav()
pozdrav()
pozdrav()
```

Co se stane, když volání dáš *nad* definici funkce, místo na konec programu?

```python
pozdrav()

def pozdrav():
    print('Ahoj!')
    print('Jak se máš?')
```

{% filter solution %}
``` pycon
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
NameError: name 'pozdrav' is not defined
```

Python si stěžuje na `NameError` – nezná nic jménem `pozdrav`.

Python totiž program čte odzhora dolů.
Až příkazem `def` se „naučí" jak zdravit –
Předtím, než se k příkazu `def` dostane, funkce neexistuje.
{% endfilter %}

# Parametry

Funkce jako `len('slovo')` a `print(1 + 2)` umí navíc pracovat s hodnotou.

Pojďme napisať funkciu, ktorá ťa pozdraví menom.
(Uľahčíme si to použitím jazyka, ktorý nepoužíva piaty pád.)

```python
def pozdrav(meno):
    print('Vitam ťa,', meno)

pozdrav('Ola')
pozdrav('Soňa')
pozdrav('Hubert')
pozdrav('Anička')
```

Jak to funguje?
V definici funkce uvedeš závorkách *parametr* – jméno proměnné se kterou bude
funkce pracovat.
Hodnotu pro tenhle parametr pak zadáš při volání funkce.

Zvládneš napsat program, který se zeptá na jméno a pak tě pozdraví?

{% filter solution %}
```python
def pozdrav(meno):
    print('Vitam ťa,', meno)

pozdrav(input('Jak se jmenuješ? '))
```
{% endfilter %}

Co se stane, když funkci zavoláš bez hodnoty pro parametr?

{% filter solution %}
``` pycon
Traceback (most recent call last):
  File "<stdin>", line 9, in <module>
TypeError: pozdrav() missing 1 required positional argument: 'meno'
```

Python si stěžuje na `TypeError` – funkce `pozdrav` nedostala povinný
argument `meno`.
{% endfilter %}

Funkce může obsahovat jakýkoli kód.
Třeba podmíněný příkaz, `if`.
Příkazy po `if` je pak potřeba odsatit o *další* čtyři mezery:

```python
def pozdrav(meno):
    print('Vitam ťa,', meno)
    if meno == 'Ola':
        print('Ty umíš programovať!')

pozdrav('Hubert')
pozdrav('Ola')
pozdrav('Soňa')
```

## Smyčky/Loops

Nyní pojďme na poslední část. To bylo rychlé, co? :)

Programátoři se neradi opakují. Programování je o automatizaci věci, takže nechceme zdravit každého člověka podle jeho jména manuálně, že? Zde se budou smyčky hodit.

Ještě si vzpomínáš na seznamy? Udělejme seznam dívek:

```python
girls = ['Rachel', 'Monica', 'Phoebe', 'Ola', 'You']
```

Chceme pozdravit všechny s použitím jejich jména. Máme funkci `hi`, která to umí udělat. Tak ji použijeme ve smyčce:

```python
for name in girls:
```

Příkaz ~ ~ ~ for ~ ~ ~ se chová podobně jako příkaz ~ ~ ~ if ~ ~ ~, v následujícím kódu musíme oba řádky odsadit o čtyři mezery.

Zde je celý kód, který umístíme do souboru:

```python
def hi(name):
     print('Hi ' + name + '!')

girls = ['Rachel', 'Monica', 'Phoebe', 'Ola', 'You']
for name in girls:
     hi(name)
     print('Next girl')
```

A když ho spustíme:

```
$ python3 python_intro.py
Hi Rachel!
Next girl
Hi Monica!
Next girl
Hi Phoebe!
Next girl
Hi Ola!
Next girl
Hi You!
Next girl
```

Jak vidíš, vše, co jsi vložila dovnitř příkazu `for` s odsazením, se zopakuje pro každý prvek seznamu `girls`.

Ve funkci `for` můžeš také použít čísla pomocí funkce `range`:

```python
for i in range(1, 6):
     print(i)
```

Což ti vypíše:

```
1
2
3
4
5
```

`range` je funkce, která vytvoří seznam s posloupností čísel (tato čísla zadáváš jako parametry funkce).

Všimni si, že druhé z těchto dvou čísel není zahrnuto v seznamu, který je výstupem Pythonu (`range (1, 6)` počítá od 1 do 5, ale nezahrnuje číslo 6). To je proto, že "range" je z poloviny otevřený, čímž myslíme, že obsahuje první hodnotu, ale ne poslední.

## Shrnutí

A je to. **Jsi naprosto skvělá!** To byla složitá kapitola, takže bys na sebe měla být hrdá. My jsme na tebe velmi hrdí za to, že ses dostala tak daleko!

Můžeš si jít krátce odpočinout - protáhnout se, projít se, zavřít oči - než se pustíme do další kapitoly. :)

![Hrnek][3]

 [3]: images/cupcake.png
