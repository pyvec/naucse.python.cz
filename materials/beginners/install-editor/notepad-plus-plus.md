{% set editor_name = 'Notepad++' %}
{% set editor_url = 'https://notepad-plus-plus.org/' %}
{% extends lesson.slug + '/_base.md' %}

{% block name_gen %} Notepadu++ {% endblock %}

{% block install %}

Notepad++ je k dispozici pouze pro Windows.

Stáhni jej z jeho [domovské stránky](https://notepad-plus-plus.org/)
a nainstaluj.

{% endblock %}


{% block setup %}

Odsazování
:   V menu Nastavení zvol Předvolby a pak nastav
    „Nastavení tabulátoru<span class="en">/Tab Settings</span>“ na 
    „Zaměnit za mezery<span class="en">/Replace by Space</span>“.

Obarvování bude fungovat automaticky v souborech s koncovkou `.py`
(jako Python).
V jiných programovacích jazycích se totiž odsazuje i obarvuje jinak.

Proto, jakmile v tomhle editoru vytvoříš nový soubor,
měl{{a}} bys ho co nejdřív uložit pod správným jménem.

{% endblock %}
