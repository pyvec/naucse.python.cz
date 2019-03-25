{# Global "index" variable for page-wide numbering of tasks #}
{# (In Jinja we need to store the variable in a "namespace") #}
{% set global = {'index': 0} %}

<ol start="{{ global.index }}">
{% for task in data.tasks %}
    {% if 'section' in task %}
        </ol>
        {% if global.index %}<hr>{% endif -%}
        {% if 'markdown' in task.section -%}
            <div class="group-heading">
                {{ task.section.markdown | markdown }}
            </div>
        {% endif %}
        <ol start="{{ global.index }}">
    {% else %}
        <li>
            {{ task.markdown | markdown }}
        </li>
        {% set _ = global.update(index = global.index + 1) %}
    {% endif %}
{% endfor %}
</ol>
