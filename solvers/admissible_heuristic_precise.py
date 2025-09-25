from board import Board
from .utils import astar, manhattan_distance

def admissible_heuristic_precise(board: Board, save_path: str = "admissible_heuristic_precise.json"):
    return astar(start_board=board, heuristic_fn=manhattan_distance, save_path=save_path)
