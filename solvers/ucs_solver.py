from __future__ import annotations
from queue import PriorityQueue
from typing import List, Optional, Set, Tuple
from board import Board, Direction
from dataclasses import dataclass
from datetime import datetime


@dataclass
class SearchNode:
    board: Board
    parent: Optional[SearchNode]
    action: Optional[Direction]
    cost: int

    def __lt__(self, other):
        return self.cost < other.cost


class Reporter:
    def __init__(self, file_path: Optional[str] = None):
        self.file_path = file_path
        self.start_time = None
        self.visited_states = 0
        self.max_frontier_size = 0
        self.solution_depth = 0
        self.solution_path = []

    def start_search(self):
        self.start_time = datetime.now()

    def log(self, message: str):
        if self.file_path:
            with open(self.file_path, 'a') as f:
                f.write(f"{message}\n")
        else:
            print(message)

    def report_state(self, node: SearchNode, frontier_size: int):
        self.visited_states += 1
        self.max_frontier_size = max(self.max_frontier_size, frontier_size)
        board_str = '\n'.join(' '.join(f"{n:2}" for n in node.board.get_board()[i:i+node.board.game_size])
                             for i in range(0, len(node.board.get_board()), node.board.game_size))
        self.log(f"\nVisiting state (cost={node.cost}):\n{board_str}")

    def report_solution(self, final_node: Optional[SearchNode]):
        end_time = datetime.now()
        duration = (end_time - self.start_time).total_seconds()

        if final_node:
            # Reconstruct path
            node = final_node
            path = []
            while node:
                path.append({
                    'board': node.board.get_board(),
                    'action': node.action.name if node.action else None,
                    'cost': node.cost
                })
                node = node.parent
            path.reverse()
            self.solution_path = path
            self.solution_depth = len(path) - 1

        # Report statistics
        stats = {
            'duration_seconds': duration,
            'visited_states': self.visited_states,
            'max_frontier_size': self.max_frontier_size,
            'solution_found': final_node is not None,
            'solution_depth': self.solution_depth if final_node else None,
            'solution_cost': final_node.cost if final_node else None
        }

        self.log("\n=== Search Statistics ===")
        self.log(f"Duration: {duration:.2f} seconds")
        self.log(f"States visited: {stats['visited_states']}")
        self.log(f"Maximum frontier size: {stats['max_frontier_size']}")
        self.log(f"Solution found: {stats['solution_found']}")
        if final_node:
            self.log(f"Solution depth: {stats['solution_depth']}")
            self.log(f"Solution cost: {stats['solution_cost']}")
            self.log("\n=== Solution Steps ===")
            moves = [step['action'] for step in self.solution_path if step['action']]
            self.log("Sequence of moves to solve the puzzle:")
            self.log(" -> ".join(moves if moves else ["Already solved!"]))
            
            self.log("\n=== Detailed Solution ===")
            self.log(f"Final State")
            self.report_state(final_node, 0)
            # for step in self.solution_path:
            #     if step['action']:
            #         self.log(f"\nMove: {step['action']} (cost: {step['cost']})")
            #     board_str = '\n'.join(' '.join(f"{n:2}" for n in step['board'][i:i+int(len(step['board'])**0.5)])
            #                          for i in range(0, len(step['board']), int(len(step['board'])**0.5)))
            #     self.log(board_str)


def uniform_cost_search(initial_board: Board, reporter: Reporter):
    reporter.start_search()
    reporter.report_state(SearchNode(initial_board, None, None, 0), 1)
    
    frontier = list[SearchNode]()
    
    heapq.heappush(frontier, SearchNode(board=initial_board, parent=None, action=None, cost=0))


    def board_key(b: Board):
        return ''.join(str(x) for x in b.get_board())

    best_cost = { board_key(initial_board): 0 }

    visited = list[Board]()

    while frontier:
        state: SearchNode
        
        # frontier.sort(key=lambda x: x.cost)  # Sort by cost to simulate priority queue behavior

        state = heapq.heappop(frontier)  # tipo: SearchNode
        
        if state.board.is_soluted():
            reporter.report_solution(state)
            return state
  
        state_key = board_key(state.board)
        if state.cost > best_cost.get(state_key, float("inf")):
            continue
        
        # visited.append(state.board)

        for next_state, move in state.board.possible_next_states():
            step_cost = 1 
            new_cost = state.cost + step_cost
            next_key = board_key(next_state)

            if new_cost >= best_cost.get(next_key, float("inf")):
                continue

            best_cost[next_key] = new_cost
            next_node = SearchNode(board=next_state, parent=state, action=move, cost=new_cost)
            reporter.report_state(next_node, len(frontier))            
            frontier.append(next_node)

    # If we get here, no solution was found
    return None
    
import heapq
import itertools
from typing import Optional

def uniform_cost_search_new(initial_board: Board, reporter: Reporter) -> Optional[SearchNode]:
    reporter.start_search()
    root = SearchNode(board=initial_board, parent=None, action=None, cost=0)
    reporter.report_state(root, 1)

    heap = list()
    counter = itertools.count()
    heapq.heappush(heap, (0, next(counter), root))

    def board_key(b: Board):
        return tuple(b.get_board())

    best_cost = { board_key(initial_board): 0 }

    while heap:
        cost, _, node = heapq.heappop(heap)
        key = board_key(node.board)

        if cost > best_cost.get(key, float("inf")):
            continue

        reporter.report_state(node, len(heap))

        # checa solução (suporta is_soluted ou is_solved)
        if (hasattr(node.board, "is_soluted") and node.board.is_soluted()) or \
           (hasattr(node.board, "is_solved") and node.board.is_solved()):
            reporter.report_solution(node)
            return node

        # expande vizinhos
        for next_board, move in node.board.possible_next_states():
            step_cost = 1  # custo unitário por movimento (ajuste se necessário)
            new_cost = node.cost + step_cost
            next_key = board_key(next_board)

            # se encontramos caminho melhor para next_key, atualizamos e empurramos no heap
            if new_cost < best_cost.get(next_key, float("inf")):
                best_cost[next_key] = new_cost
                next_node = SearchNode(board=next_board, parent=node, action=move, cost=new_cost)
                heapq.heappush(heap, (new_cost, next(counter), next_node))
                # opcional: reporte do nó recém-gerado (comentável se gerar muito I/O)
                reporter.report_state(next_node, len(heap))

    # sem solução
    reporter.report_solution(None)
    return None