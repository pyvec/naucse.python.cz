# Instalace Gnome Boxes

Gnome Boxes jsou pro Linux k dispozici normálním způsobem, kterým instaluješ
a spouštíš grafické („okýnkové“) programy.

Z příkazové řádky to jde takto:

* Fedora

  ```console
  $ sudo dnf install gnome-boxes
  ```

* Debian/Ubuntu

  ```console
  $ sudo apt-get install gnome-boxes
  ```

Program pustíš opět stejným způsobem jako grafické programy, případně
z řádky:

  ```console
  $ gnome-boxes
  ```

Spuštěný program by měl vypadat nějak takto:


  {{ figure(
    img=static('boxes-01.png'),
    alt='Gnome Boxes',
  ) }}

## Vytvoření virtuálního počítače

V levém horním rohu je tlačítko **+**.
Klikni na něj a vyber *Vytvořit virtuální stroj* (*Create a Virtual Machine*).

V následujícím okně ignoruj nabídku systémů a zvol *Vybrat soubor*:

  {{ figure(
    img=static('boxes-02.png'),
    alt='Gnome Boxes – vytvořit box',
  ) }}

Vyber ISO soubor se systémem, který jsi před chvílí stáhl{{a}}.
V dalším kroku je možnost virtuální poc'itač přizpůsobiut, což není nutné.
Zvol *Vytvořit*:

  {{ figure(
    img=static('boxes-03.png'),
    alt='Gnome Boxes – přehled',
  ) }}

Tím je virtuální počítač vytvořen!
Pokračuj [instalací systému]({{ subpage_url('index#install-system') }}).
