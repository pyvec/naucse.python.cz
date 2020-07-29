# Rekurze

*Rekurze* (angl. *recursion*) je programátorská technika,
kdy funkce volá sebe sama.

Taková rekurze skončí nekonečným voláním.
Když zadáš tento program:

```python
def rekurzivni_funkce():
    vysledek = ...
    rekurzivni_funkce()
    return vysledek

rekurzivni_funkce()
```

Jak to funguje?

* Python si nadefinuje funkci `rekurzivni_funkce`
* Zavolá funkci `rekurzivni_funkce`:
  * Vypočítá výsledek
  * Zavolá funkci `rekurzivni_funkce`:
    * Vypočítá výsledek
    * Zavolá funkci `rekurzivni_funkce`:
      * Vypočítá výsledek
      * Zavolá funkci `rekurzivni_funkce`:
        * Vypočítá výsledek
        * Zavolá funkci `rekurzivni_funkce`:
          * ...
            * ...
               * po stovkách opakování si Python všimne, že tohle asi
                 nikam nevede, a skončí s chybou.

Tomu odpovídá chybová hláška:

```
Traceback (most recent call last):
  File "/tmp/ukazka.py", line 4, in <module>
    rekurzivni_funkce()
  File "/tmp/ukazka.py", line 2, in rekurzivni_funkce
    return rekurzivni_funkce()
  File "/tmp/ukazka.py", line 2, in rekurzivni_funkce
    return rekurzivni_funkce()
  File "/tmp/ukazka.py", line 2, in rekurzivni_funkce
    return rekurzivni_funkce()
  [Previous line repeated 996 more times]
RecursionError: maximum recursion depth exceeded
```

Hláška je zkrácená – dva řádky by se správně měly opakovat 999×, ale novější
verze Pythonu je vypíšou jen třikrát.


# Kontrolované zanoření

Jak rekurzi využít v praxi?
Jeden způsob je si počítat, kolikrát se ještě „zanořit“.

Představ si potápěče, který prozkoumává mořské hlubiny následujícím způsobem:

* Jak *„prozkoumat moře“* v určité hloubce:
  * Porozhlédnu se kolem
  * Jsem-li už teď moc hluboko, kašlu na to; nebudu prozkoumávat dál.
  * Jinak:
    * Zanořím se o 10 m níž
    * *Prozkoumám moře* v nové hloubce
    * Zase se o 10 m vynořím

Neboli v Pythonu:

```python
def pruzkum(hloubka):
    print(f'Rozhlížím se v hloubce {hloubka} m')

    if hloubka >= 30:
        print('Už toho bylo dost!')
    else:
        print(f'Zanořuju se (z {hloubka} m)')

        pruzkum(hloubka + 10)

        print(f'Vynořuju se (na {hloubka} m)')

pruzkum(0)
```

* Python si nadefinuje funkci `pruzkum`
* Zavolá funkci `pruzkum` s hloubkou 0:
  * Vypíše `Rozhlížím se v hloubce 0 m`
  * Zkontroluje, že `0 ≥ 30` (což neplatí)
  * Vypíše `Zanořuju se (z 0 m)`
  * Zavolá funkci `pruzkum` s hloubkou 10 m:
    * Vypíše `Rozhlížím se v hloubce 10 m`
    * Zkontroluje, že `10 ≥ 30` (což neplatí)
    * Vypíše `Zanořuju se (na 10 m)`
    * Zavolá funkci `pruzkum` s hloubkou 20 m:
      * Zkontroluje, že `20 ≥ 30` (což neplatí)
      * Vypíše `Zanořuju se (na 20 m)`
        * Zavolá funkci `pruzkum` s hloubkou 30 m:
          * Zkontroluje, že `30 ≥ 30` (což platí! konečně!)
            * Vypíše `Už toho bylo dost!`
            * a skončí
      * Vypíše `Vynořuju se (na 20 m)`
    * Vypíše `Vynořuju se (na 10 m)`
  * Vypíše `Vynořuju se (na 0 m)`


# Lokální proměnné

Na předchozím příkladu je vidět zajímavé chování lokálních proměnných.
Když je potápěč „na dně“, jakou hodnotu má proměnná *hloubka*?

Tahle otázka je chyták. *Která* proměnná `hloubka`?
Když je program „na dně“, existují čtyři *různé* lokální proměnné `hloubka`:
každé zanoření, každé zavolání funkce `pruzkum`, má vlastní proměnnou.

Podobně jako když máš globální a lokální proměnnou stejného jména,
každá funkce „vidí“ jen tu svoji proměnnou.
Ale když se potápěč vynoří a volání funkce se ukončí, tato proměnná
přestane existovat.
A „volající“ funkce vidí svoji proměnnou, ve které je stále původní hodnota.


# Pro matematiky

> [note]
> Nemáš-li rád{{a}} matematiku, tuhle sekci přeskoč!

Rekurzivní algoritmy mají původ v matematice. Faktoriál <var>x</var>, neboli
součin všech  čísel od 1 do <var>x</var>, zapsaný jako <var>x</var>!,
matematici definují takto:

* 0! = 1
* Pro kladná <var>x</var> je <var>x</var>! = <var>x</var> · (<var>x</var> - 1)!

Neboli v Pythonu:

```python
def factorial(x):
    if x == 0:
        return 1
    elif x > 0:
        return x * factorial(x - 1)

print(factorial(5))
print(1 * 2 * 3 * 4 * 5)
```
