import sys
import os
sys.path.append(os.getcwd())

import unittest
from sudoku.src.sudoku import SudokuGenerator
import ConfigParser

config = ConfigParser.RawConfigParser()
config.read('./default.cfg')

class TestSudokuGenerator(unittest.TestCase):

    """setup info"""
    def setUp(self):
        self.sudoku_full_board = SudokuGenerator().transpose_board(SudokuGenerator().shuffle_board(SudokuGenerator().construct_board()))
        self.grid_number = int(config.get('GridNumber', 'number'))
        self.grid = self.grid_number * self.grid_number
        self.easy = int(config.get('Difficulty', 'easy'))
        self.intermediate = int(config.get('Difficulty', 'intermediate'))
        self.difficult = int(config.get('Difficulty', 'difficult'))

    """checks for 81 cells in  a 9*9 sudoku grid"""
    def test_cell_count(self):
        cell_count_holder = []
        for elems in self.sudoku_full_board:
            for elem in elems:
                cell_count_holder.append(elem)
        self.assertEqual(self.grid * self.grid, len(cell_count_holder), '[ERROR]: Total number of cells does not equal {0}'.format(self.grid * self.grid))

    """checks for numbers between 1-9 in a 9*9 sudoku grid"""
    def test_numbers_generated(self):
        number_holder = []
        for elems in self.sudoku_full_board:
            for elem in elems:
                number_holder.append(elem)
        number_holder.sort()
        self.assertEqual(list(set(number_holder)), range(1, self.grid+1), '[ERROR]: Numbers do not lie between 1 and {0}'.format(self.grid))

    """checks for 9 rows in a 9*9 sudoku grid"""
    def test_row_count(self):
        self.assertEqual(self.grid, len(self.sudoku_full_board), '[ERROR]: Number of rows does not equal {0}'.format(self.grid))

    """checks for 9 columns in a 9*9 sudoku grid"""
    def test_col_count(self):
        sudoku_full_board_transposed = zip(*self.sudoku_full_board)
        self.assertEqual(self.grid, len(sudoku_full_board_transposed), '[ERROR]: Number of rows does not equal {0}'.format(self.grid))

    """checks for sum of a row = 45 in a 9*9 sudoku grid (checks for duplicates or out of range numbers)"""
    def test_row_sum(self):
        for rows in self.sudoku_full_board:
            row_holder = []
            for row in rows:
                row_holder.append(row)
            self.assertEqual(sum(range(1, self.grid + 1)), sum(row_holder), '[ERROR]: Sum of rows does not equal {0}'.format(sum(range(1, self.grid + 1))))

    """checks for sum of a column = 45 in a 9*9 sudoku grid (checks for duplicates or out of range numbers)"""
    def test_col_sum(self):
        sudoku_full_board_transposed = zip(*self.sudoku_full_board)
        for cols in sudoku_full_board_transposed:
            col_holder = []
            for col in cols:
                col_holder.append(col)
            self.assertEqual(sum(range(1, self.grid + 1)), sum(col_holder), '[ERROR]: Sum of columns does not equal {0}'.format(sum(range(1, self.grid + 1))))

    """checks for duplicates in a row"""
    def test_row_dup(self):
        for rows in self.sudoku_full_board:
            row_holder = []
            for row in rows:
                row_holder.append(row)
            self.assertEqual(len(set(row_holder)), len(row_holder), '[ERROR]: There are duplicates in a row')

    """checks for duplicates in a column"""
    def test_col_dup(self):
        sudoku_full_board_transposed = zip(*self.sudoku_full_board)
        for cols in sudoku_full_board_transposed:
            col_holder = []
            for col in cols:
                col_holder.append(col)
            self.assertEqual(len(set(col_holder)), len(col_holder), '[ERROR]: There are duplicates in a column')

    """checks for duplicates in a block (3*3 grid)"""
    def test_block_dup(self):
        a = self.sudoku_full_board
        block_holder = []
        for i in range(self.grid):
            block_holder.append(a[i][:self.grid_number])
        b = []
        for i in range(self.grid/self.grid_number):
            b.append(block_holder[i])
        block_holder_val = []
        for j in range(len(b)):
            block_holder_val.append(sum(b[j]))
        self.assertEqual(sum(range(1, self.grid + 1)), sum(block_holder_val), '[ERROR]: Block sum does not equal {0}'.format(sum(range(1, self.grid + 1))))

    """checks removal of cells for an "easy" sudoku game"""
    def test_cells_removed_easy(self):
        board_removed_cells = SudokuGenerator().remove_cells(self.sudoku_full_board, self.easy)
        elem_holder = []
        for elems in board_removed_cells:
            for elem in elems:
                if elem == 0:
                    elem_holder.append(elem)
        self.assertEqual(self.easy, len(elem_holder), '[ERROR]: [EASY] - number of empty cells do not match')

    """checks removal of cells for an "intermediate" sudoku game"""
    def test_cells_removed_intermediate(self):
        board_removed_cells = SudokuGenerator().remove_cells(self.sudoku_full_board, self.intermediate)
        elem_holder = []
        for elems in board_removed_cells:
            for elem in elems:
                if elem == 0:
                    elem_holder.append(elem)
        self.assertEqual(self.intermediate, len(elem_holder), '[ERROR]: [INTERMEDIATE] - number of empty cells do not match')

    """checks removal of cells for a "difficult" sudoku game"""
    def test_cells_removed_difficult(self):
        board_removed_cells = SudokuGenerator().remove_cells(self.sudoku_full_board, self.difficult)
        elem_holder = []
        for elems in board_removed_cells:
            for elem in elems:
                if elem == 0:
                    elem_holder.append(elem)
        self.assertEqual(self.difficult, len(elem_holder), '[ERROR]: [DIFFICULT] - number of empty cells do not match')

    def test_empty_difficulty_parameter(self):
        with self.assertRaises(TypeError):
            SudokuGenerator().remove_cells(self.sudoku_full_board, None)

    def test_passing_difficulty_parameter(self):
        self.assertIsNotNone(SudokuGenerator().remove_cells(self.sudoku_full_board, 25), '[ERROR]: Data is missing even when parameter is provided')

    def test_additional_difficulty_parameter(self):
        with self.assertRaises(TypeError):
            SudokuGenerator().remove_cells(self.sudoku_full_board, None, 25)


if __name__ == '__main__':
    unittest.main()