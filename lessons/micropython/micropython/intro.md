## MicroPython – taky Python

Tak jako máš na počítači nainstalovaný operační
systém, na vývojové desce je takzvaný *firmware*,
program, který ovládá všechny ty drátky,
čipy a světýlka, co v ní jsou.
My používáme firmware zvaný *MicroPython*,
který navíc rozumí jazyku Python a umí provádět pythonní příkazy. Zkus si to!
Tři zobáčky, které vyskočily v minulém kroku, přišly
ze zařízení, které teď netrpělivě čeká na příkaz.

```pycon
>>> 1+1
2
>>> print('Hello World')
Hello World
```

Téměř vše, co používáš v Pythonu na počítači,
umí MicroPython taky: čísla, řetězce, seznamy, třídy,
výjimky, moduly a tak dál.
Některé detaily ale jsou trochu osekané, aby se všechno
vešlo do extrémně malého prostoru.
Zkus si, jak se liší efekt následujících příkazů
od „velkého” Pythonu:

```pycon
>>> print
>>> import math
>>> math.pi
```

Nejdůležitější věc, která je osekaná, je *standardní
knihovna* – většina modulů, které na
počítači můžeš naimportovat, v MicroPythonu chybí.
U modulů jako `turtle` je to pochopitelné,
ale v rámci šetření místem chybí i moduly jako `random`.
Většinou to příliš nevadí – malá zařízení se používají
na jiné věci než ty velké – ale je potřeba si na to
dát pozor.

Některé věci ze standardní knihovny se dají najít
ve zjednodušené formě na jiných místech.
Například ačkoliv modul `random` chybí,
náhodné číslo od 0 do 255 se dá získat pomocí:

```pycon
>>> from os import urandom
>>> urandom(1)[0]
61
```


## Ovládání konzole

Při psaní složitějšího kódu si všimneš, že konzole MicroPythonu automaticky odsazuje.
To je pro malé programy pohodlné, ale umí to i znepříjemnit život – hlavně když chceš
kód do konzole zkopírovat odjinud.

Proto má konzole MicroPythonu speciální vkládací mód, který automatické odsazování vypíná.
Aktivuje se pomocí <kbd>Ctrl+E</kbd> a ukončuje se pomocí <kbd>Ctrl+D</kbd>.
