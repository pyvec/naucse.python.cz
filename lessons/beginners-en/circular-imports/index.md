## Circular imports

In the 1D tic-tac-toe game for your homework, you will probably write several modules.
It will look like this:
(Arrows between modules are showing the imports.)

```plain
┌──────────────────╮ ┌───────────────╮  ┌──────────────────╮ 
│      ai.py       │  │ tictactoe.py  │   │    game.py       │
├──────────────────┤  ├───────────────┤   ├──────────────────┤
│                  │◀-│ import ai     │◀-│import tictactoe  │
├──────────────────┤  ├───────────────┤   ├──────────────────┤
│ def ai_move      │  │ def evaluate  │   │                  │
│                  │  │ def move      │   │                  │
└──────────────────┘  │def player_move│   └──────────────────┘
                      │               │
                      └───────────────┘
                          ▲
                          │
                          │ ┌───────────────────╮
                          │ │ test_ticktactoe.py│
                          │ ├───────────────────┤
                          └─│ import tictactoe  │
                            ├───────────────────┤
                            │ def test_...      │
                            │                   │
                            └───────────────────┘
```

But function `ai_move` needs to call function `move`.<br>
What can we do?<br>
Could you import `ai` from `tictactoe` while you are importing `tictactoe` from `ai`?


```plain
┌──────────────────╮ ┌───────────────╮
│      ai.py       │  │ tictactoe.py  │
├──────────────────┤  ├───────────────┤
│                  │◀-│ import ai     │
│import ticktaktoe │-▶│               │
│                  │  │               │
│   def ai_move    │  │ def evaluate  │
│                  │  │ def move      │
└──────────────────┘  │def player_move│
                      │               │
                      └───────────────┘  
```
We can look at it from the point of view of Python,
which is executing the commands.
When it has to import `tictactoe.py`, it process the file line by line.
And it almost at the begging see command `import ai`.
So it opens file `ai.py` and it start to process it line by line.
And of course it will soon get to `import tictactoe`. What next?

To avoid an infinite loop - one file would import another one and this one would import
the first one over and over again - 
Python will make some workaround when we run `tictactoe`:
when it notices that `tictactoe` is already being imported in `ai.py`,
it will import the part of `tictactoe` that it's just before `import ai` into `ai` module
and this will replace line `import tictactoe` so it's no longer there. And then it can continue the
import of `ai` in `tictactoe.py`.
When it finishes this import it will continue in `tictactoe` and all its functions and commands.

This could be useful but in most of the times it behaves very unpredictable therefore it's dangerous.

In other words: when two modules are trying to import the other one
the program doesn't have to work as expected.

We want to prevent this kind of situation.

How will we do it? We have two options.


## Organise modules by dependency

First option is to move function `move` to module `ai` and we can use it from there.
That's easy but that's not what we wont from `ai` module, because it should contain
the logic how our "AI" is choosing where to move only.
It definitely shouldn't contain other functions which might be useful somewhere else.


```plain
┌──────────────────╮ ┌───────────────╮
│      ai.py       │  │ tictactoe.py  │
├──────────────────┤  ├───────────────┤
│                  │◀-│ import ai     │
│                  │  │               │
│ def ai_move      │  │ def evaluate  │
│ def move         │  │def player_move│
│                  │  │               │
└──────────────────┘  └───────────────┘
```

## Support module

Second option is to define new module which will be used in
`tictactoe.py` and in `ai.py`.

This module is usually as `util.py` (=utility).


```plain
              ┌──────────────────╮
              │ util.py          │
              ├──────────────────┤
              │ def move         │
              └──────────────────┘
                      ▲  ▲
                      │  │
┌──────────────────╮ │  │  ┌───────────────╮
│      ai.py       │  │  │  │ tictactoe.py  │
├──────────────────┤  │  │  ├───────────────┤
│ import util      │──┘  └──│ import util   │
│                  │◀───────│ import ai     │
│                  │        │               │
│ def ai.move      │        │ def evaluate  │
│                  │        │def player_move│
│                  │        │               │
└──────────────────┘        └───────────────┘
```

Disadvantage of support module is that it can easily 
become non-maintained storage of your code, which you used on so
many places that you have no idea where exactly you used it and whether 
you can modify or delete it.

What you should choose always depends on the current situation.
