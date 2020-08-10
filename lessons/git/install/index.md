# Git

Další program, který budeme později potřebovat,
nám později umožní (mimojiné) spolupracovat
na vznikajících programech s ostatními.
Jmenuje se Git.
Pojďme si ho nainstalovat a nastavit.

Instalace je různá pro různé operační systémy, vyber ten svůj.


## Linux

Instalaci na Linux zvládneme jedním příkazem:

**Fedora, RHEL**:

```console
$ sudo dnf install git gitk git-gui nano
```

**Ubuntu, Debian**:

```console
$ sudo apt-get install git gitk git-gui nano
```

U jiných Linuxů předpokládám, že instalovat umíš; nainstaluj si *git*,
*gitk*, *git gui* a *nano*.

Jestli máš nainstalováno, ještě nastav Gitu editor.
Pokud nemáš rád{{a}} Vim (nebo nevíš co to je),
zadej tento příkaz:

```console
$ git config --global core.editor nano
```

Dál pokračuj obecným [nastavením](#config) níže.


## Windows

Jdi na stránku [git-scm.org](https://git-scm.org), stáhni si
Git a nainstaluj si ho.

Při instalaci se ujisti, že jsou vybrány tyto volby:

* Adjusting your PATH enviroment: Git from the command line and also from 3rd-party software
* Configuring the line ending conversions: Checkout Windows-style, commit Unix-style line endings

Ostatní možnosti neměň.

Potom Gitu nastav editor.
Máš-li otevřenou příkazovou řádku, zavři ji a otevři novou.
(Instalace mění systémové nastavení, které se musí načíst znovu.)
V nové příkazové řádce zadej:

```console
> git config --global core.editor notepad
> git config --global format.commitMessageColumns 80
> git config --global gui.encoding utf-8
```

A teď pokračuj v sekci [Nastavení](#config) níže – macOS přeskoč.


## macOS

Spusť v příkazové řádce `git`.
Je-li už nainstalovaný, dozvíš se, jak ho používat
(výpis začíná `usage`).
Jinak ho nainstaluj pomocí Homebrew:

```console
$ brew install git git-gui
```

Nainstalovanému Gitu je ještě potřeba nastavit editor (zadej `nano`,
i když sis v rámci instalace editoru nainstaloval{{a}} např. Atom).
Dělá se to tímto příkazem:

```console
$ git config --global core.editor nano
```

Dál pokračuj obecným nastavením:


{{ anchor('config') }}
## Nastavení

Na projektu, který bude uložen v Gitu, může
spolupracovat více lidí.
Aby šlo dohledat, kdo udělal kterou změnu, je Gitu
potřeba říct jméno a e-mail.
Do příkazové řádky zadej následující příkazy, změň v nich ale
jméno a adresu:

```console
$ git config --global user.name "Adéla Novotná"
$ git config --global user.email adela.novotna@example.cz
```

Můžeš samozřejmě použít i přezdívku, nebo dokonce
falešný e-mail, ale v takovém případě bude složitější se
zapojit do týmových projektů.
Každopádně, jméno i e-mail jdou kdykoli změnit
tím, že konfigurační příkazy zadáš znovu.

> [note]
> Pokud se bojíš spamu, neboj: nezačneš ho dostávat víc
> než při normálním používání e-mailu.
> Adresa se zobrazí jen lidem, kteří si stáhnou projekt,
> do kterého jsi přispíval{{a}}.
> Spammeři se většinou zaměřují na méně technicky zdatné
> lidi, než jsou uživatelé Gitu. :)

Dále si můžeš nastavit barevné výpisy – pokud si tedy
(jako někteří autoři Gitu) nemyslíš, že příkazová
řádka má být černobílá:

```console
$ git config --global color.ui true
```

> [note]
> Spuštění `git config` nevypíše žádnou hlášku, že se operace povedla.
> To je normální; stejně se chová spousta dalších příkazů, např. `cd`.
>
> Aktuální konfiguraci gitu si můžeš zkontrolovat příkazem:
>
> ```console
> $ git config --global --list
> user.name=Adéla Novotná
> user.email=adela.novotna@example.cz
> ```

A to je vše! Git máš nainstalovaný. Gratuluji!
