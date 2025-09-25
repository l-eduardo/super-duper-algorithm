from board import Board
from .utils import astar, manhattan_distance

def nilsson_sequence_score(board: Board) -> float:
    arr = board.get_board()
    dist = manhattan_distance(board)

    seq = [0, 1, 2, 5, 8, 7, 6, 3]
    bonus = 0
    for i in range(len(seq)):
        current_val = arr[seq[i]]
        next_val = arr[seq[(i + 1) % len(seq)]]
        if current_val == -1 or next_val == -1:
            continue
        if (current_val + 1) % 9 != next_val % 9:
            bonus += 2

    return dist + bonus

def inadmissible_heuristic(start_board: Board):
    return astar(start_board, lambda b: nilsson_sequence_score(b),
                 save_path="inadmissible_heuristic.json")
