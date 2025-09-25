from board import Board
from solvers.ucs_solver import Reporter, uniform_cost_search, uniform_cost_search_new


def main():
    reporter = Reporter()
    
    board = Board(3, [6, 4, 7, 8, 5, -1, 3, 2, 1])
    # board.shuffle_board()
    uniform_cost_search(initial_board=board, reporter=reporter)

if __name__ == "__main__":
    main()