# Soubory a cesty

Informace uložené v Pythonních proměnných – seznamech, slovnících, a tak dále – jsou dočasné.
Jakmile Python ukončíš, zmizí.
Chceš-li něco uložit na delší dobu, nebo třeba sdílet s jinými programy,
můžeš si informace uložit do souboru.

S počítačovými soubory (angl. *files*) už ses asi setkal{{a}}.
Teď se na ně ale podívejme trochu podrobněji.

Soubor je místo, kam se dají ukládat informace – *obsah*. Kromě obsahu mají soubory ještě další vlastnosti:

* *jméno*, podle kterého se soubor dá najít,
* informace o *vlastnictví* a *oprávnění*, které určují kdo může ze souboru
  číst a kdo do něj může zapisovat,
* informace o *časech* vytvoření, posledního zápisu, a podobně,
* a další informace, na každém druhu operačního systému jiné.

Tak jako je kapitola v knížce poskládaná z písmenek, obsah souboru je
poskládaný z *bajtů* (angl. *bytes*) – malých čísel.
Každá informace, kterou počítač umí zpracovat, se dá zakódovat do bajtů
podobně jako se z písmenek skládá text.

Soubory jsou většinou uloženy na disku (nebo podobném médiu), kde bývá místo
na bilióny bajtů.
Aby počítač poznal, kde na disku je který soubor, používá *souborový systém*
(angl. *filesystem*).
Ten plní podobnou funkci jako v knížce obsah, jména kapitol a čísla stránek.


## Operační systémy

Souborových systémů existuje spousta druhů.
Experti nám snad prominou hrubé zjednodušení, když si je rozdělíme na dva
druhy: ty pro Windows a ty pro Unix.

Unix je operační systém, vytvořený v sedmdesátých letech, ze kterého vycházejí
dnešní systémy Linux, macOS a další.
Základní principy, o kterých bude řeč tady, se od dob Unixu většinou
příliš nezměnily.
A tak když v těchto materiákech uvidíš jméno „Unix“, jde o něco společné pro
Linux i macOS.
Hlavní rozdíly mezi Linuxem a macOS jsou v konvencích – např. na Linuxu se
místo pro domovské adresáře jmenuje většinou `/home`, kdežto na macOS `/Users`.

Další rozšířený operační systém, Windows, z Unixu nevychází.
Některé věci se v něm, jak později uvidíme, chovají jinak.


## Adresáře

Na dnešních souborových systémech jsou soubory tříděny do *adresářů* neboli
*složek* (angl. *directory*, *folder*).
Adresář může obsahovat spoustu souborů nebo i jiných adresářů.

A teď něco, co pro tebe může být nové: pro programátory jsou adresáře taky soubory.
Souborů je dokonce spousta druhů: *normální soubory* s informacemi, adresáře
(které obsahují další soubory), speciální soubory které můžou reprezentovat
celý disk nebo spojení mezi počítači, odkazy na jiné soubory, a tak dále.
Co je a co není soubor závisí na systému.
Dnes se proto omezíme jen na dva druhy souborů, které najdeme jak na Windows
tak na Unixu: normální datové soubory (ty, které si pod jménem „soubor“
představí běžný uživatel) a adresáře.


## Cesty

Abys mohl/a najít nějaký soubor, potřebuješ znát jeho jméno a adresář,
který ten soubor obsahuje.
Abys pak mohl/a najít ten adresář, musíš opět znát jméno adresáře a adresář,
který ho obsahuje.
A tak dál, až se dostaneš ke *kořenovému adresáři* (angl. *root directory*),
který (zjednodušeně řečeno) obsahuje celý souborový systém.
Když napíšeš jména všech adresářů které takhle projdeš za sebe, dostaneš
*cestu* (angl. *path*) k danému souboru.
Taková cesta by mohla na Unixu být třeba:

* Linux: `/home/janca/Documents/archiv.tar.gz`
* macOS: `/Users/janca/Documents/archiv.tar.gz`

To znamená, že začneš v kořenovém adresáři (který se na Linuxu jmenuje `/`),
v něm hledáš adresář `home` nebo `Users` (ten tradičně obsahuje domovské
adresáře uživatelů), v něm pak `janca` (podle uživatelského jména),
v něm `Documents`, a v něm pak `archiv.tar.gz`.
To už není adresář, ale normální soubor do kterého se dají zapsat informace.

Obdobná cesta na Windows by mohla být třeba:
`C:\Users\Jana\Documents\archiv.tar.gz`

Tahle cesta začíná na disku `C:`.
Windows mají na rozdíl od Unixu zvláštní souborový systém pro každý disk,
a tak mají víc kořenových adresářů – třeba `C:\` a `D:\`.
Dál je to podobné jako na Unixu, jen oddělovač adresářů je zpětné lomítko
místo obyčejného.

## Absolutní a relativní cesty

Cesta, která začíná v konkrétním kořenovém adresáři, se nazývá *absolutní*
cesta (angl. *absolute* path). Je jako úplná poštovní adresa:
správně nadepsaný dopis můžu hodit do schránky kdekoli na světě a (teoreticky)
vždy dojde k adresátovi.

Když ale dopis do Česka házím do české schránky, můžu vynechat informaci
o kontinentu a zemi.
Je to tak kratší a jednodušší‚ ale z Austrálie by to nefungovalo.

Na podobném principu jsou založeny *relativní cesty* (angl. *relative paths*).
Když už jsi v domovském adresáři, stačí zadat cestu `Documents/archiv.tar.gz`,
bez lomítek či jména disku na začátku.
To znamená, že cesta nezačíná v kořenovém adresáři, ale v *aktuálním adresáři*
(angl. *current directory*) – tam, kde právě jsi.
Kdyby ses pomocí `cd` přepnul{{a}} jinam, tahle relativní cesta by přestala
fungovat.

Kde relativní cesta „začíná“, to záleží na kontextu – většinou jde o aktuální 
adresář, ale může to být třeba gitový repozitář
(hlavní adresář nějakého projektu), adresář s programem který právě běží,
a podobně.

## Dvě tečky a jedna tečka

Každý adresář obsahuje dva speciální záznamy: `..` a `.`.

Jméno `.` (tečka) vždy označuje samotný adresář.
Tudíž `/home/janca` je stejný adresář jako `/home/janca/.`,
`/home/janca/././././.` a tak dál.
To nezní moc užitečně – ale jen do té doby, než potřebuješ zadat jako
relativní cestu samotný aktuální adresář.

Jméno `..` (dvě tečky) označuje *nadřazený adresář*.
Když se tohle jméno objeví v cestě, znamená to, že potřebujeme přejít
o úroveň výš.
Jsi-li v adresáři `/home/janca/Pictures/dovolena`, tak:

* cesta `..` znamená adresář `/home/janca/Pictures`
* cesta `../../programy/venv` znamená `/home/janca/programy/venv`
* absolutní cesta `/home/janca/Documents/../Pictures/dovolena`
  znamená `/home/janca/Pictures/dovolena`

> [note]
> Striktně řečeno, výše uvedené neplatí vždycky:
> speciální soubory zvané *symbolické odkazy* (angl. *symlinks*) můžou počítač
> při procházení cesty přesměrovat tak, že `Documents/../Pictures` bude jiný
> soubor než `Pictures`.
> Detaily jsou nad rámec těchto materiálů, nicméně je to důvod, proč Python
> nebude automaticky nahrazovat `Documents/../Pictures` za `Pictures`.


## Jména souborů

Jméno souboru je řetězec. Nemůže to ale být jakýkoli řetězec.
Různé systémy mají různou maximální délku jména (i když na tenhle limit dnes 
většinou nenarazíš).
A navíc je omezen i obsah – jméno souboru nesmí obsahovat:

* na Unixu oddělovač adresářů `/` ani speciální nulový znak,
* na windows oddělovač `\`, znaky `<>:"/|?*` ani speciální znaky (např.
  tabulátor, znak nového řádku).

Nedoporučuji s názvy příliš experimentovat, protože některé validní znaky
můžou v určitých kontextech mít zvláštní význam (např. `*` a `?` jako zástupné
znaky), špatně se používají (např. mezery a nové řádky), působí problémy
s kódováním (např. písmena s diakritikou nebo emoji), nebo naráží na problémy
s tím, že Windows nerozlišují velikost písmen ale Unix ano.

Programátoři by se tak měli omezit na:

* malá písmena bez diakritiky,
* číslice `0` - `9`,
* pomlčku `-`,
* podtržítko `_`, a
* tečku jako oddělovač přípony.

Možná sis všiml{{a}}, že normální lomítko, `/`, nesmí na Windows být ve jménu
souboru.
Spousta moderních programů (včetně většiny knihoven v Pythonu) toho využívá a
dopředná lomítka automaticky zaměňuje za zpětná.
Můžeš tak na všech systémech používat stejné relativní cesty: `Documents/archiv.tar.gz` většinou funguje i na Windows.


## Přípony

Hodně jmen souborů obsahuje tečku a za ní krátkou *příponu* (angl. *extension*),
která tradičně indikuje formát souboru – způsob,
kterým jsou v souboru zakódovány informace.
Například soubor `hrad.jpeg` má příponu `.jpeg`.
Ten kdo ví, že [JPEG](https://cs.wikipedia.org/wiki/JPEG) je způsob zakódování
obrázku (zvlášť vhodný pro fotografie), si tak může domyslet že v souboru je
nejspíš fotka hradu.

Pythonisti zase poznají příponu `.py`.
Python samotný ji vyžaduje: příkaz `import module` hledá soubor `module.py`.

Přípony jsou zvlášť důležité na Windows, kde se podle nich vybírá program,
kterým se soubor otevře.
(Unix se oproti tomu dívá v prvé řadě na samotný obsah souboru.)

Přípon se může objevit i víc: `archiv.tar.gz` nejspíš obsahuje několik souborů spojených dohromady ve formátu [tar](https://cs.wikipedia.org/wiki/Tar_%28informatika%29) a pak zkomprimovaných ve formátu [gzip](https://cs.wikipedia.org/wiki/Gzip).
