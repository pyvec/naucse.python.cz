{% set editor_name = 'MU' %}
{% set editor_url = 'https://codewith.mu/en/download' %}
{% extends lesson.slug + '/_base.md' %}

{% block name_gen %} Mu {% endblock %}

{% block install %} 
Na Windows
si stáhni {{ editor_name }} z jeho [domovské stránky]({{ editor_url }})
a nainstaluj. Použij 64-bitovou nebo 32-bitovou verzi, stejně jako v případě Pythonu.

Na Linuxu se Mu instaluje přes `pip`, který je součástí Pythonu.
```console
$ python -m pip install mu-editor
```
Editor pak můžeš spustit z příkazové řádky
```console
$ mu-editor
```
nebo si vyrobit zkratku.
```console
$ shortcut mu-editor
```
Zkratka se vytvoří ve složce, ve které se právě nacházíš, poté ji můžeš přesunout kam chceš.
K jejímu vytvoření je třeba balík `shortcut`, ten se dá naistalovat opět pomocí pipu.
```console
$ python -m pip install shortcut
```


{% endblock %}

{% block setup %}
Při prvním spuštění vyber mód Python.

{{ figure(img=static('mu-mode.png'), alt="Mu run") }}

Jinak se v Mu nemusí nic nastavovat, ani to moc nejde, funguje „z výroby“ jednoduše tak, jak má.

Odsazování a obarvování bude fungovat správně jen v souborech s koncovkou `.py`
(jako Python).
V jiných programovacích jazycích se totiž odsazuje i obarvuje jinak.

Proto jakmile v tomhle editoru vytvoříš nový soubor,
měl{{a}} bys ho co nejdřív uložit pod správným jménem.

## Spouštění programů
Mu není jen obyčejný editor pro psaní kódu, umí programy v Pythonu i spouštět, stačí kliknout a tlačítko Run a
kód, který máš právě otevřený se spustí, v dolní části okna se objeví výstup. Více si ukážeme na lekci.

{{ figure(img=static('mu-run.png'), alt="Mu run") }}

## Kontrola stylu zdrojového kódu

Tak jako čeština má Python typografická pravidla.
Například za čárkou se píše mezera, ale před ní ne.
Jsou nepovinná, program bude fungovat i při jejich nedodržení,
ale pomáhají psát přehledný kód, tak je dobré je dodržovat už od začátku.
Pravidla pro Python jsou popsána v dokumentu
[PEP8](https://www.python.org/dev/peps/pep-0008/).

Aby sis je nemusel{{a}} všechny pamatovat a postupně si na ně zvykla provádí kontrolu Mu za tebe.
Stačí kliknout na ikonku zdviženého palce a Mu ti zkoukne kód a řekne, kde není správně upravený.

{{ figure(img=static('mu-syntax-check.png'), alt="Mu syntax chceck") }}



{% endblock %}


