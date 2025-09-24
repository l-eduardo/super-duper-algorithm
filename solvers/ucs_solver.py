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
            
            self.log("\n=== Detailed Solution Path ===")
            for step in self.solution_path:
                if step['action']:
                    self.log(f"\nMove: {step['action']} (cost: {step['cost']})")
                board_str = '\n'.join(' '.join(f"{n:2}" for n in step['board'][i:i+int(len(step['board'])**0.5)])
                                     for i in range(0, len(step['board']), int(len(step['board'])**0.5)))
                self.log(board_str)


def uniform_cost_search(initial_board: Board, reporter: Reporter) -> Optional[SearchNode]:
    reporter.start_search()
    
    frontier = PriorityQueue()
    initial_node = SearchNode(initial_board, None, None, 0)
    frontier.put((0, initial_node))
    
    # Using string representation of board state for visited set
    visited = set()
    
    while not frontier.empty():
        _, current_node = frontier.get()
        current_state = str(current_node.board.get_board())
        
        if current_state in visited:
            continue
            
        reporter.report_state(current_node, frontier.qsize())
        visited.add(current_state)
        
        # Check if current state is goal state (sorted except for -1 at the end)
        current_board = current_node.board.get_board()
        if current_board:
            reporter.report_solution(current_node)
            return current_node
            
        # Expand current node
        for next_state in current_node.board.possible_next_states():
            if str(next_state.get_board()) not in visited:
                move = None
                for direction in Direction:
                    test_board = Board(current_node.board.game_size, current_node.board.get_board().copy())
                    try:
                        if direction == Direction.Left:
                            test_board.move_left()
                        elif direction == Direction.Right:
                            test_board.move_right()
                        elif direction == Direction.Up:
                            test_board.move_up()
                        elif direction == Direction.Down:
                            test_board.move_down()
                        
                        if test_board.get_board() == next_state.get_board():
                            move = direction
                            break
                    except ValueError:
                        continue
                
                new_node = SearchNode(
                    board=next_state,
                    parent=current_node,
                    action=move,
                    cost=current_node.cost + 1
                )
                frontier.put((new_node.cost, new_node))
    
    reporter.report_solution(None)
    return None