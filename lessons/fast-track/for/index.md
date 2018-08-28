# Cykly

Programátoři se neradi opakují.
Programování je o automatizaci: nebudeme zdravit každého člověka zvlášť,
vezměme seznam padesáti lidí a pozdravíme je všechny najednou!

(Hm, někteří programátoři nejsou moc sociálně nadaní.
Ale jinde se ta automatizace fakt hodí!)

Ještě si vzpomínáš na seznamy?
Udělej si seznam jmen:

```python
jmena = ['Rachel', 'Monica', 'Phoebe', 'Ola', 'Ty']
```

Udělejme program, který:

* Pro každé jméno ze seznamu jmen:
    * pozdraví daným jménem

V Pythonu se takový *cyklus* – opakování „pro každý prvek seznamu“ – píše
pomocí příkazu `for`:

``` python
for jmeno in jmena:
    pozdrav(jmeno)
```

Celý program bude tedy vypadat takto:

```python
def pozdrav(meno):
    print('Vitam ťa,', meno)

jmena = ['Rachel', 'Monica', 'Phoebe', 'Ola', 'Ty']
for jmeno in jmena:
    pozdrav(jmeno)
```

A když ho spustíme:

``` console
$ python3 python_intro.py
Vitam ťa, Rachel
Vitam ťa, Monica
Vitam ťa, Phoebe
Vitam ťa, Ola
Vitam ťa, Ty
```

Jak vidíš, vše, co jsi vložila dovnitř příkazu `for` s odsazením,
se zopakuje pro každý prvek seznamu `jmena`.

{# XXX: exercise? #}

## Opakuj <var>n</var>-krát

Cyklus `for` můžeš použít i s jinými hodnotami než se seznamy.

Často se používá s funkcí `range()`.
Když chceš něco 200-krát zopakovat, napiš:

```python
for i in range(200):
     print("Nebudu házet igelit do táboráku!")
```

Jak to funguje?
`for i in range(X)` se dá přeložit jako „pro každé číslo
od nuly do <var>X</var>“.
Do proměnné `i` Python uloží, pokolikáté cyklem prochází – počínaje,
v programátorském stylu, od nuly:

```python
for i in range(5):
     print(i)
```
```
0
1
2
3
4
```

`range` je funkce, která vytvoří seznam s posloupností čísel (tato čísla zadáváš jako parametry funkce).

Všimni si, že druhé z těchto dvou čísel není zahrnuto v seznamu, který je výstupem Pythonu (`range (1, 6)` počítá od 1 do 5, ale nezahrnuje číslo 6). To je proto, že "range" je z poloviny otevřený, čímž myslíme, že obsahuje první hodnotu, ale ne poslední.

## Shrnutí

A je to.
*Jsi naprosto skvěl{{gnd('ý', 'á')}}!*
Tohle byla složitá kapitola, takže bys na sebe měl{{a}} být hrd{{gnd('ý', 'á')}}.
My jsme na tebe velmi hrdí za to, že ses dostal{{a}} tak daleko!

Naučil{{a}} ses:

*   **Definice funkcí** – jak pojmenovat pár příkazů
*   **Cykly** – jak opakovat nějaký postup několikrát po sobě

Můžeš si jít krátce odpočinout – protáhnout se, projít se,
zavřít oči – než se pustíme do další kapitoly. :)

🧁

 {# XXX: range #}
