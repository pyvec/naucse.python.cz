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
Pokud ne, podívej se do nastavení a zjisti, jak se to zapíná.


## Obarvování

Ulož soubor s koncovkou `.py` – například `zkouska.py` – a zkopíruj do něj
následující program:

```python
def foo():
    return "abc" * 2
```

Jestli se text automaticky obarví (klidně jinými barvami než tady),
je tvůj editor nastavený správně.
Jinak se podívej do nastavení a zjisti, jak se to zapíná.


## Odsazování

Stisknutím klávesy <kbd>Tab</kbd> na *začatku řádku* se vloží 4 mezery.
Pro psaní a sdílení kódu v Pythonu je důležité,
aby byly čtyři a aby to byly opravdu mezery.

Jestli to jsou mezery, se dá zjistit tak, že odsazení na začátku vybereš myší.
Jde-li vybírat po jednotlivých mezerách, je všechno v pořádku.

Nejde-li vybírat po jednotlivých mezerách, nebo pokud se jich po stisknutí
<kbd>Tab</kbd> vloží jiný počet než 4, podívej se do nastavení po možnostech
jako „velikost odsazení“ nebo „nahrazovat tabulátory za mezery”.


## Kontrola stylu zdrojového kódu

Editory často podporují instalaci pluginů, které mohou psaní kódu usnadnit
a pomoci s jeho kontrolou.
Jeden z neužitečnějších je plugin pro kontrolu správného stylu zdrojového kódu.

Tak jako čeština má Python typografická providla.
Například za čárkou se píše mezera, ale před ní ne.
Jsou nepovinná, program bude fungovat i při jejich nedodržení,
ale pomáhají psát přehledný kód, tak je dobré je dodržovat už od začátku.
Tato pravidla jsou popsána
v dokumentu [PEP8](https://www.python.org/dev/peps/pep-0008/).

Zkus takový plugin pro svůj editor najít a nainstalovat.

{% endblock %}
