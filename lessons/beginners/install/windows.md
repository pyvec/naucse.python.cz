# Instalace Pythonu pro Windows

Go to the [Pythonu webpage](https://www.python.org/downloads/)
and download installer of the newest stable version of Python. For our course, please download version **3.8.1 or newer**.

How to recognise what installer is right for you?
In case you have 64-bit version of the Windows, download *Windows x86-64 executable installer*.
In case of 32-bit Windows, download *Windows x86 executable installer*.

Test

> [note]
> In case you are not sure whether you are using 32 or 64-bit Windows, open
> **Start**, serch „System“ and open **System information**.
>
> {{ figure(
    img=static('windows_32v64-bit.png'),
    alt='Screenshot zjišťování verze systému',
) }}

Then run installer.
At the beginning of the installation process choose **Install launcher for all Users**
and also **Add Python 3.8 to PATH**.

(In case you don't have admin account on your computer, don't check option
*Install launcher for all Users* )

{{ figure(
    img=static('windows_add_python_to_path.png'),
    alt='Screenshot instalace Pythonu',
) }}

Press **Install now** and follow the instructions



## Vytvoření virtuálního prostředí

<!-- Pozn. Tahle sekce je velice podobná pro Linux, Mac i Windows;
     měníš-li ji, koukni se jestli není změna potřeba i jinde. -->

{%- if var('pyladies') -%}
{% set rootname = 'pyladies' %}
{%- else -%}
{% set rootname = 'naucse-python' %}
{%- endif -%}

Once the Python will be installed, please create virtuall environment.

Choose the folder where you want to have files related to the Tieto Python Academy.
It can be for example `C:\{{ rootname }}`.

Open the command line({{ lesson_url('beginners/cmdline') }})
and using `cd` switch to it.
Create virtual environment:

```dosvenv
> py -3 -m venv venv
```

Directory <code><span class="pythondir">~/{{ rootname }}</span>\venv</code> were created,


## Virtual environment activation

You canenable the virtual environment like this:

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
