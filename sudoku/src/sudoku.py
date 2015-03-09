import random
import copy
import numpy
import sys
import ConfigParser

"""config settings"""
config = ConfigParser.RawConfigParser()
config.read('./default.cfg')


class SudokuGenerator(object):

    def __init__(self):
        self.grid_number = int(config.get('GridNumber', 'number'))
        self.grid = self.grid_number * self.grid_number


    """replaces zeros with underscore(_)"""
    def display_board(self, board):
        for row in board:
            print ' '.join([str(n or '_') for n in row])

    """removes positions from the sudoku board"""
    def remove_cells(self, board, num_cells):
        if num_cells != 0:
            col = random.randint(0, self.grid - 1)
            row = random.randint(0, self.grid - 1)
            if board[row][col] == 0:
                return self.remove_cells(board, num_cells)
            else:
                board[row][col] = 0
                return self.remove_cells(board, num_cells - 1)

        else:
            return board

    """transposes the sudoku board while still retaining validity"""
    def transpose_board(self, board):
        transposed = numpy.array(zip(*board))
        return transposed

    """switches mid-section of the sudoku board with the last section while still retaining"""
    """retaining validity"""
    def shuffle_board(self, board):
        board_swap = copy.deepcopy(board)
        for i in range(self.grid_number, self.grid):
            if i+self.grid_number < self.grid:
                for j in range(self.grid):
                    a = board_swap[i][j]
                    b = board_swap[i+self.grid_number][j]
                    board_swap[i][j], board_swap[i+self.grid_number][j] = b, a
        return board_swap

    """constructs a fully solved sudoku board"""
    def construct_board(self):
        while True:
            try:
                board_layout = [['_'] * self.grid for i in range(self.grid)]
                rows = [set(range(1, self.grid + 1)) for i in range(self.grid)]
                columns = [set(range(1, self.grid + 1)) for i in range(self.grid)]
                blocks = [set(range(1, self.grid + 1)) for i in range(self.grid)]

                for i in range(self.grid):
                    for j in range(self.grid):
                        choices = rows[i].intersection(columns[j]).intersection(blocks[(i/self.grid_number)*self.grid_number + j/self.grid_number])
                        choice = random.choice(list(choices))
                        board_layout[i][j] = choice
                        rows[i].remove(choice)
                        columns[j].remove(choice)
                        blocks[(i/self.grid_number)*self.grid_number + j/self.grid_number].remove(choice)

                return board_layout

            except IndexError:
                pass

    def start_sudoku_generation(self, complexity):
        board_base = self.construct_board()
        board_shuffled = self.shuffle_board(board_base)
        board_shuffled_and_transposed = self.transpose_board(board_shuffled)
        board_removed_cells = self.remove_cells(board_shuffled_and_transposed, complexity)
        self.display_board(board_removed_cells)

    def sudoku_generator(self):
        if len(sys.argv) != 2:
            print '[INFO]: Usage is - "python sudoku/src/sudoku.py [easy|intermediate|difficult]"'
        else:
            try:
                complexity = int(config.get('Difficulty', str(sys.argv[1])))
                self.start_sudoku_generation(complexity)

            except ConfigParser.NoOptionError, err:
                print '[ERROR]: {0}. Choose between [easy|intermediate|difficult]'.format(str(err))


if __name__ == "__main__":
    SudokuGenerator().sudoku_generator()

