{% set editor_name = 'Visual Studio Code' %}
{% set editor_url = 'https://code.visualstudio.com/Download' %}
{% extends lesson.slug + '/_base.md' %}

{% block name_gen %} Visual Studio Code{% endblock %}

{% block setup %}

Ve VSCodu se nemusí nic nastavovat, funguje „od výroby“ tak, jak má.

Odsazování a obarvování bude fungovat správně jen v souborech s koncovkou `.py`
(jako Python).
V jiných programovacích jazycích se totiž odsazuje i obarvuje jinak.

Proto jakmile v tomhle editoru vytvoříš nový soubor,
měl{{a}} bys ho co nejdřív uložit pod správným jménem.

{% endblock %}
