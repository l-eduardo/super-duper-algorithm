from board import Board
from solvers.admissible_heuristic import admissible_heuristic
from solvers.inadmissible_heuristic import inadmissible_heuristic
from solvers.admissible_heuristic_precise import admissible_heuristic_precise
from solvers.ucs_solver import Reporter, uniform_cost_search


def menu():
    print("=== 8-Puzzle Solver ===")
    print("Escolha o algoritmo a ser utilizado:")
    print("1 - Custo Uniforme")
    print("2 - A* (heurística não admissível)")
    print("3 - A* (heurística admissível simples)")
    print("4 - A* (heurística admissível precisa)")

    escolha = input("Digite o número do algoritmo: ").strip()
    if escolha not in ["1", "2", "3", "4"]:
        print("Opção inválida!")
        return

    tabuleiro = [8, 7, 6,
               5, -1, 4,
               3, 2, 1]

    b = Board(3, tabuleiro)

    if escolha == "1":
        reporter = Reporter(file_path="./uniform_cost_search.txt")
        uniform_cost_search(b, reporter)
        print("Resultado Algoritmo 1 (Custo Uniforme):", "./uniform_cost_search.txt")

        return
    elif escolha == "2":
        result = inadmissible_heuristic(b)
        print("Resultado Algoritmo 2 (Não admissível):", result["result"])
    elif escolha == "3":
        result = admissible_heuristic(b)
        print("Resultado Algoritmo 3 (Admissível simples):", result["result"])
    elif escolha == "4":
        result = admissible_heuristic_precise(b)
        print("Resultado Algoritmo 4 (Admissível precisa):", result["result"])

    print("Arquivos gerados:")
    print("Fronteira:", result["frontier_file"])


if __name__ == "__main__":
    menu()
