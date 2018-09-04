## Conditionals, Loops

### Import statement

Typical import:

```
import something
```

or

```
from somemodule import somefunction
```

or 

```
from somemodule import somefunction, anotherfunction
```

or

```
from somemodule import *
```

or

```
from somemodule import somefunction as different_name
```

### Boolean values

False:

```
False    None    0    ""    ()    []    {}
```

True:

```
True	1	"Some string"	(1, 2)  [1, 2]  {1: 'One'}
```

### if-elif-else

Most common decision construction is *if-elif-else*.


```
if condition1:
	body1
elif condition2:
	body2
elif condifion3:
	body3
.
.
.
elif condition(n-1)
	body(n-1)
else:
	body(n)
```

Examples:

```
num = int(input('Enter a number: '))
if num > 0:
    print('The number is positive')
elif num < 0:
    print('The number is negative')
else:
    print('The number is zero')
```

Example with pass:

```
if x < 5:
	pass
elif x > 5:
	pass
else:
	x = 5
```

Nested block example:

```
name = input('What is your name? ')
if name.endswith('Gumby'):
    if name.startswith('Mr.'):
        print('Hello, Mr. Gumby')
    elif name.startswith('Mrs.'):
        print('Hello, Mrs. Gumby')
    else:
        print('Hello, Gumby')
else:
    print('Hello, stranger')
```

### Comparison Operators


|Expression   | Description  |
|---|---|
|x == y   |x equals y   |
| x < y  |  x is less than y |
|  x > y |  x is greater than y |
| x >= y  | x is greater than or equal to y  |
|  x <= y |  x is less than or equal to y |
|  x !=  y |  x is not equal to y |
|  x is y |x and y are the same object|
| x is not y  |  x and y are different objects |
|x in y|  x is a member of the container (e.g., sequence) y |
|  x not in y |  x is not a member of the container (e.g., sequence ) y |


**is: The identity operator**

```
>>> x = y = [1, 2, 3]
>>> z = [1, 2, 3]
>>> x == y
True
>>> x == z
True
>>> x is y
True
>>> x is z
False
```


### Loops

#### while loops

```
while condition:
	body
else: # optional
	code continuation
```

Example:

```
x = 1
while x <= 100:
    print(x)
    x += 1
```

#### for loops

```
for variable in sequence:
	body
else: # optional
	code continuation
```


Example:

```
numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
for number in numbers:
    print(number)
```

#### range() function

Function range can be used in combination with len and for loop like this:

```
>>> x = [1, 2, 3, -7, 5, 10, -5, 4]
>>> for i in range(len(x)):
...  if x[i] < 0:
...    print("Negative number on index ", i)
...
Negative number on index  3
Negative number on index  6
```

```
>>> range(10)
range(0, 10)
```

The following program writes out the numbers from 1 to 100:

```
for number in range(1,101):
    print(number)
```

Iterating over dictionaries:

```
d = {'x': 1, 'y': 2, 'z': 3}
for key, value in d.items():
    print(key, 'corresponds to', value)
```

#### Breaking out of loop

**break**

To end (break out of) a loop, you use break.

```
>>> x = 1
>>>
>>> while True:
...   x += 1
...   if x == 10:
...     break
...   else:
...     print("Value is ", x)
...
Value is  2
Value is  3
Value is  4
Value is  5
Value is  6
Value is  7
Value is  8
Value is  9
```

**continue**

It causes the current iteration to end and to “jump” to the beginning of the next.

```
>>> x = 1
>>>
>>> while True:
...   x += 1
...   if x < 10:
...     continue
...   else:
...     print("x has the value ", x)
...     break
...
x has the value  10
```