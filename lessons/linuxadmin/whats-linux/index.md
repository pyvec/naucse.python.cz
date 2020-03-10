# Co je to ten „Linux“?

Máme tu kurz Linuxové administrace, ale co je vlastně Linux?

Striktně řečeno, *Linux* je název *jádra* (angl. *kernel*) operačního systému,
tedy softwaru, který se stará o najzákladnější funkčnost počítače:
o komunikaci s hardwarem (klávesnicí, obrazovkou, diskem, síťovou kartou atd.),
a o to, aby na počítači mohly běžet ostatní programy.

Celý systém se pak skládá ze spousty dalších komponent, které se starají např.
o spouštění programů, vykreslování grafických okýnek, připojování k internetu,
ediaci souborů nebo přehrávání hudby.

Na to všechno existuje software s *otevřeným zdrojovým kódem* (Open Source),
což znamená, že si kdokoli může stáhnout kód daného programu a upravit si ho
podle sebe (nebo někomu zaplatit, aby ho upravil).
Případné opravy pak může poslat zpět původním autorům, aby mohly
sloužit ostatním.
A nebo – třeba pokud původní autor se změnou nesouhlasí – může svoji novou
verzi dát k dispozici zvlášť, typicky pod jiným názvem.

Pro všechno, co budeme v tomto kurzu probírat, proto nutně existuje několik
variant (kde ne, tam může kdokoli vytvořit svoji):

* Jádro systému – Linux, FreeBSD, OpenBSD, …
* Shell – Bash, zsh, csh, Fish, Xonsh, sh, …
* Základní nástroje – GNU coreutils, BusyBox, …
* Balíčkovací systém – DNF, APT, pacman, …
* Správce služeb – systemd, upstart. openrc, init, …
* Grafické prostředí – GNOME, KDE Plasma, XFCE, Mate, Sugar, …
* Textový editor – Gedit, Kate, vim, Emacs, Atom, nano, …
* Webový prohlížeč – Firefox, Chromium, qutebrowser, links, …
* Správce souborů – Nautilus, Dolphin, Konqueror, Thunar, …
* Kancelářské programy – LibreOffice, OpenOffice, Calligra Suite, …
* … a tak dále

Teoreticky si můžeš vybrat jednotlivé části podle sebe, nainstalovat si je
a propojit.
Existují ale i tzv *distribuce* (angl. *distros*), jejichž autoři to dělají za
tebe.
Obsahují předpřipravený výběr programů, které spolu fungují.
Různé distribuce se liší nejen výběrem programů, ale i třeba filosofií, s jakou
je vybírají a nastavují, a tím, kde nachází rovnováhu mezi jednoduchostí
a možností si všechno nastavit po svém.

A tak si můžeš vybrat jen z jedné kategorie:

* Distribuce – Fedora, Ubuntu, OpenSUSE, Debian, Arch, Gentoo, Alpine, …

Abychom tento kurz zvládli řídit a neutopili se ve spoustě možností,
jak můžou různé komponenty selhat, vybíráme ze všech těch variant jednu – tu,
se kterou mají autoři tohoto kurzu největší zkušenosti.
Konkrétní technologie, které v těchto materiálech použijeme,
jsou v seznamech výše uvedeny na prvním místě.
Všechno, co se naučíme, se ale – s větší či menší dávkou studia dokumentace –
dá použít i s alternativními technologiemi.

První věc, na kterou se podíváme, je základní ovládání grafického prostředí,
což je (v základní variantě Fedory) *GNOME*.
