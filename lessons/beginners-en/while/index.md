# While

In addition to the `for` loop, we have a second type of loop, namely, the `while` loop.
Unlike `for`, where we *know the number of repetitions* in advance, `while` is used when the 
loop depends on some condition. The loop body is repeated until the condition is met.

```python
response = input('Say aaa!')
while response != 'aaa':
	print('Incorrect, try again')
	response = input('Say aaa!')
```

But pay attention! It is very easy to write a loop with a condition that is always true.
This kind of loop will be repeated forever.

```python
from random import randrange

while True:
    print('The number is', randrange(10000))
    print('(Wait for the computer to get tired…)')
```

The program can be interrupted with
<kbd>Ctrl</kbd>+<kbd>C</kbd>.

> [note]
> This shortcut will raise an error
> and the program will end - like after every error.

Finally, we have the `break` command, that will signal the process to ‘jump out’ of the loop,
and commands after the loop will be performed immediately.


```python

while True:
    response = input('Say aaa!')
    if response == 'aaa':
        print('Good')
        break
    print('Incorrect, try again')

print('Yay and it did not even hurt')
```

The break command can only be used inside a loop (`while` or `for`), 
and if we have nested loops, it will only jump out of the one where it is used. 

```python
for i in range(10):  # Outer loop
    for j in range(10):  # Inner loop
        print(j * i, end=' ')
        if i <= j:
            break
    print()
```
`Break` will jump out of the inner loop and back to the outer loop 
when <var>i</var> is less or equal than <var>j</var>.

Back to `while`!
Can you write the following program?

## 21

* You start with 0 points
* In each round, the computer shows how many points you have, and asks if you want to continue
* If you answer ‘No’, the game ends.
* If you answer ‘Yes’, the computer ‘turns a card’ (randomly selects a number from 2 to 10)
 and adds its value to the current points.
* If you go over 21, you lose
* The aim of the game is to get as many points as possible, but you win only if you get 21.


{% filter solution %}
```python
from  random  import  randrange

sum = 0
while sum < 21:
    print('You have', sum, 'points.')
    answer = input('Turn card? ')
    if answer == 'yes':
        card = randrange(2,11)
        print("You've got number", card)
        sum = sum + card
    elif answer == 'no':
        break
    else:
        print('I do not understand! Answer "yes" or "no"' )

if sum == 21:
    print('Congratulations! You won!')
elif sum > 21:
    print('Bad luck!', sum, 'points is too much!')
else:
    print('So close! You missed', 21 - sum, 'points!')
```
{% endfilter %}
