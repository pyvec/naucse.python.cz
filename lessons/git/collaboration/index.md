{% set coach_username = var('coach-username') or 'encukou' %}

# Spolupráce

„Opravdové” programy zřídka vznikají prací jednoho člověka.
Víc hlav víc ví, a tak je dobré si na projekt vytvořit tým.

Každý člen týmu potřebuje mít přístup k práci ostatních.
K tomu se dá použít Git: někde na internetu si zařídíme *sdílený repozitář*,
se kterým se všichni budou synchronizovat.


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

## Spojení tvého repozitáře s remote repozitářem
Na úvodní stránce Githubu po založení účtu uvidíš na úvodní stránce `Learn Git and GitHub without any code!` a pod ním najdeš tlačítko `Start a project`. Zvol si jméno pro svůj nový repozitář, třeba `pyladies` a zbytek nastavení nech tak, jak je a klikni na `Create repository`.

Uvidíš stránku s velkým množství různých příkazů. Nás zajímá druhá sekce `…or push an existing repository from the command line`.

Zkopíruj si příkaz začínající na `git remote add origin ...` a vlož ho do příkazové řádky tak, kde máš svůj gitový repozitář, který jsme si společně nastavily. Po stisknutí `enter` ti příkazová řádka nic nevypíše, což je signál, že všechno proběhlo v pořádku.

Stejným způsobem si zkopíruj a vlož k sobě do terminálu příkaz `git push -u origin master`. Github se tě zeptá na tvé přihlašovací údaje. Vlož je (pozor, když budeš psát heslo, tak to bude vypadat, že vůbec nepíšeš, to je však jen z důvodu bezpečnosti) a pak už by si měla vidět `Branch 'master' set up to track remote branch 'master' from 'origin'.`

To znamená, že tvoj lokální repozitář se právě nahrál na tzv. remote repozitář. Repozitář jsme označili jménem *origin*. Když se proklikneš do svého nového repozitáře na Githubu (`https://github.com/tvoje_jmeno/nazev_repozitare`), uvidíš tu přesnou kopii tvé složky s lekcemi.


## Posílání změn <small>(<code>git push</code>)</small>

Co když uděláš nějaké změny, například vypracuješ domácí úkol na svém druhém počítači a chtěla by, aby změny byly vidět v tvém repozitáři na Githubu? K tomu slouží příkat `git push`.

Pamatuješ ještě na básničku, kterou jsme psali, když jsme se učili s Gitem? Napiš si jí ještě jednou, ať já neztratíme. Přepni se do složky aktuální lekce, vytvoř soubor `basnicka.txt` a napiš do něj nějakou básničku. Přidej jí do Gitu (pomocí příkazů `git add` a `git commit`).

Pomocí příkazu `git push origin master` nahraješ nové změny na Github.


## Stažení změn <small>(<code>git pull</code>)</small>

Máš zase svůj oblíbený počítač, kde máš všechny materiály, ale chybí ti tam úkol, který si vypracovala na svém druhém počítači a nahrála na Github?

Přepni se do složky s materiály, kde máš svůj Gitový repozitář a napiš `git pull origin master`.
Všechny změny by se ti měly stáhnout do tvého lokálního repozitáře.


## Žádost o začlenění <small>(<em>pull request</em>)</small>

Pull requesty se používají, když chceš začlenit nějaké změny do projektu, na kterém pracuješ. Ve větvi `master` by měl být funkční a hotový kód, na růzké pokusy slouží větve `branch`, o kterých jsme mluvili v minulé sekci.

My budeme využívat pull requesty k efektivní kontrole domácích projektů. Vytvoř si teď pro demonstraci novou větev, ve které upravíme naší básničku `git branch uprava_basnicky` a přepni se do ní `git checkout uprava_basnicky`. Teď udělej nějaké změny v básničce, přidej autora, další sloku, cokoliv tě napadne.

Přijde úpravy do Git jako novou revizi pomocí příkazů `git add` a `git commit`. Pak pomocí příkazu `git push origin uprava_basnicky` nahraj změny na Github. Vidíš, že v tomhle případě *napíšeme* `git push origin master`, protože teď nechcem zveřenovat změny ve větvi master, ale ve větvi, kde jsme upravili naší básničku.

Jdi do svého repozitáře na Github a klikni na sekci `Pull requests`. Uvidíš velké zelené tlačítko `New pull request`. Po kliknutí uvidíš stránku nadepsanou `Compare changes`. Tady musíš nastavit, co kam chceš vlastně začlenit. Jako `base` nech větev master a do `compare` zvol větev `uprava_basnicky`.

Github ti ukáže všechny změny, které si na té větvi udělala, pak už stačí jen kliknout na `Create new pull request`. V sekci `Pull requests` najednou uvidíš v závorce (1). To znamená, že si vytvořila pull request.

Pošli odkaz na pull request svému kouči, který ti domácí úkol opraví. Díky Githubu ti může napsat komentáře přímo do kódu a nebude tak muset vypisovat čísla řádků a do je na nich špatně. Až ti kouč úkol schválí, můžeš změny sloučit do master větve pomocí tlačítka `Merge pull request`. Pak se ti správný a schválený úkol nahraje do tvé master větve. Aby si ho měla v master větvi i ve svém počítači, použij náš známý příkaz `git pull origin master`.


## Naklonování repozitáře <small>(<code>git clone</code>)</small>

Pokud budeš chtít mít přístup ke svým materiálům z lekcí z dalšího počítače, je nutné si tam repozitář tzv. naklonovat.
Na úvodní stránce tvého repozitáře uvidíš velké zelené tlačítko `Clone or download`. Klikni na něj a zvol možnost `Clone with HTTPS`. Ještě tu je druhá možnost (`Clone with SSH`), kterou nebudeme využívat. V příkazové řádce uvidíš `Cloning into 'nazev_repozitare'...`. Vytvořila se ti nová složka, kde je přesná kopie tvého repozitáře z githubu. Přepni se do ní, zkus příkaz `git status`. Funguje?


## Hlášení chyb <small>(<em>issues</em>)</small>

Občas nastane situace, kdy v nějakém projektu najdeš chybu, ale nemáš čas nebo
znalosti, abys ji opravil{{a}}. Pro tyto případy slouží na GitHubu záložka
 *Issues*, kde se nachází seznam nahlášených problémů.
Nenajdeš-li mezi nimi „svoji” chybu, můžeš ji
nahlásit – stačí kliknout na *New Issue*
a můžeš psát, kdy chyba nastává, co program dělá
špatně a co by měl dělat místo toho.

> [note]
> Některé projekty nepoužívají Issues na GitHubu.
> Kdybys záložku Issues {{gnd('nenašel', 'nenašla')}}, podívej se
> do dokumentace projektu, jestli tam není odkaz na
> seznam chyb.
