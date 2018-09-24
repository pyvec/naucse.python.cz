# Functions
In the previous [lesson]({{ lesson_url('beginners/functions') }}) 
we were working with functions that were written by someone else - they are
already built-in in Python.


```python
from math import pi

print(pi)
```

Today we will learn how to code our own functions
which will be helpful when we need to run tasks repeatedly. 

It's not hard:


```python
def  find_perimeter( width ,  height ): 
    "Returns the rectangle's perimeter of the given sides" 
    return  2 * (width  +  height)

print ( find_perimeter(4 ,  2))

```

How does it work?

You *define* a function with the command `def`. Right after that
you have to write name of the function, parentheses (which may contain 
*arguments*) and then, of course, a colon. 

We have already said that after a colon, everything that 
belongs to (in our case) the function must be indented. 
The indented code is called *function body* and it contains 
the commands that the function performs. 
In the body you can use various commands including `if`, `loop`, etc.

The body can start with a *documentation comment* which describes what
the function is doing.

A function can return a value with the `return` command.


```python
def  print_score(name, score): 
    print (name, 'score is', score) 
    if score > 1000:
        print('World record!') 
    elif score > 100: 
        print('Perfect!') 
    elif score > 10: 
        print('Passable.') 
    elif score > 1: 
        print('At least something. ') 
    else: 
        print('Maybe next time. ')

print_score('Your', 256) 
print_score('Denis', 5)

```

When you call a function, the arguments you write in parentheses
are assigned to the corresponding variables in the function definition's
parentheses.
So when you call our new function with `print_score('Your', 256)`,
imagine that, internally, it assigns the values like this:


```python
name = 'Your'
score = 256

print (name, 'score is', score) 
if score > 1000:
    ... #etc.
        
```
## Return

The `return` command *terminates* the function and returns the calculated value 
out of the function. You can use this command only in functions.

It behaves similar to the `break` command that terminates loops.


```python
def yes_or_no(question):
    "Returns True or False, depending on the user's answers."
    while True:
        answer = input(question)
        if answer == 'yes':
            return True
        elif answer == 'no':
            return False
        else:
            print('What do you want!! Just  type "Yes" or "No".')

if yes_or_no('Do you want to play a game?'):
    print('OK, but you have to program it first.')
else:
    print('That is sad.' )

```

> [note]
> Same as `if` and `break`, `return` is a *command*, not a function.
> That's why `return` has no parentheses after it.

Try to write a function that returns the area of an ellipse with given 
dimensions.
The formula is <var>A</var> = π<var>a</var><var>b</var>,
where <var>a</var> and <var>b</var> are the lengths of the axes.
Then call the function and print the result.

{% filter solution %}
```python
from math import pi

def ellipse(a, b): 
    return pi * a * b
    
print('The ellipsis area with 3 cm and 5 cm axes length is', ellipse(3, 5),'cm2.')

```
{% endfilter %}


### Return or print?

The last program could be also written like that:

```python
from math import pi

def ellipse(a, b): 
    print('The area is', pi * a * b) # Caution, 'print' instead of 'return'!
    
ellipse(3, 5)

```

The program works this way, too. But it loses one of the main advantages
that functions have - when you want to use the value differently than to `print` it.

A function that *returns* its result can be used as part of other calculations:


```python
def elliptical_cylinder(a, b, hight):
    return ellipse(a, b) * hight

print(elliptical_cylinder(3, 5, 3))
```

But if our ellipse function just *printed* the result, we wouldn't be
able to calculate the area of elliptical cylinder this way.

The reason why `return` is better than `print` is that a function
can be re-used in many different situations. When we don't actually
want to know the intermediate results, we can't use functions with `print`. 

Using `return`, we can re-use the same function, for example, in graphic games, 
web applications, or even to control a robot.

It is similar with input: If I hardcoded `input` into a function, I could use
it only in situations where there's a user with keyboard present.
That's why it's always better to pass arguments to a function, and call
`input` outside of the function:

```python
from  math import pi

def ellipse(a, b): 
    """This reusable function returns only the result - the ellipse's area with a and b axes"""
    #This is only the calculation
    return pi * a * b
    
#print and input are "outside" the reusable function!
x = input('Enter length of 1st axis: ')
y = input('Enter length of 2nd axis: ')
print('The ellipsis area is', ellipse(x, y),'cm2.')
```

There are of course exceptions: A function that directly generates 
a text can be written with `print`, or a function that processes text information.
But when the function calculates something it's better to not have
`print` and `input` inside it.


## None

When the function does not end with an explicit `return`,
the value that it returns is automatically `None`.

`None` is a value that is already "inside" Python (same as `True` and `False`).
It's literally "none, nothing".

```python
def nothing():
    "This function isn't doing anything."

print(nothing())
```


## Local variables

Congratulations! You can now define your own functions!
Now we have to explain what local and global variables are.

A function can use variables from "outside":

```python
pi = 3.1415926  # a variable defined outside the function

def circle_area(radius):
    return pi * radius ** 2

print(circle_area(100))
```

But every variable and argument that is defined within the function body are
*brand new* and they share nothing with "outside" code.

Variables that are defined inside a function body are *local variables*,
because they work only locally inside the function.
For example, the following won't work how you would expect:

```python
x = 0  # Assign value to global variable x

def set_x(value):
    x = value  # Assign value to local variable x

set_x(40)
print(x)
```

Variables that are not local are *global variables* -
they exist throughout the whole program. But if a function defines
a local variable with the same name, this local variable will only  
have the value that was assigned within the function.

Let's look at an example.
Before you run the next program, try to guess how it will behave.
Then run it, and if it did something different than
you expected, try to explain why.
There is a catch! :)

```python
from math import pi
area = 0
a = 30

def ellipse_area(a, b):
    area = pi * a * b  # Assign value to 'area`
    a = a + 3  # Assign value to 'a`
    return area

print(ellipse_area(a, 20))
print(area)
print(a)
```

Now try to answer the following questions:

* Is the variable `pi` local or global?
* Is the variable `area` local or global?
* Is the variable `a` local or global?
* Is the variable `b` local or global?


{% filter solution %}
* `pi` is global - it's not defined within the function and it's
accessible in the whole program.
* `area` - Note there are two variables of that name! One is global
ant the other one is local inside the function `ellipse_area`.
* `a` - Note there are also two variables of that name. This was that catch:
Writing `a = a + 3` has no point. A value is assigned to the local
variable `a`, but the function ends right after that, and this `a` is no 
longer available, it will never be used.
* `b` is only local - it's an argument for the `ellipse_area` function. 

{% endfilter %}

If it seems confusing and complicated just avoid naming variables (and
function's arguments) within a function the same as those outside.
