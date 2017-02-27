{% set editor_name = 'Kate' %}
{% set editor_cmd = 'kate' %}
{% set editor_url = 'https://kate-editor.org/get-it/' %}
{% extends lesson.slug + '/_linux_base.md' %}

{% block name_gen %} Kate {% endblock %}


{% block setup %}

Číslování řádků
:   V menu Pohled<span class="en">/View</span> vyber
    Ukazovat čísla řádek<span class="en">/Show Line Numbers</span>.

Odsazování
:   V Menu Nastavení<span class="en">/Settings</span> vyber
    Nastavit 'Kate'<span class="en">/Configure Kate</span>.

    Tam v Úpravy<span class="en">/Editing</span> vyber
    Odsazování<span class="en">/Indentation</span>.

    Tam nastav:

    * Výchozí režim odsazení<span class="en">/Default indentation mode</span>: Python
    * Odsazovat pomocí<span class="en">/Indent using</span>: Mezer<span class="en">/Spaces</span>
    * Šířka tabulátoru<span class="en">/Tab Width</span>: 4 znaky
    * Odsadit pomocí<span class="en">/Indentation width</span>: 4 znaky
    * Klávesa Backspace zpětně odsazuje v úvodních mezerách<span class="en">/Backspace key in leading blank space unindents</span>

Obarvování
:   Obarvování funguje automaticky, ale způsob obarvování se vybírá podle
    koncovky souboru – např. `.py` pro Python.

    Proto, jakmile v tomhle editoru vytvoříš nový soubor, měl{{a}} bys ho co
    nejdřív uložit pod správným jménem.

{% endblock %}
