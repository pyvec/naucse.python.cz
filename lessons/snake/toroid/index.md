# Nekonečná klec

Místo konce hry při naražení do okraje okýnka můžeš nechat hada „projít“
a objevit se na druhé straně.

Z pohledu logiky hry to není tak složité, jak to může znít.
Stačí v `move` místo ukončení hry správně nastavit příslušnou hodnotu.
Je ale potřeba si dát pozor kde použít `new_x` a kde `new_y`, kde `width` a kde
`height`, a kde přičíst nebo odečíst jedničku, aby při číslování od nuly
všechno sedělo.
Zkus to!

{% filter solution %}
```python
        # Kontrola vylezení z hrací plochy
        if new_x < 0:
            new_x = self.width - 1
        if new_y < 0:
            new_y = self.height - 1
        if new_x >= self.width:
            new_x = 0
        if new_y >= self.height:
            new_y = 0
```
{% endfilter %}

Jestli ale vykresluješ hada (místo housenky), narazíš teď na problém
s vybíráním správných dílků – okraj herní plochy hada vizuálně rozdělí
na dva menší.
Řešení tohoto problému nechávám na čtenáři – s tím, že je to hodně těžký
problém.


## Zbytkové řešení

Jde logiku vylázání z okýnka vyřešit jednodušeji? Jde!
Matematikové vymysleli operaci, která se jmenuje *zbytek po dělení*.
Ta dělá přesně to, co tu potřebuješ – zbytek po dělení nové souřadnice velikostí
hřiště dá souřadnici, která leží v hřišti.
Když byla předchozí souřadnice o jedna větší než maximum,
zbytek po dělení bude nula; když byla -1, dostaneme maximum.

Python moužívá pro zbytek po dělení operátor `%`. Zkus si to:

``` pycon
>>> 6 % 10      # Zbytek po dělení šesti desíti
6
>>> 10 % 10
0
>>> -1 % 10
9
```

Celý kód pro kontrolu a ošetření vylézání z hrací plochy tak jde
nahradit dvěma řádky:

```python
        new_x = new_x % self.width
        new_y = new_y % self.height
```

Podobné matematické „zkratky“ umí programátorům často usnadnit život.
Jen přijít na ně nebývá jednoduché.
Ale nevěš hlavu: neláká-li tě studovat informatiku na škole, věz, že to jde
i bez „zkratek“. Jen občas trochu krkoloměji.

> [note]
> To, že existuje přesně operace kterou potřebujeme, není až tak úplně náhoda.
> Ona matematická jednoduchost je spíš  *důvod*, proč se hrací plocha
> u spousty starých her chová právě takhle.
> Odborně se tomu „takhle“ říká
> [toroidální topologie](https://en.wikipedia.org/wiki/Torus#Topology).

> [note] Pro matematiky
> Zkušení matematici si teď možná stěžují na nutnost definovat zbytek po
> dělení záporným číslem. Proto dodám, že ho Python schválně
> [definuje vhodně](https://docs.python.org/3/reference/expressions.html#binary-arithmetic-operations)
> pro tento účel; `a % b` má vždy stejné znaménko jako `b`.


{# XXX

## Vykreslování

> Volné chvilce se pokus problém opravit.
> Doporučuji se vrátit k „abstraktní“ funkci, která jen vypisuje souřadnice
> a směry:
>
> ```
> 1 2 tail right
> 2 2 left right
> 3 2 left top
> 3 3 bottom top
> 3 4 bottom top
> 3 5 bottom right
> 4 5 left head
> ```
> Jdeš-li podle návodu, tuhle funkci máš uloženou v souboru `smery.py`
> Oprav nejdřív tu, a řešení „transplantuj“ do hry.
#}

