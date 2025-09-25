from __future__ import annotations
import heapq
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

        if self.file_path:
            with open(self.file_path, 'w') as f:
                f.write(f"")

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

        stats = {
            'duration_seconds': duration,
            'visited_states': self.visited_states,
            'max_frontier_size': self.max_frontier_size,
            'solution_found': final_node is not None,
            'solution_depth': self.solution_depth if final_node else None,
            'solution_cost': final_node.cost if final_node else None,
            'solution_path': self.solution_path if final_node else None
        }

        print("\n=== Search Statistics ===")
        print(f"Duration: {duration:.2f} seconds")
        print(f"States visited: {stats['visited_states']}")
        print(f"Maximum frontier size: {stats['max_frontier_size']}")
        print(f"Solution found: {stats['solution_found']}")
        if final_node:
            print(f"Solution depth: {stats['solution_depth']}")
            print(f"Solution cost: {stats['solution_cost']}")
            print("\n=== Solution Steps ===")
            moves = [step['action'] for step in self.solution_path if step['action']]
            print("Sequence of moves to solve the puzzle:")
            print(" -> ".join(moves if moves else ["Already solved!"]))
            
            print("\n=== Detailed Solution ===")
            print(f"Final State")
            self.report_state(final_node, 0)

def board_to_key(b: Board):
        return ''.join(str(x) for x in b.get_board())

def uniform_cost_search(initial_board: Board, reporter: Reporter):
    reporter.start_search()
    reporter.report_state(SearchNode(initial_board, None, None, 0), 1)
    
    frontier = list[SearchNode]()
    
    heapq.heappush(frontier, SearchNode(board=initial_board, parent=None, action=None, cost=0))    

    best_cost = { board_to_key(initial_board): 0 }

    while frontier:
        state: SearchNode
        
        state = heapq.heappop(frontier)  # tipo: SearchNode
        
        if state.board.is_soluted():
            reporter.report_solution(state)
            return state
  
        state_key = board_to_key(state.board)
        if state.cost > best_cost.get(state_key, float("inf")):
            continue
        
        for next_state, move in state.board.possible_next_states():
            step_cost = 1 
            new_cost = state.cost + step_cost
            next_key = board_to_key(next_state)

            if new_cost >= best_cost.get(next_key, float("inf")):
                continue

            best_cost[next_key] = new_cost
            next_node = SearchNode(board=next_state, parent=state, action=move, cost=new_cost)
            reporter.report_state(next_node, len(frontier))            
            frontier.append(next_node)

    return None