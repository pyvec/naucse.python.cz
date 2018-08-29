## První příkazy v Pythonu

Pojďme si vyzkoušet, že nainstalovaný Python funguje!

Zkontroluj si, že máš aktivované virtuální prostředí (na začátku příkazové
řádky ti svítí `(venv)`).

Je-li tomu tak, nezbývá než – konečně – pustit Python.
K tomu použij příkaz `python`:

``` console
(venv)$ python
Python 3.6.0 (default, Jan 26 2014, 18:15:05)
[GCC 4.8.2 20131212 (Red Hat 4.8.2-7)] on linux
Type "help", "copyright", "credits" or "license" for more information.
```

Příkaz vypíše několik informací.
Z prvního řádku se můžeš ujistit, že používáš Python 3.

Python pak třemi „zobáčky“ `>>>` poprosí o instrukce.
Je to jako v příkazové řádce, ale místo příkazů jako
`cd` a `mkdir` sem budeš psát příkazy Pythonu.

Nejjednodušší příkaz Pythonu je prosté číslo. Zkus to:

```pycon
>>> 1
1
>>> 42
42
>>> -8.3    # (Python používá desetinnou tečku)
-8.3
```

> [note]
> Zobáčky `>>>` i odpověď vypisuje sám Python!
> {{ gnd('sám', 'sama') }} zadej jen číslo a Enter.

Čísla umí Python i sečítat. Třeba takhle:

```pycon
>>> 8 + 2
10
```

Všimni si, že příkazy z příkazové řádky v Pythonu nefungují,
ačkoli okýnko vypadá skoro stejně:

```pycon
>>> whoami
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
NameError: name 'whoami' is not defined
```

Tohle je *chybová hláška*, která se objeví vždycky,
když uděláš něco špatně.
V průběhu kurzu jich uvidíš ještě spoustu,
takže si ji dobře prohlédni, ať ji příště poznáš.

Pokud ses dostal{{a}} až sem, gratuluji!
Python máš nejen nainstalovaný, ale taky ti funguje.
Stačí ho už jen zavřít a pak opustit i samotnou příkazovou řádku.
V Pythonu se to dělá pomocí `quit()`, s prázdnými závorkami na konci.

<div class="highlight"><pre>
<span class="gp">&gt;&gt;&gt;</span> quit()
<span class="gp">(venv)$</span>
</pre></div>

Zobáčky `>>>` se změnily na výzvu
příkazové řádky (která začíná `(venv)` a končí `$` nebo `>`).
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
