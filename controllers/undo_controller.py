

class UndoController:
    def __init__(self):
        self._undo_stack = []
        self._redo_stack = []
        self._flag = False

    def recordOp(self, operation):
        if self._flag is True:
            return
        self._undo_stack.append(operation)
        self._redo_stack.clear()

    def undo(self):
        if len(self._undo_stack) == 0:
            raise ValueError("No more undo's!")
        self._flag = True
        undoable = self._undo_stack.pop()
        undoable.undo()
        self._redo_stack.append(undoable)
        self._flag = False

    def redo(self):
        if len(self._redo_stack) == 0:
            raise ValueError("No more redo's!")
        self._flag = True
        redoable = self._redo_stack.pop()
        redoable.redo()
        self._undo_stack.append(redoable)
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
        self._operations[0].redo()