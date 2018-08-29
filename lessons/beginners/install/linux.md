# Instalace Pythonu na Linux

Nainstalovat Pyhon na Linux je většinou jednoduché.
Jen existuje spousta druhů Linuxu a máme s ním největší zkušenosti,
tak jsou tyhle instrukce trochu delší.
Nezalekni se – většinu sekcí pravděpodobně přeskočíš. :)

## Instalace Pythonu 3

Na Linuxu většinou Python 3 už bývá. Abys to zkontroloval{{a}}, spusť
v [příkazové řádce]({{ lesson_url('beginners/cmdline') }}) příkaz:

```console
$ python3 --version
```

Objeví-li se „Python“ a číslo verze (např. `Python 3.6.6`)
a verze je 3.6 nebo vyšší, máš nainstalováno.
Přejdi na další sekci, [kontrolu `tkinter`](#check-tkinter).

Objeví-li se „Python“ a verze 3.5 nebo nižší,
{% if var('coach-present') -%}
poraď se s koučem.
{%- else -%}
aktualizuj systém (nebo se poraď s někým, kdo to umí) a zkus to znovu.
{%- endif %}

Objeví-li se `bash: python3: command not found` nebo podobná chyba,
doinstaluj Python.
Konkrétní příkaz záleží na distribuci:

* Fedora:
  {% filter markdown(inline=True) %}
  ```console
  $ sudo dnf install python3
  ```
  {% endfilter %}
* Ubuntu:
  {% filter markdown(inline=True) %}
  ```console
  $ sudo apt-get install python3
  ```
  {% endfilter %}

Používáš-li jinou distribuci, předpokládám, že instalovat programy už umíš. :)


{{ anchor('check-tkinter') }}
## Kontrola Tkinter

Některé linuxové distribuce obsahují standardně jen část celkové funkčnosti
Pythonu.
Konkrétně knihovnu `tkinter` (která umožňuje např. kreslit „želví obrázky“)
často musíme nainstalovat zvlášť.
Abys zjistil{{a}}, jestli je už je nainstalovaná, zadej příkaz:

```console
$ python3 -m tkinter
```

Objeví-li se okýnko, je všechno v pořádku.
Zavři ho a přejdi na [doinstalování `virtualenv`](#install-virtualenv).

Jestli ne, modul `tkinter` ještě nainstaluj:

* Fedora:
  {% filter markdown(inline=True) %}
  ```console
  $ sudo dnf install python3-tkinter
  ```
  {% endfilter %}
* **Ubuntu**:
  {% filter markdown(inline=True) %}
  ```console
  $ sudo apt-get install python3-tk
  ```
  {% endfilter %}

Používáš-li jinou distribuci, musíš si správné jméno balíčku najít na Internetu.

{{ anchor('install-virtualenv') }}
## Doinstalování Virtualenv

Novější verze Pythonu mají zabudovaný nástroj `venv`, který použijeme níže.
Starší verze ho ale nemají (a některé distribuce Linuxu ho dokonce z Pythonu
vyřadily).
Potřebuješ proto zjistit, jestli `venv` máš, a případně nainstalovat alternativu.

Spusť v příkazové řádce příkaz:

```console
$ python3 -m ensurepip --version
```

Objeví-li se výpis začínající „pip“, máš funkční `venv` nainstalovaný.
Přejdi na sekci [vytvoření virtuálního prostředí](#setup-venv).

Objeví-li se nápis `No module named ensurepip`, je potřeba doinstalovat
alternativu, Virtualenv.
Zapamatuj si, že Virtualenv budeš muset v dalším kroku použít,
a nainstaluj ho:

<!-- na Fedoře se tohle nestává -->

* Ubuntu:
  {% filter markdown(inline=True) %}
  ```console
  $ sudo apt-get install python-virtualenv
  ```
  {% endfilter %}

Používáš-li jinou distribuci, předpokládám, že instalovat programy už umíš. :)


{{ anchor('setup-venv') }}
## Vytvoření virtuálního prostředí

<!-- Pozn. Tahle sekce je velice podobná pro Linux, Mac i Windows;
     měníš-li ji, koukni se jestli není změna potřeba i jinde. -->

{%- if var('pyladies') -%}
{% set rootname = 'pyladies' %}
{%- else -%}
{% set rootname = 'naucse-python' %}
{%- endif -%}

Nakonec vytvoř virtuální prostředí.

Zvol si adresář (složku), ve které budeš mít soubory k PyLadies.
Může to být třeba <code>/home/<i>jméno</i>/{{ rootname }}</code>,
neboli <code class="pythondir">~/{{ rootname }}</code>.
Adresář vytvoř a poznamenej si, kde je.

Vytváříš-li adresář jinde, nebo s jiným názvem, tak kdykoli ve zbytku
materiálů uvidíš <code class="pythondir">~/{{ rootname }}</code>, doplň
místo toho „svůj“ adresář.

Zvolený adresář po vytvoření nesmíš přesouvat jinam – když to uděláš,
přestane virtuální prostředí fungovat.
Proto ho nedoporučuji vytářet na Ploše.

> [note]
> Kdybys někdy chtěl{{a}} adresář přece jen přesunout,
> musel{{a}} bys smazat virtuální prostředí a vytvořit nové.

Teď když je tenhle adresář vytvořený, otevři příkazovou řádku
a příkazem `cd` se do něj přepni:
<!-- XXX: Special highlight in source code needed -->
```console
$ cd ~/{{ rootname }}
```

Pak virtuální prostředí vytvoř.
Pokud jsi v přeskočil{{a}} instalaci Virtualenv, zadej:

```console
$ python3 -m venv venv
```

jinak:

```console
$ virtualenv -p python3 venv
```

Tím se ti vytvořil adresář <code><span class="pythondir">~/{{ rootname }}</span>/venv</code>,
ve kterém jsou soubory s virtuálním prostředím.
Můžeš se podívat dovnitř, ale nikdy tam nic neměň.


## Aktivace virtuálního prostředí

Nakonec virtuální prostředí aktivuj:

<div class="highlight">
<pre><code><span class="gp">$</span> source <span class="pythondir">~/{{ rootname }}</span>/venv/bin/activate
</code></pre>
</div>

Po spuštění tohoto příkazu by se mělo na začátku příkazové řádky
(před `$`) objevit slovo `(venv)`.
Tak poznáš, že je virtuální prostředí *aktivní*.

Tenhle příkaz si zapiš. Budeš ho muset zadat vždycky, když pustíš příkazovou řádku,
než se pustíš do programování.

{% if var('pyladies') %}
Máš-li vytištěné <a href="http://pyladies.cz/v1/s001-install/handout/handout.pdf">domácí projekty</a>,
příkaz si poznač, ať ho do příště nezapomeneš :)
{% endif %}

Python máš, můžeš se pustit do programování!
To už bude stejné pro tebe i pro lidi na Linuxu a Windows.
Sejdeme se na [další stránce]({{ lesson_url('beginners/first-steps') }}), kde uděláme první krůčky s Pythonem.
