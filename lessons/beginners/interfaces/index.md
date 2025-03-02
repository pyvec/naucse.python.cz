# Rozhraní

Už víš že funkce ti umožňují kousek kódu:

* použít (zavolat) na více místech v programu, i když definice je jen jedna,
* vyčlenit, aby detail (jako načtení čísla od uživatele) „nezavazel“ ve větším 
  programu, který tak může být přehlednější, a
* pojmenovat, aby bylo jasné co kód dělá i bez toho, abys musel{{a}} číst
  samotné tělo funkce.

Další výhoda funkce je, že ji můžeš jednoduše vyměnit za jinou,
lepší funkci – pokud má ta lepší funkce stejné *rozhraní* (angl. *interface*).

Aby se ti líp představovalo, o čem budeme povídat, představ si elektrickou
zásuvku ve zdi.
Do takové zásuvky můžeš zapojit počítač, lampu, nabíječku na mobil, vysavač,
nebo rádio.
Zásuvka poskytuje elektrický proud; je jedno, jak ho použiješ.
Stejně tak je jedno jestli je „druhý konec“ zásuvky připojený k solárnímu
panelu nebo k atomové elektrárně.
Zásuvka poskytuje elektrický proud, a jsou u ní důležité určité parametry
(tvar, napětí, frekvence, maximální proud) na kterých se obě strany,
poskytovatel proudu i spotřebič, shodly.


# Funkce jako rozhraní

Podívej se na tuhle hlavičku funkce.
Víš z ní, co ta funkce dělá a jak ji použít?

```python
def ano_nebo_ne(otazka):
    """Zeptá se uživatele na otázku a vrátí True nebo False dle odpovědi"""
```

Podobnou funkci už jsi napsala; víš že „vevnitř“ volá `input` a ptá se na
příkazové řádce.

Co kdybys ale měla následující funkci?

```python
def ano_nebo_ne(otazka):
    """Ukáže tlačítka "Ano" a "Ne" a až uživatel jedno zmáčkne, vrátí True
    nebo False dle stisknutého tlačítka."""
```

<img src="{{ static('yn.png') }}" alt="Screenshot s tlačítky Ano a Ne" style="display:block;float:right;">

Když zavoláš tuhle funkci, `ano_nebo_ne('Chutná ti čokoláda?')`, ukáže se
okýnko se dvěma tlačítky.
Když uživatel jedno zmáčkne, funkce vrátí True nebo False.

Z hlediska programu se nic nemění: jediné co se změní je *definice funkce*;
volání je pak stejné jako dřív.


# Vyzkoušej si to!

Najdi nějaký svůj program, který používá `ano_nebo_ne`, případně jen `print`
a `input`.

Stáhni si modul <a href="{{ static('tkui.py') }}"><code>tkui.py</code></a>
do adresáře se svým programem.
Naimportuj z něho funkce, které potřebuješ.
Jsou k dispozici čtyři:

```python
from tkui import input, nacti_cislo, ano_nebo_ne, print
```

Tento import *přepíše* vestavěné funkce `input` a `print` variantami,
které mají (téměř) stejné rozhraní – jen dělají něco trochu jinak.

Případné vlastní definice funkcí `nacti_cislo` a `ano_nebo_ne` pak z programu
vyndej, aby se použily ty naimportované.

Program by měl fungovat stejně jako dřív!

Je to tím, že tyto funkce mají stejné rozhraní jako jejich dřívější protějšky,
tedy:

* jméno, kterým se funkce volá,
* argumenty, které bere (např. `input` bere otázku jako řetězec; `print`
  může bere více argumentů k vypsání), a
* návratovou hodnotu, se kterou program pracuje dál (např `input` vrací
  řetězec; u `print` nevrací nic smysluplného).

Většina z těchto informací je přímo v hlavičce funkce.
Ty ostatní je dobré popsat v dokumentačním řetězci, aby ten, kdo chce funkci
použít, věděl jako na to.


# Je to dobrý nápad?

Modul `tkui` je jen ilustrační. Nedoporučuju ho používat.

Příkazová řádka je dělaná tak, aby byla užitečná pro programátory.
Až se naučíš základy a vytvoříš nějaký skvělý program, přijde čas
k logice (tzv. *backendu*) přidat část, která bude lépe použitelná pro
uživatele – tedy okýnko nebo webovou stránku (tzv. *frontend*).

Udělat hezké a funkční *uživatelské* rozhraní je ovšem většinou celkem složité,
a často se dělá až potom, co jsou samotné „vnitřnosti“ funkční a otestované.
Doporučuju postupovat stejně, když se programování učíš: zůstaň u základních
`print` a `input`, dokud nezvládneš samotné programování.
A pak se můžeš naučit něco nového!

Co si ale z této lekce odnes je koncept rozhraní: při zachování několika
informací z hlavičky je možné vyměnit funkci za něco úplně jiného.
A stejně tak je možné jednu funkci (třeba `input`) volat ze spousty různých
programů, pokud znáš její rozhraní.
