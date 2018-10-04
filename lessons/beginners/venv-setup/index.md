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

# Nastavení prostředí

V této sekci si připravíš adresář, do kterého budeš ukládat soubory
k začátečnickým kurzům Pythonu, a aktivuješ si virtuální prostředí.

## Příprava adresáře

Programátoři vytváří spoustu souborů, a víc než u mnoha jiných uživatelů
počítače záleží na tom, kde jsou ty soubory uložené.

Níže uvedený postup zdaleka není jediná možnost, jak si organizovat soubory.
Když ale použiješ tenhle ozkoušený způsob,
může to hodně zjednodušit život těm, kteří ti budou pomáhat
s případnými problémy.

{%- if var('pyladies') -%}
{% set rootname = 'pyladies' %}
{%- else -%}
{% set rootname = 'naucse-python' %}
{%- endif %}

Nejdřív vytvoř adresář (složku), ve kterém budeš mít soubory ke kurzu Pythonu.
Může to být třeba `{{ rootname }}` ve tvém domovském adresáři.
(Můžeš ho pojmenovat i jinak, ale `{{ rootname }}` používají příklady níže.)

Zvolený adresář po vytvoření nesmíš přesouvat jinam.
Proto ho nedoporučuji vytvářet na Ploše.

> [note]
> Kdybys někdy adresář přece jen přesunul{{a}} jinam,
> přestane fungovat *virtuální prostředí*, které za chvíli vytvoříme.
> Musel{{a}} bys ho smazat a vytvořit nové.

Po vytvoření adresáře si poznamenej, kde přesně je.
Budeš ho potřebovat na celý zbytek kurzu i na případné navazující kurzy.


### Adresář pro každou lekci

Nový adresář je zatím prázdný.
To se ale brzo změní a čím víc věcí v něm bude, tím bude důležitější
mít obsah zorganizovaný.

Pro začátek si budeme tvořit nový podadresář pro každou lekci tohoto kurzu.
Aby byly tyhle adresáře hezky seřazené, budeme je číslovat:
tahle první lekce bude mít číslo `01`,
příště si vytvoříš adresář `02` a tak dále.

Všechny budou v tvém novém adresáři, který jsi vytvořil{{a}} před chvilkou.

Adresář `01` si vytvoř už teď.
(Možná do něj dnes nic nedáš, ale hodí se ho mít jako ukázku pro příště.)


### Přepnutí

Pak otevři příkazovou řádku a příkazem `cd` přepni do adresáře,
ve kterém jsi právě vytvořila `01` (t.j. ne přímo do `01`).
Například:

```console
$ cd {{ rootname }}
```

Pak zkontroluj, že jsi na správném místě:
* Pomocí příkazu `pwd` (na Windows `cd`) zkontroluj,
  že opravdu jsi v nově vytvořeném adresáři.
* Pomocí příkazu `ls` (na Windows `dir`) zkontroluj,
  že v něm je podadresář `01`.

Například:

{% call sidebyside(titles=['Unix (Linux, macOS)', 'Windows']) %}
$ pwd
/home/helena/{{rootname}}

$ ls
01
---
> cd
C:\Users\Helena\{{rootname}}

> dir
 Directory of C:\Users\Helena\{{rootname}}
05/08/2014 07:28 PM <DIR>  01
{% endcall %}

{% if var('coach-present') -%}
Výsledek pro kontrolu ukaž koučovi.
{%- endif %}


## Virtuální prostředí

Teď nainstalujeme *virtuální prostředí* pro Python.

Virtuální prostředí je něco, co nám zajistí, že se všechny počítače budou
chovat zhruba stejně.
Až ho zprovozníme, nebudeme potřebovat instrukce zvlášť pro Linux,
zvlášť pro Windows a zvlášť pro macOS.

> [note]
> V budoucnu využijeme druhou výhodu: každé virtuální prostředí je oddělené od
> ostatních, takže když doinstalujeme nějakou knihovnu (rozšíření pro Python),
> projeví se to jen v jednom virtuálním prostředí.
> Pokud by se při práci na projektu něco pokazilo, neohrozí to další projekty
> ve tvém počítači.

Jak na to?
Na každém systému jinak!

* normální **Linux** (pokud jsi přeskočil{{a}} instalaci Virtualenv):

   ```console
   $ python3 -m venv venv
   ```

* starší **Linux** (pokud jsi musel{{a}} instalovat Virtualenv):

   ```console
   $ virtualenv -p python3 venv
   ```

* **macOS**:

   ```console
   $ python3 -m venv venv
   ```

* **Windows**:

   ```doscon
   > py -3 -m venv venv
   ```

Tím se ti vytvořil adresář `venv`, který virtuální prostředí obsahuje.
Můžeš se podívat dovnitř, ale neukládej tam své soubory a nikdy tam nic neměň!

Zkontroluj si, že `01` a `venv` jsou pěkně vedle sebe:

{% call sidebyside(titles=['Unix', 'Windows']) %}
$ ls
01
venv
---
> dir
 Directory of C:\Users\Helena\{{rootname}}
05/08/2014 07:28 PM <DIR>  01
05/08/2014 07:38 PM <DIR>  venv
{% endcall %}

V grafickém prohlížeči souborů to vypadá např. takto:

{{ figure(
    img=static('dirs.png'),
    alt="(adresáře '01' a 'venv' vedle sebe)",
) }}

{% if var('coach-present') -%}
Výsledek pro kontrolu ukaž koučovi.
{%- endif %}


### Aktivace virtuálního prostředí

Nakonec virtuální prostředí aktivuj:

{% call sidebyside(titles=['Unix', 'Windows']) %}
$ source venv/bin/activate
---
> venv\Scripts\activate
{% endcall %}

Po spuštění tohoto příkazu by se mělo na začátku příkazové řádky
(před `$` nebo `>`) objevit slovo `(venv)`.
Tak poznáš, že je virtuální prostředí *aktivní*.

Aktivační příkaz si zapiš.
Bude potřeba ho zadat vždycky, když pustíš příkazovou řádku,
ve které budeš zkoušet své programy.

{% if var('pyladies') %}
Máš-li vytištěné <a href="http://pyladies.cz/v1/s001-install/handout/handout.pdf">domácí projekty</a>,
příkaz si poznač tam, ať ho do příště nezapomeneš :)
{% endif %}
