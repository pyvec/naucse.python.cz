## Řetězce (Strings)

Všechny standarní sekvenční operace (indexing, slicing, multiplication, membership, length, minimum, maximum) jsou použitelné také u řetězců.

Pamatujte ale, že řetězce jsou immutable, proto následující kód nebude fungovat.

```
>>> website = 'http://www.python.org'
>>> website[-3:] = 'com'
Traceback (most recent call last):
  File "<pyshell#19>", line 1, in ?
  website[-3:] = 'com'
TypeError: object doesn't support slice assignment
```

## Formátování řetězců

Jednou ze metod jak vytisknout a formátovat řetězce operátor %, tak jako v jazyce C.

Jako hodnoty, které chceme vytisknout můžeme použít string, integer, tuple nebo dictionary.

```
>>> format = "Hello, %s. %s are you?"
>>> values = ('world', 'How')
>>> format % values
'Hello, world. How are you?'
```

%s je tzv. *conversion specifiers*. Označují místa, kde se má vložit hodnoty z pravé strany přiřazení.

Další možné použití:

```
%s - string
%i - integer
%f - floating point
```

Nejnovější a doporučovaný způsob formátování řetězců je pomocí metody *format()*. Každé položka řetězce, kterou chceme formátovat je reprezentována složenými závorkami *{}* a může obsahovat jméno a také informace o tom, jak správně řetězec zformátovat.

```
>>> "{}, {} and {}".format("first", "second", "third")
'first, second and third'
>>> "{0}, {1} and {2}".format("first", "second", "third")
'first, second and third'
```

Můžeme formátovat i takto:

```
>>> "{3} {0} {2} {1} {3} {0}".format("be", "not", "or", "to")
'to be or not to be'
```
Hodnoty můžeme také pojmenovávat:


```
>>> from math import pi
>>> "{name} is approximately {value:.2f}.".format(value=pi, name="π")
'π is approximately 3.14.'
```

*.2f* znamená, že číslo bude vytištěno s přesností na dvě desetinná místa.

V Pythonu 2.6 můžeme formátovat řetězec i takto:

```
>>> from math import e
>>> f"Euler's constant is roughly {e}."
"Euler's constant is roughly 2.718281828459045."
```

Starší ekvivalent stejného kódu je: 

```
>>> "Euler's constant is roughly {e}.".format(e=e)
"Euler's constant is roughly 2.718281828459045."
```

Formátování řetězců (funkce format) používá templatovací jazyk. Každá hodnota, která má být nahrazena je uložená ve složených uvozovkách *{}*, tzv *replacement fields*. Poud chceme vypsat ve výpisu složené uvozovky, musíme to udělat takto:

{% raw %}
```
>>> "{{ double braces }}".format()
'{ double braces }'
```
{% endraw %}

###  Replacement Fields

Skládají se z:

**Field name** - index nebo indentifikátor

**Conversion flag** - Vykřičník následovaný jedním znakem

* r - repr
* s - string
* a - ascii

**Format specifier** - dojtečka následovaná výrazem templatovacího jazyka

Příklady použití:

```
>>> "{foo} {} {bar} {}".format(1, 2, bar=4, foo=3)
'3 1 4 2'
```

Můžeme přistupovat také jen k části hodnoty (pole), kterou chceme vytisknout:

```
>>> fullname = ["Alfred", "Hitchcock"]
>>> "Mr {name[1]}".format(name=fullname)
'Mr Hitchcock'
```

### Základní konverze

```
>>> print("{pi!s} {pi!r} {pi!a}".format(pi="π"))
π 'π' '\u03c0'
```

Floating point *format specifier*

```
>>> "The number is {num}".format(num=42)
'The number is 42'
>>> "The number is {num:f}".format(num=42)
'The number is 42.000000'
```

Binary *format specifier*

```
>>> "The number is {num:b}".format(num=42)
'The number is 101010'
```

**Format specifier**

* b - binary
* c - integer
* d - integer vytiskne jako decimal
* f - decimal s fixním počtem desetinných míst
* o - integer jako osmičkové číslo

Více v dokumentaci.

### Šířka zarovnání

```
>>> "{num:10}".format(num=3)
'         3'
>>> "{name:10}".format(name="Bob")
'Bob       '
```

### Precison

```
>>> "Pi is {pi:.2f}".format(pi=pi)
'Pi is 3.14'
```

Formátování se zarovnáním:

```
>>> "{pi:10.2f}".format(pi=pi)
'      3.14'
```

Přesnost zarovnání se dá použít také takto:

```
>>> "{:.5}".format("Guido van Rossum")
'Guido'
```

Můžeme specifikovat několik typů zarovnání.

Zero-padded:

```
>>> '{:010.2f}'.format(pi)
'0000003.14'
```

Levé, pravé a vycentrované:

```
>>> print('{0:<10.2f}\n{0:^10.2f}\n{0:>10.2f}'.format(pi))
3.14
   3.14
      3.14
```

Můžeme specifikovat jakým znakem vyplníme volné místa, jako náhradu za mezeru:

```
>>> "{:$^15}".format(" I WON ")
'$$$$ I WON $$$$'
```

Jak formátovat čísla se znaménky?

```
>>> print('{0:-.2}\n{1:-.2}'.format(pi, -pi)) # Default
3.1
-3.1
>>> print('{0:+.2}\n{1:+.2}'.format(pi, -pi))
+3.1
-3.1
>>> print('{0: .2}\n{1: .2}'.format(pi, -pi))
 3.1
-3.1
```

Praktický příklad:

{% raw %}

```
# Print a formatted price list with a given width

width = int(input('Please enter width: '))

price_width = 10
item_width  = width - price_width

header_fmt = '{{:{}}}{{:>{}}}'.format(item_width, price_width)
fmt        = '{{:{}}}{{:>{}.2f}}'.format(item_width, price_width)

print('=' * width)

print(header_fmt.format('Item', 'Price'))

print('-' * width)

print(fmt.format('Apples', 0.4))
print(fmt.format('Pears', 0.5))
print(fmt.format('Cantaloupes', 1.92))
print(fmt.format('Dried Apricots (16 oz.)', 8))
print(fmt.format('Prunes (4 lbs.)', 12))                                                                              

print('=' * width)
```

{% endraw %}


Výstup:

```
Please enter  width: 35
===================================
Item                          Price
-----------------------------------
Apples                         0.40
Pears                          0.50
Cantaloupes                    1.92
Dried  Apricots (16 oz.)       8.00
Prunes (4 lbs.)               12.00
===================================
```

## Metody řetězců

### center()

```
>>> "The Middle by Jimmy Eat World".center(39)
'     The Middle by Jimmy Eat World     '
>>> "The Middle by Jimmy Eat World".center(39, "*")
'*****The Middle by Jimmy Eat World*****'
```

### find()

Vrací levý index, na kterém našel výskyt řetězce.

```
>>> 'With a moo-moo here, and a moo-moo there'.find('moo')
7
>>> title = "Monty Python's Flying Circus"
>>> title.find('Monty')
0
>>> title.find('Python')
6
>>> title.find('Flying')
15
>>> title.find('Zirquss')
-1
```

### join()

```
>>> seq = [1, 2, 3, 4, 5]
>>> sep = '+'
>>> sep.join(seq) # Trying to join a list of numbers
Traceback (most recent call last):
  File "<stdin>", line 1, in ?
TypeError: sequence item 0: expected string, int found
>>> seq = ['1', '2', '3', '4', '5']
>>> sep.join(seq) # Joining a list of strings
'1+2+3+4+5'
>>> dirs = '', 'usr', 'bin', 'env'
>>> '/'.join(dirs)
'/usr/bin/env'
>>> print('C:' + '\\'.join(dirs))
C:\usr\bin\env
```
Inverzní funkce je *split()*.

### lower()

Vrací lowercase verzi řetězce:

```
>>> 'Dance Floor'.lower()
'dance floor'
```

Reverzní funkce *upper()*.

### replace()

Všechny výskyty hledaného řetězce jsou nahrazeny.

```
>>> 'This is a test'.replace('is', 'eez')
'Theez eez a test'
```

### split()

```
>>> '1+2+3+4+5'.split('+')
['1', '2', '3', '4', '5']
>>> '/usr/bin/env'.split('/')
['', 'usr', 'bin', 'env']
>>> 'Using   the   default'.split()
['Using', 'the', 'default']
```

### strip()

Vrací řetězec bez prázdných znaků na začátku a na konci.

```
>>> '    internal whitespace is kept    '.strip()
'internal whitespace is kept'
```

