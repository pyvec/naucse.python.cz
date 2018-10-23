# One-dimensional tic-tac-toe

You plan 1-D tic-tac-toe on a board which has one row with 20 spaces.

There are two players. 
The first player make a move by putting `x` to an empty space.
The second player puts `o`. Then the first player plays again.

For example:
1. move: `-------x------------`
2. move: `-------x--o---------`
3. move: `-------xx-o---------`
4. move: `-------xxoo---------`
5. move: `------xxxoo---------`
   
They player who puts three same symbols next to each other wins.

## Assignment 1

Write a function `evaluate` that gets a string with the board of 1D tic-tac-toe
and returns one character based on the state of the game:

- `"x"` – The player who uses crosses (Xs) wins (the board contains `xxx`)
- `"o"` – The player who uses noughts (Os) wins (the board contains `ooo`)
- `"!"` – Draw (the board is full but nobody wins)
- `"-"` – Otherwise (i.e. the game is not finished)

## Assignment 2

Write a move function that gets a string with a game field, a field number (0-19),
and a (x or o) symbol and returns a game field (i.e., a string with a given symbol located on the given position.
The function header should look something like this:

```python
def move(field, symbol, symbol):
    # Returns a game field with a given symbol on the given position
    ...
```

## Assignment 3

Write a player_move function, which gets a string with a game field, asks the player 
to which position he wants to play,
and returns the game field with the player's move. The function should reject 
negative or too large numbers and moves to an occupied position. If user enters wrong 
argument, the function should ask again.

## Assignment 4

Write a pc_move function that gets a string with the game field.
It will select a position to play, and returns
the game field with computer's move.<br>
Use a simple random "strategy":
* Select random number from 0 to 19.
* If the position is empty put computer's symbol there.
* If not, repeat from the first step (random number).
The function header should look something like this:

```python
def pc_move(field):
    # Returns a game field with computer move
    ...
```


## Assignment 5

Write a 1D_tictactoe function that creates a string with a game field and alternately calls the player_move and
pc_move functions until someone wins or draws.
Do not forget to check the status of the game after every turn.

##### Can you program a better strategy for your computer? 