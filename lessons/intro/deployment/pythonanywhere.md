Deployment webových aplikací na PythonAnywhere
==============================================

[Python Anywhere] je pro limitované použití zdarma.

K posílání kódu na produkční prostředí budeme používat Git.
Nejprve proto uložte celý projekt do Gitu a nahrajte na GitHub.

Potom se zaregistrujte na
[www.pythonanywhere.com](https://www.pythonanywhere.com/) a vyberte
Beginner Account.
Po přihlášení se ukáže záložka *Consoles*, kde vytvoříme "Bash" konzoli.
V té vytvořte a aktivujte virtuální prostředí a nainstalujte Flask (plus
případně další závislosti nebo jiný webový framework).

PythonAnywhere používá specificky nastavený Linux,
tak je ve webové konzoli potřeba použít jiný příkaz
na vytvoření virtuální prostředí, než jste z toho kurzu zvyklí.
Napište příkazy takto (bez úvodního `$`):

```console
$ virtualenv --python=python3.6 __venv__
$ . __venv__/bin/activate
$ python -m pip install flask
```

Následně naklonujte na PythonAnywhere náš kód.
S veřejným repozitářem je to jednodušší – stačí ho naklonovat „anonymně”
(`git clone https://github.com/<github-username>/<github-repo>`).
Pokud ale používáme privátní repozitář, bude potřeba si vygenerovat SSH klíč:

```console
$ ssh-keygen  # (zeptá se na hesla ke klíči)
$ cat ~/.ssh/id_rsa.pub
```

Obsah souboru `~/.ssh/id_rsa.pub` je pak potřeba přidat na GitHub v osobním
nastavení v sekci "SSH and GPG Keys".
Pak můžeme klonovat přes SSH:

```console
$ git clone git@github.com:<github-username>/<github-repo>.git
```

Zbývá nastavit, aby PythonAnywhere tento kód spustil jako webovou aplikaci.

Přejděte na stránkách PythonAnywhere do *Dashboard* do záložky *Web*,
a vytvořte novou aplikaci.
V nastavení zvolte *Manual Configuration* a *Python 3.6*.

V konfiguraci vzniklé webové aplikace je potřeba nastavit *Virtualenv*
na cestu k virtuálnímu prostředí (`/home/<jméno>/__venv__`),
a obsah *WSGI Configuration File* přepsat.
To jde buď kliknutím na odkaz v konfiguraci (otevře se webový editor)
nebo zpět v bashové konzoli pomocí editoru jako `vi` nebo `nano`.

Nový obsah souboru by měl být:

```python
import sys
path = '/home/<uživatelské-jméno>/<jméno-adresáře>'
if path not in sys.path:
    sys.path.append(path)

from <jméno-souboru> import app as application
```

(Za `<uživatelské-jméno>`, `<jméno-adresáře>` a `<jméno-souboru>` je samozřejmě potřeba doplnit
vaše údaje. Jméno souboru je zde bez přípony `.py`.)

Nakonec restartujte aplikaci velkým zeleným tlačítkem na záložce *Web*
a na adrese `<uživatelské-jméno>.pythonanywhere.com` si ji můžete
prohlédnout.

[Python Anywhere]: https://www.pythonanywhere.com/

### Deployment soukromých údajů

Protože vaše hesla, tajné klíče apod. nejsou v repozitáři, je nutné je předat
aplikaci zvlášť.
Konfigurační i jiné soubory jde nahrát v záložce *Files* nebo opět vytvořit
a editovat ve webové konzoli.

> [note]
> Doporučujeme pro tyto potřeby stejně raději nepoužívat API klíče
> k vlastním účtům, raději si vyrobte nějaké účty pouze pro tento účel.
> Twitter vyžaduje před vydáním API klíčů zadání a potvrzení telefonního čísla.
> GitHub povoluje všem vytvořit si jeden účet pro robota, ale musí to mít
> napsané v popisu.


### Aktualizace

Když nahrajeme nový kód na GitHub, je vždy potřeba provést na PythonAnywhere
v konzoli `git pull` a pak v záložce *Web* aplikaci restartovat.

Placená varianta PythonAnywhere má API a tento proces jde zautomatizovat.

Ve verzi zadarmo to není tak pohodlné.
