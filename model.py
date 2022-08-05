from common import *
import random


class Matrix:

    def __init__(self, sizex, sizey):
        self.sizex = sizex
        self.sizey = sizey
        self._board = None
        self.clear()

    def clear(self):
        self._board = [LifeStatus.ST_EMPTY for _ in range(self.sizex*self.sizey)]

    def random(self, fillLevel):
        # define lambda function for generating random values depending on fill grade
        rv = lambda: LifeStatus.ST_LIFE if random.random() < fillLevel / 100.0 else LifeStatus.ST_EMPTY
        self._board = [rv() for _ in range(self.sizex*self.sizey)]

    # helper for moving table
    OFFSET = {
        Direction.LEFT: (-1, -0),
        Direction.RIGHT: (1, 0),
        Direction.BOTTOM: (0, -1),
        Direction.TOP: (0, 1)
    }

    def move(self, direction):

        sizex = self.sizex
        sizey = self.sizey
        (offx, offy) = Matrix.OFFSET[direction]

        m = Matrix(sizex, sizey)

        for x in range(sizex):
            for y in range(sizey):
                if x+offx < sizex and y+offy < sizey:
                    m.setCell(x+offx, y+offy, self.getCell(x, y))

        self._board = m._board

    def countStatus(self):

        life = 0
        dead = 0
        born = 0

        for x in range(self.sizex):
            for y in range(self.sizey):
                v = self._board[x + y * self.sizex]
                if v == LifeStatus.ST_LIFE:
                    life += 1
                elif v == LifeStatus.ST_BORN:
                    life += 1
                    born += 1
                elif v == LifeStatus.ST_DEAD:
                    dead += 1

        return (life, born, dead)

    def setCell(self, x, y, v):
        if 0 <= x < self.sizex and 0 <= y < self.sizey:
            self._board[x + y * self.sizex] = v

    def getCell(self, x, y):
        if 0 <= x < self.sizex and 0 <= y < self.sizey:
            return self._board[x + y * self.sizex]
        else:
            return None

    def asTable(self):
        table = []
        for y in range(0, self.sizey):
            row = []
            for x in range(0, self.sizex):
                row.append(self.getCell(x, y))
            table.append(row)
        return table

    def fromString(self, strCoded):
        y = -1
        x = -1
        for c in strCoded:
            x += 1
            if c == '/':
                y += 1
                x = 0
            elif c == 'l':
                self.setCell(x, y, LifeStatus.ST_LIFE)
            else:
                self.setCell(x, y, LifeStatus.ST_EMPTY)

    def asString(self):

        codedString = '/'
        for y in range(self.sizey):
            for x in range(self.sizex):
                c = self.getCell(x, y)
                if c == LifeStatus.ST_BORN or c == LifeStatus.ST_LIFE:
                    codedString = codedString+str('l')
                else:
                    codedString = codedString + str('e')
            codedString = codedString + '/'
        return codedString

