import marshal

from board import Board
from common import Direction, LifeStatus
from guielems import UIObject
from lifegui import LifeGUI


# Info about PySimpleGUI can be found at https://www.pysimplegui.org/en/latest/cookbook/
# Info about Conways Game of Life https://de.wikipedia.org/wiki/Conways_Spiel_des_Lebens

class GameController:

    def __init__(self, sizex=70, sizey=25):
        self._autoRun = False
        self._board = Board(dimx=sizex, dimy=sizey)
        self._mx = self._board.getMatrix()
        self._lg = LifeGUI(start_lifes=50, dimx=sizex, dimy=sizey)

        self._uiButtonRun = UIObject.resolve(LifeGUI.ELEM_BTN_RUN)
        self._uiButtonStop = UIObject.resolve(LifeGUI.ELEM_BTN_STOP)
        self._uiBoard = UIObject.resolve(LifeGUI.ELEM_UI_BOARD)
        self._uiFieldStatus = UIObject.resolve(LifeGUI.ELEM_TEXT_STATUS)
        self._uiFieldStartLifes = UIObject.resolve(LifeGUI.ELEM_INPUT_START_LIFES)
        self._uiFieldGeneration = UIObject.resolve(LifeGUI.ELEM_INPUT_GENERATION)
        self._uiButtonLeft = UIObject.resolve(LifeGUI.ELEM_BTN_LEFT)
        self._uiButtonRight = UIObject.resolve(LifeGUI.ELEM_BTN_RIGHT)
        self._uiButtonTop = UIObject.resolve(LifeGUI.ELEM_BTN_TOP)
        self._uiButtonBottom = UIObject.resolve(LifeGUI.ELEM_BTN_BOTTOM)
        self._uiButtonRandom = UIObject.resolve(LifeGUI.EV_BTN_RANDOMSET)
        self._uiButtonClear = UIObject.resolve(LifeGUI.EV_BTN_CLEAR)
        self._uiButtonLoad = UIObject.resolve(LifeGUI.ELEM_BTN_LOADPATTERN)
        self._uiButtonSave = UIObject.resolve(LifeGUI.ELEM_BTN_SAVEPATTERN)
        self._uiButtonGeneration = UIObject.resolve(LifeGUI.ELEM_BTN_GENERATION)
        self.loop()

    def setAutorun(self, flag):
        self._autoRun = flag
        self._uiButtonRun.enable(not flag)
        self._uiButtonStop.enable(flag)
        self._uiButtonLeft.enable(not flag)
        self._uiButtonRight.enable(not flag)
        self._uiButtonTop.enable(not flag)
        self._uiButtonBottom.enable(not flag)
        self._uiButtonLoad.enable(not flag)
        self._uiButtonSave.enable(not flag)
        self._uiButtonRandom.enable(not flag)
        self._uiButtonClear.enable(not flag)
        self._uiFieldStartLifes.enable(not flag)
        self._uiFieldGeneration.enable(not flag)
        self._uiButtonGeneration.enable(not flag)

    def isAutorun(self):
        return self._autoRun

    def configChanged(self):
        self.setAutorun(False)
        self._board.resetStatistics()

    def savePattern(self, values):
        p = self._mx.asString()
        fn = values[LifeGUI.ELEM_INPUT_SAVEPATTERN]
        fp = open(fn, "wb")
        b = marshal.dumps(p)
        fp.write(b)
        fp.close()

    def loadGeneration(self, values):
        id = int(values[LifeGUI.ELEM_INPUT_GENERATION])
        lineup = self._board.getHistory().getGenerationAsString(id)
        self._mx.fromString(lineup)
        self._uiFieldGeneration.setValue(0)

    def loadPattern(self, values):
        fn = values[LifeGUI.ELEM_INPUT_LOADPATTERN]
        fp = open(fn, "rb")
        ba = bytearray(fp.read())
        fp.close()
        p = marshal.loads(ba)
        self._mx.fromString(p)

    def toggleCellStatus(self, values):
        (x, y) = self._uiBoard.getXYCell(values)
        if self._mx.getCell(x, y) == LifeStatus.ST_LIFE:
            self._mx.setCell(x, y, LifeStatus.ST_EMPTY)
        else:
            self._mx.setCell(x, y, LifeStatus.ST_LIFE)

    # config change events
    CC_EVENTS = [
        LifeGUI.EV_BTN_TOP, LifeGUI.EV_BTN_BOTTOM,
        LifeGUI.EV_BTN_RIGHT, LifeGUI.EV_BTN_LEFT,
        LifeGUI.EV_BTN_CLEAR, LifeGUI.EV_BTN_RANDOMSET, LifeGUI.EV_UI_BOARD,
        LifeGUI.EV_INPUT_SAVEPATTERN, LifeGUI.EV_INPUT_LOADPATTERN,
        LifeGUI.EV_BTN_GENERATION
    ]

    def loop(self):
        while True:
            event, values = self._lg.readEvent(timeout=250)
            if event == LifeGUI.EV_WIN_CLOSE:
                break
            # skip event for timeout when autorun is off
            elif not self._autoRun and event == LifeGUI.EV_BTN_TIMEOUT:
                continue
            else:
                if event in (LifeGUI.ELEM_BTN_TOP, LifeGUI.ELEM_BTN_BOTTOM, LifeGUI.ELEM_BTN_RIGHT, LifeGUI.ELEM_BTN_LEFT):
                    # TODO !
                    if self._uiButtonLeft.isEnabled() and \
                            self._uiButtonRight.isEnabled() and \
                            self._uiButtonTop.isEnabled() and \
                            self._uiButtonBottom.isEnabled():
                        self._mx.move(event)
                elif event == LifeGUI.EV_BTN_TIMEOUT:
                    self._board.nextGeneration()
                    if self._board.getHistory().isFinished():
                        self.setAutorun(False)
                elif event == LifeGUI.EV_INPUT_START_LIFES:
                    self._uiFieldStartLifes.validate(values, 0, 100)
                elif event == LifeGUI.EV_INPUT_GENERATION:
                    gid = self._board.getHistory().generationId()
                    self._uiFieldGeneration.validate(values, 0, gid)
                elif event == LifeGUI.EV_BTN_GENERATION:
                    self.loadGeneration(values)
                elif event == LifeGUI.EV_BTN_RUN:
                    self._board.nextGeneration()
                    self.setAutorun(True)
                elif event == LifeGUI.EV_BTN_STEP:
                    self._board.nextGeneration()
                    self.setAutorun(False)
                elif event == LifeGUI.EV_BTN_STOP:
                    self.setAutorun(False)
                elif event == LifeGUI.EV_BTN_CLEAR:
                    self._mx.clear()
                elif event == LifeGUI.EV_BTN_RANDOMSET:
                    self._mx.random(int(values[LifeGUI.ELEM_INPUT_START_LIFES]))
                elif event == LifeGUI.EV_UI_BOARD:
                    self.toggleCellStatus(values)
                elif event == LifeGUI.EV_INPUT_SAVEPATTERN:
                    self.savePattern(values)
                elif event == LifeGUI.EV_INPUT_LOADPATTERN:
                    self.loadPattern(values)
                else:
                    # should not happen
                    print("invalid event: " + event)

                if event in GameController.CC_EVENTS and not self.isAutorun():
                    self.configChanged()

                # update all ui elements
                self._uiBoard.update(self._mx.asTable(), values[LifeGUI.ELEM_GEN_INFO])
                self._uiFieldStatus.setStatusText(self._board.statusAsString())

        self._lg.winClose()


gc = GameController()
