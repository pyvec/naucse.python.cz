# 3. sraz - Procesy a soubory

Motto:
> I grafické apl. se dají spouštět z příkazové řádky.

Grafické programy se dají spustit nejen z hlavní nabídky aplikací, ale taky z příkazové řádky. To si teďka vyzkoušíme.

Otevři si příkazovou řádku a zkus tam napsat některý z následujích příkazů. (Znak dolaru `$` neopisuj, takto je zvykem uvozovat text, který se má zadat do příkazové řádky):
```
$ firefox
```
nebo
```
$ gedit
```
nebo taky
```
$ gmome terminal
```




Bezva, takto jsme spustili program. Můžeme mu předat i parametry, jak to již známe z ne-grafických programů. Např:
```
$ firefox github.com
```


Co všechno se dá takhle nastavit? To nám řekne nápověda
```
$ firefox --help
Usage: /usr/lib64/firefox/firefox [ options ... ] [URL]
       where options include:

X11 options
  --display=DISPLAY  X display to use
  --sync             Make X calls synchronous
  --g-fatal-warnings Make all warnings fatal

Firefox options
  -h or --help       Print this message.
  -v or --version    Print Firefox version.
  -P <profile>       Start with <profile>.
  --profile <path>   Start with profile at <path>.
  --migration        Start with migration wizard.
  --ProfileManager   Start with ProfileManager.
  --no-remote        Do not accept or send remote commands; implies
                     --new-instance.
  --new-instance     Open new instance, not a new window in running instance.
  --UILocale <locale> Start with <locale> resources as UI Locale.
  --safe-mode        Disables extensions and themes for this session.
  -MOZ_LOG=<modules> Treated as MOZ_LOG=<modules> environment variable, overrides it.
  -MOZ_LOG_FILE=<file> Treated as MOZ_LOG_FILE=<file> environment variable, overrides it.
                     If MOZ_LOG_FILE is not specified as an argument or as an environment variable,
                     logging will be written to stdout.
  --headless         Run without a GUI.
(...)
```

## Proces

Co je to proces?
> Proces JE běžící program.
* dělá akce
* pracuje na datch
* může ukazovat věci v okýnkách

Příklad s terminálem:
Když si otevřu několik terminálů, vytvoří se několik procesů. Každý má svůj vlastní stav, svou cestu, pamatuje si poslední spuštěný příkaz


### Jaké procesy aktuálně běží?

To nám řekne příkaz `ps`:
```
$ ps
  PID TTY          TIME CMD
 5403 pts/8    00:00:00 bash
 5449 pts/8    00:00:00 ps
```

Toho není moc, že? S parametrem `-a` dostaneme ... ()
```
$ ps -a
```

Hezčí výstup:
```
$ htop
```

```
$ top
```
Co tady vidím?
* procesy jsou seřazeny podle toho, kolik zabírají prostředků (procesoru)
* asi tam budeš mít nějaký “shell”
* gnome-shell je taky druh shellu, ale grafický
* pro posun ve výpisu použij PageUp/Down


`Xorg` - grafické prostředí, stará se o vykreslování oken
firefox


Každý proces má nějaké informace:
PID - process ID, unikátní číslo, číslo toho procesu


**Úkol:** Zkuste si najít číslo toho “topu”
Budeš na to potřebovat ještě druhý terminál.
* v jednom spustit `top`
* ve druhém spustit:
    ```
    $ ps -a | grep top
    ```


1. sloupec je **číslo procesu** (tzv. PID)
Podle čísla procesu se dá ovládat. Například ho ukončit:
    ```
    $ kill <číslo procesu>
    ```

    `kill` “hezky poprosí” proces, aby se ukončil


2. sloupec USER **vlasník**
Každý uživatel na počítači má svůj vlastní uživatelský účet, třeba `hanka`, ale vždy tam je i `root`, který má přístup k celému systému


(případně $ ps aux)


3. **PR - priorita** - některé procesy jsou důležitější, než ostatní
  `51` má nižší prioritu
  `20` má vyšší
4. **NI - nice** - podobně, jako priorita, ale tady to je ve smyslu _jak hezky se tento proces chová k ostatním_. Priorita i hodnota nice jsou samostatné vlastnosti procesu
5. **VIRT**
6. **RES**
7. **SHR** - tyto tři atributy popisují, kolik proces zabírá v paměti
8. **S** je stav procesu. Ten může být _běžící_, _spící_ a další
9. **%CPU** - procentuální vytížení procesoru
10. **%MEM** - procentuální využití paměti
11. **TIME** - jak dlouho už proces běžel - ale jen procesorový čas, když spí, tak se nepočítá
12. a konečně ten samotný příkaz

`top` ukončíš skrze klávesu `q`.


# Soubory
Co je to soubor?
* je to místo v paměti, kt. obsahuje data, mělo by to být možné přečíst
* "něco z čeho můžeme číst, nebo můžeme zapisovat"
    * jsou sobory kde můžu číst
    * jen zapisovat
    * klidně oboje (číst i zapisovat)
    * ani jedno (třeba kvůli právům), ale tím se teďka nebudeme rozptylovat


Soubory se kterými máte největší zkušenosti jsou uložené na disku. Proces si je může otevřít, přečíst a zapsat.


ps aux | … zapisuje výsledky do souboru
ps aux > vystup.txt
        bashi spust ps aux a řeknu mu ,aby psal do souboru vystup.txt


ps píše na standardní výstup, což je pro něj soubor a v tomto případě to je konkrétně vystup.txt


Když pustím ps jenom tak, tak on stejně píše do souboru, akorát neví, že to je terminál, do kterého se dá psát i číst, podobně jako soubor na disku. Bash čte ze souboru pro terminál a rovnou ho zapisuje zpátku, aby bylo vidět, co se píše. Terminál je taky soubor, i když není na disku.


ps aux | grep top … bash vytvoří tzv. rouru, do které ps zapisuje a grep čte.


Zatím známe 3 druhy souboruů:
   * na disku
   * terminál
   * roura

```
$ ls -l /proc/self/fd/1
lrwx------. 1 mpavlase mpavlase 64 Oct 10 18:43 /proc/self/fd/1 -> /dev/pts/0
```

toto je speciální soubor, podíváme se na to zas přístě.


pro 


-> znamená symbolický odkaz (viz příště)
teďka nás zajímá `/dev/pts/…`


Otevřu si další okno a zadám
```
$ echo abc > /dev/pts/12
```
… se objeví v druhém terminálu


Když znám jméno souboru, tak do něj můžu zapisovat. Je zvláštní v tom, že tenhle bash zapisuje zrovna do tohohle terminálu.


K čemu to je dobré? Můžete takhle psát zprávy dalším lidem, co zrovna pracují na tom samém stroji, ale dnes se to už tolik nepoužívá


Q: Není to už moc velká magie? :thinkingface: pravděpodobně ano


Pamatujete si `$$`?
Číslo procesu aktuálního bashe.


Každý program si může otevřít další soubory a podíváme se, jak to zjistit.
```
$ lsof -p <číslo procesu>
$ lsof -p $$
```
FD
   * cwd
   * rtd
   * txt
   * mem
   * 0u
   * 1u - otevřeno pro R i W
   * 2r - otevřeno pro čtení
   * 3w - otevřeno pro zápis
CWD - spec. hodnota pro aktuální adresář
TYPE
DEVICDE - číslo souboru
SIZE/OFF - veliksot
NODE - další číslto souboru
NAME - cesta k souboru


Otevřete si textové editory, začneme si torchu hrát v pythonu.


# souboruy.py
import os   # modul, kde jsou zpřístupněné služby operačního systému


print(os.getpid())
# to číslo, co to vypíše je vždcky jiné.
import time
time.sleep(600)


(otevřu si další terminál, kde ten soubry.py spustím)
v samostatném terminálu pak pustím
$ lsof -p <číslo procesu>






teďka si v pythonu otevřu soubor (jak se to dělá?)
with open(‘soubor.txt’) as soubor:
        time.sleep(600)


kdyuž se teďka podívám na lsof, tak by tam měl přibýt i záznam o tom “soubor.txt”, pravděpodobně pod číslem 3. 


with os.open(‘soubor.txt’) as soubor:
        with open sobor.txt, “w” as fd2:
        time.sleep(600)




tím číslem 2r se 


soubor (fd) python toho pro nás dělá hodně, dělá abstrakci (vlastní pythonní objekt) nad systémovým souborem.
(ty soubory už musí existovat. Když chybí, tak přes touch)


soubor1 = os.open(‘soubor.txt’, os.O_RDONLY)
soubor2 = os.open(‘soubor2.txt’, os.O_WRDONLY)
print(soubor1, soubor2)
sleep(600)         # cheme, aby program stál a my si mohli opsat číslo procesu (PID)


poznámka pro zvídavé: os.O_RDONLY je jen číslo


je tam třeba používat speciální značky, což je rozdíl oproti běžné funkci “open” 


v soubor1 i 2 mám čísla. Každý soubor je takhle očíslovaný a podle toho pak můžu s nima pracvat.


print(os.read(soubor1, 10))    # načtu prvních 10 bajtů ze souboru soubor.txt (protože ho mám k dispozici jako soubor1


Komunikuje se typicky pomocí čísel a krátkých jmen.


os.write(souboru2, b’abcd\n’) zapíše 4 znaky do soubor2.txt


když se na konec nenapíše \n, tak se to vypíše (reps. přepíše) do aktuálního řádku a pak se na to blbě kouká.


Nakonec je zavřu. Je to velmi nízkoúrovňová práce, proto není možné jich zavřít víc.
os.close(soubor1)
os.close(soubor2)


A teďka se mrkneme, co znamená to 0, 1, 2… (z FD)


os.write(1, b‘Tohle jde do souboru 1\n’)
os.write(1, b‘Tohle jde do souboru 2\n’)
Q: Kampak se to vypíše?
A: Oboje se vypíše do terminálu.


$ python soubory.py > jiny.txt
Tohle jde do souboru 2


Do souboru jiny.txt se zapíše Tohle jde do souboru 1


print(os.read(0, 10))


$ python soubory.py
… můžete zkusit něco napsat


0 je standartní vsup, tzn. to, co do programu leze ($ ps -a | grep), takže grep má stdin to samé, co stdout ps.
$ grep má standartní vstup z terminálu.


1 je standartní výstup, 


2 standartní chybový výstup, což je taky temrinál, ale tam programy píší chybové hlášky
$ cp a b        # a chybí, takže
cp: cannot stat a no such file or dir
$ cp a b > jiny.txt
cp: cannot stat a no such file or dir
… jakto? Protože ta hláška je na chybovém výstupu
> přesměrovává standartní výstup
chybový výstup se běžně nepřesměrovává


os.write(1, b‘Tohle jde do stdout\n’)
os.write(1, b‘Tohle jde do stderr\n’)


I pythonní traceback jde do chybového výstupu. Všechny chyby.


Q: Co kdybych chtěl přesměrovat ten druhý, chybový, výstup?
ptyhon soubor.py 2> jiny.txt


Můžu použít i oboje:
$ python soubor.py > vystup.txt 2> chyby.txt
$ cat vystup.txt
$ cat chyby.txt


Záleží na pořadí > a 2> ? Ne, tady ne, dělá to v pořadí, v jakém to napíšu.


Můžu přesměrovat i standartní vstup.
$ python soubor.py < jiny.txt
[placeholder pro výstup]


$ cat jiny.txt | python.py
ukázat lsof, roura má FIFO, obsah je stejný, ale jednou to je typ souboru soubor na disku, podruhé to je roura.


grep abc jiny.txt
(placeholder červený výstup)


grep abc jiny.txt | cat
(placeholder nebarevný výstup)


grep se totiž dívá, jakého typu soubu je stdout a podle toho ne/obarvuje výstup


odbočka pro zvídavé:
python soubory.py 8< jiny.txt
(placeholder z lsof)


find /var/cache > /dev/null
find: … Permision denied


Přesměrování obojeho
Zatím každá věc šla někam jinam, ale zkusíme si oboje přesměrovat do toho samého.


python soubory.py > jiny 2>&1
                           ^--- chybový směruje tam, co první


tohle nepřepisuje soubory, protože to neotevírá další souboru, ale přidává se to za sebe. všechny zápisy jdou přímo do něj


Tady už záleží v jakém pořadí, tohle fungoat nebude.




                       v --- přesměruje stdout do souboru
python soubory.py 2>&1 > jiny
                  ^ --- přesměruje stderr na stdout, který je aktálně terminálem


Proto stderr půjde na terminál a stdout do souboru




Jak se tvoří procesy (teoreticky)
je zajímavé to znát.


print(len(‘abc’))
.. print se vrátí
… len se vrátí


Q: ex. fce, kte se nevrací?


exit()
… se nevrátí


Můžeme mít i fci, co se vrací 2x.


import os
os.fork()
print(“Tohle se stane.”)


# vypíše se dvakrát


Fork je vidlička, nebo když se dělí řeka.


To volání naklonuje aktuální proces a pokračuje dál. Už každý samostatně.


hodnota = os.fork()
Ty procesy se liší tím, co vrátí os.fork().


   * Jednou to je 1827, což je číslo procesu
   * a druhé 0


Rodič dostane 1827, aby mohl toho potomka ovládat
a 0 dostane potomek.


if hodnota == 0:
        print já jsem dítě
else:
        print já jsem rodič


Před forkem se často vytvoří roura, což je soubor, který má dva konce:
   * jeden pro čtení,
   * a druhý pro zápis
r, w = os.pipe()


if hodnota == 0:
        print já jsem dítě
os.close(r)
os.write(1, b’Ahoj’)
else:
        print já jsem rodič
        os.close(w)
        pozdrav = os.read(r, 10)
        print(pozdrav)


Roura otevře dva soubory
print(r, w)


   * pak ten proces rozdvojím
   * zapíšu do roury z 


Není praktické vidět dovnitř jak se to dělá vevnitř, ale je to zajímavé z pohledu konceptu.
