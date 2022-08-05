import PySimpleGUI as sg

from common import *
from guielems import UIObject


# cell base class
class Cell(UIObject):

    BS = 18

    def __init__(self, graph, x, y):
        super().__init__(graph, 'NONAME')

        self._x = x
        self._y = y


# empty cell
class EmptyCell(Cell):

    def __init__(self, graph, x, y):

        super().__init__(graph, x, y)

    def render(self):

        x = self._x
        y = self._y

        self._graph.draw_rectangle(
            (x * Cell.BS, y * Cell.BS + Cell.BS - 1),
            (x * Cell.BS + Cell.BS - 1, y * Cell.BS),
            line_color="white", fill_color="gray")


# dead cell
class DeadCell(EmptyCell):

    def __init__(self, graph, x, y):
        super().__init__(graph, x, y)

    def render(self):

        x = self._x
        y = self._y

        # TODO change thos
        self._graph.draw_line(
            (x * Cell.BS + Cell.BS / 2, y * Cell.BS + Cell.BS / 8),
            (x * Cell.BS + Cell.BS / 2, y * Cell.BS + Cell.BS * 7 / 8),
            color="white", width=1)
        self._graph.draw_line(
            (x * Cell.BS + Cell.BS / 4, y * Cell.BS + Cell.BS * 3 / 5),
            (x * Cell.BS + Cell.BS * 3 / 4, y * Cell.BS + Cell.BS * 3 / 5),
            color="white", width=1)


# life cell
class LifeCell(Cell):

    def __init__(self, graph, x, y):
        super().__init__(graph, x, y)

    def render(self):

        x = self._x
        y = self._y

        graph = self._graph.draw_rectangle(
            (x * Cell.BS, y * Cell.BS + Cell.BS - 1),
            (x * Cell.BS + Cell.BS - 1, y * Cell.BS),
            line_color="white", fill_color="blue")


# new born cell
class BornCell(LifeCell):

    def __init__(self, graph, x, y):
        super().__init__(graph, x, y)

    def render(self):

        x = self._x
        y = self._y

        graph = self._graph.draw_circle(
            (x * Cell.BS + Cell.BS / 2, y * Cell.BS + Cell.BS / 2), Cell.BS / 4,
            line_color="gray", line_width=1)


# board custom ui element
class Board(UIObject):

    # constructor
    def __init__(self, name, graph, sizex, sizey):
        super().__init__(graph, name, initialize=True)

        self._sizex = sizex
        self._sizey = sizey

    # create object
    @staticmethod
    def create(sizex, sizey, name):
        obj = sg.Graph(
            canvas_size=(sizex * Cell.BS, sizey * Cell.BS),  # in pixel
            graph_bottom_left=(0, 0),
            graph_top_right=(sizex * Cell.BS, sizey * Cell.BS),
            key=name, enable_events=True
        )
        Board(name, obj, sizex, sizey)
        return obj

    # first render
    def render(self):

        m = [[LifeStatus.ST_EMPTY for _ in range(self._sizex)] for _ in range(self._sizey)]
        self.update(m, False)

    # update board by given matrix
    def update(self, matrix, showGenInfo):

        graph = self._graph
        graph.erase()

        dimx = len(matrix[0])
        dimy = len(matrix)

        for x in range(dimx):
            for y in range(dimy):
                status = matrix[y][x]

                if not showGenInfo and status == LifeStatus.ST_DEAD:
                    status = LifeStatus.ST_EMPTY
                elif not showGenInfo and status == LifeStatus.ST_BORN:
                    status = LifeStatus.ST_LIFE

                if status == LifeStatus.ST_LIFE:
                    LifeCell(graph, x, y).render()
                elif status == LifeStatus.ST_DEAD:
                    DeadCell(graph, x, y).render()
                elif status == LifeStatus.ST_EMPTY:
                    EmptyCell(graph, x, y).render()
                elif status == LifeStatus.ST_BORN:
                    BornCell(graph, x, y).render()

    # determine click cell
    def getXYCell(self, values):
        x, y = values[self._name]
        return int(x / Cell.BS), int(y / Cell.BS)
