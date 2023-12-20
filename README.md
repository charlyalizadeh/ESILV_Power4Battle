# Automatic battle

Code to automate the battle between different IA.

## Usage

You only need `numpy`.
Then run `python battle.py`.

## Format

If you want to test that your IA is working with this code clone this directory and copy your code inside a directory with
the name of your group. Inside this directory you must have a file called `minimax.py` and another called `__init__.py`.

```
.
├── battle.py
├── *YOUR CODE DIRECTORY*
│   ├── __init__.py
│   └── minimax.py
└── README.md
```

`minimax.py` must contains the following functions:

* `def init()`: a function to do everything you need before the start of the battle
* `def minimax_play()`: play a move with the current board situation and return the action played (you must use a global variable for the board)
* `def opponent_play(action)`: apply the opponent move to your board

`action` must be a tuple with:
  - action[0]: the row coordinate
  - action[1]: the column coordinate

If you did everything right you can just copy and paste the template of `__init__.py` inside your code directory.

If your code doesn't comply with this format your grade will be divided by 2.

If you have any question please send a mail to: charly.alizadeh@ext.devinci.fr

Good Luck!

## Common error

* `AttributeError: module 'YOUR DIRECTORY' has no attribute 'minimax'`: You must copy `__init__.py` inside your directory and have a `minimax.py` file
* `AttributeError: module 'YOUR DIRECTORY.minimax' has no attribute 'init'` (or `minimax_play` or `opponent_play`): You must have the function `init`, `minimax_play` and `opponent_play` inside the `minimax.py` file
