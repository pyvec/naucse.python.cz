# Soubory

Dnes se podíváme na to, jak v Pythonu číst z
(a pak i zapisovat do) souborů.

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
soubor.close()

print(obsah)
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
Nakonec metoda `close()` otevřený soubor zase zavře.


## Automatické zavírání souborů

Soubory se dají přirovnat k ledničce: abys něco
mohl{{a}} z ledničky vzít, nebo dát dovnitř, musíš
ji předtím otevřít a potom zavřít.
Bez zavření to sice na první pohled funguje taky,
ale pravděpodobně potom brzo něco zplesniví.

Stejně tak je docela důležité soubor zavřít po tom,
co s ním přestaneš pracovat.
Bez zavření to na první pohled funguje, ale složitější programy se můžou dostat
do problémů.
Operační systémy mají limity na počet
současně otevřených souborů, které se nezavíráním
dají snadno překročit.
Na Windows navíc nemůžeš soubor, který je stále
otevřený, otevřít znovu.

Na korektní zavření souboru ale programátoři často zapomenou.
Proto Python poskytuje příkaz `with`, který soubory zavírá automaticky.
Používá se takhle:

```python
with open('basnicka.txt', encoding='utf-8') as soubor:
    obsah = soubor.read()

print(obsah)
```

Příkaz `with` vezme otevřený soubor (který vrací funkce `open`)
a přiřadí ho do proměnné `soubor`.
Pak následuje odsazený blok kódu, kde se souborem můžeš pracovat – v tomhle
případě pomocí metody `read` přečíst obsah jako řetězec.
Když se Python dostane na konec odsazeného bloku, soubor automaticky zavře.

V naprosté většině případů je pro otevírání souborů nejlepší použít `with`.


## Iterace nad soubory

Otevřené soubory se, jako např. řetězce či `range`,
dají použít s příkazem `for`.
Tak jako `for i in range` poskytuje za sebou jdoucí čísla a `for c in 'abcd'`
poskytuje jednotlivé znaky řetězce, `for radek in soubor` bude do proměnné
`radek` dávat jednotlivé řádky čtené ze souboru.

Například můžeš básničku odsadit,
aby se vyjímala v textu:

```python
print('Slyšela jsem tuto básničku:')
print()

with open('basnicka.txt', encoding='utf-8') as soubor:
    for radek in soubor:
        print('    ' + radek)

print()
print('Jak se ti líbí?')
```


Když to zkusíš, zjistíš, že trochu nesedí
řádkování. Zkusíš vysvětlit, proč tomu tak je?

{% filter solution %}
Každý řádek končí znakem nového řádku, `'\n'`,
který možná znáš ze [sekce o řetězcích](../str/).
Při procházení souboru Python tento znak nechává na konci řetězce `radek` ¹.
Funkce `print` pak přidá další nový řádek, protože ta na konci
výpisu vždycky odřádkovává – pokud nedostane argument `end=''`.

---

¹ Proč to dělá? Kdyby `'\n'` na konci řádků nebylo,
nedalo by se např. dobře rozlišit, jestli poslední řádek
končí na `'\n'`

{% endfilter %}

Ideální způsob, jak odřádkování spravit, je odstranit z konce řetězce
bílé znaky (mezery a nové řádky) pomocí metody `rstrip`:


```python
print('Slyšela jsem tuto básničku:')
print()

with open('basnicka.txt', encoding='utf-8') as soubor:
    for radek in soubor:
        radek = radek.rstrip()
        print('    ' + radek)

print()
print('Jak se ti líbí?')
```


## Psaní souborů

> [warning] Pozor!
> Pro Python není problém smazat obsah jakéhokoli souboru.
> Psaní do souborů si zkoušej v adresáři, ve kterém nemáš uložené
> důležité informace!

Soubory se v Pythonu dají i zapisovat.
Pro zápis soubor otevři s pojmenovaným
argumentem `mode='w'` (z angl. *mode*, mód a *write*, psát).

Pokud soubor už existuje, otevřením s `mode='w'` se veškerý jeho obsah smaže.
Po zavření tak v souboru bude jen to, co do něj ve svém programu zapíšeš.

Informace pak do souboru zapiš známou funkcí `print`,
a to s pojmenovaným argumentem `file`:

```python
with open('druha-basnicka.txt', mode='w', encoding='utf-8') as soubor:
    print('Naše staré hodiny', file=soubor)
    print('Bijí', 2+2, 'hodiny', file=soubor)
```
