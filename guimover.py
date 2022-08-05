import PySimpleGUI as sg

from common import Direction
from guielems import UIObject
from guimxtransform import Transformer


# custom UI component
class MoverButton(UIObject):

    # button polygon pattern (position from 0 to 8 - 9 pixel)
    # position arrow shows to top
    POLY_COORD = [
        [0, 2],
        [4, 6],
        [8, 2],
        [0, 2],
    ]

    # colors
    COLOR_ENABLED = "gray"
    COLOR_DISABLED = "light gray"

    # rotation info 0, 90, 180, 270 degrees
    ROT = None

    def __init__(self, graph, name, sizeX, sizeY, orientation):

        super().__init__(graph, name, initialize=True)

        self._sizeX = sizeX
        self._sizeY = sizeY
        self._orientation = orientation
        self._bc = MoverButton.COLOR_ENABLED
        self._id = None
        self._enabled = True

        # initialize rotation info
        if not MoverButton.ROT:
            MoverButton.ROT = {
                Direction.BOTTOM: Transformer.ROT_180,
                Direction.RIGHT: Transformer.ROT_90,
                Direction.LEFT: Transformer.ROT_270,
                Direction.TOP: Transformer.ROT_0}

    # create element
    @staticmethod
    def create(name, sizex, sizey, orientation):

        obj = sg.Graph(
            canvas_size=(sizex, sizey),  # in pixel
            graph_bottom_left=(0, 0),
            graph_top_right=(sizex, sizey),
            key=name, enable_events=True
        )

        obj._id = MoverButton(obj, name, sizex, sizey, orientation)
        return obj

    # render element
    def render(self):

        # rotation angle for arrow
        rot = MoverButton.ROT[self._orientation]

        # calculate arrow position in canvas
        if rot == Transformer.ROT_180:
            offx = self._sizeX/2
            offy = 0
        elif rot == Transformer.ROT_90:
            offx = 0
            offy = self._sizeY/2
        elif rot == Transformer.ROT_270:
            offx = 0
            offy = self._sizeY/2
        else:
            offx = self._sizeX/2
            offy = 0

        # resize factor for pixel matrix
        factor = 2

        # process all pixels in polygon
        tl = []
        for t in MoverButton.POLY_COORD:

            (x, y) = Transformer.rotate(t, rot, boxsize=9)
            tl.append((x*factor + offx, y*factor + offy))

        # draw object
        graph = self._graph
        self._id = graph.draw_rectangle((0, self._sizeY), (self._sizeX, 0), line_color="white", fill_color=self._bc)
        graph.draw_polygon(tl, fill_color='white')

    def isEnabled(self):
        return self._enabled

    def enable(self, flag):
        self._enabled = flag
        self._graph.delete_figure(self._id)
        if (flag):
            self._bc = MoverButton.COLOR_ENABLED
        else:
            self._bc = MoverButton.COLOR_DISABLED
        self.render()