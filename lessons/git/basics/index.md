# Git

Ať už programuješ nebo píšeš dokumenty, stává se,
že vytvoříš několik verzí.
Tuhle chceš archivovat část, která už není potřeba,
tamhle chceš svoji práci poslat k ohodnocení,
nebo dokonce kolegům kteří na ni spolupracují.
A když se verze začnou kupit, může být problém se v nich vyznat.

Část těchto problémů řeší nástroje jako Dropbox či
Google Drive, se kterými ses možná již setkal{{a}}.
Tam můžeš například sdílet svůj dokument s dalšími
lidmi nebo se můžeš vrátit k dřívější verzi dokumentu,
když něco pokazíš a nemůžeš si vzpomenout, jak to bylo
předtím. Příklad toho, jak to může vypadat, je zde:

{{ figure(
    img=static('dropbox.png'),
    alt="Verzovací Rozhraní služby Dropbox"
) }}

V tomto rozhraní ale vidíš pouze verze *jednoho dokumentu* a navíc
nemůžeš tušit, ke které verzi se to vlastně chceš
vrátit. Nevidíš ani čím se jednotlivé verze liší.
Pro větší projekt by byl takový způsob práce
neefektivní.

Programátoři proto používají mocnější nástroje na
správu verzí (angl. version control system. VCS).
Asi nejpopulárnější z nich je Git, se kterým
se teď seznámíme.

!!! note ""
    Budeme hodně pracovat s příkazovou řádkou.
    Jestli se s ní ještě nekamarádíš, koukni se na
    [úvod]({{ lesson_url('beginners/cmdline') }}).

    Nezapomeň: `$` na začátku se nepíše;
    je tu proto, aby šlo poznat že jde o příkaz.


## Instalace

Popis instalace Gitu najdeš
[zde]({{ lesson_url('git/install') }}).
Jestli jsi instalaci přeskočil{{a}}, projdi si ji teď.


## Repozitář

Každý projekt, který budeš verzovat, musí mít pro sebe
vyhrazený adresář.
Vytvoř si tedy nový adresář a přepni se do něj (pomocí `cd`).
Pak vytvoř gitový <em>repozitář</em> (angl. repository)
pomocí příkazu `git init`:

```ansi
␛[36m$␛[0m git init
Initialized empty Git repository in ./.git/
```

Na první pohled to vypadá že se nic nestalo.
Tenhle příkaz totiž vytvořil *skrytý* adresář
`.git`, do kterého uložil nějaké informace.
Přesvědč se příkazem `ls -a` (Linux) nebo `dir /a` (Windows).
Adresář `.git` je schovaný proto, že
ho spravuje Git a ty bys v něm neměl{{a}} nic měnit.

V repozitáři zatím nic není.
Zkus to ověřit příkazem `git status`, který
vypisuje informace o stavu repozitáře:

```ansi
␛[36m$␛[0m git status
On branch master

Initial commit

nothing to commit (create/copy files and use "git add" to track)
```

*„On branch master”* říká něco o větvích, k tomu se vrátíme později.
*„Initial commit”* říká, že zatím nemáš uloženou žádnou revizi.
A *„nothing to commit”* říká, že je adresář
prázdný – nejsou tu žádné soubory u verzování.


## První revize

Teď si zkus do Gitu něco přidat!

Vytvoř soubor `basnicka.txt` a napiš do něj
nějakou básničku.
Měla by mít aspoň pět řádků, ať pak máme s čím pracovat.
Pak zkus znovu `git status`: Git oznámí,
že v adresáři je soubor, o kterém ještě „neví“.

<!-- XXX: Color coding! -->

```ansi
␛[36m$␛[0m git status
On branch master

Initial commit

Untracked files:
  (use "git add <file>..." to include in what will be committed)

        ␛[31mbasnicka.txt␛[m

nothing added to commit but untracked files present (use "git add" to track)
```

U každého nového souboru musíme Gitu říct, že
chceme jeho obsah sledovat.
Proveď to se svojí básničkou:

```ansi
␛[36m$␛[0m git add basnicka.txt
```

a znovu zkontroluj stav repozitáře:

```ansi
␛[36m$␛[0m git status
On branch master

Initial commit

Changes to be committed:
  (use "git rm --cached <file>..." to unstage)

        ␛[32mnew file:   basnicka.txt␛[m

```

To, co je zelené („changes to be committed“),
se přidá do další *revize* (angl. *commit*),
kterou vytvoříš.
Pojď tedy vytvořit revizi:

```ansi
␛[36m$␛[0m git commit
[master (root-commit) 7465169] První revize
 1 file changed, 11 insertions(+)
 create mode 100644 basnicka.txt
```

Po zadání tohoto příkazu se otevře editor,
do kterého musíš napsat nějaký popisek,
abys věděl{{a}}, co tahle revize obsahuje za změny.
Pro začátek napiš jen `První revize`.
Předvyplněné řádky začínající `#` nech být
(nebo vymaž, podle chuti – Git je ignoruje).
Pak soubor ulož, a zavři editor.

!!! note "Jak na editory?"

    Na Windows, máš-li
    [správně nastavený Git]({{ lesson_url('git/install') }}),
    se použije Poznámkový blok (Notepad) – stačí něco
    napsat, uložit (<kbd>Ctrl</kbd>+<kbd>S</kbd>) a zavřít
    (<kbd>Alt</kbd>+<kbd>F4</kbd>).

    Na Linuxu a macOS se objeví editor v příkazové řádce,
    který se jmenuje Nano.
    Pozná se tak, že v dolních dvou řádcích má malou nápovědu.
    Něco napiš, pomocí <kbd>Ctrl</kbd>+<kbd>O</kbd>
    soubor ulož, potvrď jméno souboru (<kbd>Enter</kbd>),
    a pomocí <kbd>Ctrl</kbd>+<kbd>X</kbd> editor zavři.

    Nemáš-li Git nastavený podle instrukcí, objeví se přímo
    v příkazové řádce Vim – poměrně složitý editor, který
    se teď učit nebudeme. Pozná se tak, že úplně
    spodní řádek je prázdný.
    V takovém případě stiskni
    <kbd>Esc</kbd>, napiš `:q!` (dvojtečka, Q, vykřičník),
    a potvrď pomocí <kbd>Enter</kbd>.
    Pak si nastav Git a zkus `git commit` znovu.


Znovu zkus vypsat stav repozitáře:

```ansi
␛[36m$␛[0m git status
On branch master
nothing to commit, working tree clean
```

Tenhle krátký výstup znamená, že od poslední revize
se nic nezměnilo.
Což dává smysl – poslední revizi jsi právě vytvořil{{a}}!

A co všechno je v téhle první/poslední revizi?
To ti poví příkaz `git show`:

```ansi
␛[36m$␛[0m git show
␛[33mcommit 7465169a16eb1ee39352ab3d23ced4d213960e9d␛[m
Author: Adéla Novotná <adela.novotna@example.cz>
Date:   Mon Mar 20 11:46:47 2017 +0100

    První revize

␛[1mdiff --git a/basnicka.txt b/basnicka.txt␛[m
␛[1mnew file mode 100644␛[m
␛[1mindex 0000000..18b2f69␛[m
␛[1m--- /dev/null␛[m
␛[1m+++ b/basnicka.txt␛[m
␛[36m@@ -0,0 +1,11 @@␛[m
␛[32m+␛[m␛[32mHaló haló␛[m
␛[32m+␛[m␛[32mco se stalo?␛[m
␛[32m+␛[m␛[32mKolo se mi polámalo␛[m
␛[32m+␛[m
␛[32m+␛[m␛[32mJaké kolo?␛[m
␛[32m+␛[m␛[32mFavoritka,␛[m
␛[32m+␛[m␛[32mpřeletěl jsem přes řidítka␛[m
␛[32m+␛[m
␛[32m+␛[m␛[32mCo jste dělal?␛[m
␛[32m+␛[m␛[32mBlbnul jsem,␛[m
␛[32m+␛[m␛[32mdo příkopy zahnul jsem␛[m
```

Vidíš unikátní
<span class="yellow">označení revize</span>,
pomocí kterého se vždy bude dát dostat k této konkrétní
verzi projektu.
Pak je tam jméno autorky a datum vytvoření,
popisek,
a nakonec shrnutí změn: byl přidán soubor <tt class="strong">basnicka.txt</tt>
s nějakým <span class="green">obsahem</span>.

!!! note ""
    Když je výpis moc dlouhý, můžeš se v něm pohybovat
    (<kbd>↓</kbd>, <kbd>↑</kbd>, <kbd>PgUp</kbd>, <kbd>PgDn</kbd>),
    a zpět se dostaneš klávesou <kbd>Q</kbd> jako *Quit*.

## Druhá revize

Udělej v básničce nějakou malou změnu – změň slovo,
uprav interpunkci nebo přidej sloku.
Pak se opět zeptej Gitu na stav repozitáře.

```ansi
␛[36m$␛[0m git status
On branch master
Changes to be committed:
  (use "git reset HEAD <file>..." to unstage)

        ␛[32mmodified:   basnicka.txt␛[m

```

Soubor je opět červený! Něco se v něm změnilo!
Ale co?
Na to nám odpoví příkaz <code>git diff</code>.

```ansi
␛[36m$␛[0m git diff
␛[1mdiff --git a/basnicka.txt b/basnicka.txt␛[m
␛[1mindex 18b2f69..9290e0e 100644␛[m
␛[1m--- a/basnicka.txt␛[m
␛[1m+++ b/basnicka.txt␛[m
␛[36m@@ -3,8 +3,7 @@␛[m ␛[mco se stalo?␛[m
 Kolo se mi polámalo␛[m
 ␛[m
 Jaké kolo?␛[m
␛[31m-Favoritka,␛[m
␛[31m-přeletěl jsem přes řidítka␛[m
␛[32m+␛[m␛[32mFavoritka! Přeletěl jsem přes řidítka!␛[m
 ␛[m
 Co jste dělal?␛[m
 Blbnul jsem,␛[m
```

Změny se ukazují po řádcích.
Červeně, s <tt class="red">-</tt>, jsou ukázány
odebrané řádky; zeleně s <tt class="green">+</tt>
řádky přidané.

!!! note ""
    Změnilo-li se na řádku jen jedno slovo nebo i písmeno,
    celý řádek se ukáže jako smazaný a zase přidaný.
    Dá se to nastavit i jinak, když je potřeba,
    ale je dobré si na tento standard zvyknout.

Takhle se dá jednoduše zjistit, co se dělo od poslední verze.
Když ti program přestane fungovat (a v poslední uložené
revizi fungoval), použij <code>git diff</code> –
v jedné ze změn musí být chyba!

!!! note ""
    Řádek začínající <tt class="blue">@@</tt> říká,
    kde v souboru změna je (u mě začínal vypsaný kousek
    souboru řádkem 3, a měl 8 řádků; v nové verzi je
    opět od 3. řádku, ale má už jen 7 řádků).

Jsi-li se změnami spokojen{{a}}, řekni Gitu ať je
použije v další revizi:

```ansi
␛[36m$␛[0m git add basnicka.txt
```

A pro úplnost se znovu koukni co říká
`status` – co je zelené, přidá se do další
revize.

```ansi
␛[36m$␛[0m git status
On branch master
Changes to be committed:
  (use "git reset HEAD <file>..." to unstage)

        ␛[32mmodified:   basnicka.txt␛[m

```

Než uděláš druhou revizi, ještě řeknu něco o tom,
jak správně psát k revizím popisky.
Na to je totiž úzus, který téměř všichni programátoři
respektují: na prvním řádku je krátké shrnutí změn,
následuje prázdný řádek, a pak detailnější popis důvodů
ke změně a případně změny samotné.
Snaž se délku řádků držet do zhruba 70 znaků;
vodítkem můžou být předvyplněné řádky začínající `#`.
Nemá cenu popisovat co je jasné ze změn samotných,
zajímavé jsou hlavně širší souvislosti a důvody ke změnám.
Cokoli, co může přijít vhod až se změny bude snažit někdo pochopit.
(Ten někdo můžeš být klidně ty, za pár měsíců.)

Můj popisek bude znít takhle:

```plain
Druhá sloka: Sloučení posledních dvou řádků

Sloučení řádků rozbíjí monotónnost formy básně – nestejný počet
veršů ve sloce je prý moderní. (Ale, co si budeme povídat, hlavní 
důvod je líp ukázat co dělá `git diff`.)

Použití vykřičníku místo čárky zdůrazňuje naléhavost situace.
```

!!! note ""
    Nebude-li se ti někdy dařit shrnout změnu
    v 70 znacích, zamysli se, jestli neděláš moc velkou
    změnu najednou – např. "změna řetězce X
    a dopsání nového cyklu Y" by bývalo lepší uložit
    jako dvě různé revize.

Pomocí `git commit` vytvoř druhou revizi.
Pak ji zkontroluj:

```ansi
␛[36m$␛[0m git show
␛[33mcommit 303761b29fb6ef0bfd961b311131c224b918ffc5␛[m
Author: Adéla Novotná <adela.novotna@example.cz>
Date:   Mon Mar 20 11:46:47 2017 +0100

    Druhá sloka: Sloučení posledních dvou řádků
    
    Sloučení řádků rozbíjí monotónnost formy básně – nestejný počet
    veršů ve sloce je prý moderní. (Ale, co si budeme povídat, hlavní
    důvod je líp ukázat co dělá `git diff`.)
    
    Použití vykřičníku místo čárky zdůrazňuje naléhavost situace.

␛[1mdiff --git a/basnicka.txt b/basnicka.txt␛[m
␛[1mindex 18b2f69..9290e0e 100644␛[m
␛[1m--- a/basnicka.txt␛[m
␛[1m+++ b/basnicka.txt␛[m
␛[36m@@ -3,8 +3,7 @@␛[m ␛[mco se stalo?␛[m
 Kolo se mi polámalo␛[m
 ␛[m
 Jaké kolo?␛[m
␛[31m-Favoritka,␛[m
␛[31m-přeletěl jsem přes řidítka␛[m
␛[32m+␛[m␛[32mFavoritka! Přeletěl jsem přes řidítka!␛[m
 ␛[m
 Co jste dělal?␛[m
 Blbnul jsem,␛[m
```

## Diagram
Pro lepší pochopení, co dělají jednotlivé příkazy a v jakém
stavu můžou být soubory/změny, přikládám tento diagram:

{{ figure(
    img=static('diagram.png'),
    alt="Diagram revizí"
) }}

## Log

Teď, když máme za sebou první(ch) pár revizí,
si ukážeme několik příkazů, které nám umožní se
v nich orientovat.
První z nich je <code>git log</code>.

```ansi
␛[36m$␛[0m git -c color.ui=always -c color.diff=always -c color.status=always log
␛[33mcommit 303761b29fb6ef0bfd961b311131c224b918ffc5␛[m
Author: Adéla Novotná <adela.novotna@example.cz>
Date:   Mon Mar 20 11:46:47 2017 +0100

    Druhá sloka: Sloučení posledních dvou řádků
    
    Sloučení řádků rozbíjí monotónnost formy básně – nestejný počet
    veršů ve sloce je prý moderní. (Ale, co si budeme povídat, hlavní
    důvod je líp ukázat co dělá .)
    
    Použití vykřičníku místo čárky zdůrazňuje naléhavost situace.

␛[33mcommit 7465169a16eb1ee39352ab3d23ced4d213960e9d␛[m
Author: Adéla Novotná <adela.novotna@example.cz>
Date:   Mon Mar 20 11:46:47 2017 +0100

    První revize
```

Git log vypíše všecny revize od té nejnovější až po
úplný začátek projektu.

Až budeš mít verzí tolik, že se nevejdou najednu
na obrazovku, můžeš se v logu pohybovat pomocí šipek a
<kbd>PgUp</kbd>/<kbd>PgDn</kbd>.
„Ven“ se dostaneš klávesou <kbd>q</kbd>.


!!! note ""
    Je spousta možností jak vypisovat historii pomocí `git log`.
    Všechno je podrobně – možná až moc podrobně –
    popsáno v dokumentaci; stačí zadat `git help log`.
    „Ven“ z dokumentace se opět dostaneš klávesou <kbd>q</kbd>.

    Já často používám `git log --oneline --graph --decorate --cherry-mark --boundary`.
    Chceš-li tyhle možnosti studovat, začni v tomto
    pořadí, a dej si pauzu vždycky když přestaneš
    rozumět :)

Když se na nějakou verzi budeš chtít podívat podrobněji,
napiš `git show 5ff0b`, kde místo `5ff0b
uveď prvních několik čísel z <span class="yellow">označení revize</span>.

## gitk

Z příkazové řádky se dá vyčíst všechno potřebné,
ale chce to trochu praxe.
Někdy je přehlednější použít grafické „klikátko“ jménem
*gitk*, které se dá spustit příkazem
`gitk --all`:

```console
$ gitk --all
```

{{ figure(
    img=static('gitk.png'),
    alt="",
) }}


Tenhle program vypadá celkem šeredně (skoro jako by ho
psali programátoři, které místo designu zajímá co je
„vevnitř“), ale pro naše účely postačí.
Zkus se v něm trochu zorientovat, pak ho zavři,
udělej dalších pár revizí, a koukni se na ně přes
`git log` a `gitk --all`.

## Závěr

A to je všechno, co z Gitu zatím budeš potřebovat.
Vždycky, když uděláš <code>git add <var>soubor</var></code>
a `git commit`,
aktuální verze souborů se uloží, a už nejde (jednoduše)
smazat – pokud nesmažeš celý adresář `.git`.
Jednotlivé verze, a změny od posledního uložení,
si umíš i prohlížet.

Možná to všechno zní jako zbytečně moc práce.
Máš tak trochu pravdu – naše projekty jsou zatím
dost malé na to, aby se jen pro ně vyplatilo učit Git.
Ale je dobré ho používat už od začátku.
Až bude správa verzí opravdu potřeba, bude se tenhle
trénink hodit.

Takže, odteď, kdykoliv uděláš v rámci PyLadies funkční
verzi nějakého programu, pomocí `git add` a `git commit` si ji ulož do Gitu.
