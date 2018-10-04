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

Většina uživatelů ovládá počítač v *grafickém rozhraní* – myší nebo prstem
kliká na ikonky, vybírá příkazy z menu a kouká na animace.
Programátoři ale často ovládají počítač *textově*, v příkazové řádce:
napíšou příkaz nebo otázku a přečtou si případnou odpověď.
Někteří to nemají moc rádi (příkazy je potřeba si pamatovat), někteří si
to užívají (textové příkazy lze jednoduše opakovat a automatizovat),
ale fakt je, že bez základní znalosti příkazové řádky se programátor neobejde.

Seznamme se tedy se způsobem, který programátoři používají na zadávání příkazů.

Příkazová řádka (respektive program, kterému se říká i *konzole* či *terminál*;
anglicky *command line*, *console*, *terminal*)
se na různých systémech otevírá různě:

* Windows (české): Start → napsat na klávesnici „cmd“ → Příkazový řádek
* Windows (anglické): Start → napsat na klávesnici „cmd“ → Command Prompt
* macOS (anglický): Applications → Utilities → Terminal
* Linux (GNOME): Menu Aktivity (levý horní roh) → hledat Terminál
* Linux (KDE): Hlavní Menu → hledat Konsole

Nevíš-li si rady, zkus
{% if var('coach-present') -%}
se zeptat kouče.
{%- else -%}
buď googlit, nebo se zeptat e-mailem.
{%- endif %}

Po otevření konzole tě uvítá okýnko s řádkem textu,
kterým počítač vybízí k zadání příkazu.
Podle systému bude tento řádek končit buď znakem `$` nebo `>`,
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
Objeví se přihlašovací jméno. Třeba u Heleny to vypadalo takhle:

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

Je to podobné, jako když si na počítači otevřeš prohlížeč souborů.
Na každém počítači takový program vypadá trochu jinak, ale většinou máš
nahoře jméno aktuálního adresáře a v hlavním okýnku seznam souborů,
které v tom adresáři jsou:

{{ figure(
     img=static('dirs.png'),
     alt='Screenshot prohlížeče souborů',
) }}

Podobně příkazová řádka je vždy „v“ nějakém *aktuálním adresáři*.
Který to je, to bývá napsáno před znakem `$` nebo `>` (občas ve zkrácené podobě).
Vždycky se ale dá vypsat příkazem, který se podle systému
jmenuje `pwd` nebo `cd` (z angl. *print working directory* – vypiš pracovní
adresář, resp. *current directory* – aktuální adresář).

{% call sidebyside() %}
$ pwd
/home/helena/
---
> cd
C:\Users\helena
{% endcall %}

U tebe se bude aktuální adresář nejspíš jmenovat trochu jinak.

Tento adresář – ten, ve kterém příkazová řádka „začíná“ – je tvůj
*domovský adresář*.
Typicky obsahuje všechny tvoje soubory a nastavení.


## Co v tom adresáři je?

V prohlížeči souborů se ukazují soubory v aktuálním adresáři neustále.
V příkazové řádce si o ně ale musíš „říct“ příkazem `ls` nebo `dir`
(z angl. *list* – vyjmenovat, resp. *directory* – adresář).
Ten vypíše, co aktuální adresář obsahuje: všechny soubory,
včetně podadresářů, které se v aktuálním adresáři nacházejí.
Na některých systémech ukáže jen jména, jinde i další informace.
Například:

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

Na tvém počítači nejspíš budou jiné soubory, ale aspoň `Desktop` a `Music`
(nebo `Plocha` a `Hudba`) na většině počítačů jsou.


## Kopírování textu

Z příkazové řádky se dá kopírovat text.
Háček je ale v tom, že to nejde přes <kbd>Ctrl</kbd>+<kbd>C</kbd> – tahle
zkratka tu znamená něco jiného.

Zkus si zkopírovat jméno aktuálního adresáře.

* Na **Linuxu** všech systémech text vyber myší, pak klikni pravým tlačítkem
  myši a z menu vyber kopírování.
  Případně funguje zkratka <kbd>Ctrl</kbd>+<kbd>Insert</kbd>.

* Na **macOS** to je nejjednodušší: text vyber a zkopíruj pomocí
  <kbd>⌘</kbd>+<kbd>C</kbd>

* Na **Windows** napřed klikni na ikonku okýnka, rozbal *Edit* a vyber
  *Vybrat* (*Select*). Pak text vyber myší a zkopíruj klávesou
  <kbd>Enter</kbd>.

  (Na některých verzích Windows jde vybírat přímo myší, nemusíš přes menu.)

Zkus zkopírované jméno adresáře vložit do grafického prohlížeče souborů.
Měl{{a}} bys pak vidět obsah i tam.

V dalších sekcích budeme potřebovat adresáře `Desktop` a `Music` (nebo `Plocha`
a `Hudba`).
Jestli je ve svém domovském adresáři nemáš, v grafickém prohlížeči si je
vytvoř a v příkazové řádce zkontroluj, že je máš.

{% call sidebyside() %}
$ ls
…
Desktop
Music
…
---
> dir
 Directory of C:\Users\helena
…
05/08/2014 07:28 PM <DIR>  Desktop
05/08/2014 07:28 PM <DIR>  Music
…
{% endcall %}


## Změna aktuálního adresáře

Aktuální adresář se dá změnit pomocí příkazu `cd`
(z angl. *change directory* – změnit adresář).
Za `cd` se píše jméno adresáře, kam chceš přejít.

> [note] Déjà vu?
> Jsi-li na Windows, příkaz `cd` už jsi používal{{a}}.
> Chová se ale různě podle toho, jestli něco napíšeš za něj nebo ne!

Přejdi do adresáře `Desktop` (nebo `Plocha`).
Pak si nový aktuální adresář vypiš, aby sis ověřil{{a}},
že jsi na správném místě.

{% call sidebyside() %}
$ cd Desktop
$ pwd
/home/helena/Desktop
---
> cd Desktop
> cd
C:\Users\helena\Desktop
{% endcall %}

> [note] Velikost písmen
> Jsi-li na Linuxu nebo macOS, dej si pozor na velikost písmen: na těchto
> systémech jsou `Desktop` a `desktop` dvě různá jména.

> [note] Windows a disky
> Pokud přecházíš do adresáře na jiném disku,
> například `D:` místo `C:`, je potřeba kromě `cd`
> zadat jméno disku s dvojtečkou jako zvláštní příkaz (např. `D:`).


## Cesta zpět

Zkusíme teď místo do `Desktop` (nebo `Plocha`) přejít do `Music`
(nebo `Hudba)`.

Když zadáš `cd Music`, pravděpodobně uvidíš *chybu*: v aktuálním
adresáři (`Desktop`) žádné `Music` není.

Aby ses do něj dostal{{a}}, musíš nejdřív zpátky, do „nadřazeného“ adresáře.
To dělá příkaz `cd ..` – `cd`, mezera, a dvě tečky.
Zkus ho zadat a pak se podívat, jak se aktuální adresář změnil:

{% call sidebyside() %}
$ cd ..
$ pwd
/home/helena
---
> cd ..
> cd
C:\Users\helena
{% endcall %}

Z domovského adresáře už můžeš zadat `cd Music` (nebo `cd Hudba`) bez chyby.


## Další příkazy

Textových příkazů existuje daleko víc než `whoami` a `cd`.
Z příkazové řádky můžeš vytvářet adresáře, měnit soubory, nebo si třeba přečíst
e-mail.

I „grafické“ programy, které máš na počítači nainstalované, jdou
z příkazové řádky spustit – a to většinou jen zadáním jména.
Zkus, jestli na tvém počítači bude fungovat `firefox`, `notepad`, `safari`
nebo `gedit`.

Při učení Pythonu si ale vystačíme s málem: s `cd`/`pwd` a několika příkazy,
které zanedlouho nainstalujeme – například `python`.


## Konec

Nakonec vyzkoušej ještě jeden příkaz.
Ten, který příkazovou řádku zavírá: `exit`.

Příkaz `exit` funguje stejně na všech systémech.
Proto už nebudu používat ukázku rozdělenou pro Unix a Windows.

```console
$ exit
```

Ve zbytku těchto materiálů budeme pro kód, který je potřeba zadat do
příkazové řádky, používat unixovské `$`.
S touto konvencí se setkáš i ve většině návodů na internetu.
Používáš-li Windows, je dobré si na `$` zvyknout, i když ve své
řádce máš místo něj `>`.

