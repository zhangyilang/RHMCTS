import math
import time
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
    def __init__(self, policy_value_fn, c_puct=5, max_depth=5):
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
        self.num_simu = max_depth
        # self.moved = []
        # self.adjancent = []

    def playout(self, state, num_simu=3):
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
                for i in range(num_simu):
                    new_board = deepcopy(board)
                    new_board[act[0]][act[1]] = player
                    winner = self.simulate((new_board, opponent))   # 0 for a tie, 1 for P1, 2 for P2
                    # backpropagation
                    leaf_value = -1 if winner == opponent else winner
                    node.children[act].update_recursive(leaf_value)

        elif end is True:
            node.update_recursive(1.)
        else:  # end == -1 (tie)
            node.update_recursive(0.)

    def simulate(self, state, limit_depth=50):
        # simulation stage
        board, player = state
        # adjacent = self.adjancent
        # moved = self.moved  # the coordinates placed by chess piece
        for depth in range(limit_depth):
            if time.time() > time_end:
                return 0
            x, y = simulation_policy((board, player))
            board[x][y] = player
            # moved.append((x, y))
            # adjacent = self.updata_adjacent(moved, adjacent, (x,y))
            end = self.isTerminal(board, x, y, player)
            if end is True:
                return player
            player = 1 if player == 2 else 2  # switch player
        return 0

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

        action = heuristic1(board, 1)
        if action is not None:
            return action
        action = heuristic1(board, 2)
        if action is not None:
            return action
        action = heuristic2(board, 1)
        if action is not None:
            return action
        action = heuristic2_op(board, 2)
        if action is not None:
            return action
        action = heuristic3(board, 1)
        if action is not None:
            return action
        action = heuristic3(board, 2)
        if action is not None:
            return action

        if time_end == -1:
            actions = policy_evaluation_function((board, 1)) if self.root.is_leaf() else self.root.children.items()
            return max(actions, key=lambda x: x[1])[0]

        for n in range(self.num_simu):
            if time.time() > time_end:
                break
            state_copy = deepcopy((board, 1))  # we are player 1
            self.playout(state_copy)
        return max(self.root.children.items(), key=lambda x: x[1].Q)[0]

    def update_with_move(self, last_move):
        # self.moved.append(last_move)
        # self.adjancent = self.updata_adjacent(self.moved, self.adjancent, last_move)
        # Step forward in the tree, keeping everything we already know about the subtree.
        if last_move in self.root.children:
            self.root = self.root.children[last_move]
        else:
            self.root = TreeNode(None, 1.0)

    def print_Board(self, board):
        for i in range(20):
            print(board[i])

    # def updata_adjacent(self, moved, adjacent_ori, action):
    #     h, w = action
    #     width = 20
    #     height = 20
    #     adjacent = set()
    #     if h < width - 1:
    #         adjacent.add((h + 1, w))  # right
    #     if h > 0:
    #         adjacent.add((h - 1, w))  # left
    #     if w < height - 1:
    #         adjacent.add((h, w + 1))  # upper
    #     if w > 0:
    #         adjacent.add((h, w - 1))  # lower
    #     if w < width - 1 and h < height - 1:
    #         adjacent.add((h + 1, w + 1))  # upper right
    #     if h > 0 and w < height - 1:
    #         adjacent.add((h - 1, w + 1))  # upper left
    #     if h < width - 1 and w > 0:
    #         adjacent.add((h + 1, w - 1))  # lower right
    #     if w > 0 and h > 0:
    #         adjacent.add((h - 1, w - 1))  # lower left
    #     adjacent = adjacent - set(moved)
    #     adjacent = adjacent | set(adjacent_ori)
    #     return list(adjacent)


class RHMCTSPlayer(object):
    def __init__(self, policy_evaluation_fn=policy_evaluation_function, c_puct=5, max_depth=4):
        self.rhmcts = RHMCTS(policy_evaluation_fn, c_puct, max_depth)

    def get_action(self, board, time_limit):
        global time_end
        time_end = time_limit if time_limit != -1 else -1
        action = self.rhmcts.get_action(board)
        return action


# test
if __name__ == "__main__":
    test_board = [[0 for i in range(20)] for j in range(20)]
    test_board[3][1] = 1
    test_board[2][2] = 2
    test_board[1][3] = 1
    test_board[9][9] = 2
    test_board[10][10] = 2
    test_board[3][1] = 1
    test_board[1][4] = 2
    test_board[1][1] = 1
    test_board[1][2] = 1
    test_board[4][1] = 1
    test_board[2][1] = 2

    player1 = RHMCTSPlayer()
    # time1 = time.time()
    # print(player1.get_action(test_board, time1 + 15))
    # print(time.time() - time1)
    player1.rhmcts.print_Board(test_board)
    while (True):
        print('================')
        time1 = time.time()
        x, y = player1.get_action(test_board, time1 + 15)
        print("the new move is ({},{})".format(x, y))
        if player1.rhmcts.isTerminal(test_board, x, y, 1):
            print('AI wins!')
            break
        test_board[x][y] = 1
        player1.rhmcts.print_Board(test_board)
        player1.rhmcts.update_with_move((x, y))

        move = input('your move:')
        x, y = move.strip().split(',')
        x = int(x)
        y = int(y)
        test_board[x][y] = 2
        if player1.rhmcts.isTerminal(test_board, x, y, 1):
            print('AI wins!')
            break
        player1.rhmcts.print_Board(test_board)
