{%- macro sidebyside(titles=['Unix', 'Windows']) -%}
    <div class="row side-by-side-commands">
        {%- for title in titles -%}
            <div class="col">
                <h4>{{ title }}</h4>
{%- filter markdown() -%}
```{%- if title.lower().startswith('win') -%}dosvenv{%- else -%}console{%- endif -%}
{{ caller() | extract_part(loop.index0, '---') | dedent }}
```
{%- endfilter -%}
            </div>
        {%- endfor -%}
    </div>
{%- endmacro -%}

{%- if var('pyladies') -%}
{% set purpose = 'PyLadies' %}
{% set dirname = 'pyladies' %}
{%- else -%}
{% set purpose = 'Python' %}
{% set dirname = 'naucse-python' %}
{%- endif -%}


# Příkazová řádka

V této lekci se seznámíme s *příkazovou řádkou* – černým okýnkem,
které programátoři používají na zadávání příkazů.
Na první pohled může vypadat nepřirozeně, ale dá se na ni zvyknout :)


Příkazová řádka
(respektive program, kterému se říká i *konzole* či *terminál*;
anglicky *command line*, *console*, *terminal*)
se na různých systémech otevírá různě:

* Windows (české): Start → napsat na klávesnici „cmd“ → Příkazový řádek
* Windows (anglické): Start → napsat na klávesnici „cmd“ → Command Prompt
* macOS (anglický): Applications → Utilities → Terminal
* Linux (KDE): Hlavní Menu → hledat Konsole
* Linux (GNOME): Super → hledat Terminál

Nevíš-li si rady, zkus buď googlit,
{% if var('coach-present') -%}
nebo se jednoduše zeptat kouče.
{%- else -%}
nebo se zeptat e-mailem.
{%- endif %}


Po otevření konzole tě uvítá řádek,
kterým počítač vybízí k zadání příkazu.
Podle systému bude končit buď znakem `$` nebo `>`,
před nímž můžou být ještě další informace:

{% call sidebyside(titles=['Unix (Linux, macOS)', 'Windows']) %}
$
---
>
{% endcall %}

Podle systému se potom liší i samotné příkazy, které budeš zadávat.

> [note] Velikost písma
> Je-li ve Windows moc malé písmo, klikni na ikonku okna a vyber Možnosti.
> V záložce Písmo si pak můžeš vybrat větší font.
> <!-- XXX: are the Czech names correct? -->
>
> {{ figure(
     img=static('windows-cmd-properties.png'),
     alt='Screenshot menu příkazové řádky',
) }}
>
> Na ostatních systémech hledej v nastavení, nebo zkus
> <kbd>Ctrl</kbd>+<kbd>+</kbd> a
> <kbd>Ctrl</kbd>+<kbd>-</kbd> (příp. se Shift).


## První příkaz

Začneme jednoduchým příkazem.
Napiš `whoami` (z angl. *who am I?* – kdo jsem?)
a stiskni <kbd>Enter</kbd>.
Objeví se přihlašovací jméno. Třeba u Heleny by to vypadalo takhle:

{% call sidebyside() %}
$ whoami
helena
---
> whoami
pocitac\Helena
{% endcall %}



> [note]
> Znak `$` nebo `>` je v ukázce jen proto, aby bylo jasné, že zadáváme
> příkaz do příkazové řádky.
> Vypíše ho počítač, většinou ještě s něčím před ním,
> takže ho nepiš sama! Zadej jen `whoami` a <kbd>Enter</kbd>.
>
> Stejně tak počítač sám vypíše přihlašovací jméno.


## Aktuální adresář

Příkazová řádka pracuje vždy v nějakém *adresáři* (neboli *složce*,
angl. *directory*, *folder*).
Ve kterém adresáři zrovna je, to nám poví příkaz, který se podle systému
jmenuje `pwd` nebo `cd` (z angl. *print working directory* – vypiš pracovní
adresář, resp. *current directory* – aktuální adresář).

{% call sidebyside() %}
$ pwd
/home/helena/
---
> cd
C:\Users\helena
{% endcall %}


Aktuální adresář se většinou ukazuje i před znakem `$` nebo `>`,
ale je dobré `pwd`/`cd` znát, kdyby ses náhodou ztratil{{a}}
(nebo musel{{a}} pracovat na počítači který před `$` ukazuje něco jiného).


## Co v tom adresáři je?

Příkaz `ls` nebo `dir` (z angl. *list* – vyjmenovat, resp. *directory* – adresář)
nám vypíše, co aktuální adresář obsahuje: všechny soubory,
včetně podadresářů, které se v aktuálním adresáři nacházejí.

{% call sidebyside() %}
$ ls
Applications
Desktop
Downloads
Music
…
---
> dir
 Directory of C:\Users\helena
05/08/2014 07:28 PM <DIR>  Applications
05/08/2014 07:28 PM <DIR>  Desktop
05/08/2014 07:28 PM <DIR>  Downloads
05/08/2014 07:28 PM <DIR>  Music
…
{% endcall %}


## Změna aktuálního adresáře

Aktuální adresář se dá změnit pomocí příkazu `cd`
(z angl. *change directory* – změnit adresář).
Za `cd` se píše jméno adresáře, kam chceme přejít.
Pokud máš adresář `Desktop` nebo `Plocha`, přejdi tam. Pak nezapomeň ověřit,
že jsi na správném místě.

Jsi-li na Linuxu nebo macOS, dej si pozor na velikost písmen: na těchto
systémech jsou `Desktop` a `desktop` dvě různá jména.

Jsi-li na Windows, `cd` už jsi používal{{a}} – tento příkaz se chová různě
podle toho, jestli něco napíšeš za něj nebo ne.

{% call sidebyside() %}
$ cd Desktop
$ pwd
/home/helena/Desktop
---
> cd Desktop
> cd
C:\Users\helena\Desktop
{% endcall %}

> [note] Poznámka pro Windows
> Pokud přecházíš do adresáře na jiném disku,
> například `D:` místo `C:`, je potřeba kromě `cd`
> zadat jméno disku s dvojtečkou jako zvláštní příkaz (např. `D:`).

## Vytvoření adresáře

Co takhle si vytvořit adresář na {{ purpose }}? To se dělá příkazem `mkdir`
(z angl. *make directory* – vytvořit adresář).
Za tento příkaz napiš jméno adresáře, který chceš vytvořit – v našem případě
`{{ dirname }}`:


{% call sidebyside() %}
$ mkdir {{ dirname }}
---
> mkdir {{ dirname }}
{% endcall %}

Teď se můžeš podívat na Plochu nebo do nějakého grafickém programu na
prohlížení adresářů: zjistíš, že adresář se opravdu vytvořil!

## Úkol
Zkus v nově vytvořeném adresáři `{{ dirname }}`
vytvořit adresář `test`
a zkontrolovat, že se opravdu vytvořil.

Budou se hodit příkazy `cd`, `mkdir` a `ls` či `dir`.

{% filter solution %}
{% call sidebyside() %}
$ cd {{ dirname }}
$ mkdir test
$ ls
test
---
> cd {{ dirname }}
> mkdir test
> dir
05/08/2014 07:28 PM <DIR>  test
{% endcall %}
{% endfilter %}


## Úklid

Teď vytvořené adresáře zase smažeme.

Nemůžeš ale smazat adresář, ve kterém jsi.
Proto se vrátíme na `Desktop`.
Ale nemůžeme použít `cd Desktop` – v aktuálním adresáři žádný `Desktop` není.
Potřebuješ se dostat do *nadřazeného adresáře*: toho, který obsahuje
adresář ve kterém právě jsi.
Nadřazený adresář se značí dvěma tečkami:

{% call sidebyside() %}
$ pwd
/home/helena/Desktop/{{ dirname }}
$ cd ..
$ pwd
/home/helena/Desktop
---
> cd
C:\Users\helena\Desktop\{{ dirname }}
> cd ..
> cd
C:\Users\helena\Desktop
{% endcall %}

Teď můžeš smazat vytvořený adresář `{{ dirname }}`.
K tomu použij příkaz `rm` nebo `rmdir`
(z *remove* – odstraň, resp. *remove directory* – odstraň adresář).

> [warning] Pozor!
> Příkazová řádka nepoužívá odpadkový koš!
> Všechno se nadobro smaže. Takže si dobře překontroluj, že mažeš
> správný adresář.

Na Unixu za tento příkaz musíš napsat ještě jedno slovo: `-rv` (minus,
`r`, `v`).
To je takzvaný *přepínač*, který příkazu říká, že má smazat celý adresář
včetně všeho, co obsahuje (`r`),
a že má informovat o tom co dělá (`v`).

Obdobně i na Windows je potřeba zadat přepínač, který říká, že má smazat
adresář a veškerý jeho obsah. Tentokrát je to `/S` (lomítko, `S`).
Příkaz `rmdir` se automaticky ujistí, jestli to co mažeš opravdu chceš smazat.

{% call sidebyside() %}
$ pwd
/home/helena/Desktop
$ rm -rv {{ dirname }}
removed directory: ‘{{ dirname }}’
---
> cd
C:\Users\helena\Desktop
> rmdir /S {{ dirname }}
{{ dirname }}, Are you sure <Y/N>? Y
{% endcall %}


## Shrnutí

Tady je tabulka základních příkazů, se kterými si zatím vystačíme:

<table class="table">
    <tr>
        <th>Unix</th>
        <th>Windows</th>
        <th>Popis</th>
        <th>Příklad</th>
    </tr>
    <tr>
        <td><code>cd</code></td>
        <td><code>cd</code></td>
        <td>změna adresáře</td>
        <td><code>cd test</code></td>
    </tr>
    <tr>
        <td><code>pwd</code></td>
        <td><code>cd</code></td>
        <td>výpis aktuálního adresáře</td>
        <td><code>pwd</code><br><code>cd</code></td>
    </tr>
    <tr>
        <td><code>ls</code></td>
        <td><code>dir</code></td>
        <td>výpis adresáře</td>
        <td><code>ls</code><br><code>dir</code></td>
    </tr>
    <tr>
        <td><code>cp</code></td>
        <td><code>copy</code></td>
        <td>zkopírování souboru</td>
        <td>
            <code>cp puvodni.txt kopie.txt</code>
            <br>
            <code>copy puvodni.txt kopie.txt</code>
        </td>
    </tr>
    <tr>
        <td><code>mv</code></td>
        <td><code>move</code></td>
        <td>přesun/přejmenování souboru</td>
        <td>
            <code>mv puvodni.txt novy.txt</code>
            <br>
            <code>move puvodni.txt novy.txt</code>
        </td>
    </tr>
    <tr>
        <td><code>mkdir</code></td>
        <td><code>mkdir</code></td>
        <td>vytvoření adresáře</td>
        <td><code>mkdir test</code></td>
    </tr>
    <tr>
        <td><code>rm</code></td>
        <td><code>del</code></td>
        <td>smazání souboru</td>
        <td><code>rm test.txt</code><br><code>del test.txt</code></td>
    </tr>
    <tr>
        <td><code>rm -r</code></td>
        <td><code>rmdir /S</code></td>
        <td>smazání adresáře</td>
        <td><code>rm -r test</code><br><code>rmdir /S test</code></td>
    </tr>
    <tr>
        <td><code>exit</code></td>
        <td><code>exit</code></td>
        <td>ukončení</td>
        <td><code>exit</code></td>
    </tr>
</table>

Příkazů existuje samozřejmě daleko víc.
Dokonce každý program, který máš na počítači nainstalovaný, jde spustit
z příkazové řádky – a to většinou jen zadáním jeho jména.
Zkus, jestli na tvém počítači bude fungovat `firefox`, `notepad`, `safari`
nebo `gedit`.
{% if var('coach-present') -%}
Kdyby nefungoval ani jeden, zeptej se kouče ať najde nějaký, co u tebe fungovat
bude.
{%- endif %}

Při učení Pythonu použiješ programy/příkazy jako `python` a `git`, které
zanedlouho nainstalujeme.
<!--- XXX: this assumes installation is after intro to cmdline -->


## Konec

Nakonec vyzkoušej ještě jeden příkaz.
Ten, který příkazovou řádku zavírá: `exit`.

Jako většina příkazů (kromě pár z těch základních) funguje `exit`
stejně na všech systémech.
Proto už nebudu používat ukázku rozdělenou pro Unix a Windows.

```console
$ exit
```

Ve zbytku těchto materiálů budeme pro kód, který je potřeba zadat do
příkazové řádky, používat unixovské `$`.
S touto konvencí se setkáš i ve většině návodů na internetu.
Používáš-li Windows, je dobré si na `$` zvyknout, i když ve své
řádce máš místo něj `>`.

