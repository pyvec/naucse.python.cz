# Linuxová administrace - 4. sraz


## Linux
https://en.wikipedia.org/wiki/Linux#Design

jádro systému je program co komunikuje s HW a zprostředkovává služby výše a hlídá aby 
programy mohly běžet vedle sebe, správu uživatelů atd. (plánovač procesů)

userspace:
glibc - zprostředkovává služby jádra vyšším vrstvám
pulseaudio - 
démon - program co běží pořád 
    - systemd - stará se o spouštění a správu ostatních demonů

wayland - vykreslování grafických oken na na obrazovku
knihovny jako GTK+, Qt vykreslují grafické ovládací prvky
uživatelské programy používají typicy GTK+/Qt

pro mnoho komponent existuje více variant (implementací). Když se ti nějaká nelíbí, můžeš použít jinou, či si napsat vlastní.

Z toho vychází trable se spolupráci programů mezi sebou a spousta více či méně funkčních kombinací. Proto se to seskupuje do tzv. distribucí, kde jsou poskládané programy, které umí spolupracovat.

* Gnome
* xfce4
* KDE
* Mate

Klidně můžeš používat aplikace i z jiných grafických prostředí.

Gnome je velmi běžné
Nastavení  - Zařízení - Klávesnice ... přehled klávesových zkratek
* můžeš si přidat i vlastní

Pozor, spuštěný program se typicky jmenuje jinak, než název binárky. "nautilus" -> "Soubory"

`which` - existuje spíš z historických důvodů, ale stejně ji spousta lidí stále používá.
Novější alternativou je:
`$ type git`
`git is /bin/git`

tady to je jedno, co se použije, ale třeba `cd` je už rozdíl:
```
$ type cd
cd is a shell builtin
```

```

bash ----+--- bash ----------+-----------------
         |                   |
         +--- firefox        +--- bash -- X
```
`bash` se rozdvojí, jedna ta větev se nahradí programem `firefox`

Pomocí aliasu si můžeme vytvořit vlastní zkratku.
```
$ alias vykricnik='echo !'
$ vykricnik 
!
```

tohle ale bude fungovat jen v akutálním shellu.
Když pak zadáš `bash`, tak tam už `vykricnik` nebude fungovat (protože v něm není nadefinovaný).

skript.sh
```

#! /bin/bash

cd ..
alias kocka=cat
promenna=123
```

```

$ chmod +x skript.sh
$ ./skript.sh
$ type kocka
$ bash: type: kocka: not found
$ echo $promenna


```
Ten spuštěný skript běží v samostatném procesu (tzv. subshell) a ten má svůj vlastní stav. Když skončí, tak stav zanikne. Proto alias ani proměnná v tom skriptu nikdy nezmění stav zdrojového shellu.

`mcd`
```

#! /bin/bash

mkdir $1
cd $1
```
nebude úplně fungovat, protože:
```

          mcd test
bash ----+----------------------------------------
         |                                   ^
         |   bash `mcd test`      cd test    .
         +--- O ------------------- O-------X
              |                 ^
              |                 .
              +--- mkdir test-- X
```




Proměnná se ve výchozím stavu nekopíruje do podprocesu. Abychom toho docílili, je třeba použít `export`.

Soubor: `print-promenna`
```
#! /bin/bash

echo $promenna
```

```

$ echo $promenna
$ promenna=123
$ echo $promenna
123
$ ./print-promenna

```

`type export` nám řekne, že to je `shell built-in`


Vlastní bashovou funkci nadefinujeme takto:

```

vypis () {
    echo $ahoj
}
```
Je možné to napsat i do jediného řádku, ale pak je třeba dávat pozor, kam patří středníky atd. na opravení

# source
* umožňuje spouštět daný skript/program v aktuálním bashovém procesu

jen spuštění vypadá:
```

bash ----+----------------------------------------
         |                                   ^
         |   bash cd      alias    ...
         +--- O ------------O------ O-------X
```

`source` spustí skript v aktuálním shellu:

```

           bash cd       alias    ...
bash ------- O ------------O-------O-------X
```

Namísto source lze použít i `.`, což je oboje _shell builtin_(v `man bash` zjistíme tak, že má `.` i `source` stejný popis)

`/usr/bin/echo abc`

vs.

`echo abc`

Na spouštění podprocesů existuje i zkratka:
`( cd test; pwd); pwd`

```
/home/karel/test
/home/karel
```



```

         (
bash ----+----------------------------------------
         |                                   ^
         |   bash    cd           pwd   )    .
         +---------- O ------------O---------X
```




(standartní) vstup do programu **není** to samé, co argument


```

$ pwd | cat
/home/karel

$ echo /home/karel
/home/karel
```


```
$ echo $( pwd )
/home/karel
```


Cvičení:
```

$ echo $( ls )
$ cat $( ls )
```

```

$ echo $( ls )
venv skript.sh
```
vs.
```

$ cat $( ls )
$ cat venv skript.sh
```

```

$ cat $( ls ) > /dev/null 
cat: test: Is a directory
cat: venv: Is a directory
```


```
$ cat $( ls ) | head
#! /bin/bash
cat:
mkdir -p $1
testcd $1
...
cat: venv: Is a directory
...
```

```

$ echo <( ls )
/dev/fd/63
```

```

$ cat <( ls )
mcd
```



Porovnání dvou souborů - program `diff`

`diff -U3 basnicka.txt basnicka2.txt`


```

# basnicka.txt

# basnicka2.txt
Halo halo???
```

```

diff -U3 <( cat basnicka.txt ) <( cat basnicka2.txt )

```

`mkfifo`


```

diff -U3 <( cat 1 ) <( cat 2 )


bash ----+---+---+--------------------------------
         |   |   | 
         |   |   +---- diff -U3 p1 p2
         |   |                  ^   ^
         |   |                  |   |
         |   |              /...|.../
         |   +--- cat 2 > p2    |
         |                      |
         |             /......../
         |             |
         +--- cat 1 > p1
                  ....
```

`.bashrc` je skript, který bash spustí, když se sám spouští. Když si chceš nastavit vlastní _persistentní_ aliasy atd. tak toto je to správné místo.
```


$ cat .bashrc 
# .bashrc

# Source global definitions
if [ -f /etc/bashrc ]; then
	. /etc/bashrc
fi
```

Když změníš tento soubor, změny se projeví až v dalších nově spuštěných shellech, již běžící to neovlivní. Nebo `source ~/.bashrc`

```

b=$(basename $1)
${b%%.git}
```

Více info: `man bash`, hledat '${param'. Těch transformací tam je celý kopec...

```

$ file basnicka.txt
basnicka.txt: UTF-8 text
```

Když nevíš, co ten soubor je, tak `file` dost napoví. Typicky když ten obsah souboru je nějaký binární nepořádek.

`groups`
Když je uživatel ve skupině `wheel`, tak si pak může přes `sudo` zažádat o oprávnění správce `root`.

Když člověk nezná heslo pro uživatele `root`, dá se to udělat jako `sudo s`

