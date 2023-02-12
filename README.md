# GomokuAI
### What is gomoku
Gomoku is a simple game, very similar to tic-tac-toe. It is played generally on a 15x15 squares board by two players. Each player has to put down it's piece and the one that gets a '5 in a row' (either vertically, horizontally or diagonally) wins!

It is a [perfect information game](https://en.wikipedia.org/wiki/Perfect_information) and has simple rules, so it was a good playground for me to experiment basic AI algorithms, heuristics and code optimization.

### Minimax algorithm
The idea of the minimax algorithm is to describe the game as having a state and two players that alternate eachother in turns. It assigns to each state a score and, since gomoku can be considered a [zero-sum game](https://en.wikipedia.org/wiki/Zero-sum_game) (meaning that the advantage of one player is equivalent to the disadvantage of the other player), one player wants to maximize the state's score (called maximizer), while the other one wants to minimize it (called minimizer). In this case the GomokuAI will be the maximizer, while the human player will be the minimizer. 

The minimax algorithm recursively explores all the future possible game states evaluating them. It represents this as a tree and as an output it suggest the current move corresponding to the higher score possible. 

The algorithm is exponential, for the first move it has 225 choices and for each of them it has to consider every possible future move, thus only for the first two moves it has to compute 225*224=50400 states. It is clearly unfeasible to compute everytime every scenario development until the end of the game, so a maximum depth has to end the recursion. Furthermore not all possible moves are meaninful in order to maximize the score, thus in the following sections will discuss ways to prune some of the possible moves.

### Alpha-beta pruning

### Nearest squares 

### Threat sequences

``` python
for i in range(10):
  doThis().test
``` 
