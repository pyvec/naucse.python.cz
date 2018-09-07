## Abstraction - Functions

In Python, function is a group of related statements that perform a specific task.

Functions help break our program into smaller and modular chunks. As our program grows larger and larger, functions make it more organized and manageable.

Furthermore, it avoids repetition and makes code reusable.

A function is something you can call (optionally with some parameters). Function is providing some action and returns some value.

In Python we can declare function like this:


```
def name(parameter1, parameter2,...):
	body
```

Simple example:

```
def hello(name):
     return 'Hello, ' + name + '!'
```

Function hello returns string with a greeting and name given as a parameter.
We can call this function like this:

```
>>> print(hello('world'))
Hello, world!
>>> print(hello('Peter'))
Hello, Peter!
```

### Documenting functions

You should document your functions, so you (or others!) will later understand, what is the purpose of the functon, which parameters areaccepting and what value returns.

How to document functions? If you put the documentation string on the line below the function declaration, you will create so called *docstring*.

```
def multiple(x):
    'Multiplication of the number x.'
    return x * x
```

You can then access the documentation of the function like this:

```
>>> def multiple(x):
...     'Multiplication of the number x.'
...     return x * x
...
>>> multiple.__doc__
'Multiplication of the number x.'
```

> [note] __doc__ is a function attribute.

### The return statement

The return statement is used to exit a function and go back to the place from where it was called.

Syntax:

```
return [expression_list]
```

### Types of Functions

**Build-in**

chr()	-	Returns a Character (a string) from an Integer

dict()	-	Creates a Dictionary
...

**User-defined**

User-Defined Functions (UDFs). All the other functions that we write on our own fall under user-defined functions. So, our user-defined function could be a library function to someone else.

**Anonymous functions**

Also called lambda functions, because they are not declared with the standard def keyword.

### Parameters

Your function should do its job with supplied (correct) parameters and fails if the parameters are wrong.

Assigning a new value to a parameter inside a function won't change the outside code.

```
>>> def try_change_variable(n):
...  n = 'Hello World'
...
>>> name = 'Hello Tieto'
>>> try_change_variable(name)
>>> name
'Hello Tieto'
```

> [note] Parameters are in *local scope*.

> [warning] Please be careful about changing mutable data structure:
> 
> ```
> >>> def change(n):
> ...  n[0] = 'Mr. Foo'
> ...
> >>> names = ['Mr. Bar', 'Mr. Baz']
> >>> change(names)
> >>> names
> ['Mr. Foo', 'Mr. Baz']
> ```

**There are four types of arguments that Python UDFs can take:**

* Default arguments
* Required arguments
* Keyword arguments
* Variable number of arguments

#### Default arguments

Default arguments are those that take a default value if no argument value is passed during the function call. You can assign this default value by with the assignment operator =, just like in the following example:

```
def plus(a, b=2):
  return a + b
  
# Call `plus()` with only `a` parameter
plus(a=1)

# Call `plus()` with `a` and `b` parameters
plus(a=1, b=3)
```

#### Required arguments

The required arguments of a UDF are those that have to be in there. These arguments need to be passed during the function call and in exactly the right order, just like in the following example:

```
def plus(a, b):
  return a/b
```

#### Keyword Arguments

If you want to make sure that you call all the parameters in the right order, you can use the keyword arguments in your function call. You use these to identify the arguments by their parameter name.

```
def  hello_1(greeting, name):
     print('{}, {}!'.format(greeting, name))
```

```
>>> hello_1(greeting='Hello', name='world')
Hello, world!
>>> hello_1(name='world', greeting="Hello")
Hello, world!
```

### Variable Number of Arguments

In cases where you don’t know the exact number of arguments that you want to pass to a function, you can use the following syntax with *args:

```
# Define `plus()` function to accept a variable number of arguments
def plus(*args):
  return sum(args)

# Calculate the sum
>>> plus(1,4,5)
10
```

### Usage of *args


*args and **kwargs are mostly used in function definitions. *args and **kwargs allow you to pass a variable number of arguments to a function. What does variable mean here is that you do not know before hand that how many arguments can be passed to your function by the user so in this case you use these two keywords. *args is used to send a non-keyworded variable length argument list to the function.

```
def test_var_args(f_arg, *argv):
    print "first normal arg:", f_arg
    for arg in argv:
        print "another arg through *argv :", arg

test_var_args('yasoob','python','eggs','test')
```

```
first normal arg: yasoob
another arg through *argv : python
another arg through *argv : eggs
another arg through *argv : test
```

### Usage of **kwargs

\**kwargs allows you to pass keyworded variable length of arguments to a function. You should use \**kwargs if you want to handle named arguments in a function. 

```
def greet_me(**kwargs):
    if kwargs is not None:
        for key, value in kwargs.iteritems():
            print("%s == %s" %(key,value))
```

```
>>> greet_me(name="yasoob")
name == yasoob
```

### Global vs Local Variables
In general, variables that are defined inside a function body have a local scope, and those defined outside have a global scope. That means that local variables are defined within a function block and can only be accessed inside that function, while global variables can be accessed by all functions that might be in your script:

```
# Global variable `init`
init = 1

# Define `plus()` function to accept a variable number of arguments
def plus(*args):
  # Local variable `sum()`
  total = 0
  for i in args:
    total += i
  return total
  
# Access the global variable
print("this is the initialized value " + str(init))

# (Try to) access the local variable
print("this is the sum " + str(total))
```

### Anonymous Functions

Anonymous functions are also called lambda functions in Python because instead of declaring them with the standard def keyword, you use the lambda keyword.

```
double = lambda x: x*2

double(5)
```

Another example of lambda function:

```
# `sum()` lambda function
sum = lambda x, y: x + y;

# Call the `sum()` anonymous function
sum(4,5)

# UDF equivalent
def sum(x, y):
  return x+y
```

#### Using main() as a Function

In many programming languages, main function is required in order to execute functions. Not in Python, but you might want to write code like this:

```
# Define `main()` function
def main():
  hello()
  print("This is a main function")
  
# Execute `main()` function 
if __name__ == '__main__':
    main()
```