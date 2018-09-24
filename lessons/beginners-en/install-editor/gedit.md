{% set editor_name = 'Gedit' %}
{% set editor_cmd = 'gedit' %}
{% set editor_url = 'https://wiki.gnome.org/Apps/Gedit' %}
{% extends lesson.slug + '/_linux_base.md' %}

{% block name_gen %} Gedit {% endblock %}


{% block setup %}

To set up Gedit you have to go to <span class="en">Preferences</span>.

{{ figure(img=static('gedit_prefs.png'), alt="") }}

Line numbers
:   In View check Display Line Numbers

    {{ figure(img=static('gedit_linenums.png'), alt="") }}

Indent
:   Editor:

    * Tab width: 4
    * Insert spaces instead of tabs
    * Enable automatic indentation

    {{ figure(img=static('gedit_indent.png'), alt="") }}

Colours:
:   Colouring of code is automatic if you save the file with proper extension
    – e. g. `.py` for Python.

    So it's better if you save your file as early as possible.

{% endblock %}
