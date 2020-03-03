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
```ef

Virtualbox ve verzi 6.1.3 stále není kompatibilní s kernelem 5.3

## Stažení obrazu 

Existuje velké množství tzv. distribucí, tj. variant linuxů. Ty se liší typicky v dostupném software, grafickém prostředí, způsobu instalace softwarových balíčků a spoustě dalších detailů. Pro jednotnost si budeme všechno ukazovat na distribuci Fedora, kterou získáš na:
https://getfedora.org/cs/workstation/download/

Pro virtuální počítač budeme potřeboat tzv. obraz disku - ISO soubor.

# Instalace Fedory

Při prvním spuštění je (virtuální) pevný disk zatím prázdný a ve virtuálním počítači vsunuta do virtuální DVD mechaniky ISO obraz, který obsahuje soubory potřebné k samotné instalaci.

V černém okně vyber šipkami na klávesnici (myš v tuto chvíli nelze použít) **Start Fedora-Workstation-Live 31** a potvrď klávesou Enter.

Po chvilce se zobrazí už grafické okno, kde myší klepni na **Install to Hard Drive**. Tím se spustí samotná instalace. Druhá volba Try Fedora ti 