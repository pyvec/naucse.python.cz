{% set coach_username = var('coach-username') or 'naucse' %}

# Spolupráce

„Opravdové” programy zřídka vznikají prací jednoho člověka.
Víc hlav víc ví, a tak je dobré si na projekt vytvořit tým.

Každý člen týmu potřebuje mít přístup k práci ostatních.
K tomu se dá použít Git: někde na internetu si zařídí *sdílený repozitář*,
se kterým se všichni budou synchronizovat.

> [note] Pro samostudium
> Pokud materiály čteš z domu a máš možnost se
> v budoucnu dostat na nějaký sraz, zatím tuhle sekci přeskoč.
> Na sraze pak popros zkušenější programátory, aby ti pomohli.
> (Nechystáš-li se na sraz, můžeš pokračovat –
> zvládnout se to dá.)

> [note] Pro kouče
> Udělej na GitHubu repozitář jménem `prezencka` a dej do
> něj soubor se svým jménem. Příklad je na
> [naucse/prezencka](https://github.com/naucse/prezencka).
> Nasdílej s účastníky příkaz na jeho naklonování (přes https).


## Open Source

Nejde mluvit o Gitu a spolupráci a nezastavit se chvíli u otevřeného
zdrojového kódu.
První programy vznikaly v akademické sféře, kde byly zcela přirozeně sdíleny,
jako je to s poznatky mezi vědci běžné.
50\. a 60. léta byla obdobím velké kreativity, kdy vzniklo mnoho z konceptů
a technologií, které dnes používáme.
Pak se začalo programování postupně komercializovat a firmy začaly zdrojový
kód skrývat jako konkurenční výhodu.
Do té doby víceméně jednolitá komunita programátorů byla nucena se rozdělit.

Některým programátorům tohle skrývání kódu hluboce vadilo.
Roku 1985 publikoval
[Richard Stallman](https://en.wikipedia.org/wiki/Richard_Stallman)
[GNU Manifesto](https://www.gnu.org/gnu/manifesto.en.html),
kde vysvětlil, proč hodlá vytvořit operační systém s otevřeným kódem a
odstartoval tak hnutí svobodného softwaru.
To prosazuje 4 následující svobody (převzato
z [Wikipedie](https://cs.wikipedia.org/wiki/Svobodn%C3%BD_software)):

<ol start="0">
<li>svoboda používat program za jakýmkoliv účelem,</li>
<li>svoboda studovat, jak program pracuje a možnost přizpůsobit ho svým potřebám,</li>
<li>svoboda redistribuovat kopie programu,</li>
<li>svoboda vylepšovat program a zveřejňovat zlepšení, aby z nich mohla mít prospěch celá komunita.</li>
</ol>

Dnes je spousta projektů s otevřeným zdrojovým kódem (tzv. *open-source* projektů)
dostupná na Internetu a každý je používáme.
Jejich další sdílení je upraveno jednou z licencí,
které tyto základní svobody zaručují.

Ne všechny jsou v Pythonu (a těm co jsou zatím
nebudeš všem rozumět). Ne všechny jsou v Gitu.
Ne všechny jsou kvalitní – protože si
každý může zveřejnit co chce, na Internetu se válí
spousta nedodělků, opuštěných nápadů a nepodařených experimentů.
A bohužel, ne všechny projekty mají přátelské autory.

Na druhou stranu ale open-source programy
mají svoje výhody: nejenom že se z nich může kdokoli
učit, ale každý může i zkontrolovat, jestli
dělají to, co dělat mají.
Populární open-source programy tě například
pravděpodobně nebudou špehovat (tj. hlásit autorovi,
co na počítači děláš), ani většinou neobsahují
reklamy: kdyby to dělaly, najde se
někdo kdo tyhle „funkce” odstraní a lidi – časem –
začnou používat opravenou verzi.

Některé příklady populárních open-source projektů:

* [Mozilla Firefox](https://github.com/mozilla/gecko-dev),
  [Chromium](https://chromium.googlesource.com/chromium/src.git)
  (prohlížeče)
* [VS Code - OSS](https://github.com/Microsoft/vscode),
  [Atom](https://github.com/atom/atom),
  [gedit](https://github.com/GNOME/gedit)
  (textové editory)
* [CPython](https://github.com/python/cpython)
  (jazyk Python)
* [Linux](https://github.com/torvalds/linux),
  [Android](https://github.com/aosp-mirror)
  (jádra operačních systémů)
* [Pytest](https://github.com/pytest-dev/pytest/)
  (pythonní knihovna na testování)
* [Django](https://github.com/django/django),
  [Flask](https://github.com/mitsuhiko/flask),
  [Requests](https://github.com/kennethreitz/requests)
  (webové knihovny pro Python)
* [NumPy](https://github.com/numpy/numpy),
  [Jupyter](https://github.com/jupyter/notebook),
  [Matplotlib](https://github.com/matplotlib/matplotlib)
  (pythonní knihovny pro vědce a analytiky)
* [Materiály](https://github.com/pyvec/naucse.python.cz) k tomuto kurzu

Jak vidno z posledního příkladu, nejen softwarové
projekty se dají vést takhle veřejně.
Tento kurz vychází z principů open source:
všechno know-how je sdílené a budeme rádi, když
se zapojíš.

Až příště uvidíš v materiálech chybu (nebo jestli o nějaké víž už teď),
dnes se dozvíš, jak ji opravit!

A co tvůj kód? Chceš ho taky dávat takhle veřejně k dispozici?
Nutné to samozřejmě není – Git se dá používat i
v uzavřeném týmu – ale na druhou stranu,
máš důvod proč to nedělat?
Zveřejňovat zdrojový kód se hodí už jen pro to,
aby ti s ním mohli zkušenější programátoři snadněji pomáhat.


## GitHub

Na Internetu existuje spousta stránek, kam se dají nahrávat gitové repozitáře
s kódem – např. [GitLab](https://gitlab.com/),
[BitBucket](https://bitbucket.org),
[Pagure](https://pagure.io/) nebo
[Launchpad](https://launchpad.net/).
Aktuálně nejpopulárnější je ale [GitHub](https://github.com), který si tady
ukážeme.

Jestli ještě nemáš uživatelský účet na [github.com](https://github.com), jdi
tam a založ si ho.


## Naklonování repozitáře <small>(<code>git clone</code>)</small>

Pro začátek zkusíme práci s repozitářem, který už vytvořil někdo jiný.
V příkazové řádce zadej příkaz, který ti oznámí kouč; něco jako

```console
$ git clone https://github.com/{{coach_username}}/prezencka
```

Vytvoří se ti nový repozitář – adresář se jménem
`prezencka`, ve kterém je nějaký soubor.


Na URL (adresu), kterou jsi v tomhle příkladě
použil{{a}}, se můžeš podívat i v prohlížeči.
Uvidíš seznam souborů a spoustu odkazů k
informacím o repozitáři (například pod „commits”
je historie).

Přepni se do nového adresáře (`cd prezencka`)
a zkus se podívat na historii (`gitk` nebo `git log`).
Možná je krátká, ale hlavně, že nějaká je.
Máš na počítači kopii projektu, který založil někdo jiný!

Jak už napovídá název repozitáře, tvůj příspěvek do tohoto projektu bude
zápis do prezenčky: konkrétně přidání souboru s tvým jménem.
Jméno je to proto, aby nedocházelo ke kolizím: potřebujeme, aby příspěvky od
všech lidí, kteří prochází tenhle kurz, byly jiné.

Tvůj příspěvek bude ovšem veřejně vystaven na internetu.
Pokud nechceš vystavovat svoje občanské jméno, použij místo něj klidně
přezdívku, oblíbené jídlo nebo pár náhodných písmen. Ale:
* když budeš pojmenovávat soubor, buď originální, aby nedošlo ke konfliktům, a
* nesdílej nic, co nemáš právo sdílet (např. texty moderních písní).


## Vytvoření větve

Pomocí `git branch` zjisti, na jaké jsi aktuálně větvi.
Měla by to být větev `master`.

Tuhle „základní“ větev je dobré používat jen na revize, na kterých se už
shodl celý tým.
Proto když chceš do projektu přispět, jako první krok si pro svůj příspěvek
udělej novou větev a přepni se do ní.
Například pomocí:

```console
$ git branch pridani-jmena
$ git checkout pridani-jmena
```


## Posílání změn <small>(<code>git push</code>)</small>

Teď se do projektu zapoj.
Přidej soubor pojmenovaný podle tvého jména (nebo přezdívky)
a dej ho do gitu (<code>git add <var>...</var></code>; <code>git commit</code>).

Teď zbývá „jen” změnu začlenit do původního sdíleného repozitáře.
To ale není jen tak: repozitář, který jsi
naklonoval{{a}}, patří koučovi. A tomu by se asi
nelíbilo, kdyby kdokoliv na Internetu mohl přijít
a nahrát mu do repozitáře změny.

Spousta míst na Internetu (blogy, zpravodajství, e-shopy) funguje tak, že
vybraná skupina lidí, „editorů“, má právo měnit obsah, jak se jim líbí.
Takovým editorům musí správce projektu věřit, než jim přístup povolí.

S Gitem se používá trošku jiný mechanismus:
změny nahraješ do *vlastního* sdíleného
repozitáře, který máš právo měnit jen ty.
Majiteli původního projektu pak napíšeš
žádost o začlenění těch změn (angl. *pull request*).
Může to být třeba mail se slovy „Hele, na té a té
adrese mám nějaké změny, které by se ti mohly hodit!
Přidej je do svého projektu!”

Výhoda je v tom, že se do projektu – pokud je
veřejný – může zapojit kdokoliv. Nemusíš se
předem ptát, nemusíš dokazovat že jsi důvěryhodná
osoba, stačí něco změnit a poslat.
Jestli se změna bude autorům projektu líbit nebo
ne, to už je jiná věc – ale můžou posuzovat samotnou
změnu, ne důvěryhodnost jejího autora.

Služby jako [github.com](https://github.com/)
ti umožňují si udělat vlastní sdílený repozitář (který bude k dispozici na
internetu) a zjednodušují začleňování změn (místo posílání mailů stačí
zmáčknout tlačítko). Pojďme se podívat, jak na to.

Přihlaš se na GitHub a pak zajdi na adresu
kterou jsi použil{{a}} pro `git clone`.
Vlevo nahoře najdi tlačítko „Fork” a klikni na něj.
Tím si vytvoříš na GitHubu vlastní kopii repozitáře:
adresa by měla být něco jako
<code>https://github.com/<i>tvojejmeno</i>/prezencka</code>.


> [note]
> Kdybys měl{{a}} v různých kopiích repozitáře zmatek,
> přijde vhod malé vysvětlení: jedna kopie je původní
> projekt na GitHubu, kam správce projektu dává
> aktuální „oficiální“ nebo „hlavní“ verzi. Další kopie na GitHubu
> je „tvoje“ a můžeš si do ní nahrát co chceš
> (nejčastěji v ní ale zveřejňuješ změny, které můžou
> být užitečné pro ostatní).
> Tyhle dvě  kopie existují na serverech GitHubu a jsou volně dostupné
> přes internet.
>
> Třetí kopii repozitáře pak máš u sebe na počítači.
> K té se dostaneš jen ty.
>
> Z „hlavní“ verze si stáhneš práci ostatních členů týmu;
> do *tvého* projektu na GitHubu dáváš své změny, aby je ostatní mohli
> schválit a začlenit do „hlavní“ verze.
>
> {{ figure(
    img=static('gh-workflow-diagram.svg'),
    alt='Diagram tří repozitářů'
) }}

A teď, jak z tvého počítače nahrát změny na GitHub?
Git si u každého repozitáře na tvém počítači
pamatuje adresy, odkud se dají stahovat
a kam se dají posílat změny.
Seznam těchhle adres ti ukáže příkaz `git remote -v`.
Třeba:

```console
$ git remote -v
origin  https://github.com/{{coach_username}}/prezencka (fetch)
origin  https://github.com/{{coach_username}}/prezencka (push)
```

Tenhle výstup znamená, že pod zkratkou „origin”
se schovává adresa, ze které jsi repozitář
naklonoval{{a}}.

Přidej si podobnou zkratku pro vlastní repozitář na GitHubu.
Nezapomeň nahradit <i>tvojejmeno</i> za jméno účtu,
který máš na GitHubu ty. (Pozor, v příkazu je <i>tvojejmeno</i> dvakrát!)

<div class="highlight codehilite">
<pre><code><span class="gp">$</span> git remote add <i>tvojejmeno</i> https://github.com/<i>tvojejmeno</i>/prezencka
</code></pre></div>

a zkontroluj si, že se to povedlo:

<div class="highlight codehilite">
<pre><code><span class="gp">$</span> git remote -v
<span class="go">origin  git@github.com:{{coach_username}}/prezencka.git (fetch)</span>
<span class="go">origin  git@github.com:{{coach_username}}/prezencka.git (push)</span>
<span class="go"><i>tvojejmeno</i>      https://github.com/<i>tvojejmeno</i>/prezencka (fetch)</span>
<span class="go"><i>tvojejmeno</i>      https://github.com/<i>tvojejmeno</i>/prezencka (push)</span>
</code></pre></div>

Tolik k nastavení – `git remote add`
stačí udělat jednou pro každý repozitář.
Pak už můžeš změny nahrávat pomocí:


<div class="highlight codehilite">
<pre><code><span class="gp">$</span> git push <i>tvojejmeno</i> pridani-jmena
</code></pre></div>

což znamená: pošli na adresu uloženou pod zkratkou
<code><i>tvojejmeno</i></code>
větev `pridani-jmena`.

Funguje? Podívej se na
<code>https://github.com/<i>tvojejmeno</i>/prezencka</code>
v prohlížeči a ujisti se, že tam tvoje změny jsou.


## Žádost o začlenění <small>(<em>pull request</em>)</small>

Teď zbývá požádat autory původního projektu,
aby změny z tvého sdíleného repozitáře přidali do svojí kopie.
GitHub na to má mechanismus zvaný *pull request* (žádost o začlenění).

Jdi na stránku původního projektu (na adresu,
kterou jsi použil{{a}} na začátku pro
`git clone`).
Měl{{a}} bys tam vidět oznámení o své nově nahrané větvi
s velkým zeleným tlačítkem *Compare & pull request*.
Klikni na něj. Pokud chceš, tak dopiš/změň popisek
toho, co tahle změna obnáší.
Pak zmáčkni další tlačítko.

> [note]
> Jestli tlačítko *Compare & pull request* nevidíš, běž na adresu
> *své* kopie repozitáře a stiskni tlačítko *New pull request*.
> Vyber, co kam chceš začlenit, dopiš/změň popisek a pak zmáčkni
> *Create pull request*.

Hotovo; teď je na autorech projektu, aby
se na změny podívali a přijali – nebo začali diskusi
o tom, jak je ještě vylepšit.
(Diskutovat se dá na stránce *pull requestu* nebo přes mail.)

> [note] Pro samostudium
> Procházíš-li materiály z domu, musíš teď počkat,
> než si někdo tvé žádosti všimne a začlení ji.
> To může trvat i pár dní; kdyby to bylo přes týden,
> tak se na stránce *pull requestu* zkus připomenout.

U přidání jména do prezenčky se to asi nestane, ale kdybys potřeboval{{a}}
na změně před začleněním ještě trochu zapracovat (třeba i po
pár dnech diskuse), nebyl by to problém.
Přepni se na svém počítači do větve `pridani-jmena`, udělej další revize,
a pomocí <code>git push <i>tvojejmeno</i> pridani-jmena</code>
*pull request* aktualizuj.


## Aktualizace <small>(<code>git pull</code>)</small>

Když budou tvé změny – a změny od ostatních –
začleněné, můžeš si aktualizovat lokální repozitář. (To je ten,
který máš u sebe na počítači.)

Nejdřív se přepni zpět do větve `master`.
Teď už nebudeš pracovat na `pridani-jmena`; tahle větev už je odeslaná.

To se dělá příkazem
`git pull origin master` (stáhni změny
z větve „master” z adresy pod zkratkou „origin”).
Pomocí `gitk --all` nebo `git log`
se můžeš podívat, jak se projekt mezitím vyvinul.

Tohle `git pull` je dobré provést vždycky předtím, než začneš pracovat na
nové změně/větvi.
Zaručíš tím, že projekt, který měníš, je „čerstvý“.

Gratuluji! Právě jsi {{gnd('prošel', 'prošla')}} „kolečkem“,
které většina programátorů dělá denně: udělání nějaké změny,
odeslání kolegům na kontrolu a začlenění a stažení změn od ostatních.


## Hlášení chyb <small>(<em>issues</em>)</small>

Občas nastane situace, kdy v nějakém projektu
na GitHubu najdeš chybu, ale nemáš čas nebo
znalosti, abys ji opravil{{a}}. V takovém případě
často na GitHubu na stránce projektu pod záložkou *Issues*
najdeš seznam nahlášených problémů.
Nenajdeš-li mezi nimi „svoji” chybu, můžeš ji
nahlásit – stačí kliknout na *New Issue*
a můžeš psát, kdy chyba nastává, co program dělá
špatně a co by měl dělat místo toho.

> [note]
> Některé projekty nepoužívají Issues na GitHubu.
> Kdybys záložku Issues {{gnd('nenašel', 'nenašla')}}, podívej se
> do dokumentace projektu, jestli tam není odkaz na
> seznam chyb.

## README: Informace pro ostatní

Pokud vytváříš projekt a chceš, aby do něj přispívali i ostatní,
je potřeba aby věděli, co tvůj projekt dělá, k čemu se hodí,
jak se používá a podobně.

Na základní informace o projektu/repozitáři se používá soubor `README`
(z angl. _read me_, _čti mě_).
Do tohoto souboru patří mj.:

* název projektu,
* stručný popis projektu (jedna až dvě věty),
* krátký návod k instalaci projektu,
* krátký návod ke spuštění projektu,
* krátký návod k používání projektu, případně odkaz na rozsáhlejší dokumentaci,
* pokud má projekt testy, informace o tom, jak je spustit,
* informace o tom, jak se zapojit do vývoje projektu,
* informace o autorech projektu,
* informace o licenci (více se licencích dozvíš později).

README by mělo být členěné a jeho přečtení by nemělo zabrat uživateli hodinu,
většinou stačí krátké úderné informace s případným odkazem někam dál.
Nemusíš tedy například vysvětlovat v každém projektu, jak se instaluje Python.
Stačí říct, že Python je potřeba (a v jaké verzi)
a odkázat uživatele na patřičný návod.
Je také třeba brát v úvahu, kdo bude README číst.
Píšeš-li program pro jiné vývojářky a vývojáře,
často nemusíš zabrušovat do detailů.

GitHub (a spousty jiných podobných služeb) umožňuje pro README použít nějaký
značkovací jazyk, například [Markdown](https://cs.wikipedia.org/wiki/Markdown).
Je možné pak používat nadpisy, obrázky apod.

A v neposlední řadě: aby se do projektu mohl zapojit
kdokoli z celého světa, bývají open-source projekty v angličtině.
Jména proměnných, komentáře, dokumentace – všechno
je primárně v anglické verzi.
Tenhle kurz je česky, aby byly začátky jednodušší,
ale jestli se ti programování zalíbilo a chceš
v něm po kurzu pokračovat dál, bez angličtiny
to bude velice složité.

## Licence

Aby sdílení fungovalo i pro právní stránce,
nestačí když nahraješ kus kódu na Internet.
Musíš taky oficiálně oznámit, že si s ním ostatní můžou hrát.
Na svůj kód totiž máš autorské právo, podle kterého ostatní nesmí tvůj program
používat, natož vylepšovat, dokud jim to nepovolíš.
Pro formální udělení tohohle povolení se používají *licence*, které píšou
právníci.

Problematika licencí může být, bohužel, docela složitá.
Když to ale zjednodušíme na minimum, budeš
chtít jen zajistit, aby každý mohl tvůj výtvor
používat, učit se z něj, předávat ho dál
a vylepšovat ho. V tom případě vyber třeba
licenci [MIT](https://choosealicense.com/licenses/mit/).

> [note]
> Pokud chceš navíc zabránit tomu, že si tvůj kód
> někdo vezme a začne ho „vylepšovat“ a vydělávat na
> něm, aniž by se o vylepšení podělil s ostatními,
> zkus licenci [AGPL](https://choosealicense.com/licenses/agpl-3.0/).

> [note]
> A tyto materiály jsou pod ještě jinou licencí –
> [CC BY-SA](https://choosealicense.com/licenses/cc-by-sa-4.0/) –
> protože výše jmenované licence jsou dělané na programy, ne na text.

Kód se nejčastěji licencuje tak, že text licence
dáš do souboru jménem `LICENSE` a přidáš do Gitu.
Je dobré licenci zmínit i v souboru `README`.

Chceš-li si o licencích přečíst něco víc, odkážu tě na
[choosealicense.com](http://choosealicense.com/),
případně [creativecommons.org](http://creativecommons.org/choose/)
a [opensource.org](https://opensource.org/licenses).
