## Modules, packages and others

Any Python program can be imported as a module. 

A simple module:

```
# hello.py
print("Hello, world!")
```

Then you can tell your interpreter where to look for the module by executing the following (using the Windows directory):

```
>>> import sys
>>> sys.path.append('C:/python')
```

Now you can import your module:

```
>>> import hello
Hello, world!
```

### Defining a function in a module

```
# hello2.py
def hello():
    print("Hello, world!")
```

Import:

```
>>> import hello2
```

The module is then executed, which means that the function hello is defined in the scope of the module, so you can access the function like this:

```
>>> hello2.hello()
Hello, world!
```

### Adding Test Code in a Module

```
# hello3.py
def hello():
    print("Hello, world!")

# A test:
hello()
```

If you import it as a module, to use the hello function in another program, the test code is executed, as in the first hello module in this chapter.

```
>>> import hello3
Hello, world!
>>> hello3.hello()
Hello, world!                                                                              
```

This is not what you want. The key to avoiding this behavior is checking whether the module is run as a program on its own or imported into another program. To do that, you need the variable __name__.

```
>>> __name__
'__main__'
>>> hello3.__name__
'hello3'
```

Correct version:

```
# hello4.py

def hello():
    print("Hello, world!")

def test():
    hello()

if __name__ == '__main__': test()
```

If you run this as a program, the hello function is executed; if you import it, it behaves like a normal module.

```
>>> import hello4
>>> hello4.hello()
Hello, world!
```

### Make your module available

You have to put your modules to the right place:

```
>>> import sys, pprint
>>> pprint.pprint(sys.path)
['',
 '/usr/local/Cellar/python/3.7.0/Frameworks/Python.framework/Versions/3.7/lib/python37.zip',
 '/usr/local/Cellar/python/3.7.0/Frameworks/Python.framework/Versions/3.7/lib/python3.7',
 '/usr/local/Cellar/python/3.7.0/Frameworks/Python.framework/Versions/3.7/lib/python3.7/lib-dynload']
```

Place your hello script to one of the site-packages directory and try to import module again.

### Telling the Interpreter Where to Look

Use environment variable PYTHONPATH.

```
export PYTHONPATH=$PYTHONPATH:∼/python
```

## PACKAGES

To structure your modules, you can group them into packages. A package is basically just another type of module. The interesting thing about them is that they can contain other modules.

While a module is stored in a file (with the file name extension .py), a package is a directory. To make Python treat it as a package, it must contain a file named __init__.py.

Simple example:


|  File/Directory | Description  |
|---|---|
| ∼/python/  |  Directory in PYTHONPATH |
| ∼/python/drawing/  | Package directory (drawing package)  |
| ∼/python/drawing/__init__.py  |  Package code (drawing module) |
|  ∼/python/drawing/colors.py |  colors module |
|  ∼/python/drawing/shapes.py |  shapes module |


Now we can do following:

```
import drawing             # (1) Imports the drawing package
import drawing.colors      # (2) Imports the colors module
from drawing import shapes # (3) Imports the shapes module
```

### Using dir()

To find out what a module contains, you can use the dir function , which lists all the attributes of an object (and therefore all functions, classes, variables, and so on, of a module). If you print out dir(copy), you get a long list of names. 

```
>>> import copy
>>> [n for n in dir(copy) if not n.startswith('_')]
['Error', 'PyStringMap', 'copy', 'deepcopy', 'dispatch_table', 'error', 'name', 't', 'weakref']
```

### Help and documentation

```
>>> help(copy.copy)
Help on function copy in module copy:

copy(x)
    Shallow copy operation on arbitrary Python objects.

    See the module's __doc__ string for more info.
```

This tells you that __copy__ takes a single argument x and that it is a "shallow copy operation."


```
print(range.__doc__)
range(stop) -> range object
range(start, stop[, step]) -> range object

Return an object that produces a sequence of integers from start (inclusive)
to stop (exclusive) by step.  range(i, j) produces i, i+1, i+2, ..., j-1.
start defaults to 0, and stop is omitted!  range(4) produces 0, 1, 2, 3.
These are exactly the valid indices for a list of 4 elements.
When step is given, it specifies the increment (or decrement).
```

### Source code

If you want to find source code of the script on filesystem, try following:

```
>>> print(copy.__file__)
/usr/local/Cellar/python/3.7.0/Frameworks/Python.framework/Versions/3.7/lib/python3.7/copy.py
```

## The standard library

### sys

The sys module gives you access to variables and functions that are closely linked to the Python interpreter.

| Function/Variable  |  Description |
|---|---|
|  argv |  The command-line arguments, including the script name |
|  exit([arg]) |  Exits the current program, optionally with a given return value or error message |
| modules  |  A dictionary mapping module names to loaded modules |
|  path |  A list of directory names where modules can be found |
| platform  | A platform identifier such as sunos5 or win32  |
| stdin | Standard input stream—a file-like object |
| stdout | Standard output stream—a file-like object |
| stderr| Standard error stream—a file-like object |


### os

| Function/Variable  | Description  |
|---|---|
| environ  | Mapping with environment variables  |
| system(command)  |  Executes an operating system command in a subshell |
| sep  |  Separator used in paths |
| linesep  | Line separator ('\n', '\r', or '\r\n')  |
| urandom(n)  | Returns n bytes of cryptographically strong random data  |

