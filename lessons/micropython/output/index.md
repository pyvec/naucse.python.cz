## Obvod

Teď na chvíli necháme programování a postavíme si elektrický obvod.
Vezmi si modrou svítivou diodu (LED) a nepájivé pole.
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
> Základní vlastnost **diody** je ta, že pustí
> elektrický proud jen jedním směrem. **Svítící** dioda
> (angl. *Light Emitting Diode, LED*; českou hantýrkou „LEDka“) ještě k tomu
> navíc svítí.

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

Zkus si, co se stane, když diodu zapojíš naopak.

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
