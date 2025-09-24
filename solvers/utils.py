import heapq
import json
import time
from typing import Callable, Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from board import Board, Direction

@dataclass(order=True)
class PrioritizedItem:
    priority: float
    count: int
    state_key: Tuple[int, ...] = field(compare=False)
    node: "Node" = field(compare=False)

@dataclass
class Node:
    board: Board
    parent: Optional["Node"]
    move: Optional[Direction]
    g: int
    h: float
    f: float

# ---------------- Heurísticas ----------------

# ---------------- Funções auxiliares ----------------
def board_to_key(board: Board) -> Tuple[int, ...]:
    return tuple(board.get_board())

def reconstruct_path(node: Node) -> List[Direction]:
    path = []
    cur = node
    while cur and cur.move is not None:
        path.append(cur.move)
        cur = cur.parent
    return path[::-1]

# ---------------- Algoritmo A* ----------------
def astar(
    start_board: Board,
    heuristic_fn: Callable[[Board], float],
    save_path: str
) -> Dict:
    start_time = time.perf_counter()
    start_key = board_to_key(start_board)

    open_heap: List[PrioritizedItem] = []
    open_map: Dict[Tuple[int, ...], Node] = {}
    closed_map: Dict[Tuple[int, ...], Node] = {}

    start_h = heuristic_fn(start_board)
    start_node = Node(start_board, None, None, 0, start_h, start_h)
    counter = 0
    heapq.heappush(open_heap, PrioritizedItem(start_node.f, counter, start_key, start_node))
    open_map[start_key] = start_node
    max_frontier_size = 1
    nodes_visited = 0

    while open_heap:
        item = heapq.heappop(open_heap)
        cur_node = item.node
        cur_key = item.state_key

        if cur_key in closed_map:
            continue

        open_map.pop(cur_key, None)
        closed_map[cur_key] = cur_node
        nodes_visited += 1

        if cur_node.board.is_soluted():
            end_time = time.perf_counter()
            path = reconstruct_path(cur_node)
            result = {
                "path": [d.name for d in path],
                "path_length": len(path),
                "nodes_visited": nodes_visited,
                "time_seconds": end_time - start_time,
                "max_frontier_size": max_frontier_size,
            }
            with open(save_path, "w", encoding="utf-8") as f:
                json.dump({"result": result}, f, indent=2, ensure_ascii=False)
            return result

        for direction in cur_node.board.possible_moves():
            new_board = Board(cur_node.board.game_size, cur_node.board.get_board().copy())
            if direction == Direction.Left:
                new_board.move_left()
            elif direction == Direction.Right:
                new_board.move_right()
            elif direction == Direction.Up:
                new_board.move_up()
            elif direction == Direction.Down:
                new_board.move_down()

            child_key = board_to_key(new_board)
            tentative_g = cur_node.g + 1

            if child_key in closed_map:
                continue

            child_h = heuristic_fn(new_board)
            child_f = tentative_g + child_h

            if child_key in open_map and tentative_g >= open_map[child_key].g:
                continue

            child_node = Node(new_board, cur_node, direction, tentative_g, child_h, child_f)
            counter += 1
            heapq.heappush(open_heap, PrioritizedItem(child_node.f, counter, child_key, child_node))
            open_map[child_key] = child_node

        max_frontier_size = max(max_frontier_size, len(open_heap))

    return {"status": "no_solution"}
