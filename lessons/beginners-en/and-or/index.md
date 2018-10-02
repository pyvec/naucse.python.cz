
# *Or* & *and*

In addition to the operators that we saw in the Comparison lesson, we will now add 3 more logical (Boolean) operators to the table:

<table class="table">
    <tr>
        <th>Symbol</th>
        <th>Example</th>
        <th>Description</th>
    </tr>
    <tr>
        <td><code>and</code></td>
        <td><code>x and y</code></td>
        <td>True if both operands are true</td>
    </tr>
    <tr>
        <td><code>or</code></td>
        <td><code>x or y</code></td>
        <td>True if either operand is true</td>
    </tr>
    <tr>
        <td><code>not</code></td>
        <td><code>not x</code></td>
        <td>True if the operand is false<br> 
        (it negates the operand)</td>
    </tr>
</table>



```python
# This program gives naive life advice.

print('Answer "yes" or "no".')
happy_status = input('Are you happy?')
if happy_status == 'yes':
    happy = True
elif happy_status == 'no':
    happy = False
else:
    print('I do not understand!')

rich_status = input('Are you rich?')
if rich_status == 'yes':
    rich = True
elif rich_status == 'no':
    rich = False
else:
    print('I do not understand!')

if rich and happy:
    # rich and at the same time.
    print('Congratulations!')
elif rich:
    # rich but not "rich and happy",
    #so must be only rich.
    print('Try to smile more.')
elif happy:
    # must be only happy.
    print('Try to spend less.')
else:
    # neither happy nor rich.
    print("I'm sorry for you.")

```

> [note]
> What happens if you answer something other than "Yes" or "No"?
>
> The variables `happy` and `rich` won't be set, and later when they are needed, the program will end with an error.
>
> We will learn how to handle errors [next time]({{ lesson_url('beginners/exceptions') }}).
