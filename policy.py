from random import choice
from utils import *


def policy_evaluation_function(state):
    """
    Return a list of the best n substates (n might change for different states) for current player given current state;
    :param state: [board, player], where board is a 2-d list and player is either 1 or 2;
    :return: a list of the best n substates. Each substate is a tuple ((x, y), prob) of a board coordinate to place the
             piece and corresponding estimated winning prob for current player.
    """
    board, player = state
    moved = []
    for i in range(20):
        for j in range(20):
            if board[i][j] > 0:
                moved.append((i, j))

    substate = []
    adjacent = adjacent_moves(moved)  # get the adjacent of the moved

    # suppose the coordinates in the adjacent have been placed by chess piece
    # moved = moved + adjacent_eight
    # new_adjacent = adjacent_moves(moved)  # the adjacent' adjacent
    # adjacent = adjacent + new_adjacent

    # sum_score = 0  # normalization factor

    for (x, y) in adjacent:
        if board[x][y] > 0:
            continue
        else:
            board[x][y] = player
            score = board_evaluation(board, player)
            board[x][y] = 0
            # sum_score += score
            substate.append(((x, y), score))

    #print(substate)

    # print(substate)

    # Normalize the sub-state
    # sub = []
    # for item in substate:
    #     coord = item[0]
    #     score_ori = item[1]
    #     score_new = score_ori / sum_score
    #     sub.append((coord, score_new))

    # choose the 5 sub-state with the highest scores
    sub = sorted(substate, key=lambda x: x[1], reverse=True)[:3]
    # print(sub)

    # normalization
    sub_norm = []
    max_score = sub[0][1]
    min_score = sub[-1][1]
    # print(max_score)
    # print(min_score)
    # print(sub)
    if max_score != min_score:
        for s in sub:
            sub_norm.append((s[0], (s[1] - min_score + 5) / (max_score - min_score) * 0.9))
    else:
        for s in sub:
            sub_norm.append((s[0], 0.9))

    # print(sub_norm)

    return tuple(sub_norm)


def simulation_evaluation_function(state):
    """
    Simplified version of policy_evaluation function. Return more possible actions without probability.
    :param state: [board, player]
    :return: [(x0, y0), (x1, y1), ... , (xn, yn)]
    """
    board, player = state
    moved = []  # the coordinates placed by chess piece
    k = len(board)  # the size of the board
    for i in range(k):
        for j in range(k):
            if board[i][j] > 0:
                moved.append((i, j))
    adjacent = adjacent_moves(moved)  # get the adjacent of the moved

    substate = []
    for (x, y) in adjacent:
        if board[x][y] > 0:
            continue
        else:
            board[x][y] = player
            score = board_evaluation(board, player)
            board[x][y] = 0
            substate.append(((x, y), score))

    substate = sorted(substate, key=lambda x: -x[1])[:10]
    sub = []
    for item in substate:
        coord = item[0]
        sub.append(coord)
    return sub


def simulation_policy(state):
    board, player = state
    opponent = 1 if player == 2 else 2

    action = heuristic1(board, player)
    if action is not None:
        return action
    action = heuristic1(board, opponent)
    if action is not None:
        return action

    action = heuristic2(board, player)
    if action is not None:
        return action
    action = heuristic2(board, opponent)
    if action is not None:
        return action

    action = heuristic3(board, player)
    if action is not None:
        return action
    action = heuristic3(board, opponent)
    if action is not None:
        return action

    moved = []
    for i in range(20):
        for j in range(20):
            if board[i][j] > 0:
                moved.append((i, j))
    adjacent = adjacent_moves(moved)  # get the adjacent of the moved
    actions = list(set(adjacent) - set(moved))

    # actions = simulation_evaluation_function(state)
    return choice(actions)


# Heuristic Knowledge
def heuristic1(board, player):
    # heuristic for direct winning
    boardLength = len(board)
    opp = 3 - player
    # column
    for x in range(boardLength-4):
        for y in range(boardLength):
            pieces = tuple(board[x+d][y] for d in range(5))
            if pieces.count(player) == 4 and 0 in pieces:
                d = pieces.index(0)
                return x + d, y
            if pieces.count(opp) == 4 and 0 in pieces:
                d = pieces.index(0)
                return x + d, y
    # row
    for x in range(boardLength):
        for y in range(boardLength-4):
            pieces = tuple(board[x][y+d] for d in range(5))
            if pieces.count(player) == 4 and 0 in pieces:
                d = pieces.index(0)
                return x, y + d
            if pieces.count(opp) == 4 and 0 in pieces:
                d = pieces.index(0)
                return x, y + d
    # positive diagonal
    for x in range(boardLength-4):
        for y in range(boardLength-4):
            pieces = tuple(board[x+d][y+d] for d in range(5))
            if pieces.count(player) == 4 and 0 in pieces:
                d = pieces.index(0)
                return x + d, y + d
            if pieces.count(opp) == 4 and 0 in pieces:
                d = pieces.index(0)
                return x + d, y + d
    # oblique diagonal
    for x in range(boardLength-4):
        for y in range(4, boardLength):
            pieces = tuple(board[x+d][y-d] for d in range(5))
            if pieces.count(player) == 4 and 0 in pieces:
                d = pieces.index(0)
                return x + d, y - d
            if pieces.count(opp) == 4 and 0 in pieces:
                d = pieces.index(0)
                return x + d, y - d
    return None


def heuristic2(board, player):
    # heuristic for direct winning
    boardLength = len(board)
    opp = 3 - player
    # column
    for x in range(boardLength-5):
        for y in range(boardLength):
            pieces = tuple(board[x+d][y] for d in range(6))
            if pieces[0] == 0 and pieces[5] == 0 and pieces[1:5].count(player) == 3 and 0 in pieces[1:5]:
                d = pieces.index(0, 1, -1)
                return x + d, y
            if pieces[0] == 0 and pieces[5] == 0 and pieces[1:5].count(opp) == 3 and 0 in pieces[1:5]:
                d = pieces.index(0, 1, -1)
                return x + d, y
    # row
    for x in range(boardLength):
        for y in range(boardLength-5):
            pieces = tuple(board[x][y+d] for d in range(6))
            if pieces[0] == 0 and pieces[5] == 0 and pieces[1:5].count(player) == 3 and 0 in pieces[1:5]:
                d = pieces.index(0, 1, -1)
                return x, y + d
            if pieces[0] == 0 and pieces[5] == 0 and pieces[1:5].count(opp) == 3 and 0 in pieces[1:5]:
                d = pieces.index(0, 1, -1)
                return x, y + d
    # positive diagonal
    for x in range(boardLength-5):
        for y in range(boardLength-5):
            pieces = tuple(board[x+d][y+d] for d in range(6))
            if pieces[0] == 0 and pieces[5] == 0 and pieces[1:5].count(player) == 3 and 0 in pieces[1:5]:
                d = pieces.index(0, 1, -1)
                return x + d, y + d
            if pieces[0] == 0 and pieces[5] == 0 and pieces[1:5].count(opp) == 3 and 0 in pieces[1:5]:
                d = pieces.index(0, 1, -1)
                return x + d, y + d
    # oblique diagonal
    for x in range(boardLength-5):
        for y in range(5, boardLength):
            pieces = tuple(board[x+d][y-d] for d in range(6))
            if pieces[0] == 0 and pieces[5] == 0 and pieces[1:5].count(player) == 3 and 0 in pieces[1:5]:
                d = pieces.index(0, 1, -1)
                return x + d, y - d
            if pieces[0] == 0 and pieces[5] == 0 and pieces[1:5].count(opp) == 3 and 0 in pieces[1:5]:
                d = pieces.index(0, 1, -1)
                return x + d, y - d
    return None


def heuristic2_op(board, player):
    # heuristic for 3 pieces in a line
    boardLength = len(board)
    # column
    for x in range(boardLength-5):
        for y in range(boardLength):
            pieces = tuple(board[x+d][y] for d in range(6))
            if pieces[0] == 0 and pieces[5] == 0 and pieces[1:5].count(player) == 3 and 0 in pieces[1:5]:
                d = pieces.index(0, 1, -1)
                actions = [(x, y), (x + 4, y)] if d == 4 else [(x + 1, y), (x + 5, y)] if d == 1 \
                           else [(x, y), (x + d, y), (x + 5, y)]
                max_s = 0
                max_act = None
                for act_x, act_y in actions:
                    board[act_x][act_y] = player
                    score = board_evaluation(board, player)
                    board[act_x][act_y] = 0
                    if score > max_s:
                        max_s = score
                        max_act = (act_x, act_y)
                return max_act
    # row
    for x in range(boardLength):
        for y in range(boardLength-5):
            pieces = tuple(board[x][y+d] for d in range(6))
            if pieces[0] == 0 and pieces[5] == 0 and pieces[1:5].count(player) == 3 and 0 in pieces[1:5]:
                d = pieces.index(0, 1, -1)
                actions = [(x, y), (x, y + 4)] if d == 4 else [(x, y + 1), (x, y + 5)] if d == 1 \
                    else [(x, y), (x, y + d), (x, y + 5)]
                max_s = 0
                max_act = None
                for act_x, act_y in actions:
                    board[act_x][act_y] = player
                    score = board_evaluation(board, player)
                    board[act_x][act_y] = 0
                    if score > max_s:
                        max_s = score
                        max_act = (act_x, act_y)
                return max_act
    # positive diagonal
    for x in range(boardLength-5):
        for y in range(boardLength-5):
            pieces = tuple(board[x+d][y+d] for d in range(6))
            if pieces[0] == 0 and pieces[5] == 0 and pieces[1:5].count(player) == 3 and 0 in pieces[1:5]:
                d = pieces.index(0, 1, -1)
                actions = [(x, y), (x + 4, y + 4)] if d == 4 else [(x + 1, y + 1), (x + 5, y + 5)] if d == 1 \
                    else [(x, y), (x + d, y + d), (x + 5, y + 5)]
                max_s = 0
                max_act = None
                for act_x, act_y in actions:
                    board[act_x][act_y] = player
                    score = board_evaluation(board, player)
                    board[act_x][act_y] = 0
                    if score > max_s:
                        max_s = score
                        max_act = (act_x, act_y)
                return max_act
    # oblique diagonal
    for x in range(boardLength-5):
        for y in range(5, boardLength):
            pieces = tuple(board[x+d][y-d] for d in range(6))
            if pieces[0] == 0 and pieces[5] == 0 and pieces[1:5].count(player) == 3 and 0 in pieces[1:5]:
                d = pieces.index(0, 1, -1)
                actions = [(x, y), (x + 4, y - 4)] if d == 4 else [(x + 1, y - 1), (x + 5, y - 5)] if d == 1 \
                    else [(x, y), (x + d, y - d), (x + 5, y - 5)]
                max_s = 0
                max_act = None
                for act_x, act_y in actions:
                    board[act_x][act_y] = player
                    score = board_evaluation(board, player)
                    board[act_x][act_y] = 0
                    if score > max_s:
                        max_s = score
                        max_act = (act_x, act_y)
                return max_act
    return None


def heuristic3(board, player):
    # heuristic for 'double four', 'one four one three' and 'double three'
    boardLength = len(board)
    opp = 3 - player
    # possible placement to achieve four
    # column
    col4 = set()
    for x in range(boardLength - 4):
        for y in range(boardLength):
            pieces = tuple(board[x + d][y] for d in range(5))
            if pieces.count(0) == 2 and pieces.count(player) == 3:
                for d in range(5):
                    if pieces[d] == 0:
                        col4.add((x + d, y))
            if pieces.count(0) == 2 and pieces.count(opp) == 3:
                for d in range(5):
                    if pieces[d] == 0:
                        col4.add((x + d, y))
    # row
    row4 = set()
    for x in range(boardLength):
        for y in range(boardLength - 4):
            pieces = tuple(board[x][y + d] for d in range(5))
            if pieces.count(0) == 2 and pieces.count(player) == 3:
                for d in range(5):
                    if pieces[d] == 0:
                        row4.add((x, y + d))
            if pieces.count(0) == 2 and pieces.count(opp) == 3:
                for d in range(5):
                    if pieces[d] == 0:
                        row4.add((x, y + d))
    # positive diagonal
    pos4 = set()
    for x in range(boardLength - 4):
        for y in range(boardLength - 4):
            pieces = tuple(board[x + d][y + d] for d in range(5))
            if pieces.count(0) == 2 and pieces.count(player) == 3:
                for d in range(5):
                    if pieces[d] == 0:
                        pos4.add((x + d, y + d))
            if pieces.count(0) == 2 and pieces.count(opp) == 3:
                for d in range(5):
                    if pieces[d] == 0:
                        pos4.add((x + d, y + d))
    # oblique diagonal
    ob4 = set()
    for x in range(boardLength - 4):
        for y in range(4, boardLength):
            pieces = tuple(board[x + d][y - d] for d in range(5))
            if pieces.count(0) == 2 and pieces.count(player) == 3:
                for d in range(5):
                    if pieces[d] == 0:
                        ob4.add((x + d, y - d))
            if pieces.count(0) == 2 and pieces.count(opp) == 3:
                for d in range(5):
                    if pieces[d] == 0:
                        ob4.add((x + d, y - d))

    # possible placement to achieve three
    # column
    col3 = set()
    for x in range(boardLength - 5):
        for y in range(boardLength):
            pieces = tuple(board[x + d][y] for d in range(6))
            if pieces[0] == 0 and pieces[5] == 0 and pieces[1:5].count(player) == 2 and pieces[1:5].count(0) == 2:
                for d in range(1, 5):
                    if pieces[d] == 0:
                        col3.add((x + d, y))
            if pieces[0] == 0 and pieces[5] == 0 and pieces[1:5].count(opp) == 2 and pieces[1:5].count(0) == 2:
                for d in range(1, 5):
                    if pieces[d] == 0:
                        col3.add((x + d, y))
    # row
    row3 = set()
    for x in range(boardLength):
        for y in range(boardLength - 5):
            pieces = tuple(board[x][y + d] for d in range(6))
            if pieces[0] == 0 and pieces[5] == 0 and pieces[1:5].count(player) == 2 and pieces[1:5].count(0) == 2:
                for d in range(1, 5):
                    if pieces[d] == 0:
                        row3.add((x, y + d))
            if pieces[0] == 0 and pieces[5] == 0 and pieces[1:5].count(opp) == 2 and pieces[1:5].count(0) == 2:
                for d in range(1, 5):
                    if pieces[d] == 0:
                        row3.add((x, y + d))
    # positive diagonal
    pos3 = set()
    for x in range(boardLength - 5):
        for y in range(boardLength - 5):
            pieces = tuple(board[x + d][y + d] for d in range(6))
            if pieces[0] == 0 and pieces[5] == 0 and pieces[1:5].count(player) == 2 and pieces[1:5].count(0) == 2:
                for d in range(1, 5):
                    if pieces[d] == 0:
                        pos3.add((x + d, y + d))
            if pieces[0] == 0 and pieces[5] == 0 and pieces[1:5].count(opp) == 2 and pieces[1:5].count(0) == 2:
                for d in range(1, 5):
                    if pieces[d] == 0:
                        pos3.add((x + d, y + d))
    # oblique diagonal
    ob3 = set()
    for x in range(boardLength - 5):
        for y in range(5, boardLength):
            pieces = tuple(board[x + d][y - d] for d in range(6))
            if pieces[0] == 0 and pieces[5] == 0 and pieces[1:5].count(player) == 2 and pieces[1:5].count(0) == 2:
                for d in range(1, 5):
                    if pieces[d] == 0:
                        ob3.add((x + d, y - d))
            if pieces[0] == 0 and pieces[5] == 0 and pieces[1:5].count(opp) == 2 and pieces[1:5].count(0) == 2:
                for d in range(1, 5):
                    if pieces[d] == 0:
                        ob3.add((x + d, y - d))

    sets = [col4, row4, pos4, ob4, col3, row3, pos3, ob3]
    for i in range(8):
        for j in range(i+1, 8):
            intersect = sets[i] & sets[j]
            if len(intersect) != 0:
                return list(intersect)[0]
