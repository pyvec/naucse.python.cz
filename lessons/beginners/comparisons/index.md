# Porovnávání

Pamatuješ si ještě, co je to <em>operátor</em>?

V domácím projektu jsme si ukázal{{ gnd('i', 'y', both='i') }} základní aritmetické operátory.
Přidáme-li jeden další (`//`), jsou to tyhle:

<table class="table">
    <tr>
        <th>Symbol</th>
        <th>Příklad</th>
        <th>Popis</th>
    </tr>
    <tr>
        <td><code>+</code>, <code>-</code>, <code>*</code>, <code>/</code></td>
        <td><code>1 + 1</code></td>
        <td>Základní aritmetika</td>
    </tr>
    <tr>
        <td><code>-</code></td>
        <td><code>-5</code></td>
        <td>Negace</td>
    </tr>
    <tr>
        <td><code>//</code>; <code>%</code></td>
        <td><code>7 // 2</code>; <code>7 % 2</code></td>
        <td>Dělení se zbytkem (<em>celočíselné dělení</em>); zbytek</td>
    </tr>
    <tr>
        <td><code>**</code></td>
        <td><code>3 ** 2</code></td>
        <td>Umocnění (3 na druhou)</td>
    </tr>
</table>

Python ale zná i další druhy operátorů.
Důležité jsou operátory *porovnávací*.
Zkus si co dělají!
(Buď z programu pomocí `print`,
nebo pusť `python` z příkazové řádky.)

<table class="table">
    <tr>
        <th>Symbol</th>
        <th>Příklad</th>
        <th>Popis</th>
    </tr>
    <tr>
        <td><code>==</code>, <code>!=</code></td>
        <td><code>1 == 1</code>, <code>1 != 1</code></td>
        <td>Je rovno, není rovno</td>
    </tr>
    <tr>
        <td><code>&lt;</code>, <code>&gt;</code></td>
        <td><code>3 &lt; 5</code>, <code>3 &gt; 5</code></td>
        <td>Větší než, menší než</td>
    </tr>
    <tr>
        <td><code>&lt;=</code>, <code>&gt;=</code></td>
        <td><code>3 &lt;= 5</code>, <code>3 &gt;= 5</code></td>
        <td>Větší nebo rovno, menší nebo rovno</td>
    </tr>
</table>

Hodnoty provnání jsou takzvané *booleovské* hodnoty
(angl. *boolean*, podle [G. Boolea](http://en.wikipedia.org/wiki/George_Boole)).
V Pythonu se používají vždycky, když potřebujeme vědět, jestli něco platí
nebo neplatí.
Jsou jenom dvě – buď `True` (pravda), nebo `False` (nepravda).

Jako všechny hodnoty, `True` a `False` se dají přiřazovat do proměnných:

```python
pravda = 1 < 3
print(pravda)

nepravda = 1 == 3
print(nepravda)
```

> [note]
> Všimni si, že rovnost se zjišťuje pomocí dvou rovnítek: `3 == 3`.
> Jedno rovnítko přiřazuje do proměnné; dvě rovnítka porovnávají.

Slova <code>True</code> a <code>False</code> jdou
v programu použít i přímo,
jen je potřeba dávat pozor na velikost písmen:

```python
print(True)
print(False)
```

## Podmínky

Teď oprášíme program na výpočet obvodu a obsahu.

Otevři si v editoru nový soubor.
Jestli ještě v adresáři, kde máš soubory ke kurzům Pythonu,
nemáš adresář pro tuto lekci (třeba `02`), vytvoř si ho.
Nový soubor ulož do něj pod jménem `if.py`.

Do souboru pak napiš následující program:

```python
strana = float(input('Zadej stranu čtverce v centimetrech: '))
print('Obvod čtverce se stranou', strana, 'je', 4 * strana, 'cm')
print('Obsah čtverce se stranou', strana, 'je', strana * strana, 'cm2')
```

Program spusť. Funguje?

Co se stane, když jako stranu zadáš záporné číslo?
Dává výstup smysl?

Tady je vidět, jak počítač dělá přesně, co se mu řekne. Nepřemýšlí o významu.
Bylo by dobré uživateli, který zadá záporné číslo,
přímo říct, že zadal blbost. Jak na to?

Nejdřív zkus nastavit proměnnou která bude `True`,
když uživatel zadal kladné číslo.


{% filter solution %}
    Taková proměnná se dá nastavit pomocí tohoto kódu:

    ```python
    strana = float(input('Zadej stranu čtverce v centimetrech: '))
    cislo_je_spravne = strana > 0
    ```
{% endfilter %}

A nyní řekneme počítači, aby tuhle proměnnou použil.
K tomu se používá dvojice příkazů `if` (*pokud*)
a `else` (*jinak*).
Nejlepší bude je ukázat na příkladu:

```python
strana = float(input('Zadej stranu čtverce v centimetrech: '))
cislo_je_spravne = strana > 0

if cislo_je_spravne:
    print('Obvod čtverce se stranou', strana, 'je', 4 * strana, 'cm')
    print('Obsah čtverce se stranou', strana, 'je', strana * strana, 'cm2')
else:
    print('Strana musí být kladná, jinak z toho nebude čtverec!')

print('Děkujeme za použití geometrické kalkulačky.')
```

Neboli: po `if` následuje *podmínka* (angl. *condition*),
což je výraz, podle kterého se budeme rozhodovat.
Za podmínkou je dvojtečka.
Potom následují příkazy, které se provedou, pokud je podmínka pravdivá.
Všechny jsou odsazeny o čtyři mezery.<br>
Po téhle části stačí napsat neodsazené `else:`, zase s dvojtečkou na konci,
a odsazené příkazy, které se provedou v opačném případě.<br>
Potom můžeš psát příkazy, které se provedou vždycky – ty odsazené nebudou,
podmíněná část programu už skončila.

> [note]
> Čistě technicky, odsazení nemusí být o čtyři mezery.
> Může být třeba o dvě nebo o jedenáct, nebo dokonce o tabulátor.
> V rámci jednoho bloku musí být ale odsazení vždycky stejné,
> takže když pak na jednom programu spolupracuje více lidí, musí se shodnout.
> No a na čtyřech mezerách se shodla většina Pythonního světa.

## Další podmíněné příkazy

Někdy není `else` vůbec potřeba.
V následujícím programu se nedělá nic navíc, pokud je číslo nenulové:

```python
cislo = int(input('Zadej číslo, přičtu k němu 3: '))
if cislo == 0:
    print('Jé, to je jednoduché!')
print(cislo, '+ 3 =', cislo + 3)
```

Někdy je naopak potřeba podmínek několik,
k čemuž slouží příkaz `elif` – kombinace `else` a `if`.
Dává se „mezi“ bloky `if` a `else`.
Příkazů `elif` může být za jedním `if`-em několik,
ale vždy se provede jen jedna „větev“:
ta první, jejíž podmínka je splněna.

```python
vek = int(input('Kolik ti je let? '))
if vek >= 150:
    print('A ze kterépak jsi planety?')
elif vek >= 18:
    # Tahle větev se např. pro "200" už neprovede.
    print('Můžeme nabídnout: víno, cider, nebo vodku.')
elif vek >= 1:
    print('Můžeme nabídnout: mléko, čaj, nebo vodu')
elif vek >= 0:
    print('Sunar už bohužel došel.')
else:
    # Nenastala ani nedna ze situací výše – muselo to být záporné
    print('Návštěvníky z budoucnosti tady nevidíme rádi.')
```

## Kámen nůžky papír

Příkazy `if` se dají *zanořovat* (angl. *nest*):
jeden může být vevniř ve druhém.
Třeba takhle:

```python
tah_pocitace = 'kámen'
tah_cloveka = input('kámen, nůžky, nebo papír? ')

if tah_cloveka == 'kámen':
    if tah_pocitace == 'kámen':
        print('Plichta.')
    elif tah_pocitace == 'nůžky':
        print('Vyhrála jsi!')
    elif tah_pocitace == 'papír':
        print('Počítač vyhrál.')
elif tah_cloveka == 'nůžky':
    if tah_pocitace == 'kámen':
        print('Počítač vyhrál.')
    elif tah_pocitace == 'nůžky':
        print('Plichta.')
    elif tah_pocitace == 'papír':
        print('Vyhrála jsi!')
elif tah_cloveka == 'papír':
    if tah_pocitace == 'kámen':
        print('Vyhrála jsi!')
    elif tah_pocitace == 'nůžky':
        print('Počítač vyhrál.')
    elif tah_pocitace == 'papír':
        print('Plichta.')
else:
    print('Nerozumím.')
```

Vida, tvoje první hra!
Jen je ještě potřeba před každým spuštěním přepsat řetězec na prvním řádku.
Jak zařídit, aby počítač vybíral náhodně, to si povíme později.
