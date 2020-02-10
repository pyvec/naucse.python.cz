# Úvod do CSS
V přechozí lekci jste si zkusily navrhnout webovou stránku jen pomocí HTML a asi jste zjistily, že taková stránka
 vypadá dosti nevábně. Asi jako nevybarvené omalovánky. Ve světě webových stránek jsou právě Kaskádové styly (**CSS**)
  naše pastelky (**barvičky**).
  
  Špatnou zprávou je, že syntaxe **CSS** je rozdílná od HTML, takže si budeš muset v mozku vyčlenit další místo. Dobrou
   zprávou je, že i **CSS** jde psát jako Python (Pythonic way), ale více až na konci lekci.
    Teď se musíme naučit čísté **CSS**.
    
  Pro zopakování **CSS** znamená **Cascading Styles Sheets** (v češtině: Kaskádové styly).
  
 ## Aplikace CSS stylů
  Máte napsanou HTML stránku a teď si asi říkáte, musím to celé přepisovat, když chci mít růžové pozadí a žluté písmo?
  Opověď zní, ano můžu, ale naštěstí nemusím. Existují tři způsoby jak dodat HTML stránce grafický styl:
  
  1. **Inline**: CSS styly jsou vložené přímo v HTML tagu zadané pomocí atributu **style**.
    
    ```html
    <p style="color: red">text</p>
    ```
  Tímto zápisem říkáme, že celý text v odstavci má mít červenou barvu.

  2. **Interní CSS**: CSS styly jsou vkládáne pomocí tagu `<style> </style>` do hlavičky dokumentu `<head> </head>`:
  
    ```html
    <!DOCTYPE html>
        <html>
            <head>
                <title>CSS Example</title>
                <style>
                
                p {
                    color: red;
                }
                
                a {
                    color: orange;
                }
                
                </style>
            </head>
            <body>
                <p>Ahoj pyladies!<p>
                <a href="https://naucse.python.cz/">Oranžový odkaz na nauč se</a>
            </body>
        </html>
    ```
  3. **Externí CSS**: Poslední možností je uložit CSS jako externí soubor (přípona *.css). Vytvoř si soubor `styl.css`
   a ulož ho do stejné složky, kde máš html soubor. Do souboru vlož jen vnitřek z předchozího příkladu:
   
   `styl.css`:
   
   ```css
    p {
        color: red;
    }
    
    a {
        color: orange;
    }
  ```
 
   Nyní svému HTML musíš říct, kde má hledat soubory se stylem.:
   
   `moje_stranka.html`:
       
   ```html
    <!DOCTYPE html>
    <html lang="html">
        <head>
            <title>CSS Example</title>
            <link rel="stylesheet" href="style.css">
        </head>
        <body>
            <p>Ahoj pyladies!<p>
            <a href="https://naucse.python.cz/">Oranžový odkaz na nauč se</a>
        </body>
    </html>
   ```

   Odkaz na CSS obstaral tag `<link>`, který má dva atributy. Atribut **rel** udává vztah (relationship) mezi
   současným HTML a odkazovaným dokumentem. Hodnotou _stylesheet_ říkáme, že má očekávat **css** soubor.
    Atribut **href** (hypertext reference) odkazuje na umístění souboru, které může být relativní i absolutní. 

> [warning] Pozor!
> Je dobrou praxí style do HTML nezadávat, tak abychom oddělili struktru dokumentu **HTML** od jeho stylu **CSS**.
> Inline CSS používáme jen v případě pokud je důležité, aby byl text červený v každé šabloně.

## Syntaxe CSS
Ve zkratce se syntaxe skládá ze **selektorů**, **vlastností** a **hodnot**. Výhodou je, že už známe Python, takže si
 můžeme pomoci jeho syntaxí. Představte si, že selektor je **slovník**, **vlastnost** je klíč a hodnota je **hodnota**.
 Definicí slovníku známe, ale co s tím, co kam ukládat? Vysvětlíme si to postupně na příkladu:
 
 ```css
body {
    font-size: 14px;
    color: deeppink;
}
```

* **selektor**: Určuje, na který tag chceme aplikovat styl a můžeme si ho představit jako jméno proměnné slovníku. V 
příkladu je to tag **body**. 

* **vlastnost (property)**: Jak už název napovídá, říká nám kterou vlastnost daného tagu chceme měnit. V příkladu m
áme vlastnosti dvě **font-size (velikost písma)** a **color (barvu písma)**. Když zůstaneme u Pythonu, tak můžeme
 vlastnost připodobnit ke klíči slovníku.
 
* **hodnota (value)**: Hodnota je hodnota vlastnosti, je to trochu definice kruhem, ale snad je to zřejmé. Hodnotu
 stejně jako v Pythonu píšeme za dvojtečku.
 
> [warning] Pozor!
> Neberte příklad s Pythonem doslova, jednolivé páry vlastnost:hodnota se v CSS oddělují středníkem a středník musí
> být i za poslední dvojicí. Stejně tak selektor se nepřiřazuje k "slovníku" znaménkem rovná se, ale jen mezerou.


### Jednotky délky
Možná sis v předchozím příkladu všimla podivné jednoty u font-size **px**. *px* je jednotka pixelu. Co je to pixel?
Je to bod na tvé obrazovce, který může mít v jeden okamžik jen jednu barvu. Možná si vzpomínáš na pravěk počítačů,
 kdy obrázky vypadaly nějak takto:
{{ figure(
    img=static('heart.png'),
    alt='obrázek srdce'
) }} 

Na srdíčku jsou vidět jednotlivé čtverečky. A jeden ten čtvereček je pixel. S dnešním _Ultra HD_ rozlišením už
 jednotlivé pixely(čtverečky) neuvidíš. 

A jaké jednotky délky můžeš používat? V CSS se dělí na absolutní a relativní. Pojdmě si napsat seznam:

* **absolutní**:
    * **cm**: centimetr
    * **mm**: milimetr
    * **in**: palec (1in = 96px = 2.54cm)
    * **px**: pixel (1px = 1/96 palce)
    * **pt**: bod (1pt = 1/72 palce)
    * **pc**: picas (1pc = 12 pt)
    
    
* **relativní**:
    * **em**: násobek velikosti písma
    * **ex**: násobek velikosti písma na x-ové souřadnici (zřídka používané)
    * **ch**: násobek šířky znako 0 (nula)
    * **rem**: násobek velikosti písma kořenového tagu (elementu)
    * **vw**: procentní bod šířky okna prohlížeče
    * **vh**: procentní bod výšky okna prohlížeče
    * **vmin**: procentní bod menšího rozměru z okna prohlížeče
    * **vmax**: procentní bod většího rozměru z okna prohlížeče
    * **%**: procentní bod velikosti nadřazeného elementu (tagu)
    
## Barvy
Včelí medvídci ze známého večerníčku chtěli natírat svět nabílo (viz poznámka). Natírat svět jenom na bílo je nuda.
 CSS poskytuje 16&nbsp;777&nbsp;216 různých barev. A jak barvy zadávat, když jich je tolik?

> [note]
> Nás by tak nejvíce vábilo,
> natírat celý svět na bílo.
> Motýla i jeho larvu,
> milujeme bílou barvu. Bílá, bílá, bílá, bílá,
> komu by se nelíbila.
> Bílá vrána, bílá noc,
> bílé není nikdy moc."Čmeláci vy jste snad šílení,
> okamžitě nechte bílení."
>-- Zdeněk Svěrák
 
Nemusíš se bát, že bys musela znát názvy všech barev. Pokud znáš anglický název barvy můžeš ho zkusit a pro ty jiné
barvy tu jsou číselné zápisy. Jak jinak, programátoři mají čísla rádi. Způsoby zadávání barev:

1. **Slovně**: Barvu musíš zadávat anglickým názvem. Současné prohlížeče podporují
 [140 názvů barev](https://www.w3schools.com/colors/colors_names.asp).

1. **RGB**:   RGB znamená Red - Green - Blue. To, že se dá každá barva složit kombinací červené, modré a zelené barvy
 si už asi někde slyšela. Podivej se ukázku a hned si řekneme více:
     ```css
        p {
            color:rgb(255,255,255);
        }
        
        h1 {
            color: rgb(100%,100%,100%);
        }
    ```
  V našem příkladu jsme zadali, že všechny odstavce (**p**) budou mít bílou barvu a stejně tak všechny nadpisy
   (**h1**) budou mít také bílou barvu. Obsah každé složky barvy můžeme vkládat pomocí procent, to je asi z příkladu
    zřejmé a pochopitelné. Ale co je za číslo **255**?
    
  Teď zase zpátky k matematice. Počítače pracují na principu **nul** a **jedniček**. Ano, týká se to i webových 
  stránek. Pradávné počítače pracovali s osmibitovými procesory, což zjednodušeně znamená, že má 8 drátků, kam můžeme
   pouštět proud. Na každém drátku proud běží(1)/neběží(0). Tímto způsobem procesor umí pracovat s `2*2*2*2*2*2*2*2
    = 2^8 = 256` hodnotami. Historicky se ustanovilo, že **8 bitů** bude jeden **bajt**. A obřím skokem, počítačoví 
    inženýři prominou, se dostáváme k rgb.
     
 Matematiky a počítačové inženýry jsme odbyli, ale malíř by namítnul, že když smíchá **červenou**, **zelenou**
  a **modrou** ve stejněm poměru, tak dostane **černou**. Jak to, že jsme dostali bílou? Důvod je takový, že my nemích
  áme vodovky, ale světelné paprsky, které vytvářejí pixel. Takže když smícháš **červené**, **zelené** a **modré** 
  světlo dostaneš světlo...**bílé**. 
  
2. **Hexadecimální zápis**: Zdál se ti předchozí výklad o rgb, bitech a bajtech složitý. Jsi ráda, že už trošku
 chápeš dvojkovou soustavu, tak věř, že to není všechno. Proč používat dvojkovou soustavu, když můžeme používat
  soustavu šestnáctkovou (hexadecimální). Proč by to někdo dělal? Programátoři jsou líní, to je často odpověd na
   takové otázky. 