# Instalace pro Windows


## Instalace ovladače a číslo COM portu

> [note]
> Tento návod je pro destičky s USB převodníkem CP2102.
> Některé levnější modely používají převodník CH340G.
> Který převodník máš se nejlíp dozvíš od toho, kdo ti destičku poskytl.
> Ovladač k CH340G se dá dostat
> [z tohoto blogu](https://iotta.cz/ovladace-pro-ch340g/).

Po připojení destičky se Windows nejspíš pokusí nainstalovat ovladač.
To je dobře.
Kdyby instalace potřebovala vybrat soubor, ovladač stáhni [ze stránek výrobce][cp2012-driver], rozbal a vyber.

Ze systémového menu (klávesa Windows) otevři *správce zařízení*
(Device Manager).
Pod *Ostatní zařízení* (Other Devices) nebo *Ports (COM & LPT)*
najdi položku obsahující *CP2102* nebo *CP210x*.

Je-li u položky ikonka varování ⚠, stáhni ovladač [ze stránek výrobce][cp2012-driver],
pak klikni na položku pravým tlačítkem, vyber aktualizaci ovladače a použij
dříve stažený ovladač.

Jestli ikonka ⚠ chybí (nebo zmizela), na konci jména položky by mělo
být číslo COM portu – například `(COM13)`. Číslo si zapamatuj.


## Instalace a nastavení PuTTY

Pak si nainstaluj program
[PuTTY](http://www.chiark.greenend.org.uk/~sgtatham/putty/download.html)
(`putty.exe`) a spusť ho.
V konfiguračním okýnku zaškrtni *Connection Type: Serial* a
do *Serial line:* zadej svůj COM port.
Pak přepni v seznamu vlevo na *Serial* (úplně dole) a nastav *Speed* na *115200*
a *Flow Control* na *None*:

{{ figure(
    img=static("putty-config.jpg"),
    alt='Obrázek nastavení PuTTY',
) }}

Potom zpátky v kategorii *Session* můžeš nastavení uložit pro příště:
do políčka *Saved Sessions* zadej *MicroPython* a klikni *Save*.

Nakonec klikni *Open*. Mělo by se otevřít
okýnko podobné konzoli, kde se, když zmáčkneš
na modulu `RST`, objeví nakonec tři zobáčky: `>>>`.

[cp2012-driver]: https://www.silabs.com/products/development-tools/software/usb-to-uart-bridge-vcp-drivers
