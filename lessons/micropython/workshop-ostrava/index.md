# MicroPython na malém zařízení

> [note] Tahle sekce bohužel nejde jednoduše projít z domu.
> Využíváme speciální vybavení, které je potřeba nejdřív
> sehnat. Máš-li možnost se dostat na sraz, nebo
> aspoň kontaktovat organizátory, doporučujeme shánět
> spíš tímto způsobem.
> Případně jde daný hardware objednat přes Internet,
> typicky z čínských e-shopů.

> [note]
> Materiály byly připraveny pro celodenní workshop;
> na kratší lekcích může být něco vynecháno.

{{ figure(
    img=static('nodemcu-devkit.jpg'),
    alt='LoLin NodeMCU v3 – Vývojová deska s čipem ESP8266',
    float='right',
) }}

Dnes budeme programovat malé zařízení –
tak malé, že se ho pohodlně schováš v ruce.
Konkrétně budeme používat „chytrou destičku”, modul zvaný
*NodeMCU Devkit*, která by měla ležet před tebou.
Než ji vyndáš z obalu, měl/a by ses *vybít*:
dotkni se něčeho kovového, co je spojeno se zemí,
třeba radiátoru nebo kovové části schránky nějakého
spotřebiče, který je zapojený do zásuvky.
Tím se zbavíš statické elektřiny, která by mohla
malinké zařízení poškodit.
Pak přístroj vyndej z obalu. Snaž se ho držet za
hrany a příliš se nedotýkat elektroniky a kovových
částí.

> [note]
> Obal bude nejspíš roztržený, protože organizátoři
> na destičku před začátkem kurzu nainstalovali
> MicroPython.

> [warning]
> Obal je vodivý a nesmí přijít do styku se zapojenou destičkou,
> protože by mohl zkratovat její vývody a tím ji zničit.
> Proto obal raději hned schovej a používej ho jen k transportu destičky.

Teď, když destičku držíš v ruce, si
pojďme projít její základní součásti.

<br style='clear: both;'>

{{ figure(
    img=static("nodemcu-popisky.svg"),
    alt='Obrázek desky NodeMCU DevKit',
    float='left',
) }}

Nejdůležitější část vývojové desky je v oplechované
krabičce s logem "Wi-Fi" a "FCC":
<span class="part-green">mikroprocesor ESP8266</span>.
To je „mozek” celého zařízení, který – když je
správně naprogramován – umí provádět pythonní
příkazy a programy.
Procesor sedí na malé destičce, na které je ještě
<span class="part-cyan">anténa</span>, kterou
přístroj může komunikovat s okolím.

Tahle malá destička se dá použít i samostatně;
všechno ostatní, co kolem ní zabírá tolik místa,
nám jen ulehčí hraní a umožní se zařízením
jednoduše komunikovat a krmit ho elektřinou.

Komunikace a „krmení” se děje přes
<span class="part-red">mikro-USB konektor</span>,
do kterého zapojíš kabel ze svého počítače.
Když je modul naprogramovaný, stačí ho místo do
počítače zapojit do nabíječky či externího zdroje
(powerbanky) a bude fungovat samostatně.

Kolem USB konektoru jsou dvě tlačítka:
<code class="part-orange">RST</code>, kterým se destička restartuje
(skoro jako kdybys ho odpojila a zase zapojila, což
se hodí, když něco uděláš špatně a modul „zamrzne”),
a <code class="part-yellow">FLASH</code>, o kterém si povíme později.

Po stranách modulu jsou dvě řady
<span class="part-blue">„nožiček”</span>, na které
se dá napojit celá řada nejrůznějších hraček.
Zkontroluj si, jestli jsou všechny nožičky rovné;
kdyby byla některá ohnutá, tak ji (nejlépe s pomocí
kouče) narovnej nebo si vezmi jinou destičku.

<br style='clear: both;'>


## Instalace

Bohužel se dnes neobejdeme bez instalace. Musíš naučit
svůj počítač, aby si s destičkou povídal.

Nejdřív si do virtuálního prostředí nainstaluj program Ampy od Adafruitu.
Ten budeme později používat na nahrávání kódu:

```console
(env)$ python -m pip install adafruit-ampy
```

Pak propoj modul s počítačem přes USB kabel,
jako kdybys připojoval{{a}} třeba mobil.

> [note]
> Je potřeba použít kvalitní datový kabel.
> Nekvalitní kabely (např. spousta kabelů k
> nabíječkám) jsou často nepoužitelné.

Dál postupuj podle operačního systému na svém počítači.
Kdyby něco nefungovalo, poraď se s koučem.
Původní (anglický) návod k této části je na
<a href="http://docs.micropython.org/en/latest/pyboard/pyboard/tutorial/repl.html">stránkách MicroPythonu</a>.


### Linux

Na správně nastaveném počítači stačí zadat:

```console
$ picocom -b 115200 --flow n /dev/ttyUSB0
```

Pokud příkaz neskončí s chybou, stiskni tlačítko `RST` na modulu.
Měly by se nakonec objevit tři zobáčky, `>>>`.

Většina počítačů ale na komunikaci s malými zařízeními nastavená není.
Skončí-li příkaz `picocom` s chybou,
oprav ji podle následujícího návodu a zkus to znova.
(Možná bude potřeba vyřešit víc než jednu chybu.)

* Nemáš-li příkaz `picocom` nainstalovaný,
  je potřeba ho nainstalovat (např.
  `sudo dnf install picocom` nebo
  `sudo apt-get install picocom`).
* Pokud `picocom` skončil s chybou
  `No such file or directory`, pravděpodobně
  je potřeba k zařízení přistupovat přes jiný soubor.
  Použij příkaz `dmesg | tail`, který vypíše něco jako:

  {#- XXX: ttyUSB0 should be highlighted #}

  ```console
  $ dmesg | tail
  [703169.886296] ch341 1-1.1:1.0: device disconnected
  [703176.972781] usb 1-1.1: new full-speed USB device number 45 using ehci-pci
  [703177.059448] usb 1-1.1: New USB device found, idVendor=1a86, idProduct=7523
  [703177.059454] usb 1-1.1: New USB device strings: Mfr=0, Product=2, SerialNumber=0
  [703177.059457] usb 1-1.1: Product: USB2.0-Serial
  [703177.060474] ch341 1-1.1:1.0: ch341-uart converter detected
  [703177.062781] usb 1-1.1: ch341-uart converter now attached to ttyUSB0
  ```

  Máš-li místo `ttyUSB0` něco jiného, v příkazu `picocom` to použij místo
  `ttyUSB0`.

* Pokud `picocom` skončil s chybou `Permission denied`, potřebuješ získat
  přístup k souboru zařízení.
  To znamená přidat se do příslušné skupiny:

  ```console
  $ sudo usermod -a -G dialout $(whoami)
  ```

  Poté je potřeba se znovu přihlásit, třeba příkazem:

  ```console
  $ su - $(whoami)
  ```

  Pro ověření spusť příkaz `groups`; v jeho výstupu by mělo být `dialout`.
  Například:

  ```console
  $ groups
  kristyna lp wheel dialout mock
  ```

  Kdyby to nefungovalo, na srazu ti může pomoci nějaký kouč.
  Jestli procházíš materiály z domu a nepovedlo
  se ti přidat do skupiny, dá se to obejít tak,
  že místo `picocom` použiješ `sudo picocom`.


### Windows

MicroPython se přihlásí jako COM port. Otevři
správce zařízení a zjisti, který COM port to je (kouč s tím pomůže).

Nebylo-li zařízení nalezeno, je potřeba nainstalovat
*driver*, který je ke stažení třeba
[z tohoto blogu](https://iotta.cz/ovladace-pro-ch340g/).

Pak si nainstaluj program
[PuTTY](http://www.chiark.greenend.org.uk/~sgtatham/putty/download.html)
(`putty.exe`) a spusť ho.
V konfiguračním okýnku zaškrtni *Connection Type: Serial* a
do *Serial line:* zadej svůj COM port.
Pak přepni v seznamu vlevo na *Serial* a nastav *Speed* na *115200*
a *Flow Control* na *None*:

{{ figure(
    img=static("putty-config.jpg"),
    alt='Obrázek nastavení PuTTY',
) }}
{# XXX: Better picture #}

Potom zpátky v kategorii *Session* můžeš nastavení uložit pro příště:
do políčka *Saved Sessions* zadej *MicroPython* a klikni OK.

Nakonec klikni *Open*. Mělo by se otevřít
okýnko podobné konzoli, kde se, když zmáčkneš
na modulu `RST`, objeví nakonec tři zobáčky: `>>>`.


### macOS

V příkazové řádce zadej:

```console
$ screen /dev/tty.usbmodem* 115200
```

a stiskni Enter.
Pak na modulu zmáčkni `RST`.
Měly by se nakonec objevit tři zobáčky, `>>>`.

Nejde-li to, je možná potřeba nainstalovat driver. Ten se dá stáhnout
z [tohoto blogu](https://iotta.cz/ovladace-pro-ch340g/).


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
To je pro malé programy pohodlné, ale umí to i znepříjemnit život – hlavně když chceme kód do konzole vložit.

Proto má konzole MicroPythonu speciální vkládací mód, který automatické odsazování vypíná.
Aktivuje se pomocí <kbd>Ctrl+E</kbd> a ukončuje se pomocí <kbd>Ctrl+D</kbd>.

## Vstup

MicroPython na malé destičce obsahuje některé
moduly, které jinde nenajdeš. Ten hlavní se jmenuje
`machine` a zpřístupňuje základní funkce zařízení. Zkus si:

```python
from machine import Pin
pin = Pin(0, Pin.IN)
print(pin.value())
```

Zmáčkni a drž tlačítko `FLASH` vedle USB konektoru.
Přitom pusť `print(pin.value())` znovu.
Jak se hodnota změní?

Jak tomuhle kódu rozumět?
Třída `Pin` ti umožňuje ovládat jednotlivé
„nožičky”, kterými zařízení komunikuje s vnějším
světem: buď na nich nastavovat napětí, nebo zkoumat
jestli na nich nějaké napětí je.

`Pin(0, Pin.IN)` vytvoří objekt třídy Pin,
který bude načítat data z „nožičky” číslo 0.
(`IN` znamená načítání – informace jdou *do* procesoru).
Funkce `pin.value()` změří napětí na dané
„nožičce” a vrátí buď 1 nebo 0 podle toho, jestli nějaké naměřila.

No a „nožička” číslo 0 je připojená k tlačítku `FLASH`,
kterým se tak dá ono napětí ovládat.
Informace o tom, která nožička je kam připojená,
máš na [taháku](https://pyvec.github.io/cheatsheets/micropython/nodemcu-cs.pdf) –
můžeš si zkontrolovat, že Pin(0) u sebe má poznámku FLASH.


## Obvod

Teď na chvíli necháme programování a postavíme si elektrický obvod.
Vezmi si modrou svítivou diodu (LED, „světýlko”) a
nepájivé pole („hloupou destičku”).
Zkusíme světýlko rozsvítit.

LED rozsvítíš tak, že ji připojíš ke *zdroji napětí*, například k baterce.

Jako zdroj napětí můžeme použít i náš modul.
Ten bere elektřinu přes USB a dává nám ji k dispozici
na některých svých „nožičkách”:
konkrétně plus na nožičce označené `3V`
a mínus na nožičce označené `G`.
Na tyhle nožičky musíš zapojit diodu.

Připojování diody má jeden háček:
musíš ji zapojit správným směrem – plus na plus, mínus na mínus.
Opačně dioda svítit nebude. Dobrá zpráva je, že
když diodu otočíš špatně, nic se jí nestane.

> [note]
> Základní vlastnost *diody* je ta, že pustí
> elektrický proud jen jedním směrem. Svítící dioda
> – *angl. Light Emitting Diode, LED* – ještě k
> tomu navíc svítí.

Je potřeba rozpoznat rozdíl mezi nožičkami diody.
*Katoda* (`-`) je ta kratší nožička.
Pouzdro diody je u katody trochu seříznuté
a vevnitř v pouzdře, když se pozorně podíváš, uvidíš
u katody větší plíšek.
Té druhé nožičce se říká anoda (`+`).

Tak, teď víš, kam diodu zapojit: katodu (kratší nožičku)
na `G` a anodu na `3V`.

Držení nožiček diody u nožiček modulu by ti nejspíš
zaměstnalo obě ruce. Aby sis je uvolnila, použij
*nepájivé pole* (angl. *breadboard*).
Je v něm spousta dírek, do kterých se dají strkat dráty.
V rámci každé poloviny destičky je každá řada dírek –
tedy každá pětice – spojená dohromady.
Když zapojíš drátky do stejné řady, spojíš je tím.

Zasuň modul do nepájivého pole. Pak připoj katodu
do dírky ve stejné řadě, kde je nožička
`3V` modulu, a podobně anodu k `G`.
Mělo by to vypadat jako na tomto obrázku:

{{ figure(
    img=static("circuits/led_bb.svg"),
    alt="diagram zapojení",
) }}

Potom zapoj USB kabel. Dioda by se měla rozsvítit!

Zkus si, co se stane, když obě nožičky diody zapojíš ke `G`.

{{ figure(
    img=static("circuits/led_bb_off.svg"),
    alt="diagram zapojení",
) }}

Aby dioda svítila, musí být připojená na dvě místa,
mezi kterými je takzvaný *potenciálový rozdíl* — napětí.
Na nožičce `G` je 0 voltů; na nožičce
`3V` jsou 3,3 volty – je tedy mezi nimi rozdíl 3,3 V, přesně tolik,
kolik modrá LED potřebuje ke svícení.

> [note]
> Samotná hodnota napětí nedává smysl – například
> říct, že je na jednom místě 3,3 V je nepřesné.
> Hodnota ve voltech se vždycky musí k něčemu vztahovat;
> vyjadřuje rozdíl mezi dvěma místy.
> V elektronice používáme rozdíl oproti „zemi” – napětí
> na nožičce `G`. Stanovíme si, že tam je
> 0 voltů a ostatní napětí počítáme vzhledem k ní.
> Na nožičce `3V` je tedy napětí 3,3 V vzhledem k zemi.


## Výstup

Proč jsme diodu na to, aby se rozsvítila,
připojili k modulu a ne jen k baterce?
Ten modul je trošku složitější zařízení než baterka a jedna důležitá věc,
kterou umí navíc, je nastavovat napětí na různých nožičkách.
Umí zařídit, aby se nožička chovala jednou jako `3V` a jindy jako `G`.
Když připojíš diodu mezi `G` a takovou
přepínatelnou nožičku, můžeš nastavit, kdy svítí a kdy ne.

Přepoj anodu diody z `3V3` na `D5`. Katodu nech na `G`.

Máš-li zapojeno, znovu se připoj k MicroPythonu a zadej následující kód:

```python
from machine import Pin
pin = Pin(14, Pin.OUT)
pin.value(0)
pin.value(1)
```

Když objekt Pin vytvoříš s `Pin.OUT`, MicroPython na něm bude nastavovat
napětí – buď 3,3 V (`value(1)`) nebo 0 V (`value(0)`).
A tak se dá s diodou blikat.

> [note]
> Číslování nožiček je bohužel dvojí – nožička
> označená jako `D5` má v procesoru přiřazené číslo 14.
> Třída `Pin` v MicroPythonu používá číslování procesoru.
> Naštěstí máš [tahák](https://pyvec.github.io/cheatsheets/micropython/nodemcu-cs.pdf),
> kde snadno dohledáš že `D5` a `Pin(14)` jsou dvě jména stejné nožičky.

Zvládneš napsat program, který zařídí, aby dioda
svítila pouze když je zmáčknuté tlačítko `FLASH` a jinak ne?

> [note]
> Nápověda: Můžeš pořád dokola zjišťovat stav tlačítka
> a nastavovat podle něj stav LED.

{% filter solution %}
```python
from machine import Pin
pin_diody = Pin(14, Pin.OUT)
pin_tlacitka = Pin(0, Pin.IN)
while True:
    pin_diody.value(1 - pin_tlacitka.value())
```
{% endfilter %}


## Pouštění kódu ze souboru

Jak začneš psát trochu složitější programy,
mohlo by se stát, že tě konzole MicroPythonu začne trochu štvát.
Špatně se v ní opravují chyby a automatické odsazování funguje jen většinou.
Pojďme se podívat, jak naštvání předejít.

Doporučuji si větší kousky kódu – a určitě takové,
ve kterých je nějaký cyklus, podmínka či funkce –
psát v textovém editoru a do modulu pak posílat celý soubor.

Zkus si to. Do souboru `blikajici_led.py` dej následující kód:

```python
from machine import Pin
from time import sleep
pin_diody = Pin(14, Pin.OUT)
while True:
    pin_diody.value(0)
    sleep(1/2)
    pin_diody.value(1)
    sleep(1/2)
```

Potom zavři konzoli (`picocom`, PuTTY nebo `screen`).

K pouštění programu použijeme `ampy`, který jsi nainstaloval{{a}} dříve.
Ke spuštění budeš potřebovat znát port:

* Linux: port používáš v příkazu `picocom`, např. `/dev/ttyUSB0`
* Windows: port používáš v PuTTY, např. `COM13`
* macOS: port používáš v příkazu `screen`, např. `/dev/tty.usbmodem*`

`ampy` spusť následujícím příkazem, jen za `PORT` doplň svůj port:

```console
(venv)$ ampy -p PORT run blikajici_led.py
```

Program by měl blikat diodou.
Využívá k tomu funkci `time.sleep()`, která počká daný počet vteřin –
tedy `time.sleep(1/2)` zastaví program na půl sekundy.


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

<!-- XXX: Solution? -->

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


## Tóny a melodie

Vezmi si další součástku – piezobudič, neboli „bzučítko”.

Tahle malá věc obsahuje speciální materiál, který se,
když ho připojíš ke zdroji napětí, trošku roztáhne.
Roztažením zatlačí na okolní vzduch a vytvoří tlakovou
vlnu, která může doputovat až k tvým uším.

Zkus si to – když bzučítko připojíš na `3V`
a `G` (tentokrát je jedno kterým směrem), uslyšíš tiché lupnutí.
A podobné lupnutí uslyšíš když součástku zase odpojíš.

Co se stane, když budeš napětí připojovat a odpojovat, řekněme, 32× za vteřinu?

Nebo 65×?

Nebo některou z těchto frekvencí?
Hz – [Hertz](https://en.wikipedia.org/wiki/Hertz) – je jednotka frekvence;
„49 Hz“ znamená „49× za sekundu“.

| Nota | Frekvence |
|:-----|----------:|
| C1   | 32,70 Hz  |
| D    | 36,71 Hz  |
| E    | 41,20 Hz  |
| F    | 43,65 Hz  |
| G    | 49,00 Hz  |
| A    | 55,00 Hz  |
| H    | 61,74 Hz  |
| C2   | 65,41 Hz  |

Naprogramuj písničku! Potřebuješ-li víc not, pusť si [program](static/noty.py),
který vypočítá další frekvence.


## Další ovládání

Teď si vezmi tlačítko a připoj ho k modulu:
`GND` vždycky na `G`, `VCC` vždycky na `3V` a
`OUT` na `D1`.

Tlačítko funguje tak, že `OUT` spojí buď s `VCC` (`3V`)
nebo `GND`, podle toho, jestli je tlačítko stisknuté.
(A navíc to taky teda svítí, ale to je teď vedlejší.)

Zkus si, jestli se zvládneš MicroPythonu zeptat, jestli je tlačítko zapnuté.
Mělo by to být podobné jako u příkladu s tlačítkem `FLASH`.

Zvládneš napsat program, který bude bzučet bzučítkem
a přitom se bude dát tlačítkem změnit tón?

Program si (na svém počítači) ulož, ať se k němu můžeš vrátit.

## Barevná světýlka

Je čas na novou hračku!
Tentokrát to bude LED pásek.

Na pásku máš 8 malých čtverečků.
Každý z nich obsahuje docela hodně elektroniky:
tři barevné LED (červenou, zelenou a modrou)
a čip, který je umí ovládat pomocí informací,
které dostane přes jediný drátek z modulu.

Takové pásky se prodávají po metrech a dají se
nastříhat – mezi jednotlivými světýlky si všimni čárky,
která naznačuje, kde máš střihnout.
Energie z USB stačí zhruba na osm světýlek, proto jsi jich dostal{{a}} tolik.

Tenhle LED pásek je stavěný na pět voltů. Naštěstí ale potřebuje 5 V jen
na <em>napájení</em>; řídící signál s informacemi o barvičkách může mít 3,3 V.

Pojďme pásek zapojit:

* `GND` pásku (bílý drátek) připoj na `G`
* `DI` (*data in* – zelený drátek) připoj na `D4`
* `+5V` (červený drátek) připoj:
  * na `VU`, má-li tvoje destička tuhle nožičku,
  * jinak na `VIN`.

Nožička `VU`/`VIN` poskytuje 5 voltů.
Pozor na ni: nepřipojuj na ni zařízení, které se s pěti volty nevyrovnají.

Máš-li zapojeno, můžeš začít programovat.
„Jazyk”, kterým „mluví” tenhle LED pásek je trošku
složitější než signál PWM, ale MicroPython obsahuje
speciální knihovnu, která s páskem komunikovat umí.
Vypadá to nějak takhle:


<pre>
from machine import Pin
from neopixel import NeoPixel

POCET_LED = 8
pin = Pin(2, Pin.OUT)
np = NeoPixel(pin, POCET_LED)
np<span class="highlight-nocolor">[0]</span> = (<span class="highlight-red">255</span>, <span class="highlight-green">255</span>, <span class="highlight-blue">255</span>)
np.write()
</pre>


Co znamenají ta čísla (`0` a `255`), na to už jistě přijdeš sám/sama.
Jen při experimentování nezapomeň zavolat
`np.write()`, tím se informace pošlou do LED pásku.

Zvládneš naprogramovat semafor?

## Teploměr

Poslední součástkou, kterou si dnes ukážeme, bude jednoduchý teploměr DS18B20.
Tento teploměr se vyrábí v několika provedeních a je velmi populární především
pro jednoduchost použití a velmi nízkou cenu.

Stejně jako si MicroPython pomocí speciálního „jazyka” rozumí s LED páskem, ovládá
i „jazyk” pro komunikaci s teploměrem a řadou dalších zařízení. 1-wire sběrnice
má navíc tu výhodu, že se na jednu nožičku naší destičky dá připojit hned
několik teploměrů a číst teploty z každého z nich.

Otoč teploměr tak, aby jeho „břicho” směřovalo směrem od tebe a takto jej zapoj
do nevyužité části nepájivého pole. Následně propoj nožičky teploměru
s destičkou takto:

* Levou nožičku propoj s `G`
* Prostřední nožičku propoj s `D2`
* Pravou nožičku propoj s `3V`

> [note]
> Po zapojení drž teploměr na chvíli mezi prsty. Pokud je zapojený špatně začne
> se velmi rychle zahřívat a v takovém případě jej okamžitě odpoj.

Pokud je vše zapojeno správně, můžeme přistoupit k měření teploty.

```python
from time import sleep
from machine import Pin
import onewire
from ds18x20 import DS18X20


pin = machine.Pin(4, Pin.IN)
ow = DS18X20(onewire.OneWire(pin))

sensory = ow.scan()
ow.convert_temp()
sleep(1)
teplota = ow.read_temp(sensory[0])
print("Teplota je", teplota)
```

Nejdříve si opět připravíme nožičku (pin) pro komunikaci a následně si na ní
připravíme komunikační protokol OneWire. Prvním krokem k teplotě je nalezení
všech dostupných teploměrů na dané sběrnici, což nám zajistí metoda `ow.scan()`,
která nám vrátí seznam identifikátorů nalezených teploměrů.
Metoda `ow.convert_temp()` pak pošle všem teploměrům příkaz, aby změřily
teplotu. Po tomhle rozkazu musíme alespoň vteřinu počkat a následně můžeme
teplotu z našeho čidla přečíst.

## WiFi

Jak jsme zmínili na začátku, byl čip ESP8266 primárně určen pro práci s WiFi
a tato schopnost mu zůstala. Umí se buď připojit k existující síti, nebo
ze sebe udělat hotspot a vytvořit si tak vlastní WiFi síť. Obě tyto možnosti
nám umožní spojit se s destičkou bezdrátově a pracovat s ní skrze
webový prohlížeč pomocí tzv. WebREPL, nebo použít připojení k síti k odesílání
dat z destičky pro další zpracování.

Používání WiFi je ovšem mimo možnosti tohoto workshopu. Vše potřebné k jejímu
zprovoznění je k dispozici [v této části dokumentace](https://docs.micropython.org/en/latest/esp8266/esp8266/tutorial/repl.html#webrepl-a-prompt-over-wifi).

## Kam dál

Fantazii se meze nekladou a možnosti jsou nepřeberné.
Velké množství informací naleznete v [dokumentaci](https://docs.micropython.org/en/latest/esp8266/).
