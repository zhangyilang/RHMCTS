# 辉哥这两个函数交给你了
def policy_evaluation_function(state):
    '''
    Return a list of the best n substates (n can be 1) for current player given current state;
    :param state: [board, player], where board is a 2-d list and player is either 1 or 2;
    :return: a list of the best n substates. Each substate is a tuple ((x, y), prob) of a board coordinate to place the
             piece and corresponding estimated winning prob for current player.
    '''
    board, player = state
    pass

def simulation_evaluation_function(state):
    pass

def simulation_policy():
    pass


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
