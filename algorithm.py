import math
from copy import deepcopy
from policy import *


class TreeNode(object):
    '''
        A node in the MCTS tree.
        Each node keeps track of its own value Q, prior probability P, and
        its visit-count-adjusted prior score U.
    '''
    def __init__(self, parent, prior_P):
        self.parent = parent
        self.P = prior_P    # prior probability for winning
        self.children = dict()
        self.visits = 0     # number of visits
        self.Q = 0          # Q-value (exploitation)
        self.U = 0          # visit-count-adjusted prior score (exploration)

    def select(self, c_puct):
        # selection stage
        return max(self.children.items(), key=lambda x: x[1].get_value(c_puct))

    def expand(self, action_prob):
        # expansion stage
        for action, prob in action_prob:
            if action not in self.children:
                self.children[action] = TreeNode(self, prob)

    def update_recursive(self, leaf_value):
        if self.parent:
            self.parent.update_recursive(-leaf_value)
        self.visits += 1
        self.Q += (leaf_value - self.Q) / self.visits   # running average

    def get_value(self, c_puct):
        self.U = (c_puct * self.P * math.sqrt(self.parent.visits) / (1 + self.visits))
        return self.Q + self.U

    def is_leaf(self):
        return len(self.children) == 0

    def is_root(self):
        return self.parent is None


class RHMCTS(object):
    def __init__(self, policy_value_fn, c_puct=1, num_simu=10000):
        """
        :param policy_value_fn: a function that takes in a board state and outputs
            a list of (action, probability) tuples and also a score in [-1, 1]
            (i.e. the expected value of the end game score from the current
            player's perspective) for the current player.
        :param c_puct: a number in (0, inf) that controls how quickly exploration
            converges to the maximum-value policy. A higher value means
            relying on the prior more.
        :param num_simu: number of simulations.
        """
        self.root = TreeNode(None, 1.0)
        self.policy = policy_value_fn
        self.c_puct = c_puct
        self.num_simu = num_simu

    def playout(self, state):
        board, player = state
        node = self.root

        # selection: find out the leaf node to be expand
        end = False
        while not node.is_leaf():
            (action_x, action_y), node = node.select(self.c_puct)
            board[action_x][action_y] = player
            player = 1 if player == 2 else 2    # switch player
            end = self.isTerminal(board, action_x, action_y, player)

        if end is False:
            # expansion: expand the best n substates.
            action_prob = self.policy((board, player))
            node.expand(action_prob)
            # simulation
            opponent = 1 if player == 2 else 2    # switch player
            for act, _ in action_prob:
                new_board = deepcopy(board)
                new_board[act[0]][act[1]] = player
                winner = self.simulate((new_board, opponent))
                # backpropagation
                if winner == player:
                    leaf_value = 1
                elif winner == opponent:
                    leaf_value = -1
                else:
                    leaf_value = 0
                node.children[act].update_recursive(leaf_value)

        elif end is True:
            node.update_recursive(1.)
        else:  # end == -1 (tie)
            node.update_recursive(0.)

    def simulate(self, state, limit_depth=20):
        # simulation stage
        board, player = state
        for depth in range(limit_depth):
            x, y = simulation_policy((board, player))
            board[x][y] = player
            end = self.isTerminal(board, x, y, player)
            if end is True:
                return player
            player = 1 if player == 2 else 2  # switch player

    def isTerminal(self, board, x, y, player):
        boardLength = len(board)
        # column
        d_start = max(-1 * x, -4)
        d_end = min(boardLength - x - 5, 0)
        for d in range(d_start, d_end + 1):
            pieces = [board[x + d + k][y] for k in range(5)]
            if pieces == [player] * 5:
                return True
        # row
        d_start = max(-1 * y, -4)
        d_end = min(boardLength - y - 5, 0)
        for d in range(d_start, d_end + 1):
            if board[x][y + d:y + d + 5] == [player] * 5:
                return True
        # positive diagonal
        d_start = max(-1 * x, -1 * y, -4)
        d_end = min(boardLength - x - 5, boardLength - y - 5, 0)
        for d in range(d_start, d_end + 1):
            pieces = [board[x + d + k][y + d + k] for k in range(5)]
            if pieces == [player] * 5:
                return True
        # oblique diagonal
        d_start = max(-1 * x, y - boardLength + 1, -4)
        d_end = min(boardLength - x - 5, y - 5, 0)
        for d in range(d_start, d_end + 1):
            pieces = [board[x + d + k][y - d - k] for k in range(5)]
            if pieces == [player] * 5:
                return True
        # tie (-1) or not terminal (False)
        for row in board:
            if 0 in row:
                return False
        return -1

    def get_action(self, board):

        actions = heuristic(board, 1, 4)
        if len(actions) != 0:
            return choice(actions)
        actions = heuristic(board, 2, 4)
        if len(actions) != 0:
            return choice(actions)
        actions = heuristic(board, 1, 3)
        if len(actions) != 0:
            return choice(actions)
        actions = heuristic(board, 2, 3)
        if len(actions) != 0:
            return choice(actions)

        for n in range(self.num_simu):
            state_copy = deepcopy((board, 1))  # 1 for we player 1
            self.playout(state_copy)
        return max(self.root.children.items(), key=lambda x: x[1].Q)[0]

    def update_with_move(self, last_move):
        # Step forward in the tree, keeping everything we already know about the subtree.
        if last_move in self.root.children:
            self.root = self.root.children[last_move]
        else:
            self.root = TreeNode(None, 1.0)


class RHMCTSPlayer(object):
    # def __init__(self, policy_evaluation_fn=policy_evaluation_function, c_puct=5, num_simu=100):
    def __init__(self, policy_evaluation_fn=coarse_policy_eva_fn, c_puct=1, num_simu=20):
        self.rhmcts = RHMCTS(policy_evaluation_fn, c_puct, num_simu)

    def get_action(self, board):
        action = self.rhmcts.get_action(board)
        self.rhmcts.update_with_move(-1)     # 改进：向下走两步，重复利用模拟结果
        return action


# test
# if __name__ == "__main__":
#     test_board = [[0 for i in range(20)] for j in range(20)]
#     test_board[1][5] = 1
#     test_board[2][4] = 1
#     test_board[3][3] = 1
#     player1 = RHMCTSPlayer()
#     print(player1.get_action(test_board))
