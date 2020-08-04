# First-Games
Games Coding Practice

Current Games:
(finished)

Tetris - Python & JavaScript

Rules:
Left / Right key for going left / right, space key for rotation, in JS pressing Down key can instantly going down, not in Python version.
Can customize Gamesize, split (how many boxes in one line) and difficulty according to the commented rules.

Known issues: 
In Python version, the speed up function is used by taking log of the scores that player currently has, which makes it behave badly when score reaches certain threshold (it suddenly speeds up too fast); in JS version this function is removed since the speed up needs to be calculated by frame rate, which must be an int, and when frame rate is below 4 game becomes unplayable (too fast). 
Also in JS, holding space key will result in the system infinitely rotate and makes the "hit" function operators in a weird way, it may possibly calculates the wrong hit point (where the rotation is not done, but "hit" calculates the position when it rotates), so do not hold space key, just press it. Same should go for left/right key but did not encounter any issue for this so far.
