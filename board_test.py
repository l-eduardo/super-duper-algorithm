import unittest
from board import *

class TestBoardInitialization(unittest.TestCase):
    def setUp(self):
        self.game = Board(3)

    def test_initial_board(self):
        board = Board(3)
        expected_board = [1,2,3,4,5,6,7,8,-1]
        self.assertEqual(board.get_board(), expected_board)

    def test_initial_board_with_board_param(self):
        custom_board = Board.parse([1,2,3,4,5,6,7,8,-1])
        board = Board(3)
        self.assertEqual(board.get_board(), custom_board.get_board())

    def test_get_board_correct(self):
        custom_board = [1,2,3,4,5,6,7,8,-1]
        self.game.set_board(custom_board)
        self.assertEqual(self.game.get_board(), custom_board)

    def test_get_board(self):
        board = self.game.get_board()
        self.assertIsInstance(board, list)

    def test_shuffle_board(self):
        before = self.game.get_board().copy()
        self.game.shuffle_board()
        after = self.game.get_board()
        self.assertNotEqual(before, after)


class TestValidations(unittest.TestCase):
    def setUp(self):
        self.game = Board(3)

    def test_can_move_methods_center(self):
        self.game.set_board([1,2,3,4,-1,5,6,7,8])
        self.assertTrue(self.game.can_move_left())
        self.assertTrue(self.game.can_move_right())
        self.assertTrue(self.game.can_move_up())
        self.assertTrue(self.game.can_move_down())

    def test_can_move_methods_top_left(self):
        self.game.set_board([-1,2,3,4,5,6,7,8,1])
        self.assertFalse(self.game.can_move_left())
        self.assertFalse(self.game.can_move_up())
        self.assertTrue(self.game.can_move_right())
        self.assertTrue(self.game.can_move_down())

    def test_get_empty_index_correct(self):
        self.game.set_board([1,2,3,4,5,6,7,-1,8])
        self.assertEqual(self.game.get_empty_index(), 7)

    def test_get_empty_index(self):
        idx = self.game.get_empty_index()
        self.assertIsInstance(idx, int)


class TestPossibleMoves(unittest.TestCase):
    def setUp(self):
        self.game = Board(3)

    def test_possible_moves_bottom_right(self):
        self.game.set_board([1,2,3,4,5,6,7,8,-1])
        moves = self.game.possible_moves()

        self.assertIn(Direction.Left, moves)
        self.assertIn(Direction.Up, moves)

        self.assertEqual(len(moves), 2)

    def test_possible_moves_top_left(self):
        self.game.set_board([-1,2,3,4,5,6,7,8,1])
        moves = self.game.possible_moves()
        
        self.assertIn(Direction.Right, moves)
        self.assertIn(Direction.Down, moves)

        self.assertEqual(len(moves), 2)

    def test_possible_moves_returns_list(self):
        moves = self.game.possible_moves()
        self.assertIsInstance(moves, list)


class TestMovementExecution(unittest.TestCase):
    def setUp(self):
        self.game = Board(3)

    def test_move_up_success(self):
        self.game.set_board([1,2,3,4,5,6,7,8,-1])
        self.game.move_up()
        self.assertEqual(self.game.get_board(), [1,2,3,4,5,-1,7,8,6])

    def test_move_up_failure(self):
        self.game.set_board([-1,2,3,4,5,6,7,8,1])
        with self.assertRaises(ValueError):
            self.game.move_up()

    def test_move_down_success(self):
        self.game.set_board([-1,2,3,4,5,6,7,8,1])
        self.game.move_down()
        self.assertEqual(self.game.get_board(), [4,2,3,-1,5,6,7,8,1])

    def test_move_down_failure(self):
        self.game.set_board([1,2,3,4,5,6,7,8,-1])
        with self.assertRaises(ValueError):
            self.game.move_down()

    def test_move_left_success(self):
        self.game.set_board([1,2,-1,4,5,6,7,8,3])
        self.game.move_left()
        self.assertEqual(self.game.get_board(), [1,-1,2,4,5,6,7,8,3])

    def test_move_left_failure(self):
        self.game.set_board([-1,2,3,4,5,6,7,8,1])
        with self.assertRaises(ValueError):
            self.game.move_left()

    def test_move_right_success(self):
        self.game.set_board([1,-1,3,4,5,6,7,8,2])
        self.game.move_right()
        self.assertEqual(self.game.get_board(), [1,3,-1,4,5,6,7,8,2])

    def test_move_right_failure(self):
        self.game.set_board([1,2,3,4,5,6,7,8,-1])
        with self.assertRaises(ValueError):
            self.game.move_right()


if __name__ == "__main__":
    unittest.main()