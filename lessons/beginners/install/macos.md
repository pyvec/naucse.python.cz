# Instalace Pythonu pro Mac OS

Nainstaluj si nástroj [Homebrew](http://brew.sh), který řeší a zjednodušuje
instalaci aplikací a knihoven, které budeme potřebovat pro programování.
Jak na to?

Spusť v [příkazové řádce]({{ lesson_url('beginners/cmdline') }}) příkaz:

```console
$ /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
```

Pak stačí zadat následující příkaz, a Python bude nainstalovaný:

```console
$ brew install python3
```

## Vytvoření virtuálního prostředí

<!-- Pozn. Tahle sekce je velice podobná pro Linux, Mac i Windows;
     měníš-li ji, koukni se jestli není změna potřeba i jinde. -->

Nakonec vytvoř virtuální prostředí.

{%- if var('pyladies') -%}
{% set rootname = 'pyladies' %}
{%- else -%}
{% set rootname = 'naucse-python' %}
{%- endif -%}

Zvol si adresář (složku), ve které budeš mít soubory k PyLadies.
Může to být třeba <code>/home/<i>jméno</i>/{{ rootname }}</code>,
neboli <code class="pythondir">~/{{ rootname }}</code>.
Vytvoř ho a poznamenej si, kde je.

Vytváříš-li adresář jinde, nebo s jiným názvem, tak kdykoli ve zbytku
materiálů uvidíš <code class="pythondir">~/{{ rootname }}</code>, doplň
místo toho „svůj“ adresář.

Zvolený adresář po vytvoření nesmíš přesouvat jinam – když to uděláš,
přestane virtuální prostředí fungovat.
Proto ho nedoporučuji vytářet na Ploše.

!!! note ""
    Kdybys někdy chtěl{{a}} adresář přece jen přesunout,
    musel{{a}} bys smazat virtuální prostředí a vytvořit nové.

Teď když je tenhle adresář vytvořený, otevři příkazovou řádku
a příkazem `cd` se do něj přepni:
<!-- XXX: Special highlight in source code needed -->
```console
$ cd ~/{{ rootname }}
```

Pak virtuální prostředí vytvoř:

```console
$ python3 -m venv venv
```

Tím se ti vytvořil adresář <code><span class="pythondir">~/{{ rootname }}</span>/venv</code>,
ve kterém jsou soubory s virtuálním prostředím.
Můžeš se podívat dovnitř, ale nikdy tam nic neměň.


## Aktivace virtuálního prostředí

Nakonec virtuální prostředí aktivuj:

<div class="codehilite">
<pre><code><span class="gp">$</span> source <span class="pythondir">~/{{ rootname }}</span>/venv/bin/activate
</code></pre>
</div>

Po spuštění tohoto příkazu by se mělo na začátku příkazové řádky
(před `$`) objevit slovo `(venv)`.
Tak poznáš, že je virtuální prostředí *aktivní*.

Tenhle příkaz si zapiš. Budeš ho muset zadat vždycky když pustíš příkazovou řádku,
než se pustíš do programování.

{% if var('pyladies') %}
Máš-li vytištěné <a href="http://pyladies.cz/v1/s001-install/handout/handout.pdf">domácí projekty</a>,
příkaz si poznač, ať ho do příště nezapomeneš :)
{% endif %}

Pusťme se tedy do programování!
To už bude stejné pro tebe i pro lidi na Linuxu a Windows.
Sejdeme se na [další stránce]({{ subpage_url('first-steps') }}).
