# Linuxová administrace - 2. sraz
- opakovaní

```
ls *.txt
ls *[AB].txt
ls *A.txt *B.txt
```

`head -n3 *.dat` získá první 3 řádky všech souborů končící na .dat

## Proměnná
`jmeno=minotaur.dat` !nesmí být mezery vedle rovnítka
`echo $jmeno` vypíše proměnnou jmeno na stdout

příklad použití:
`head -n2 $jmeno | tail -n1` získáme druhý řádek ze souboru minotaur.dat, který je uložený v proměnné jmeno

moje_skrolovatko=head
$moje_skrolovatko unicorn.dat

`PAGER=more git log` PAGER - proměnná prostředí
`env` vypíše všechny proměnné prostředí
- podstatné proměnné SHELL, HOSTNAME, PATH, PWD, VISUAL, DISPLAY

`PS1` do této proměnné se dá zapsat, čím nám bude začínat každý řádek v bashi, můžeme přepsat např. jen na `PS1='$ '`
`PS2` je pokračovací znak (při víceřádkovém zadávání v shellu)

`$?` návratová hodnota posledního příkazu
- pokud vypíše '0', pak proběhl příkaz v pořádku
- hodnota jiná než '0', příkaz skončil chybou

`$$` hodnota procesu

`echo ${jmeno}abc` výstup: minotaur.databc
složené závorky je potřeba použít pokud skládáme proměnnou s řetězcem

`$@` použije všechny argumenty, nejlépe dávat do uvozovek


## Cykly
### For
```
for jmeno in a b c
do
    echo $jmeno
done
```

Cyklus se dá také zapsat na jeden řádek, v tom případě musí být jednotlivé příkazy odděleny středníkem:
```
for jmeno in a b c; do echo $jmeno; done
```

V našem případě budeme chtít vypsat druhý řádek ze souborů creatures:
```
for x in *.dat
do
    head -n 2 $x | tail -n 1
done
```
### While
```
while true; do head /dev/urandom|sha256sum; done
```


## Historie

pomocí PageUp / PageDn můžu listovat v historii
např. zadám `cat ` a pak procházím všemi zadanými příkazy

ctrl-R: stisknu ctrl-R, pak zadám část příkazu a zobrazí se mi nejbližší příkaz který vyhovuje podmínce. Pokud chci procházet dále, pak opakovaně použiji ctrl-R.

history - zobrazení historie

ctrl-D ukončí zadávání vstupu
ctrl-L vyčistí obrazovku
ctrl-W smaže slovo
ctrl-šipky přesunují mezi slovy
ctrl-s pozastaví výstup (jakoby terminál zamrznul), ale příkazy se provádí
ctrl-q zobrazí vše, co bylo stisknuto po ctrl-s
ctrl-Z pozastaví právě prováděný příkaz a vrátí vás zpět do příkazové řádky, k zastavenému příkazu se lze vrátit pomocí 
`[1]+  Stopped                 python`

jobs - jaké jsou pozastavené příkazy
fg - vrátí se k poslednímu zastavenému příkazu
bg - spustí se zastavený program na pozadí
kill %1 - můžu ukončit konkrétní proces (zastavený příkaz číslo 1)

pokud spustím příkaz s & na konci, spustí se proces přímo na pozadí
`gitk --all &`

## Bash skript
Do souboru můžu zapisovat bash příkazy, které se postupně provedou.

`touch klasifikace`
do souboru zapíšeme:
```
for x in *.dat
do
    head -n 2 $x | tail -n 1
done
```

Následně skript spustím. Musím být ve složce, která obsahuje tento soubor.
`bash klasifikace`


Na začátek skriptu by se měl zapsat *shebang*, který říká jakým program se soubor bude spouštět. V našem případě chci spouštět bash:
`#! /bin/bash`

ls -l klasifikace zobrazí informaci o souboru, důležitá jsou práva:
rw-rw-r--
- r - právo pro čtení
- w - právo na zápis
- x - právo na spuštění

tyto práva se opakují 3x za sebou, pro ...

přidat právo na spuštění:
- `chmod +x klasifikace`


shebang:

v souboru:
```
#! /usr/bin/cat


Tady jsou informace
```
```
$ cat README
```
při zadání pouze $ klasifikace nebude fungovat, protože cesta ke klasifikaci není v $PATH

```
$ echo $PATH

/home/user/.local/bin:/home/user/bin:/usr/share/Modules/bin:/usr/local/bin:/usr/local/sbin:/usr/bin:/usr/sbin:/var/lib/snapd/snap/bin
```
v `/home/user/bin` můžeme definovat vlastní příkazy
`~/.bashrc` soubor ve kterém je možné definovat úpravy v prostředí, např. přidat cesty do Path, upravit PS1, atd.


klasifikuj:
```
#! /bin/bash

head -n2 "$1" | tail -n1
```


uvozovky - argument dávat do uvozovek, protože v případě kdy je převzatém argumentu mezera, vzala by se jinak pouze část
$0 - nultý argument, tedy název programu
./klasifikuj minotaur.dat


## Hledání

### grep
`grep not haiku.txt` hledá v souboru haiku.txt řetězec not a vypíše každý řádek s tímto řetězcem

přepínače:
- i - nezáleží na velikosti písmen
- n - vypíše čísla řádků
- w - 

regulární výrazy grep -i .+ haiku.txt
grep -i '.*' haiku.txt

### find
find . -name '*.txt'
hledá v tomto adresáři a všech podadresářích .txt soubory


## Úkol

Inspirace Bashe: https://github.com/encukou/bin


Naklonuj si tyto repozitáře (přímo v adresáři pro tento kurz; `git clone` udělá nový podadresář):

    $ git clone https://github.com/pyladiescz/pyladies.cz
    $ git clone https://github.com/pyvec/pyvo-data

Data si prohlédni a zjisti, co se v nich skrývá za informace. Zvlášť doporučuju třeba soubor `pyvo-data/series/brno-pyvo/events/2018-10-25-casove.yaml`.

Použij základní shellové příkazy (ne Python) na zodpovězení těchto otázek:

* Kolik bylo kurzů/srazů PyLadies?

* Kolik bylo Pyv v Brně?
* Kolik bylo Pyv celkem?
* Z kolika přednášek na Pyvech jsou videa?  *(Předpokládej že kazdá přednáška může mít max. 1 video)*
* Z kolika Pyv jsou videa?

* Vypiš všechna místa konání Pyv (stačí identifikátor jako `artbar`) a kolikrát tam Pyvo bylo.
* Jaké jsou 3 nejčastější křestní jména organizátorů/koučů/atd. PyLadies?

YAML soubory by se správně měl číst knihovnou na YAML, aby byla zachována struktura. Ty je ale ber jako "čistý text", kde hledané informace jsou na čádcích ve tvaru `klíč: hodnota` (příp. s nějakýma mezerama a/nebo pomlčkama navíc). Odpovědi tak nemusí být 100% přesné.


---

V Pythonu napiš funkci, která bere řetězec a vrátí "obrácený" řetězec: znaky jsou v něm pozpátku a podle následujícího slovníku. Znaky, které ve slovníku nejsou, program vypíše nezměněné.

(Nápověda k Pythonu je níže.)

    {'a': 'ɐ', 'b': 'q', 'c': 'ɔ', 'd': 'p', 'e': 'ǝ', 'f': 'ɟ', 'g': 'ƃ',
    'h': 'ɥ', 'i': 'ᴉ', 'j': 'ɾ', 'k': 'ʞ', 'l': 'l', 'm': 'ɯ', 'n': 'u',
    'o': 'o', 'p': 'd', 'q': 'b', 'r': 'ɹ', 's': 's', 't': 'ʇ', 'u': 'n',
    'v': 'ʌ', 'w': 'ʍ', 'x': 'x', 'y': 'ʎ', 'z': 'z', 'A': '∀', 'B': 'B',
    'C': 'Ɔ', 'D': 'D', 'E': 'Ǝ', 'F': 'Ⅎ', 'G': 'פ', 'H': 'H', 'I': 'I',
    'J': 'ſ', 'K': 'ʞ', 'L': '˥', 'M': 'W', 'N': 'N', 'O': 'O', 'P': 'Ԁ',
    'Q': 'Q', 'R': 'R', 'S': 'S', 'T': '┴', 'U': '∩', 'V': 'Λ', 'W': 'M',
    'X': 'X', 'Y': '⅄', 'Z': 'Z', '0': '0', '1': 'Ɩ', '2': 'ᄅ', '3': 'Ɛ',
    '4': 'ㄣ', '5': 'ϛ', '6': '9', '7': 'ㄥ', '8': '8', '9': '6', ',': "'",
    '.': '˙', '?': '¿', '!': '¡', '"': '„', "'": ',', '`': ',', '(': ')',
    ')': '(', '[': ']', ']': '[', '{': '}', '}': '{', '<': '>', '>': '<',
    '&': '⅋', '_': '‾'}

Např.:

    >>> obrat("Ahoj, brněnské PyLadies!")
    '¡sǝᴉpɐ˥ʎԀ éʞsuěuɹq 'ɾoɥ∀'

Udělej z toho program pro příkazovou řádku, který bere soubory k obrácení. Když nedostane žádný argument, použije standardní vstup. Argument `-` taky znamená standardní vstup.

    $ echo Ahoj | obrat
    ɾoɥ∀
    $ echo Ahoj | obrat -
    ɾoɥ∀


    $ echo 'Ahoj,
    > PyLadies!' > pozdrav.txt
    $ obrat pozdrav.txt
    'ɾoɥ∀
    ¡sǝᴉpɐ˥ʎԀ
    $ echo haha | echo obrat pozdrav.txt - pozdrav.txt
    'ɾoɥ∀
    ¡sǝᴉpɐ˥ʎԀ
    ɐɥɐɥ
    'ɾoɥ∀
    ¡sǝᴉpɐ˥ʎԀ

Zařiď, aby s přepínačem `--help` program vypsal krátkou nápovědu (a ignoroval ostatní argumenty).
Je-li použit jiný přepínač (začínající `-`), program by měl učivateli vynadat (na chybovém výstupu), vrátit chybovou návratovou hodnotu a ignorovat ostatní argumenty.

Nakonec program změň tak, aby vracel chybovou návratovou hodnotu když některý znak chybí ve slovníku.

    $ echo Ahoj | obrat
    ɾoɥ∀
    $ echo $?
    0
    $ echo Čau | obrat
    nɐČ
    $ echo $?
    1

Naimportuješ-li `sys` a `os`, pak:

* `sys.argv` je seznam argumentů (včetně jména programu)
* `sys.stdin` je *už otevřený* soubor se std. vstupem (netřeba `with` či `close`)
* Podobně `sys.stdout` je soubor se standardním výstupem (tam píše `print`) a `sys.stderr` je soubor chybovým výstupem.
* `os.environ` je slovník* s proměnnýma prostředí
* `exit(1)` ukončí program s danou hodnotou

(* přesněji řečeno, objekt který se chová jako slovník)

