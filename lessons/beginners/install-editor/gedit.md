{% set editor_name = 'Gedit' %}
{% set editor_cmd = 'gedit' %}
{% set editor_url = 'https://wiki.gnome.org/Apps/Gedit' %}
{% extends lesson.slug + '/_linux_base.md' %}

{% block name_gen %} Geditu {% endblock %}


{% block setup %}

Gedit se nastavuje v Předvolbách <span class="en">(Preferences)</span>.

{{ figure(img=static('gedit_prefs.png'), alt="") }}

Číslování řádků
:   V sekci Zobrazit/<span class="en">View</span> vyber
    Zobrazovat čísla řádků/<span class="en">Display Line Numbers</span>.

    {{ figure(img=static('gedit_linenums.png'), alt="") }}

Odsazování
:   V sekci Editor vyber:

    * Šířka tabulátorů/<span class="en">Tab width</span>: 4
    * Vkládat mezery místo tabulátorů<span class="en">/Insert spaces instead of tabs</span>
    * Povolit automatické odsazování<span class="en">/Enable automatic indentation</span>

    {{ figure(img=static('gedit_indent.png'), alt="") }}

Obarvování
:   Obarvování funguje automaticky, ale způsob obarvování se vybírá podle
    koncovky souboru – např. `.py` pro Python.

    Proto jakmile v tomhle editoru vytvoříš nový soubor, měl{{a}} bys ho co
    nejdřív uložit pod správným jménem.

{% endblock %}
