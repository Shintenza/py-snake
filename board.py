import random

from enums.cell_type import CellType
from enums.direction import Direction

from typing import List
from cell import Cell
from pygame import Rect, draw, Surface



class Board:
    EMPTY_CELL_COLOR = 116, 242, 107
    SNAKE_CELL_COLOR = 255, 17, 0
    FOOD_CELL_COLOR = 69, 69, 69
    BORDER_COLOR = 242, 242, 242

    BORDER_WIDTH = 5
    STARTING_SNAKE_SIZE = 3


    def __init__(self, screen: Surface, left, top, x_size, y_size, cell_size):
        self.left = left
        self.top = top
        self.x_size = x_size
        self.y_size = y_size
        self.cell_size = cell_size
        self.screen: Surface = screen

        self.board_matrix: List[List[Cell]] = [
            [Cell(row, col) for col in range(x_size)] for row in range(y_size)
        ]

    def get_cell(self, row, col):
        return self.board_matrix[row][col]

    def draw_board(self):
        self.border_box = Rect(
            self.left,
            self.top,
            self.x_size * self.cell_size + 2 * self.BORDER_WIDTH,
            self.y_size * self.cell_size + 2 * self.BORDER_WIDTH,
        )
        game_background = Rect(
            self.left + self.BORDER_WIDTH,
            self.top + self.BORDER_WIDTH,
            self.x_size * self.cell_size,
            self.y_size * self.cell_size,
        )

        draw.rect(self.screen, self.BORDER_COLOR, self.border_box)
        draw.rect(self.screen, self.EMPTY_CELL_COLOR, game_background)

        for row in range(self.y_size):
            for col in range(self.x_size):
                cell = Rect(
                    self.BORDER_WIDTH + self.left + col * (self.cell_size),
                    self.BORDER_WIDTH + self.top + row * (self.cell_size),
                    self.cell_size,
                    self.cell_size,
                )

                if self.board_matrix[row][col].cell_type == CellType.FOOD:
                    draw.rect(self.screen, self.FOOD_CELL_COLOR, cell)
                if self.board_matrix[row][col].cell_type == CellType.SNAKE_PART:
                    draw.rect(self.screen, self.SNAKE_CELL_COLOR, cell)

    def starting_snake_cells(self):
        col = self.x_size // 2
        row = self.y_size // 2

        cell = self.board_matrix[row][col]

        cells = [cell]

        for _ in range(self.STARTING_SNAKE_SIZE):
            cell = self.get_next_cell(cell, Direction.LEFT)
            cells.append(cell)

        return cells

    
    def get_next_cell(self, cell: Cell, direction: Direction):
        cell_row = cell.row
        cell_col = cell.col


        if direction == Direction.LEFT and cell_col > 0:
            return self.board_matrix[cell_row][cell_col-1]
        elif direction == Direction.RIGHT and cell_col < self.x_size:
            return self.board_matrix[cell_row][cell_col+1]
        elif direction == Direction.UP and cell_row > 0:
            return self.board_matrix[cell_row - 1][cell_col]
        elif direction == Direction.DOWN and cell_row < self.y_size:
            return self.board_matrix[cell_row + 1][cell_col]
        else: 
            raise IndexError



    def generate_food(self):
            while True:
                col = random.randint(0, self.x_size - 1)
                row = random.randint(0, self.y_size - 1)
                cell = self.board_matrix[row][col]

                if cell.cell_type == CellType.EMPTY:
                    cell.cell_type = CellType.FOOD
                    self.current_food_position =  (row, col)
                    break

    def remove_food(self):
        food_cell = self.board_matrix[self.current_food_position[0]][self.current_food_position[1]]
        food_cell.cell_type = CellType.EMPTY


    @property
    def bottom_left_point(self):
        return self.border_box.bottomleft
