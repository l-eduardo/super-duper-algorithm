from board import Board
from utils import astar

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

def algoritmo2(start_board: Board):
    return astar(start_board, lambda b: inflated_manhattan(b, factor=1.5),
                 save_path="alg2_inadmissivel.json")

if __name__ == "__main__":
    initial = [8, 7, 6,
               5, 4, 3,
               2, 1, -1]
    b = Board(3, initial)
    result = algoritmo2(b)
    print("Resultado Algoritmo 2 (não admissível):", result)
