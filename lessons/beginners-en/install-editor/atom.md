{% set editor_name = 'Atom' %}
{% set editor_url = 'https://atom.io' %}
{% extends lesson.slug + '/_base.md' %}

{% block name_gen %} Atom {% endblock %}

{% block setup %}

You don't have to set up anything in Atom.

Indentation and colouring, how we want it, works only with files with `.py`
extension.

So it's better if you save your file as early as possible.

## Code style

There is just one thing missing in Atom: plug-in for checking
code style

As every written language Python also has its typographic rules.
You can find them here in [PEP8](https://www.python.org/dev/peps/pep-0008/) document.

If you don't want to remember them just install plug-in which will always
notice you if you violate some.

Firstly we will have to install special library which takes care of this.
Write into your command line:

```console
$ python -m pip install flake8
```

And now just install the plug-in.
In the main menu choose "File > Settings" and click on "Install".
Then search for „linter-flake8“ and in the list click "Install" next to
the "linter-flake8". You will be also asked for installation of every 
dependency.

{% endblock %}
