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


## Funkce print

Zkus toto:

``` pycon
>>> jmeno = 'Marie'
>>> jmeno
'Marie'
>>> print(jmeno)
Marie
```

Zadáš-li jen `name`, Python vypíše řetězec obklopený jednoduchými uvozovkami.
To je *reprezentace* řetězce `'Marie'` – způsob, jak tuhle hodnotu
zadat v Pythonu.

Funkce `print`, místo toho vypíše hodnotu bez uvozovek, což vypadá lépe
(i když pro progrmátora to může být méně užitečné).

Jak uvidíme později, vypisování pomocí funkce `print()` je také užitečná,
když chceme vypsat věci uvnitř funkce nebo na více řádcích.

{# XXX: why is print here??? #}

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
>>> print(loterie)
[3, 12, 19, 30, 42, 59]
```

Čísla v seznamu jsou nyní seřazena od nejnižší k nejvyšší hodnotě.

Podobně funguje metoda `reverse`, která obrátí pořadí prvků.
Vyzkoušej si ji!

``` pycon
>>> loterie.reverse()
>>> print(loterie)
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
>>> print(loterie)
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

Slovník je podobný seznamu, ale pro přístup k hodnotám se používá klíč místo indexu. Klíč může být jakýkoli řetězec nebo číslo. Syntaxe pro definování prázdného slovníku je:

```
>>> {}
{}
```

Vidíš, že jsi právě vytvořila prázdný slovník. Hurá!

A teď zkus napsat následující příkaz (zkus nahradit vlastními informacemi):

```
>>> participant = {'name': 'Ola', 'country': 'Poland', 'favorite_numbers': [7, 42, 92]}
```

Tímto příkazem jsi právě vytvořila proměnnou s názvem `participant` s třemi dvojicemi klíčů hodnot:

*   Klíč `name` odkazuje na hodnotu `"Ola"` (`string/řetězcový` objekt),
*   klíč`country`, ukazuje na `"Polsko"` (další `řetězec`)),
*   a `favorite_numbers` ukazuje `[7, 42, 92]` (`list/seznam` obsahující 3 čísla).

Můžeš zkontrolovat obsah jednotlivých klíčů následující syntaxí:

```
>>> print(participant['name'])
Ola
```

Je to podobné seznamu. Ale není nutné si pamatovat index - jen jméno.

Co se stane, když se zeptáme Pythonu na hodnotu klíče, který neexistuje? Zkus hádat! Pojďme to vyzkoušet a uvidíš!

```
>>> participant['age']
Traceback (most recent call last):
File "<stdin>", line 1, in <module>
KeyError: 'age'
```

Podívej, další chyba! Toto je **KeyError**. Python ti napomáhá a řekne ti, že klíč `"věk"` v tomto slovníku neexistuje.

Kdy použít slovník a kdy seznam? To je dobrý postřeh k zamyšlení. Kdy použít jakou variantu pochopíš, až si přečteš následující řádky.

*   Potřebuješ jen seřazenou sekvenci položek? Použij seznam.
*   Pokud potřebuješ přiřadit hodnotám klíče, abys je mohla později efektivně vyhledávat (klíčem)? Používej slovník.

Slovníky stejně jako seznamy jsou *mutable/proměnlivé*, což znamená, že je lze změnit po jejich vytvoření. Do slovníku můžeš přidat nové páry klíč/hodnota po jeho vytvoření:

```
>>> participant['favorite_language'] = 'Python'
```

Stejně jako u seznamů můžeš použít metodu `len()` na slovníky, vrací počet párů klíč/hodnota ve slovníku. Nestyď se a zadej příkaz:

```
>>> len(participant)
4
```

Doufám, že ti to nyní dává větší smysl. :) Připravena na více zábavy se slovníky? Pojďme na další řádek a další úžasné věci.

Příkazem `pop()` odstraníš položky ve slovníku. Například pokud chceš odstranit záznam, kterému odpovídá klíč `"favorite_numbers"`, zadej následující příkaz:

```
>>> participant.pop('favorite_numbers')
>>> participant
{'country': 'Poland', 'favorite_language': 'Python', 'name': 'Ola'}
```

Jak vidíš, z výstupu byla odstraněna odpovídající dvojice klíč hodnota 'favorite_numbers'.

Kromě toho můžeš také změnit hodnotu přidruženou k již vytvořenému klíči ve slovníku. Napiš:

```
>>> participant['country'] = 'Germany'
>>> participant
{'country': 'Germany', 'favorite_language': 'Python', 'name': 'Ola'}
```

Jak můžeš vidět, hodnota klíče `'country'` se změnila z `"Poland"` na `"Germany"`. :) Úžasné? Hurá! Právě jsi se naučila další úžasnou věc.

### Shrnutí

Skvělé! Nyní víš o programování hodně. V této poslední části jsi se naučila o:

*   **errors/chyby** - nyní víš jak číst a pochopit chyby, které ti Python zobrazí, pokud nerozumí příkazu, který jsi zadala
*   **proměnné/variables** - názvy pro objekty, které umožňují psát kód snadněji tak, aby byl čitelnější
*   **seznamy/lists** - seznamy objektů uložených v určitém pořadí
*   **slovníky/dictionaries** - objekty, které jsou uloženy jako dvojice klíč–hodnota

Jsi připravena na další část?

## Porovnávání věcí

Velká část programování zahrnuje porovnání věci. Co je nejjednodušší věc k porovnání? Čísla, samozřejmě. Podívejme se, jak to funguje:

```
>>> 5 > 2
True
>>> 3 < 1
False >>> 5 > 2 * 2
True
>>> 1 == 1
True
>>> 5 != 2
True
```

Dali jsme Pythonu nějaká čísla na porovnání. Jak vidíš, Python může porovnávat nejen čísla, ale může také porovnat výsledky metod. Pěkný, co?

Zajímá tě, proč jsme daly dva symboly rovná se `==` vedle sebe pro porovnání, zda jsou čísla stejná? Jedno rovnítko `=` používáme pro přiřazení hodnoty do proměnné. Vždy, **vždy** musíte dát dvě rovnítka `==`, pokud chcete zkontrolovat, jestli se věci navzájem rovnají. Můžeme také zjišťovat, že se věci navzájem nerovnají. Pro takové porovnání můžeme použít symbol `!=`, jak je uvedeno v příkladu výše.

Dejme Pythonu dva další úkoly:

```
>>> 6 >= 12 / 2
True
>>> 3 <= 2
False
```

`>` a `<` jsou pro použití snadné, ale co `> =` a `< =` - víš, co se tím myslí? Podívejme se na to:

*   x `>` y znamená: x je větší než y
*   x `<` y znamená: x je menší než y
*   x `<=` y znamená: x je menší nebo rovno y
*   x `>=` y znamená: x je větší nebo rovno y

Úžasné! Chceš zkusit ještě něco? Zkuste tohle:

```
>>> 6 > 2 and 2 < 3
True
>>> 3 > 2 and 2 < 1
False
>>> 3 > 2 or 2 < 1
True
```

Pythonu můžeš dát porovnat tolik čísel kolik chceš a na vše ti dá odpověď! Je docela chytrý, že?

*   **and** - Pokud použiješ operátor `and`, obě strany musí být pravdivé, aby celý příkaz byl pravdivý
*   **or** - Pokud použiješ operátor `or`, stačí, aby jen jedna strana z porovnání byla pravdivá, aby celý příkaz byl pravdivý

Už jsi někdy slyšela výraz "srovnávat jablka a hrušky"? Zkusme v Pythonu ekvivalent:

```
>>> 1 > 'django'
Traceback (most recent call last):
File "<stdin>", line 1, in <module>
TypeError: '>' not supported between instances of 'int' and 'str'
```

Zde vidíš, že stejně jako nelze srovnávat "jablka a hrušky", Python není schopen porovnávat řetězce (`str`) a čísla (`int`). Místo toho zobrazí **TypeError** a říká nám, že tyto dva typy nelze srovnávat společně.

## Logic hodnoty/Booleany

Mimochodem právě jste se dozvěděly o novém typu objektu v Pythonu. Říká se mu **boolean** a je to asi nejjednodušší typ.

Existují pouze dva logické objekty: - True - False

Aby Python pochopil, že se jedná o tento typ, je potřeba vždy psát jako True (první písmeno velké, zbytek malý). **true, TRUE, tRUE nebude fungovat – jedině True je správně.** (Totéž samozřejmě platí pro False.)

Pravdivostní hodnoty mohou být také v proměnné! Viz zde:

```
>>> a = True
>>> a
True
```

Rovněž to můžete provést takto:

```
>>> a = 2 > 5
>>> a
False
```

Zkoušej a bav se s logickými hodnotami. Zkus spustit následující příkazy:

*   `True and True`
*   `False and True`
*   `True or 1 == 1`
*   `1 != 2`

Gratulujeme! Logické hodnoty jsou jedny z nejbezvadnějších vlastností v programování a vy jste se je právě naučily používat!

# Ulož to!

Zatím jsme psaly všechny naše programy v konzoli v interaktivním režimu Pythonu, který nás omezuje na jeden řádek kódu v jednu chvíli. Normální programy jsou uloženy v souborech a spouští je **konzole** nebo **překladač** programovacího jazyku. Zatím jsme spouštěly naše programy po jednom řádku v **konzoli, v interaktivním režimu** Python. Pro příštích několik úkolů budeme potřebovat více než jeden řádek kódu, takže rychle musíme:

*   Ukončit interaktivní režim Pythonu
*   Otevřít náš zvolený editor kódu
*   Uložit nějaký kód do nového pythonovského souboru
*   Spustit ho!

Chceš-li opustit interaktivní režim Pythonu, který jsme dosud používaly, jednoduše zadejte ~ ~ ~ exit() ~ ~ ~ funkci:

```
>>> exit()
$
```

{# (((((((( XXX )))))))) #}
> [Note]
> Pokud budeš chtít Python konzoli ukončit, zadej `exit()` nebo použíj
> zkratku `Ctrl + D` (pro Mac/Linux) nebo `Ctrl + Z` (na Windows).
> Pak již neuvidíš `>>>`.


Tak se dostaneš zpět do příkazové řádky.

Dříve sis vybrala editor kódu v části [editor kódu][2]. Nyní potřebujeme editor otevřít a napsat vlastní kód do nového souboru:

 [2]: ../code_editor/README.md

```python
print('Hello, Django girls!')
```

> **Poznámka:** Měla bys objevit jednu z nejúžasnější věcí na editorech kódu: barvy! V interaktivním režimu Pythonu mělo vše stejnou barvu, ale nyní bys měla vidět, že funkce `print` je jinou barvou než řetězec uvnitř. To se nazývá "zvýrazňování syntaxe" a je to opravdu užitečná funkce při kódování. Barvy ti napoví, že máš neuzavřený řetězce nebo překlep v názvu slova (jako `def` ve funkci, kterou uvidíš níže). To je jeden z důvodů, proč používáme editory kódu :)

Samozřejmě teď jsi již pěkně ostřílená python programátorka, tak neváhej napsat nějaký kód, který ses dnes naučila.

Teď potřebujeme uložit vytvořený soubor a dát mu popisný název. Pojďme ho nazvat **python_intro.py** a uložit jej na plochu. Soubor můžeš pojmenovat jakkoliv chceš, ale důležitá věc je, aby ses ujistila, že soubor končí na **.py**. Přípona **.py** říká našemu operačnímu systému, že jde o **spustitelný soubor Pythonu** a Python ho může spustit.

Pokud máš soubor uložen, je čas jej spustit! Pomocí dovedností, které jsi se naučila v sekci příkazová řádka, **změň adresář**  pomocí terminálu na plochu.

Na Macu bude příkaz vypadat přibližně takto:

```
$ cd ~/Desktop
```

Na Linuxu to bude vypadat takto (slovo "Desktop" (Plocha) může být přeloženo do tvého jazyka):

```
$ cd ~/Desktop
```

A na Windows to bude vypadat takto:

```
> cd %HomePath%\Desktop
```

Pokud nevíš jak dál, stačí požádat o pomoc kouče.

Nyní pomocí Pythonu spustíš kód v souboru takto:

```
$ python3 python_intro.py
Hello, Django girls!
```

V pořádku! Právě jsi spustila svůj první program v Pythonu, který byl uložen do souboru. Cítíš se úžasně?

Nyní můžeme přejít k základním nástrojům pro programování:

## If...elif...else

Spousty věcí v kódu chceme provádět, jen pokud jsou splněny určité podmínky. To je důvod, proč Python má něco, čemu se říká **if statements**.

Nahraďte kód v souboru **python_intro.py** tímto:

```python
if 3 > 2:
```

Pokud jsi soubor uložila a spustila, pravděpodobně uvidíš následující chybu:

```
$ python3 python_intro.py
File "python_intro.py", line 2
          ^
SyntaxError: unexpected EOF while parsing
```

Python očekává, že mu dáš další pokyny, které mají být provedeny, pokud bude podmínka `3 > 2` splněna (`True`). Řekněme tedy Pythonu, ať vypíše "Funguje to!". Změň svůj kód v souboru **python_intro.py** na tento:

```python
if 3 > 2:
     print('It works!')
```

Všimla sis, jak jsme odsadily poslední řádek kódu o 4 mezery? Musíme to udělat, podle toho Python pozná, jakou část kódu má spustit, pokud vyhodnotí předchozí výraz jako pravdivý. Můžete udělat jen jednu mezeru, ale téměř všichni programátoři v Pythonu dělají 4, aby kód vypadal upraveně a čitelně. Jeden `Tab` bude také počítán jako 4 mezery.

Ulož a spusť:

```
$ python3 python_intro.py
It works!
```

### Co když podmínka není pravdivá?

V předchozích příkladech byl kód proveden pouze v případě, že podmínky byly splněny. Python má také příkazy `elif` a `else`:

```python
if 5 > 2:
     print('5 is indeed greater than 2')
else:
     print('5 is not greater than 2')
```

Pokud je výraz pravdivý, po spuštění se vytiskne:

```
$ python3 python_intro.py
5 is not greater than 2
```

Kdyby 2 bylo větší než 5, spustil by se první příkaz. Jak snadné! Podívejme se, jak funguje `elif`:

```python
name = 'Sonja'
if name == 'Ola':
     print('Hey Ola!')
elif name == 'Sonja':
     print('Hey Sonja!')
else:
     print('Hey anonymous!')
```

a spusť:

```
$ python3 python_intro.py
Hey Sonja!
```

Viděla jsi co se tam stalo? `elif` umožňuje přidat další podmínky, které se spustí, pokud se předchozí podmínky nezdaří.

Můžeš po počátečním `if` přidat tolik `elif` příkazů, kolik se ti zlíbí. Například:

```python
volume = 57
if volume < 20:
     print("Je to dost potichu.")
elif 20 <= volume < 40:
     print("Jako hudba v pozadí dobré.")
elif 40 <= volume < 60:
     print("Skvělé, slyším všechny detaily.")
elif 60 <= volume < 80:
     print("Dobré na party.")
elif 80 <= volume < 100:
     print("Trochu moc nahlas!")
else:
    print("Krvácí mi uši!")
```

Python prochází a testuje každou položku v posloupnosti a vypíše:

```
$ python3 python_intro.py
  Skvělé, slyším všechny detaily.
```

### Shrnutí

V posledních třech cvičeních ses dozvěděla o:

*   **Porovnání věcí** - v Pythonu můžeš porovnat věci pomocí operátorů `>`, `> =`, `==` `< =`, `<` a `and`, `or`
*   **Logické hodnoty / Booleany** - typy, které mohou mít pouze jednu ze dvou hodnot: `True` nebo `False`
*   **Ukládání do souborů** - pokud uložíme kód do souboru, můžeme spouštět velké programy
*   **if...elif...else** - příkazy, které umožňují spouštět kód pouze v případě, kdy jsou splněny určité podmínky.

Čas na poslední část této kapitoly!

## Vlastní funkce!

Pamatuješ na funkci `len()`, kterou jsi spouštěla v Pythonu? Máme pro tebe dobrou zprávu. Nyní se dozvíš, jak napsat své vlastní funkce!

Funkce je sled instrukcí, které by měl Python provést. Každá funkce v Pythonu začíná klíčovým slovem `def`, dále je uveden název a funkce může mít také nějaké parametry. Začněme u té nejlehčí. Nahraď kód v **python_intro.py** následujícím:

```python
def hi():
     print('Hi there!')
     print('How are you?')

hi()
```

Naše první funkce je připravena!

Asi se divíš, proč jsme napsaly název funkce v dolní části souboru. To je proto, že Python přečte soubor a spustí ho od shora dolů. Pokud chceš využívat svou funkci, musíš její název znovu napsat dole (tím ji zavoláš/spustíš).

Tak to teď zkus a uvidíš, co se stane:

```
$ python3 python_intro.py
Hi there!
How are you?
```

To bylo snadné! Napišme naši první funkci s parametry. Použijeme předchozí příklad - napíšeme funkci, která nás pozdraví podle toho, jaké zadáme jméno při jejím spuštění:

```python
def hi(name):
```

Jak vidíš, nyní jsme přidaly naší funkci parametr, `name`:

```python
def hi(name):
     if name == 'Ola':
         print('Hi Ola!')
     elif name == 'Sonja':
         print('Hi Sonja!')
     else:
         print('Hi anonymous!')

hi()
```

Pamatuj si: Funkce `print` je odsazená čtyři mezery v příkazu `if`. To je proto, aby se funkce spustila, pokud je splněna podmínka. Podívej se, jak to funguje nyní:

```
$ python3 python_intro.py
Traceback (most recent call last):
File "python_intro.py", line 10, in <module>
   hi()
TypeError: hi() missing 1 required positional argument: 'name'
```

Jejda, chyba. Naštěstí nám Python vypsal docela užitečnou chybovou zprávu. Jak vidíš, funkce `hi()` (kterou jsme definovaly) má jeden povinný parametr `(s názvem name)`, který jsme zapomněly při volání funkce předat. Pojďme to opravit v následující části:

```python
hi("Ola")
```

A znovu jej spusť:

```
$ python3 python_intro.py
Hi Ola!
```

A co když změníme jméno?

```python
hi("Sonja")
```

Spustíme:

```
$ python3 python_intro.py
Hi Sonja!
```

C myslíš, že se stane, když tam napíšeš jiné jméno než Ola nebo Sonja? Zkus to a uvidíme, jestli máš pravdu. Mělo by to vypsat toto:

```
Hi anonymous!
```

To je paráda, co? Nemusíš se opakovat a měnit takto jméno pokaždé, když chceš, aby funkce pozdravila jinou osobu. To je přesně důvod, proč potřebujeme funkce: abychom nikdy neopakovaly náš kód!

Udělejme to ještě chytřeji – existuje více jmen než dvě a psaní podmínky pro každé jméno by bylo těžké, že?

```python
def hi(name):
     print('Hi ' + name + '!')

hi("Rachel")
```

Pojďme zavolat náš nový kód:

```
$ python3 python_intro.py
Hi Rachel!
```

Blahopřejeme! Právě ses naučila, jak psát funkce :)

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
