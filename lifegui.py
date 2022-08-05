import PySimpleGUI as sg
import guielems as ge
import guiboard as gb
import guimover
from common import *


class LifeGUI:

    EV_BTN_TIMEOUT = "TIMEOUT"
    EV_BTN_STEP    = "STEP"
    EV_BTN_RUN    = "RUN"
    EV_BTN_STOP    = "STOP"
    EV_BTN_CLEAR   = "CLEAR"
    EV_BTN_RANDOMSET = "RANDOMSET"
    EV_BTN_GENERATION = "GENERATION"
    EV_INPUT_GENERATION = "INPUT_GENERATION"
    EV_INPUT_START_LIFES = 'ELEM_START_LIFES'
    EV_UI_BOARD = 'ELEM_BOARD'
    EV_INPUT_LOADPATTERN = 'ELEM_LOADPATTERN'
    EV_INPUT_SAVEPATTERN = 'ELEM_SAVEPATTERN'
    EV_BTN_BOTTOM = Direction.BOTTOM
    EV_BTN_TOP = Direction.TOP
    EV_BTN_LEFT = Direction.LEFT
    EV_BTN_RIGHT = Direction.RIGHT
    EV_WIN_CLOSE = sg.WIN_CLOSED

    ELEM_UI_BOARD = EV_UI_BOARD
    ELEM_INPUT_LOADPATTERN = EV_INPUT_LOADPATTERN
    ELEM_INPUT_SAVEPATTERN = EV_INPUT_SAVEPATTERN
    ELEM_BTN_LOADPATTERN = 'ELEM_BTN_LOADPATTERN'
    ELEM_BTN_SAVEPATTERN = 'ELEM_BTN_SAVEPATTERN'
    ELEM_INPUT_START_LIFES = EV_INPUT_START_LIFES
    ELEM_GEN_INFO = 'ELEM_GEN_INFO'
    ELEM_TEXT_STATUS = 'ELEM_STATUS'
    ELEM_BTN_RUN = EV_BTN_RUN
    ELEM_BTN_STOP = EV_BTN_STOP
    ELEM_INPUT_GENERATION = EV_INPUT_GENERATION
    ELEM_BTN_GENERATION = EV_BTN_GENERATION

    ELEM_BTN_BOTTOM = EV_BTN_BOTTOM
    ELEM_BTN_TOP = EV_BTN_TOP
    ELEM_BTN_LEFT = EV_BTN_LEFT
    ELEM_BTN_RIGHT = EV_BTN_RIGHT

    BS = gb.Cell.BS

    def __init__(self, start_lifes=30, dimx=20, dimy=20):

        self._dimx=dimx
        self._dimy=dimy

        layout = [
            (
                [
                    sg.Canvas(size=(LifeGUI.BS, LifeGUI.BS)),
                    guimover.MoverButton.create(Direction.BOTTOM, dimx * LifeGUI.BS, LifeGUI.BS, Direction.BOTTOM),
                    sg.Canvas(size=(LifeGUI.BS, LifeGUI.BS))
                ],
                [
                    guimover.MoverButton.create(Direction.RIGHT, LifeGUI.BS, dimy * LifeGUI.BS, Direction.RIGHT),
                    gb.Board.create(dimx, dimy, LifeGUI.ELEM_UI_BOARD),
                    guimover.MoverButton.create(Direction.LEFT, LifeGUI.BS, dimy * LifeGUI.BS, Direction.LEFT),
                ],
                [
                    sg.Canvas(size=(LifeGUI.BS, LifeGUI.BS)),
                    guimover.MoverButton.create(Direction.TOP, dimx * LifeGUI.BS, LifeGUI.BS, Direction.TOP),
                    sg.Canvas(size=(LifeGUI.BS, LifeGUI.BS))
                ],
                [ge.Text.create(LifeGUI.ELEM_TEXT_STATUS)],
                [
                    ge.Button.create(LifeGUI.EV_BTN_STEP, 'Step', True),
                    ge.Button.create(LifeGUI.EV_BTN_RUN, 'Run', True),
                    ge.Button.create(LifeGUI.EV_BTN_STOP, 'Stop', False),
                    sg.Checkbox('Generation Info', False, key=LifeGUI.ELEM_GEN_INFO),
                    ge.MinMaxInput.create(LifeGUI.ELEM_INPUT_GENERATION, 0, True),
                    ge.Button.create(LifeGUI.ELEM_BTN_GENERATION, 'Choose Generation', True),
                ],
                [
                    ge.Button.create(LifeGUI.EV_BTN_CLEAR, 'Clear', True),
                    ge.Button.create(LifeGUI.EV_BTN_RANDOMSET, 'Random Set', 'True'),
                    sg.Input(enable_events=True, key=LifeGUI.ELEM_INPUT_LOADPATTERN, visible=False),
                    ge.FileBrowserButton.create(LifeGUI.ELEM_BTN_LOADPATTERN, 'Load', ge.FileBrowserButton.TYPE_LOAD, True),
                    sg.Input(enable_events=True, key=LifeGUI.ELEM_INPUT_SAVEPATTERN, visible=False),
                    ge.FileBrowserButton.create(LifeGUI.ELEM_BTN_SAVEPATTERN, 'Save', ge.FileBrowserButton.TYPE_SAVE, True),
                ],
                [
                    sg.Text('Start lifes in %'),
                    ge.MinMaxInput.create(LifeGUI.ELEM_INPUT_START_LIFES, str(start_lifes), True)
                ]
            )
        ]

        self._layout = layout
        self.window = sg.Window("Conways Game of Life (by Rainer Matzke)", layout)
        self.window.Finalize()

        ge.UIObject.initRender()

    def readEvent(self, timeout=250):
        return self.window.Read(timeout=timeout, timeout_key=LifeGUI.EV_BTN_TIMEOUT)

    def winClose(self):
        self.window.close()
