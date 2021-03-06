"""
- Student: <studentID>, <name>, <group>.
- Assignment: <assignmentID>, <description>, <deadline>.
- Grade: <assignmentID>, <studentID>, <grade>.
"""
from new_files.exceptions import *
import datetime

class Student:
    def __init__(self, studentID, name, group):
        self._studentID = studentID
        self._name = name
        self._group = group

    @property
    def id(self):
        return str(self._studentID)

    @property
    def name(self):
        return self._name

    @property
    def group(self):
        return str(self._group)

    @id.setter
    def id(self, new_id):
        if new_id.isnumeric():
            self._studentID = int(new_id)
        else:
            raise NotAnInt("ID should be int!")

    @name.setter
    def name(self, new_name):
        self._name = new_name

    @group.setter
    def group(self, new_group):
        if new_group.isnumeric():
            self._group = new_group
        else:
            raise NotAnInt("Group should be int!")

    def __str__(self):
        return 'ID: ' + str(self.id) + ' | Name: ' + self.name + ' | Group: ' + str(self.group)

    def __eq__(self, other):
        return self.id == other.id and self.name == other.name and self.group == other.group

class Assignment:
    def __init__(self, assignmentID, description, year, month, day):
        self._assignmentID = assignmentID
        self._description = description
        if day.isnumeric() and month.isnumeric() and year.isnumeric():
            self._deadline = datetime.datetime(int(year), int(month), int(day))
        else:
            raise NotAnInt("Day month and year should be numbers!")

    @property
    def id(self):
        return str(self._assignmentID)

    @property
    def description(self):
        return str(self._description)

    @property
    def deadline(self):
        return self._deadline.date()

    @id.setter
    def id(self, new_id):
        if new_id.isnumeric():
            self._assignmentID = new_id
        else:
            raise NotAnInt("ID should be int!")

    @description.setter
    def description(self, new_description):
        self._description = new_description

    @deadline.setter
    def deadline(self, new_deadline):
        self._deadline = new_deadline

    def __eq__(self, other):
        return self.id == other.id and self.description == other.description and self.deadline == other.deadline

    def __str__(self):
        return 'ID: ' + self.id + ' | Description: ' + self.description + ' | Deadline: ' + str(self.deadline)

class Grade:
    def __init__(self, studentID, assignmentID, grade):
        if assignmentID.isnumeric():
            self._assignmentid = assignmentID
        else:
            raise NotAnInt("Assignment ID should be an int!")
        if studentID.isnumeric():
            self._studentid = studentID
        else:
            raise NotAnInt("Student ID should be an int!")
        if grade is None or grade == 'None':
            self._grade = None
        elif type(grade) == int or grade.isnumeric():
            grade = int(grade)
            if grade in range(11):
                self._grade = grade
            else:
                raise ValueError("Grade should be from 0 to 10!")
        else:
            raise NotAnInt("Grade should be an int!")

    @property
    def assignmentID(self):
        return str(self._assignmentid)

    @property
    def studentID(self):
        return str(self._studentid)

    @property
    def grade(self):
        return self._grade

    @assignmentID.setter
    def assignmentID(self, newid):
        self._assignmentid = newid

    @studentID.setter
    def studentID(self, newid):
        self._studentid = newid

    @grade.setter
    def grade(self, new_grade):
        if new_grade is None:
            self._grade = None
            return
        if new_grade.isnumeric() is False:
            raise NotAnInt("Grade should be an int!")
        new_grade = int(new_grade)
        if new_grade not in range(11):
            raise ValueError("Grade should be between 0 and 10!")
        if self._grade is None:
            self._grade = new_grade
        else:
            raise SetError("Grade cannot be changed!")

    def __eq__(self, other):
        return self.assignmentID == other.assignmentID and self.studentID == other.studentID

    def __str__(self):
        return "Student: " + str(self.studentID) + " | Assignment: " + str(self.assignmentID) + " | Grade: " + str(self.grade)

