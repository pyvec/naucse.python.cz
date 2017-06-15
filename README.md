# Nauč se Python

Otevřené materiály pro výuku Pythonu – jak na organizovaných kurzech,
tak pro samouky.

Dostupné na [naucse.python.cz](http://naucse.python.cz).


## Instalace a spuštění

Chceš-li server spustit na svém počítači, např. proto, že se chceš zapojit,
nebo abys ho měl/a k dispozici i bez připokení k Intenetu, je potřeba ho
nejdřív nainstalovat:

* Vytvoř a aktivuj si [virtuální prostředí](http://naucse.python.cz/lessons/beginners/install/).
* Přepni se do adresáře s kódem projektu.
* Nainstaluj závislosti:
   ```console
   $ python -m pip install -r requirements.txt
   ```

Nainstalovanou aplikaci spustíš následovně:

* Aktivuj si virtuální prostředí.
* Nastav proměnnou prostředí:
  * Linux a Mac OS:
    ```console
    $ export PYTHONPATH=.
    ```
  * Windows:
    ```console
    > set PYTHONPATH=.
    ```
* Spusť server:
  ```console
  $ python -m naucse serve
  ```
* Program vypíše adresu (např. `http://0.0.0.0:8003/`); tu navštiv v prohlížeči.


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
