# sudoku-generator

## Introduction
* Sudoku Generator creates an n^2 * n^2 matrix
* Size of the matrix and difficulty level can be adjusted through the config file

## Strategy
* Create a fully solved sudoku board
* Transpose and shift blocks without affecting validity
* Remove cells based on difficulty level

## Configuration
###### default.cfg
* By default a 9*9 sudoku grid will be generated
* Easy setting = 25 empty cells
* Intermediate setting = 35 empty cells
* Difficult setting = 45 empty cells

## Installation
* git clone https://github.com/southekal/sudoku-generator.git

## Running and Generation
* From the home directory "sudoku-generator" run:
* python sudoku/src/sudoku.py [easy | intermediate | difficult]

## Tests
* From the home directory "sudoku-generator" run:
* python -m unittest discover --pattern 'test.py'  --verbose





