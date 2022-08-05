import re

import PySimpleGUI as sg


# base class for custom ui elements
class UIObject:
    
    registry = {}

    def __init__(self, graph, name, initialize=False):
        self._graph = graph
        self._name = name
        self._initialize = initialize
        UIObject.registry[name] = self

    def markedInitialize(self):
        return self._initialize

    # static method for render object
    @staticmethod
    def initRender():

        # render registered initial ui objects
        # list must be a copy since registry changes during rendering
        initObjs = list(UIObject.registry.values())
        for o in initObjs:
            if o.markedInitialize():
                o.render()

    # search function for custom ui elements by name
    @staticmethod
    def resolve(name):
        return UIObject.registry[name]


# custom file browser
class FileBrowserButton(UIObject):

    TYPE_LOAD = 1
    TYPE_SAVE = 2

    def __init__(self, graph, name):
        super().__init__(graph, name)

    @staticmethod
    def create(name, text, type, enabled):
        if type == FileBrowserButton.TYPE_LOAD:
            obj = sg.FileBrowse(button_text=text, file_types=[("Pattern", "*.lgp")], key=name)
        else:
            obj = sg.FileSaveAs(button_text=text, file_types=[("Pattern", "*.lgp")], key=name)
        FileBrowserButton(obj, name)
        return obj

    def enable(self, flag):
        self._graph.update(disabled=(not flag))


# custom UI component
class Button(UIObject):

    def __init__(self, graph, name):
        super().__init__(graph, name)

    @staticmethod
    def create(name, text, enabled):
        obj = sg.Button(text, key=name, disabled=(not enabled))

        Button(obj, name)
        return obj

    def enable(self, flag):
        self._graph.update(disabled=(not flag))


# custom UI component
class MinMaxInput(UIObject):

    RE_POSITIVE_NUMBER = "^[0-9]+$"

    def __init__(self, graph, name):
        super().__init__(graph, name)

    @staticmethod
    def create(name, text, validation):

        obj = sg.Input(key=name, default_text=text, enable_events=validation, size=3)
        MinMaxInput(obj, name)
        return obj

    def validate(self, values, min, max):
        v = values[self._name]

        if len(v) > 0:
            mo = re.match(MinMaxInput.RE_POSITIVE_NUMBER, v)
            if mo:
                v = int(v)
                if v > max:
                    v = max
            else:
                v = min
        else:
            v = min

        self._graph.update(str(v))

    def setValue(self, value):
        self._graph.update(str(value))

    def enable(self, flag):
        self._graph.update(disabled=(not flag))


# custom UI component
class Text(UIObject):

    def __init__(self, graph, name):
        super().__init__(graph, name)

    @staticmethod
    def create(name):

        obj = sg.Text('', key=name, auto_size_text=True)
        Text(obj, name)
        return obj

    def setStatusText(self, text):
        self._graph.Update(text)
