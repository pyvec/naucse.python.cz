{% extends lesson.slug + '/_linux_base.md' %}

{% block name_gen %} editoru {% endblock %}

{% block install %}

Používáš-li editor, pro který nemáme instrukce, budeš ho muset nastavit
{{ gnd('sám', 'sama') }}.
Tady je pár tipů, na co si dát pozor.

{% endblock %}

{% block setup %}

## Číslování řádků

Ujisti se, že ti editor čísluje řádky.
Pokud ne, podívej se do nastavení a zjisti jak se to zapíná.


## Obarvování

Ulož soubor s koncovkou `.py` – například `zkouska.py`, a zkopíruj do něj
následující program:

```python
def foo():
    return "abc" * 2
```

Jestli se text automaticky obarví (klidně jinými barvami než tady),
je tvůj editor nastavený správně.
Jinak se podívej do nastavení a zjisti jak se to zapíná.


## Odsazování

Stisknutím klávesy <kbd>Tab</kbd> na *začatku řádku* se vloží 4 mezery.
Pro psaní a sdílení kódu v Pythonu je důležité,
aby byly čtyři, a aby to byly opravdu mezery.

Jestli to jsou mezery, se dá zjistit tak, že odsazení na začátku vybereš myší.
Jde-li vybírat po jednotlivých mezerách, je všechno v pořádku.

Nejde-li vybírat po jednotlivých mezerách, nebo pokud se jich po stisknutí
<kbd>Tab</kbd> vloží jiný počet než 4, podívej se do nastavení po možnostech
jako „velikost odsazení“ nebo „nahrazovat tabelátory za mezery”.

{% endblock %}
