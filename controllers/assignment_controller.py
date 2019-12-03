from new_files.better_repo import Repository
from controllers.grade_controller import GradeController
from controllers.undo_controller import *
from new_files.domain import Assignment
from copy import deepcopy
from new_files.exceptions import *
from new_files.validation_service import AssignmentValidator

class AssignmentController:
    def __init__(self, assignmentRepo: Repository, gradeController: GradeController, undoController: UndoController):
        self._assignmentRepo = assignmentRepo
        self._gradeController = gradeController
        self._undoController = undoController
        self._assignmentValidator = AssignmentValidator()

    def add_assignment(self, aid, desc, day, month, year):
        assignment = Assignment(aid, desc, year, month, day)
        self._assignmentValidator.validate_assignment(assignment)
        self._assignmentRepo.add_object(assignment)
        redo = FunctionCall(self.add_assignment, aid, desc, day, month, year)
        undo = FunctionCall(self.remove_assignment, aid)
        operation = Operation(undo, redo)
        self._undoController.recordOp(operation)

    def remove_assignment(self, aid):
        self._assignmentValidator.validate_ID(aid)
        operations = []
        idx = self._assignmentRepo.find_object(aid)
        assignment = self._assignmentRepo[idx]
        self._assignmentRepo.remove_object(aid)
        redo = FunctionCall(self.remove_assignment, aid)
        undo = FunctionCall(self.add_assignment, assignment.id, assignment.description, str(assignment.deadline.day),
                            str(assignment.deadline.month), str(assignment.deadline.year))
        operation = Operation(undo, redo)
        operations.append(operation)
        operations.extend(self._gradeController.remove_assignment_grade(aid))
        cascade = CascadingOperation(operations)
        self._undoController.recordOp(cascade)

    def update_assignment(self, aid, new_aid, new_desc, new_day, new_month, new_year):
        if not aid.isnumeric():
            raise NotAnInt("ID should be an int!")
        idx = self._assignmentRepo.find_object(aid)
        if idx is None:
            raise NotExistent("Assignment does not exist!")

        if (new_aid.isnumeric() or new_aid == '') and new_aid != aid:
            for assig in self._assignmentRepo:
                if assig.id == new_aid:
                    raise NotUnique("ID should be unique!")
        else:
            raise NotAnInt("ID should be an int!")
        updated = 0
        assignment = []
        old_assignment = self._assignmentRepo[idx]
        if new_aid != '':
            assignment.append(new_aid)
            updated = 1
        else:
            assignment.append(old_assignment.id)
        if new_desc != '':
            assignment.append(new_desc)
            updated = 1
        else:
            assignment.append(old_assignment.description)
        if new_year != '':
            assignment.append(new_year)
            updated = 1
        else:
            assignment.append(old_assignment.deadline.year)
        if new_month != '':
            assignment.append(new_month)
            updated = 1
        else:
            assignment.append(old_assignment.deadline.month)
        if new_day != '':
            assignment.append(new_day)
            updated = 1
        else:
            assignment.append(old_assignment.deadline.day)
        if updated == 0:
            raise NoUpdate("No changes made!")
        assignment = Assignment(assignment[0], assignment[1], assignment[2], assignment[3], assignment[4])
        operations = []
        self._assignmentRepo.update_object(idx, assignment)
        redo = FunctionCall(self.update_assignment, aid, assignment.id, assignment.description, str(assignment.deadline.day),
                                                   str(assignment.deadline.month), str(assignment.deadline.year))
        undo = FunctionCall(self.update_assignment, assignment.id, old_assignment.id, old_assignment.description,
                                                   str(old_assignment.deadline.day), str(old_assignment.deadline.month), str(old_assignment.deadline.year))
        operations.append(Operation(undo, redo))
        operations.append(self._gradeController.update_assignment_id(old_assignment.id, new_aid))
        cascade = CascadingOperation(operations)
        self._undoController.recordOp(cascade)

    def get_assignments(self):
        return deepcopy(self._assignmentRepo.get_objects())

    def show_assignments(self):
        return [str(assignment) for assignment in self.get_assignments()]