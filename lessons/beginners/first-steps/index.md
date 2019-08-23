# Interaktivní režim Pythonu

Chceš-li si začít hrát s Pythonem, otevři *příkazový řádek* a aktivuj virtuální prostředí.
Zkontroluj si, že ti na začátku příkazové řádky svítí `(venv)`.

Je-li tomu tak, nezbývá než – konečně – pustit Python. K tomu použij příkaz `python`:

``` console
$ python
Python 3.6.6 (...)
Type "help", "copyright", "credits" or "license" for more information.
>>>
```

Příkaz vypíše několik informací. Z prvního řádku se můžeš ujistit, že používáš Python 3.
(Verze by měla být `3.6` nebo vyšší. Vidíš-li číslo jako `2.7.11`, něco je špatně – popros o radu kouče.)
Další řádek je informační: Python má k dispozici návody a informace sám o sobě,
ale jsou psané v angličtině a pro trochu pokročilejší publikum.

Třemi „zobáčky“ `>>>` pak Python poprosí o instrukce.
Je to jako v příkazové řádce, ale místo příkazů jako `cd` a `mkdir` sem budeš psát příkazy Pythonu.

Příkazy z příkazové řádky v Pythonu nefungují,
ačkoli okýnko vypadá skoro stejně.
Vyzkoušej si to. Za „zobáčky“ napiš `whoami` a zmáčkni Enter:

```pycon
>>> whoami
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
NameError: name 'whoami' is not defined
```

Tohle je *chybová hláška*, která se objeví vždycky,
když Python nebude spokojený.
V průběhu kurzu jich uvidíš ještě spoustu,
takže si ji dobře prohlédni, ať ji příště poznáš.

## První příkaz

Třemi „zobáčky“ `>>>` Python prosí o instrukce.
Pojď mu nějakou dát!

Ze začátku použij Pythonu jako kalkulačku.
Za tři zobáčky napiš třeba `2 + 3` a zmáčkni <kbd>Enter</kbd>.

``` pycon
>>> 2 + 3
5
```

> [note]
> Zobáčky `>>>` i odpověď vypisuje sám Python!
> {{ gnd('sám', 'sama') }} zadej jen číslo a Enter.

Zobrazila se ti správná odpověď?
Pokud ano, gratuluji! První příkaz v Pythonu máš za sebou.

Zkusíš i odečítání?

A jak je to s násobením?
Na kalkulačce bys zadal{{a}} `4 × 5`, což se na klávesnici píše špatně.
Python proto používá symbol `*`.

``` pycon
>>> 4 * 5
20
```

Symboly jako `+` a `*` se odborně nazývají *operátory*.

Operátor pro dělení je `/` – jako u násobení, znak `÷` by se psal špatně.

Při dělení může vzniknout necelé číslo, třeba dva a půl.
Python používá desetinnou *tečku*, ukáže se tedy `2.5`:

``` python
>>> 5 / 2
2.5
```

Z důvodů, do kterých teď nebudeme zabíhat, se při dělení desetinná tečka
objeví, i když vyjde číslo celé:
``` pycon
>>> 4 / 2
2.0
```

Občas se hodí použít dělení se zbytkem, kdy výsledek zůstane jako celé číslo.
Na to má Python operátory `//` (podíl) a `%` (zbytek):

``` pycon
>>> 5 // 2
2
>>> 5 % 2
1
```

> [style-note]
> Mezery mezi čísly a znamínkem nejsou nutné: `4*5` i `4       * 5` dělá
> to samé co `4 * 5`.
> Je ale zvykem psát kolem operátoru jednu mezeru z každé strany – tak jako
> v těchto materiálech.
> Kód je pak čitelnější.


### Ukončení

Pokud ses dostal{{a}} až sem, gratuluji!
Python máš nejen nainstalovaný, ale taky ti funguje.
Stačí ho už jen zavřít a pak opustit i samotnou příkazovou řádku.
V Pythonu se to dělá pomocí `quit()`, s prázdnými závorkami na konci.

<div class="highlight"><pre>
<span class="gp">&gt;&gt;&gt;</span> quit()
<span class="gp">(venv)$</span>
</pre></div>

Zobáčky `>>>` se změnily na výzvu
příkazové řádky, která začíná `(venv)` a končí `$` nebo `>`.
Teď fungují příkazy jako `whoami` a `cd`, ale příkazy Pythonu
jako `1 + 2` fungovat nebudou, dokud Python opět nepustíš pomocí
příkazu `python`.

Ukončit virtuální prostředí můžeš příkazem `deactivate` –
tentokrát bez závorek.

```console
(venv)$ deactivate
```

Příkazovou řádku můžeš nakonec zavřít příkazem `exit`.

```console
$ exit
```

Pro cvik si zkus Python znovu spustit – nejdřív otevři příkazovou řádku,
pak aktivuj virtuální prostředí, potom spusť Python samotný.
