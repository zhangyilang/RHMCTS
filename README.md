# RHMCTS



Final project of FDU DATA130008, AI (artificial intelligence) in 2019 spring semester.

Group members: 张奕朗, 谢炳辉.

Algorithm: Restricted Heuristic Monte Carlo Tree Search.



### Algorithm

##### 1. Selection

Start from the root node (each node is a Q-state for current player), search along the highest U value (adjusted UCB value to keep a balance between exploration and exploitation) until a leaf node.

-  If this leaf node is a termination node, do **backpropagation** with leaf value of 1 (for winning) or 0 (for tie).
-  If this leaf node is not a termination node, do **expansion**.



##### 2. Expansion

Expand the selected leaf node with the best n actions selected by our `policy_evaluation_function`, then do **simulation**.

*Note*: we expand n actions here for the following 2 reasons:

-  It’s faster than expanding 1 action. In the case of expanding 1 action, the max U value seems to change after many times of expansion. That is to say, we would expand the same node with different actions for many time. So we want to coalesce these expansion into 1 only step.
- It’s efficient than expanding all the actions. We restrict the width of Monte Carlo Tree to n with our evaluation function since there might be so many obviously useless actions.



##### 3. Simulation

Do simulation with our `heuristic_function`, which would recognize termination early by our heuristic knowledge. If no heuristic to depend on, the candidate placement of piece will be generated from `simulation_evaluation_function` which is simple and fast. Then do **backpropagation** with the result of our simulation. Furthermore, simulation will be restricted to a certain depth to speed up.



##### 4. Backpropagation

Backpropagate from the selected leaf node to root, compute running average of Q-value. The new observed Q-value will be 1 for the winner, -1 for the loser and 0 for a tie.