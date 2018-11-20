# Hra typu Had

Dnes to všechno — třídy, grafiku, seznamy a tak dále –
spojíme dohromady do závěrečného projektu.
Doufám, že se ti bude líbit!

Naším cílem bude vytvořit klon známé hry [Snake (neboli Had)](<https://en.wikipedia.org/wiki/Snake_(video_game_genre)>)
jejíž princip je tu s námi od roku 1976. Největší popularity se Had dočkal
díky mobilním telefonům Nokia, kde je jako základní hra dostupný od roku 1998
až dodnes.

Projekt není zase tak složitý, protože jeho základní principy už dobře znáš
z domácích projektů a lekcí kurzu. Následující text je tedy spíše
zadání než výukový materiál a v projektu jistě narazíš na něco, co jsme
společně neprobírali. V takovém případě se neboj zeptat nebo si informace
dohledat!

A ještě jedna věc: protože začátečnický kurz končí,
začneme kód psát v angličtině, aby se pak dal sdílet s celým světem.

> [note]
> Procházíš-li si projekt doma, je možné, že narazíš na
> něco s čím si nebudeš vědět rady.
> Kdyby se to stalo, prosím, ozvi se nám!
> Rádi ti s projektem pomůžeme.

## Logika hry a fáze projektu

Základní princip hry máš v malíčku, pokud jsi dokončil{{a}} domácí projekt
po [lekci o seznamech](../../beginners/list/). Pokud jej nemáš, doporučuji
se k němu vrátit.

Práci s pygletem jsme dělali v [lekci o grafice](../../intro/pyglet/).

Teď nám nezbývá než princip tolik populární hry a znalosti z kurzu spojit
dohromady. Doporučuji začít s čistým souborem v prázdné složce a do hotových
programů se koukat jen v případě potřeby.

Jak postupovat, aby se projekt nezdál nedosažitelný už na začátku? Třeba takto:

0. Promysli si, jak bude hra fungovat a jak přeneseme mřížku s hadem
z příkazové řádky do grafického okna.
1. Vykresli hada do grafického okna (ve formě barevných čtverců)
2. Přidej funkci, která bude hadem hýbat.
3. Umožni změnit směr hada pomocí klávesnice.
4. Nenech hada utéct z herní plochy a nabourat do sebe sama.
5. Přidej hadovi jídlo a zajisti, aby po jídle rostl.
6. Vyměň barevné čtverečky za opravdovou grafiku.

Po těchto krocích budeš mít základní hru, ale tou to nekončí, právě naopak!
Budeš mít vlastní hru, jejímuž fungování rozumíš jako nikdo jiný, a to je to pravé pro
přidávání dalších možností. Fantazii se meze nekladou. Například:

1. Ve hře mohou být dva nebo třeba tři hadi najednou – každý ovládaný
jinými klávesami — navzájem soupeřící o jídlo.
2. Kromě jídla se mohou na ploše objevovat i jiné objekty – překážky,
do kterých nesmí had narazit, otrávené jídlo, které hada zkrátí atp.
3. Hrací plocha může být nekonečná a když z ní had vyleze, objeví se
na druhé straně.

## Z příkazové řádky do grafické aplikace

V příkazové řádce měl had souřadnice označující řádek a sloupec. V grafické
aplikaci to bude podobné, ale protože pixelů na obrazovce je mnohem více, budeme
si muset vytvořit pomyslnou síť stejně velkých čtverců, které nám nahradí
řádky a sloupce. Velikost takového čtverce bude konstanta, kterou se vyplatí
mít po celou dobu hry k dispozici, aby se podle ní daly vypočítat
souřadnice k vykreslení obrázků. Pro začátek řekněme, že ideální velikost
takového čtverce bude 64 × 64 pixelů.

Z velikosti čtverce, kterou si můžeme v budoucnu libovolně změnit,
a velikosti okna aplikace můžeme vypočítat, kolik se nám do okna takových
čtverců vejde na šířku a na výšku a tím i zjistit, kolik pomyslných
sloupců a řádků bude naše hrací plocha mít.

## Vykreslení hada

Abychom mohli hada vykreslit, potřebujeme si pro začátek uložit jeho souřadnice.
K tomu můžeš použít seznam dvojic – stejně jako v domácím projektu. Podobných
informací, které se budou v průběhu hry dynamicky měnit, budeme mít už
za malou chvíli více. Proto dává smysl si pro stav hry vytvořit třídu, která
bude tyto informace obsahovat jako atributy a bude s nimi umět pracovat.

> [note]
> I když se může na začátku zdát vlastní třída jako zbytečná
> komplikace, později zjistíš, že ne všechno by se dalo snadno udržovat v globálních
> proměnných.

{{ figure(
    img=static('coords.svg'),
    alt="Had na „šachovnici“ se souřadnicemi",
) }}

Když už je had definován, budeme potřebovat jednoduchou funkci, která
na ta správná místa umístí obrázky. Pro začátek si vystačíme se zeleným
čtvercem. Obrázek si [stáhni zde]({{ static('green.png')}}) a ulož
do složky k programu.

Stejně jako na lekci i zde použijeme pro vykreslení `Sprite`, kterému už při
vytvoření můžeme zadat obrázek pro vykreslení a vypočtené souřadnice.
Pro jednoduchost stačí `Sprite` vytvořit, vykreslit a „zapomenout“. Není to ale
optimální přístup a tak tohle může být jedním z adeptů pro pozdější vylepšení.

## Rozpohybování hada

Aby se mohl had hýbat, potřebuje znát směr pohybu. V příkazové řádce jsme
vždy počkali, až nám směr zadá uživatel, ale v opravdové hře se bude had
pohybovat sám. Bude tedy potřeba nějaký atribut v naší třídě, kde bude směr
neustále uložen a měnit se bude podle stisknutých kláves v dalším kroku.

Směr pohybu může být uložen v libovolné podobě – světové strany, slovní
označení strany, nebo třeba dvojice s číselným označením pohybu
(`(0, 1)` pro pohyb nahoru, `(-1, 0)` pro pohyb doleva atp.). Podle vybraného
formátu pak bude třeba směr zpracovat.

Pro tuhle chvíli mu tedy bude stačit nastavit směr napevno a napsat funkci,
nebo metodu, která hadem pohne. Pohyb bude probíhat
naprosto stejně jako v příkazové řádce – přidáme do seznamu souřadnice,
kde by měla být „nová hlava“ a umažeme poslední kousek hada.

Protože se pohyb má provádět pravidelně, bude potřeba tuto operaci provádět
automaticky v pravidelných intervalech. `pyglet.clock.schedule_interval` je
zde jasná volba.

## Ovládání pomocí klávesnice

Reagovat na stisknuté klávesy jsme se už taky učili. Teď to tedy využijeme,
abychom dokázali změnit nastavený směr pohybu z předchozího bodu. Bude pro to
samozřejmě potřeba funkce, kterou v pygletu zaregistrujeme pro spuštění po
stisku klávesy.

Protože had už se nám v závislosti na směru pohybuje, měl by začít reagovat
na jeho změnu.

V tuto chvíli:

* Směr se mění podle stisknuté klávesy.
* Had se sám pohybuje podle zadaného směru.
* Nová pozice hada se automaticky vykresluje jako zelené čtverečky.

Vida, máme hotový základ!

## Nenechme ho utéct

Had už se nám hýbe podle našich představ, ale stačí ho nechat chvíli bez dozoru
a uteče nám z hrací plochy. Tomu není těžké zabránit, když víme, že žádná
souřadnice hada nesmí být menší než nula a větší než je velikost hrací plochy.
Kontrolovat je potřeba souřadnice jeho hlavy, která bude vždy všude jako první.

Reagovat na náraz do zdi se dá mnoha způsoby. Nejjednodušší by asi bylo
ukončit hru, ale to by se pak hráč nemohl podívat na tu šlamastiku, do které
se dostal. Proto bude lepší místo toho pouze zastavit časovač, který se stará
o pohyb hada.

Stejným způsobem a na stejném místě v programu bude třeba vyřešit i situaci,
kdy had narazí sám do sebe.

## Jen ať jí, hlavně že mu chutná

Jezdit s hadem po hrací ploše může být chvíli zábava, ale protože had neroste,
není to žádná výzva. A aby mohl růst, potřebuje jíst.

K tomu budeš potřebovat další globálně dostupný seznam (nejlépe atribut
existující třídy), který bude obsahovat informace (souřadnice) o existujícím
jídle na hrací ploše. Navíc bude potřeba mít k dispozici metodu, která bude
umět jídlo na hrací plochu přidat.

Záleží jen na tobě, zda se bude nové jídlo objevovat, když had jedno
z existujících sní, nebo automaticky v pravidelných intervalech.

Jídlo vykreslíme stejným způsobem jako hada (ve stejné funkci/metodě) a jako
obrázek použijeme třeba [jablko]({{ static('apple.png')}}).

První závan grafiky :-)

## Čtverečky ven, grafiku sem

Čtverečky jsou fajn, ale hra by měla lahodit oku a had by měl vypadat jako had.
K tomu máme připravenou sadu obrázků - [ke stažení zde]({{ static('snake-tiles.zip') }}).
Archiv si rozbal do adresáře s hrou tak, aby adresář `snake-tiles` byl na stejné
úrovni jako soubor s programem.

{{ figure(
    img=static('snake-tiles.png'),
    alt="Kousky hada",
) }}

### Načtení všech obrázků ze složky

Nejdříve si načteme všechny obrázky do hry, abychom je pak mohli bez potíží
použít. Protože se nechceme opakovat (DRY), bude potřeba to udělat nějak
poloautomaticky. Python obsahuje knihovnu [`pathlib`](https://docs.python.org/3/library/pathlib.html),
která umí velmi přehledně pracovat s cestami k souborům a třeba nám dát
i seznam všech souborů ve složce.

Nejdříve si z této knihovny naimportujeme třídu `Path`, která reprezentuje
soubor či složku na disku a vytvoříme z ní instanci, která bude
ukazovat do naší složky s obrázky.

```python
from pathlib import Path

TILES_DIRECTORY = Path('snake-tiles')
```

Třída `Path` má metodu `glob()`, která nám ze zadané cesty umí vrátit sekvenci
s názvy souborů dle argumentem zadaných kritérií. My potřebujeme všechny soubory
s příponou `.png` bez ohledu na jméno. Jakýkoli řetězec je v regulárních
výrazech označen hvězdičkou (`*`), takže argument pro metodu `glob()` bude
`*.png`, což označuje jakýkoli soubor s příponou `.png`. Jako výsledek
dostaneme sekvenci cest k souborům s obrázky, kterou můžeme projít pomocí cyklu
`for`, a každý obrázek si můžeme načíst do slovníku, kde hodnotou bude samotný obrázek
`pyglet.image` a klíčem jeho název. Z názvu však potřebujeme jen samotný název souboru
bez přípony a názvu složky – ten je uložen v atributu `stem`.

Výsledný slovník by měl vypadat takto:

```
{'right-tongue': <ImageData 64x64>, 'top-tongue': <ImageData 64x64>,
 'right-top': <ImageData 64x64>, 'left-bottom': <ImageData 64x64>,
 'tail-left': <ImageData 64x64>, 'bottom-tongue': <ImageData 64x64>,
 'left-top': <ImageData 64x64>, 'bottom-bottom': <ImageData 64x64>,
 ...
```

Pokud je tohle pro tebe příliš mnoho nových věcí najednou a nedaří se ti to
vyřešit, zkus to ještě jednou a pak se můžeš podívat na řešení.

{% filter solution %}
```python
from pathlib import Path

import pyglet

TILES_DIRECTORY = Path('snake-tiles')

snake_tiles = {}
for path in TILES_DIRECTORY.glob('*.png'):
    snake_tiles[path.stem] = pyglet.image.load(path)

print(snake_tiles)
```
{% endfilter %}

### Housenka

Než se začneme zabývat různými obrázky, uděláme pokus k ověření, že nám vše stále funguje.
Jako mezistupeň od hranatého hada k jeho věrné grafické podobě vytvoř housenku.
Uděláš to jednoduše tak, že místo zeleného čtverce použiješ k vykreslení hada
obrázek `tail-head.png`, který máš ve slovníku načten jako pod klíčem `tail-head`.

Funguje? No výborně! Před pokračováním si u jeho hraní na chvíli odpočiň.
Začne to být náročnější.

{{ figure(
    img=static('screenshot-cat.png'),
    alt="Housenka",
) }}

### Výběr správných obrázků

Jistě sis všiml{{a}}, že některé obrázky v naší sadě jsou téměř identické a liší
se jen v otočení. V tuhle chvíli máme totiž dvě možnosti, jak vykreslit
celého hada pomocí správných obrázků na správných pozicích:

1. Můžeme vzít jeden obrázek pro tělo, jeden pro ohyb a po jednom pro
hlavu a ocas a ty otáčet tak, jak to bude pro konkrétní kousek hada potřeba.
2. Můžeme využít všech dostupných (různé otočených) obrázků a použít ten
správný obrázek na tom správném místě.

Bod č. 2 je v tuto chvíli snazší a tak budeme pokračovat tímto způsobem.

Jak vybrat správné obrázky na ta správná místa? Jména obrázků (klíče ve slovníku)
obsahují informaci, odkud kam daný obrázek vede. Stačí se tedy při
vykreslování každého kousku hada podívat na umístění jednoho před ním
a jednoho za ním a podle toho vybrat ze slovníku ten správný obrázek.
U každého kousku hada a kousku před i za ním tě budou zajímat jejich
souřadnice, protože podle nich lze velmi snadno poznat, zda je zkoumaný kousek
nalevo, napravo, nahoře, nebo dole.

Způsobů, jak toho docílit, je celá řada a i když se to může zdát jako složitější
úkol, vše potřebné k jeho vyřešení znáš.

{{ figure(
    img=static('screenshot-final.png'),
    alt="Finální had",
) }}

Odměnou za vyřešení ti bude kompletní grafická hra Had. Gratuluji!

## Optimalizace, úklid

Než se po dokončení základní hry vrhneš na její rozšiřování, měl by se celý kód
uklidit a zpřehlednit, aby se v něm další úpravy dělaly snáze a s menším
rizikem, že se něco pokazí.

Body k zamyšlení:

* Pokud se ti tam opakuje nějaký kousek kódu vícekrát, možná by se dal
vložit do funkce nebo cyklu.
* Mají všechny proměnné smysluplná jména?
* Při vykreslování možná tvoříš pro každý kousek hada nový `Sprite` a ten
je po vykreslení zapomenut. Optimálnější by možná bylo použít seznam
a v něm všechny instance třídy `Sprite` uchovávat a používat znovu a znovu.
`Sprite` přeci můžeme posunout na libovolné místo i změnit obrázek, který
obsahuje.
* Používáš globální proměnné? Nebylo by lepší mít jednu třídu pro stav hry
a v ní všechny podstatné informace a metody?
* Funguje ovládání dle tvých představ nebo by šlo nějak zlepšit?
