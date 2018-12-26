{% extends lesson.slug + '/_base.md' %}

{% block install %}

Na Linuxu se {{ editor_name }} instaluje jako ostatní programy:

Fedora
:   ```console
    $ sudo dnf install {{ editor_cmd }}
    ```

Ubuntu
:   ```console
    $ sudo apt-get install {{ editor_cmd }}
    ```

Používáš-li jiný Linux, předpokládám že programy instalovat umíš. :)

Pro Windows a macOS se {{ editor_name }} dá stáhnout z [domovské stránky]({{ editor_url }}).

{% endblock %}

