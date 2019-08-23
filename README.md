# Nauč se Python

Otevřené materiály pro výuku Pythonu – jak na organizovaných kurzech,
tak pro samouky.

Dostupné na [naucse.python.cz](https://naucse.python.cz).


## Instalace a spuštění

Chceš-li server spustit na svém počítači, např. proto, že se chceš zapojit
do vývoje, je potřeba ho nejdřív nainstalovat:

* (nepovinné) Vytvoř a aktivuj si [virtuální prostředí](https://naucse.python.cz/lessons/beginners/install/) v Pythonu 3.6.
* Přepni se do adresáře s kódem projektu.
* Nainstaluj závislosti:

  * Linux/Mac:

    ```console
    $ python3 -m pip install pipenv
    $ pipenv install
    ```

  * Windows:

    ```doscon
    > py -3 -m pip install pipenv
    > pipenv install
    ```

Nainstalovanou aplikaci spustíš následovně:

* (nepovinné) Aktivuj si virtuální prostředí, máš-li ho vytvořené.
* Spusť vývojový server:
  ```console
  $ pipenv run serve
  ```
* Program vypíše adresu (např. `http://0.0.0.0:8003/`); tu navštiv v prohlížeči.

Pokud chceš místo vývojového spuštění vygenerovat statické HTML soubory (např. pro nahrání na statický hosting):

* Spusť freeze. Parametr `--serve` provede spuštění webserveru, pomocí kterého si lze vygenerované soubory prohlédnout:
  ```console
  $ PYTHONPATH=. pipenv run freeze --serve
  ```
* HTML stránky jsou v adresáři `naucse/_build`.
  Program vypíše adresu (např. `http://0.0.0.0:8000/`); tu navštiv v prohlížeči.

## Externí kurzy

Na naucse.python.cz jsou k dispozici i *externí* kurzy, které spravují více
či méně důvěryhodní lidé.
Proces vykreslování obsahu těchto kurzů jim dává velkou volnost: můžou převzít
plnou kontrolu nad počítačem, na kterém `naucse` běží.
Kvůli bezpečnosti je proto `naucse` ve výchozím nastavení neukazuje.


## Licence

Kód je k dispozici pod licencí MIT, viz soubor [LICENSE.MIT].

Obsah kurzů má vlastní licenci, která je uvedena v metadatech.
Používáme pouze [licence pro otevřený obsah][free content licenses].
Všechen obsah musí mít uvedenou licenci.

---

The code is licensed under the terms of the MIT license, see [LICENSE.MIT] file
for full text. By contributing code to this repository, you agree to have it
licensed under the same license.

Content has its own license specified in the appropriate matadata.
Only [free content licenses] are used. By contributing to an already licensed
document, you agree to have it licensed under the same license.
(And feel free to add yourself to the authors list in its metadata.)
When contributing new document(s) a license must be specified in the metadata.

[LICENSE.MIT]: https://github.com/pyvec/naucse.python.cz/blob/master/LICENSE.MIT
[free content licenses]: https://en.wikipedia.org/wiki/List_of_free_content_licenses
