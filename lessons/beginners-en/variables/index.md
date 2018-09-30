# Square

Now we'll go back to elementary school and try to write a program 
that calculates the perimeter and the area of a square.

> [note] Maths
> I hope that this won't scare anyone off
> but the word "conputer" is derived of the
> word *computing*. So there's no need
> to be scared, knowledge from elementary
> school will be enough for the basic programming.

The perimetr of a square with side <var>a</var>
can be computed by formula <var>O</var> = 4<var>a</var>
and the area's formula is <var>S</var> = <var>a</var>².
So let's say that our square has side <var>a</var> = 356 cm.


Print the result with `print()`.
Save the program into file <code>~/pyladies/02/sqare.py</code>
and run it; this is what it should print:

```
The perimeter of a square with a side of 356 cm is 1424 cm.
The area of a square with a side of 356 cm is 126736 cm2
```

The result shoould be computed by Python so don't write the
numbers 1424 and  126736 into your code. <br>
If you don't know what to do look into your program <code>printing.py</code>
from [lesson about `print`]({{ lesson_url('beginners/print') }}), 
where one line  does the similar thing.

{% filter solution %}
    Program which will print the right result could look like this:

    ```python
    print('The perimeter of a square with a side of 356 cm is', 4 * 356, 'cm')
    print('The area of a square with a side of 356 cm is', 356 * 356, 'cm2')
    ```
{% endfilter %}


## Smaller square

If everything works try to change the program
so it would compute the perimeter and the area
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
If the program would be longer (few pages)
how would you make sure that you didn't forgot
to rewrite one of the numbers?

There is a way how to write a program without
rewriting all the numbers every time:
you will name the side and then you are just
using that name. For the names of a values 
we have *variables* in Python.
They are being used this way:

```python
side = 123
print("The perimeter of a square with a side of", side,"cm is ", side * 4,"cm.")
print("The area of a square with a side of", side,"cm is", side * side, "cm2.")
```

So you write the name then `=` and after that
the expression whose value will be *assigned*
to that variable.
When you will write the name of the variable
Python will use just its value.

> [style-note]
> The convention here is to put space berore and after equal.

Which lead us to one of the core programmer's
principle: *Don't repeat yourself*, <abbr class="initialism">DRY</abbr>.
When there is some value, some expression or same 
piece of code repeatedly, good programmer will
name that piece and then they use just that name.
Because there is a need to change something often - either
there is a mistake or the task has changed.
And it is easier to make that change only on one place.

On top of that clear names makes reading of the 
program much easier: `4 * side` (maybe `squareSide` would be clearer)
doesn't need any comment, but `4 * 183` it is not clear what
those numbers mean.


> [extra-activity]
>
> ## Circles
>
> *This is extra task! You can skip it.*
>
> Change of the task!
> Try to add computing the perimeter and the area of
> a circle where side will be radius into your code
> The perimeter of a circle with radius <var>r</var>
> is <var>o</var> = 2π<var>r</var>, the area is <var>S</var> = π<var>r</var>²
> and π is approx. 3,1415926.
>
> Name approprietly all the numbers.


## Comments

We will make our code clearer now wit *comments*
In Python, the comment begins with a Hash (Pound) sign #, 
after which you can write anything until the end of the line. Everything is ignored.

Comments are important! Programs are not read only by computers, but also by other humans.
In your comments, you can include statements like: what the whole program does,
explain how a more complicated part works amd clarify something
that is not clear enough.

Whenever you write a program, try to get into the role of someone who will read it,
and all that may be unclear should be specified in the comments.
Help yourself. After a few months you will not remember what the code is about.

```python
# This program computes the perimeter and the area of a sqare

side = 123
print("The perimeter of a square with a side of", side,"cm is ", side * 4,"cm.")
print("The area of a square with a side of", side,"cm is", side * side, "cm2.")
```

> [style-note]
> The convention is that when you are writing comment on the same line
> as the code there are two spaces or more before `#`.
> Then after `#` there is one space.


## Input

Finally we will learn how to do it so the number wouldn't have to
be written in the program - how users can (in)put it there on their own.

Just like you used `print`, we will now use different *function* 
to capture user input:
We will explain details later, for now just remember those:

* If you want to retrieve **a text(string)** use:

  ```python
  variable = input('Enter some text: ')
  ```

* If you want to retrieve **a whole number** use:

  ```python
  variable = int(input('Enter some whole number: '))
  ```

* If you want to retrieve **a decimal** use:

  ```python
  variable = float(input('Enter some decimal: '))
  ```
The text inside the parentheses can be tailored according to your needs. 
It serves as the prompt for the user, so use it to ask for needed info.

Final code can look like this:

```python
# This program computes the perimeter and the area of a sqare

side = float(input('Enter the side of a square in centimeters: '))
print("The perimeter of a square with a side of", side,"cm is ", side * 4,"cm.")
print("The area of a square with a side of", side,"cm is", side * side, "cm2.")
```
