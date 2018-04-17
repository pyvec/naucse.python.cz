# Pokyny pro organizátory

Tento motivační wokshop s MicroPythonem potřebuje speciální hardware.
Tady je popsáno, jak jsme všechno připravili.


## Nákupní seznam

NodeMCU Devkit v2
:   Dá se koupit z Číny, např.
    z [Aliexpressu](https://www.aliexpress.com/wholesale?SearchText=nodemcu+v2+esp8266+ch340).

Malé nepájivé pole (Mini Breadboard)
:   Dá se koupit z Číny, např.
    z [Aliexpressu](https://www.aliexpress.com/wholesale?SearchText=mini+breadboard+170).

Modul s tlačítkem
:   Dá se koupit z Číny, např.
    z [Aliexpressu](https://www.aliexpress.com/wholesale?SearchText=impact+switch+module+dupont).

Modrá LED (<var>U<sub>f</sub></var>=3,3V)
:   Dá se koupit z Číny, nebo např.
    v [GME](https://www.gme.cz/led-kulate-pouzdro?tech_par[103][]=18997&showFilter=103).

Pásek s 8 LED moduly WS2812 s konektorem
:   Dá se koupit po metrech z Číny, např.
    v [Aliexpressu](https://www.aliexpress.com/wholesale?SearchText=ws2812+strip),
    rozstříhat, a napájet na konektory – opět např.
    z [Aliexpressu](https://www.aliexpress.com/wholesale?SearchText=3+pin+WS2812+connector).

Malý servomotor, např. TowerPro SG92R
:    Dá se koupit z Číny, např.
    v [Aliexpressu](https://www.aliexpress.com/wholesale?SearchText=sg92r).

Spojovací drátky
:   Opět se dají koupit z Číny, např.
    v [Aliexpressu](https://www.aliexpress.com/wholesale?SearchText=dupont+jumper+cable+m-m).
    <br>
    Jsou potřeba takové, aby se jimi dal připojit LED pásek a motorek
    k nepájivému poli.

MicroUSB kabel
:   Jak pro mobil. Doporučuji koupit kvalitní datový kabel.
    Případně si můžou účastníci donést vlastní, je ale dobré jich mít pár
    v zásobě, kdyby si přinesli nedatový kabel od nabíječky.

Počítač
:   Je potřeba i „velký“ počítač – hlavně kvůli obrazovce a klávesnici.
    Viz nastavení níže.


## Příprava hardwaru

NodeMCU zasuň do nepájivého pole, aby na každé delší straně zbyla řada dírek.
Do nich zapoj komponenty:

| Pin | – Součástka                   |
| --: | :---------------------------- |
|  D1 | – Anoda LED (delší nožička)   |
|  D2 | – Katoda LED (kratší nožička) |
| 3V3 | – `VCC` tlačítka              |
| GND | – `GND` tlačítka              |
|  D5 | – `OUT` tlačítka              |
|  D6 | – `DI` LED pásku              |
|  D8 | – `Data` servomotoru          |
| GND | – `GND` servomotoru           |
| 3V3 | – `VCC` servomotoru           |
| GND | – `GND` LED pásku             |
| Vin | – `+5V` LED pásku             |

Nejsou-li vstupy servomotorku označené, bývá červený VCC, hnědý GND,
zbylý Data.

{{ figure(
    img=static('module_full.jpg'),
    alt='Fotografie modulu s veškerým příslušenstvím',
) }}

{{ figure(
    img=static('module_detail.jpg'),
    alt='Detailní záběr na osazené nepájivé pole',
) }}

## Příprava počítače

Na workshop doporučujeme použít počítače s [Fedorou][Fedora] Workstation 25.
Pár věcí je potřeba nastavit:

* Uživatel musí být členem skupiny `dialout`:

  ```console
  $ sudo usermod -a -G dialout $(whoami)
  $ su - $(whoami)
  ```

  (Po tomto nastavení je potřeba se přihlásit a znovu odhlásit,
  případně v každém terminálu zadat `su - $(whoami)`.)

* Musí být nainstalované balíčky `picocom` a `ampy`:

  ```console
  $ sudo dnf install picocom ampy
  ```

  (Na jiných systémech nemusí být `ampy` v systémových repozitářích.
  V takovém případě se dá nainstalovat pomocí
  `python3 -m pip install --user adafruit-ampy`.)

* Aplikace Terminal (`gnome-terminal`) a Textový editor (`gedit`)
  jsme dali do oblíbených položek v GNOME.
  (Klávesa Super – na klávesnici napsat Terminal – přetáhnout ikonku do levého
  proužku. Zopakovat pro Gedit.)

* Textový editor jsme nastavili pro Python: odsazování čtyřmi mezerami,
  ukazování čísel řádků.
  Podrobněji viz náš [návod pro začátečníky][gedit-setup].

* Nastavili jsme možnost výběru české/anglické klávesnice.
  (Ikonka v pravém horním rohu obrazovky – ikonka s klíčem a šroubovákem –
  Regional Settings)


## Firmware

K flashování je potřeba stáhnout
binární obraz [MicroPythonu pro ESP8266][micropython] a
náš předpřipravený začátečnický soubor [boot.py].

Potřebné nástroje, [esptool] a [ampy], můžeme na Fedoře nainstalovat z balíčků:

```console
$ sudo dnf install esptool ampy
```

> [note]
>
> Na systémech, kde tyto nástroje v systémových balíčcích nejsou,
> se dají nainstalovat do virtuálního prostředí:
>
> ```console
> $ python3 -m venv venv
> $ . venv/bin/activate
> (venv)$ python -m pip install esptool adafruit-ampy
> ```

Připojíme NodeMCU přes USB a pomocí `esptool` ho naflashujeme:

```console
(venv)$ esptool.py --port /dev/ttyUSB0 erase_flash
(venv)$ esptool.py --port /dev/ttyUSB0 --baud 460800 write_flash 0 esp8266-20161110-v1.8.6.bin
```

(Kdyby neexistovalo zařízení `/dev/ttyUSB0`, ve výstupu `dmesg | tail` se dá
dohledat, kam se NodeMCU připojilo. V takovém případě ale bude potřeba změnit
instrukce k workshopu.)

Nakonec na NodeMCU stiskneme tlačítko RST, pustíme a pak nahrajeme `boot.py`:

```console
(venv)$ ampy -p /dev/ttyUSB0 put boot.py
```

Soubor `boot.py` obsahuje testovací režim pro kontrolu, že je vše nahráno
správně.
Podržíme-li tlačítko na modulu stisknuté, po resetu (tlačítkem RST nebo
přpojením USB kabelu) se motorek otočí a modrá LED i LED pásek zablikají.


[Fedora]: https://getfedora.org/
[gedit-setup]: {{ lesson_url('beginners/install-editor', page='gedit') }}
[micropython]: https://micropython.org/download#esp8266
[boot.py]: static/boot.py
[esptool]: https://github.com/espressif/esptool
[ampy]: https://github.com/adafruit/ampy
