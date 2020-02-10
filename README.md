# Linuxová administrace

Tady budou vznikat otevřené materiály pro kurz linuxové administrace.


## Instalace a spuštění

Chceš-li server spustit na svém počítači, např. proto, že se chceš zapojit do
vývoje, je potřeba ho nejdřív nainstalovat:

* Vytvoř a aktivuj si [virtuální prostředí](https://naucse.python.cz/lessons/beginners/install/).
* Přepni se do adresáře s kódem projektu.
* Nainstaluj závislosti:

  * Linux/Mac:

    ```console
    $ python3 -m pip install pipenv
    $ pipenv install --dev
    ```

  * Windows:

    ```doscon
    > py -3 -m pip install pipenv
    > pipenv install --dev
    ```

Nainstalovanou aplikaci spustíš následovně:

* Aktivuj si virtuální prostředí, máš-li ho vytvořené.
* Spusť vývojový server:
  ```console
  $ pipenv run serve
  ```
* Program vypíše adresu (např. `http://0.0.0.0:8003/`); tu navštiv v prohlížeči.


## Licence

Každá lekce má vlastní licenci, která je uvedena v metadatech.
Používáme pouze [licence pro otevřený obsah][free content licenses].
Všechen obsah musí mít uvedenou licenci.

---

Content has its own license specified in the appropriate matadata.
Only [free content licenses] are used. By contributing to an already licensed
document, you agree to have it licensed under the same license.
(And feel free to add yourself to the authors list in its metadata.)
When contributing new document(s) a license must be specified in the metadata.

[free content licenses]: https://en.wikipedia.org/wiki/List_of_free_content_licenses
