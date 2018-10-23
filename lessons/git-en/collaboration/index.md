{% set coach_username = var('coach-username') or 'encukou' %}

# Collaboration

“Real” programs rarely are created by a single person.
Two heads are better than one, so it's better to work on a projekt in a team.

Each team member needs to be able to share their progress with others.
Git can be used exactly for that: you can set up a *shared repository* online
that your team members will synchronize with.

> [note] Self-study
> If you study at home but you plan to attend a coding event soon,
> skip this section for now.
> Ask more experienced attendees for help when you get the chance.
> (Otherwise, keep reading. You can do this.)

> [note] For mentors
> Create a GitHub repository called `attendance`. Add a new file
> with your name to the repository. See an example here:
> [encukou/attendance](https://github.com/encukou/attendance).
> Share the command to clone your repository using https with other attendees.


## Open-Source

We can't talk about Git and collaboration without discussing the open-source code first.
The first programs came from the academia and were shared freely with the wider community,
as is common with any scientific research.
The 1950s and 1960s was the time of great creativity.
Many concepts and technologies that we use today originate in that era.
As programming began to move to the commercial sphere, the source code developed
by companies wasn't being shared anymore in order to maintain competitive advantage.
The community of programmers, united in the past, has split up.

Some programmers loathed the closed source approach.
In 1985, [Richard Stallman](https://en.wikipedia.org/wiki/Richard_Stallman)
published [GNU Manifesto](https://www.gnu.org/gnu/manifesto.en.html)
where he proposed to create an open-source operating system, 
thus starting the free software movement.
The manifesto lists the following four freedoms (taken from
[Wikipedia](https://en.wikipedia.org/wiki/Free_software)):

<ol start="0">
<li>freedom to run the program for any purpose.</li>
<li>freedom to study how the program works, and change it to make it do what you wish.</li>
<li>freedom to redistribute and make copies so you can help your neighbor.</li>
<li>freedom to improve the program, and release your improvements (and modified versions in general)
to the public, so that the whole community benefits.</li>
</ol>

Today, many open-source projects are available freely on the Internet for anone to use them.
Their availability is governed by one of the licenses that guarantee these fundamental freedoms.

Not all these projects were created using Python (and for now,
it might be difficult for you to understand those that were).
Not all are hosted using Git.
Neither are all of a high quality; anyone can publish any piece of their own work,
so the Internet is filled with unfinished projects, abandoned ideas and failed experiments.
Unfortunatelly, not all authors are friendly either.

On the other hand, open-source applications have their benefits too:
not only can they help others to learn how to create them,
anyone can check that the code is doing exactly what it's supposed to.
For example, popular open-source applications are unlikely to spy on you
(i.e. record what you do with your computer and share that with somebody else).
Advertisements are rarely a part of the apps too.
Were any of these “features” included, somebody would remove them
and release their alternative version of the project eventually.

Few examples of popular open-source projects:

* [Mozilla Firefox](https://github.com/mozilla/gecko-dev),
  [Chromium](https://chromium.googlesource.com/chromium/src.git)
  (internet browsers)
* [Atom](https://github.com/atom/atom),
  [gedit](https://github.com/GNOME/gedit)
  (text editors)
* [CPython](https://github.com/python/cpython)
  (the Python language)
* [Linux](https://github.com/torvalds/linux),
  [Android](https://github.com/aosp-mirror)
  (kernels of operating systems)
* [Pytest](https://github.com/pytest-dev/pytest/)
  (test library for Python)
* [Django](https://github.com/django/django),
  [Flask](https://github.com/mitsuhiko/flask),
  [Requests](https://github.com/kennethreitz/requests)
  (web libraries for Python)
* [NumPy](https://github.com/numpy/numpy),
  [Jupyter](https://github.com/jupyter/notebook),
  [Matplotlib](https://github.com/matplotlib/matplotlib)
  (Python libraries for scientists and analysts)
* [Materials](https://github.com/pyvec/naucse.python.cz) for this course

As shown by the last example, the free and open model is not only limited to software projects.
This course is based on the open-source principles:
all know-how is shared and we will be glad when you get involved.

Today you'll learn how you can collaborate on a Git-hosted project.
The next time you notice an error in these materials (or if you know of one already),
you'll be able to fix it yourself!

Finally, what about your own code? Would you like to share it freely in a similar fashion?
It's not mandatory of course, Git can be used even by a closed team; on the other hand,
why wouldn't you share it?
Making your code public can have one more benefit:
more experienced programmers can help you improve it very easily.


## GitHub

Na Internetu existuje spousta stránek, kam se dají nahrávat gitové repozitáře
s kódem – např. [GitLab](https://gitlab.com/),
[BitBucket](https://bitbucket.org),
[Pagure](https://pagure.io/) nebo
[Launchpad](https://launchpad.net/).
Aktuálně nejpopulárnější je ale [GitHub](https://github.com), který si tady
ukážeme.

Jestli ještě nemáš uživatelský účet na [github.com](https://github.com), jdi
tam a založ si ho.


## Naklonování repozitáře <small>(<code>git clone</code>)</small>

Pro začátek zkusíme práci s repozitářem, který už vytvořil někdo jiný.
V příkazové řádce zadej příkaz, který ti oznámí kouč; něco jako

```console
$ git clone https://github.com/{{coach_username}}/attendance
```

Vytvoří se ti nový repozitář – adresář se jménem
`attendance`, ve kterém je nějaký soubor.


Na URL (adresu), kterou jsi v tomhle příkladě
použil{{a}}, se můžeš podívat i v prohlížeči.
Uvidíš seznam souborů a spoustu odkazů k
informacím o repozitáři (například pod “commits”
je historie).

Přepni se do nového adresáře (`cd attendance`)
a zkus se podívat na historii (`gitk` nebo `git log`).
Možná je krátká, ale hlavně, že nějaká je.
Máš na počítači kopii projektu, který založil někdo jiný!


## Posílání změn <small>(<code>git push</code>)</small>

Teď se do projektu zapoj.
Přidej soubor se svým jménem (nebo přezdívkou)
a dej ho do gitu (`git add jmeno.txt`, `git commit`).

Teď zbývá “jen” změnu začlenit do původního sdíleného repozitáře.
To ale není jen tak: repozitář, který jsi
naklonoval{{a}}, patří koučovi. A tomu by se asi
nelíbilo, kdyby kdokoliv na Internetu mohl přijít
a nahrát mu do repozitáře změny.

Spousta míst na Internetu funguje tak, že vybraná
skupina lidí má “přístup”: můžou dělat změny,
jak se jim líbí.

S Gitem se používá jiný přístup:
změny nahraješ do *vlastního* sdíleného
repozitáře a majiteli původního projektu napíšeš
žádost o začlenění těch změn (angl. *pull request*).
Může to být třeba mail se slovy “Hele, na té a té
adrese mám nějaké změny, které by se ti mohli hodit!
Přidej je do svého projektu!”

Výhoda je v tom, že se do projektu – pokud je
veřejný – může zapojit kdokoliv. Nemusíš se
předem ptát, nemusíš dokazovat že jsi důvěryhodná
osoba, stačí něco změnit a poslat.
Jestli se změna bude autorům projektu líbit nebo
ne, to už je jiná věc. Ale záleží hlavně na samotné
změně, ne na tom, kdo ji udělal.

Služba [github.com](https://github.com/)
ti umožňuje si udělat vlastní sdílený repozitář a zjednodušuje
začleňování změn (místo posílání mailů stačí
zmáčknout tlačítko). Pojďme se podívat, jak na to.

Přihlaš se na GitHub a pak zajdi na adresu
kterou jsi použil{{a}} pro `git clone`.
Vlevo nahoře najdi tlačítko “Fork” a klikni na něj.
Tím si vytvoříš na GitHubu vlastní kopii repozitáře:
adresa by měla být něco jako
<code>https://github.com/<i>tvojejmeno</i>/attendance</code>.


> [note]
> Kdybys měl{{a}} v různých kopiích repozitáře zmatek,
> přijde vhod malé vysvětlení: jedna kopie je původní
> projekt na GitHubu, kam správce projektu dává
> aktuální "oficiální verzi". Další kopie na GitHubu
> je "tvoje" a můžeš si do ní nahrát co chceš
> (nejčastěji v ní ale zveřejňuješ změny, které můžou
> být užitečné pro ostatní). A třetí kopii repozitáře
> máš u sebe na počítači.

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
origin  https://github.com/{{coach_username}}/attendance (fetch)
origin  https://github.com/{{coach_username}}/attendance (push)
```

Tenhle výstup znamená, že pod zkratkou “origin”
se schovává adresa, ze které jsi repozitář
naklonoval{{a}}.

Přidej si podobnou zkratku pro vlastní repozitář na GitHubu.
Nezapomeň nahradit <i>tvojejmeno</i> za jméno účtu,
který máš na GitHubu ty. (Pozor, v příkazu je <i>tvojejmeno</i> dvakrát!)

<div class="highlight codehilite">
<pre><code><span class="gp">$</span> git remote add <i>tvojejmeno</i> https://github.com/<i>tvojejmeno</i>/attendance
</code></pre></div>

a zkontroluj si, že se to povedlo:

<div class="highlight codehilite">
<pre><code><span class="gp">$</span> git remote -v
<span class="go">origin  git@github.com:{{coach_username}}/attendance.git (fetch)</span>
<span class="go">origin  git@github.com:{{coach_username}}/attendance.git (push)</span>
<span class="go"><i>tvojejmeno</i>      https://github.com/<i>tvojejmeno</i>/attendance (fetch)</span>
<span class="go"><i>tvojejmeno</i>      https://github.com/<i>tvojejmeno</i>/attendance (push)</span>
</code></pre></div>

Tolik k nastavení – `git remote add`
stačí udělat jednou pro každý repozitář.
Pak už můžeš změny nahrávat pomocí:


<div class="highlight codehilite">
<pre><code><span class="gp">$</span> git push <i>tvojejmeno</i> master
</code></pre></div>

což znamená: pošli na adresu uloženou pod zkratkou
<code><i>tvojejmeno</i></code>
větev `master`.

Funguje? Podívej se na
<code>https://github.com/<i>tvojejmeno</i>/attendance</code>
v prohlížeči a ujisti se, že tam tvoje změny jsou.


## Žádost o začlenění <small>(<em>pull request</em>)</small>

Teď zbývá požádat autory původního projektu,
aby změny z tvého sdíleného repozitáře přidali do svojí kopie.
GitHub na to má mechanismus zvaný *pull request* (žádost o začlenění).

Jdi na stránku původního projektu (na adresu,
kterou jsi použil{{a}} na začátku pro
`git clone`).
Měl{{a}} bys tam vidět oznámení o své nově nahrané větvi
s velkým zeleným tlačítkem *Compare & pull request*.
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


## Aktualizace <small>(<code>git pull</code>)</small>

Když budou tvé změny – a změny od ostatních –
začleněné, můžeš si aktualizovat lokální repozitář. (To je ten,
který máš u sebe na počítači.)

To se dělá příkazem
`git pull origin master` (stáhni změny
z větve “master” z adresy pod zkratkou “origin”).
Pomocí `gitk --all` nebo `git log`
se můžeš podívat, jak se projekt mezitím vyvinul.

Gratuluji! Právě jsi {{gnd('prošel', 'prošla')}} “kolečkem”,
které většina programátorů dělá denně: udělání nějaké změny,
odeslání kolegům na kontrolu a začlenění a stažení změn od ostatních.


## Hlášení chyb <small>(<em>issues</em>)</small>

Občas nastane situace, kdy v nějakém projektu
na GitHubu najdeš chybu, ale nemáš čas nebo
znalosti, abys ji opravil{{a}}. V takovém případě
často na GitHubu na stránce projektu pod záložkou *Issues*
najdeš seznam nahlášených problémů.
Nenajdeš-li mezi nimi “svoji” chybu, můžeš ji
nahlásit – stačí kliknout na *New Issue*
a můžeš psát, kdy chyba nastává, co program dělá
špatně a co by měl dělat místo toho.

> [note]
> Některé projekty nepoužívají Issues na GitHubu.
> Kdybys záložku Issues {{gnd('nenašel', 'nenašla')}}, podívej se
> do dokumentace projektu, jestli tam není odkaz na
> seznam chyb.


## Licence a jazyk

Aby sdílení fungovalo i pro právní stránce,
nestačí když nahraješ kus kódu na Internet.
Musíš taky oficiálně oznámit, že si s ním ostatní můžou hrát.
Bez *licence* totiž nemá nikdo právo tvůj
program ani používat, natož vylepšovat.

Problematika licencí může být, bohužel, docela složitá.
Když to ale zjednodušíme na minimum, budeš
chtít jen zajistit, aby každý mohl tvůj výtvor
používat, učit se z něj, předávat ho dál
a vylepšovat ho. V tom případě vyber třeba
licenci [MIT](https://choosealicense.com/licenses/mit/).

> [note]
> Pokud chceš navíc zabránit tomu, že si tvůj kód
> někdo vezme a začne ho "vylepšovat" a vydělávat na
> něm, aniž by se o vylepšení podělil s ostatními,
> zkus licenci [AGPL](https://choosealicense.com/licenses/agpl-3.0/).

> [note]
> A tyto materiály jsou pod ještě jinou licencí –
> [CC BY-SA](https://choosealicense.com/licenses/cc-by-sa-4.0/) –
> protože výše jmenované licence jsou dělané na programy, ne na text.

Kód se nejčastěji licencuje tak, že text licence
dáš do souboru jménem `LICENSE` a přidáš do Gitu.

Chceš-li si o licencích přečíst něco víc, odkážu tě na
[choosealicense.com](http://choosealicense.com/),
případně [creativecommons.org](http://creativecommons.org/choose/)
a [opensource.org](https://opensource.org/licenses).

A nakonec – aby se do projektu mohl zapojit
kdokoli z celého světa, bývají open-source projekty v angličtině.
Jména proměnných, komentáře, dokumentace – všechno
je primárně v anglické verzi.
Tenhle kurz je česky, aby byly začátky jednodušší,
ale jestli se ti programování zalíbilo a chceš
v něm po kurzu pokračovat dál, bez angličtiny
to bude velice složité.