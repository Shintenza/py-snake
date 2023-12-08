from typing import List
from cell import Cell

from enums.cell_type import CellType


class Snake:
    def __init__(self, starting_cells:List[Cell]):
        self.snake_parts:List[Cell] = []
        self._snake_head = starting_cells[0]

        for cell in starting_cells:
            cell.cell_type = CellType.SNAKE_PART

        self.snake_parts.extend(starting_cells)



    @property
    def snake_head(self):
        return self._snake_head

    def move(self, next_cell: Cell):
        if next_cell.cell_type != CellType.FOOD:
            popped_cell = self.snake_parts.pop()
            popped_cell.cell_type = CellType.EMPTY

        self._snake_head = next_cell
        self._snake_head.cell_type = CellType.SNAKE_PART
        self.snake_parts.insert(0, next_cell)


    def check_self_bite(self, next_cell: Cell):
        return next_cell.cell_type == CellType.SNAKE_PART

    def __del__(self):
        for cell in self.snake_parts:
            cell.cell_type = CellType.EMPTY
