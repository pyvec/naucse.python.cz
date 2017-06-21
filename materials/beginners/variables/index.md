# Čtverec

Teď se vrátíme do základní školy a zkusíme si napsat program,
který vypočítá obsah a obvod čtverce, u kterého známe délku strany.

> [note] Matematika!
> Doufám, že tenhle příklad nikoho neodradí,
> ale „počítač“ je holt od slova *počítat*.
> Není třeba se děsit;
> na základy programování si vystačíme s matematickými
> znalostmi ze základní školy.

Pro připomenutí, obvod čtverce se stranou <var>a</var>
se dá vypočítat jako <var>O</var> = 4<var>a</var>
a obsah jako <var>S</var> = <var>a</var>².
Řekněme, že náš čtverec má stranu <var>a</var> = 356 cm.


{% if var('pyladies') -%}
{% set rootname = 'pyladies' %}
{%- else -%}
{% set rootname = 'naucse-python' %}
{%- endif %}

Výsledky vypiš pomocí `print()`.
Program ulož do <code><span class="pythondir">~/{{ rootname }}</span>/02/ctverec.py</code>
a spusť; mělo by se vypsat něco jako:

```
Obvod čtverce se stranou 356 cm je 1424 cm
Obsah čtverce se stranou 356 cm je 126736 cm2
```

Výsledky by měl samozřejmě spočítat Python; číslo 1424 nebo 126736 do programu nepiš.<br>
Jestli si nevíš rady, podívej se na program <code>printing.py</code>
z [lekce o `print`]({{ lesson_url('beginners/print') }}), kde jeden řádek dělá něco podobného.

{% filter solution %}
    Program, který vypíše správný výsledek, může vypadat třeba takhle:

    ```python
    print('Obvod čtverce se stranou 356 cm je', 4 * 356, 'cm')
    print('Obsah čtverce se stranou 356 cm je', 356 * 356, 'cm2')
    ```
{% endfilter %}


## Menší čtverec

Jestli všechno funguje, zkus změnit program tak,
aby počítal obsah a obvod čtverce o straně 123 cm.

{% filter solution %}
    ```python
    print('Obvod čtverce se stranou 123 cm je', 4 * 123, 'cm')
    print('Obsah čtverce se stranou 123 cm je', 123 * 123, 'cm2')
    ```
{% endfilter %}


## Proměnné

Zvládneš to i pro stranu 3945 cm, 832 cm, 956 cm?
Baví tě přepisování čísel?
Kdyby byl program delší (několikastránkový),
jak bys zajistil{{a}}, že jedno z těch čísel nepřehlédneš?

Existuje způsob, jak program napsat,
aniž bys musela pokaždé přepisovat všechna čísla:
stranu čtverce si „pojmenuješ“ a potom používáš jenom její jméno.
V Pythonu na pojmenovávání hodnot slouží *proměnné* (angl. *variables*).
Používají se takto:

```python
strana = 123
print('Obvod čtverce se stranou', strana, 'je', 4 * strana, 'cm')
print('Obsah čtverce se stranou', strana, 'je', strana * strana, 'cm2')
```

Neboli: napíšeš jméno, pak rovnítko a za rovnítkem výraz,
jehož hodnota se do proměnné *přiřadí*.
Když potom napíšeš jméno proměnné ve výrazu,
použije se zapamatovaná hodnota.

To nás vede k jedné ze základních programátorských
zásad: „neopakuj se“ (anglicky *Don't repeat yourself*, <abbr class="initialism">DRY</abbr>).
Když se někde opakuje stejná hodnota, stejný výraz
nebo stejný kus kódu,
{{ gnd('dobrý programátor', 'dobrá programátorka', both='dobrý programátor') }}
ten kus programu pojmenuje
a několikrát pak použije jen jméno.
Často se totiž stává, že je program potřeba změnit –
buď je v něm chyba nebo se změní zadání.
A potom je mnohem jednodušší změnu udělat jen na jednom místě.

Kromě toho dobrá jména usnadňují čtení programu:
`4 * strana` nepotřebuje komentář, ale
u `4 * 183` není příliš jasné, co ta čísla znamenají.


> [extra-activity]
>
> ## Kruhy
>
> *Tohle je příklad navíc! Klidně ho přeskoč.*
>
> Změna zadání!
> Zkus program doplnit tak, aby kromě čtverce počítal
> i obvod a obsah kruhu se stejným poloměrem,
> jakou má čtverec stranu.
>
> Pro připomenutí, obvod kruhu s poloměrem <var>r</var>
> je <var>o</var> = 2π<var>r</var>, obsah <var>S</var> = π<var>r</var>²
> a π je zhruba 3,1415926.
>
> Všechna čísla, která matematici označují jen jedním
> písmenkem (klidně řeckým), vhodně pojmenuj.


## Komentáře

Program si teď zpřehledníme *komentářem*.
V Pythonu komentář začíná dvojkřížkem (`#`),
za který můžeš napsat úplně cokoliv – až do konce
řádku bude Python všechno ignorovat.

Komentáře jsou důležité: programy nečte jen počítač, ale i lidé.
Do komentářů si můžeš poznamenat, co dělá celý program,
vysvětlit, jak funguje nějaká složitější část,
nebo vyjasnit něco, co není jasné přímo z programu.

Vždycky, když píšeš program, snaž se vžít do role někoho,
kdo potom ten program bude číst,
a všechno, co by mohlo být nejasné, upřesnit v komentářích.
(Nejčastěji to budeš číst {{ gnd('sám', 'sama') }}, třeba po několika měsících,
takže tím pomáháš {{ gnd('sám', 'sama') }} sobě!)

```python
# Tento program počítá obvod a obsah čtverce.

strana = 123  # v centimetrech
print('Obvod čtverce se stranou', strana, 'je', 4 * strana, 'cm')
print('Obsah čtverce se stranou', strana, 'je', strana * strana, 'cm2')
```

## Načítání vstupu

Nakonec se podíváme, jak zařídit, aby číslo nemuselo být
zapsáno v programu, ale aby ho mohl uživatel zadat sám.

Stejně jako když ses naučil{{a}} používat `print`
i tady jen řeknu, že na to použijeme *funkce*.
Detaily si vysvětlíme později;
pro teď to budou kouzelná zaříkadla:

* Chceš-li načíst **řetězec**, použij:

  ```python
  promenna = input('Zadej řetězec: ')
  ```

* Chceš-li načíst **celé číslo**, použij:

  ```python
  promenna = int(input('Zadej číslo: '))
  ```

* Chceš-li načíst **desetinné číslo**, použij:

  ```python
  promenna = float(input('Zadej číslo: '))
  ```

Místo řetězce `'Zadej …'` se dá napsat i jiná výzva. 
A výsledek se samozřejmě dá uložit i do jiné proměnné než `promenna`.

Hotový program může vypadat takto:

```python
# Tento program počítá obvod a obsah čtverce.

strana = float(input('Zadej stranu v centimetrech: '))
print('Obvod čtverce se stranou', strana, 'je', 4 * strana, 'cm')
print('Obsah čtverce se stranou', strana, 'je', strana * strana, 'cm2')
```
