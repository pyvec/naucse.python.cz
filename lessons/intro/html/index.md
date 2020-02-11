# Úvod do HTML
Co je to HTML? Je to anglická zkratka slov **Hypertex Markup Language**, což ve volném překladu znamená
Hypertextový značkovací jazyk. Již z názvu vyplývá, že HTML není programovacím jazykem.
 A co to je vlastně značkovací jazyk? Značkovací jazyk přidává dodatečné informace o prostém textu a&nbsp;jeho formátu.
 Například, když chceme zobrazit **tučný text** nebo *kurzívu*, tak použijeme značky (tagy).
 
 A kde se to HTML používá? Každá internetová stránka je tak napsaná. Zde pozor, dnes již nejsou internetové stránky
  napsané jen v čistém HTML, to bychom se museli vrátit do webového pravěku 90. let.
   Dnes jsou webové stránky tvořené tzv. svatou trojicí: **HTML, CSS a&nbsp;JavaScript**.
    O&nbsp;HTML jsme si už něco pověděli, to tvoří kostru stránky.
    
CSS znamená **Cascading Style Sheets** v překladu *kaskádové styly*, které se starají o to jak stránka bude vypadat
 po grafické stránce.
 
 A co ten JavaScript? JavaScript je další programovací jazyk.
  Možná se zeptáš proč se musím učit JavaScript, když už umím Python.
   Důvody a&nbsp;přesnou historii vám nepovím, ale faktem je, že webové prohlížeče podporují
    z historických důvodů právě JavaScript. JavaScript umožňuje, aby byl web živý. Efekt promáčknutého tlačítka,
     animace, funkce **drag and drop** (tahni a&nbsp;pusť) a&nbsp;další vymoženosti moderního webu.
     
 Konec nudné teorie, jdeme psát weby!!!
 
 ##HTML
 Soubor s příponou ***.html** je obyčejný textový soubor. Otevři si svůj textový editor a&nbsp;do něho napiš:
 
 ```HTML
    Ahoj světe!
```

 Soubor ulož jako `moje_stranka.html` a&nbsp;otevři ho ve svém prohlížeči. Prohlížeč zobrazí, to co jsi napsala.
  Gratuluji, napsala jsi svou první webovou stránku. Že takto stránky nevypadají? Hm...pravda,
   abysme mohli psát stránky jako **[naucse.python.cz](https://naucse.python.cz/)** nebo snad
    **[facebook.com](https://facebook.com/])**, tak musíme přidat více znalosti. Jdeme na to!?
 
 ##Tagy - značky
 Na začátku jsem zmínil, že HTML je značkovací jazyk. Tak kde jsou ty značky?
  Takže obyčejná HTML "ahoj světe stránka" by vypadala asi nějak takto:
  
```HTML
   <!DOCTYPE html>
    <html>
    <body>
        <h1>Ahoj světe</h1>
    </body>
    </html>
```
 
 Takto vypadá webová stránka s minimální strukturou.
  HTML značky (tagy) se zapisují mezi znaménka větší/menší `tag` 
  a&nbsp;většina značek (tagů) musí být ukončena `</tag>`, tak že za znamenéko větší než přidáme **lomeno /**.
  Existují html značky, které nejsou párové a&nbsp;nemusí být ukončený např.: `<br>`, `<a>` atd.
  Obsah webové stránky se píše mezi tagy `<body>` a&nbsp;`</body>`
  
 ##Atributy
 Aby toho nebylo málo, tak každá značka může obsahovat atributy, které význam značky nějakým způsobem modifikují.
  Nejčastěji se setkáme s hypertextovým odkazem:
  
  ```HTML
   <!DOCTYPE html>
    <html>
    <body>
        <h1>Ahoj světe</h1>
        <a href="naucse.python.cz">Nauč se python</a>
    </body>
    </html>
```

Slovo **href** je v tomto případě atribut , který odkazuje na URL adresu.
 Href je anglická zkratka **HyperText Reference**.
 
 ##Hlavička - title
 Jak jsme si před chvilkou řekli, obsah stránky se píše do oblasti **`<body>`**,
  kam se zapisuje vše, co by mělo být vidět. Nicméně webová stránka může obsahovat
   i&nbsp;další potřebné informace např. odkaz na CSS styly, odkaz na JavaScript, název stránky nebo logo,
    které se zobrazuje v panelu. Všechny tyto informace se píší mezi tagy **`<head>`** a&nbsp;**`</head>`**.
    My si ukážeme, jak pojmenovat naší stránku. K tomu slouží tag **`<title>`**:
    
```HTML
<!DOCTYPE html>
<html>
<head>
    <title>Moje první stránka</title>
</head>
<body>
    <h1>Ahoj světe</h1>
    <a href="naucse.python.cz">Nauč se python</a>
</body>
</html>
```

##Odstavec
Základem jakéhokoliv textu je odstavec. Odstavec se zapisuje mezi značky `<p>` a&nbsp;`</p>`.
 Písmeno P pochází z anglického **Paragraph**. Pojďme si do naší stránky přidat odstavec.
 
 ```HTML
<!DOCTYPE html>
<html>
<head>
    <title>Moje první stránka</title>
</head>
<body>
    <h1>Ahoj světe</h1>
    <a href="naucse.python.cz">Nauč se python</a>
    <p>
     Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aliquam ante. Quisque tincidunt scelerisque libero.
     Nulla turpis magna, cursus sit amet, suscipit a, interdum id, felis. Nullam sit amet magna in
     magna gravida vehicula. Fusce consectetuer risus a&nbsp;nunc. Class aptent taciti sociosqu ad litora torquent per
     conubia nostra, per inceptos hymenaeos. Etiam sapien elit, consequat eget, tristique non, venenatis quis, ante.
     Morbi imperdiet, mauris ac auctor dictum, nisl ligula egestas nulla, et sollicitudin sem purus in lacus.
     Aliquam ornare wisi eu metus. Nulla turpis magna, cursus sit amet, suscipit a, interdum id, felis.
     Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aliquam erat volutpat. Donec ipsum massa, ullamcorper in,
     auctor et, scelerisque sed, est. Aliquam in lorem sit amet leo accumsan lacinia. Curabitur ligula sapien,
     pulvinar a&nbsp;vestibulum quis, facilisis vel sapien. In convallis. Donec vitae arcu.
    </p>
</body>
</html>
```
 
 A co ta latina, co je to za blbost? Inu, nějakého líného programátora nebavilo vymýšlet umělé texty,
  když potřeboval otestovat chování své webové stránka,
   a&nbsp;tak napsal generátor náhodných latinských slov. A vzniklo **Lorem ipsum**. Zkus toto slovní spojení vygooglit :-)
   
Pro psaní odstavců se hodí zmínit další značky:
* `<storng> </strong>`**: zvýrazní text **tučně**
* `<em> </em>`: zvýrazní text _kurzívou_

> [warning] Pozor!
> Některé prohlížeče toto pravidlo nerespektují a&nbsp;mohou tyto tagy zobrazovat rozdílně!

* `<br>`: vloží prázdný řádek

A teď si to všechno vyzkoušíme:

 ```HTML
<!DOCTYPE html>
<html>
    <head>
        <title>Moje první stránka</title>
    </head>
    <body>
        <h1>Ahoj světe</h1>
        <a href="naucse.python.cz">Nauč se python</a>
        <p>
            <strong>Tučný text</strong>
            <em>Text kurzívou</em>
            <br>
        </p>
    </body>
</html>
```

##Nadpisy
HTML umožňuje sedm úrovní nadpisů. Největší úroveň nadpisu je **`<h1>`** **`</h1>`** 
a nejnižší **`<h7>`** **`</h7>`**. Vyzkoušej si to.

> [warning] Pozor!
>Možná se ti zdá nadpis h1 moc velký. To nevadí. Pamatuj HTML neřeší grafickou stránku.
> Vždy bys měla dodržet pořadí h1, h2, h3 atd. Grafickou stránku vyřešíš pomocí CSS.

##Seznamy
Seznamy? To už jsem někde viděla? **Pozor** zde se jedná o číslované seznamy nebo odrážky, tak jak je znáš z textových
 editorů. Prosím nepleť si s Pythonem.
 Existují dva nejpouživanější seznamy: číslovaný a&nbsp;nečíslovaný (odrážky).
 
 * Číslovaný seznam **`<ol>`**&nbsp;**`</ol>`** (ordered list):
 
  ```HTML
<!DOCTYPE html>
<html>
    <head>
        <title>Moje první stránka</title>
    </head>
    <body>
        <ol>
            <li>Položka 1</li>
            <li>Položka 2</li>
        </ol>
    </body>
</html>
```

 * Odrážkový seznam **`<ul>`** **`</ul>`** (unordered list):
 
  ```HTML
<!DOCTYPE html>
<html>
    <head>
        <title>Moje první stránka</title>
    </head>
    <body>
        <ul>
            <li>Položka 1</li>
            <li>Položka 2</li>
        </ul>
    </body>
</html>
```

Všimni si, že jednotlivá položka seznamu se v obou případech značí **`<li>`** **`</li>`**.

##Odkazy
Co by to bylo za webové stránky, kdyby neobsahovaly odkazy? Odkaz může směřovat na jinou webovou stránku, a&nbsp;nebo na
 stejnou stránku na určité místo.
 
 * Odkaz na webovou stránku **`<a href="https://naucse.python.cz" >` odkaz `</a>`**
 * Odkaz na umístění v té samé stránce **`<a href="#id">`** odkaz **`</a>`**
 
```HTML
<!DOCTYPE html>
<html>
<head>
    <title>Moje první stránka</title>
</head>
<body>
    <h1 id="nadpis">Nadpis 1</h1>
    <a href="https://naucse.python.cz">Externí odkaz na Nauč se</a>
    <a href="#nadpis">Odkaz na nadpis uvnitř tohoto HTML</a>
</body>
</html>
```

Všimni si, že jsme nadpisu **h1** přidali atribut **id="nadpis"**, čím jsme ho jednoznačně identifikovali a&nbsp;můžeme na
 něj
 v dalším textu odkazovat.
 
 ##Obrázky
 Co by to bylo za web kdybychom nemohli přidávat multimédia, na a&nbsp;nejběžnějším multimediem na webu je obrázek. Značka
  pro přidání obrázku vypadá nějak takto:
  
 ```HTML
<img src="https://www.python.org/static/community_logos/python-logo-master-v3-TM.png" width="120" height="90" alt
="Python logo">
```

Všimni si, že tag **`<img>`** je nepárový a&nbsp;nemusíme ho nijak ukončovat. Stejně jako u&nbsp;hypertextového odkazu mus
íme přidat atribut, který nám udává umístění obrázku. Atribut odkazující na umístění se nazývá **src** z anglického
 source. Dále je dobrou praxí udávat atribut **alt**, který zobrazí textový popisek obrázku pokud se ho nepodaří 
 z nějákého důvodu načíst a&nbsp;nejen to. Nevidomým lidem pomáhají tyto popisky s orientací na stránce. Atribut
  **width** udává šířku obrázku a&nbsp;atribut **height** výšku.
  
> [note]
> **Velikost obrázku**  
> S velikostí obrázků to není vždy jednoduché. Musíte zachovat poměr stran, aby nebyly zdeformované. Velikost okna
> webové stránky se nustále mění. Takže webový vývojář musí řešit dynamickou změnu velikosti obrázku podle velikosti
> okna, tak aby vizuální styl byl stále konzistetní.

##Tabulky
Tabulky byly a&nbsp;stále jsou často zneužíváné k tvorbě rozvržení stránky. Na to tabulky nejsou vhodné a&nbsp;prosím
 vyvaruj
 se toho. Tabulky mají stejný účel jako v textových procesorech, zobrazovat přehledně data a&nbsp;k tomu jsou určeny a&nbsp;k
  ničemu jinému. Samozřejmě tabulky mohou vypadat různě, ale to je záležitost kaskádových stylů (CSS). Ukázka
   tabulky:
   
 ```html
<table>
    <tr>
        <th>Sloupec 1 - nadpis</th>
        <th>Sloupec 2 - nadpis</th>
        <th>Sloupec 3 - nadpis</th>
    </tr>
    <tr>
        <td>Řádek 1, Buňka 1</td>
        <td>Řádek 1, Buňka 2</td>
        <td>Řádek 1, Buňka 3</td>
    </tr>
    <tr>
        <td>Řádek 2, Buňka 1</td>
        <td>Řádek 2, Buňka 2</td>
        <td>Řádek 2, Buňka 3</td>
    </tr>
    <tr>
        <td>Řádek 3, Buňka 1</td>
        <td>Řádek 3, Buňka 2</td>
        <td>Řádek 3, Buňka 3</td>
    </tr>
    <tr>
        <td>Řádek 4, Buňka 1</td>
        <td>Řádek 4, Buňka 2</td>
        <td>Řádek 4, Buňka 3</td>
    </tr>
</table>
```

Nyní si rozklíčujeme použité tagy:
* **`<table>` `<\table>`**: je jen "obal", který vytváří tabulku, ale zatím bez dat
* **`<th>` `<\th>`**: vychází ze slov table heading (nadpis tabulky)
* **`<tr>` `<\tr>`**: vychází ze slov table row (řádek tabulky)
* **`<td>` `<\td>`**: vychází ze slov table data (data tabulky) a&nbsp;definuje jednu buňku v řádku, mezi tento
 tag se zapisují konečná data.
 
##Formuláře
Zde začíná konečně zábava, alespoň pro nás programátory. Ptáte se proč? Přes
 formuláře komunikujeme s našimi uživateli a&nbsp;formuláře jsou prostředek naší komunikace přes které nám uživatele
  poskytují data. Nicméně HTML tyto infromace umí sbírat, ale už je neumí zpracovávat. To je už úkol programovacího
   jazky v našem případu **Pythonu**. Vše si vysvětlíme na příkladu:
 ```html
    <form action="" method="post">
        <p>Jméno:</p>
        <p><input name="name" value="Tvoje jméno"></p>
        
        <label for="fname">Křestní jméno: </label><input type="text" id="fname" name="fname"><br><br>
        <label for="lname">Přijmení: </label><input type="text" id="lname" name="lname"><br><br>

        <p>Komentář: </p>
        <p><textarea rows="10" cols="20" name="comments">Tvůj komentář</textarea></p>

        <p>Tvoje pohlaví:</p>
        <p><input type="radio" name="sex" value="female"> žena</p>
        <p><input type="radio" name="sex" value="male"> muž</p>

        <select name="language">
            <option>Python</option>
            <option>JavaScript</option>
            <option value="third option">C</option>
        </select>

        <p><input type="submit" value="odeslat"></p>
    </form>
```
Zdá se ti to jako zmatek? Zkus kód vložit do editoru a&nbsp;pusť si ho v prohlížeči. Pojďme si vysvětlit jednotlivé tagy:
* `<form action="" method="post"> </form>`: Tento tag definuje celý formulář a&nbsp;veškeré další tagy, které souvisí s
 daným formulářem by měly být uvnitř tohoto tagu. Všimtěte si atributů **action** a&nbsp;**method**.
 * **action**: Zde se zapisuje url adresa, kam se mají odeslat data z formuláře. Ve Flasku je běžné, že adresa je
  prázdný řetězec, což znamená, že se data z formuláře pošlou na stejnou url adresu, kde zrovna jsme.
   Více si ukážeme v lekci o [Flasku](https://naucse.python.cz/2020/praha-jaro-knihovny/intro/flask/).
 * **method**: Určuje HTTP metodu odeslání dat. Pro formuláře existují metody GET a&nbsp;POST.
 
 
* `<input>`: Tag pro vstupní informace. V ukázkové kódu si můžeš všimnout, že tag není samostatně, ale obsahuje 
    další atributy, také je tag nepárový a&nbsp;veškeré informace se vkládají přes atributy. Pojďme se podívat na některé atributy:
    * **name**: Definuje jméno elementu, představ si ho jako proměnnou v Pythonu, protože u&nbsp;formulářu se na pozadí 
    prohlížeče ukládají data z elementu právě pod jménem.
    * **type**: Definuje typ vstupu. Implicitně je type nastaven na text. Což je klasické textové políčko. Další
     bežné možnosti jsou: (`password`, `checkbox`, `radio` a&nbsp;`submit`). Zkus si teď chvilku hrát v textovém editoru s
      typy a&nbsp;zobrazovat si je v prohlížeči.
    * **id**:  Jedná se o textový identifikátor, na který můžeme odkazovat pomocí tagu `<a>`, a&nbsp;také můžeme k
     jednotlivým
     `<input>` vkládat popisek pomocí tagů `<label>`.
    * **value**: U klikacích možností (např.: **radio** nebo **checkbox** typů) musíme připsat tento atribut, který nám určí
    jaká hodnota se uloží, když zaškrtneme tuto možnost.
    
  
* `<label> </label>`: Tag, který definuje popisek k nějakému vstupu (`<input>`). Metoda má jen dva atributy:
    * **for**: Label lze spárovat s input pokud zadáme do **for** id tagu `<input>`.
    * **form**: Definuje, ke kterému formuláři popisek (`<lable>`) patří.


* `<textarea> </textarea>`: Tag, který se hodí pro zadávání dlouhých textů. Může mít již známe atributy (name, form
a id) a&nbsp;navíc je potřeba udat velikost pole pomocí řádků a&nbsp;sloupců resp. (**rows** a&nbsp;**cols**).


* `<select> </select>`: Definuje rolovací seznam. Neměli bychom zapomenout na atribut **name**.


* `<option> </option>`: Definuje možnosti rolovacího seznamu, a&nbsp;proto má vždy nadřazený tag `<select>`.
 Tag má "povinný" atribut **value**, kterým přiřadíme hodnotu k dané možnosti, která se odešle ke zpracování.
 
 
 Uff, je to za námi. HTML samozřejmě obsahuje spoustu zákoutí a&nbsp;podivností, ale při běžné každodenní práci jsou
  formuláře nejkomplexnější oblast. Neukázali jsem si všechno, ale teď už víš jak to asi funguje.
  
  
> [note]
> Zdá se ti HTML moc "ukecané" a&nbsp;chtěla bys ho psát jako Python?
> Par chytrých hlav se dalo dohromady a&nbsp;vymyslelo **pudla** resp. **Pug** (v překladu pudl). Pug odstraňuje
> párové tagy a&nbsp;kód se strukturuje pomocí odsazení jako python. Dále odpadly známenka `<>`, tagy se píšou bez nich a
> atributy se píši do závorky. Více na https://pugjs.org/.
