# Square

Now we'll go back to elementary school and try to write a program
that calculates the perimeter and the area of a square.

> [note] Maths
> I hope that this won't scare anyone off
> but the word "computer" is derived from the
> word *computing*. So there's no need
> to be scared, knowledge from elementary
> school will be enough for basic programming.

The perimeter of a square with a side length of <var>a</var>
can be computed by the <var>P</var> = 4<var>a</var>
formula, and the area formula is <var>S</var> = <var>a</var>².
So let's say that our square has a side length of <var>a</var> = 356 cm.


Print the result with `print()`.
Save the program into the file <code>~/pyladies/02/sqare.py</code>
and run it; this is what it should print:

```
The perimeter of a square with a side of 356 cm is 1424 cm.
The area of a square with a side of 356 cm is 126736 cm2
```

The result should be computed by Python so don't write the
numbers 1424 and 126736 into your code. <br>
If you don't know what to do, look into your program <code>printing.py</code>
from the lesson about [`print`]({{ lesson_url('beginners/print') }}),
where one of the lines does a similar thing.

{% filter solution %}
    A program which prints the right result could look like this:

    ```python
    print('The perimeter of a square with a side of 356 cm is', 4 * 356, 'cm')
    print('The area of a square with a side of 356 cm is', 356 * 356, 'cm2')
    ```
{% endfilter %}


## Smaller square

If everything works, try to change the program
so it computes the perimeter and the area
of a square with a side of 123 cm.

{% filter solution %}
    ```python
    print('The perimeter of a square with a side of 123 cm is', 4 * 123, 'cm')
    print('The area of a square with a side of 123 cm is', 123 * 123, 'cm2')
    ```
{% endfilter %}


## Variables

Could you make it even for a side of 3945 cm, 832 cm, 956 cm?
Do you enjoy rewriting numbers?
If the program were longer (few pages)
how would you make sure that you didn't forget
to rewrite one of the numbers?

There is a way how to write a program without
rewriting all the numbers every time:
You name the side of the square and then you just
use that name. In Python, *variables* are used to name values.
They are being used this way:

```python
side = 123
print("The perimeter of a square with a side of", side,"cm is ", side * 4,"cm.")
print("The area of a square with a side of", side,"cm is", side * side, "cm2.")
```

So you write the name, then `=` and after that
the expression whose value will be *assigned*
to that variable.
When ever you write the name of the variable,
Python will use just its value.

> [style-note]
> The convention here is to put a space before and after the equals sign.

Which leads us to one of the core principles of programming:
*Don't repeat yourself*, <abbr class="initialism">DRY</abbr>.
When there is a value, an expression or the same
piece of code repeatedly, a good programmer will
name that part, and then they use the name several times.
It often happens that the program needs to be changed - either
there is a mistake or the task has changed.
And then, it is easier to make that change only in one place.

On top of that, clear names makes reading the
program much easier: `4 * side` (maybe `squareSide` would be clearer)
doesn't need any comment, but with `4 * 183`, it's not clear what
the numbers mean.


> [extra-activity]
>
> ## Circles
>
> *This is an extra task! You can skip it.*
>
> Change of the task!
> Try to expand the program so that it computes the perimeter and the area of
> a circle where the radius will be the same value as the side length from your code.
> The perimeter of a circle with radius <var>r</var>
> is <var>o</var> = 2π<var>r</var>, the area is <var>S</var> = π<var>r</var>²
> and π is approx. 3.1415926.
>
> Feel free to use more variables! It's a good practice to first calculate the result. Store it in a variable and then use it in a `print`.
>
> Name all variables appropriately.
>
> ### But wait, there's more
> Python already has some variables (or constants) defined for you. You can put `from math import pi` in the beginning of your program. Now you have a variable `pi` available, which holds the value of π. What exactly is `from math import pi`? You'll learn that during one of the future lessons! 


## Comments

Now we will make our code clearer with *comments*.
In Python, the comment begins with a Hash (Pound) sign #,
after which you can write anything until the end of the line. Everything is ignored.

Comments are important! Programs are not read only by computers, but also by other humans.
In your comments, you can include statements like: what the whole program does,
explain how a more complicated part works and clarify something
that is not clear enough.

Whenever you write a program, try to get into the role of someone who will read it,
and all that may be unclear should be specified in the comments.
Help yourself. After a few months you will not remember what the code is about.

```python
# This program computes the perimeter and the area of a square

side = 123
print("The perimeter of a square with a side of", side,"cm is ", side * 4,"cm.")
print("The area of a square with a side of", side,"cm is", side * side, "cm2.")
```

> [style-note]
> The convention is that when you write a comment on the same line
> as the code, there are two spaces or more before `#`,
> then after `#` there is one more space.


## Input

Finally, we learn how to improve the program so that we don't have to write the number 
in the program - and users can (in)put their own number.

Just like you used `print`, we will now use a different *function*
to capture user input:
We will explain the details later, for now, just remember these:

* If you want to retrieve **a text(string)**, use:

  ```python
  variable = input('Enter some text: ')
  ```

* If you want to retrieve **a whole number**, use:

  ```python
  variable = int(input('Enter some whole number: '))
  ```

* If you want to retrieve **a decimal**, use:

  ```python
  variable = float(input('Enter some decimal: '))
  ```
The text inside the parentheses can be tailored according to your needs.
It serves as the prompt for the user, so use it to ask for any needed info.

The final code might look like this:

```python
# This program computes the perimeter and the area of a sqare

side = float(input('Enter the side of a square in centimeters: '))
print("The perimeter of a square with a side of", side,"cm is ", side * 4,"cm.")
print("The area of a square with a side of", side,"cm is", side * side, "cm2.")
```
