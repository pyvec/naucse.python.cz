# Převádění typů

Pojď zkusit něco nového: zjistit délku čísla stejným způsobem,
jakým jsi zjišťoval{{a}} délku svého jména.
Zadej `len(304023)` a stiskni <kbd>Enter</kbd>:

``` pycon
>>> len(304023)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: object of type 'int' has no len()
```

Zobrazila se ti chyba!
Ta říká, že objekty typu `int` (zkratka anglického *integer*, celé číslo)
nemají délku.
Co můžeš udělat teď?
Možná můžeš zkusit napsat číslo jako řetězec?
Řetězce mají délku, že?

```pycon
>>> len("304023")
6
```

Jde to ale i bez uvozovek
Existuje i funkce, která *převede* číslo na řetězec.
Jmenuje se `str`:

```pycon
>>> str(304023)
"304023"
>>> len(str(304023))
6
```

Když zadáváš číslo přímo, bude asi příjemnější použít uvozovky.
Funkce `str` ale začne být užitečnější až budeš chtít výpočet
čísla přenechat Pythonu:

```pycon
>>> str(304023 * 12345 * 83845)
'314684030130075'
>>> len(str(304023 * 12345 * 83845))
15
```

Podobně jako `str` převádí na řetězce, funkce `int` převádí věci na celá čísla:

```pycon
>>> int("304023")
```

Číslo na text můžeš převést vždy, ale naopak to vždy nejde.
Co se stane, když se pokusíš na číslo převést řetězec bez
číslic – třeba `'ahoj'`?

{% filter solution() %}
Nastane chyba!

``` pycon
>>> int('ahoj')
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
ValueError: invalid literal for int() with base 10: 'ahoj'
```

Hláška obsahuje užitečné informace, i když je k nim potřeba angličtina
a pokročilejší znalost (infor)matiky.
V doslovnějším překladu hláška zní *Chyba hodnoty: špatný zápis celého čísla
v desítkové soustavě: `'ahoj'`*.
Důležité je ale hlavně to `ValueError`, chyba hodnoty.
{% endfilter %}
