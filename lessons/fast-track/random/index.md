# Náhoda

Občas je potřeba vybrat náhodnou hodnotu.
Na to není v Pythonu funkce k dispozici přímo, ale dá se zpřístupnit
pomocí příkazu `import`"

```pycon
>>> from random import randrange
>>> randrange(6)
3
```

Neboli:

* Z modulu `random` (který obsahuje funkce kolem náhodných hodnot)
  zpřístupni funkci `randrange` (která umí vybírat náhodná čísla).
* Vyber náhodné číslo ze šesti možností.

Volání funkce `randrange` několikrát opakuj.
Jaká čísla můžeš dostat?

{% filter solution %}
Čísla od 0 do 5 – šestku ne.
Programátoři totiž počítají od nuly, a když počítáš od nuly a chceš šest čísel, dostaneš se jen k pětce.
{% endfilter %}

Modulů jako `random`, ze kterých se dají *naimportovat* užitečná rozšiření,
je spousta – na práci s textem, kreslení obrázků, práci se soubory nebo dny
v kalendáři, kompresi dat, posílání e-mailů, stahování z internetu…
Stačí jen vědět (nebo umět najít), jak se ten správný modul a funkce jmenuje.
A kdyby nestačilo to, co má Python zabudované v sobě, další rozšiřující moduly
se dají doinstalovat.

## Náhodný výběr

Když už jsme u náhody, zkusme si ještě vylosovat náhodné číslo v loterii.
Na výběr ze seznamu má modul `random` funkci `choice`:

```pycon
>>> from random import choice
>>> loterie = [3, 42, 12, 19, 30, 59]
>>> choice(loterie)
12
```

Podobně se dá vybrat náhodná karta z ruky, náhodný účastník kurzu,
náhodná barva – cokoli, co umíš dát do seznamu.


## Shrnutí

* Příkaz **import** ti dá k dispozici funkčnost, která není k dispozici přímo
  v Pythonu.
* Modul **random** obsahuje funkce **randrange** (náhodné číslo) a **choice**
  (náhodný prvek seznamu).
