# Slovníky

Jiný typ hodnot, které v sobě mohou obsahovat další hodnoty, je *slovník*.
Pro příklad si představ překladový slovník, třeba tenhle česko-anglický:

* **Jablko**: Apple
* **Knoflík**: Button
* **Myš**: Mouse

Slovník v Pythonu obsahuje záznamy, a každý záznam přiřazuje
nějakému *klíči* nějakou *hodnotu*.
V našem příkladu je klíči *Jablko* přiřazena hodnota *Apple*,
klíči *Knoflík* náleží hodnota *Button*
a klíč *Myš* ukazuje na *Mouse*.

V Pythonu by se takový slovník napsal následovně:

``` pycon
>>> slovnik = {'Jablko': 'Apple', 'Knoflík': 'Button', 'Myš': 'Mouse'}
```

Naše klíče a hodnoty jsou slova – krátké texty, tedy řetězce,
které je potřeba dát do uvozovek.
Každý klíč je od své hodnoty oddělený dvojtečkou,
jednotlivé dvojice se od sebe oddělují čárkou,
a celý slovník je uzavřený ve složených závorkách.

Když budeš chtít v takovém slovníku něco najít, potřebuješ vědět co hledat.
Potřebuješ *klíč*.
Pomocí hranatých závorek můžeš zjistit hodnotu, která danému klíči odpovídá:


``` pycon
>>> slovnik['Jablko']
'Apple'
```

Je to podobné jako u seznamů, jen v hranatých závorkách není index
(pořadí prvku) nebo rozmezí s dvojtečkou, ale právě klíč.

> [note]
> Naopak to nejde – slovník neumožňuje podle hodnoty přímo zjistit klíč.
> Na překlad z angličtiny do češtiny bys potřeboval{{a}} druhý slovník.

## Měnění slovníků

Co se stane, když klíč ve slovníku není?

``` pycon
>>> slovnik['Pes']
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
KeyError: 'Pes'
```

Python si postěžuje na `KeyError` – chybu klíče.

Podobně jako seznamy se ale slovníky dají měnit.
Nový záznam vytvoříš takhle:

``` pycon
>>> slovnik['Pes'] = 'Dog'
>>> slovnik
{'Jablko': 'Apple', 'Knoflík': 'Button', 'Myš': 'Mouse', 'Pes': 'Dog'}
```

> [note]
> Na rozdíl od překladového slovníku nemusí být Pythonní slovník seřazený
> podle abecedy.
> Není to potřeba, počítač umí rychle vyhledávat i bez seřazení.

Kdybys potřebovala{{a}} změnit už existující záznam, použij stejný příkaz.
K jednomu klíči může patřit jen jedna hodnota.

``` pycon
>>> slovnik['Pes'] = 'Extension cord'
>>> slovnik
{'Jablko': 'Apple', 'Knoflík': 'Button', 'Myš': 'Mouse', 'Pes': 'Extension cord'}
```

{# XXX: Zmínit se o nehomogenních slovnících? #}

Chceš-li ze zlovníku nějaký záznam smazat, dělá se to podobně jako
u seznamů příkazem `del`:

``` pycon
>>> del slovnik['Pes']
>>> slovnik
{'Jablko': 'Apple', 'Knoflík': 'Button', 'Myš': 'Mouse'}
```

A když budeš chtít zjistit, kolik je ve slovníku záznamů,
zeptáš se podobně jako na počet znaků řetězce nebo prvků seznamu.
Použiješ funkci `len()`.

``` pycon
>>> len(slovnik)
3
```

{# XXX

* Kontakty
* Když číslo není číslo
* Více čísel

## K zamyšlení

Ke každému klíči může patřit jen jedna hodnota.
Jak bys zařídil{{a}}, aby hodnot víc?

Zkus do Pythonní proměnné uložit tyto kontakty:

* Katka:
    * 4925219
* Jirka:
    * 7477058
    * 3251156
* Verča:
    * 1019103

{% filter solution %}
Více hodnot se dá uložit do seznamu.
Hodnoty budou seznamy čísel:

```pycon
>>> kontakty = {'Katka': ['4925219'], 'Jirka': ['7477058', '3251156'], 'Verča': ['1019103']}
```
{% endfilter %}

Verča se přestěhovala do zahraničí a má nové číslo: `+897 3788509`.

#}

## Shrnutí

Skvělé! Co víš o slovnících:

* **Záznam** se skládá z **klíče** a **hodnoty**.
* Ve slovníku se hledá pomocí **klíče**.
* Záznamy se dají přepsat, přidat, nebo pomocí `del` smazat.

Jsi připraven{{a}} na další část?
