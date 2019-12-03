from new_files.exceptions import *
from new_files.domain import Student, Grade, Assignment
import datetime

# TODO: VALIDATIONS BOIIIII

def is_unique(objectList: list, myObject):
    for obj in objectList:
        if myObject.id == obj.id:
            raise NotUnique("ID is not unique!")

class StudentValidator:
    """
    Validates a student
    """

    def validate_student(self, student: Student):
        """
        Validates a student
        :param student: the new student
        :param student_repo: the repository of students.txt
        :return None: success
        :raises : not ok bro
        """
        self.validate_ID(student.id)
        self.validate_group(student.group)

    @staticmethod
    def validate_ID(ID: str):
        if not ID.isnumeric():
            raise NotAnInt("Student ID should be of type int!")

    @staticmethod
    def validate_group(group: str):
        if not group.isnumeric():
            raise NotAnInt("Group should be of type int!")


class AssignmentValidator:
    """
    Validates a student
    """

    def validate_assignment(self, assignment: Assignment):
        """
        Validates a student
        :param assignment: the new assignment
        :param assignment_repo: the repository of assignments
        :return None: success
        :raises : not ok bro
        """
        self.validate_ID(assignment.id)

    @staticmethod
    def validate_ID(ID: str):
        if not ID.isnumeric():
            raise NotAnInt("Assignment ID should be of type int!")

class GradeValidator:
    @staticmethod
    def validateGrade(grade: Grade):
        if grade.grade < 0 or grade.grade > 10 or grade.grade is not None:
            raise ValueError("Grade should be between 0 and 10!")

