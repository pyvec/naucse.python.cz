# Lokální instalace Nauč se python

K přidání kurzu nejdřív člověk potřebuje vlastní, lokální instalaci webové aplikace Nauč se Python.

## Příprava

První věc, kterou budeš potřebovat, je Python, a to alespoň ve verzi 3.6.
Pokud zrovna danou verzi Pythonu nainstalovanou nemáš, můžeš postupovat podle [návodu na instalaci Pythonu][beginners-install].

[beginners-install]: {{lesson_url("beginners/install")}}

Druhá věc, kterou budeš potřebovat, je Git – pokud nemáš ten, můžeš postupovat podle [návodu na instalaci Gitu]({{lesson_url("git/install")}}).

Poslední věc, kterou potřebuješ, už není žádný program, ale pár schopností.
Je potřeba, abys uměl{{a}} pracovat s příkazovou řádkou (terminálem) a s Gitem.
Vše potřebné si můžeš připomenout v [návodu na používání terminálu]({{lesson_url("beginners/cmdline")}}), respektive v [návodu na používání Gitu]({{lesson_url("git/git-collaboration-2in1")}}).

## Instalace

Nauč se Python používá k definici závislostí Pipenv, který si nejspíš budeš muset doinstalovat.
Postupovat můžeš podle [návodu na instalaci Pipenvu][pipenv-install].

[pipenv-install]: https://pipenv.readthedocs.io/en/latest/install/#installing-pipenv

Po instalaci si musíš naklonovat repozitář, ze kterého se Nauč se Python vykresluje.
To uděláš tímto příkazem:

```console
$ git clone https://github.com/pyvec/naucse.python.cz
```

Poté přepni adresář do naklonovaného repozitáře:

```console
$ cd naucse.python.cz
```

Zbývá už jen nainstalovat závislosti, to uděláš pomocí následujícího příkazu, který za tebe zároveň i vytvoří virtuální prostředí.

```console
$ pipenv install
```

{{ anchor('launch') }}
## Spuštění

Nauč se Python jde pustit ve dvou režimech.
První režim vykresluje každou stránku pokaždé znova – hodí se na vývoj, aby byly všechny změny okamžitě vidět.
Pustí se následovně:

```console
$ pipenv run naucse serve
 * Running on http://0.0.0.0:8003/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 256-270-314
```

V ukázce vidíš rovnou i příklad toho, co to vypíše – zajímá tě jen adresa, zde `http://0.0.0.0:8003/` (u tebe se může lišit).
Když si ji zkopíruješ a otevřeš ve webovém prohlížeči, uvidíš vlastní běžící Nauč se Python.

Druhý režim nejdříve vykreslí všechny stránky a až poté ti je zobrazí – hodí se spíše na kontrolu toho, že se při vývoji nic nepokazilo.
Pustí se následovně (pozor, nějakou chvíli to trvá):

```console
$ pipenv run naucse freeze --serve
Generating HTML...
 * Running on http://127.0.0.1:8003/ (Press CTRL+C to quit)
```

> [note]
> Když odnaviguješ například do seznamu kurzů, je možné, že tam nebudou všechny.
> To jsou kurzy, které se vykreslují z jiných forků, které jsou na lokálním prostředí
> automaticky vypnuté.
