from new_files.exceptions import *
from new_files.domain import Student, Grade, Assignment
from new_files.better_repo import Repository
import datetime

# TODO: VALIDATIONS BOIIIII

class StudentValidator:
    """
    Validates a student
    """

    def validate_student(self, student: Student, student_repo: Repository):
        """
        Validates a student
        :param student: the new student
        :param student_repo: the repository of students
        :return None: success
        :raises : not ok bro
        """
        self.validate_ID(student.id)
        self.validate_group(student.group)
        for stud in student_repo:
            if student.id == stud.id:
                raise NotUnique("Student ID should be unique!")

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

    def validate_assignment(self, assignment: Assignment, assignment_repo: Repository):
        """
        Validates a student
        :param assignment: the new assignment
        :param assignment_repo: the repository of assignments
        :return None: success
        :raises : not ok bro
        """
        self.validate_ID(assignment.id)
        for assig in assignment_repo:
            if assignment.id == assig.id:
                raise NotUnique("Student ID should be unique!")

    @staticmethod
    def validate_ID(ID: str):
        if not ID.isnumeric():
            raise NotAnInt("Student ID should be of type int!")

class GradeValidator:
    @staticmethod
    def validateGrade(grade: Grade):
        if grade.grade < 0 or grade.grade > 10 or grade.grade is not None:
            raise ValueError("Grade should be between 0 and 10!")

