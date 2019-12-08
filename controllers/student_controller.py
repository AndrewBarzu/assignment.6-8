from new_files.exceptions import *
from new_files.better_repo import Repository
from new_files.domain import Student
from copy import deepcopy
import new_files.validation_service as ValidationServices

class StudentController:
    def __init__(self, studentRepo: Repository):
        self._studentRepo = studentRepo

    def add_student(self, student: Student):
        """
        Adds a new student

        :param student: the student to be added
        :return None: success
        :raises NotUnique: id is not unique
        :raises NotAnInt: id is not an int or the group is not an int
        :raises NotAString: name is not a string
        """
        ValidationServices.validate_student(student)
        ValidationServices.is_unique(self.get_students(), student)
        self._studentRepo.add_object(student)

    def remove_student(self, studentID):
        """
        Removes a student by it's id

        :param studentID: the id of the student
        :return None: success
        :raises NotAnInt: the id is not an int
        :raises NotExistent: the student does not exist
        """
        ValidationServices.validate_id(studentID)
        self._studentRepo.remove_object(studentID)

    def update_student(self, studentID, newStudent):
        """
        Updates the id, name and/or group of a student

        :param studentID: the id of the student
        :return None: success
        :raises NotAnInt: id, new_id or group are not ints
        :raises NotAString: the name is not a string
        :raises NotExistent: student does not exist
        :raises NotUnique: new id is not unique
        :raises NoUpdate: student was not changed
        """
        idx = self._studentRepo.find_object(studentID)
        for student in self._studentRepo:
            if student.id == newStudent.id and student.id != studentID:
                raise NotUnique("ID should be unique!")
        self._studentRepo[idx] = newStudent

    def get_students(self):
        return deepcopy(self._studentRepo.get_objects())

    def get_students_in_group(self, group):
        return [student for student in self._studentRepo if student.group == group]

    def show_students(self):
        return [str(student) for student in self.get_students()]

    def find_student(self, studentID):
        return self._studentRepo.find_object(studentID)

    def get_student_object(self, studentID):
        return deepcopy(self._studentRepo[self.find_student(studentID)])