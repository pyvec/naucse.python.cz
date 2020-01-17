# Vylepšení ovládání Hada

Možná si všimneš, zvlášť jestli jsi už nějakou verzi hada hrál{{a}},
že ovládání tvé nové hry je trošku frustrující.
A možná není úplně jednoduché přijít na to, proč.

Můžou za to (hlavně) dva důvody:

1. Když zmáčkneš dvě šipky rychle za sebou, v dalším „tahu“
   hada se projeví jen ta druhá.
2. Když se had plazí doleva a hráč zmáčkne šipku doprava,
   had se otočí a hlavou si narazí do krku.

Pojďme je vyřešit.

## Fronta pokynů

Když zmáčkneš dvě šipky rychle za sebou, v dalším „tahu“ hada se projeví jen
ta druhá.

Z pohledu programu to chování dává smysl – po stisknutí šipky se uloží
její směr, a při „tahu“ hada se použije poslední uložený směr.
S tímhle chováním je ale složité hada rychle otáčet: hráč si musí pohlídat,
aby pro každý „tah“ hada nezmáčkl víc než jednu šipku.
Lepší by bylo, kdyby se ukládaly *všechny* stisknuté klávesy, a had by
v každém tahu reagoval maximálně jednu.
Další by si „schoval“ na další tahy.

Takovou „frontu“ stisků kláves lze uchovávat v seznamu.
Přidej si na to do stavu hry seznam (v metodě `__init__`):

```python
        self.queued_directions = []
```

Tuhle frontu plň po každém stisku klávesy, metodou `append`.
Je potřeba změnit většinu funkce `on_key_press` – místo změny
atributu se nový směr přidá do seznamu.
Abys nemusel{{a}} psát čtyřikrát `append`,
můžeš uložit nový směr do pomocné proměnné:

```python
@window.event
def on_key_press(key_code, modifier):
    if key_code == pyglet.window.key.LEFT:
        new_direction = -1, 0
    if key_code == pyglet.window.key.RIGHT:
        new_direction = 1, 0
    if key_code == pyglet.window.key.DOWN:
        new_direction = 0, -1
    if key_code == pyglet.window.key.UP:
        new_direction = 0, 1
    state.queued_directions.append(new_direction)
```

A zpátky k logice. V metodě `move` místo
`dir_x, dir_y = self.snake_direction` z fronty vyber první nepoužitý prvek.
Nezapomeň ho pak z fronty smazat, ať se dostane i na další:

```python
        if self.queued_directions:
            new_direction = self.queued_directions[0]
            del self.queued_directions[0]
            self.snake_direction = new_direction
```

Zkontroluj, že to funguje.

### Zpátky ni krok

Když hráč zmáčkne šipku opačného směru, než se had právě plazí, had se otočí a 
hlavou si narazí do krku.

Z pohledu programu to opět dává smysl: plazí-li se had doleva,
políčko napravo od hlavy je plné.
Když tedy had začne plazit doprava, narazí na políčko s hadem a hráč prohrává.
Z pohledu hry (a biologie!) ale narážení do krku moc smyslu nedává.
Lepší by bylo obrácení směru úplně ignorovat.

A jak poznat opačný směr?
Když se had plazí doprava, `(1, 0)`, tak je opačný směr doleva, `(-1, 0)`.
Když se plazí dolů, `(0, -1)`, tak naopak je nahoru, `(0, 1)`.
Obecně, k (<var>x</var>, <var>y</var>) je opačný směr
(-<var>x</var>, -<var>y</var>).

Zatím ale pracujeme s celými <var>n</var>-ticemi, takže je potřeba obě
na <var>x</var> a <var>y</var> „rozbalit“.
Kód tedy bude vypadat takto:

```python
            old_x, old_y = self.snake_direction
            new_x, new_y = new_direction
            if (old_x, old_y) != (-new_x, -new_y):
                self.snake_direction = new_direction
```

Dej ho místo puvodního `self.snake_direction = new_direction`.
