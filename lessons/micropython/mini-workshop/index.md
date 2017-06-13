
> [note]
>
> Tento workshop nejde projít jen tak z domu – je potřeba speciální příprava.
> Pokyny pro organizátory najdeš
> na [podstránce]({{ subpage_url('organizers') }}).

Jedna varianta Pythonu, MicroPython, běží na malých zařízeních.
Taková zařízení si teď můžeš vyzkoušet.

Jak na to?


## Otevření příkazové řádky

<img src="{{ static('icon_terminal.png')}}" style="float:right;height:5em;">

Klikni na *Activities*; potom vyber z levého panelu *Terminal* (ikonka
černého okýnka).

Objeví se černé okýnko s bílým textem, kam můžeš zadávat příkazy – příkazová
řádka.



## Otevření komunikačního kanálu

V příkazové řádce by měl být řádek končící dolarem.
Za ten dolar napiš:

```bash
picocom -b 115200 /dev/ttyUSB0
```

Opisuj opatrně, každé písmenko má smysl!
Pak zmáčkni Enter.
Měl by se objevit následující výpis:

```plain
picocom v1.7

port is        : /dev/ttyUSB0
flowcontrol    : none
baudrate is    : 115200
parity is      : none
databits are   : 8
escape is      : C-a
local echo is  : no
noinit is      : no
noreset is     : no
nolock is      : no
send_cmd is    : sz -vv
receive_cmd is : rz -vv
imap is        : 
omap is        : 
emap is        : crcrlf,delbs,

Terminal ready
```

Pak stiskni Enter.
Měly by se objevit tři zobáčky, kterými MicroPython prosí o instrukce:

```plain
>>>
```


<div style="page-break-after: always;"></div>

## Kalkulačka

Za tři zobáčky můžeš zadat nějaký matematický příklad. MicroPython ho spočítá.
Zkus třeba tyhle (zobáčky nepiš, ty vypíše sám MicroPython:

```pycon
>>> 1 + 1

>>> 3 * 3

>>> 1 / 4

>>> (84 + 5) * 253
```


## Světýlko

MicroPython na našich destičkách má připravený objekt `led`, jehož metodou
`value` jde ovládat svítící dioda.
Stačí jen zadat správné příkazy:

```pycon
>>> led.value(1)
>>> led.value(0)
```


## Tlačítko

K destičce je připojeno i tlačítko.
Metodou `btn.value()` se zeptáš, jestli je právě zmáčknuté nebo ne.

```pycon
>>> btn.value()
```

Zkus tenhle příkaz zadat, zatímco tlačítko držíš.


## Výrazy

Informace o tom, jestli je tlačítko zmáčknuté – `btn.value()` – je číslo:
buď 0 nebo 1.
Výraz `btn.value()` můžeš použít kdekoliv, kde se objevuje číslo
0 nebo 1 – třeba pro rozsvícení nebo zhasnutí diody:

```pycon
>>> led.value(btn.value())
```


## Cyklus

Existuje způsob, jak nechat MicroPython něco opakovat stále dokola:
takzvaný *nekonečný cyklus*.
Na jeden řádek napiš `while True:` (s velkým T a dvojtečkou na konci),
a potom *tělo cyklu* – příkaz, který se má provést.
MicroPython tělo cyklu automaticky *odsadí* – přidá na začátek řádku
mezery. Ty mezery nemaž.

Nakonec několikrát stiskni Enter, dokud se program nespustí.

```pycon
>>> while True:
...     led.value(btn.value())
...
...
```

Nekonečný cyklus se opakuje donekonečna.
Je ale způsob jak ho přerušit, až tě omrzí: zmáčkni
<kbd>Ctrl</kbd>+<kbd>C</kbd>.

<div style="page-break-after: always;"></div>

## Motorek

Další objekt, který můžeš použít, je `servo`.
Ten ovládá servomotor, který můžeš nastavit na konkrétní úhel. Třeba:

```pycon
>>> servo.duty(120)
>>> servo.duty(40)
```

... nebo něco mezi tím.

Nepoužívej prosím čísla menší než 40 nebo větší než 120, motorek se tím může
ničit.


## Matematika

Před chvílí jsme si ukázali tento kód:

```pycon
>>> led.value(btn.value())
```

Hodnota `btn.value()` může být buď 1 nebo 0.
Pojďme ji použít pro motorek: chceme, aby se natočil buď na `40` nebo na
`120`, podle toho, jestli je tlačítko zmáčknuté.
Použij trochu matematiky:

    40 + 0 * 80 = 40
    40 + 1 * 80 = 120

a dostaneš následující kód:

```pycon
>>> servo.duty(40 + btn.value() * 80)
```

Změníš program tak, aby se natáčel na `50` nebo `90`?

Dokážeš výsledek dát do cyklu, aby program na zmáčknutí či puštění tlačítka
reagoval automaticky?


## Barvy

Poslední věc připojená k destičce je LED pásek s *několika* světýlky.
Každé z nich se dá nastavit na nějakou barvu.
Zkus si to:

```pycon
>>> strip[0] = RED
>>> strip[1] = GREEN
>>> strip[2] = BLUE
>>> strip.write()
```

První tři příkazy připravují jednotlivé barvy, a poslední všechno připravené
pošle do LED pásku.
Až budeš experimentovat, nezapomeň na `strip.write()` – bez toho
se barvy neukážou.

<div style="page-break-after: always;"></div>

## Program

<img src="{{ static('icon_gedit.png')}}" style="float:right;height:5em;">

Teď si přestaneme jen tak hrát, a začneme psát program.

Spusť *editor*: Klikni na *Activities*; potom vyber z levého panelu
*Text Editor* (ikonka zápisníku s tužkou).

Objeví se bílé okýnko, do kterého napiš:

```python
strip[0] = WHITE
strip[1] = OFF
strip[2] = OFF
strip.write()
```

Soubor ulož (*Save*) pod jménem `main.py`.

Potom se vrať k příkazové řádce a ukonči `picocom`:
stiskni <kbd>Ctrl</kbd>+<kbd>A</kbd> a pak <kbd>Ctrl</kbd>+<kbd>Q</kbd>.
Měl by se objevit řádek končící dolarem.

Za dolar napiš:

```bash
ampy -p /dev/ttyUSB0 run main.py
```

... a stiskni Enter.
Tento příkaz soubor s programem do zařízení nahraje a rovnou spustí.

Zkus v editoru nastavit jiné barvy a program znovu uložit
(<kbd>Ctrl</kbd>+<kbd>S</kbd>).

Potom v příkazové řádce zmáčkni *šipku nahoru*.
Tím se vrátíš k předchozímu příkazu (`ampy`), a můžeš znovu stisknout Enter
a program spustit.


## Blikání

Tady je program, který rozbliká LED pásek.
Ukazuje větší cyklus, a navíc funkci `sleep`, která MicroPython na chvíli
zdrží: `sleep(1/4)` čeká čtvrtinu sekundy.

Při přepisování dávej pozor na odsazení – řádky vevnitř v cyklu musí být
všechny odsazené o čtyři mezery.

```python
strip[0] = OFF
strip[1] = OFF
strip[2] = OFF

while True:
    strip[0] = RED
    strip[1] = OFF
    strip.write()
    sleep(1/4)

    strip[0] = OFF
    strip[1] = RED
    strip.write()
    sleep(1/4)
```

## Semafor

<img src="{{ static('semafor.gif')}}" style="float:right;height:5em;">

Dokážeš naprogramovat semafor?

Se závorou?

{# <div style="page-break-after: always;"></div> #}

## Cyklus s podmínkou

Cykly nemusí být jen nekonečné.
Tady je cyklus, který čeká dokud není stisknuté tlačítko.

Potom se rozsvítí světlo – všimni si, že příkaz `led.value(1)` už není
odsazený. Není součást cyklu.

```python
led.value(0)

while btn.value():
    sleep(1/100)

led.value(1)
```


## Alarm

Polož na tlačítko nějaký těžší předmět (třeba myš) tak, aby bylo zmáčknuté.
Když někdo předmět vezme, tlačítko přestane být zmáčknuté.

Napiš program, který na to bude čekat, a jakmile někdo myš ukradne,
LED pásek začne zuřivě blikat.


## Konec?

Tím dnešní krátká exkurze do světa MicroPythonu končí.
Jestli tě programování zaujalo a chceš v něm pokračovat, dej nám vědět!

Nebo pak z klidu domova napiš Petrovi na pviktori@redhat.com.


