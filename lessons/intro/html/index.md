# Úvod do HTML
Co je to HTML? Je to anglická zkratka slov **Hypertex Markup Language**, což ve volném překladu znamená
Hypertextový značkovací jazyk. Již z názvu vyplývá, že HTML není programovacím jazykem.
 A co to je vlastně značkovací jazyk? Značkovací jazyk přidává dodatečné informace o prostém textu a jeho formátu.
 Například, když chceme zobrazit **tučný text** nebo *kurzívu*, tak použijeme značky (tagy).
 
 A kde se to HTML používá? Každá internetová stránka je tak napsaná. Zde pozor, dnes již nejsou internetové stránky
  napsané jen v čistém HTML, to bychom se museli vrátit do webového pravěku 90. let.
   Dnes jsou webové stránky tvořené tzv. svatou trojicí: **HTML, CSS a JavaScript**.
    O&nbsp;HTML jsme si už něco pověděli, to tvoří kostru stránky.
    
CSS znamená **Cascading Style Sheets** v překladu *kaskádové styly*, které se starají o to jak stránka bude vypadat
 po grafické stránce.
 
 A co ten JavaScript? JavaScript je další programovací jazyk.
  Možná se zeptáte proč se musím učit JavaScript, když už umím Python.
   Důvody a přesnou historii vám nepovím, ale faktem je, že webové prohlížeče podporují
    z historických důvodů právě JavaScript. JavaScript umožňuje, aby byl web živý. Efekt promáčknutého tlačítka,
     animace, funkce **drag and drop** (tahni a pusť) a další vymoženosti moderního webu.
     
 No a teď hurá na základy HTML.
 
 ##HTML
 Soubor s příponou *.html je obyčejný textový soubor. Otevři si svůj textový editor a do něho napiš:
 
 ```HTML
    Ahoj světe!
```

 Soubor ulož jako **název.html** a otevři ho ve svém prohlížeči. Prohlížeč zobrazí, to co jsi napsala.
  Gratuluji, napsala jsi svou první webovou stránku. Že takto stránky nevypadají? Hm...pravda,
   abysme mohli psát stránky jako seznam.cz, tak musíme přidat více znalosti. Jdeme na to?
 
 ##Tagy - značky
 Na začátku jsem zmínil, že HTML je značkovací jazyk. Tak kde jsou ty značky.
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
  HTML značky (tagy) se zapisují mezi znaménka větší/menší **&lt;tag&gt;** 
  a většina značek (tagů) musí být ukončena **&lt;/tag&gt;**, tak že za znamenéko větší než přidáme **lomeno /**.
  Existují html značky, které nejsou párové a nemusí být ukončený např.: **&lt;br&gt;**, **&lt;a&gt;** atd.
  Obsah webové stránky se píše mezi tagy **&lt;body&gt;** a **&lt;/body&gt;**
  
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
 Jak jsme si před chvilkou řekli, obsah stránky se píše do oblasti **&lt;body&gt;**,
  kam se zapisuje vše, co by mělo být vidět. Nicméně webová stránka může obsahovat
   i další potřebné informace např. odkaz na CSS styly, odkaz na JavaScript, název stránky nebo logo,
    které se zobrazuje v panelu. Všechny tyto informace se píší mezi tagy **&lt;head&gt;** a **&lt;/head&gt;**.
    My si ukážeme, jak pojmenovat naší stránku. K tomu slouží tag **&lt;title&gt;**:
    
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
Základem jakéhokoliv textu je odstavec. Odstavec se zapisuje mezi značky **&lt;p&gt;** a **&lt;/p&gt;**.
 Písmeno P pochází z anglického **Paragraph**. Pojďme si do naší stránky přidat nějaký ten odstavec.
 
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
     magna gravida vehicula. Fusce consectetuer risus a nunc. Class aptent taciti sociosqu ad litora torquent per
     conubia nostra, per inceptos hymenaeos. Etiam sapien elit, consequat eget, tristique non, venenatis quis, ante.
     Morbi imperdiet, mauris ac auctor dictum, nisl ligula egestas nulla, et sollicitudin sem purus in lacus.
     Aliquam ornare wisi eu metus. Nulla turpis magna, cursus sit amet, suscipit a, interdum id, felis.
     Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aliquam erat volutpat. Donec ipsum massa, ullamcorper in,
     auctor et, scelerisque sed, est. Aliquam in lorem sit amet leo accumsan lacinia. Curabitur ligula sapien,
     pulvinar a vestibulum quis, facilisis vel sapien. In convallis. Donec vitae arcu.
    </p>
</body>
</html>
```
 
 A co ta latina, co je to za blbost? Inu, nějakého líného programátora nebavilo vymýšlet nějaké umělé texty,
  když potřeboval otestovat chování své webové stránka,
   a tak napsal generátor náhodných latinských slov. A vzniklo **Lorem ipsum**. Zkus toto slovní spojení vygooglit :-)
   
Pro psaní odstavců se hodí zmínit další značky:
* **&lt;strong&gt;** **&lt;/strong&gt;**: zvýrazní text **tučně**
* **&lt;em&gt;** **&lt;/em&gt;**: zvýrazní text _kurzívou_

> [warning] Pozor!
> Některé prohlížeče toto pravidlo nerespektují a mohou tyto tagy zobrazovat rozdílně!

* **&lt;br&gt;**: vloží prázdný řádek

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
HTML umožňuje sedm úrovní nadpisů. Největší úroveň nadpisu je **&lt;h1&gt;** **&lt;/h1&gt;** 
a nejnižší **&lt;h7&gt;** **&lt;/h7&gt;**. Vyzkoušej si to.

> [warning] Pozor!
>Možná se ti zdá nadpis h1 moc velký. To nevadí. Pamatuj HTML neřeší grafickou stránku.
> Vždy bys měla dodržet pořadí h1, h2, h3 atd. Grafickou stránku vyřešíš pomocí CSS.

##Seznamy
Seznamy? To už jsem někde viděla? **Pozor** zde se jedná o číslované seznamy nebo odrážky, tak jak znáš z textových
 editorů. Prosím nepleť si s Pythonem.
 Existují dva nejpouživanější seznamy: číslovaný a nečíslovaný (odrážky).
 
 * Číslovaný seznam **&lt;ol&gt;** **&lt;/ol&gt;** (ordered list):
 
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

 * Odrážkový seznam **&lt;ul&gt;** **&lt;/ul&gt;** (unordered list):
 
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

Všimni si, že jednotlivá položka seznamu se v obou případech značí **&lt;li&gt;** **&lt;/li&gt;**.

##Odkazy
Co by to bylo za webové stránky, kdyby neobsahovaly odkazy? Odkaz může směřovat na jinou webovou stránku, a nebo na
 stejnou stránku na určité místo.
 
 * Odkaz na webovou stránku **&lt;a href="https://naucse.python.cz"&gt;** odkaz **&lt;/a&gt;**
 * Odkaz na umístění v té samé stránce **&lt;a href="#id"&gt;** odkaz **&lt;/a&gt;**
 
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

Všimni si, že jsme nadpisu **h1** přidali atribut **id="nadpis"**, čím jsme ho jednoznačně identifikovali a můžeme na
 něj
 v dalším textu odkazovat.