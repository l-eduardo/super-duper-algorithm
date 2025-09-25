from board import Board
from .utils import astar

def misplaced_tiles(board: Board) -> int:
    arr = board.get_board()
    count = 0
    for i, v in enumerate(arr):
        if v == -1:
            continue
        if v != i + 1:
            count += 1
    return count

def admissible_heuristic(start_board: Board):
    return astar(start_board, misplaced_tiles,
                 save_path="admissible_heuristic.json")
