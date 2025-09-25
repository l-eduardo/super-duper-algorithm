from board import Board
from solvers.admissible_heuristic import admissible_heuristic
from solvers.inadmissible_heuristic import inadmissible_heuristic
from solvers.admissible_heuristic_precise import admissible_heuristic_precise

EASY_1 = [1,2,3,
          4,-1,6,
          7,5,8]
MEDIUM_1 = [1,6,7,
          5,-1,3,
          8,2,4]
MEDIUM_2 = [7,2,4,
          5,-1,6,
          8,3,1]
HARD_1 = [8,6,7,
          2,5,4,
          3,-1,1]
HARD_2 = [1,2,3,
          4,5,6,
          8,-1,7]
HARD_3 = [6,4,7,
          8,5,-1,
          3,2,1]

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

    tabuleiro = HARD_3

    b = Board(3, tabuleiro)

    # if escolha == "1":
    #     result = uniform_cost(b)
    #     print("Resultado Algoritmo 1 (Custo Uniforme):", result["result"])
    if escolha == "2":
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
