from random import choice

from .tile import Tile


TILE_VALUES = [pow(2, x) for x in range(1, 11)]
DOMINANT_VALUE = [2, 2, 2, 2, 2, 2, 2, 4]


class Board:
    def __init__(self, size=4):
        self.tiles = [[Tile() for _ in range(size)] for _ in range(size)]

    def move_tiles(self, direction):
        delta_y, delta_x = direction

        size = len(self.tiles)

        for y in range(size):
            for x in range(size):

                if self.tiles[y][x].getvalue() == 0:
                    continue

                next_y = y + delta_y
                next_x = x + delta_x

                self.tiles[y][x].move_to(self.tiles[next_y][next_x])

    def reset(self):

        size = len(self.tiles)

        y = choice(range(size))
        x = choice(range(size))
        val = choice(DOMINANT_VALUE)
        self.tiles[y][x].setvalue(val)

        y = choice(range(size))
        x = choice(range(size))
        val = choice(DOMINANT_VALUE)
        self.tiles[y][x].setvalue(val)

    def set_tiles(self, tiles):
        row_size = len(self.tiles)
        col_size = len(self.tiles[0])
        if len(tiles) != row_size or len(tiles[0]) != col_size:
            raise ValueError(
                f"List provided doesn't match the sizes of this board ({row_size} x {col_size})"
            )

        self.tiles = [
            [x.setvalue(y) for x, y in zip(i, j)] for i, j in zip(self.tiles, tiles)
        ]

    def __str__(self) -> str:
        string = ""
        for _ in self.tiles:
            string += "  ".join([f"{x.getvalue()}" for x in _])
            string += "\n"

        return string
