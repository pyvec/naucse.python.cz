{% set editor_name = 'Kate' %}
{% set editor_cmd = 'kate' %}
{% set editor_url = 'https://kate-editor.org/get-it/' %}
{% extends lesson.slug + '/_linux_base.md' %}

{% block name_gen %} Kate {% endblock %}


{% block setup %}

Line numbers
:   In menu View pick Show Line Numbers.

Indentation:
:   In Settings choose Configure Kate

    Editing > Indentation

    Now set here:

    * Default indentation mode: Python
    * Indent using: Spaces
    * Tab Width: 4
    * Indentation width: 4
    * Backspace key in leading blank space unindents

Colours:
:   Colouring of code is automatic if you save the file with proper extension
    – e. g. `.py` for Python.

    So it's better if you save your file as early as possible.
{% endblock %}
