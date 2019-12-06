from new_files.exceptions import *
import datetime

# TODO: VALIDATIONS BOIIIII

def is_unique(objectList: list, myObject):
    for obj in objectList:
        if myObject.id == obj.id:
            raise NotUnique("ID is not unique!")

def validate_id(id):
    if not id.isnumeric():
        raise NotAnInt("ID should be an int!")

def validate_student(student):
    """
    Validates a student
    :param student: the new student
    :param student_repo: the repository of students.txt
    :return None: success
    :raises : not ok bro
    """
    if not student.id.isnumeric():
        raise NotAnInt("Student ID should be of type int!")
    if not student.group.isnumeric():
        raise NotAnInt("Group should be of type int!")


class GradeValidator:
    @staticmethod
    def validateGrade(grade):
        if grade.grade < 0 or grade.grade > 10 or grade.grade is not None:
            raise ValueError("Grade should be between 0 and 10!")

