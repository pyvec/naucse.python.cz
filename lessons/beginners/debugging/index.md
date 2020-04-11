# Hledání chyb

Jednou z klíčových vlastností vývojáře je umět najít a opravit defekt v programu. V programátorské hantýrce se tento proces nazývá jako _debugging_. Takový defekt (__bug__) totiž nutně nemusí být na první pohled vidět, dokonce nám ani nemusí způsobit výjimku, ale způsobí, že se náš program za určitých podmínek začne chovat nestandardně. Nestandardní chování programu pak může mít různě závažné důsledky.

Typický postup při debuggingu je následující:


1. __Zjistím__, že v programu mám bug.
2. __Najdu__, na kterém místě v programu se bug nachází.
3. __Opravím__ bug.
4. __Otestuji__, že program již funguje správně.

Jeden z prvních nástrojů, který nám pomohl identifikovat, co máme v programu špatně, byla nezachycená výjimka a její popisná zpráva. [Jak číst chyby]({{ lesson_url('beginners/print') }}) jsme probírali již v první lekci.

## Ladící výpisy

Další nástroj, se kterým jsi už určitě sama debuggovala, je funkce `print`. Funkce `print` je jednoduchá a rychlá metoda, jak získat náhled do toho, co se v programu děje. Tomuto vypisování dodatečných informací se říká _ladící výpisy_. Ty slouží čistě k tomu, aby nám umožnily pochopit kde přesně bug je a čím je způsoben. Obzvláště pokud je pro ladící výpisy použita funkce `print`, tyto výpisy by měly být odstraněny před používáním programu uživatelem. Zprávy z ladících výpisů nejsou pro běžného uživatele přínosné a tím pádem zhoršují použitelnost a čitelnost výstupu programu.
Ukažme si to na následujícím programu, který od uživatele načte číslo, přičte k němu jedničku, vynásobí výsledek dvěmi a nakonec od něj odečte pětku. Výsledek vypíše uživateli.

```python
cislo = int(input("Zadej číslo:"))
cislo = cislo + 1
cislo = cislo ** 2
cislo = cislo - 5
print("Výsledek je:", cislo)
```

Jak možná vidíš výpočet neprobíhá úplně správně. Pojďme si to odladit ladícím výpisem.

```python
print("Načítám číslo od uživatele")
cislo = int(input("Zadej číslo:"))
print("Zadané čislo je:", cislo)
print("Přičítám jedničku")
cislo = cislo + 1
print("Po přičtení jedničky je hodnota:", cislo)
print("Násobím dvěmi")
cislo = cislo ** 2
print("Po vynásobení dvěmi je hodnota:", cislo)
print("Odečítám pětku")
cislo = cislo - 5
print("Po odečtení 5 je výsledek:", cislo)
print("Výsledek je:", cislo)
print("Konec programu")
```

Pro číslo `5` získáme následující výstup:

```
Načítám číslo od uživatele
Zadej číslo:5
Zadané čislo je: 5
Přičítám jedničku
Po přičtení jedničky je hodnota: 6
Násobím dvěmi
Po vynásobení dvěmi je hodnota: 36
Odečítám pětku
Po odečtení 5 je výsledek: 31
Výsledek je: 31 .
Konec programu
```

Z výpisu lze sice poznat, že chyba je v násobení dvěmi, nicméně program v takovém stavu nemůžu předat uživateli. Uživatele zajímá pouze výsledek a nikoliv mezivýpočty. To pro uživatele představuje zbytečné informace, ve kterých musí výsledek hledat.

Ladící výpisy také mohou prozradit citlivá data, tedy data, se kterými sice náš program potřebuje pracovat, ale uživateli by je prozradit neměl a proto musíme dávat pozor, abychom je důkladně promazali.

## Logování

Abychom neustále nemuseli myslet na mazání ladících printů a při každé chybě je vracet zase zpět, nabízí se zapisovat zprávy do souboru, tzv. __logu__. To nám umožňuje i výpisy uchovávat a vrátit se k nim, když problém zjistíme později.Nebo nám je může uživatel snadno zaslat a my vidíme, co se u uživatele dělo. Python nám za tímto účelem poskytuje šikovný modul `logging`, který se za nás postará o zapisování do souboru. Zároveň mu můžeme říct, aby nám ukládal zprávy jen důležité zprávy a zbytek ignoroval.

Pojďme se podívat na možnou důležitost (__level__) zpráv a na co se daná důležistost (__level__) hodí.

* __CRITICAL__ = závažná chyba v programu, program dále nemusí fungovat
* __ERROR__ = kvůli závažnější chybě program nemohl dokončit některou operaci
* __WARNING__ = oznámení, že se děje něco, kvůli čemu program může přestat fungovat (např. dochází místo na disku), program ale doposud funguje dle očekávání
* __INFO__ = potvrzení, že program funguje dle očekávání
* __DEBUG__ = detailní informace o tom, co se v programu děje, potřebné pro diagnostiku problémů

Důležitost je seřazena od nejvyšší po nejnižší.

Základní použití tohoto modulu vypadá takto:

```python
import logging

# nastavení logging modulu
# filename nám udává cestu k souboru, do kterého chceme zapisovat
# level nám udává jak důležité zprávy chceme logovat, udává se jako logging.LEVEL, pozor - není to string
logging.basicConfig(filename='podivny_vypocet.log',level=logging.DEBUG)

logging.info("Načítám číslo od uživatele")
cislo = int(input("Zadej číslo:"))
logging.info("Zadané čislo je:", cislo)

logging.info("Přičítám jedničku")
cislo = cislo + 1
logging.debug("Po přičtení jedničky je hodnota:", cislo)

logging.info("Násobím dvěmi")
cislo = cislo ** 2
logging.debug("Po vynásobení dvěmi je hodnota:", cislo)

logging.info("Odečítám pětku")
cislo = cislo - 5
logging.debug("Po odečtení 5 je výsledek:", cislo)

print("Výsledek je:", cislo)

logging.info("Konec programu")
```

Výstup z programu do konzole je pouze oznámení výsledku, veškeré ostatní výpisy se nachází v souboru `podivny_vypocet.log`, který se nachází v adresáři, ze kterého jsme program pustili.

Jak je vidět z programu, pokud chci zaznamenat zprávu pomocí modulu `logging` musím na to použít funkci modulu. Možné funkce jsou vidět v následující ukázce:

```python
import logging

logging.basicConfig(filename='log_test.log',level=logging.DEBUG)

# zaznamenávání ladících výpisů s příslušným levelem (důležitostí)
logging.critical"Tohle je závažná chyba. Program ti nefunguje.")
logging.error("Kvůli chybě se nedala dokončit operace.")
logging.warning("Je možné, že se ti za chvíli něco rozbije.")
logging.info("Funguju na pohodu!")
logging.debug("Tohle jsou podrobné informace důležité pro ladění programu.")
```

Všechny výpisy bychom měli vidět v souboru `log_test.log`, protože `level` máme nastavený na `logging.DEBUG`, který je nejnižší (s nejnižší důležitostí). Kromě nastaveného levelu se totiž logují i všechny levely vyšší (důležitější) a to jsou u nastavení `DEBUG` všechny. Pokud změníme `level` na `INFO` výpis z `logging.debug` už neuvidíme.

> Logování je důležité, ale je to jedna z věcí, na kterou je potřeba cit, který si člověk osvojí až praxí. Loguj moc a tvé logy budou nečitelné, loguj málo a informace budou nedostatečné. Nicméně si nedělej hlavu, pokud zrovna nevíš co použít za level, nebo co vlastně logovat. Prostě loguj.

## Debugger

Ačkoliv jsou ladící výpisy užitečné, někdy je potřeba se uchýlit k sofistikovanějšímu nástroji. Ukažme si tedy, jak funguje debugovací nástroj v MuCode.
