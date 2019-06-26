# RHMCTS



Final project of FDU DATA130008, AI (artificial intelligence) in 2019 spring semester.

Group members: 张奕朗, 谢炳辉.

Algorithm: Restricted Heuristic Monte Carlo Tree Search.

### Basic ideas

To start with, we choose original Monte Carlo Tree Search as our basic algorithm. 

<img src="/images/1.gif" style='zoom:80%'>

After trying with it, we found that  MCTS has some disadvantages that could and should get improved:

- The width of the tree is so wide if without any constraints since the board is so large.
- Default policy in the simulation stage is random selection, while the sample space is so large that it needs tremendous times of simulations to converge to the true winning distribution.
- With the above two reasons, original MCTS is so slow to meet the time limit of our gomoku game.
- The tree policy in the selection stage seems to be a little short-sighted.

To overcome these deficiencies, we modify the original MCTS in the following two aspects:

- Limit the width of the tree by only expanding some of the nodes which have higher winning probabilities or scores than a threshold.
- Add some heuristic knowledge to guide the simulation policy to “directed walking” instead of “random walking” (The is a little like the change from UCS to A* search). 
- Deepen the tree as much as possible to “look ahead”.



### Algorithm

<img src="/images/2.jpg" style='zoom:80%'>

**0. Heuristic**

If the state satisfies some specific heuristic knowledge, which would leads to winning or avoid losing, we would directly apply it. The following are heuristics we have adopted:

<img src="/images/3.png" style='zoom:50%'>

- Heuristic 1: If we have 4 pieces in a continous line of 5 grids and have at least 1 empty place for the fifth piece, we’ll place our piece there for winning.
- Heuristic 2: If our opponent has 4 pieces in a continous line of 5 grids and have at least 1 empty place for the fifth piece, we’ll place our piece there to block him.
- Heuristic 3: If we have 3 pieces in the central 4 grids (the rest one is empty) of a continous 6 grids whose two heads are empty, we’ll place our piece there to block him.
- Heuristic 4: If our opponent have 3 pieces in the central 4 grids (the rest one is empty) of a continous 6 grids whose two heads are empty, we’ll put our piece in the center or on the head to block him. But which of the actions to take here is determined by the scores of actions (we select one action to block with probabilities in proportion to their scores which are get by our board evaluation function).
- Heuristic 5: If there is “double 3”, make it or block your opponent to become “double 4” (see details in figure above and in our codes).
- Heuristic 6: If there is “one 3 and one 2”, make it or block your opponent to become “one 4 and one 3”.
- Heuristic 6: If there is “double 2”, make it or block your opponent to become “double 3”.



##### 1. Selection

Start from the root node, search along the highest U value (adjusted UCB value to keep a balance between exploration and exploitation) until a leaf node.

- If this leaf node is a termination node, do **backpropagation** with leaf value of 1 (for winning) or 0 (for tie).
- If this leaf node is not a termination node, do **expansion**.



##### 2. Expansion

Expand the selected leaf node with the best n actions selected by our `policy_evaluation_function`, then do **simulation** for all expanded subnodes. And it should be stressed that if current state satisfies our **heuristic**, we’ll expand corresponding substates to get winning or avoid losing.

*Note*: we decide to expand *n* actions here for the following 2 reasons:

- It’s faster than expanding 1 action. In the case of expanding 1 action, the max U value seems to change after many times of expansion. That is to say, we would expand the same node with different actions for many time. So we want to coalesce these expansion into 1 only step.
- It’s efficient than expanding all the actions. We restrict the width of Monte Carlo Tree to n with our evaluation function since there might be so many obviously useless actions.



##### 3. Simulation

Do simulation for *k* times with our `heuristic_function`, which would recognize termination early by our heuristic knowledge 1. If no heuristic to depend on, the candidate placement of piece will be generated from `simulation_evaluation_function` which is simple and fast, then one of the candidate will be chosen randomly. Nest, do **backpropagation** with the result of our simulation. Furthermore, simulation will be restricted to a certain depth for a fast enough speed.



##### 4. Backpropagation

Backpropagate from the each of the subnodes of selected leaf node to root, compute running average of Q-value. The new observed Q-value will be 1 for the winner, -1 for the loser and 0 for a tie.



##### 5. simulation_evaluation_function

If the next move can not lead to the fatal move, we need use this function to find a move which can increase the winning possibility. In order to get  a good new move which can lead to win, we need to find the possible domain and the optimal move. For most situations, the next move which can make a direct difference to the situation is the places close to the positions which have been placed by the players. So we set the possible domain of the next move as the neighboring points of the moved

No matter what the possible domain of the next move will be, it is necessary to design our heuristic function to evaluate how the situation will change after the next move. Thus we can know what's is the optimal move from the possible domain.



**6. Point evaluation**

As mentioned above, we need to know the performance of the next move. With the score function, we check the four directions (row, line, positive diagonal, oblique diagonal) of the new move and score the line if it satisfies certain patterns and sum the respective scores as the total score of the new move. 

<img src="/images/point.png" style='zoom:80%'>

And the patterns are external knowledge we collect from some Blogs. Thanks to the limited number of the patterns, we can use a dictionary to store them. 

<img src="/images/table.png" style='zoom:80%'>



**7. Board evaluation**

with point evaluation method, we can evaluate the whole board by sum of the scores of each piece. And we know we must prevent the opponent to win while we are trying to get 5 our pieces in one row. So board evaluation scores should include the defend scores and the attack scores. We use the score of the current player minus the score of the opponent to represent the total score.
$$
S = S_{defend} + S_{attack} = S_{self} - S_{opponent}
$$
When we get the scores for each candidate in the possible domain, we can give the top-K (K is a hyper-parameter) candidates with the highest scores. It is a greedy policy, but it can save us more time. Then the expansion and simulation parts will use the candidates to do the next move.



### Conclusion

We use the Monte Carlo Tree Search as our basic algorithm. And based the alogrithm, we proposed some fatal move patterns. So if we will win or loss at the next move, we will make us win or block the opponent. If we can not win or loss in the next move. We must find a place can help us win. We use the board evaluation function to evaluate the board after the possible next move. And we use greedy policy to find the candidates with the highest score. And the simulation part will simulate the next 20 steps for several times and find if we can win. Then we get a simulation score from the simulation part. The expansion part will balance the evaluation score and the simulation score to find the optimal move.



### Reference

[1] Jun Hwan Kang,Hang Joon Kim, Effective Monte-Carlo Tree Search Strategies for Gomoku AI, IJCTA, 9(10), 2016, pp. 4833-4841

[2] Junru Wanga, Lan Huangb,Evolving Gomoku Solver by Genetic Algorithm,IEEE WARTIA,2014

[3] JINXING XIE and JIEFANG DONG,Heuristic Genetic Algorithms for General Capacitated Lot-Sizing Problems,2001

[4] Louis Victor Allis,Searching for Solutions in Games and Articial Intelligence,Version 8.0 of July 1, 1994