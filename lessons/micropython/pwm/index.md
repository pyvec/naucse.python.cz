## Velice rychle blikat

Jedna z nevýhod „našeho” čipu ESP8266 je, že na svých
nožičkách umí nastavovat jen dvě hodnoty – 3,3 V a zem, jedničku a nulu.
Dioda tak buď svítí, nebo nesvítí – nedá se
nastavit poloviční intenzita, nedá se plynule rozsvěcet nebo zhasínat.

Tuhle nevýhodu ale můžeme obejít s využitím dvou faktů.
Ten první je, že diodám – na rozdíl od žárovek nebo
zářivek – nevadí časté vypínání a zapínání.
Opotřebovávají se spíš svícením a časem.
Druhý je, že lidské oko nestačí zaznamenat pohyby a
změny, které probíhají rychleji než zhruba za
setinu vteřiny.

Pojďme tedy velice rychle blikat – a oblafnout tak naše oči a mozky!

```python
from machine import Pin
from time import sleep

pin_diody = Pin(14, Pin.OUT)
while True:
    pin_diody.value(0)  # vypnout LED
    sleep(2/100)  # počkat dvě setiny vteřiny
    pin_diody.value(1)  # zapnout LED
    sleep(1/100)  # počkat jednu setinu vteřiny
```

Zkus si pohrát s hodnotami pro `time.sleep`.

> [note]
> Takhle fungují prakticky všechna stmívatelná LED
> světla – rychlé blikání je ekonomičtější a přesnější
> než např. nastavování nižšího napětí.

Dokážeš napsat program, který diodu postupně, plynule rozsvítí?

{% filter solution %}
```python
from machine import Pin
from time import sleep

pin_diody = Pin(14, Pin.OUT)

for x in range(100):
    pin_diody.value(0)
    sleep((100-x)/10000)
    pin_diody.value(1)
    sleep(x/10000)
```

Princip je úplně stejný, jen proměnná `x` se neustále mění a tím ovlivňuje
intenzitu svícení.
{% endfilter %}


Protože je takovéhle rychlé blikání užitečné ve spoustě
různých situací, obsahuje MicroPython speciální funkci: umí blikat samostatně.
Nastavíš, jak rychle má blikat a jak dlouho má trvat
každé bliknutí, a MicroPython pak bude blikat automaticky,
zatímco tvůj program se může věnovat něčemu jinému.

Téhle funkci se říká *pulzně šířková modulace* –
angl. *Pulse Width Modulation*, neboli *PWM*.
Z MicroPythonu jde tahle funkce ovládat pomocí třídy
`machine.PWM`.
Každý objekt téhle třídy umí ovládat jednu nožičku
a dají se u něj nastavit dva parametry:

* `freq` – frekvence, tedy kolikrát za sekundu se LED rozsvítí a zase zhasne a
* `duty` – anglicky *duty cycle*, česky *střída*, nastavuje „šířku pulzu”,
  tedy jak dlouho bude dioda při každém bliknutí svítit.
  Hodnota `duty` může být od 0, kdy LED
  nesvítí vůbec, do 1023, kdy svítí celou dobu.
  Nastavíš-li `duty=512`, bude dioda
  svítit s poloviční intenzitou (512 = 1024/2).

Nastavíš-li `PWM(freq=50, duty=512)`, dioda bude blikat 50× za sekundu.
Vždycky jednu setinu vteřiny bude svítit a na jednu
setinu vteřiny zhasne.

```python
from machine import Pin, PWM

pin_diody = Pin(14, Pin.OUT)
pwm = PWM(pin_diody, freq=50, duty=512)
```

Zkus nastavit i nižší frekvenci, třeba 3 nebo 1, ať blikání vidíš přímo!

PWM se dá zrušit metodou `pwm.deinit()`.
Jako s otvíráním souborů, je dobré po sobě uklidit –
i když zatím můžeš jednoduše restartovat celé zařízení.
