{% extends lesson.slug + '/_base.md' %}

{% block install %}

Na Linuxu se {{ editor_name }} instaluje jako ostatní programy:

Fedora
:   `sudo dnf install {{ editor_cmd }}`

Ubuntu
:   `sudo apt-get install {{ editor_cmd }}`

Používáš-li jiný systém, předpokládám že programy instalovat umíš :)

Pro Windows a MacOS se {{ editor_name }} dá stáhnout z [domovské stránky]({{ editor_url }}).

{% endblock %}

