# Odkazy

Vyvoříme si nový soubor `basnicka.txt`
```
Kdyz byl pepa jeste mlady
nevedle si s nicim rady
```

```
$ ls -i
```

```
540792 drwxr-xr-x. 2 guest guest 4096 Mar 13  2016 basnicka.txt
557103 drwxrwxr-x. 4 guest guest 4096 Feb  1  2019 dev
557071 drwxr-xr-x. 2 guest guest 4096 Mar 13  2016 Documents
```

V prvním sloupci je identifikační číslo souboru.

```
$ ln basnicka.txt basen.txt
```

```
534799 -rw-rw-r--. 2 guest guest    0 Oct 24 18:23 basen.txt
534799 -rw-rw-r--. 2 guest guest    0 Oct 24 18:23 basnicka.txt
```
Oba soubory jsou zcela stejné. Když změním jeden, změní se i druhý.

tomu se říká **hardlink**.


```
534799 -rw-rw-r--. 2 guest guest    0 Oct 24 18:23 basen.txt
534799 -rw-rw-r--. 2 guest guest    0 Oct 24 18:23 basnicka.txt
                   ^
                   |
                   +-- toto počítadlo existence soubour na disku
                       (=kolikrát se na disku nachází)   
```

Hardlink není úplně šikovný. Užitečnější je ale **symlink**.
```
$ ln -s BASEN basnicka.txt
```

```
$ ls -li
534947 lrwxrwxrwx. 1 guest guest    9 Oct 24 18:26 BASEN -> basen.txt
534799 -rw-rw-r--. 2 guest guest    0 Oct 24 18:23 basen.txt
```

dá se udělat i odkaz někam, kde nic není.


* je to užitečné kvůli tomu, že odkazem se nic nekopíruje
* symlink může odkazovat i na adresáře
* na to je dobré dávat pozor, až budete příště něco psát, co čte soubory z disku


# Jak jsou uspořádané soubory na disku

Zkus si otevřít adresář `/`

Což je hlavní rozdík oproti Windows, kde jsou C:, D:

V UNIXu je všechno uloženo někde pod adresářem `/`.

Wiki: filesystem hiearchy standard

To jak vypadá vychází mj. z historických důvodů. Je totiž univerzální, 
Jsou rozdělené které jsou pro čtení, které pro zápis, které jsou přístupné pro všechny adresáře, pro každého uživatele zvlášt, software, ktrý se instaluje přes nějaký systémový instalátor, programy, které si člověk nainstaluje ručně.

## /bin
Obsahuje všechny příkazy, které můžu spustit.

Možná to budeš mít jako symlink na `/usr/bin`. V `/bin` jsou věci, které potřebuje systémový admninistrátor, aby mohl počítač opravit.

V `/usr/bin` jsou věci, které už jsou navíc a 


## /boot

Soubory na inicializaci systému. Načte to jádro, připraví zbytek disku, aby se dal používat a to jádro to pustí. Když máš nainstalovaných víc OS, tak tady je menu pro jejich výběr.

## /cd-rom
V dřívější době se tady objevil obsah vloženého CD. Dneska se to ale už dává jinam. Ne na každém systému tento adresář najdeš.

## /dev

"dev" je od "device" - zařízení. Tady jsou sobyr, které ovládají, či řídí zařízení.
Komunikují dost přímo s věcmi, kteér jsou připojené k počítači.

* procesoru
* sdílené paměti,
* disky,
* zvukové karty,
* spousta tty (něco),
* video karty,


Je potřeba být superuživatleem, aby bylo možné něco zapsat a když tam zapíšeš něco špatného, tak si tím můžeš rozbít systém.

## /etc

Konfigurační soubory. Když jsme sysadmin a chci, aby všichni uživatelé mají červené pozadí, tak to nastavím tady - pro celý systém.

Např. `cups` je věc na tisk...
Hesla jsou tady taky. 

Je konvencí, že konfigurace se ukládá jako textový soubor.

Informace o uživatelích je v `passwd`. Je jich tam spousta. Typicky pro každou app je jeden uživatel, kterému se povolí dělat jen tu či onu činnost.
Jako první je uživatel `root`. Někde ke konci bude i tvoje uživatelské jméno.

```

  jmého uživatlee          login shell
  |                         |
root:x:0:0:root:/root:/bin/bash
            |
           jméno hlavní skupiny
            
bin:x:1:1:bin:/bin:/sbin/nologin
daemon:x:2:2:daemon:/sbin:/sbin/nologin
```

Proč `root` nemá svou složku v /home? Jde o to, že běžné uživatelské účty bývají sdílené (jsou k dispozici z více počítačů - přes síť třeba). Zato root se .

Když je login shell `nologin`, tak se nepůjde přihlásit.

Když unix vznikal, tak nevadilo, že se heslo ukládalo přímo do toho souboru. Jenže to se moc neujalo.

Reálná hesla jsou uložená v souboru `shadow`. Ten soubor nemůže nidko přečíst, jsou zahashovaná.

Přidání/smazání uživatele se udělá právě v `/passwd`. Když se za jméno souboru dá tilda `~`, tak 

### hosts
seznam jmen počítačů na síti.


### group
seznam všech uživatelských skupin na počítači.
```
root:x:0:
         
```
Přidáním svého jména na konci 



### fstab
které disky na tomto počítači chcete vidět jako připojené souborové systémy

## /home

místo pro uživatelské domovské složky
Protože tam bude spousta souborů, které začínají `.neco`. Moderní aplikace si ukládají svou konfiguraci do `.config`, kde si to ukládají do složek podle svého jména.

Krom toho by tam mělo být `.local`, kde jsou složky
* `bin` - `pip --user nejakypythonnnastroj` ho nainstaluje právě tady
* `etc`
* `lib`
* `share`
* `var`

Jména těch adresářů mají stejný význam, jako přímov `/`, akorát, že tady to je pro toho konkrétního uživatele.

## /lib a /lib64

jsou odkazy na `/lib`, ten symlink je ze stejného důvodu, jako `/bin` a `/usr/bin`.

poznámka k architekturám - x86_64, arm atd. Python funguje "všude", protože 

```
less /bin/cat
```

Uvidíš spoustu binárního "smetí", což jsou konkrétní 

`glibc.so`
Spousta těch souborů má na konci `.1` či jiné číslo. Název bez této koncovky typicky je symlink na poslední 



`python --> python2`
`python2 --> python2.7`


### /libexec
jsou programy, které by se neměly přímo spouštět z příkazové řádky


## /lost+found
když spadne počítač a zhavaruje disk a najde nějaké soubory, které nejsou zařazené do nějakého adresáře, tak skončí tady. 


## /media
když vložím flashku či CD, tak tady se vytvářely adresáře s obsahem toho zařízení. Což se už dneska zas tak moc nedělá a je pro to lepší místo. Tady se to dává "automaticky".

## /mnt
tady se připojovaly disky - kdysi ručně. Dneska se s tím už tolik nepotkáte, ale klasicky na univerzitách se tady 


## /opt
Tady se dávají věci, které nejsou dělané přímo pro tu distribuci. Aplikace, které spolu dobře spolupracují. Pro ty ostatní případy se to dává do `/opt`.

Typicky třeba Google Chrome. Ten není opensoubrce


## /proc
informace o aktuálně běžících procesech. Každý proces tady má svou složku.
`mem`
`fd` - file descriptors, tady jsou otevřené soubory
`self` je symlink na adresář s aktuálně běžícím procesem.


## /root
domovský adresář pro superuživatele


## /run
toto je docela nová věc, tady se dávají soubory, které se používají za běhu (např docker kontejner)

`/run/media/` - tady se objeví obsah např. připojené flashky (toto je nejaktuálnější místo)

## /sbin
dneska se už tak moc nepoužívá, tady jsou programy pro superuživatele, který by neměl spouštět běžný uživatel - správa disků, analýza chyb, nastavení sítě...

## /srv
tady se tradičně dávají věci přístupné z webového serveru

## /sys
informace o systému, dá se tím i nastavit např. rychlost větráčků atd.

## /tmp
velice zajímavá složka - tady se dávají dočasné soubory. Na moderních systémech se tato složka automaticky smaže při startu systému. Historicky se tady ukládaly např. stažené soubory z prohlížeče, rozbalené archivy atd.

Krom toho existuje i `/var/tmp`, kam se dávají dočasné soubory, které nechci smazat při restartu počítače.

## /usr
složky pro uživatele 

## /var
tady jsou soubory, co se mění za běhu systému.
`/var/mail` je systémová pošta. Pošta je starší, než  internet - daly se posílat maily mezi uživateli.

`/var/cache/` - tady se dávají soubory, co zrychlují práci, ale dají se vygenerovat znova.

`/var/run/` - TODO doplnit info
(`/var/run/`) může být symlink na `/var/`

## /cache




# Volné místo na disku
`df` je od disk free
`df -h` je výpis pro "lidi"
