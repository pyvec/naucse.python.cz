# MicroPython na malém zařízení

> [note] Tahle sekce bohužel nejde jednoduše projít z domu.
> Využíváme speciální vybavení, které je potřeba nejdřív
> sehnat. Máš-li možnost se dostat na sraz, nebo
> aspoň kontaktovat organizátory, doporučujeme shánět
> spíš tímto způsobem.
> Případně jde daný hardware objednat přes Internet,
> typicky z čínských e-shopů.

{{ figure(
    img=static('nodemcu-devkit.jpg'),
    alt='LoLin NodeMCU v3 – Vývojová deska s čipem ESP8266',
    float='right',
) }}

Dnes budeme programovat malé zařízení –
tak malé, že se ho pohodlně schováš v ruce.
Konkrétně budeme používat „chytrou destičku”, modul zvaný
*NodeMCU Devkit*, která by měla ležet před tebou.
Než ji vyndáš z obalu, měl{{a}} by ses *vybít*:
dotkni se něčeho kovového, co je spojeno se zemí,
třeba radiátoru nebo kovové části schránky nějakého
spotřebiče, který je zapojený do zásuvky.
Tím se zbavíš statické elektřiny, která by mohla
malinké zařízení poškodit.
Pak přístroj vyndej z obalu. Snaž se ho držet za
hrany a příliš se nedotýkat elektroniky a kovových
částí.

> [note]
> Obal bude nejspíš roztržený, protože organizátoři
> na destičku před začátkem kurzu nainstalovali
> MicroPython.

> [warning]
> Obal je vodivý a nesmí přijít do styku se zapojenou destičkou,
> protože by mohl zkratovat její vývody a tím ji zničit.
> Proto obal raději hned schovej a používej ho jen k transportu destičky.

Teď, když destičku držíš v ruce, si
pojďme projít její základní součásti.

<br style='clear: both;'>

{{ figure(
    img=static("nodemcu-popisky.svg"),
    alt='Obrázek desky NodeMCU DevKit',
    float='left',
) }}

Nejdůležitější část vývojové desky je v oplechované
krabičce s logem "Wi-Fi" a "FCC":
<span class="part-green">mikroprocesor ESP8266</span>.
To je „mozek” celého zařízení, který – když je
správně naprogramován – umí provádět pythonní
příkazy a programy.
Procesor sedí na malé destičce, na které je ještě
<span class="part-cyan">anténa</span>, kterou
přístroj může komunikovat s okolím.

Tahle malá destička se dá použít i samostatně;
všechno ostatní, co kolem ní zabírá tolik místa,
nám jen ulehčí hraní a umožní se zařízením
jednoduše komunikovat a krmit ho elektřinou.

Komunikace a „krmení” se děje přes
<span class="part-red">mikro-USB konektor</span>,
do kterého zapojíš kabel ze svého počítače.
Když je modul naprogramovaný, stačí ho místo do
počítače zapojit do nabíječky či externího zdroje
(powerbanky) a bude fungovat samostatně.

Kolem USB konektoru jsou dvě tlačítka:
<code class="part-orange">RST</code>, kterým se destička restartuje
(skoro jako kdybys ho odpojila a zase zapojila, což
se hodí, když něco uděláš špatně a modul „zamrzne”),
a <code class="part-yellow">FLASH</code>, o kterém si povíme později.

Po stranách modulu jsou dvě řady
<span class="part-blue">„nožiček”</span>, na které
se dá napojit celá řada nejrůznějších hraček.
Zkontroluj si, jestli jsou všechny nožičky rovné;
kdyby byla některá ohnutá, tak ji (nejlépe s pomocí
kouče) narovnej nebo si vezmi jinou destičku.

<br style='clear: both;'>
