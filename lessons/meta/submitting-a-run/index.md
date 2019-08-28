# Přidání kurzu na Nauč se Python

Když už máme nadefinováný vlastní kurz, zbývá nám jen ho dostat na [naucse.python.cz](https://naucse.python.cz/).
Budeme k tomu potřebovat jen pár příkazu v Gitu a trochu trpělivosti.

## Nahrání do vlastního forku

První věc, kterou budeš potřebovat, je vlastní účet na [GitHubu](https://github.com/).

Přihlaš se na GitHub a vytvoř „fork” [repozitáře pyvec/naucse.python.cz](https://github.com/pyvec/naucse.python.cz).
Na stránce repozitáře vpravo nahoře na to je tlačítko _Fork_.

<div style="text-align: center">
{{ figure(
    img=static('naucse_fork.png'),
    alt="Tlačítko na vytvoření forku repozitáře s Nauč se Python",
) }}
</div>

Jsi-li na GitHubu v nějaké organizaci (např. PyLadiesCZ), můžeš vybrat,
jestli *fork* bude pod tvým účtem nebo pod organizací.
Děláš-li kurz pro organizaci, použij tu,
abyste do materiálů mohli přispívat všichni.
Jinak udělej kurz pod vlastním účtem.

Vytvoření chvilku trvá.
To, že je fork vytvořen, poznáš tak, že tě GitHub přesměruje na stránku, která bude skoro stejná, ale v hlavičce bude jiné uživatelské jméno (tvoje nebo tvé
organizace) a pod tím text `forked from pyvec/naucse.python.cz`.

Tvůj fork si teď potřebuješ přidat do lokálního repozitáře jako *referenci*, abys tam pak mohl{{a}} poslat svůj kurz.
To uděláš pomocí příkazu (nahraď obě `uzivatelskejmeno` za uživatelské jméno,
pod kterým fork je):

```console
$ git remote add uzivatelskejmeno https://github.com/uzivatelskejmeno/naucse.python.cz.git
```

Dále potřebuješ vytvořit commit se svým kurzem a případně se změnami v materiálech.
Je dobré změny dělat v zvláštní větvi, ne v `master`.
Vymysli si název větve (např. `podzim-2016`) a pusť příkazy

```console
$ git branch nazevvetve
$ git checkout nazevvetve
```

Jak vytvořit commit, se dozvíš například v [návodu na používání Gitu]({{lesson_url("git/git-collaboration-2in1")}}).
Více o větvích se můžeš dozvědět v [návodu na větvení v Gitu]({{lesson_url("git/branching")}}).

Svůj commit teď potřebuješ dostat do svého forku na GitHubu.
To uděláš příkazem (`uzivatelskejmeno` nahraď za uživatelské jméno, pod kterým fork
je):

```console
$ git push uzivatelskejmeno
```

## Informace o forku pro Nauč se Python

Teď potřebuješ dostat informaci o tvém forku do základního repozitáře.
To se dělá pomocí souboru `link.yml`, se kterým se udělá _Pull Request_ do základního repozitáře.

Nejdřív si vytvoř novou větev odvozenou od původního repozitáře, ve které vytvoříš soubor `link.yml`.
To uděláš tímto příkazem (`pridanikurzu` můžeš změnit, je to název nové větve):

```console
$ git checkout -b pridanikurzu origin/master
```

Možná sis všiml{{a}}, že tvoje změny jsou najednou pryč, ale neboj, ony jsou uloženy na tvém počítači i na GitHubu, jen zrovna nejsou vidět.

Teď potřebuješ vytvořit stejnou složku jako jsi vytvořil{{a}} pro soubor `info.yml` – musí se jmenovat úplně stejně.
V té složce vytvoř soubor, který se tentokrát bude jmenovat `link.yml`.
Bude zase ve formátu YAML, ale tentokrát bude jednoduchý.
Jedinou povinou informací je klíč `repo`, do kterého musíš dát odkaz na tvůj fork.
Jméno větve pak napiš do klíče `branch`.
Pozor, jedná se o větev s kurzem, ne o větev, ze které kurz přidáváš na Nauč se Python (tedy **ne** `pridanikurzu` z příkladu výše).

Výsledný soubor pak vypadá následovně:

```yaml
repo: https://github.com/uzivatelskejmeno/naucse.python.cz.git
branch: nazevvetve
```

Vytvoř s tímto souborem (a jen tímto souborem) commit a zase odešli změnu na GitHub.

```console
$ git push uzivatelskejmeno
```

Teď už potřebuješ udělat _Pull Request_ (dále jen jako PR) se souborem `link.yml`.
Jak udělat PR je popsáno v [návodu na používání Gitu]({{lesson_url("git/git-collaboration-2in1")}}).
Ideálně do popisku napiš, kdo jsi a co organizuješ za kurz, ať to správci nemusí zjišťovat například z popisku v `info.yml`.

Po tom, co správci PR schválí a sloučí tvoje změny do základního repozitáře, stačí počkat pár minut a tvůj kurz se objeví na [naucse.python.cz](https://naucse.python.cz/).

## Upravování kurzu

Pokud budeš chtít na svém kurzu něco změnit, musíš se nejdřív zpátky přepnout do větve, ve které ten kurz je.
To uděláš následujícím příkazem.
`nazevvetve` nahraď za větev, ve které kurz máš.

```console
$ git checkout nazevvetve
```

S každou změnou pak musíš udělat commit a odeslat commit na GitHub.

Už naprosto poslední věc, kterou je potřeba zařídit, je aby se změny ve tvém kurzu u tebe ve forku projevily na Nauč se.
To se dělá pomocí tzv. webhooků, webových adres, které reagují na nějaké akce.
Musíš tedy nastavit svůj fork, aby posílal akce na webhook, který vyvolá nové nasazení webové stránky [naucse.python.cz](https://naucse.python.cz/).

Pro instalaci webhooků máme speciální aplikaci, která je umí sama nastavit.
Běží na adrese [hooks.nauc.se](https://hooks.nauc.se).
Když se v té aplikaci přihlásíš, uvidíš tam svůj fork repozitáře naucse.python.cz (a všechny ostatní forky Nauč se, do kterých máš přístup).
Poté už jen stačí kliknout na tlačítko _Aktivovat_ u správného repozitáře a webhook se nainstaluje.
A to je všechno! Přidal{{a}} jsi kurz na Nauč se Python!

> [note]
> Pokud to umíš a chceš, můžeš si webhook nainstalovat {{gnd("sám", "sama")}} manuálně.
> Adresa webhooku je `https://hooks.nauc.se/hooks/push`, je potřeba `Content-Type` `application/json` a secret není potřeba zadávat.
