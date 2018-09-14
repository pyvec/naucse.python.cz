## Exceptions

An exception is an event, which occurs during the execution of a program that disrupts the normal flow of the program's instructions. In general, when a Python script encounters a situation that it cannot cope with, it raises an exception. An exception is a Python object that represents an error.

When a Python script raises an exception, it must either handle the exception immediately otherwise it terminates and quits.

```
>>> 1 / 0
Traceback (most recent call last):
   File "<stdin>", line 1, in ?
ZeroDivisionError: integer division or modulo by zero
```

### raise statement

You can raise exceptions in several ways by using the raise statement. An exception can be a string, a class or an object. Most of the exceptions that the Python core raises are classes, with an argument that is an instance of the class.

```
>>> raise Exception
Traceback (most recent call last):
   File "<stdin>", line 1, in ?
Exception
>>> raise Exception('hyperdrive overload')
Traceback (most recent call last):
   File "<stdin>", line 1, in ?
Exception: hyperdrive overload
```

Build-in Exceptions:

|  Class Name |  Description |
|---|---|
| Exception  | The base class for almost all exceptions.  |
|  AttributeError | Raised when attribute reference or assignment fails.  |
|  OSError |  Raised when the operating system can’t perform a task, such as a file, for example. Has several specific subclasses. |
| IndexError  | Raised when using a nonexistent index on a sequence. Subclass of LookupError.  |
|  KeyError | Raised when using a nonexistent key on a mapping. Subclass of LookupError.  |
| NameError  |  Raised when a name (variable) is not found. |
| SyntaxError  |  Raised when the code is ill-formed. |
|  TypeError |  Raised when a built-in operation or function is applied to an object of the wrong type. |
|  ValueError |  Raised when a built-in operation or function is applied to an object with the correct type but with an inappropriate value. |
| ZeroDivisionError  |  Raised when the second argument of a division or modulo operation is zero. |

### Create custom exception class

```
class SomeCustomException(Exception): pass
```

### Catching exceptions

```
try:
    x = int(input('Enter the first number: '))
    y = int(input('Enter the second number: '))
    print(x / y)
except ZeroDivisionError:
    print("The second number can't be zero!")
```

**More than one except clause**

```
try:
   x = int(input('Enter the first number: '))
   y = int(input('Enter the second number: '))
   print(x / y)
except ZeroDivisionError:
   print("The second number can't be zero!")
except TypeError:
   print("That wasn't a number, was it?")
```

**Two exceptions with one block**

```
try:
   x = int(input('Enter the first number: '))
   y = int(input('Enter the second number: '))
   print(x / y)
except (ZeroDivisionError, TypeError, NameError):
   print('Your numbers were bogus ...')
```

**Printing error**

```
try:
    x = int(input('Enter the first number: '))
    y = int(input('Enter the second number: '))
    print(x / y)
except (ZeroDivisionError, TypeError) as e:
    print(e)
```

**Catching all**

```
try:
    x = int(input('Enter the first number: '))
    y = int(input('Enter the second number: '))
    print(x / y)
except:
    print('Something wrong happened ...')
```

**Catching all, done right**

```
try:
    x = int(input('Enter the first number: '))
    y = int(input('Enter the second number: '))
    print(x / y)
except Exception as e:
    print('Something wrong happened: %s' % (e,))
```

**Using else clause**

```
try:
   print('A simple task')
except:
   print('What? Something went wrong?')
else:
   print('Ah ... It went as planned.')
```

**Using finally clause**

```
x = None
try:
    x = 1 / 0
finally:
    print('Cleaning up ...')
    del x
```

**Combine it all**

```
try:
    1 / 0
except NameError:
    print("Unknown variable")
else:
    print("That went well!")
finally:
    print("Cleaning up.")
```

