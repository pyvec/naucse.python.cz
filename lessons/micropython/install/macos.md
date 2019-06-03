# Instalace pro macOS

V příkazové řádce zadej:

```console
$ screen /dev/tty.usbmodem* 115200
```

a stiskni Enter.
Pak na modulu zmáčkni `RST`.
Měly by se nakonec objevit tři zobáčky, `>>>`.

Nefunguje-li to, zadej

```console
$ ls /dev/tty.*
```

a vyber jméno zařízení které přísluší tvé destičce.
(Neboj se si nechat poradit od někoho zkušenějšího.)
Toto jméno použij místo `/dev/tty.usbmodem*` v příkazu `screen` výše.

Není-li jméno zařízení vidět, je možná potřeba nainstalovat ovladač pro
USB převodník CP2102.
Ten se dá stáhnout [ze stránek výrobce][cp2012-driver].

> [note]
> Odkaz je pro destičky s USB převodníkem CP2102.
> Některé levnější modely používají převodník CH340G.
> Který převodník máš se nejlíp dozvíš od toho, kdo ti destičku poskytl.
> Ovladač k CH340G se dá dostat
> [z tohoto blogu](https://iotta.cz/ovladace-pro-ch340g/).

[cp2012-driver]: https://www.silabs.com/products/development-tools/software/usb-to-uart-bridge-vcp-drivers
