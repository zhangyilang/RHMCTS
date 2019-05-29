import numpy as np
import random
import copy


class TreeNode(object):
    '''
        A node in the MCTS tree.
        Each node keeps track of its own value Q, prior probability P, and
        its visit-count-adjusted prior score U.
    '''
    def __init__(self, parent, prior_P):
        self.parent = parent
        self.P = prior_P    # prior probability
        self.children = dict()
        self.visits = 0     # number of visits
        self.Q = 0          # evaluated value (exploitation)
        self.U = 0          # visit-count-adjusted prior score (exploration)

    def select(self, c_puct):
        return max(self.children.items(), key=lambda x: x[1].get_value(c_puct))

    def expand(self, action_prob):
        for action, prob in action_prob:
            if action not in self.children:
                self.children[action] = TreeNode(self, prob)

    def update_recursive(self, leaf_value):
        if self.parent:
            self.parent.update_recursive(leaf_value)
        self.visits += 1
        self.Q += (leaf_value - self.Q) / self.visits   # running average

    def get_value(self, c_puct):
        self.U = (c_puct * self.P * np.sqrt(self.parent.visits) / (1 + self.visits))
        return self.Q + self.U

    def is_leaf(self):
        return len(self.children) == 0

    def is_root(self):
        return self.parent is None


def lookaround(board, n):
    # look around for n grids
    actions = set()
    for x in range(0, len(board)):
        for y in range(0, len(board)):
            if board[x][y] != 0:
                for i in range(max(x-n, 0), min(x+n, len(board))):
                    for j in range(max(y-n, 0), min(y+n, len(board))):
                        if board[i][j] == 0:
                            actions.add((i, j))
    return actions


def isTerminal(state, x, y):
    boardLength = len(state)
    player = state[x][y]
    # column
    d_start = max(-1*x, -4)
    d_end = min(boardLength-x-5, 0)
    for d in range(d_start, d_end+1):
        pieces = [state[x+d+k][y] for k in range(5)]
        if pieces == [player] * 5:
            return True
    # row
    d_start = max(-1*y, -4)
    d_end = min(boardLength-y-5, 0)
    for d in range(d_start, d_end+1):
        if state[x][y+d:y+d+5] == [player] * 5:
            return True
    # positive diagonal
    d_start = max(-1*x, -1*y, -4)
    d_end = min(boardLength-x-5, boardLength-y-5, 0)
    for d in range(d_start, d_end+1):
        pieces = [state[x+d+k][y+d+k] for k in range(5)]
        if pieces == [player] * 5:
            return True
    # oblique diagonal
    d_start = max(-1*x, y-boardLength+1, -4)
    d_end = min(boardLength-x-5, y-5, 0)
    for d in range(d_start, d_end+1):
        pieces = [state[x+d+k][y-d-k] for k in range(5)]
        if pieces == [player] * 5:
            return True
    return False


def heuristic(state, player, number):
    # Heuristic Knowledge
    boardLength = len(state)
    opponent = 2 if player == 1 else 1
    heuristicActions = []
    # column
    for x in range(boardLength-4):
        for y in range(boardLength):
            pieces = [state[x+d][y] for d in range(5)]
            if pieces.count(player) == number and opponent not in pieces:
                heuristicActions += [(x+d, y) for d in range(5) if state[x+d][y] == 0]
    # row
    for x in range(boardLength):
        for y in range(boardLength-4):
            pieces = [state[x][y+d] for d in range(5)]
            if pieces.count(player) == number and opponent not in pieces:
                heuristicActions += [(x, y+d) for d in range(5) if state[x][y+d] == 0]
    # positive diagonal
    for x in range(boardLength-4):
        for y in range(boardLength-4):
            pieces = [state[x+d][y+d] for d in range(5)]
            if pieces.count(player) == number and opponent not in pieces:
                heuristicActions += [(x+d, y+d) for d in range(5) if state[x+d][y+d] == 0]
    # oblique diagonal
    for x in range(boardLength - 4):
        for y in range(4, boardLength):
            pieces = [state[x+d][y-d] for d in range(5)]
            if pieces.count(player) == number and opponent not in pieces:
                heuristicActions += [(x+d, y-d) for d in range(5) if state[x+d][y-d] == 0]
    return heuristicActions


def getaction(state, player):
    # 可以改进的地方：
    # 1. 如果某一步棋有多重效果（如一三一四、既给自己制造机会又封锁对面的机会等），可以增大其被选中的几率
    # 2. lookaround代替随机选(已改)
    opponent = 2 if player == 1 else 1
    actions = heuristic(state, player, 4)
    if len(actions) != 0:
        return random.choice(actions), 'W'  # win
    actions = heuristic(state, opponent, 4)
    if len(actions) != 0:
        return random.choice(actions), 'U'  # unknown
    actions = heuristic(state, player, 3)
    if len(actions) != 0:
        return random.choice(actions), 'U'
    actions = heuristic(state, opponent, 3)
    if len(actions) != 0:
        return random.choice(actions), 'U'
    empty = list(lookaround(state, 2))
    if len(empty) == 0:
        return (-1, -1), 'D'                # draw
    return random.choice(empty), 'U'


def simulation(state, player):
    (x, y), status = getaction(state, player)
    if status == 'W':
        return 1 if player == 1 else 0
    if status == 'D':
        return 0.5
    state[x][y] = player
    player = 2 if player == 1 else 1    # change player
    return simulation(state, player)


def HMCTS(moves, board, simuTimes):
    probabilities = []
    for x, y in moves:
        reward = 0
        board[x][y] = 1
        if isTerminal(board, x, y):
            reward = simuTimes
        else:
            for i in range(simuTimes):
                board_new = copy.deepcopy(board)
                reward += simulation(board_new, 2)
        board[x][y] = 0
        probabilities.append(reward/simuTimes)
    return probabilities


def ADP(board):
    pass


def adpwithmcts(board, ratio, simuTimes):
    '''
    implement ADP with MCTS
    :param board: 2-d list for the gomoku board, board[i][j] == 0 for empty, 1 for my move, 2 for opponents's move
    :param ratio: parameter lambda to adjust the ratio between ADP and MCTS
    :param simuTimes: simulation times of MCTS
    :return: the action to take
    '''
    M_ADP, W_ADP = ADP(board)   # M is moves and W is corresponding winning probability
    W_MCTS = HMCTS(M_ADP, board, simuTimes)
    max_p = 0
    action = None
    for i in range(len(W_ADP)):
        p = ratio * W_ADP[i] + (1 - ratio) * W_MCTS[i]
        if p > max_p:
            max_p = p
            action = M_ADP[i]
    return action


# test
if __name__ == "__main__":
    MAX_BOARD = 20
    board = [[0 for i in range(MAX_BOARD)] for j in range(MAX_BOARD)]
    board[5][5] = 2
    board[6][5] = 2
    board[8][5] = 2
    print(getaction(board, 1))
