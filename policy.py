from random import choice, sample


heuristic4_p1 = {(1, 1, 1, 1, 0): 4, (1, 1, 1, 0, 1): 3, (1, 1, 0, 1, 1): 2, (1, 0, 1, 1, 1): 1, (0, 1, 1, 1, 1): 0}
heuristic4_p2 = {(2, 2, 2, 2, 0): 4, (2, 2, 2, 0, 2): 3, (2, 2, 0, 2, 2): 2, (2, 0, 2, 2, 2): 1, (0, 2, 2, 2, 2): 0}
h4 = {1: heuristic4_p1, 2: heuristic4_p2}

heuristic3_p1 = {(0, 1, 1, 1, 0, 0): 4, (0, 0, 1, 1, 1, 0): 1, (0, 1, 1, 0, 1, 0): 2, (0, 1, 1, 0, 1, 0): 3}
heuristic3_p2 = {(0, 2, 2, 2, 0, 0): 4, (0, 0, 2, 2, 2, 0): 1, (0, 2, 2, 0, 2, 0): 2, (0, 2, 2, 0, 2, 0): 3}
h3 = {1: heuristic3_p1, 2: heuristic3_p2}


# 辉哥这两个函数交给你了
def policy_evaluation_function(state):
    '''
    Return a list of the best n substates (n might change for different states) for current player given current state;
    :param state: [board, player], where board is a 2-d list and player is either 1 or 2;
    :return: a list of the best n substates. Each substate is a tuple ((x, y), prob) of a board coordinate to place the
             piece and corresponding estimated winning prob for current player.
    '''
    board, player = state
    pass


def simulation_evaluation_function(state):
    '''
    Simplified version of policy_evaluation function. Return more possible actions without probability.
    :param state: [board, player]
    :return: [(x0, y0), (x1, y1), ... , (xn, yn)]
    '''
    board, player = state
    pass


def coarse_policy_eva_fn(state):
    board, player = state
    actions = [(x, y) for x in range(len(board)) for y in range(len(board)) if board[x][y] == 0]
    act_prob = [(act, 1/len(actions)) for act in actions]
    return sample(act_prob, 5)


def coarse_simu_eva_fn(state):
    board, player = state
    actions = [(x, y) for x in range(len(board)) for y in range(len(board)) if board[x][y] == 0]
    return actions


def simulation_policy(state):
    board, player = state
    opponent = 1 if player == 2 else 2

    actions = heuristic(board, player, 4)
    if len(actions) != 0:
        return choice(actions)

    actions = heuristic(board, opponent, 4)
    if len(actions) != 0:
        return choice(actions)

    actions = heuristic(board, player, 3)
    if len(actions) != 0:
        return choice(actions)

    actions = heuristic(board, opponent, 3)
    if len(actions) != 0:
        return choice(actions)

    # actions = simulation_evaluation_function(state)
    actions = coarse_simu_eva_fn(state)
    return choice(actions)


# Heuristic Knowledge
def heuristic(board, player, number):
    h = h4 if number == 4 else h3
    pieceLen = 5 if number == 4 else 6
    boardLength = len(board)
    heuristicActions = []
    # column
    for x in range(boardLength-pieceLen+1):
        for y in range(boardLength):
            pieces = tuple(board[x+d][y] for d in range(pieceLen))
            if pieces in h[player]:
                d = h[player][pieces]
                heuristicActions.append((x + d, y))
    # row
    for x in range(boardLength):
        for y in range(boardLength-pieceLen+1):
            pieces = tuple(board[x][y+d] for d in range(pieceLen))
            if pieces in h[player]:
                d = h[player][pieces]
                heuristicActions.append((x, y + d))
    # positive diagonal
    for x in range(boardLength-pieceLen+1):
        for y in range(boardLength-pieceLen+1):
            pieces = tuple(board[x+d][y+d] for d in range(pieceLen))
            if pieces in h[player]:
                d = h[player][pieces]
                heuristicActions.append((x + d, y + d))
    # oblique diagonal
    for x in range(boardLength-pieceLen+1):
        for y in range(pieceLen-1, boardLength):
            pieces = tuple(board[x+d][y-d] for d in range(pieceLen))
            if pieces in h[player]:
                d = h[player][pieces]
                heuristicActions.append((x + d, y - d))
    return heuristicActions
