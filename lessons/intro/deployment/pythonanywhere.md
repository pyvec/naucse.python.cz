Deployment webových aplikací na PythonAnywhere
==============================================

[PythonAnywhere] je pro limitované použití zdarma.

K posílání kódu na produkční prostředí budeme používat Git.
Nejprve proto uložte celý projekt do Gitu a nahrajte na GitHub.

Potom se zaregistrujte na
[www.pythonanywhere.com](https://www.pythonanywhere.com/) a vyberte
*Beginner Account*.
Po přihlášení se ukáže záložka *Consoles*, kde vytvořte "Bash" konzoli.
V té vytvořte a aktivujte virtuální prostředí a nainstalujte Flask (plus
případně další závislosti nebo jiný webový framework).

PythonAnywhere používá specificky nastavený Linux,
tak je ve webové konzoli potřeba použít jiný příkaz
na vytvoření virtuální prostředí, než jste z toho kurzu zvyklí.
Napište příkazy takto (bez úvodního `$`):

```console
$ virtualenv --python=python3.7 __venv__
$ . __venv__/bin/activate
$ python -m pip install flask
```

> [note]
> Pokud máte na PythonAnywhere starší účet, možná tam Python 3.7 nenajdete.
> Můžete použít Python 3.6, nemělo by to vadit, protože tento návod je
> koncipován tak, aby s touto verzí také fungoval.
> Případně můžete [zažádat o aktualizaci systémové
> image](https://www.pythonanywhere.com/forums/topic/12878/#id_post_52160).


Následně naklonujte na PythonAnywhere váš kód.
S veřejným repozitářem je to jednodušší – stačí ho naklonovat „anonymně”
(`git clone https://github.com/<github-username>/<github-repo>`).
Pokud ale používáme privátní repozitář, bude potřeba si vygenerovat SSH klíč:

```console
$ ssh-keygen  # (zeptá se na hesla ke klíči)
$ cat ~/.ssh/id_rsa.pub
```

Obsah souboru `~/.ssh/id_rsa.pub` je pak potřeba přidat na GitHub v osobním
nastavení v sekci "SSH and GPG Keys".
Pak můžete klonovat přes SSH:

```console
$ git clone git@github.com:<github-username>/<github-repo>.git
```

Zbývá nastavit, aby PythonAnywhere tento kód spustil jako webovou aplikaci.

Přejděte na stránkách PythonAnywhere do *Dashboard* do záložky *Web*,
a vytvořte novou aplikaci.
V nastavení zvolte *Manual Configuration* a *Python 3.7*.
(Volby jiné než *Manual Configuration* automaticky vytvoří kostru aplikace.
Vy ale už aplikaci máte hotovou, takže je nepotřebujete.)

V konfiguraci vzniklé webové aplikace je potřeba nastavit *Virtualenv*
na cestu k virtuálnímu prostředí (<code>/home/<var>&lt;uživatelské-jméno&gt;</var>/__venv__</code>),
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

(Za <code><var>&lt;uživatelské-jméno&gt;</var></code>,
<code><var>&lt;jméno-adresáře&gt;</var></code> a
<code><var>&lt;jméno-souboru&gt;</var></code>
je samozřejmě potřeba doplnit
vaše údaje. Jméno souboru je zde bez přípony `.py`.)

Nakonec restartujte aplikaci velkým zeleným tlačítkem na záložce *Web*
a na adrese <code><var>&lt;uživatelské-jméno&gt;</var>.pythonanywhere.com</code>
si ji můžete prohlédnout.

[PythonAnywhere]: https://www.pythonanywhere.com/

### Deployment soukromých údajů

Protože vaše hesla, tajné klíče apod. nejsou v repozitáři, je nutné je předat
aplikaci zvlášť.
Konfigurační i jiné soubory jde nahrát v záložce *Files* nebo opět vytvořit
a editovat ve webové konzoli.

Pokud vaše aplikace vyžaduje nastavení nějakých proměnných prostředí
(například s cestou ke konfiguračnímu souboru nebo přímo s nějakou konfigurací),
můžete tak učinit přímo z *WSGI Configuration File*.
Buďto „nízkoúrovňově“ (`os.environ`) nebo více sofistikovaně například pomocí modulu `dotenv`,
což ostatně [doporučují i v dokumentaci](https://help.pythonanywhere.com/pages/environment-variables-for-web-apps/).

> [note]
> Doporučujeme pro tyto potřeby stejně raději nepoužívat API klíče
> k vlastním účtům, raději si vyrobte nějaké účty pouze pro tento účel.
> GitHub povoluje všem vytvořit si jeden účet pro automatické operace, ale
> takový účet musí mít napsané v popisu, že je robot.


### Aktualizace

Když nahrajeme nový kód na GitHub, je vždy potřeba provést na PythonAnywhere
v konzoli `git pull` a pak v záložce *Web* aplikaci restartovat.

Placená varianta PythonAnywhere má API a tento proces jde zautomatizovat.

Ve verzi zadarmo to není tak pohodlné.
