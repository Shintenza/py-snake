from enums.cell_type import CellType


class Cell:
    def __init__(self, row: int, column: int):
        self.__row = row
        self.__col = column
        self.__cell_type = CellType.EMPTY

    @property
    def row(self):
        return self.__row

    @property
    def col(self):
        return self.__col

    @property
    def cell_type(self):
        return self.__cell_type

    @cell_type.setter
    def cell_type(self, cell_type: CellType):
        self.__cell_type = cell_type
