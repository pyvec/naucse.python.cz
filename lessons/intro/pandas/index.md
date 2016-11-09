Materiály k tomuto cvičení jsou k dispozici [na GitHubu][nb].

[nb]: https://github.com/cvut/MI-PYT/blob/master/tutorials/06-pandas/pandas-intro.ipynb

---

Vašim úkolem za pět bodů je odpovědět na otázky a vyřešit úkoly níže.

Řešení může být zpracováno buď jako Jupyter Notebook, ve kterém bude patrné,
která část kódu odpovídá na kterou otázku, nebo jako skript v jazyce Python,
který otázky a odpovědi bude vypisovat na standardní výstup např. tímto stylem:

    Počet památných stromů v Brně:
    44

    Celková délka deseti nejdelších řek (km):
    56289

Repozitář musí obsahovat všechny soubory potřebné k běhu skriptu či Notebooku,
včetně vstupních dat.
Můžete předpokládat, že skript/notebook bude spouštěn z kořenového adresáře
repozitáře.

Kód musí názorným způsobem vypočítat výsledek ze zadaných dat, a nesmí způsobit
neošetřenou výjimku.
V případě Notebooku nesmí výjimku způsobit žádná buňka.

Je zakázáno používat zkratky, zejména `import *` a výběr prvků bez použití
indexeru.

U úloh, kde je výstupem graf, skript graf uloží do souboru a odkáže na něj
ze std. výstupu.
U Notebooku musí být grafy součást výstupu.

Případné grafy musí odpovídat zobrazovaným hodnotám, např. body by neměly být
propojeny čárou, pokud interpolace mezi nimi nedává smysl.

Kód musí korektně zpracovávat neznámé hodnoty (např. člověk s neznámým věkem
nemá 0 let).

K řešení použijte klasická data o pasažérech Titanicu, která jsou distribuována
s jazykem R.
Jsou ke stažení v repozitáři [vincentarelbundock/Rdatasets][data-repo],
konkrétně [zde][data-csv].
Dokumentace k datům je k dispozici [ve stejném repozitáři][data-docs].

[data-repo]: https://github.com/vincentarelbundock/Rdatasets
[data-csv]: https://raw.githubusercontent.com/vincentarelbundock/Rdatasets/master/csv/datasets/Titanic.csv
[data-docs]: http://vincentarelbundock.github.io/Rdatasets/doc/datasets/Titanic.html

Tato data jsou z dnešního pohledu nekompletní, nicméně pro úkol použijte
právě je.

Řešení se odevzdává jako repozitář jménem `titanic` pod studentovým
účtem na GitHubu.
Případné výjimky (např. jméno `titanic` už používáte na něco jiného)
řešte e-mailem.

Otázky a úkoly:

* O kolika pasažérech Titanicu víme?
* Kolik procent jich přežilo?
* Kolik procent žen přežilo? Kolik procent mužů?
* Pro každou třídu vypište kolik pasažérů dané třídy nastoupilo na loď, kolik
  jich přežilo, a kolik to dělá procent přeživších.
* Vykreslete graf procenta přeživších podle dekády věku (t.j. procento pro
  0-9 let, 10-19 let, atd.).
* Závisí na sobě třída a věk pasažéra? Jak? Vykreslete graf(y), které tuto
  závislost znázorňují.
