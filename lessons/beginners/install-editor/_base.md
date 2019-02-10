# Instalace {% block name_gen %} editoru {{ var('editor_name') }} {% endblock %}


{% block install %}

Editor {{ editor_name }}
si stáhni z jeho [domovské stránky]({{ editor_url }})
a nainstaluj.

{% endblock %}

## Nastavení

{% block setup %}

(Tohle by nemělo být vidět)

{% endblock %}


## Nácvik odsazování

Jak už bylo zmíněno, v Pythonu je důležité, kolika mezerami řádek začíná.
Proto se nám bude hodit vědět, jak rychle odsazovat bloky textu.
Pojďme si ukázat, jak na to.

Zkopíruj si do editoru tento text:

```
Ofelie:
Ach princi!
Jak má se Vaše Výsost už tak dlouho?
Hamlet:
Děkují poníženě: skvěle, skvěle, skvěle.
Ofelie:
Mám od vás, princi, stále ještě dárky,
Jež dávno toužím vrátit. Prosím vás,
račte je přijmout teď.
Hamlet:
Kdo? Já? Já nikdy
vám nedal nic.
Ofelie:
Dal, Výsosti. A spolu s dárky slova
tak rozmilá, že každý z nich
měl jejich vůni. Ta teď vyvanula,
a tak je vracím. Dary nejbohatší
se mění v trety, když se dárce mračí.
Zde, Výsosti.
```

<small>(úryvek ze hry Hamlet, napsal W. Shakespeare, překlad E. A. Saudek)</small>


Tenhle text není moc přehledný, tak ho zkusíme poodsazovat, aby vypadal takhle:

```
Ofelie:
    Ach princi!
    Jak má se Vaše Výsost už tak dlouho?
Hamlet:
    Děkují poníženě: skvěle, skvěle, skvěle.
Ofelie:
    Mám od vás, princi, stále ještě dárky,
    Jež dávno toužím vrátit. Prosím vás,
    račte je přijmout teď.
atd.
```

Abys odsadil{{a}} jeden řádek, nastav kurzor na začátek řádku a stiskni
klávesu <kbd>Tab</kbd>.
Každým stisknutím řádek odsadíš o 4 mezery.

Odsadíš-li moc, pomocí <kbd>Shift</kbd>+<kbd>Tab</kbd> odsazení zmenšíš.

Chceš-li odsadit víc řádků najednou, všechny je vyber a stiskni <kbd>Tab</kbd>.
I výběr můžeš „od-odsadit“ pomocí <kbd>Shift</kbd>+<kbd>Tab</kbd>.


A to je vše! Teď máš nejen nastavený editor, ale umíš ho i používat.
