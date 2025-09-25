from board import Board
from .utils import astar, manhattan_distance

def inflated_manhattan(board: Board, factor: float = 1.5) -> float:
    return manhattan_distance(board) * factor

def inadmissible_heuristic(start_board: Board):
    return astar(start_board, lambda b: inflated_manhattan(b, factor=1.5),
                 save_path="inadmissible_heuristic.json")
