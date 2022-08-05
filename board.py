from common import *
from history import History, HistoryEntry
from model import Matrix


# this is the board, it contains the state machine for Game of Life and the statistics
class Board:

    def __init__(self, dimx=20, dimy=20):
        self._mx = Matrix(dimx, dimy)
        self._history = None
        self.resetStatistics()

    def resetStatistics(self):
        self._history = History()
        self._history.addEntry(HistoryEntry(self._mx))

    def getMatrix(self):
        return self._mx

    # get history
    def getHistory(self):
        return self._history

    # get status text
    def statusAsString(self):

        (life, born, dead) = self._mx.countStatus()

        actStatus = \
            "Generation (" + str(self._history.generationId()) + ")" + \
            "   life: " + str(life) + \
            " / born: " + str(born) + \
            " / dead: " + str(dead) + \
            "   "

        finishStatus = ""
        if self._history.isFinished():

            # check if history contains a looping state
            loop = self._history.getLoop()
            loopStart = loop[0]
            loopEnd = loop[1]

            finishStatus += "board is finished in generation " + str(loopEnd)
            if loopStart != loopEnd:
                finishStatus =  \
                    "board is finished, loop starts in generation " + str(loopStart) + \
                    " and ends in generation " + str(loopEnd)
            else:
                finishStatus = "board is finished in generation " + str(loopEnd)

        return actStatus + finishStatus

    # compute next generation
    def nextGeneration(self):

        sizex = self._mx.sizex
        sizey = self._mx.sizey

        # neighbour count matrix
        nm_mx = [0 for _ in range(sizex*sizey)]

        # two lambda functions:
        # access index in matrix
        nm_ix = lambda ix, iy: ix + iy * sizex
        # check boundary of indices
        nm_bounds = lambda ix, iy: True if 0 <= ix < sizex and 0 <= iy < sizey else False

        for x in range(0, sizex):
            for y in range(0, sizey):
                v = self._mx.getCell(x, y)

                # first we update cell status of born or dead cells to life or empty
                if v == LifeStatus.ST_BORN:
                    v = LifeStatus.ST_LIFE
                    self._mx.setCell(x, y, v)
                elif v == LifeStatus.ST_DEAD:
                    v = LifeStatus.ST_EMPTY
                    self._mx.setCell(x, y, v)

                # second we increment the neighbour count in neighbour cells
                if v == LifeStatus.ST_LIFE:
                    if nm_bounds(x - 1, y - 1): nm_mx[nm_ix(x-1, y-1)] += 1
                    if nm_bounds(x, y - 1):     nm_mx[nm_ix(x,   y-1)] += 1
                    if nm_bounds(x + 1, y - 1): nm_mx[nm_ix(x+1, y-1)] += 1
                    if nm_bounds(x - 1, y):     nm_mx[nm_ix(x-1, y)]   += 1
                    if nm_bounds(x + 1, y):     nm_mx[nm_ix(x+1, y)]   += 1
                    if nm_bounds(x - 1, y + 1): nm_mx[nm_ix(x-1, y+1)] += 1
                    if nm_bounds(x, y + 1):     nm_mx[nm_ix(x,   y+1)] += 1
                    if nm_bounds(x + 1, y + 1): nm_mx[nm_ix(x+1, y+1)] += 1

        # third we process the game rules
        for x in range(0, sizex):
            for y in range(0, sizey):
                v = self._mx.getCell(x, y)
                n = nm_mx[nm_ix(x, y)]
                # process rules
                if v == LifeStatus.ST_LIFE and (n < 2 or n >= 4):  # solitude and overpopulation
                    self._mx.setCell(x, y, LifeStatus.ST_DEAD)  # dead
                if v == LifeStatus.ST_EMPTY and n == 3:  # new population
                    self._mx.setCell(x, y, LifeStatus.ST_BORN)  # new born

        # update history
        self._history.addEntry(HistoryEntry(self._mx))
