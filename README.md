# Nauč se Python

Open material to learn Python - on courses we organize, but also for self-learners.

This is available at [naucse.python.cz](https://naucse.python.cz).


## Installation and local deployment

If you want to deploy this server locally, you'll need to:

* Download and install the latest [Python](https://www.python.org/downloads/)
* Clone or download this repository and go to this directory.
* Install dependencies:

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

* (optional) activate the virtual environment with `pipenv shell`.
* Start the development server:
  ```console
  $ pipenv run serve
  ```
* You can now access the server at `http://0.0.0.0:8003/`.

If you want to generate static HTML files instead of starting the development server (e.g. for static hosting):

  ```console
  $ PYTHONPATH=. pipenv run freeze --serve
  ```
* HTML pages have been generated in `naucse/_build`.

## Externí kurzy

Na naucse.python.cz jsou k dispozici i *externí* kurzy, které spravují více
či méně důvěryhodní lidé.
Proces vykreslování obsahu těchto kurzů jim dává velkou volnost: můžou převzít
plnou kontrolu nad počítačem, na kterém `naucse` běží.
Kvůli bezpečnosti je proto `naucse` ve výchozím nastavení neukazuje.

## Testy

Chceš-li pustit testy, nainstaluj si závislosti:

```console
$ pipenv install --dev
```

a testy pusť:

```console
$ pipenv run test
```


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
