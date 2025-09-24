from board import Board
from .utils import astar

def manhattan_distance(board: Board) -> int:
    arr = board.get_board()
    size = board.game_size
    dist = 0
    for idx, val in enumerate(arr):
        if val == -1:
            continue
        target = val - 1
        cur_row, cur_col = divmod(idx, int(size))
        tar_row, tar_col = divmod(target, int(size))
        dist += abs(cur_row - tar_row) + abs(cur_col - tar_col)
    return dist

def inflated_manhattan(board: Board, factor: float = 1.5) -> float:
    return manhattan_distance(board) * factor

def inadmissible_heuristic(start_board: Board):
    return astar(start_board, lambda b: inflated_manhattan(b, factor=1.5),
                 save_path="inadmissible_heuristic.json")
