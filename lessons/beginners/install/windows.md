# Instalace Pythonu pro Windows

Běž na [stahovací stránku Pythonu](https://www.python.org/downloads/)
a stáhni si instalátor nejnovější stabilní verze Pythonu. Od verze 3.6.0 má Python ve Windows jistá
vylepšení, která se nám budou hodit, a proto stahuj jen verzi **3.6.0 nebo novější**.

Jak poznat, který instalátor je ten pravý?
Pokud má tvůj počítač 64bitovou verzi Windows, stáhni si *Windows x86-64 executable installer*.
Pokud máš starší počítač s 32bitovými Windows, stáhni si *Windows x86 executable installer*.

{.note}
Kde zjistíš, zda máš 32bitové nebo 64bitové Windows? Stačí otevřít nabídku
**Start**, vyhledat „systém“ a otevřít **Systémové informace**.
Pokud máš novější počítač, téměř jistě budeš mít 64bitový systém.

![Screenshot zjišťování verze systému](windows_32v64-bit.png)

Pak instalátor spusť
Na začátku instalace zaškrtni **Install launcher for all Users**
a také **Add Python 3.6 to PATH**,
a dále se drž instrukcí.
(Tyto volby ti zjednoduší vytvoření virtuálního prostředí.)

![Screenshot instalace Pythonu](windows_add_python_to_path.png)


## Vytvoření virtuálního prostředí

<!-- Pozn. Tahle sekce je velice podobná pro Linux, Mac i Windows;
     měníš-li ji, koukni se jestli není změna potřeba i jinde. -->

Až bude Python nainstalovaný, vytvoř virtuální prostředí.

{%- if var('pyladies') -%}
{% set rootname = 'pyladies' %}
{%- else -%}
{% set rootname = 'naucse-python' %}
{%- endif -%}

Zvol si adresář (složku), ve které budeš mít soubory k PyLadies.
Může to být třeba `C:\{{ rootname }}`.

Zvolený adresář po vytvoření nesmíš přesouvat jinam – když to uděláš,
přestane virtuální prostředí fungovat.
Proto ho nedoporučuji vytářet na Ploše.

Ve zbytku materiálů budeme tento adresář nazývat <code class="pythondir">~/{{ rootname }}</code>,
i když se u tebe pravděpodobně jmenuje jinak.
Takže kdykoli odteď uvidíš <code class="pythondir">~/{{ rootname }}</code>,
doplň místo toho „svůj“ adresář.

{% filter md_note %}
Kdybys někdy chtěl{{a}} adresář přece jen přesunout,
musel{{a}} bys virtuální prostředí smazat a vytvořit nové.
{% endfilter %}

Teď když je tenhle adresář vytvořený, otevři [příkazovou řádku]({{ lesson_url('beginners/cmdline') }})
a příkazem `cd` se do něj přepni.
Pak vytvoř virtuální prostředí:

```shell
> python3 -m venv venv
```

Tím se nám vytvořil adresář <code><span class="pythondir">~/{{ rootname }}</span>\venv</code>,
ve kterém jsou soubory s virtuálním prostředím.
Můžeš se podívat dovnitř, ale nikdy tam nic neměň.

Tím máš Python a virtuální prostředí nainstalované!

## Aktivace virtuálního prostředí

Nakonec virtuální prostředí aktivuj:

<pre><code>&gt; <span class="pythondir">~/{{ rootname }}</span>\venv\Scripts\activate
</code></pre>

Po spuštění tohoto příkazu by se mělo na začátku příkazové řádky
(před `>`) objevit slovo `(venv)`.
Tak poznáš, že je virtuální prostředí *aktivní*.

Tenhle příkaz si zapiš. Budeš ho muset zadat vždycky když pustíš příkazovou řádku,
než se pustíš do programování.

{% if var('pyladies') %}
Máš-li vytištěné <a href="http://pyladies.cz/v1/s001-install/handout/handout.pdf">domácí projekty</a>,
příkaz si poznač, ať ho do příště nezapomeneš :)
{% endif %}

Pusťme se tedy do programování!
To už bude stejné pro tebe i pro lidi na Linuxu a Macu.
Sejdeme se na [další stránce]({{ subpage_url('first-steps') }}).
