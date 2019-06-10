# Motorky

Pojďme ovládat stejnosměrné motory!

Motory potřebují, na rozdíl od počítače a LED světýlek, celkem hodně elektrické
energie, a navíc můžou dokonce energii vyrábět (fungují jako dynamo).
Kdybys je připojil{{a}} přímo k destičce, která na tolik proudu není
připravená, mohla by se destička zničit.

Představ si náramkové hodninky a traktor: obě zařízení něčím točí (ručičkami
nebo koly), ale kdybys připojil{{a}} motor z traktoru na mechanismus hodinek,
moc dlouho by správný čas neukazovaly.
A motůrek z hodinek by zase nepohohl při orání pole.

Proto použijeme čip s názvem L293D, který elektřinu potřebnou pro “hrubou sílu”
motorku odstínit od logických signálů z destičky.

Potřebnou energii dodáme z baterií.

Čip je černá krabička, která na sobě má trochu textu, ale ne dost na to,
abys poznal{{a}} co dělá.
To je deteilně popsáno v takzvaném *datasheetu* – PDF, které vypadne když
zadáš „L293D“ do vyhledávače.
Tam lze najít kompletní popis této součástky včetně diagramy, který ukazuje
kde najít kterou nožičku:

{{ figure(img=static('l293d.svg'), alt="L293D pinout") }}

Všimni si, že nahoře je znázorněné „vykousnutí“ (zde oranžově),
které najdeš i na součástce.
Je důležité mít čip správně otočený, jinak nebudeš zapojovat správné nožičky.

Čip posílá do své nožičky `1Y` energii z_`Vpower`, pokud je signál na
`1A` i `1,2EN` současně. Jinak nožičku `1Y` spojí se zemí (`GND`).
Podobně pro `2Y` (`2A` i `1,2EN`), `3Y` (`3A` i `3,4EN`), `4Y` (`4A` i `3,4EN`).
Co to pro nás znamená, je vysvětleno níže.)


# Zapojení

Čip a motorky zapoj následovně:

* Napájení
  * V<sub>logic</sub> čipu k 5V – `Vin` na destičce
  * V<sub>power</sub> čipu k `+` na baterii
  * GND (jedno který) čipu k `GND` na destičce
  * GND (jedno který) čipu k `-` na baterii
* První motorek:
  * `1A` čipu na `D1` na destičce
  * `2A` čipu na `D2` na destičce
  * `1,2EN` čipu na `D3` na destičce
  * `1Y` a `2Y` čipu k dvěma kontaktům motorku
* Druhý motorek:
  * `3A` čipu na `D6` na destičce
  * `4A` čipu na `D7` na destičce
  * `3,4EN` čipu na `D8` na destičce
  * `3Y` a `4Y` čipu k dvěma kontaktům motorku

{{ figure(img=static('motors_bb.svg'), alt="L293D pinout") }}


# Ovládání

Motorek se točí, pokud je na jeho kontaktech rozdíl napětí: pro první motorek
musí být na `1Y` jiná hodnota než na `2Y`.
Pro obě musí být aktivní nožička `1,2EN`, a pak `1A` ovládá `1Y` a
`2A` ovládá `2Y`.

```
from machine import Pin

pin_1a = Pin(5, Pin.OUT)  # D1 na destičce, 1A na čipu
pin_2a = Pin(4, Pin.OUT)  # D2 na destičce, 2A na čipu
pin_12en = Pin(0, Pin.OUT)  # D3 na destičce, 1,2EN na čipu

pin_1a.value(1)
pin_2a.value(0)
pin_12en.value(1)
```

Když prohodíš hodnoty `pin_1a` a `pin_2a`, motorek se začne točit opačným
směrem.

Pro nastavení rychlosti otáčení se hodí použít obdélníkovou vlnu, PWM,
nastavenou na nožičce `1,2EN`:

```
from machine import Pin

pwm_1 = PWM(pin_12en, freq=100, duty=512)
...
pwm_1.duty(1024)
...
pwm_1.duty(256)
```

Druhý motorek se dá ovládat podobně, jen s jinými čísly pinů.
Tady jsou:

```
pin_3a = Pin(12, Pin.OUT)  # D6 na destičce, 3A na čipu
pin_4a = Pin(13, Pin.OUT)  # D7 na destičce, 4A na čipu
pin_34en = Pin(15, Pin.OUT)  # D8 na destičce, 3,4EN na čipu
```



