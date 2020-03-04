# Virtuální počítač

V tomto kurzu se budeme učit pracovat s operačním systémem Linux.
To je možné i v případě, že aktuálně používáš jiný operační systém - díky tzv. virtuálním počítači. To je program, který se tváří jako opravdový počítač a dá se do něj nainstalovat jiný operační systém.

To je velmi výhodné pro různé testování a objevování. Když si takový počítač rozbiješ, smažeš jo stejně snadno, jako soubor a máš uklizeno.

V tomto kurzu budeme používat **Virtualbox** (existuje ale i několik dalších).

**Hostitel** (anglicky **host**) je termín označující operační systém/počítač, v rámci kterého budeš provozovat ten virtuální. Tomu virtuálnímu se česky říká **host** (anglicky **guest**).

# Příprava hosta

Virtualbox si nejdříve stáhni z webových stránek https://www.virtualbox.org/wiki/Downloads a postupuj podle pokynů k tvému aktuálně běžícímu operačnímu systému (hostiteli).

Na jednom hostiteli tak může běžet několik hostů.

## Fedora

Viz https://www.if-not-true-then-false.com/2010/install-virtualbox-with-yum-on-fedora-centos-red-hat-rhel/

Pokud používáš i rpmfusion, je třeba použít verzi přímo od Oracle.

```
dnf install --disablerepo rpmfusion-free VirtualBox-6.1
```

Virtualbox ve verzi 6.1.3 stále není kompatibilní s kernelem 5.3

## Stažení obrazu 

Existuje velké množství tzv. distribucí, tj. variant linuxů. Ty se liší typicky
v dostupném software, grafickém prostředí, způsobu instalace softwarových
balíčků a spoustě dalších detailů. Pro jednotnost si budeme v šechno ukazovat
na distribuci Fedora, kterou získáš na:
https://getfedora.org/cs/workstation/download/

Pro virtuální počítač budeme potřeboat tzv. obraz disku - ISO soubor.

# Instalace Fedory

Při prvním spuštění je (virtuální) pevný disk zatím prázdný a ve virtuálním
počítači vsunuta do virtuální DVD mechaniky ISO obraz, který obsahuje
soubory potřebné k samotné instalaci. 

![][f-01]

V černém okně vyber šipkami na klávesnici (myš v tuto chvíli nelze použít)
**Start Fedora-Workstation-Live 31** a potvrď klávesou Enter. 

![][f-02]

Po chvilce se zobrazí už grafické okno, kde myší klepni na **Install to Hard
Drive**. Tím se spustí samotná instalace. (Druhá volba *Try Fedora ti spustí
operační systém rovnou z DVD k vyzkoušení - tu ale nyní nevyužijeme).

## Instalační obrazovky

* **Výběr jazyka** - v levém panelu vyber *Čeština*, poté klepni na *Pokračovat*

 ![][f-03]

* **Přehled instalace** - instalátor potřebuje potvrdit kde se bude instalace
 provádět. Klepni na *Cíl instalace*, která ti nabídne dostupné pevné disky.

 ![][f-04]

* **Cíl instalace** - tady není potřeba nic měnit, vlevo nahoře najdeš tlačítko
*Hotovo*, kterým obrazovku potvrdíš.

 ![][f-05]

* **Přehled instalace** - nyní už instalátor ví vše potřebné. Vpravo dole
 klepni na tlačítko *Spustit instalaci*. Od tohoto okamžiku se začne reálně
 zapisovat na vybraný pevný disk.
 
 ![][f-06]

* **Průběh instalace** - tento krok bude trvat nejdéle. V závislosti na
 rychlosti Tvého počítače to může být od minut po malé desítky minut.
 Nakonec se vpravo dole objeví tlačítko *Dokončit instalaci*. Tím dojde k 
 uzavření instalačního programu a je třeba provést restart.
 
 ![][f-07]
  
* **Restart** - K tomu je potřeba kliknout na symbol ⏻ úplně vpravo nahoře,
 poté na další ⏻ a nakonec na tlačítko *Restart*.

 ![][f-09]

#### Dokončení instalace

V této části už je operační systém nainstalovaný,
 zbývá akorát provést posledních několik nastavení. To se děje formou průvodce
 kde je tlačítko *Další* vždy vpravo nahoře.

* **Soukromí**
  * Geolokační služby - můžeš klidně vypnout
  * Automatické hlášení problémů - můžeš nechat zapnuté

 ![][f-11]
  
* **Účty online** - tento krok můžeš klidně přeskočit (a provést později)
  
 ![][f-12]
  
* **O vás** - je nejdůležitějším krokem. Tady doplň *Celé jméno* (diakritika
 nevadí) a především *Uživatelské jméno* (pouze znaky `a-z`, `_`, `-`, číslice
 ). To je nejdůležitější. Tím se budeš přihlašovat do systému. Oba údaje lze
 změnit i později, avšak byť je změna *Uživatelského jména* v budoucnu
 technicky vzato možná, jde o problematický úkon. Proto je velmi důležité si
 ho dobře rozmyslet hned na začátku. (*Celé jméno* slouží jen jako popiska
  k uživatelskému jménu.) Pokračuj tlačítkem *Další*.

 ![][f-13]

 * **Nastavení hesla** - je heslo k uživatelskému jménu vyplněném v předchozím
 kroku. Heslo je potřeba zadat do obou polí stejné.

 ![][f-14]
  
 * **Připraveno k používání** - Výborně, všechno je již nastaveno a můžeš se
  pustit do objevování. Klepnutím na *Začít používat systém Fedora*


[f-01]: img/fedora-install-01.png
[f-02]: img/fedora-install-02.png
[f-03]: img/fedora-install-03.png
[f-04]: img/fedora-install-04.png
[f-05]: img/fedora-install-05.png
[f-06]: img/fedora-install-06.png
[f-07]: img/fedora-install-07.png
[f-08]: img/fedora-install-08.png
[f-09]: img/fedora-install-09.png
[f-10]: img/fedora-install-10.png
[f-11]: img/fedora-install-11.png
[f-12]: img/fedora-install-12.png
[f-13]: img/fedora-install-13.png
[f-14]: img/fedora-install-14.png
