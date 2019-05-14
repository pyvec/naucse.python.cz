# Relační Databáze

Většina aplikací, zejména těch webových, potřebuje manipulovat s daty.
Může se jednat třeba o správu objednávek, produktů na eshopu nebo bankovních transakcí.

Vzhledem k tomu, že databáze jsou velice komplexní téma, tak si v této lekci
projedeme jen základy. Pokud vás ale databáze zaujmou, tak je dobré se podívat
po dalších materiálech, například na [W3Schools](https://www.w3schools.com/sql/).

Nad daty provádíme čtyři druhy operací - vytváření, čtení, úpravu a mazání.
Tyto operace se sdružují do zkratky **CRUD** (Create, Read, Update, Delete).

Existují různé možnosti, kam data ukládat. Mohli bychom například vše zapisovat
do jednoho souboru. Brzy bychom ale zjistili, že se jedná o velice neefektivní
způsob - operace nad daty by s rostoucím počtem záznamů začaly být pomalé.
V těchto situacích nastupují na scénu databáze (resp. databázové systémy).

Jedná se o vysoce sofistikovaná řešení různých výrobců (zmínit můžeme třeba
*Oracle* nebo *MySQL*). Výhodou je, že tyto systémy mají společný způsob,
jakým se s nimi komunikuje (API) - prostřednictvím jazyka **SQL**. Nemusí nás tedy
zajímat, jak databáze funguje uvnitř.

Základem relačních databází jsou **tabulky**. Můžeme si je představit jako jeden
list sešitu MS Excel (celý sešit by pak odpovídal databázi). Jednotlivé řádky
tabulky jsou **záznamy**. Ty se skládají z několika **atributů** (sloupců).
Řádky a sloupce odpovídají Excelovým řádkům a sloupcům.

Můžeme mít například tabulku `OBJEDNAVKA`. Bude tvořena sloupci `ID_OBJEDNAVKY`,
`ID_ZAKAZNIKA`, `DATUM`, `CENA`. Jednotlivé záznamy představují jednotlivé
objednávky - víme tedy kdy si kdo udělal objednávku, a kolik za ni zaplatil.

## SQL
SQL (Structured Querying Language - Strukturovaný dotazovací jazyk) nám umožňuje
komunikovat s databází. Výrobci jednolivých databází obvykle jazyk v některých
oblastech rozšiřují, základ je ale společný a standardzivaný. Kromě práci s daty
(CRUD) se jazyk používá pro vytváření tabulek a dalších objektů, pro správu
uživatelů databáze apod.

SQL příkazy mohou být do databáze posílány z webové aplikace (Python, Javascript, ...),
z terminálu, nebo třeba z aplikace přímo určené pro správu databáze.
Je zvykem jednotlivé příkazy jazyka psát `VELKÝMI PÍSMENY`. Příkazy oddělujeme
středníkem `;`. Jednořádkové komentáře uvozujeme dvěma spojovníky `--`
a víceřádkové komentáře píšeme mezi `/*` a `*/`.

Pojďme se podívat na některé z příkazů, které SQL podporuje.

### Tabulky
Pro vytvoření tabulky použijeme příkaz `CREATE TABLE`, následovaný jménem tabulky
a definicí jednotlivých sloupců. U sloupců definuje jméno, typ a případně další
vlastnosti.

```sql
/* Vytvoří tabulku ROBOT se sloupci ID, NAME a TYPE.
   ID je celé číslo, NAME a TYPE jsou řetězce.
*/
CREATE TABLE ROBOT (
    ID      INT     PRIMARY KEY,
    NAME    TEXT,
    TYPE    TEXT
)
```

Význam `PRIMARY_KEY` si vysvětlíme později. Pokud bychom chtěli tabulku smazat,
tak použijeme `DROP TABLE JMENO_TABULKY`. Jen pozor - spolu s tabulkou se
**smažou všechny záznamy** v ní obsažené.

### INSERT
Jakmile máme vytvořenou tabulku, můžeme do ní vkládat záznamy. Děláme tak
pomocí příkazu `INSERT`. Uvedeme jméno tabulky a pak hodnoty, představující
záznam (nebo záznamy), které se mají vložit.

```sql
-- Vloží do tabulky ROBOT nového Robota s ID 1, jménem Jim a typem AGGRESIVE
INSERT INTO ROBOT (ID, NAME, TYPE) VALUES (1, "Jim", "AGGRESSIVE");

-- Vloží do tabulky ROBOT další dva Roboty
INSERT INTO ROBOT (ID, NAME, TYPE) VALUES (2, "John", "DEFENSIVE"),(3, "Jack", "DEFENSIVE");
```

### SELECT
Když už máme i nějaké zaznámy, tak je dobré mít způsob, jak je číst. Slouží
k tomu mocný příkaz `SELECT`, který v nejzákladnější podobě očekává seznam sloupců,
který se má pro jednotlivé záznamy vypsat, a jméno tabulky, ze které se mají
data číst. Seznam sloupců můžeme nahradit hvězdičkou `*`, pokud chceme vypsat
hodnoty všech sloupců.

```sql
-- vypíše hodnoty všech sloupců pro všechny roboty
SELECT * FROM ROBOT;

-- vypíše jen jména všech robotů
SELECT NAME FROM ROBOT;
```

Příkaz `SELECT` podporuje třeba také filtrování dat (ukážeme si později),
řazení (`ORDER BY`) a seskupování dat (průměr - `AVG`, suma - `SUM`, ...)

### UPDATE
V případě, že chceme data upravit (například změnit jméno robota),
tak použijeme příkaz `UPDATE`. I ten očekává jméno tabulky, jejíž záznamy se
mají upravit. Kromě toho také zadáme nové hodnoty pro jednotlivé sloupce.
Hodnoty sloupců, které neuvedeme, zůstanou nezměněné.

```sql
-- nastaví všem robotům typ na AGGRESSIVE
UPDATE ROBOT SET TYPE = "AGGRESSIVE";
```

### DELETE
A konečně poslední oprací v CRUD je mazání. V SQL se záznamy mažou pomocí příkazu
`DELETE`. I zde, stejně jako u ostatních CRUD příkazů, uvádíme jméno tabulky.

```sql
-- smaže všechny roboty
DELETE FROM ROBOT;
```

### WHERE
Nejspíš vás napadalo, že pokud bychom vždy četli, upravovali nebo mazali všechna
data v tabulce, tak by systém nebyl moc dobře použitelný. Naštěstí ale můžeme
pomocí příkazu `WHERE` ovlivnit, nad jakými záznamy se bude operace provádět.

Za `WHERE` se píší podmínky (spojované pomocí `AND` nebo `OR`), které musí
platit, aby se záznam přidal do množiny, nad kterou se bude operace
provádět. V podmínkách je možné použít různé operátory:

- rovnost: `WHERE SLOUPEC = HODNOTA`
- nerovnost: `WHERE SLOUPEC > HODNOTA` (`>`, `<`, `<>`, ...)
- jedna z hodnot: `WHERE SLOUPEC IN (HODNOTA_1, HODNOTA_2)`
- podřetězec: `WHERE SLOUPEC LIKE %HODNOTA%`

```sql
-- vypíše všechny řádky o robotech, které mají typ AGGRESSIVE
SELECT * FROM ROBOT WHERE TYPE = "AGGRESSIVE";

-- přejmenuje roboty, jejichž jména začínají na J, na Jimmy
UPDATE ROBOT SET NAME = "Jimmy" WHERE NAME LIKE "J%";

-- smaže robota s ID větším než 1
DELETE FROM ROBOT WHERE ID > 1;
```

## Primární klíče
Každá tabulka by měla mít soupec, který jednoznačně identifikuje jednotlivé řádky.
Ve sloupci musí být unikátní hodnoty. Může se jednat o uměle vytvořené číslo
(nejčastěji nazývané `ID`), nebo může jít o unikátní identifikátor z reálného
světa. Pozor ale na to, že ne každý na první pohled unikátní identifikátor je
*skutečně* unikátní - je například možné, aby dvě osoby měly stejné rodné číslo.
Je tedy obecně lepší používat uměle vytvořené primární klíče.

Primární klíče se používají proto, že zrychlují operace nad daty (rychle se podle
nich vyhledává) a také proto, že snižují riziko duplicitních dat v databázi.
Při vytváření tabulky zadáme u sloupce, který má být primárním klíčem, vlastnost
`PRIMARY KEY`.

## Cizí klíče
Cizí klíče - `FOREIGN KEY` - se využívají pro zachycení vazby mezi tabulkami.
V dceřiné tabulce máme sloupec představující cizí klíč, jehož hodnoty se
odkazují na primární klíč jiné tabulky.

Například tabulka `OBJEDNAVKA` má cizí klíč `ID_ZAKAZNIKA`. Tento cizí klíč
se odkazuje na primární klíč tabulky `ZAKAZNIK`. Tím zaručíme, že každá objednávka
musí být "napojená" na existujícího zákazníka.

{{ figure(
    img=static('fk.png'),
    alt="Cizí klíče"
) }}

[zdroj obrázku](https://cdn-images-1.medium.com/max/1600/1*yW_ha3z8Mp6fUn9m6qWwNw.png)

## Spojování tabulek
Často potřebujeme v jednom dotazu číst data z více tabulek. Používáme k tomu
příkaz `JOIN`, který je součástí příkazu `SELECT`. V základní verzi vezme
`JOIN` záznamy z jedné tabulky a připojí k nim odpovídající záznamy z druhé
tabulky. Na takto nově vzniklý řádek je možné udělat `JOIN` s další tabulkou.

To, co považujeme za "odpovídající záznam" zapíšeme jako součást `JOIN`
(za klíčové slovo `ON`). Nejdříve ale musíme zadat jméno tabulky,
kterou chceme připojit.

```sql
-- vypíše jména a příjmení zákazníků, kteří udělali objednávku za více než 500 Kč

SELECT ZAKAZNIK.JMENO, ZAKAZNIK.PRIJMENI
FROM ZAKAZNIK
JOIN OBJEDNAVKA ON OBJEDNAVKA.ZAKAZNIK_ID = ZAKAZNIK.ID
WHERE OBJEDNAVKA.CENA > 500;
```

## Transakce
Transakce jsou skupiny příkazů (`SELECT`, `INSERT`, ...), která se buď provede
celá, nebo vůbec. To má velkou výhodu v tom, že pokud některý z příkazů vyvolá
chybu, tak se databáze vrátí do původního stavu, my můžeme příkaz opravit
a celou transakci spustit znovu.

O transakcích se ale bavíme především proto, že je důležité je **ukončit**,
a to buď příkazem `COMMIT` nebo `ROLLBACK`. `COMMIT` uloží námi provedené
změny trvale do databáze, takže je uvidíme i v budoucích transakcích.
`ROLLBACK` vrátí databázi do původního stavu, což se může hodit v případě,
že jsme provedli jiné změny, než jsme chtěli.

```sql
-- vložení dat
INSERT INTO ROBOT (ID, NAME, TYPE) VALUES(1, "Jim", "AGGRESSIVE");
-- v této chvíli ještě nejsou data trvale uložena

-- uložení dat
COMMIT;
```

## SQLite
Celé povídání o databázích by nemělo moc smysl, pokud bychom si neukázali,
jak je využít z prostředí Pythonu. Jak jsme už zmínili, existují různé databázové
systémy, my se ale zaměříme na jeden z nejjednodušších na "rozjetí", a to **SQLite**.

Tento systém ukládá celou databázi do jednoho binárního souboru.
Můžeme si na něm jednoduše vyzkoušet jednotlivé SQL příkazy,
a to prostřednictvím Python balíčku `sqlite3`. Ukažme si využití tohoto balíčku
na příkladech.

```sql
import sqlite3

# Připojíme se k databázi (v souboru)
connection = sqlite3.connect('pyladies_example_1.db')

# Získáme instanci třídy `Cursor`, pomocí které bude do databáze posílat příkazy
cursor = connection.cursor()

# Pokud tabulka už existuje, tak ji odstraníme,
# abychom mohli skript spouštět opakovaně
cursor.execute("""DROP TABLE IF EXISTS ROBOT""")

# Vytvoříme jednoduchou tabulku
cursor.execute("""CREATE TABLE ROBOT (NAME TEXT, TYPE TEXT)""")

# Vložíme do tabulky data
cursor.execute("""
    INSERT INTO ROBOT (NAME, TYPE)
    VALUES ("JIM", "DEFENSIVE"), ("JACK", "OFFENSIVE")
""")

# Dotážeme se na všechny roboty, výsledky vypíšeme
robots = cursor.execute("SELECT * FROM ROBOT")
for robot in robots:
    print(robot)

# Uložíme změny a uzavřeme spojení
connection.commit()
connection.close()
```

```sql
# Složitejší příklad, který pracuje s primárními a cizími klíči
# a se spojováním tabulek

import sqlite3

# Připojíme se k databázi (v souboru)
connection = sqlite3.connect('pyladies_example_2.db')

# Získáme instanci třídy `Cursor`, pomocí které bude do databáze posílat příkazy
cursor = connection.cursor()

# Pokud tabulky už existují, tak ji odstraníme,
# abychom mohli skript spouštět opakovaně
cursor.execute("""DROP TABLE IF EXISTS ROBOT""")
cursor.execute("""DROP TABLE IF EXISTS BATTLE""")

# Vytvoříme tabulku s roboty a tabulky s výsledky bitev
cursor.execute("""
-- u jednotlivých roborů si ukládáme ID, jméno a typ
CREATE TABLE ROBOT (
    ROBOT_ID INT PRIMARY KEY,
    NAME TEXT,
    TYPE TEXT)
""")

cursor.execute("""
-- bitva se skládá z ID bitvy, ID vítěze a poraženého (odpovídají ID v tabulce ROBOT)
-- a z bodů pro vítěze a poraženého
CREATE TABLE BATTLE (
    BATTLE_ID INT PRIMARY KEY,
    WINNER_ID INT,
    LOSER_ID INT,
    WINNER_POINTS INT,
    LOSER_POINTS INT,
    FOREIGN KEY(WINNER_ID) REFERENCES ROBOT(ROBOT_ID),
    FOREIGN KEY(LOSER_ID) REFERENCES ROBOT(ROBOT_ID)
    )
""")

# Vložíme do tabulkek data
cursor.execute("""
    INSERT INTO ROBOT (ROBOT_ID, NAME, TYPE) VALUES
    (1, "JIM", "DEFENSIVE"), (2, "JACK", "OFFENSIVE"), (3, "JIMMY", "OFFESIVE")
""")

cursor.execute("""
    INSERT INTO BATTLE (BATTLE_ID, WINNER_ID, LOSER_ID, WINNER_POINTS, LOSER_POINTS) VALUES
    (1, 1, 2, 10, 8), -- robot 1 porazil robota 2 se skóre 10:8 (v bitvě 1)
    (2, 2, 1, 6, 9),
    (3, 2, 3, 10, 9),
    (4, 1, 3, 5, 4),
    (5, 3, 2, 2, 0),
    (6, 1, 2, 9, 6)
""")

# Dotážeme se na výsledky bitev, které vyhrál robot se jménem "JIM"
scores = cursor.execute("""
    SELECT BATTLE.WINNER_POINTS, BATTLE.LOSER_POINTS
    FROM BATTLE
    JOIN ROBOT ON ROBOT.ROBOT_ID = BATTLE.WINNER_ID
    WHERE ROBOT.NAME = "JIM"
""")

for score in scores:
    print(score)

# Uložíme změny a uzavřeme spojení
connection.commit()
connection.close()
```

## ORM
V Pythonu jsme se naučili data a logiku sdružovat do **tříd**. V databázích
se data sdružují do **tabulek**. O propojení těchto konceptů se stará ORM - Objektově
Relační Mapování. Pomocí ORM Frameworku (v Pythonu např.
[SQLAlchemy](https://en.wikipedia.org/wiki/SQLAlchemy)) vytváříme Python třídy,
pro které existují odpovídající tabulky v databázi.

Například Python třída `Kocka` bude mít odpovídající tabulku `KOCKA`.
Atributy třídy (`Vek`, `Barva`) budou v databázi existovat jako sloupce.
Jednotlivé řádky tabulky bude možné načíst do aplikace jako instance třídy `Kocka`.
Jednotlivé kočky samozřejmě bude možné upravovat, mazat, nebo vytvářet nové.

Ukázku ORM najdete na [Wikipedii](https://en.wikipedia.org/wiki/SQLAlchemy#Schema_definition)
