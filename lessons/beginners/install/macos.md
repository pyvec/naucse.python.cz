# Instalace Pythonu pro macOS

Nainstaluj si nástroj [Homebrew](http://brew.sh), který řeší a zjednodušuje
instalaci aplikací a knihoven, které budeme potřebovat pro programování.
Jak na to?

Spusť v [příkazové řádce]({{ lesson_url('beginners/cmdline') }}) příkaz:

```console
$ /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
```

Pak zadej následující příkaz a Python bude nainstalovaný:

```console
$ brew install python3
```

Zkontroluj si, že máš verzi 3.6 nebo vyšší:

```console
$ python3 --version
```

Objeví-li se „Python“ a číslo verze (např. `Python 3.6.6`)
a verze je 3.6 nebo vyšší, máš nainstalováno.
Jinak je něco špatně;
{% if var('coach-present') -%}
poraď se s koučem.
{%- else -%}
zkus instalaci znovu.
Když to nevyjde, poraď se s někým zkušenějším.
{%- endif %}
