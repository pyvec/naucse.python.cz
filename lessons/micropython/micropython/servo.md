## Servomotor

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
