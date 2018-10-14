# Comparisons

Do you still remember what an <em>operator</em> is?

In our homework, we learned some basic arithmetic operators.
When we add one more (`//`), our list will look like this:

<table class="table">
    <tr>
        <th>Symbol</th>
        <th>Example</th>
        <th>Description</th>
    </tr>
    <tr>
        <td><code>+</code>, <code>-</code>, <code>*</code>, <code>/</code></td>
        <td><code>1 + 1</code></td>
        <td>Basic arithmetic</td>
    </tr>
    <tr>
        <td><code>-</code></td>
        <td><code>-5</code></td>
        <td>Negation</td>
    </tr>
    <tr>
        <td><code>//</code>; <code>%</code></td>
        <td><code>7 // 2</code>; <code>7 % 2</code></td>
        <td>Integer division, remainder</td>
    </tr>
    <tr>
        <td><code>**</code></td>
        <td><code>3 ** 2</code></td>
        <td>Power (3 to the power of 2)</td>
    </tr>
</table>

Python also has other types of operators. *Comparison* (relational) 
operators are used to compare values.
Try out what they do!
(You can try them by using `print()` in your code,
or you can try `python`'s command line.)

<table class="table">
    <tr>
        <th>Symbol</th>
        <th>Example</th>
        <th>Description</th>
    </tr>
    <tr>
        <td><code>==</code>, <code>!=</code></td>
        <td><code>1 == 1</code>, <code>1 != 1</code></td>
        <td>equal, not equal</td>
    </tr>
    <tr>
        <td><code>&lt;</code>, <code>&gt;</code></td>
        <td><code>3 &lt; 5</code>, <code>3 &gt; 5</code></td>
        <td>greater than, less than</td>
    </tr>
    <tr>
        <td><code>&lt;=</code>, <code>&gt;=</code></td>
        <td><code>3 &lt;= 5</code>, <code>3 &gt;= 5</code></td>
        <td>Greater or equal, less or equal</td>
    </tr>
</table>

Comparison values are called *boolean* values
(after [G. Boole](http://en.wikipedia.org/wiki/George_Boole)).
They are used every time we want to know if something is `True` or `False`.
Boolean types are exactly those two - `True` and `False`.

Like all values, `True` and `False` can be assigned to variables:

```python
true = 1 < 3  # we have to type it in lowercase now, because True is a reserved word in Python
print(true)

false = 1 == 3
print(false)
```

> [note]
> Note that to test equality, you have to use two equal signs: `3 == 3`.
> One equal sign assigns a value to a variable, and two equal signs
> compare two values (of variables).

<code>True</code> and <code>False</code> 
can be used directly in a program.
Just keep an eye on capitalisation.

```python
print(True)
print(False)
```

## Conditions

{% if var('pyladies') -%}
{% set rootname = 'pyladies' %}
{%- else -%}
{% set rootname = 'naucse-python' %}
{%- endif %}

Write the following into a new file (e.g. `if.py`):

```python
side = float(input('Enter the side of a square in centimeters: '))
print("The perimeter of a square with a side of", side,"cm is ", side * 4,"cm.")
print("The area of a square with a side of", side,"cm is", side * side, "cm2.")
```

What happens when you enter a negative number? Does the output make sense?

As we can see, the computer does exactly what it is told and doesn't
think about context. You have to do that for it.
It would be nice if the program could tell the user who enters
a negative number that they entered nonsense.
How do we do that?

Let’s try to set a variable that will be `True` when a user enters a positive number.

{% filter solution %}
    You can set the variable like this:

    ```python
    side = float(input('Enter the side of a square in centimeters: '))
    positive_number = side > 0
    ```
{% endfilter %}

And then we will tell the program to use this variable. 
For that purpose we will use the `if` and `else` statements.


```python
side = float(input('Enter the side of a square in centimeters: '))
positive_number = side > 0


if positive_number:
    print("The perimeter of a square with a side of", side,"cm is", side * 4,"cm.")
    print("The area of a square with a side of", side,"cm is", side * side, "cm2.")
else:
    print("The side must be a positive number!")

print("Thank you for using the geometric calculator.")

```

So after `if`, there is a *condition* which is the
expression we'll use for the decision making.
After the condition you must write a colon (`:`).
The colon is followed by the commands to be executed, if the condition is True.
Indent the lines 4 spaces after every colon you use in Python.

Then on the same level as `if`, write `else:` followed by a colon. The next lines
contain the commands that are executed if the condition is False, and they must also be indented.<br>
Then you can write other code, not indented, that will be executed every time, because
the if statement has already ended.

> [note]
> The indentation doesn't need to be 4 spaces, you could use 
> 2 or even 11, or you can use the tabulator. The point is that
> within one block of code, the indentation has to be the same.
> So if you are working on some project with someone else, you
> have to agree on indentation for the program 
> to be able to run properly. Most of the people
> from the Python community agree on 4 spaces (or one tab).


## Other conditional statements

Sometimes the `else` statement is not necessary.
The following program does nothing extra if the number is not equal to zero.

```python
number = int(input('Enter a number, to which I will add 3: '))
if number == 0:
    print('This is easy!')
print(number, '+ 3 =', number + 3)
```

Sometimes several conditions are needed. For this situation, we have the `elif` statement
(combination of `else` and `if`). It's between `if` and `else`.
You can repeat the `elif` keyword after the first `if`, but 
only one branch will be executed, to be precise: the first true one
where the conditions are met. 


```python
age = int(input('How old are you? '))
if age >= 150:
    print('And from which planet are you?')
elif age >= 18:
    # This branch will not be executed for "200", for example.
    print('We can offer: wine, cider, or vodka.')
elif age >= 1:
    print('We can offer: milk, tea, or water')
elif age >= 0:
    print('Unfortunately, we are out of Sunar.')
else :
    # If no condition is met from above, the age had to be negative.
    print('Visitors from the future are not welcomed here!')
```

## Rock paper scissors

`If`s can be nested - after an `if` and its indentation, there can be other `if`.


```python
pc_choise = 'rock'
user_choise = input('rock, paper, or scissors?')

if user_choise == 'rock':
    if pc_choise == 'rock':
        print('Draw.')
    elif pc_choise == 'scissors':
        print ('You win!')
    elif pc_choise == 'paper':
        print ('Computer won!')
elif user_choise == 'scissors':
    if pc_choise == 'rock':
        print('Computer won!')
    elif pc_choise == 'scissors':
        print('Draw.')
    elif pc_choise == 'paper':
        print('You win!')
elif user_choise == 'paper':
    if pc_choise == 'rock':
        print('You win!')
    elif pc_choise == 'scissors':
        print('Computer won!')
    elif pc_choise == 'paper':
        print('Draw.')
else:
    print('I do not understand.')

```

Yay, your first game!<br>
Now we need to overwrite the pc_choice so it will act
randomly. We will talk about how to do this next time.