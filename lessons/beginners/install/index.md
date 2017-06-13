# Instalace Pythonu

V této sekci uděláme dvě věci:

* Nainstalujeme Python a Virtualenv
* Vytvoříme si virtuální prostředí pro práci v Pythonu

Možná se ptáš, proč je to všechno potřeba?

Python je jak programovací jazyk (způsob, jak říkat počítačům co dělat),
tak program, který potřebujeme, aby se s námi počítač tím jazykem domluvil.

Virtuální prostředí pak je něco, co zajistí, aby se všechny počítače chovaly
zhruba stejně.
Až ho zprovozníme, nebudeme potřebovat materiály zvlášť pro Linux, zvlášť pro
Windows, a zvlášť pro Mac.

> [note]
> V budoucnu využijeme druhou výhodu: každé virtuální prostředí je oddělené od
> ostatních, takže když doinstalujeme nějakou knihovnu (rozšíření pro Python),
> projeví se to jen v jednom virtuálním prostředí.
> Pokud by se při práci na projektu něco pokazilo, neohrozí to další projekty
> ve tvém počítači.

Instalace samotná je na každém počítači jiná.
Vyber si stránku podle svého operačního systému:

* [Linux]({{ subpage_url('linux') }})
* [Windows]({{ subpage_url('windows') }})
* [MacOS]({{ subpage_url('macos') }})

Pokud máš jiný systém než Linux, Windows nebo MacOS,
nebo pokud ke svému počítači neznáš administrátorské heslo,
{% if var('coach-present') -%}
poraď se s koučem hned, jinak se ptej, až bude něco nejasné.
{%- else -%}
napiš nám prosím e-mail. {# XXX vyřešit kam poslat samostudenty co mají problém #}
{%- endif %}
