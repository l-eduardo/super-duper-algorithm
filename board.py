from __future__ import annotations
from enum import Enum
from math import sqrt
import random
from typing import List, Tuple


class Direction(Enum):
    Left = 1
    Right = 2
    Up = 3
    Down = 4

class Board:
    def __init__(self, game_size, board = None) -> None:
        self.game_size = game_size
        
        if board is not None:
            if sqrt(len(board)) != game_size:
                raise ValueError("Board size does not match game size.")

            self.board = board
            
            return
        
        self.board = [i for i in range(1, game_size * game_size)] + [-1]

    @classmethod
    def parse(cls, board: list[int]) -> Board:
        board = Board(board=board, game_size=sqrt(len(board)))

        return board
    
    def set_board(self, board: list[int]) -> None:
        if len(board) != self.game_size * self.game_size:
            raise ValueError("Board size does not match game size.")
        
        self.board = board.copy()

    def get_board(self) -> List[int]:
        return self.board
    
    def possible_next_states(self) -> List[Board]:
        next_states = []

        for move in self.possible_moves():
            new_board = Board(self.game_size, self.board.copy())
            
            if move == Direction.Left:
                new_board.move_left()
            elif move == Direction.Right:
                new_board.move_right()
            elif move == Direction.Up:
                new_board.move_up()
            elif move == Direction.Down:
                new_board.move_down()
            
            next_states.append(new_board)

        return next_states
    
    def shuffle_board(self) -> None:
        random.shuffle(self.board)

    def is_soluted(self) -> bool:
        return self.board == [i for i in range(1, len(self.board))] + [-1]
    #moves

    def possible_moves(self) -> List[Direction]:
        moves = []

        directions = [Direction.Left, Direction.Right, Direction.Up, Direction.Down]
        
        for direction in directions:
            if (direction == Direction.Left and self.can_move_left()
                or direction == Direction.Up and  self.can_move_up()
                or direction == Direction.Down and  self.can_move_down()
                or direction == Direction.Right and self.can_move_right()):
                moves.append(direction)
            
        return moves
    
    def get_empty_index(self):
        return self.board.index(-1)

    def can_move_down(self):
        return self.get_empty_index() < self.game_size * (self.game_size - 1)

    def can_move_up(self):
        return self.get_empty_index() >= self.game_size

    def can_move_right(self):
        return self.get_empty_index() % self.game_size != self.game_size - 1

    def can_move_left(self):
        return self.get_empty_index() % self.game_size != 0
    
    def move_up(self):
        if not self.can_move_up():
            raise ValueError("Cannot move up")
        
        empty_index = self.get_empty_index()
        target_idx = empty_index - self.game_size
        self.board[empty_index], self.board[target_idx] = self.board[target_idx], self.board[empty_index]

    def move_down(self):
        if not self.can_move_down():
            raise ValueError("Cannot move down")
        
        empty_index = self.get_empty_index()
        target_idx = empty_index + self.game_size
        self.board[empty_index], self.board[target_idx] = self.board[target_idx], self.board[empty_index]

    def move_left(self):
        if not self.can_move_left():
            raise ValueError("Cannot move left")
        
        empty_index = self.get_empty_index()
        target_idx = empty_index - 1

        self.board[empty_index], self.board[target_idx] = self.board[target_idx], self.board[empty_index]
    
    def move_right(self):
        if not self.can_move_right():
            raise ValueError("Cannot move right")
        
        empty_index = self.get_empty_index()
        target_idx = empty_index + 1
        self.board[empty_index], self.board[target_idx] = self.board[target_idx], self.board[empty_index]