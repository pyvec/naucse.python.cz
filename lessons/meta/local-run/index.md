# Vytvoření lokálního kurzu

Teď, když už máš lokální instalaci aplikace Nauč se Python, můžeš začít vytvářet vlastní kurz.

První věc, kterou musíš udělat, je vybrat si identifikátor kurzu, pod kterým bude kurz uložený.
Tento identifikátor také bude ve všech adresách, které se budou týkat tohoto kurzu.
Identifikátor se může skládat pouze z malých alfanumerických znaků a spojovníků (`-`) a musí být unikátní, alespoň v daném roce.
Jak zjistit, jestli už identifikátor existuje? Podívej se do složky `runs` a pak dále do složky, která odpovídá roku, ve kterém tvůj kurz začíná.

> [note] Jak vybrat identifikátor?
> Ze správného identifikátoru (v kombinaci s rokem) by mělo být jasné, o který kurz se jedná.
> Dobrý příklad je třeba `2017/mi-pyt`, identifikátor pro předmět MI-PYT, který začal v roce 2017.
> Pro jiné kurzy může být problém přijít na unikátní identifikátor.
> Například kurzy PyLadies se organizují ve více městech několikrát ročně.
> Poté se do identifikátoru přidává i město a označení, který je to kurz v daném roce – například `2018/pyladies-ostrava-jaro`.
> Třeba v Praze ale zároveň běží i více kurzů najednou, tak se používá `2018/pyladies-praha-jaro-cznic` a `2018/pyladies-praha-jaro-ntk`, poslední část zde říká, kde se kurz koná.
>
> <br />
> Takže doporučení jsou následovné:
>   * Když víš, že kurz se stejným názvem bude v daném roce jediný, identifikátor by měl být název, bez diakritiky a se spojovníky místo mezer.
>   * Když se stejně pojmenovaný kurz koná ve více městech, přidej název města.
>   * Když se kurz koná vícekrát za rok, přidej označení v daném roce (například roční období).
>   * Když se koná více kurzů se stejným názvem ve stejném městě najednou, přidej lokaci nebo den, pokud se konají na jiných místech nebo v jiné dny.

Když už máš vymyšlený identifikátor, vytvoř ve složce s rokem složku, která se bude jmenovat podle tvého identifikátoru.
Pokud ještě složka pro daný rok neexistuje, musíš ji vytvořit také.

## Definice kurzu

Kurz se definuje pomocí souboru `info.yml`, který se umisťuje právě do složky, kterou jsi výše vytvořil{{a}}.
Tento soubor obsahuje všechny informace o kurzu – název, popisek, kde a kdy se koná a pak samozřejmě plán jednotlivých lekcí.
Soubor je formátu YAML, který si teď trochu ukážeme.

### O formátu YAML

Formát se skládá z několika stavebních bloků, které se dají poté skládat dohromady.
Prvním je seznam hodnot (podobně jako v Pythonu).
Seznam se ve formátu YAML zapisuje následovně:

```yaml
- První položka
- Druhá položka
- 3
- Položka může být i něco jiného než text!
```

Druhým stavebním blokem je slovník (zase podobně jako v Pythonu), který se skládá z klíčů a hodnot, nezáleží v ní tedy na pořadí, protože se k informaci vždy člověk dostance pomocí klíče.
Slovník se ve formátu YAML zapisuje následovně:

```yaml
klic1: Hodnota klíče klic1.
klic2: 2
klic3: I hodnoty ve slovníku mohou být něco jiného než text.
klic4: |
    Pokud potřebuješ zapsat nějaký delší text, uděláš to takhle.

    Tento text budou dva separátní odstavce v rámci jednoho klíče.
klic5:
klic6: Jak vidíš v klíči klic5, hodnota může být i prázdá.
```

Seznamy a slovníky jde samozřejmě i skládat dohromady:

```yaml
klic1: Hodnota klíče
klic2:
- Tohle je seznam, které patří pod klíč klic2
- vnorenyklic: Můžeme skládat jednotlivé typy skoro do nekonečna.
- vnorenyklic: Klíče musí být unikátní jen v rámci jednoho slovníku, takže to může být takto.
klic3:
  vnorenyklic: Slovník může obsahovat další slovník i takto.
```

### Povinné informace

Teď, když už se vyznáš ve formátu YAML, můžeš začít vytvářet soubor `info.yml`.
Celá definice kurzu je jeden velký slovník, který si postupně popíšeme a vyplníme.
Pro potřeby kurzu je [připravena šablona]({{static("info.yml")}}), kterou můžeš použít.

Nejdřív prvních pár základních povinných údajů:

* `title` slouží pro název kurzu (nepovinně lze dodefinovat pomocí `subtitle`)
* `description` slouží pro krátký popis kurzu (který se zobrazí v seznamu kurzů)
* `long_description` slouží pro dlouhý popis kurzu, který se zobrazí na stránce kurzu

A teď už jen nepovinné údaje:

* `place` slouží pro označení místa
* `time` slouží pro informaci o času (není nutný žádný specifický formát)

Jestli chceš, aby pro kurz šel vygenerovat iCal soubor s plánem lekcí, musíš dále poté vyplnit údaj `default_time`.
Tato hodnota musí být slovník, který obsahuje dva klíče `start` a `end`, kde bude čas lekcí.
Čas musí být ve formátu `HH:MM` a musí být obalen uvozovkami nebo apostrofy (kvůli té dvojtečce, aby si YAML nemyslel, že je to další slovník), takže třeba takhle:

```yaml
default_time:
  start: '18:00'
  end: '20:00'
```

Poslední nepovinná hodnota, než se dostaneme k obsahu kurzu, jsou proměné, které se definují klíčem `vars` a musí být také slovníkem.
Proměné mohou upravovat obsah lekcí a stránek kurzu, a pokud budeš vytvářet nebo upravovat materiály, můžeš si i definovat vlastní.

První proměnou, kterou můžeš použít, je `coach-present`.
Pokud je tvůj kurz s lektorem nebo koučem, nastav tuto proměnou na hodnotu `true`.

Druhou proměnou, kterou můžeš použít je `user-gender`.
Pokud víš, že na tvém kurzu budou lidé jen jednoho pohlaví, můžeš nastavit materiály (které tak byly napsány), aby vykreslily správně formátovaný obsah.
Nastavíš to pomocí písmenka `f` pro ženy, `m` pro muže.
Pokud proměnou nevyplníš, materiály vykreslí obě varianty.

Další proměnou, kterou můžeš použít, je `pyladies`.
Tu využij (nastavenín na hodnotu `true`), pokud organizuješ kurz PyLadies.
Tato proměná aktivuje v materiálech nějaké popisky navíc, například o tahácích, nebo také sjednotí názvy složek na `pyladies`.

### Plán na základě kanonických materiálů

Pro vytvoření obsahu máš dvě základní možnosti.
Buď využiješ plán existujícího kanonického kurzu, nebo si nadefinuješ svůj vlastní.
Zde je popsán postup odvozování.

Nejdřív si vyber kanonický kurz, ze kterého chceš svůj kurz odvodit.
Kanonické kurzy najdeš ve složce `courses`.
Vybraný kanonický kurz nastav v souboru `info.yml` klíčem `derives` – napiš do něj název složky kurzu (např. `pyladies` nebo `mi-pyt`).

A teď už zbývá poslední věc, a to je sestavení programu kurzu.
Kurz se skládá z jednotlivých lekcí a každá lekce se skládá z jednotlivých materiálů.
Lekce nadefinuješ klíčem `plan` v souboru `info.yml`.
Ten musí být seznam dalších slovníků.

Máš dvě možnosti, jak nadefinovat jednotlivé lekce.
Buď můžeš převzít lekci z kanonického kurzu, nebo si nadefinovat vlastní.

Nicméně, co je společné, je definování data a času kurzu.
Datum nastavíš klíčem `date`, ve formátu `YYYY-MM-DD`.
Čas nastavovat nemusíš, použije se čas z `default_time`, ale můžeš ho přenastavit pomocí klíče `time`, který bude mít jako hodnotu další slovník s hodnotami `start` a/nebo `end` (ve formátu `HH:MM` obalené uvozovkami).

#### Definice vlastní lekce

Nejdříve si ukážeme, jak se definují vlastní lekce – přebírání pak už bude jednoduché.
Nejdřív si budeš muset zase vymyslet pro lekci identifikátor, který napiš do klíče `slug`.
Identifikátor musí být zase unikántní, nicméně tentorkát jen v rámci kurzu.
Identifikátor lekce bude v adrese na tu specifickou lekci.
Dalším povinným údajem je `title` – název lekce.

Kromě definování data a času už pak při definici lekce zbývá jen seznam materiálů.
Ty se nastavují pomocí klíče `materials`.
I když nechceš žádné materiály pro lekci definovat, musíš klíč nadefinovat, a to s hodnotou `[]` (prázdný seznam).
Základní definice lekce tedy vypadá následovně:

```yaml
plan:
- slug: first-lesson
  title: Název první lekce
  date: 2018-03-07
  materials: []
```

Existují tři druhy materiálů. První druh jsou interní materiály, druhý druh jsou odkazy mimo Nauč se Python a třetí jsou jen záznam bez odkazu.
Materiály se dále pak rozdělují na několik typů, které určují ikonku, která se použije v seznamu materiálů vedle názvu.

Podporované typy jsou následující:

* `page` – výchozí typ pro druh interní materiály
* `url` – výchozí typ pro odkazy
* `cheatsheet` – pro taháky
* `homework` – pro domácí úkoly
* `special` – pro všechno ostatní

A teď už k definování.
Interní materiály se definují pomocí klíče `lesson`, do kterého patří identifikátor interního materiálu.
Interní materiály jsou definovány ve složce `lessons`.
V té složce jsou tzv. kolekce materiálů, které pak obsahují jednotlivé materiály.
Identifikátor materiálu je `<název kolekce>/<název materiálu z kolekce>`, takže například `beginners/install`.
Následovně by se použil materiál v seznamu materiálů:

```yaml
plan:
- slug: first-lesson
  title: Název první lekce
  date: 2018-03-07
  materials:
  - lesson: beginners/install
```

Druhý druh se definuje pomocí klíčů `url` a `title`.
Do `url` patří kompletní odkaz na materiál, do `title` patří název odkazu.
Nepovinně se pak může změnit typ pomocí klíče `type`.
Příklad použítí:

```yaml
plan:
- slug: first-lesson
  title: Název první lekce
  date: 2018-03-07
  materials:
  - title: Úvodní prezentace
    url: https://example.com/uvod.pdf
  - title: Tahák na příkazovou řádku
    url: https://example.com/tahak.pdf
    type: cheatsheet
  - title: Domácí projekty (PDF)
    url: https://example.com/ukol.pdf
    type: homework
```

Třetí druh se definuje stejně jako druhý, jen se do klíče `url` dá hodnota `null`.

Poslední věc, která jde definovat u materiálů, jsou proměné, pomocí klíče `vars`.
Definují se stejně jako u celého kurzu, ale mají účinek jen pro specifický materiál.
Například takhle:

```yaml
plan:
- slug: first-lesson
  title: Název první lekce
  date: 2018-03-07
  materials:
  - lesson: beginners/install
    vars:
      bonus: true
```

#### Převzetí lekce

Lekci převezmeš nastavením klíče `base` na identifikátor (`slug`) lekce z kanonického kurzu (viz soubor `info.yml` ve složce toho kurzu).
Takto převzaná lekce si vezme z kanonického kurzu název i materiály.
Lze to třeba i jen takto:

```yaml
plan:
- base: install
  date: 2018-03-07
- base: hello
  date: 2018-03-14
  time:
    start: '18:00'
    end: '20:00'
```

Nicméně můžeš ale i u převzatých kurzů změnit seznam materiálů, pomocí seznamu hodnot `materials`.
Můžeš si nadefinovat úplně nový seznam materiálů (stejně jako výše) nebo můžeš použít hodnotu `+merge`, které na dané místo v seznamu materiálů vloží všechny materiály z odvozované lekce.
To se hodí, pokud třeba jen potřebuješ přidat něco před nebo za materiály z kanonického kurzu.
Použití vypadá následovně:

```yaml
plan:
- base: install
  date: 2018-03-07
  materials:
  - title: Úvodní prezentace
    url: https://example.com/uvod.pdf
  - +merge
  - title: Domácí projekty (PDF)
    url: https://example.com/ukol.pdf
    type: homework
```

### Úplně nový plán

Pokud chceš vytvořit úplně nový plán, můžeš se řídit stejným postupem jako výše, jen nevyplňuj klíč `derives` a nevyužívej způsob definování přes lekci `base`.

## Otestování vlastního kurzu

Po vytvoření souboru `info.yml` s povinnými položkami se můžeš konečně podívat na to, jak tvůj kurz bude vypadat.
Podle instrukcí z [předchozí části manuálu](../installing-naucse/#launch) si spusť Nauč se v Python režimu `serve`.
Otevři si adresu, kterou ti příkaz napíše, a odnaviguj se do části s kurzy.

Pokud se stránka s kurzy nevykreslí, tak uvidíš Python vyjímku, která ti může pomoct, ale také může být pěkne matoucí.
Nejprve si zkontroluj, jeslti jsi vážně vyplnil{{a}} všechny povinné údaje.
Jestli si myslíš, že ano, tak se nám ozvi přes [issues na našem GitHubu](https://github.com/pyvec/naucse.python.cz/issues) a my ti rádi pomůžeme.
V opačném případě si rozklikni svůj kurz.
Pokud se ti nevykreslí detail kurzu, nejspíš jsi udělal{{a}} nějakou chybu v definici lekcí nebo materiálů – zkontroluj si, jestli například nemáš dvě lekce se stejným identifikátorem, jestli není překlep v nějakém klíčí a jestli například neodkazuješ na materiál, který neexistuje.

Dále si pak můžeš proklikat všechny jednotlivé materiály, jestli vše funguje a vypadá jak má.
Jako další test může posloužit druhý režim spuštění Nauč se Python (`freeze`), který projde všechny stránky, jestli fungují.

## Upravování a vytváření materiálů

Na závěr této části ještě trochu k materiálům.
Jak bylo zmíněno výše, obsah materiálů je definován ve složce `lessons`.
Kromě toho, že si můžeš sestavit vlastní kurz, můžeš si i upravit materiály, které využíváš, nebo si napsat úplně nové.

Většina materiálů je napsaná v formátu [Markdown](https://cs.wikipedia.org/wiki/Markdown) a pár je napsaných v [Jupyter Noteboocích]({{lesson_url("intro/notebook")}}).
Upravování je jednoduché, stačí se podívat do složky s daným specifický materiálem a upravit, co je potřeba, v souboru s obsahem.

Vytváření je trošku složitější v tom, že člověk musí vybrat správnou kolekci a název lekce a pak vytvořit ve složce kromě obsahu i soubor informacích o materiálech.
Soubor se znovu jmenuje `info.yml` a má povinné tři údaje, `title`, `style` a `license`:

- `title` nastavuje název,
- `style` může být `md` nebo `ipynb` podle toho, jaký formát bude mít text,
- `license` nastavuje licenci, pod kterou materiály píšeš – identifikátor ze složky `licenses`: doporučujeme použít `cc-by-sa-40`.

Dále má soubor nepovinné položky, první `attributions` – buď jednoduchý text, nebo seznam textů s informacemi o tom, kdo a proč materiál napsal.
Nakonec lze použít jinou licenci na ukázky kódu pomocí `license_code`: doporučujeme použít `cc0`.

> [note]
> Obecně je dobrý nápad se při psaní materiálů inspirovat již existujícími řešeními v ostatních materiálech a přebírat jejich styl a způsoby formátování.
