# Interaktivní režim Pythonu

Chceš-li si začít hrát s Pythonem, otevři *příkazový řádek* a aktivuj virtuální prostředí.  Zkontroluj si, že na začátku příkazové řádky ti svítí `(venv)`.

Je-li tomu tak, nezbývá než – konečně – pustit Python. K tomu použij příkaz `python`:

``` console
$ python
Python 3.6.6 (...)
Type "help", "copyright", "credits" or "license" for more information.
>>>
```

Příkaz vypíše několik informací. Z prvního řádku se můžeš ujistit, že používáš Python 3. (Vidíš-li číslo jako `2.7.11`, něco je špatně – popros o radu kouče.)

Třemi „zobáčky“ ``>>>` pak Python poprosí o instrukce. Je to jako v příkazové řádce, ale místo příkazů jako `cd` a `mkdir` sem budeš psát příkazy Pythonu.

Jako první instrukci použijeme Pythonu jako kalkulačku.
Za tři zobáčky napiš třeba `2 + 3` a zmáčkni <kbd>Enter</kbd>.

``` pycon
>>> 2 + 3
5
```

Zobrazila se ti správná odpověď?
Pokud ano, gratuluji! První příkaz v Pythonu máš za sebou.

Zkusíš i odečítání?

A jak je to s násobením?
{# XXX: Jak zapsat násobení? `4 x 5` `4 . 5` `4 × 5` `4 * 5` -#}
Na kalkulačce bys zadala `4 × 5`, což se na klávesnici píše špatně.
Python proto používá symbol `*`.

``` pycon
>>> 4 * 5
20
```

Symboly jako `+` a `*` se odborně nazývají *operátory*.

Operátor pro dělení je `/`.

Při dělení může vzniknout necelé číslo, třeba dva a půl.
Python používá desetinnou *tečku*, ukáže se tedy `2.5`:

``` python
>>> 5 / 2
2.5
```

Z důvodů, do kterých teď nebudeme zabíhat, se při dělení desetinná tečka
objeví i když vyjde číslo celé:
``` pycon
>>> 4 / 2
2.0
```

Občas se hodí použít dělení se zbytkem.
Výsledek tak zůstane jako celé číslo.
Na to má Python operátory `//` (podíl) a `%` (zbytek):

``` pycon
>>> 5 // 2
2
>>> 5 % 2
1
```


{# XXX:
Kolik je
<math mode="display" style="display:inline-box;" xmlns="http://www.w3.org/1998/Math/MathML"><mfrac><mrow><mn>123</mn> + <mn>456</mn></mrow><mrow><mn>789</mn></mrow></mfrac></math>?
#}

> [style-note]
> Mezery mezi čísly a znamínkem nejsou nutné: `4*5` i `4       * 5` dělá
> to samé co `4 * 5`.
> Je ale zvykem psát kolem operátoru jednu mezeru z každé strany – tak jako
> v těchto materiálech.
> Kód je pak čitelnější.


### Shrnutí

Co ses zatím naučil{{a}}?

*   **Interaktivní režim Pythonu** umožňuje zadávat příkazy (kód) pro
    Python a zobrazuje výsledky/odpovědi.
*   **Čísla** se používají na matematiku a práci s textem.
*   **Operátor** jako `+` a `*` kombinuje hodnoty a vytvoří výsledek.
