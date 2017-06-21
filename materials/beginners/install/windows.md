# Instalace Pythonu pro Windows

Běž na [stahovací stránku Pythonu](https://www.python.org/downloads/)
a stáhni si instalátor nejnovější stabilní verze Pythonu. Od verze 3.6.0 má Python ve Windows jistá
vylepšení, která se nám budou hodit, a proto stahuj jen verzi **3.6.0 nebo novější**.

Jak poznat, který instalátor je ten pravý?
Pokud má tvůj počítač 64bitovou verzi Windows, stáhni si *Windows x86-64 executable installer*.
Pokud máš starší počítač s 32bitovými Windows, stáhni si *Windows x86 executable installer*.

> [note]
> Kde zjistíš, zda máš 32bitové nebo 64bitové Windows? Stačí otevřít nabídku
> **Start**, vyhledat „Systém“ a otevřít **Systémové informace**.
> Pokud máš novější počítač, téměř jistě budeš mít 64bitový systém.
>
> {{ figure(
    img=static('windows_32v64-bit.png'),
    alt='Screenshot zjišťování verze systému',
) }}

Pak instalátor spusť.
Na začátku instalace zaškrtni **Install launcher for all Users**
a také **Add Python 3.6 to PATH**.
Tyto volby ti zjednoduší vytvoření virtuálního prostředí.

(Jestli nemáš administrátorské oprávnění, volbu
*Install launcher for all Users* nezaškrtávej.)

{{ figure(
    img=static('windows_add_python_to_path.png'),
    alt='Screenshot instalace Pythonu',
) }}

Pak zmáčkni **Install now** a dále se drž instrukcí.

Máš-li otevřenou příkazovou řádku, po instalaci Pythonu ji zavři a otevři
novou.
Instalace mění systémové nastavení, které se musí načíst znovu.


## Vytvoření virtuálního prostředí

<!-- Pozn. Tahle sekce je velice podobná pro Linux, Mac i Windows;
     měníš-li ji, koukni se jestli není změna potřeba i jinde. -->

{%- if var('pyladies') -%}
{% set rootname = 'pyladies' %}
{%- else -%}
{% set rootname = 'naucse-python' %}
{%- endif -%}

Až bude Python nainstalovaný, vytvoř virtuální prostředí.

Zvol si adresář (složku), ve které budeš mít soubory k PyLadies.
Může to být třeba `C:\{{ rootname }}`.

Zvolený adresář po vytvoření nesmíš přesouvat jinam – když to uděláš,
přestane virtuální prostředí fungovat.
Proto ho nedoporučuji vytářet na Ploše.

> [note]
> Kdybys někdy chtěl{{a}} adresář přece jen přesunout,
> musel{{a}} bys smazat virtuální prostředí a vytvořit nové.

Ve zbytku materiálů budeme tento adresář nazývat <code class="pythondir">~/{{ rootname }}</code>,
i když se u tebe pravděpodobně jmenuje jinak.
Takže kdykoli od teď uvidíš <code class="pythondir">~/{{ rootname }}</code>,
doplň místo toho „svůj“ adresář.

Teď když je tenhle adresář vytvořený, otevři [příkazovou řádku]({{ lesson_url('beginners/cmdline') }})
a příkazem `cd` se do něj přepni.
Pak vytvoř virtuální prostředí:

```console
> py -3 -m venv venv
```

Tím se nám vytvořil adresář <code><span class="pythondir">~/{{ rootname }}</span>\venv</code>,
ve kterém jsou soubory s virtuálním prostředím.
Můžeš se podívat dovnitř, ale nikdy tam nic neměň.


## Aktivace virtuálního prostředí

Nakonec virtuální prostředí aktivuj:

<div class="highlight">
<pre><code><span class="gp">&gt;</span> <span class="pythondir">~/{{ rootname }}</span>\venv\Scripts\activate
</code></pre></div>

> [note]
> Nezapomeň místo <span class="pythondir">~/{{ rootname }}</span> zadat
> „svůj“ adresář!

Po spuštění tohoto příkazu by se mělo na začátku příkazové řádky
(před `>`) objevit slovo `(venv)`.
Tak poznáš, že je virtuální prostředí *aktivní*.

Tenhle příkaz si zapiš. Budeš ho muset zadat vždycky, když pustíš příkazovou řádku,
než se pustíš do programování.
{% if var('pyladies') -%}
Máš-li vytištěné <a href="http://pyladies.cz/v1/s001-install/handout/handout.pdf">domácí projekty</a>,
můžeš si ho poznačit tam :)
{%- endif %}

Zkusme teď nainstalovaný Python použít!
To už bude stejné pro tebe i pro lidi na Linuxu a Macu.
Sejdeme se na [další stránce]({{ lesson_url('beginners/first-steps') }}), kde uděláme první krůčky s Pythonem.
