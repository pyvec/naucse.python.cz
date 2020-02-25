{% extends lesson.slug + '/_base.md' %}

{% block install %}

Linux installation:

Fedora
:   ```console
    $ sudo dnf install {{ editor_cmd }}
    ```

Ubuntu
:   ```console
    $ sudo apt-get install {{ editor_cmd }}
    ```

For Windows and macOS you can probably download {{ editor_name }} from its [webpage]({{ editor_url }}).

{% endblock %}

