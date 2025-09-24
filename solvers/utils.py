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
    save_path: str = "frontier_visited.json",
) -> Dict:
    start_time = time.perf_counter()
    start_key = board_to_key(start_board)

    open_heap: List[PrioritizedItem] = []
    open_map: Dict[Tuple[int, ...], Node] = {}
    closed_map: Dict[Tuple[int, ...], Node] = {}

    start_h = heuristic_fn(start_board)
    start_node = Node(board=start_board, parent=None, move=None, g=0, h=start_h, f=start_h)
    counter = 0
    heapq.heappush(open_heap, PrioritizedItem(start_node.f, counter, start_key, start_node))
    open_map[start_key] = start_node

    max_frontier_size = 1
    nodes_visited = 0
    iterations = 0

    while open_heap:
        iterations += 1

        item = heapq.heappop(open_heap)
        cur_node = item.node
        cur_key = item.state_key

        # lazy skip se já em closed
        if cur_key in closed_map:
            continue

        # mover para closed
        open_map.pop(cur_key, None)
        closed_map[cur_key] = cur_node
        nodes_visited += 1

        # objetivo
        if cur_node.board.is_soluted():
            end_time = time.perf_counter()
            path = reconstruct_path(cur_node)
            result = {
                "path": [d.name for d in path],
                "path_length": len(path),
                "nodes_visited": nodes_visited,
                "time_seconds": end_time - start_time,
                "max_frontier_size": max_frontier_size,
                "status": "solved"
            }
            # salva frontier/visited (no momento da terminação)
            _dump_frontier_visited(open_map, closed_map, save_path)
            return {"result": result, "frontier_file": save_path}

        # expandir
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
            else:
                continue

            child_key = board_to_key(new_board)
            tentative_g = cur_node.g + 1

            if child_key in closed_map:
                existing = closed_map[child_key]
                if tentative_g >= existing.g:
                    continue

            child_h = heuristic_fn(new_board)
            child_f = tentative_g + child_h

            in_open = open_map.get(child_key)
            if in_open is not None and tentative_g >= in_open.g:
                continue

            child_node = Node(board=new_board, parent=cur_node, move=direction, g=tentative_g, h=child_h, f=child_f)
            counter += 1
            heapq.heappush(open_heap, PrioritizedItem(child_node.f, counter, child_key, child_node))
            open_map[child_key] = child_node

        max_frontier_size = max(max_frontier_size, len(open_heap))

    # terminou sem solução
    end_time = time.perf_counter()
    result = {
        "path": None,
        "path_length": None,
        "nodes_visited": nodes_visited,
        "time_seconds": end_time - start_time,
        "max_frontier_size": max_frontier_size,
        "status": "no_solution_or_max_iterations_reached"
    }
    _dump_frontier_visited(open_map, closed_map, save_path)
    return {"result": result, "frontier_file": save_path}

def _dump_frontier_visited(open_map: Dict[Tuple[int, ...], Node],
                           closed_map: Dict[Tuple[int, ...], Node],
                           json_path: str) -> None:
    def format_3x3(state: list[int]) -> list[list[int]]:
        return [state[i:i+3] for i in range(0, 9, 3)]

    frontier_dump = [{"state": format_3x3(list(key))} for key in open_map]
    visited_dump = [{"state": format_3x3(list(key))} for key in closed_map]

    out = {
        "frontier_count": len(frontier_dump),
        "visited_count": len(visited_dump),
        "frontier": frontier_dump,
        "visited": visited_dump
    }

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)