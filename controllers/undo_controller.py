class UndoController:
    def __init__(self):
        self._undo_stack = []
        self._redo_stack = []
        self._flag = False

    def recordOp(self, operation):
        if self._flag is True:
            return
        self._undo_stack.append(operation)

    def undo(self):
        self._flag = True

        object = self._undo_stack.pop()
        print(object)
        object.undo()
        self._flag = False

    def redo(self):
        self._flag = True
        self._redo_stack.pop().redo()
        self._flag = False

class FunctionCall:
    def __init__(self, function, *params):
        self._function = function
        self._params = params

    def call(self):
        self._function(*self._params)

class Operation:
    def __init__(self, undoCall, redoCall):
        self._undo = undoCall
        self._redo = redoCall

    def undo(self):
        self._undo.call()

    def redo(self):
        self._redo.call()

class CascadingOperation:
    def __init__(self, operations: list):
        self._operations = operations

    def undo(self):
        for op in self._operations:
            op.undo()

    def redo(self):
        for op in self._operations:
            op.redo()