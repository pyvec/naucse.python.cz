# První program

```pycon
>>> 3 + 4
7
```

Psaní příkazů přímo v Pythonu, <em>interaktivně</em>,
má jednu velkou nevýhodu:
to, co napíšeš, se ztratí, jakmile zavřeš okno příkazové řádky.
Na jednoduché výpočty to nevadí, ale až budou tvoje programy složitější,
budeš je potřebovat nějak uložit.

Otevři editor
(Ten bys měl{{a}} mít nainstalovaný, jestli ne, instrukce jsou v [předchozí
lekci]({{ lesson_url('beginners/install-editor') }}).)

V něm vytvoř nový soubor, do kterého napiš následující text:

```python
print("Ahoj světe!")
```

{% if var('pyladies') -%}
{% set rootname = 'pyladies' %}
{%- else -%}
{% set rootname = 'naucse-python' %}
{%- endif %}

Pak soubor ulož pod jménem <code><span class="pythondir">~/{{ rootname }}</span>/02/ahoj.py</code>.
Za <code class="pythondir">~/{{ rootname }}</code> musíš doplnit adresář,
který jsi vytvořil{{a}} minule. Podadresář `02` musíš vytvořit.
Do něj pak soubor ulož jako `ahoj.py`.

Pokud máš v ukládacím okýnku možnost zvolit <em>kódování</em>, zvol <code>UTF-8</code>.
Můžeš–li zvolit typ souboru, zvol <code>.py</code> nebo „všechny soubory“.


Některé systémy a editory se snaží přípony jako <code>.py</code> schovávat
nebo si doplňovat přípony vlastní. V příkazové řádce se ale vždycky ukáže
opravdové jméno.
Proto ještě v příkazové řádce pomocí `cd` přejdi do adresáře <code><span class="pythondir">~/{{ rootname }}</span>/02</code>
a pomocí `ls` (Unix) nebo `dir` (Windows) zkontroluj, že se soubor opravdu
jmenuje `ahoj.py` a ne třeba `ahoj.py.txt`.


## Spuštění

Aktivuj si virtuální prostředí,
vlez do adresáře <code><span class="pythondir">~/{{ rootname }}</span>/02</code>
a zadej tento příkaz:

```console
$ python ahoj.py
```

> [note] Poznámka pro Windows a starší Python
> V nečeských Windows s Pythonem 3.5 či nižším bude třeba před
> programem spustit `chcp 1250`, jinak bude program píšící české
> znaky končit chybou `UnicodeEncodeError`.
> Je to trochu polovičaté řešení, ale pro naše příklady bude stačit.

Pokud se vypíše hláška, gratuluji!
Napsal{{a}} jsi svůj první program v Pythonu!

Jestli to nefunguje, zkontroluj, že:

* Máš zapnuté virtuální prostředí.
  (Na příkazové řádce se musí ukazovat <code>(venv)</code>;
  pokud tam není, použij příkaz „activate“ z [minula]({{ lesson_url('beginners/install') }}).)
* Jsi ve správném adresáři, <code><span class="pythondir">~/{{ rootname }}</span>/02</code>.
  (Za <span class="pythondir">~/{{ rootname }}</span> musíš doplnit adresář, který jsi vytvořila minule.)
* Soubor `ahoj.py` obsahuje správný příkaz, včetně všech uvozovek a závorek.
* Znak `$` nezadáváš – ten je tam proto, aby bylo poznat že jde o příkaz příkazové
  řádky.
  Na `$` (nebo, na Windows, `>`) končí dotaz, který vypíše počítač.
  Příkaz, který zadáváš ty, je jen `python ahoj.py`.

A jestli to pořád nefunguje, zeptej se
{% if var('coach-present') -%}
kouče.
{%- else -%}
zkušenějšího programátora. <!-- XXX: where to direct people? -->
{% endif %}

