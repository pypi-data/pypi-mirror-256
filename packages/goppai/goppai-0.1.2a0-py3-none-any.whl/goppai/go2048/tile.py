"""Board tile module"""


class Tile:
    """board tile"""

    def __init__(self) -> None:
        self.__value = 0

    def setvalue(self, value):
        """set tile value"""
        self.__value = value
        return self

    def getvalue(self):
        """get tile value"""
        return self.__value

    def move_to(self, tile):
        """move tile value"""
        if tile.getvalue() == 0:
            tile.setvalue(self.__value)
            self.__value = 0
            return self.__value

        if tile.getvalue() == self.__value:
            tile.setvalue(self.__value + tile.getvalue())
            self.__value = 0
            return tile.getvalue()

        return -1
