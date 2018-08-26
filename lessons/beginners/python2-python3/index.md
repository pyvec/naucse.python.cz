## Základní rozdíly mezi Python 2 a Python 3

### Funkce print()
Jedná se o pravděpodobně nejviditelnější změnu mezi Python 2 a Python 3. Příkaz *print* z Python 2 byl v Python 3 nahrazen funkcí *python()*.


**Python 2**


```
print 'Hello, World!'
print('Hello, World!')
print "text", ; print 'print more text on the same line'
```

```
Hello, World!
Hello, World!
text print more text on the same line
```

**Python 3**

```
print('Hello, World!')

print("some text,", end="")
print(' print more text on the same line')
```

```
Hello, World!
some text, print more text on the same line
```

```
print 'Hello, World!'
```

```
File "<ipython-input-3-139a7c5835bd>", line 1
    print 'Hello, World!'
                        ^
SyntaxError: invalid syntax
```

### Dělení celými čísly

Dělení celými čísly se chová rúzným způsobem v Python 2 a v Python 3.

**Python 2**

```
print '3 / 2 =', 3 / 2
print '3 // 2 =', 3 // 2
print '3 / 2.0 =', 3 / 2.0
print '3 // 2.0 =', 3 // 2.0
```

```
3 / 2 = 1
3 // 2 = 1
3 / 2.0 = 1.5
3 // 2.0 = 1.0
```

**Python 3**

```
print('3 / 2 =', 3 / 2)
print('3 // 2 =', 3 // 2)
print('3 / 2.0 =', 3 / 2.0)
print('3 // 2.0 =', 3 // 2.0)
```

```
3 / 2 = 1.5
3 // 2 = 1
3 / 2.0 = 1.5
3 // 2.0 = 1.0
```

### Podpora Unicode

Python 2 má separátní typy pro str(), jedná se o ASCII znaky a dále pak unicode(). V Python 3 jsou všechny řetězce str() standardně Unicode znaky. Dále pak Python 3 zavádí podporu *byte*.

### Vyvolání výjimky

V Python 2 jsou možné dvě možnosti jak vyvolat výjimku. Python 3 umožňuje jen jednu.

**Python 2**

```
raise IOError, "file error"
```

```
raise IOError, "file error"
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
IOError: file error
```

```
raise IOError("file error")
```

```
raise IOError("file error")
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
IOError: file error
```

**Python 3**

Následující způsob zápisu v Python 3 nefunguje:

```
raise IOError, "file error"
```

```
raise IOError, "file error"
  File "<stdin>", line 1
    raise IOError, "file error"
                 ^
SyntaxError: invalid syntax
```
Jediný správný zápis je tento:

```
raise IOError("file error")
```

```
raise IOError("file error")
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
OSError: file error
```

### Ošetřování výjimek

Oštřování výjimek se také změnilo. Podívej se, jak se ošetřují výjimky v Python 2 a v Python 3.

**Python 2**

```
try:
    let_us_cause_a_NameError
except NameError, err:
    print err, '--> our error message'
```

```
name 'let_us_cause_a_NameError' is not defined --> our error message
```

**Python 3**

```
try:
    let_us_cause_a_NameError
except NameError as err:
    print(err, '--> our error message')
```

```
name 'let_us_cause_a_NameError' is not defined --> our error message
```

### Uživatelské vstupy

V Pythonu 2 existují dva způsoby, jak získat vstup od uživatele. Funkce *input()* a funkce *raw_input()*. Problém ve funkci *input()* je, že může být potenciálně nebezpečná, protože nevrací vždy typ *string*.

**Python 2**

```
Python 2.7.6
[GCC 4.0.1 (Apple Inc. build 5493)] on darwin
Type "help", "copyright", "credits" or "license" for more information.

>>> my_input = input('enter a number: ')

enter a number: 123

>>> type(my_input)
<type 'int'>

>>> my_input = raw_input('enter a number: ')

enter a number: 123

>>> type(my_input)
<type 'str'>
```

**Python 3**

```
Python 3.7.0 (default, Aug 24 2018, 20:34:01)
[Clang 9.0.0 (clang-900.0.39.2)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>> my_input = input('enter a number: ')
enter a number: 123
>>> type(my_input)
<class 'str'>
```