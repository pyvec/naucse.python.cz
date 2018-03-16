# Soubory

Dnes se podíváme na to, jak v Pythonu číst z
(a pak i zapisovat do) souborů.

Ke čtení textu ze souboru jsou potřeba tři kroky:
* soubor *otevřít*,
* něco z něj *přečíst*
* a pak jej zase *zavřít*.

Vytvoř si v editoru soubor `basnicka.txt` a napiš do něj libovolnou básničku.
Soubor ulož.

> [note]
> Na uložení souboru s básničkou doporučuji použít
> stejný editor, jaký používáš na Pythonní programy.
>
> Používáš-li jiný editor než Atom, dej si při ukládání pozor na kódování:
> * Nabízí-li ti editor při ukládání výběr kódování, vyber UTF-8.
> * Je-li k dispozici kódování „UTF-8 bez BOM”, použij to.
> * Pokud musíš použít Notepad, který výše uvedené možnosti nemá, pak v kódu
>   níže použij místo `'utf-8'` nestandardní `'utf-8-sig'`.
>
> Ono [`utf-8`] je název standardního kódování.
> Zajišťuje, že se případné emoji nebo znaky s diakritikou do souboru uloží
> tak, aby se daly přečíst i na jiném počítači či operačním systému.
> 🎉

[`utf-8`]: https://en.wikipedia.org/wiki/UTF-8

Potom napiš tento program:

```python
soubor = open('basnicka.txt', encoding='utf-8')
obsah = soubor.read()
print(obsah)
soubor.close()
```

a spusť ho z adresáře, ve kterém je
`basnicka.txt` (jinými slovy, aktuální adresář musí být ten, který
obsahuje soubor s básničkou).

Obsah souboru se vypíše!

Co se tu děje?
Tak jako `int()` vrací čísla a `input()` řetězce, funkce
`open()` vrací hodnotu, která představuje *otevřený soubor*.
Tahle hodnota má vlastní metody.
Tady používáme metodu `read()`, která
najednou přečte celý obsah souboru a vrátí ho jako řetězec.
Na metodu `close()`, která otevřený soubor zavírá, se podíváme později.


## Iterace nad soubory

Otevřené soubory se, jako např. řetězce či `range`,
dají použít s příkazem `for`.
Tak jako `for i in range` poskytuje za sebou jdoucí čísla a `for c in 'abcd'`
poskytuje jednotlivé znaky řetězce, `for radek in soubor` bude do proměnné
`radek` dávat jednotlivé řádky čtené ze souboru.

Například můžeme básničku odsadit,
aby se vyjímala v textu:

```python
print('Slyšela jsem tuto básničku:')
print()
soubor = open('basnicka.txt', encoding='utf-8')
for radek in soubor:
    print('    ' + radek)
soubor.close()
print()
print('Jak se ti líbí?')
```


Když to zkusíš, zjistíš, že trochu nesedí
řádkování. Zkusíš vysvětlit, proč tomu tak je?

{% filter solution %}
Každý řádek končí znakem nového řádku (`'\n'`).
Při procházení souboru Python tento znak nechává na konci řetězce
`radek` ¹.
Funkce `print` pak přidá další nový řádek, protože ta na konci
výpisu vždycky odřádkovává – pokud nedostane argument `end=''`.
To je jeden způsob jak řádkování „spravit“; další je použít na každý řádek
metodu `rstrip`, která odstraní mezery a nové řádky z konce řetězce.

---

¹ Proč to dělá? Kdyby `'\n'` na konci řádků nebylo,
nedalo by se např. dobře rozlišit, jestli poslední řádek
končí na `'\n'`

{% endfilter %}


## Zavírání souborů

Je docela důležité soubor potom, co s ním
přestaneš pracovat, zavřít (pomocí metody `close()`).
Operační systémy mají limity na počet
současně otevřených souborů, které se nezavíráním
dají snadno překročit.
Na Windows navíc nemůžeš soubor, který je stále
otevřený, otevřít znovu.

Soubory se dají přirovnat k ledničce: abychom něco
mohly z ledničky vzít, nebo dát dovnitř, musíme
ji předtím otevřít a potom zavřít.
Bez zavření to sice na první pohled funguje taky,
ale pravděpodobně potom brzo něco zplesniví.


Zapomenout zavřít soubor je docela jednoduché:
například pokud by v rámci zpracování souboru
nastala výjimka nebo kdybys vyskočila z funkce
pomocí `return`, náš předchozí kód by `close` nezavolal,
a soubor by zůstal otevřený.

K tomu, abychom soubor nezapomněl{{gnd('i', 'y', both='i')}} v podobných
příkazech zavřít, slouží příkaz
`try/finally`, který jsme si ukázal{{gnd('i', 'y', both='i')}} v souvislosti
s výjimkami.

Pro připomenutí, `finally` se provede vždycky – i když blok `try` skončí
normálně, i když v něm nastane výjimka, i když z něj
„vyskočíš” pomocí `return` či `break`.

```python
def iniciala():
    """Vrátí první písmeno v daném souboru."""

    soubor = open('basnicka.txt', encoding='utf-8')
    try:
        obsah = soubor.read()
        return obsah[0]
    finally:
        soubor.close()

print(iniciala())
```

Blok `finally` se takhle dá použít vždycky,
když je potřeba něco ukončit nebo zavřít – ať už
je to soubor, nebo třeba připojení k databázi.


## Příkaz with

Protože je `try/finally` celkem dlouhé a nepohodlné, má Python i příjemnější
variantu, příkaz `with`:

```python
def iniciala():
    """Vrátí první písmeno v daném souboru."""

    with open('basnicka.txt', encoding='utf-8') as soubor:
        obsah = soubor.read()
        return obsah[0]

print(iniciala())
```
Tenhle příkaz jsme už viděl{{gnd('i', 'y', both='i')}} u testování,
kde uvozoval blok, ve kterém má nastat výjimka –
potom, co blok skončí, se zkontroluje, jestli
nastala a jestli je toho správného typu.
V našem případě se po skončení bloku
zavře soubor, ať už výjimka nastala nebo ne.
Podobně jako s `finally` se zavře vždycky
– ať už blok `with` skončil normálně,
výjimkou, nebo, jako tady, „vyskočením” ven.

V naprosté většině případů je pro práci se soubory
nejlepší použít `with`.


## Psaní souborů

> [warning] Pozor!
> Pro Python není problém smazat obsah jakéhokoli souboru.
> Psaní do souborů si zkoušej v adresáři, ve kterém nemáš uložené
> důležité informace!

Soubory se v Pythonu dají i zapisovat.
Pro zápis se soubor otevře pomocí pojmenovaného
argumentu `mode='w'` (z angl.
*mode*, mód a *write*, psát).
Zapisovat jednotlivé řetězce se pak dá metodou
`write`.

Pokud soubor už existuje, otevřením s `mode='w'` se veškerý jeho obsah smaže.
Po zavření tak v souboru bude jen to, co do něj ve svém programu zapíšeš.

```python
with open('druha-basnicka.txt', mode='w', encoding='utf-8') as soubor:
    soubor.write('Naše staré hodiny\n')
    soubor.write('Bijí čtyři hodiny\n')
```

> [note] Proč to \n?
> Metoda `write` neodřádkovává automaticky.
> Chceš-li do souboru zapsat více řádků, je potřeba každý z nich ukončit
> „ručně“, speciálním znakem `'\n'` který jsme si popsal{{ gnd('i', 'y', both='i')}}
> v [sekci o řetězcích]({{ lesson_url('beginners/str') }}).

Případně se dá použít funkce `print`,
která kromě do terminálu umí vypisovat i do otevřeného souboru,
a to pomocí pojmenovaného argumentu `file`.
Ostatní možnosti funkce `print` – automatické odřádkování,
převádnění na řetězce, možnost vypsat víc
hodnot najednou apod. – samozřejmě zůstávají.

```python
with open('druha-basnicka.txt', mode='w', encoding='utf-8') as soubor:
    print('Naše staré hodiny', file=soubor)
    print('Bijí', 2+2, 'hodiny', file=soubor)
```
