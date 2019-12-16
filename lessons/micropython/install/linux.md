# Instalace pro Linux

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

## Nenainstalovaný picocom

Nemáš-li příkaz `picocom` nainstalovaný,
je potřeba ho nainstalovat (např.
`sudo dnf install picocom` nebo
`sudo apt-get install picocom`).

## Neexistující soubor

Pokud `picocom` skončil s chybou
`No such file or directory`, pravděpodobně
je potřeba k zařízení přistupovat přes jiný soubor.
Použij příkaz `dmesg | tail`, který vypíše něco jako:

<pre>
$ dmesg | tail
[703169.886296] ch341 1-1.1:1.0: device disconnected
[703176.972781] usb 1-1.1: new full-speed USB device number 45 using ehci-pci
[703177.059448] usb 1-1.1: New USB device found, idVendor=1a86, idProduct=7523
[703177.059454] usb 1-1.1: New USB device strings: Mfr=0, Product=2, SerialNumber=0
[703177.059457] usb 1-1.1: Product: USB2.0-Serial
[703177.060474] ch341 1-1.1:1.0: ch341-uart converter detected
[703177.062781] usb 1-1.1: ch341-uart converter now attached to <strong>ttyUSB0</strong>
</pre>

Máš-li místo `ttyUSB0` něco jiného, v příkazu `picocom` to použij místo
`ttyUSB0`.

## Nedostatečné oprávnění

Pokud `picocom` skončil s chybou `Permission denied`, potřebuješ získat
přístup k souboru zařízení.
To znamená přidat se do příslušné skupiny.
Na spoustě systémů (Fedora, Ubuntu, Debian) bude fungovat:

```console
$ sudo usermod --append --group dialout $(whoami)
```

Kdyby si to stěžovalo že skupina neexistuje (např. na Arch Linux),
místo `dialout` použij `uucp`.

> [note] Co to dělá?
> `sudo` uvozuje administrační příkaz, který mění nastavení systému:
> v tomto případě chceš udělit oprávnění přistupovat k zařízením.
> `usermod` mění nastavení uživatelských účtů.
> `--append --group` říká, že chceš přidat uživatele do skupiny.
> `$(whoami)` doplní tvoje uživatelské jméno.

Po `usermod` je potřeba se znovu přihlásit, třeba příkazem:

```console
$ su - $(whoami)
```

> [note] Co to dělá?
> `su` umožňuje se přihlásit jako daný uživatel.
> `-` zařídí „plnohodnotné“ přihlášení – mimojiné se znovu načte seznam skupin.
> `$(whoami)` doplní tvoje uživatelské jméno: přihlašuješ se znovu jako ty
> {{gnd('sám', 'sama')}}.

Pro ověření spusť příkaz `groups`; v jeho výstupu by mělo být `dialout`
(příp. `uucp`).
Například:

```console
$ groups
kristyna lp wheel dialout mock
```

> [note] Co to dělá?
> Příkaz `groups` vypíše skupiny, do kterých tvůj uživatelský účet patří.
