# Virtuální počítač

V tomto kurzu se budeme učit pracovat s operačním systémem Linux.
To je možné i v případě, že aktuálně používáš jiný operační systém - díky tzv. virtuálnímu počítači. To je program, který se tváří jako opravdový počítač a dá se do něj nainstalovat jiný operační systém.

To je velmi výhodné pro různé testování a objevování. Když si virtuální počítač rozbiješ, smažeš ho stejně snadno, jako soubor a máš uklizeno.
Nebo si můžeš uložit stav a později se k němu vrátit.

Protože v kurzu budeme testovat, objevovat a občas i rozbíjet často,
vytvoř si virtuální i pokud používáš Linux.

Hned na začátku tě čeká malá terminologická nepříjemnost:
**Hostitel** (anglicky **host**) je termín označující operační systém/počítač, v rámci kterého budeš provozovat ten virtuální – tedy to, co máš na poc'itači nainstalováno už teď.
Virtuálnímu systému se česky říká **host** (anglicky **guest**).
Slovo **host** má tedy v češtině úplně opačný význam než v angličtině.


## Stažení obrazu 

Na opravdový počíttač se dá Linux nainstalovat z DVD nebo USB disku („flashky“).
Pro virtuální počítač budeš potřebovat virtuální DVD – soubor, který
obsahuje stejná data jako disk.
Říká se mu *obraz disku* nebo *ISO soubor*.

Existuje velké množství tzv. distribucí, tj. variant linuxů. Ty se liší typicky
v dostupném software, grafickém prostředí, způsobu instalace softwarových
balíčků a spoustě dalších detailů.
Pro jednotnost si budeme v šechno ukazovat na distribuci Fedora, kterou
si stáhni z [getfedora.org](https://getfedora.org/cs/workstation/download/) –
stáhnout soubor ISO.

Je to velký soubor (zhruba 2 GB) se jménem jako `Fedora-Workstation-Live-x86_64-31-1.9.iso`.


# Příprava hosta

Existuje několik programů, které umí simulovat virtuální počítač.
Vyber si jeden podle svého hostitelského systému a ho:

* Pokud máš Windows nebo macOS, použij Virtualbox: [instalace Virtualboxu]({{ subpage_url('virtualbox') }}).
* Pokud máš Linux s GNOME, bude lépe fungovat Gnome Boxes: [instalace Gnome Boxes]({{ subpage_url('gnome-boxes') }}).

Nevíš-li, poraď se s někým zkušenějším – nebo zkus jeden z nich.


{{ anchor('install-system') }}
# Instalace systému

Při prvním spuštění je (virtuální) pevný disk zatím prázdný a ve virtuálním
počítači vsunuta do virtuální DVD mechaniky ISO obraz, který obsahuje
soubory potřebné k samotné instalaci. 

{{ figure(
    img=static('fedora-install-01.png'),
    alt='Instalace #1',
) }}

V černém okně vyber šipkami na klávesnici (myš zatím nelze použít)
**Start Fedora-Workstation-Live 31** a potvrď klávesou Enter. 

{{ figure(
    img=static('fedora-install-02.png'),
    alt='Instalace #2',
) }}

Po chvilce se zobrazí už grafické okno, kde myší klepni na **Install to Hard
Drive**. Tím se spustí samotná instalace. (Druhá volba *Try Fedora* ti spustí
operační systém rovnou z DVD k vyzkoušení - tu ale nyní nevyužijeme).

## Instalační obrazovky

* **Výběr jazyka** - V levém panelu vyber *Čeština*, poté klepni na *Pokračovat*.
  (Můžeš vybrat i jiný jazyk, ale tyto materiály budou v češtině.)

  {{ figure(
    img=static('fedora-install-03.png'),
    alt='Instalace #3',
  ) }}


* **Přehled instalace** - Instalátor potřebuje potvrdit kde se bude instalace
  provádět. Klepni na *Cíl instalace*, která ti nabídne dostupné pevné disky.

  {{ figure(
    img=static('fedora-install-04.png'),
    alt='Instalace #4',
  ) }}


* **Cíl instalace** - U virtuálního počítače je situace jednoduchá, není tu
  potřeba nic měnit.
  vlevo nahoře najdeš tlačítko *Hotovo*, kterým obrazovku potvrdíš.

  {{ figure(
    img=static('fedora-install-05.png'),
    alt='Instalace #5',
 ) }}


* **Přehled instalace** - Nyní už instalátor ví vše potřebné. Vpravo dole
 klepni na tlačítko *Spustit instalaci*. Od tohoto okamžiku se začne
 zapisovat na vybraný pevný disk.
 
  {{ figure(
    img=static('fedora-install-06.png'),
    alt='Instalace #6',
  ) }}


* **Průběh instalace** - tento krok bude trvat nejdéle. V závislosti na
 rychlosti Tvého počítače to může být od minut po malé desítky minut.
 Nakonec se vpravo dole objeví tlačítko *Dokončit instalaci*. Tím dojde k 
 uzavření instalačního programu a je třeba provést restart.
 
  {{ figure(
    img=static('fedora-install-07.png'),
    alt='Instalace #7',
  ) }}

  
* **Restart** - K tomu je potřeba kliknout na symbol ⏻ úplně vpravo nahoře,
 poté na další ⏻ a nakonec na tlačítko *Restart*.

  {{ figure(
    img=static('fedora-install-09.png'),
    alt='Instalace #9',
  ) }}

   {{ figure(
    img=static('fedora-install-10.png'),
    alt='Instalace #10',
  ) }}


#### Dokončení instalace

V této části už je operační systém nainstalovaný,
 zbývá akorát provést posledních několik nastavení. To se děje formou průvodce
 kde je tlačítko *Další* vždy vpravo nahoře.

* **Soukromí**
  * Geolokační služby - můžeš klidně vypnout
  * Automatické hlášení problémů - radši taky vypni; ať nikdo neví jakou
    neplechu na virtuálním počítači napácháš

  {{ figure(
    img=static('fedora-install-11.png'),
    alt='Instalace #11',
  ) }}

  
* **Účty online** - tento krok můžeš klidně přeskočit (a třeba provést později)

  {{ figure(
    img=static('fedora-install-12.png'),
    alt='Instalace #12',
  ) }}

  
* **O vás** - Nejdůležitější krok. Tady doplň *Celé jméno* (diakritika
 nevadí) a především *Uživatelské jméno* (pouze znaky `a-z`, `_`, `-`, číslice
 ). To je nejdůležitější. Tím se budeš přihlašovat do systému. Oba údaje lze
 změnit i později, avšak byť je změna *Uživatelského jména* v budoucnu
 technicky vzato možná, jde o problematický úkon. Proto je velmi důležité si
 ho dobře rozmyslet hned na začátku. (*Celé jméno* slouží jen jako popiska
  k uživatelskému jménu.) Pokračuj tlačítkem *Další*.

  {{ figure(
    img=static('fedora-install-13.png'),
    alt='Instalace #13',
  ) }}


 * **Nastavení hesla** - je heslo k uživatelskému jménu vyplněném v předchozím
 kroku. Heslo je potřeba zadat do obou polí stejné.
 
 Navzdory obecným radám o heslech tady doporučuji zadat jednoduché heslo,
 třeba `123` nebo slovo `heslo`.
 Jde o *virtuální* počítač, který není potřeba nějak zvlášť chránit.

 Určitě ale nepoužívej heslo, které používáš i jinde!

  {{ figure(
    img=static('fedora-install-14.png'),
    alt='Instalace #14',
  ) }}

  Heslo si dobře zapamatuj (nebo, navzdory radám k bezpečným heslům, zapiš).

 * **Připraveno k používání** - Výborně, všechno je již nastaveno a můžeš se
  pustit do objevování. Klepni na *Začít používat systém Fedora*.

  {{ figure(
    img=static('fedora-install-15.png'),
    alt='Instalace #15',
  ) }}

Virtuální počítač můžeš vypnout přes menu v pravém horním rohu obrazovky.
