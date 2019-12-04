from controllers.grade_controller import GradeController
from controllers.undo_controller import *
from new_files.exceptions import *
from new_files.better_repo import Repository
from new_files.domain import Student
from copy import deepcopy
from new_files.validation_service import StudentValidator

class StudentController:
    def __init__(self, studentRepo: Repository, undoController: UndoController, gradeController: GradeController):
        self._studentrepo = studentRepo
        self._undoController = undoController
        self._gradeController = gradeController
        self._studentValidator = StudentValidator()

    def add_student(self, sid, name, group):
        """
        Adds a new student

        :param sid: the id of the student
        :param name: the name of the student
        :param group: the group fom which the student takes part of
        :return None: success
        :raises NotUnique: id is not unique
        :raises NotAnInt: id is not an int or the group is not an int
        :raises NotAString: name is not a string
        """
        student = Student(sid, name, group)
        self._studentValidator.validate_student(student)
        self._studentrepo.add_object(student)
        redo = FunctionCall(self.add_student, sid, name, group)
        undo = FunctionCall(self.remove_student, sid)
        operation = Operation(undo, redo)
        self._undoController.recordOp(operation)

    def remove_student(self, sid):
        """
        Removes a student by it's id

        :param sid: the id of the student
        :return None: success
        :raises NotAnInt: the id is not an int
        :raises NotExistent: the student does not exist
        """
        self._studentValidator.validate_ID(sid)
        operations = []
        idx = self._studentrepo.find_object(sid)
        student = self._studentrepo[idx]
        self._studentrepo.remove_object(student.id)
        redo = FunctionCall(self.remove_student, student.id)
        undo = FunctionCall(self.add_student, student.id, student.name, student.group)
        operation = Operation(undo, redo)
        operations.append(operation)
        operations.extend(self._gradeController.remove_student_grade(sid))
        cascade = CascadingOperation(operations)
        self._undoController.recordOp(cascade)

    def update_student(self, sid, new_id, new_name, new_group):
        """
        Updates the id, name and/or group of a student

        :param sid: the id of the student
        :param new_id: the new id (remains the same if left empty)
        :param new_name: the new name (remains the same if left empty)
        :param new_group: the new group (remains the same if left empty)
        :return None: success
        :raises NotAnInt: id, new_id or group are not ints
        :raises NotAString: the name is not a string
        :raises NotExistent: student does not exist
        :raises NotUnique: new id is not unique
        :raises NoUpdate: student was not changed
        """
        self._studentValidator.validate_ID(sid)
        idx = self._studentrepo.find_object(sid)
        if idx is None:
            raise NotExistent("Student does not exist")
        if new_id.isnumeric() or new_id == '':
            for s in self._studentrepo:
                if s.id == new_id and s.id != sid:
                    raise NotUnique("ID should be unique!")
        else:
            raise NotAnInt("ID should be an int!")
        old_student = self._studentrepo[idx]
        updated = 0
        student = []
        if new_id != '':
            student.append(new_id)
            updated = 1
        else:
            student.append(old_student.id)
        if new_name != '':
            student.append(new_name)
            updated = 1
        else:
            student.append(old_student.name)
        if new_group != '':
            student.append(new_group)
            updated = 1
        else:
            student.append(old_student.group)
        if updated == 0:
            raise NoUpdate("No changes made!")
        student = Student(student[0], student[1], student[2])
        operations = []
        self._studentrepo.update_object(self._studentrepo.find_object(sid), student)
        redo = FunctionCall(self.update_student, sid, student.id, student.name, student.group)
        undo = FunctionCall(self.update_student, student.id, old_student.id, old_student.name, old_student.group)
        operation = Operation(undo, redo)
        operations.append(operation)
        operations.append(self._gradeController.update_student_id(old_student.id, student.id))
        cascade = CascadingOperation(operations)
        self._undoController.recordOp(cascade)

    def get_students(self):
        return deepcopy(self._studentrepo.get_objects())

    def show_students(self):
        return [str(student) for student in self.get_students()]