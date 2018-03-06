# HTTP – Jak funguje Internet

Než začneme pracovat s internetem – ať už tvorbou vlastních stránek, nebo
komunikací s existujícími službami, pojďme si přiblížit, co vlastně ten
internet je a jak funguje.

Internet je celosvětová síť počítačů.
Je to spousta laptopů, stolních počítačů, malých blikajících krabiček
i obrovských blikajících skříní, které jsou navzájem propojeny pomocí
kabelů (nebo i bezdrátově).

Samozřejmě není každé zařízení propojené s každým jiným zařízením – tolik
kabelů by se na Zemi těžko vešlo.
Spousta zařízení – hlavně tzv. *routery* a *switche* – ale umí přeposílat
zprávy mezi sebou tak, že každý počítač může komunikovat s každým
jiným počítačem.
(Aspoň teoreticky – reálně je komunikace omezená např. kvůli bezpečnosti.)

Funguje to podobně jako pošta: když pošlu balíček z Brna do Melbourne,
nedostane se tam přímo.
Balíček poputuje třeba vlakem do Prahy, pak letadlem do hlavní pošty
v Austrálii a odtud náklaďákem do Melbourne, kde ho doručovatel donese až
k domu příjemce.
A k naplánování celé téhle cesty stačí napsat na obálku krátkou adresu.

Podobně cestují informace v internetu: z laptopu přes Wi-Fi do *routeru*,
odtud kabelem k poskytovateli připojení, tlustším kabelem do české
„páteřní sítě“, podmořským kabelem třeba do Ameriky… a nakonec k počítači,
se kterým jsem chtěl komunikovat.

Většinou můj laptop takhle komunikuje se *serverem*, počítačem, který
se stará o sdělování informací.
Každou webovou stránku spravuje takový server.

{{ anchor('url-anatomy') }}
## Webové adresy

Jak taková komunikace vypadá si ukážeme na příkladu –
co se stane, když do prohlížeče zadám tuhle adresu:

```plain
http://naucse.python.cz/lessons/fast-track/http/
```

Taková webová adresa – technicky zvaná URL (*Uniform Resource Locator*,
„jednotná adresa zdroje“) přesně určuje, jak se má prohlížeč dostat
k informacím, které má zobrazit.

{{ figure(
    img=static('url-anatomy.svg'),
    alt='http://naucse.python.cz/lessons/fast-track/http/'
) }}

Začátek adresy, `http://`, je jméno *protokolu* (angl. *protocol name*).
Protokol určuje způsob, *jak* se k daným informacím dostat.
Protokolů existuje spousta, každý funguje trochu jinak a každý se používá
na něco jiného:
SMTP a POP pro e-mail, FTP pro přenos souborů, SSH pro ovládání počítačů.
My se teď ale zaměříme na HTTP, který se typicky používá pro webové stránky.


Další část adresy, `naucse.python.cz`, je *jméno serveru* (angl. *server name*).
Říká, *kde* prohlížeč najde dané informace.

Jméno serveru je jako poštovní adresa – existuje počítač, který se jmenuje
`naucse.python.cz`, a každý internetový „pošťák“ ví, komu přeposlat zprávu,
aby se k tomuto počítači nakonec dostala.

> [note]
> „Skutečná“ adresa počítače, tzv. IP adresa, je číselná – například
> `151.101.37.147` nebo `2a04:4e42:9::403`.
> Existuje ale systém, jak jméno serveru na takovou *IP adresu* přeložit.
> Tenhle systém se jmenuje DNS a – abychom zůstali u přirovnání k poště –
> funguje podobně jako seznamy poštovních směrovacích čísel.


Poslední část URL, `/lessons/fast-track/http/`, je *cesta* (angl. *path*).
Říká, *co* chceme od serveru dostat: jméno konkrétní webové stránky.

U jednodušších stránek to může být přímo jméno souboru, který má server
uložený na disku – proto spousta adres na Webu končí příponou `.html`.


## Požadavek a odpověď

K získání požadované stránky prohlížeč vytvoří *požadavek* (angl. *request*)
– zprávu „Pošli mi prosím stránku `/lessons/fast-track/http/`“ – a pošle ho
serveru `naucse.python.cz`.

Server požadavek dostane a vrátí *odpověď* (angl. *response*) – zprávu
s obsahem dané stránky.
Obsah je často webová stránka v jazyce HTML, který popisuje co na stránce je,
kde jsou nadpisy a kde odstavce, jak má stránka vypadat, a tak dále.
Ale v odpovědi může být místo stránky i cokoli jiného – obrázek, video, nebo
jiná data.

Veškerá komunikace přes HTTP funguje právě takto: pošle se požadavek
a přijde na něj odpověď.

A jak tyhle zprávy vypadají?
Požadavek nějak takhle:

```http
GET /lessons/fast-track/install/ HTTP/1.1
Accept: */*
Accept-Encoding: gzip, deflate
Connection: keep-alive
Host: naucse.python.cz
User-Agent: Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:58.0) Gecko/20100101 Firefox/58.0
```

První řádek říká serveru: prosím, pošli mi (`GET`) stránku
`/lessons/fast-track/install/` s použitím protokolu `HTTP` verze `1.1`.
Další řádky jsou *hlavičky* (angl. *headers*).
Říkají například kdo se ptá (`User-Agent`) a jaký obsah očekává (`Accept`).
Většina hlaviček je nepovinná.

Odpověď pak může vypadat takto:

```http
HTTP/1.1 200 OK
Cache-Control: max-age=600
Connection: keep-alive
Content-Encoding: gzip
Content-Length: 3127
Content-Type: text/html; charset=utf-8
Date: Tue, 20 Feb 2018 15:51:24 GMT
Last-Modified: Tue, 20 Feb 2018 15:20:08 GMT
Server: GitHub.com

<!doctype html>
  <html lang="cs">
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
        <title>
                Python a jeho knihovny: HTTP – Jak funguje Internet
…
```

První řádek říká: používáme protokol `HTTP` verze `1.1`,
a všechno je v pořádku (`200 OK`).
Kromě `200` existují i další [stavové kódy] (angl. *status codes*).
Známý je např. `404` „nenalezeno“.

[stavové kódy]: https://en.wikipedia.org/wiki/List_of_HTTP_status_codes

Následují opět hlavičky – např. kdo odpovídá (`Server`), kdy byla stránka
naposledy změněna (`Last-Modified`) a jak je odpověď zakódovaná:
`Content-Type: text/html` říká, že je to stránka v jazyce HTML.

Hlavičky jsou ukončené volným řádkem, po kterém následuje samotný obsah
odpovědi ve zmíněném jazyce HTML.


## HTTP Metody

Komunikace ukázaná výše používala metodu `GET`, která slouží ke *čtení*
informací.
Když se takto prohlížeč na nějakou stránku zeptá, nic se na serveru nezmění.
Prohlížeč si takovou stránku – nebo třeba obrázek či video – může dočasně
uložit, a když bude potřeba znovu, použít uloženou verzi.

Některými požadavky ale stav serveru mění: například se přihlásí uživatel,
nakoupí zboží v e-shopu nebo odešle zpráva do diskuse.
Tyto požadavky používají místo `GET` jinou *metodu* (angl. *method*).
Co přesně která metoda na jaké adrese dělá, to záleží na autorovi stránek.
Často se používají tyto metody:

* `GET` načte informace,
* `POST` pošle na server informace, např. z formuláře, s cílem něco
  změnit nebo nastavit,
* `PUT` přidá novou stránku (nebo jiný objekt),
* `DELETE` něco smaže.

Seznam všech metod je ve
[specifikaci](https://www.w3.org/Protocols/rfc2616/rfc2616-sec9.html).

U složitějších požadavků se dají na server poslat i informace:
webové formuláře se odesílají požadavkem, který používá metodu `POST`
a vyplněné informace k dotazu „přilepí“ za hlavičky – stejným způsobem, jako se
v odpovědi posílá HTML stránka.
