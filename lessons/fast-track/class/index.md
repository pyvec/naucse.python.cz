# Třídy

Už ses seznámila se spoustou *tříd* objektů, se kterými v Pythonu můžeš
pracovat: s čísly, která se dají třeba sečítat a násobit; řetězci, která se
dají převádět na velká písmenka; seznamy, které umíš seřadit; slovníky,
ve kterých se dá vyhledávat.
Až budeš ve studiu programování pokračovat dál, objevíš další třídy objektů:
soubory, ze kterých se dá číst; Webová stránky, které se dají poslat do
prohlížeče; tlačítka, která jdou zmáčknout, a tak dále.
Tříd je nepřeberné množství.

A podobně jako si můžeš nadefinovat funkci pomocí `def`, i novou třídu si můžeš
vytvořit {{gnd('sám', 'sama')}}.
Používá se to hlavně tehdy, když v programu potřebuješ hodně objektů, které
mají společné chování.
Celá čísla, objekty třídy `int`, mají různou hodnotu ale všechna jdou sčítat.
Každý seznam, objekt třídy `list`, může mít jiný obsah, ale všechny seznamy
jsou seřadit.

Úkol pro tuto sekci bude vytvořit třídu *koťátek*, která můžou mít různá jména,
ale všechna umí mňoukat a jíst.

Začni mňoukáním:

```python
class Kotatko:
    def zamnoukej(self):
        print("Mňau!")
```

Tak jako se funkce definují pomocí `def`,
třídy mají klíčové slovo `class`,
za které napíšeš jméno třídy, dvojtečku a pak odsazené tělo třídy.
Podobně jako `def` dělá funkce, příkaz
`class` udělá novou třídu a přiřadí ji
do proměnné daného jména (tady `Kotatko`).

Třídy se tradičně pojmenovávají s velkým písmenem,
aby se nepletly s „normálními“ hodnotami.

> [note]
> Základní třídy (`str`, `int` atd.)
> velká písmena nemají, a to hlavně z historických
> důvodů – původně to byly opravdu funkce.

V těle třídy můžeš definovat metody, které vypadají
úplně jako funkce – jen mají první argument `self`.
Ten si ale vysvětlíme později – napřed zkus zamňoukat:

```python
# Vytvoření konkrétního objektu
mourek = Kotatko()

# Volání metody
mourek.zamnoukej()
```

Když definuješ třídu (pomocí bloku `class`), neznamená to zatím, že v tvém
programu je nějaké koťátko.
Třída je jako recept nebo manuál: když si koupíš kuchařku, budeš teoreticky
vědět jak upéct dort, jak bude takový dort vypadat a že se dá sníst.
Ale neznamená to ještě, že máš samotný dort!

Konkrétní objekt vytvoříš až zavoláním třídy: použiješ třídu jako funkci,
`Kotatko()`, a výsledek je nový objekt tvé třídy, který už můžeš použít.

Mňau!

## Atributy

U objektů vytvořených z „vlastních“ tříd můžeš nastavovat
*atributy* – informace, které se uloží k danému objektu.
Atributy se označují tak, že mezi hodnotu a jméno
jejího atributu napíšeš tečku:

```python
mourek = Kotatko()
mourek.jmeno = 'Mourek'
print(mourek.jmeno)
```

Řetězec `'Mourek'` teď „patří“ konkrétnímu koťátku.
Když vytvoříš další koťátko, můžeš ho pojmenovat jinak – nastavit mu
atribut `jmeno` na jiný řetězec.

```python
micka = Kotatko()
micka.jmeno = 'Micka'

print(micka.jmeno)
print(mourek.jmeno)
```

## Parametr `self`

Teď se na chvíli vraťme k metodám. Konkrétně k parametru `self`.

Každá metoda má přístup ke konkrétnímu objektu, na
kterém pracuje, právě přes argument `self`.
Teď, když máš koťátka pojmenovaná, můžeš v metodě `zamnoukej` použít `self`
a dostat se tak ke jménu daného koťátka:

```python
class Kotatko:
    def zamnoukej(self):
        print("{}: Mňau!".format(self.jmeno))

mourek = Kotatko()
mourek.jmeno = 'Mourek'

micka = Kotatko()
micka.jmeno = 'Micka'

mourek.zamnoukej()
micka.zamnoukej()
```

Co se stalo? Výraz `mourek.zamnoukej` udělá *metodu*.
Když ji pak zavoláš (`mourek.zamnoukej()`),
objekt `mourek` se předá funkci `zamnoukej` jako první argument, `self` .

Může taková metoda brát víc než jeden argument?
Může – `self` se doplní na první místo,
zbytek argumentů se vezme z volání metody.
Třeba:

```python
class Kotatko:
    def zamnoukej(self):
        print("{}: Mňau!".format(self.jmeno))

    def snez(self, jidlo):
        print("{}: Mňau mňau! {} mi chutná!".format(self.jmeno, jidlo))

mourek = Kotatko()
mourek.jmeno = 'Mourek'
mourek.snez('ryba')
```

## Shrnutí

Třídy toho umí mnohem víc, ale základ: všechny objekty dané třídy mají nějaké
společné chování (třeba koťátka umí mňoukat).
A zároveň každý objekt má i vlastní informace, jen pro něj (třeba koťátko
mňoukání).

Vlastní třídu se vyplatí napsat, když v programu máš víc objektů s podobným
chováním, anebo když jen potřebuješ mít nějakou sadu funkcí (resp. metod) pěkně
pohromadě.


A je to.
*Jsi naprosto skvěl{{gnd('ý', 'á')}}!*
Tohle byla složitá lekce, takže bys na sebe měl{{a}} být hrd{{gnd('ý', 'á')}}.
My jsme na tebe velmi hrdí za to, že ses dostal{{a}} tak daleko!

Běž si krátce odpočinout – protáhnout se, projít se,
zavřít oči – než se pustíš do další kapitoly. :)

🧁

