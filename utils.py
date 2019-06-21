import re
from collections import Counter


def extend_board(player, board):
    """
    add an edge for the board
    since the ege play the same role as the opponent for the player
    we set the ege as the opponent ( 3 - player )
    """
    k = len(board)  # the size of the board
    new_board = [[board[x-1][y-1] if 0 < x < k + 1 and 0 < y < k + 1 else 3-player \
                  for x in range(k + 2)] for y in range(k + 2)]
    return new_board


def is_special_class(board, player):
    """
    judge whether the several chess given in the list form a special class
    :param
        board: the board of gomoku
        player: the index of color, 1: black, 2: white
    :return:
        Counter: ({class: num of this class}, ...)
    """

    # Details in 'http://zjh776.iteye.com/blog/1979748'

    def _black_color(board):
        height, width = len(board), len(board[0])
        for i in range(height):
            for j in range(width):
                board[i][j] = (3 - board[i][j]) % 3
        return board

    if player == 2:
        list_str = _black_color(board)

    class_dict = {("WIN", (), ()): "11111",
                  ("H4", (0, 5), ()): "011110",
                  ("C4", (0), (5)): "011112",
                  ("C4", (5), (0)): "211110",
                  ("C4", (4), ()): r"^11110",
                  ("C4", (0), ()): r"01111$",
                  ("C4", (0, 2, 6), ()): "0101110",
                  ("C4", (0, 4, 6), ()): "0111010",
                  ("C4", (0, 3, 6), ()): "0110110",
                  ("H3", (0, 4), ()): "01110",
                  ("H3", (0, 2, 5), ()): "010110",
                  ("H3", (0, 3, 5), ()): "011010",
                  ("M3", (0, 1), (5)): "001112",
                  ("M3", (0, 1), ()): r"00111$",
                  ("M3", (4, 5), (0)): "211100",
                  ("M3", (4, 5), ()): r"^11100",
                  ("M3", (0, 2), (5)): "010112",
                  ("M3", (0, 2), ()): r"01011$",
                  ("M3", (3, 5), (0)): "211010",
                  ("M3", (3, 5), ()): r"^11010",
                  ("M3", (0, 3), (5)): "011012",
                  ("M3", (0, 3), ()): r"01101$",
                  ("M3", (2, 5), (0)): "210110",
                  ("M3", (2, 5), ()): r"^10110",
                  ("M3", (1, 2), ()): "10011",
                  ("M3", (2, 3), ()): "11001",
                  ("M3", (1, 3), ()): "10101",
                  ("M3", (1, 4), (0, 6)): "2011102",
                  ("M3", (1, 4), (6)): r"^011102",
                  ("M3", (1, 4), (0)): r"201110$",
                  ("H2", (0, 1, 4), ()): "00110",
                  ("H2", (0, 3, 4), ()): "01100",
                  ("H2", (0, 2, 4), ()): "01010",
                  ("H2", (0, 2, 3, 5), ()): "010010",
                  ("M2", (0, 1, 2), (5)): "000112",
                  ("M2", (0, 1, 2), ()): r"00011$",
                  ("M2", (3, 4, 5), (0)): "211000",
                  ("M2", (3, 4, 5), ()): r"^11000",
                  ("M2", (0, 1, 3), (5)): "001012",
                  ("M2", (0, 1, 3), ()): r"00101$",
                  ("M2", (2, 4, 5), (0)): "210100",
                  ("M2", (2, 4, 5), ()): r"^10100",
                  ("M2", (0, 2, 3), (5)): "010012",
                  ("M2", (0, 2, 3), ()): r"01001$",
                  ("M2", (2, 3, 5), (0)): "210010",
                  ("M2", (2, 3, 5), ()): r"^10010",
                  ("M2", (1, 2, 3), ()): "10001",
                  ("M2", (1, 3, 5), (0, 6)): "2010102",
                  ("M2", (1, 3, 5), (0)): r"201010$",
                  ("M2", (1, 3, 5), (6)): r"^010102",
                  ("M2", (1, 4, 5), (0, 6)): "2011002",
                  ("M2", (1, 4, 5), (6)): r"^011002",
                  ("M2", (1, 4, 5), (0)): r"201100^",
                  ("M2", (1, 2, 5), (0, 6)): "2001102",
                  ("M2", (1, 2, 5), (0)): r"200110$",
                  ("M2", (1, 2, 5), (6)): r"^001102",
                  ("S4", (), (0, 5)): "211112",
                  ("S4", (), (0)): r"21111$",
                  ("S4", (), (5)): r"^11112",
                  ("S3", (), (0, 4)): "21112",
                  ("S3", (), (0)): r"2111$",
                  ("S3", (), (4)): r"^1112",
                  ("S2", (), (0, 3)): "2112",
                  ("S2", (), (3)): r"^112",
                  ("S2", (), (0)): r"211$",
                  }

    height, width = len(board), len(board[0])
    class_counter = Counter()

    # scan by row
    for row_idx, row in enumerate(board):
        list_str = "".join(map(str, row))
        for key in class_dict:
            class_counter[key[0]] += len(re.findall(class_dict[key], list_str))

    # scan by col
    for col_idx in range(width):
        col = [a[col_idx] for a in board]
        list_str = "".join(map(str, col))
        for key in class_dict:
            class_counter[key[0]] += len(re.findall(class_dict[key], list_str))

    # scan by diag_1, from TL to BR
    for dist in range(-width + 1, height):
        row_ini, col_ini = (0, -dist) if dist < 0 else (dist, 0)
        diag = [board[i][j] for i in range(
            row_ini, height) for j in range(col_ini, width) if i - j == dist]
        list_str = "".join(map(str, diag))
        for key in class_dict:
            class_counter[key[0]] += len(re.findall(class_dict[key], list_str))

    # scan by diag_2, from BL to TR
    for dist in range(0, width + height - 1):
        row_ini, col_ini = (dist, 0) if dist < height else (
            height - 1, dist - height + 1)
        diag = [board[i][j] for i in range(
            row_ini, -1, -1) for j in range(col_ini, width) if i + j == dist]
        list_str = "".join(map(str, diag))
        for key in class_dict:
            class_counter[key[0]] += len(re.findall(class_dict[key], list_str))

    return class_counter


def class_to_score():
    """
    define the reward of some specific class of chess
    :return:
        score_map: a map from the special class(a string) to score(a real number)
    """
    score_map = {"WIN": 100000,
                 "H4": 10000,
                 "C4": 100,
                 "H3": 200,
                 "M3": 50,
                 "H2": 5,
                 "M2": 3,
                 "S4": -5,
                 "S3": -5,
                 "S2": -5
                 }
    return score_map


def board_evaluation(board):
    """
    evaluate the situation of the brain.
    :param
        board:
    :return:
        score: a real number, indicating how good the condition is
    """
    score = 0

    brain_board = extend_board(board=board, player=1)
    for a_class, num in is_special_class(brain_board, 1).items():
        score = score + class_to_score()[a_class] * num

    oppo_board = extend_board(board=board, player=2)
    for a_class, num in is_special_class(oppo_board, 2).items():
        score = score - class_to_score()[a_class] * num

    return score


def adjacent_moves(moved):
    """
    find the neighbors of the moved
    """
    adjacent = set()
    width = 20
    height = 20

    for (h, w) in moved:
        if h < width - 1:
            adjacent.add((h+1, w))  # right
        if h > 0:
            adjacent.add((h-1, w))  # left
        if w < height - 1:
            adjacent.add((h, w+1))  # upper
        if w > 0:
            adjacent.add((h, w-1))  # lower
        if w < width - 1 and h < height - 1:
            adjacent.add((h+1, w+1))  # upper right
        if h > 0 and w < height - 1:
            adjacent.add((h-1, w+1))  # upper left
        if h < width - 1 and w > 0:
            adjacent.add((h+1, w-1))  # lower right
        if w > 0 and h > 0:
            adjacent.add((h-1, w-1))  # lower left

    adjacent = list(set(adjacent) - set(moved))

    return adjacent


def adjacent_2_moves(moved):
    """
    find the neighbors of the moved
    """
    adjacent = set()
    width = 20
    height = 20

    for (h, w) in moved:
        if h < width - 1:
            adjacent.add((h+1, w))  # right
        if h > 0:
            adjacent.add((h-1, w))  # left
        if w < height - 1:
            adjacent.add((h, w+1))  # upper
        if w > 0:
            adjacent.add((h, w-1))  # lower
        if w < width - 1 and h < height - 1:
            adjacent.add((h+1, w+1))  # upper right
        if h > 0 and w < height - 1:
            adjacent.add((h-1, w+1))  # upper left
        if h < width - 1 and w > 0:
            adjacent.add((h+1, w-1))  # lower right
        if w > 0 and h > 0:
            adjacent.add((h-1, w-1))  # lower left

        # adj's adj
        if h < width - 2:
            adjacent.add((h+2, w))  # right
        if h-1 > 0:
            adjacent.add((h-2, w))  # left
        if w < height - 2:
            adjacent.add((h, w+2))  # upper
        if w > 1:
            adjacent.add((h, w-2))  # lower
        if w < width - 2 and h < height - 2:
            adjacent.add((h+2, w+2))  # upper right
        if h > 1 and w < height - 2:
            adjacent.add((h-2, w+2))  # upper left
        if h < width - 2 and w > 1:
            adjacent.add((h+2, w-2))  # lower right
        if w > 1 and h > 1:
            adjacent.add((h-2, w-2))  # lower left

        # if w < width - 2 and h < height - 1:
        #     adjacent.add((h+1, w+2))
        # if w < width - 1 and h < height - 2:
        #     adjacent.add((h+2, w+2))
        # if h > 1 and w < height - 1:
        #     adjacent.add((h-2, w+1))
        # if h > 0 and w < height - 2:
        #     adjacent.add((h-1, w+2))
        # if h < width - 2 and w > 0:
        #     adjacent.add((h+2, w-1))
        # if h < width - 1 and w > 1:
        #     adjacent.add((h+1, w-2))
        # if w > 1 and h > 0:
        #     adjacent.add((h-1, w-2))
        # if w > 0 and h > 1:
        #     adjacent.add((h-2, w-1))

    adjacent = list(set(adjacent) - set(moved))

    return adjacent
