# Had

Pojďme si udělat hru!

Uděláme hru [Had](https://en.wikipedia.org/wiki/Snake_(video_game)),
která existuje v různých variantách od sedmdesátých let.
Je to ideální hra pro začínající programátory: technicky poměrně
jednoduchá, známá (takže budeme řešit *jak* ji naprogramovat, spíš než
*co* máme programovat), a zábavná (což možná produktivitě nesvědčí,
ale výsledek nebude nudný).

Naše hra bude vypadat zhruba násldovně:

{{ figure(
    img=static('screenshot-finished.png'),
    alt="Screenshot hotové hry",
) }}

Had se bude normálně pohybovat dopředu, ale hráč ho pomocí šipek na
klávesnici může otáčet.
Když had „vyleze“ ven z okýnka, objeví se na druhé straně.
Na herní ploše bude jídlo, po jehož sežrání jídla had povyroste.
Když had narazí sám do sebe, hra končí.


## Osnova

Na začátku každého podobného projektu je dobré si ujasnit, co zhruba budeme
dělat, rozvrhnout si práci, stanovit první krok, který povede k cíli.

U tohohle projektu je takové plánování už vyřešené, takže jednotlivé kroky
na sebe budou plynule navazovat a budou seřazené tak, aby ses u to co nejvíc
(a co nejlíp) naučil{{a}}.
Podotýkám, že u „opravdového“ programování to tak většinou není, a cestu si
musíš hledat {{gnd('sám', 'sama')}}.

Jak to tedy uděláme?

Nejdřív hada *vykreslíme* – převedeme seznamy, <var>n</var>-tice a čísla
na obrazovku, zatím bez pohybování a co nejjednodušeji – bez obrázků,
které je potřeba vybírat a otáčet.

Pak přidáme jídlo, hteré had bude jíst. Pro představu, hra bude zatím
vypadat takto:

{{ figure(
    img=static('screenshot-initial.png'),
    alt="Screenshot první části hry",
) }}

Potom hada oživíme – naprogramujeme logiku hry: pohyb, zatáčení, krmení,
ale i narážení.

Nakonec, zbude-li čas a nálada, hada převlečeme do hezčího „kabátku“
a zabalíme tak, aby se dla hrát i na počítačích, kde není nainstalovaný
Python.

Připraven{{a}}? do toho!

* [Vykreslení hada](./drawing/)

