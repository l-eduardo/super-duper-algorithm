from board import Board
from utils import astar

def misplaced_tiles(board: Board) -> int:
    arr = board.get_board()
    count = 0
    for i, v in enumerate(arr):
        if v == -1:
            continue
        if v != i + 1:
            count += 1
    return count

def algoritmo3(start_board: Board):
    return astar(start_board, misplaced_tiles,
                 save_path="alg3_admissivel.json")

if __name__ == "__main__":
    initial = [1, 2, 3,
               4, -1, 6,
               7, 5, 8]
    b = Board(3, initial)
    result = algoritmo3(b)
    print("Resultado Algoritmo 3 (admissível simples):", result)

