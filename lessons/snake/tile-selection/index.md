# Vybírání kousků hada

Místo toho, aby byl všude stejný kousek hada,
budeme chtít vybrat vždycky ten správný.

Jak na to?
Podle čeho ho vybrat?

Obrázky s kousky hada jsou pojmenovány
<code><var>odkud</var>-</var>kam</var>.png</code>.
To není náhoda – ukazuje to, co potřebuješ vědět, abys mohl{{a}} ten správný
kousek vybrat.

Když máš hada podle následujícího obrázku, na políčko (3, 2) patří
kousek, na kterém had „leze“ zleva nahoru – tedy `left-top.png`

{{ figure(
    img=static('tile-selection.svg'),
    alt="Had na „šachovnici“ se souřadnicemi. Políčko (3, 2) je zvýrazněné a vedou z něj šipky doleva a nahoru, kudy had pokračuje.",
) }}

Na koncích hada je ve jménech obrázků místo směru `end`.

Pro každé z políček budeš potřebovat zjistit, odkud a kam na něm had leze –
tedy směr k *předchozí* a *následující* souřadnici:

<table class="table">
    <tr>
        <th>Souřadnice</th>
        <th>Předchozí</th>
        <th>Směr k předchozí</th>
        <th>Následující</th>
        <th>Směr k následující</th>
        <th></th>
    </tr>
    {% set data = [
        (1, 2, 'end', 'right'),
        (2, 2, 'left', 'right'),
        (3, 2, 'left', 'top'),
        (3, 3, 'bottom', 'top'),
        (3, 4, 'bottom', 'top'),
        (3, 5, 'bottom', 'right'),
        (4, 5, 'left', 'end'),
    ] %}
    {% for x, y, bef, aft in data %}
        <tr>
            <td>({{ x }}, {{ y }})</td>
            <td>{% if loop.first %}<em>není</em>{% else %}
                ({{ data[loop.index0-1][0] }}, {{ data[loop.index0-1][1] }})
            {% endif %}</td>
            <td><code>{{ bef }}</code></td>
            <td>{% if loop.last %}<em>není</em>{% else %}
                ({{ data[loop.index0+1][0] }}, {{ data[loop.index0+1][1] }})
            {% endif %}</td>
            <td><code>{{ aft }}</code></td>
            <td>
                <img
                    src="{{ static('snake-tiles/' + bef + '-' + aft + '.png') }}"
                    style="width: 1em"
                    alt="{{ bef }}-{{ aft }}.png"
                >
            </td>
        </tr>
    {% endfor %}
</table>

Toto je **těžký úkol**.
I když všechny potřebné informace a nástroje k tomu teď teoreticky znáš,
je potřeba je správným způsobem poskládat dohromady.
Tohle skládání dohromady, *návrh algoritmů*, je nejsložitější programátorská 
disciplína.

Zkus nad tím ale přemýšlet, nech si to rozležet v hlavě třeba přes noc,
vrať se k materiálům k předchozím lekcím (hlavně k úvodu do Pythonu),
zkoušej a objevuj… A časem na to přijdeš.

Jestli nemáš čas, koukněme se na to, jak se dá zařídit.


## Tohle není evangelium

Popisuju tady jedno možné řešení.
Existuje spousta jiných správných způsobů, jak vybírat políčka hada.
Možná ti dokonce jiné řešení přijde jednodušší – a možná to bude dokonce
*tvoje* řešení!


## Jednodušší podproblémy

Složité problémy programátoři většinou vhodně rozdělí na více jednodušších
problémů.
Každý pak vyřeší zvlášť a pak spojí dohromady.

Jaké jednodušší úkoly by se daly najít tady?

1. Projít všechny souřadnice, a pro každou z nich políčko zjistit
   předchozí i následující souřadnici.
2. Když mám dvě souřadnice, zjistit směr od jedné ke druhé.

Řešením prvního z nich v tabulce výše „vyplníš“ sloupečky se souřadnicemi.
Řešením druhého pak z těchto informací dostaneš *směry*, části jména obrázku.

Budeš potřebovat vyřešit oba dva problémy.
Ten druhý je ale jednodušší, tak se pojďme zaměřit na něj.

## Zjistit směr

Potřebuješ počítači říct, jak ze souřadnic dvou políček, které jsou vedle sebe,
zjistit směr od jednoho ke druhému.

Například směr od (3, 2) k (2, 2) je *doleva*.
Směr od (3, 2) k (3, 3) je *nahoru*.
(Viz obrázek, nebo třetí řádek tabulky výše.)

{{ figure(
    img=static('tile-selection.svg'),
    alt="Had na „šachovnici“ se souřadnicemi. Políčko (3, 2) je zvýrazněné a vedou z něj šipky doleva a nahoru, kudy had pokračuje.",
) }}

V Pythonu to napíšeš jako *funkci*, která bere dva argumenty (souřadnice)
a vrátí anglické jméno směru – řetězec, který se dá použít ve jméně souboru
s obrázkem.

Až bude tahle funkce hotová, měla by se dát použít následovně:

```pycon
>>> direction((3, 2), (2, 2))
'left'
>>> direction((3, 3), (3, 2))
'bottom'
>>> direction((3, 3), 'end')
'end'
```

Na koncích hada bude potřeba jako druhou souřadnici použít místo dvojice čísel
něco jiného.
Řetězec `'end'` funguje dobře, ale stejně tak by se dalo použít cokoli jiného,
co není souřadnice: `False`, `-1`, nebo třeba `[]`.
(Zkušený Pythonista by použil hodnotu `None`.)

Jak takovou funkci napsat?
Když si pořádně prohlédneš první tři sloupce tabulky výše, možná přijdeš na to,
jak se od sebe liší souřadnice, které jsou *nalevo* od sebe. Nebo *nahoru*.

* Jak zjistit směr mezi dvěma souřadnicemi:
  * Když ta druhá není souřadnice:
    * výsledek je `'end'`
  * Když se <var>x</var> té první rovná <var>x</var>+1 druhé:
    * výsledek je `'left'`
  * Když se <var>x</var> té první rovná <var>x</var>-1 druhé:
    * výsledek je `'right'`
  * Když se <var>y</var> té první rovná <var>y</var>+1 druhé:
    * výsledek je `'bottom'`
  * Když se <var>y</var> té první rovná <var>y</var>-1 druhé:
    * výsledek je `'top'`

Zkušený programátor v tento moment zbystří a zeptá se: „ale co když neplatí
ani jedna z těch podmínek“?
Taková situace ve hře nemůže nastat (nebo ano?), ale přesto je dobré ji
podchytit a na konec postupu přidat třeba „Jinak je výsledek `'end'`”.

To je složitější část řešení našeho problému.
Zbytek je jen téměř doslovný překlad z češtiny do Pythonu:

```python
def direction(a, b):
    if b == 'end':
        return 'end'

    # Rozložení souřadnic na čísla (x, y) – to je v češtině "samozřejmé"
    x_a, y_a = a
    x_b, y_b = b

    # ... a logika pokračuje
    if x_a == x_b + 1:
        return 'left'
    elif x_a == x_b - 1:
        return 'right'
    elif y_a == y_b + 1:
        return 'bottom'
    elif y_a == y_b - 1:
        return 'top'
    else:
        return 'end'

# Vyzkoušení
print('tohle by mělo být "left":', direction((3, 2), (2, 2)))
print('tohle by mělo být "bottom":', direction((3, 3), (3, 2)))
print('tohle by mělo být "top":', direction((3, 2), (3, 3)))
print('tohle by mělo být "right":', direction((1, 1), (2, 1)))
print('tohle by mělo být "end":', direction((3, 3), 'end'))
print('tohle by mělo být "end":', direction((3, 3), (80, 80)))
```


## Projít všechny souřadnice

Teď se vraťme k prvnímu problému: jak projít všechny políčka hada,
a u každého vědět předchozí a následující?

Protože rozdíl mezi souřadnicemi jako (1, 2) a (2, 2) není na první pohled
moc čitelný, kousky hada si označím písmenky.
Budu psát A místo (1, 2); B místo (2, 2); atd.:

{{ figure(
    img=static('lettered.svg'),
    alt="Had na „šachovnici“. Každý kousek hada má písmenko: A, B, C, ..., G",
) }}

Takového hada nakreslím následovně:

* Nakreslím políčko A (k čemuž potřebuju vědět, že je to začátek a po něm je B)
* Nakreslím políčko B (k čemuž potřebuju vědět, že před ním je A a po něm B)
* Nakreslím políčko C (k čemuž potřebuju vědět, že před ním je B a po něm D)
* … a tak dál:

<table class="table">
    {% set alphabet = 'ABCDEFGH' %}
    <tr>
        <th>K vykreslení</th>
        {% for x, y, bef, aft in data %}
            <td>{{ alphabet[loop.index0] }}</td>
        {% endfor %}
    </tr>
    <tr>
        <th>Předchozí</th>
        {% for x, y, bef, aft in data %}
            <td>
            {% if loop.first %}×{% else %}
                {{ alphabet[loop.index0-1] }}
            {% endif %}
            </td>
        {% endfor %}
    </tr>
    <tr>
        <th>Následující</th>
        {% for x, y, bef, aft in data %}
            <td>
            {% if loop.last %}×{% else %}
                {{ alphabet[loop.index0+1] }}
            {% endif %}
            </td>
        {% endfor %}
    </tr>
</table>

Jak na to?
První řádek tabulky, seznam [A, B, C, D, E, F, G] už máš – to jsou souřadnice
hada, `snake`.
Kdyz se ti k tomu podaří připravit seznamy s druhým řádkem,
[×, A, B, C, D, E, F], a třetím, [B, C, D, E, F, G, ×], můžeš je pak spojit
pomocí funkce `zip`.
Vzpomínáš na ni?
Prochází několik „opovídajících si“ seznamů a dá <var>n</var>-tici
prvních prvků, pak <var>n</var>-tici druhých prvků, pak třetích…

Náš příklad byl:

```python
veci = ['tráva', 'slunce', 'mrkev', 'řeka']
barvy = ['zelená', 'žluté', 'oranžová', 'modrá']
mista = ['na zemi', 'nahoře', 'na talíři', 'za zídkou']

for vec, barva, misto in zip(veci, barvy, mista):
    print(barva, vec, 'je', misto)
```

Ale stejně tak můžeš použít:

```python
snake = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
prevs = ['x', 'A', 'B', 'C', 'D', 'E', 'F']
nexts = ['B', 'C', 'D', 'E', 'F', 'G', 'x']

for coords, prev, next in zip(snake, prevs, nexts):
    print('na políčku', coords, 'had leze z', prev, 'do', next)
```

Ty dva další seznamy je ale potřeba „vyrobit“ z prvního:
vybrat správný kousek a na správnou stranu doplnit „chybějící“ prvek:

```python
snake = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
prevs = ['end'] + snake[:-1]
nexts = snake[1:] + ['end']

for coords, prev, next in zip(snake, prevs, nexts):
    print('na políčku', coords, 'had leze z', prev, 'do', next)
```

Anebo, s „opravdovými“ souřadnicemi a funkcí `direction`:

```python
snake = [(1, 2), (2, 2), (3, 2), (3, 3), (3, 4), (3, 5), (4, 5)]

for coords, prev, next in zip(snake, ['end'] + snake[:-1], snake[1:] + ['end']):
    before = direction(coords, prev)  # směr z aktuálního políčka na předchozí
    after = direction(coords, next)   # směr z aktuálního políčka na následující
    print('na', coords, 'vykreslit:', before + '-' + after)
```

Jestli jsi {{gnd('došel', 'došla')}} až sem, doufám, že nebudeš mít příliš
velké problmy s „transplantací“ tohoto kódu do tvojí hry.
