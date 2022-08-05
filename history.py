import hashlib
from model import Matrix


# history list of game
class History:

    def __init__(self):
        self._generationCounter = 0
        self._generationList = []
        self._finished = False
        self._loop = None

    def isFinished(self):
        return self._finished

    def getLoop(self):
        return self._loop

    def addEntry(self, entry):
        ix = self._searchEntry(entry)
        self._generationCounter += 1
        if ix >= 0:
            # entry exists
            if not self._finished:
                # add entry only once and finish
                self._finished = True
                self._loop = (ix, self.generationId() - 1)
                self._generationList.append(entry)
            else:
                pass
        else:
            # new entry
            self._generationList.append(entry)

    def _searchEntry(self, entry):
        ix = 0
        for e in self._generationList:
            if e.md5hash == entry.md5hash:
                return ix
            ix += 1
        return -1

    def generationId(self):
        return self._generationCounter - 1

    def getGenerationAsString(self, id):
        if id < self._generationCounter:
            return self._generationList[id].lineup
        else:
            return None


# one step of game
class HistoryEntry:

    def __init__(self, mx):
        self.lineup = mx.asString()
        md5 = hashlib.md5()
        md5.update(self.lineup.encode())
        self.md5hash = md5.hexdigest()
