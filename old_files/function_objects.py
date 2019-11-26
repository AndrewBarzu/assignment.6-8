from new_files.domain import *
"""
THESE CLASSES ARE MADE ONLY TO OPERATE WITH THE FUNCTIONS THAT ARE ALREADY BUILD IN
THEY ONLY RUN AFTER VALIDATION, AND THEY OPERATE DIRECTLY WITH THE LIST
"""

class AssignObject:
    def __init__(self, grades: list, assignment: Grade):
        self._grades = grades
        self._assignment = assignment

    def execute(self):
        self._grades.append(self._assignment)

    def undo(self):
        self._grades.remove(self._assignment)

class GradeFunctionObject:
    def __init__(self, grade: Grade, new_grade):
        self._grade = grade
        self._new_grade = new_grade

    def execute(self):
        self._grade.grade = self._new_grade

    def undo(self):
        self._grade.grade = None

class AddObject:
    def __init__(self, list, object):
        self._list = list
        self._object = object

    def execute(self):
        self._list.append(self._object)

    def undo(self):
        self._list.remove_object(self._object)

class RemoveObject:
    def __init__(self, _list: list, _object, grade_list: list,  deleted_grades: list):
        self._list = _list
        self._object = _object
        self._grade_list = grade_list
        self._deleted_grades = deleted_grades

    def execute(self):
        self._list.remove(self._object)
        for grade in self._deleted_grades:
            self._grade_list.remove(grade)

    def undo(self):
        self._list.append(self._object)
        self._grade_list.extend(self._deleted_grades)

class UpdateOBject:
    def __init__(self, list, index, object):
        self._list = list
        self._index = index
        self._object = object
        self._old_object = self._list[self._index]

    def execute(self):
        self._list[self._index] = self._object

    def undo(self):
        self._list[self._index] = self._old_object
