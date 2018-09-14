## Files

### Opening Files

You can open files with the open function , which lives in the io module but is automatically imported for you.

```
>>> f = open('somefile.txt')
```

You can specify full path to the file and some other optional arguments. In case that you are trying to open file, that doesn't exist, you will receive exception like this:

```
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
FileNotFoundError: [Errno 2] No such file or directory: 'somefile.txt'
```

### File modes

If you use open with only a file name as a parameter, you get a file object you can read from. If you want to write to the file, you must state that explicitly, supplying a mode.

| Value  | Description  |
|---|---|
| 'r'  | Read mode (default)  |
|  'w' |  Write mode |
|  'x' |  Exclusive write mode |
|  'a' |  Append mode |
|  'b' |  Binary mode |
|  't' | Text mode |
|  '+' | Read/write mode|

The default mode is 'rt', which means your file is treated as encoded Unicode text. 


### File methods

**Reading and writing**

```
>>> f = open('somefile.txt', 'w')
>>> f.write('Hello, ')
7
>>> f.write('World!')
6
>>> f.close()
```

**Partial reading**

```
>>> f = open('somefile.txt', 'r')
>>> f.read(4)
'Hell'
>>> f.read()
'o, World!'
```

**Reading from stdin**

somefile.txt file with text:

```
Welcome to this file
There is nothing here except
This stupid haiku
```

somescript.py

```
import sys
text = sys.stdin.read()
words = text.split()
wordcount = len(words)
print('Wordcount:', wordcount)
```

Command:

```
cat somefile.txt | python somescript.py
Wordcount: 12
```

### Method seek()

```
>>> f = open(r'somefile.txt', 'w')
>>> f.write('01234567890123456789')
20
>>> f.seek(5)
5
>>> f.write('Hello, World!')
13
>>> f.close()
>>> f = open(r'somefile.txt')
>>> f.read()
'01234Hello, World!89'
```

The method tell() returns the current file position.

```
>>> f = open(r'somefile.txt')
>>> f.read(3)
'012'
>>> f.read(2)
'34'
>>> f.tell()
                    5      
```

### Closing files

You should always close files before you exit the script.

* Might help to avoid keeping the file uselessly "locked" against modification in some operating systems.
* You should always close a file you have written to because Python may buffer the data you have written and the data might not be written to the file at all.

You can use try, finally:

```
# Open your file here
try:
    # Write data to your file
finally:
    file.close()
```

### With statement

```
with open("somefile.txt") as somefile:
     do_something(somefile)
```

The with statement simplifies exception handling by encapsulating common
preparation and cleanup tasks.

In addition, it will automatically close the file. The with statement provides a way for ensuring that a clean-up is always used.


**Without with statement**

```
file = open("welcome.txt")
data = file.read()
print data
file.close()  # It's important to close the file when you're done with it
```

**With with statement**

```
with open("welcome.txt") as file: # Use file to refer to the file object
   data = file.read()
   do something with data
```

### Another file methods

Let's use our somefile.txt.


**read(n)**

```
>>> f = open(r'somefile.txt')
>>> f.read(7)
'Welcome'
>>> f.read(4)
' to '
>>> f.close()
```

**read()**

```
>>> f = open(r'somefile.txt')
>>> print(f.read())
Welcome to this file
There is nothing here except
This stupid haiku
>>> f.close()
```

**readline()**

```
>>> f = open(r'somefile.txt')
>>> for i in range(3):
        print(str(i) + ': ' + f.readline(), end='')
0: Welcome to this file
1: There is nothing here except
2: This stupid haiku
>>> f.close()
```

**readlines()**

```
>>> import pprint
>>> pprint.pprint(open(r'somefile.txt').readlines())
['Welcome to this file\n',
'There is nothing here except\n',
'This stupid haiku']
```

**write(string)**

```
>>> f = open(r'somefile.txt', 'w')
>>> f.write('this\nis no\nhaiku')
13
>>> f.close()
```

>[warn] File will be overwritten!

**writelines()**

```
>>> f = open(r'somefile.txt')
>>> lines = f.readlines()
>>> f.close()
>>> lines[1] = "isn't a\n"
>>> f = open(r'somefile.txt', 'w')
>>> f.writelines(lines)
>>> f.close()
```

### Iterations

One character at a time:

```
with open('somefile.txt') as f:
    while True:
        char = f.read(1)
        if not char: break
        print('Processing:', char)
```

One line at a time:

```
with open('somefile.txt') as f:
    while True:
        line = f.readline()
        if not line: break
        print(line)    
```

Reading everything:

```
with open('somefile.txt') as f:
    for line in f.readlines():
        print(line)
```

Enother examples of iteration:

```
with open('somefile.txt') as f:
    for line in f:
        print(line)
```

```
for line in open('somefile.txt'):
    print(line)
```