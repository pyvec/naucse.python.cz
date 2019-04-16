# Debugování

Při vývoji software se často dostaneme do situace,
kdy si chceme projít kód krok za krokem a zjistit
například to, jaké jsou aktuální hodnoty proměnných,
jestli se správně vyhodnocují podmínky atd.
Tomuto procesu se česky říká *ladění*, často se ale
setkáte s anglickým výrazem *debugging*. Obvykle
ho provádíme ve chvíli, kdy se program nechová
podle očekávání, tedy jsme narazili na chybu (bug).

Možná jste byly zvyklé si na různá místa v programu
pomocí funkce `print` vypisovat aktuální stav programu.
Zjistíte, že u většího projektu je tento přístup většinou
nedostatečný a že si chcete program projít krok za krokem.

Abychom mohli debugovat, potřebujeme k tomu nástroj zvaný
*debugger*. VSCode spolu s [rozšířením pro Python](https://marketplace.visualstudio.com/items?itemName=ms-python.python) ho má zabudovaný.
Ve zbytku této lekce si ukážeme, jak ho používat.

## Ovládání debuggeru
Do debuggeru se přepneme kliknutím na tlačítko s přeškrtnutým broukem,
které vidíte na obrázku níže.

{{ figure(
    img=static('debug.png'),
    alt="(Menu debuggeru)",
) }}

Zajímají nás především:
- tlačítko pro spuštění debugování (zelený trojúhelník)
- panel s výpisem aktuálních hodnot proměnných - *Variables*
- panel pro ovládání debuggeru

**Panel pro ovládání debuggeru** se zobrazí až po spuštění debuggeru.
Po spuštění je možné debugger restartovat (spustit od začátku)
kliknutím na zelenou šipku ve tvaru kruhu
nebo ho zastavit kliknutím na červený čtvereček.

Program se chová stejně, jako by debugger nebyl zaplý.
Např., pokud se podmínka vyhodnotí jako `False`, tak do jejího těla debugger nevstoupí.
Stejně tak debugger bude procházet cyklem tolikrát, jako za normálního
běhu programu.

### Breakpoint
Klíčovou roli při debugování hraje zarážka - angl. *breakpoint*.
Když debuger narazí na zarážku, tak zastaví vykonávání programu
a předá kontrolu uživateli. Ten poté může zjistit hodnoty proměnných,
pokračovat na další krok nebo třeba vejít do funkce, která se na řádku volá.
Breakpoint umístíme kliknutím vlevo od řádku, kde chceme, aby se debugger zastavil:

{{ figure(
    img=static('breakpoint.png'),
    alt="(Umístění breakpointu)",
) }}

Pokud klikneme na tlačítko *Continue* (modrý trojúhelník nebo <kbd>F5</kbd>),
tak bude debugger pokračovat až do dalšího breakpointu,
případně na konec programu.

### Step over, into, out
Často budeme chtít pokračovat na další řádek kódu. Docílíme toho pomocí
klávesy <kbd>F10</kbd>, případně kliknutím na *Step over*.

Pokud bychom chtěli vstoupit do funkce, která je volaná na aktualním řádku,
tak toho docílíme pomocí <kbd>F11</kbd> - *Step into*.

Pro vystoupení z aktuální funkce se používá
<kbd>Shift</kbd> + <kbd>F11</kbd>.
Program pokračuje až do chvíle, než se vrátí do funkce, která volala
funkci, ze které jsme chtěli vystoupit.

## Debug testů
Často zjistíme, že nám neprocházejí testy.
Může se jednat o chybu v testu, nebo o chybu v programu.
Ideální je si test prodebugovat, a to například tak,
že dáme breakpoint na začátek testu a pak se kombinací
*Step over / into / out* dostaneme na problémové místo programu.
Budeme sledovat, jak se vyhodnocují jednotlivé podmínky,
jaké argumenty se předávají do funkcí atd.
Často se nám tímto způsobem podaří chybu najít.

Pokud máme správně nastavený VSCode, tak by se nad testovacími
funkcemi měly objevit možnosti *Run Test* a *Debug Test*
(jako na obrázku níže).

{{ figure(
    img=static('test_debug.png'),
    alt="(Debug testu)",
) }}

Jestli ve svém editoru tyto možnosti nemáš, tak zkus:
- zkontrolovat, že máš nastavený interpreter
  - v levém dolním rohu VSCode by jsi kromě verze Pythonu
    měla vidět jméno virtuálního prostředí (např. Python 3.6 (venv))
    - pokud jméno virtuálního prostředí nevidíš, tak stiskni
      <kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>P</kbd>,
      vyber *Select Python Interpreter* a zvol své virtuální prostředí
      (pravděpodobně *venv*)
- Stisknout <kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>P</kbd> a vybrat *Discover Unit Tests*

Po kliknutí na *Debug test* se spustí debugger.

## Debug console
Po spuštění debugeru je možné používat debugovací konzoli.
Najdete ji ve spodním panelu v záložce vedle integrovaného terminálu.

{{ figure(
    img=static('debug_console.png'),
    alt="(Debug konzole)",
) }}

Představ si, že jsi spustila Python z příkazové řádky
a poté zadala stejný kód, kterým debugger prošel, než se dostal na breakpoint.
V tu chvíli tedy máte k dispozici všechny inicializované globální proměnné,
můžete volat funkce nebo pracovat s proměnným úplně stejně,
jak jsme to dělali v lekcích na začátku kurzu.

Pokud například víte, že na dalším řádku vzniká `IndexError`, ale nevíte proč,
tak můžete zjistit, na jaký index se přistupuje, jaké hodnoty jsou v
seznamu nebo slovníku obsažené a co by se stalo, kdybyste použily jiný index.

Do debug konzole se také vypisují `printy`, pokud je v programu používáte.

Jen pozor - pokud upravíte hodnoty proměnných,
tak se změny promítnout do zbytku programu, takže je někdy nutné
debugger restartovat.
