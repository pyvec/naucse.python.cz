# Převádění typů

Pojď zkusit něco nového: zjistit délku čísla stejným způsobem,
jakým jsme zjišťovali délku našeho jména.
Zadej `len(304023)` a stiskni <kbd>Enter</kbd>:

``` pycon
>>> len(304023)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: object of type 'int' has no len()
```

{# XXX: tohle nebude první chyba... #}
Zobrazila se ti naše první chyba!
Ta říká, že objekty typu `int` (zkratka anglického *integer*, celé číslo)
nemají délku.
Tak co můžeme udělat teď?
Možná můžeme zkusit napsat naše číslo jako řetězec?
Řetězce mají délku, že?

```pycon
>>> len("304023")
6
```

Existuje i funkce, která *převede* číslo na řetězec. Jmenuje se `str`:

```pycon
>>> str(304023)
"304023"
>>> len(str(304023))
6
```

Podobně funkce `int` převádí věci na celá čísla:

```pycon
>>> int("304023")
```

Můžeš převést čísla na text, ale nemůžeš jen tak převést text na čísla.
Co by se stalo, kdyby ses pokusil{{a}} na číslo převést řetězec, ve kterém
nejsou číslice?

{% filter solution() %}
Nastane chyba!

``` pycon
>>> int('hello')
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
ValueError: invalid literal for int() with base 10: 'ahoj'
```
{% endfilter %}
