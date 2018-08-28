## Seznamy (Lists)

Seznamy jsou proměnlivé (mutable) a to narozdíl od neměnných n-tic (imutable). Seznamy mají mnoho specializovaných metod pro práci a modifikací se seznamy. Nejprve však syntaxe vytváření seznamů.

### Vytvoření seznamu

Prázdný seznam se vytvoří takto:

```
>>> x = []
```

Seznam s dvěmi prvky se vytvoří takto:

```
>>> list = [1, 2]
```

### Funkce list()

Pokud budeme chtít převést prvky řetězce na seznam, můžeme to udělat takto:

```
>>> list('Hello')
['H', 'e', 'l', 'l', 'o']
```

Pokud bychom chtěli naopak sloučit seznam zpět do řetězce, můžeme použít funkci *join()*.

```
>>> l = ['H', 'e', 'l', 'l', 'o']
>>> ''.join(l)
'Hello'
```

### Základní operace nad seznamy

#### Změnna prvů

```
>>> x = [1, 1, 1]
>>> x[1] = 2
>>> x
[1, 2, 1]
```

> [note]
> Nemůžete změnit prvek, který neexistuje, proto následující příklad selže
>
> ```
> >>> x = [1, 1, 1]
>>> x[3] = 4
>Traceback (most recent call last):
>  File "<stdin>", line 1, in <module>
>IndexError: list assignment index out of range
> ```

#### Odstranění prvků

```
>>> names = ['Adam', 'Beta', 'Cyril', 'Dona', 'Eda']
>>> del names[2]
>>> names
['Adam', 'Beta', 'Dona', 'Eda']
```

#### Přiřazení k řezu

```
>>> name = list('Perl')
>>> name
['P', 'e', 'r', 'l']
>>> name[2:] = list('ar')
>>> name
['P', 'e', 'a', 'r']
```

Pokud používáme přiřazení k řezu, můžeme řezem prodloužit délku seznamu.

```
>>> name = list('Perl')
>>> name[1:] = list('ython')
>>> name
['P', 'y', 't', 'h', 'o', 'n']
```

Můžeme je dokonce použít, pokud chceme *vložit* prvky, anuž bychom chtěli nějaké změnit.

```
>>> numbers = [1, 5]
>>> numbers[1:1] = [2, 3, 4]
>>> numbers
[1, 2, 3, 4, 5]
```

Pokud chceme některé prvky odstranit, můžeme to udělat takto:

```
>>> numbers
[1, 2, 3, 4, 5]
>>> numbers[1:4] = []
>>> numbers
[1, 5]
```

### Metody seznamů

Metoda je funkce, která je vázána k určitému objektu (číslo, seznam, n-tice...) a vykonává na něm nějakou akci. Volá se následovně:

```
object.method(arguments)
```

**append**

Metoda *append* přidává objekt na konec seznamu

```
>>> lst = [1, 2, 3]
>>> lst.append(4)
>>> lst
[1, 2, 3, 4]
```

> [note]
> Proč jsem nepoužil místo názvu proměnné lst list? Co by se stalo pak? Kdo na to příjde?

**clear**

Metoda clear vymaže obsah seznamu.

```
>>> lst = [1, 2, 3]
>>> lst.clear()
>>> lst
[]
```

**copy**

Metoda copy zkopíruje list. 

> [warning]
> Pozor na rozdíl mezi zkopírováním a přiřazením jiného jména k existujícímu seznamu!
> 

```
>>> a = [1, 2, 3]
>>> b = a
>>> b[1] = 4
>>> a
[1, 4, 3]
```

Pokud chcete, aby listy *a* a *b* byly oddělené seznamy, musíte je zkopírovat.

```
>>> a = [1, 2, 3]
>>> b = a.copy()
>>> b[1] = 4
>>> a
[1, 2, 3]
```
**count**

Metoda count počítá, kolikrát se prvek vyskytl v poli.

```
>>> ['to', 'be', 'or', 'not', 'to',  'be'].count('to')
2
>>> x = [[1, 2], 1,  1,  [2, 1,  [1, 2]]]
>>> x.count(1)
2
>>> x.count([1, 2])
1
```

**extend**

Tato metoda umožňuje přidat několik hodnot najednou. Seznam tedy může být rozšířen o další seznam.

```
>>> a = [1, 2, 3]
>>> b = [4, 5, 6]
>>> a.extend(b)
>>> a
[1, 2, 3, 4, 5, 6]
```

Pozor na rozdíl mezi *spojením* dvou seznamů a rozšířením. Rozdíle je vidět na násladujícím příkladu.

```
>>> a = [1, 2, 3]
>>> b = [4, 5, 6]
>>> a + b
[1, 2, 3, 4, 5, 6]
>>> a
[1, 2, 3]
```

**index**

Metoda *index* se používá k nalezení prvního výskytu hodnoty.

```
>>> n = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
>>> n.index(6)
5
>>> n.index(11)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
ValueError: 11 is not in list
```

**insert**

Tato metoda vkládá objekt do existujícího seznamu.

```
>>> numbers = [1, 2, 3, 5, 6, 7]
>>> numbers.insert(3, 'four')
>>> numbers
[1, 2, 3, 'four', 5, 6, 7]
```

**pop**

Metoda pop odstraňuje (standardně) poslední prvek seznamu a vrátí jej jako návratovou hodnotu.

```
>>> x = [1, 2, 3]
>>> x.pop()
3
>>> x
[1, 2]
>>> x.pop(0)
1
>>> x
[2]
```

**remove**

Odstraňuje první výskyt hodnoty, kterou nalezne v seznamu.

```
>>> x = ['to', 'be', 'or', 'not', 'to', 'be']
>>> x.remove('be')
>>> x
['to', 'or', 'not', 'to', 'be']
>>> x.remove('bee')
Traceback (innermost last):
 File "<pyshell>", line 1, in ?
  x.remove('bee')
ValueError: list.remove(x): x not in list
```

**reverse**

Obrací pořadí prvků v seznamu.

```
>>> x = [1, 2, 3]
>>> x.reverse()
>>> x
[3, 2, 1]
```

**sort**

Tato metoda uspořádává *in-place* prvky v seznamu. To znamená, že nevrací jako návratovou hodnotu uspořádaný seznam, ale přímo jej modifikuje.

```
>>> x = [4, 6, 2, 1, 7, 9]
>>> x.sort()
>>> x
[1, 2, 4, 6, 7, 9]
```

```
>>> x = [4, 6, 2, 1, 7, 9]
>>> y = x.sort() # Takhle to nefunguje
>>> print(y)
None
```

Místo toho můžeme použít funkci *sorted()*.

```
>>> x = [4, 6, 2, 1, 7, 9]
>>> y = sorted(x)
>>> x
[4, 6, 2, 1, 7, 9]
>>> y
[1, 2, 4, 6, 7, 9]
```