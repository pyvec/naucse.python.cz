# MicroPython na malém zařízení

> [note] Tahle sekce bohužel nejde jednoduše projít z domu.
> Využíváme speciální vybavení, které je potřeba nejdřív
> sehnat. Máš-li možnost se dostat na sraz, nebo
> aspoň kontaktovat organizátory, doporučujeme shánět
> spíš tímto způsobem.
> Případně jde případný hardware objednat přes Internet,
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
tak malé, že ho pohodlně schováš v ruce.
Konkrétně budeme používat „chytrou destičku”, modul zvaný
*NodeMCU Devkit*, která by měla ležet před tebou.
Než ji vyndáš z obalu, měla by ses *vybít*:
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
<span class="part-red">μUSB konektor</span>,
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

  {# XXX: ttyUSB0 should be highlighted #}
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
[z tohoto blogu](http://kig.re/2014/12/31/how-to-use-arduino-nano-mini-pro-with-CH340G-on-mac-osx-yosemite.html),
případně z [materiálů pro Arduino workshop](https://onedrive.live.com/?authkey=%21AKLO1lLajaeTmo4&id=182EF9BC3A8BDDA4%2166743&cid=182EF9BC3A8BDDA4).

Pak si nainstaluj si program
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
z [tohoto blogu](https://tzapu.com/ch340-ch341-serial-adapters-macos-sierra/).


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
svítila když je zmáčknuté tlačítko `FLASH`, jinak ne?

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

Zkus si to. Do souboru `led_podle_tlacitka.py` dej následující kód:

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
(venv)$ ampy -p PORT run led_podle_tlacitka.py
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
from time import sleep

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

Teď si vezmi dvě tlačítka a připoj je k modulu:
`GND` vždycky na `G`, `VCC` vždycky na `3V` a
`OUT` u jednoho tlačítka na `D1` a u druhého na `D2`.

Tlačítko funguje tak, že OUT spojí buď s VCC (5V)
nebo GND, podle toho, jestli je tlačítko stisknuté.
(A navíc to taky teda svítí, ale to je teď vedlejší.)

Zkus si, jestli se zvládneš MicroPythonu zeptat, jestli je tlačítko zapnuté.
Mělo by to být podobné jako u příkladu s tlačítkem FLASH.

Zvládneš napsat program, který bude bzučet bzučítkem
a přitom se jedním tlačítkem bude dát zvyšovat tón a druhým snižovat?

Program si (na svém počítači) ulož, ať se k němu můžeš vrátit.


## Rotace

Čas na další součástku! Tentokrát to bude *servomotor*.

Servomotor je součástka, která má v sobě zabudovaný
ovladač, se kterým si naše zařízení může povídat
jednoduchým „elektronickým jazykem” – *protokolem*.
Motorku můžeš posílat impulzy a podle délky impulzu
se servomotor natočí.
Při krátkých impulzech se natočí víc na jednu stranu,
při dlouhých na druhou.
Impulzy musíš posílat neustále, jinak se servomotor
vypne.

Na rozdíl od bzučítka, kde o výšce tónu rozhodovala
frekvence (`freq`) – kolikrát za vteřinu
se ozve lupnutí – a LED, kde o intenzitě rozhodovala
střída (`duty`) – poměr mezi dobou kdy
dioda svítí a kdy nesvítí, u servomotoru rozhoduje
tzv. *šířka pulzu*: jak dlouho se napětí udrží
na 3,3 V, než se přepne zpátky na 0 V.
<!-- XXX: Actual typical pulse widths -->


V praxi to znamená, že můžeš nastavit `freq`
na 50 Hz, a `duty` měnit cca od 35
(úplně vlevo) přes 77 (uprostřed) po 120 (úplně vpravo).

Dost ale teorie, pojďme si to vyzkoušet! Napřed musíš motorek zapojit:

* hnědý drát (zem) na `G`,
* červený drát (napájení) na `3V` a
* oranžový drát (data) na `D4`.

Nožička `D4` odpovídá `Pin(2)`, takže kód k otáčení motorku je:

```python
from machine import Pin, PWM
from time import sleep

pin_motorku = Pin(2, Pin.OUT)
pwm = PWM(pin_motorku, freq=50, duty=77)
pwm.duty(35)
```

Zkus motorkem otáčet nastavováním `duty` na 35 do 120.
Kdyby se náhodou stalo, že se modul restartuje a
konzole přestane fungovat, zkus ho odpojit a znovu
připojit. Kdyby to nepomohlo, motorek ti dneska
nebude fungovat. Za chvíli si řekneme proč; zatím (jsi-li na kurzu)
se přidej do dvojice k někomu, komu to funguje.


## Poznámka o napájení a napětí

K tomu, aby se otočil motor, je potřeba mnohem víc
energie, než k rozsvícení světýlka.
Z USB z počítače té energie dostaneš docela málo,
proto můžou být s motorkem problémy.

Jak to řešit, až si přestaneš hrát a budeš chtít motorkem otáčet „doopravdy”?

Elektronika, která je na našem modulu mimo
malou destičku s „mozkem” má dva hlavní úkoly:

* Převádět *komunikaci* z USB, která je
  celkem složitě zakódovaná, na něco čemu
  malé zařízení rozumí
  (konkrétně protokol [UART](https://en.wikipedia.org/wiki/UART) přes nožičky `TX` a `RX`).
* Převádět napětí 5 V, které poskytuje USB,
  na 3,3 V které potřebuje modul.

Když energie z USB přestane stačit, dá se koupit
zařízení, které zvládne převádět komunikaci
a napájení vyřešit z jiného zdroje 5 V.
Kdybys to někdy zkoušela, příslušné zařízení
koupíš pod názvem *USB-TTL adapter* a vypadá
nejčastěji takhle:

{{ figure(
    img=static("usb-ttl.png"),
    alt="USB-TTL adapter",
) }}

K modulu pak tento převodník a zdroj napětí připojíš takto:

<!-- XXX: obrázek -->
* `GND` na převodníku – `G` na desce
* `RX` na převodníku – `TX` (!) na desce
* `TX` na převodníku – `RX` (!) na desce
* `+5V` na zdroji napětí na `VIN` na desce
* Zem na zdroji napětí na `G` na desce

Pozor, 5V nepřipojuj jinam než na `VIN`!


## Napětí
Další důvod, proč ti servomotor někdy nefunguje dobře,
je to, že je stavěný na 5 voltů, ne na 3,3 které
poskytuje modul.

Když připojíš zařízení k menšímu napětí, než
potřebuje, většinou buď nebude fungovat, nebo bude
dělat „míň” než by mělo: LED bude míň svítit,
reproduktor bude tišší, motorek se bude točit pomaleji nebo s menší silou.

Když naopak připojíš zařízení k *většímu* napětí,
než na jaké je stavěno, nejspíš ho nadobro zničíš.
Když připojíš červenou LED přímo na 3,3 V, přestane fungovat;
když připojíš malý servomotorek na zdroj 24 V, může začít hořet.
A ačkoli lidem malá napětí jako 5 V nevadí,
když připojíš do zásuvky s 230 V {{ gnd('sám', 'sama') }} sebe, můžeš umřít.
Takže na velká napětí pozor!

My motorek připojujeme na malé napětí a zmenšený
výkon nám příliš nevadí – dokud se to
otáčí, víc rychlosti ani síly nepotřebujeme.

Až to ale potřebovat budeš – například až budeš
servomotorkem pohánět ruku robota, která bude zvedat
těžké náklady, budeš potřebovat dvě věci:

* Externí napájení – jako předtím bude motorek potřebovat zvláštní zdroj 5V.
* Na datový signál je potřeba použít *převodník úrovní*
  (angl. *logic level converter*),
  který převede třívoltový signál na pětivoltový.

Kdybys to někdy potřebovala, ozvi se koučům – i po
workshopu ti určitě rádi poradí nebo ti aspoň řeknou
koho se zeptat!

{#
## Ukládání souboru

XXX: Tahle kapitola ještě bohužel není dopsaná.
#}

## Barevná světýlka

Tak, dost teorie; vezmi si novou hračku!
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

Tenhle LED pásek je, podobně jako servomotorek, stavěný
na pět voltů. Na rozdíl od motorku, který se s 3,3 V
trochu roztočil, se ale s nižším napětím ani nerozsvítí.
Naštěstí ale potřebuje 5 V jen na <em>napájení</em>;
řídící signál s informacemi o barvičkách může mít 3,3 V.

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


Co znamenají ta čísla (`0` a `255`), na to už jistě přijdeš sama.
Jen při experimentování nezapomeň zavolat
`np.write()`, tím se informace pošlou do LED pásku.

Zvládneš naprogramovat semafor?


{#
## Wi-fi
(XXX)

## Kam dál?
(XXX)
#}
