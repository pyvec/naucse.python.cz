# Funkce

Známe spoustu matematických operací, které se zapisují pomocí symbolů – třeba
plus a minus.
Python se snaží používat stejné symboly jako matematici:

* 3 + 4
* <var>a</var> - <var>b</var>

S násobením a dělením už je to složitější.
Matematický zápis se na běžné klávesnici nedá napsat:

* 3 · 4
* ¾

V Pythonu si ale pořád vystačíme se symbolem, byť trochu jiným – `*`, `/`.

Matematici ale píšou na papír, a tak si můžou dovolit vymýšlet stále
zajímavější klikyháky, které se pak na klávesnici píšou stále hůř:

* <var>x</var>²
* <var>x</var> ≤ <var>y</var>
* sin θ
* Γ(<var>x</var>)
* ∫<var>x</var>
* |<var>s</var>|
* ⌊<var>x</var>⌋
* <var>a</var> ★ <var>b</var>
* <var>a</var> ⨁ <var>b</var>

Ne že by neexistovaly programovací jazyky,
na které je potřeba speciální klávesnice.
Třeba program v jazyce APL laik jednoduše ani nenapíše, ani nepřečte:

<!--z http://catpad.net/michael/apl/ -->
```plain
⍎’⎕’,∈Nρ⊂S←’←⎕←(3=T)∨M∧2=T←⊃+/(V⌽”⊂M),(V⊖”⊂M),(V,⌽V)⌽”(V,V←1¯1)⊖”⊂M’
```

Expert v APL může být vysoce produktivní, ale Python se zaměřuje spíš na to,
aby se dal snadno naučit.
A tak používá symboly jen pro ty nejčastější operace.
Operátorů, které využívají symboly, je tak málo, že už jich zhruba půlku znáš!

> [note]
> Pro zajímavost, tady jsou všechny – i ty co ještě neznáš:
>
> <div>
>     <code>==</code> <code>!=</code>
>     <code>&lt;</code> <code>&gt;</code>
>     <code>&lt;=</code> <code>&gt;=</code>
>     <code class="text-muted">:=</code>
>     <code class="text-muted">|</code> <code class="text-muted">^</code>
>     <code class="text-muted">&amp;</code>
>     <code class="text-muted">&lt;&lt;</code> <code class="text-muted">&gt;&gt;</code>
>     <code>+</code> <code>-</code>
>     <code>*</code> <code class="text-muted">@</code> <code>/</code>
>     <code>//</code> <code>%</code>
>     <code class="text-muted">~</code>
>     <code>**</code>
>     <code class="text-muted">[ ]</code> <code class="text-muted">( )</code>
>     <code class="text-muted">{ }</code>
>     <code class="text-muted">.</code>
> </div>

Všechno ostatní vyjádříme slovně.


## Délka řetězce

Jedna operace, na kterou v Pythonu není symbol, je zjištění délky řetězce.
Místo symbolu má název.
Jmenuje se `len` (z angl. *length*, délka), a používá se takto:

```python
slovo = 'Ahoj'
delka = len(slovo)      # Vypočítání délky
print(delka)
```

To `len` je *funkce* (angl. *function*).
Jak se takové funkce používají?

K tomu, abys funkci mohl{{a}} použít, potřebuješ znát její
*jméno* – tady `len`.
Za jméno funkce patří závorky,
do nichž uzavřeš *argument* (neboli *vstup*) funkce.
To je informace, se kterou bude funkce
pracovat – třeba `len` ze svého argumentu vypočítá délku.

Celému výrazu `len(slovo)` se říká *volání funkce* (angl. *function call*).
Jeho výsledek, takzvaná *návratová* hodnota
(angl. *return value*) se dá třeba přiřadit do proměnné.

{{ figure(img=static('call-anatomy.svg'), alt="Diagram volání funkce") }}

> [note] Pro matemati{{gnd('', 'č', both='')}}ky
> Máš-li rád{{a}} matematiku, dej pozor!
> Funkce v Pythonu je něco jiného než funkce v matematice,
> i když se stejně jmenují a podobně zapisují.
> Pythonní funkce může např. mít pro stejný argument různé hodnoty.


### Volání funkce jako výraz

Vzpomínáš si, jak Python vyhodnocuje výrazy?

```python
vysledek = 3 * (5 + 2)
#              ╰──┬──╯
vysledek = 3 *    7
#          ╰─┬────╯
vysledek =  21
```

Volání funkce je taky výraz.
Stejně jako `a + b` je výraz, který něco udělá podle hodnot `a` a `b`
a výsledek dá k dispozici, `len(slovo)` je výraz, který něco udělá
podle hodnoty `slovo` a výsledek dá k dispozici.

Vždycky, když Python při vyhodnocování narazí na jméno funkce se závorkami,
funkci *zavolá*, zjistí výsledek a dosadí ho:

```python
vysledek = len("Ahoj!")
#          ╰────┬─────╯
vysledek =      5
```

Volání funkce můžeš kombinovat s jinými výrazy, třeba se součtem:

```python
delka = len('Ahoj') + len('!')
#        ╰──┬─────╯    ╰─┬───╯
delka =     4       +    1
#           ╰───────┬────╯
delka =             5
```

Nebo v podmínce ifu – třeba u:

```python
if len('Ahoj!') <= 3:
    print('pozdrav je krátký')
```

… se za `len('Ahoj!') <= 3` nakonec dosadí nepravda (`False`):

```python
   len('Ahoj!') <= 3
#  ╰─────┬────╯
         5      <= 3
#        ╰──────┬──╯
              False
```

Volání funkce můžeš použít i jako argument pro jinou funkci:

```python
print(len('Ahoj'))
#     ╰────┬────╯
print(     4     )   # vypíše 4
```

Nebo to zkombinovat dohromady:

```python
x = 5
print(len('Ahoj') + x)
#     ╰────┬────╯   |
print(     4      + 5)
#          ╰───┬────╯
print(         9     )
```

… a podobně.


### Procedury

Možná sis všiml{{a}}, že jednu funkci už voláš déle: `print("Ahoj!")`
je taky volání funkce.
Stejně jako `len` dostává `print` v závorkách argument – hodnotu, se
kterou pracuje.
Liší se ale návratovou hodnotou.

Funkce `print` sice něco *udělá* – vypíše text
na obrazovku – ale nevrátí žádný smysluplný výsledek, který by zbytek programu
mohl dál zpracovat.

Funkcím, které nic nevrací (jen něco udělají) se občas říká *procedury*.
V Pythonu není hranice mezi „normální“ funkcí a procedurou příliš ostrá,
ale přesto se hodí tento koncept znát.
Pár příkladů:

* Funkce, která vybere náhodné číslo, je „normální“.
  Svůj výsledek vrátí; program s ním může dál pracovat.
* Funkce, která vykreslí na obrazovku kolečko, je *procedura*.
  Žádnou zajímavou hodnotu programu nevrací.
* Funkce, která spočítá průměrný věk obyvatelstva podle informací ze sčítání
  lidu je „normální“. Svůj výsledek vrátí a program s ním může dál pracovat.
* Funkce, která přehraje písničku reproduktorem, je *procedura*.
  Nic zajímavého programu nevrací.

> [note]
> Na rozdíl od ostatních termínů, které se tu učíš, není
> „procedura“ v Pythonu zavedený pojem.
> Je vypůjčený z jazyka Pascal.
> Kdybys o něm diskutoval{{a}} s nějakým zkušeným programátorem,
> odkaž ho prosím na tyto materiály.


## Argumenty

Argument je to, co funkci dáš k dispozici. Hodnota, se kterou funkce pracuje.
Chceš-li délku řetězce `Ahoj!`, použiješ funkci `len` která umí vypočítat
délku *jakéhokoli* řetězce a jako argument, v závorkách, jí dáš tu svoji
konkrétní hodnotu: `len('Ahoj!')`.

Podobně funkce `print` umí vypsat jakoukoli hodnotu.
Tu, kterou má vypsat ve tvém konkrétním případě, jí předáš jako argument.

Některým funkcím můžeš předat i více argumentů.
Třeba zrovna funkci `print`, která všechny své argumenty vypíše na řádek.
Jednotlivé argumenty se oddělují čárkami:

```python
print(1, 2, 3)
```

```python
print("Jedna plus dva je", 1 + 2)
```

Některé funkce nepotřebují žádný argument.
Příkladem je zase `print`.
Je ale nutné použít závorky – i když jsou prázdné.
Hádej, co tohle volání udělá?

```python
print()
```

{% filter solution %}
Funkce `print` zavolaná bez argumentů napíše prázdný řádek.
{% endfilter %}


### Pojmenované argumenty

Některé funkce umí pracovat i s *pojmenovanými* argumenty.
Píšou se podobně jako přiřazení do proměnné,
s rovnítkem, ale uvnitř závorek.

Třeba funkce `print` při výpisu odděluje jednotlivé argumenty mezerou,
ale pomocí argumentu `sep` se dá použít i něco jiného.

```python
print(1, 2, 3, 4, sep=', ')     # Místo mezery odděluj čárkou
```

Dá se změnit i to, co `print` udělá na konci výpisu.
Normálně přejde na nový řádek, ale argumentem `end` můžeš říct, co se má vypsat 
*místo toho*.

> [note]
> Tenhle příklad je potřeba napsat do souboru; v interaktivní konzoli
> nebude výstup vypadat tak, jak má.

```python
print('1 + 2', end=' ')     # Místo přechodu na nový řádek jen napiš mezeru
print('=', end=' ')
print(1 + 2, end='!')
print()
```


### Funkce je potřeba volat

Pozor na to, že když nenapíšeš závorky, funkce se nezavolá!
Výraz `len(s)` je *volání funkce*, ale `len` bez závorek označuje
*funkci samotnou*.

Výsledek `len(s)` je číslo; `len` je funkce.

Čísla můžeš sečítat, můžeš tedy napsat `len(s) + 1`.
Funkce ale sečítat nejde – `len + 1` nedává smysl.

Často se ale stane, že závorky prostě zapomeneš.
Zkus si, co dělají následující příklady, a pozorně si přečti výsledky
a chybové hlášky, abys pak podobné chyby poznal{{a}}:

```python
print(len('a'))     # Volání funkce (a vypsání výsledku)
print(len)          # Vypsání samotné funkce
print(len + 1)      # Sečtení funkce a čísla
```

## Přehled funkcí

A jaké funkce můžeš, kromě `len` a `print`, použít?
Přehled těch základních najdeš v [následující lekci](../basic-functions).
