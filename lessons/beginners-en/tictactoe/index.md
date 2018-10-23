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
and a (x or o) symbol and returns
a game array (i.e., a string) with a given symbol located on the given position.
The function header should look something like this:
def drag (field, symbol, symbol):
"Returns a game field with a given symbol on the given position"


## Assignment 3

TBD

## Assignment 4

TBD

## Assignment 5

TBD