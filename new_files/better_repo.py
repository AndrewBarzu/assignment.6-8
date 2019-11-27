from new_files.domain import *

class Repository:
    def __init__(self, student_list=None):
        if student_list is None:
            student_list = []
        self._objects = student_list

    def initialize_assignments(self):  # pragma: no cover
        self._objects = [Assignment('1', 'Paricel', '1999', '10', '15'), Assignment('2', 'Marcel', '2010', '12', '19'),
                         Assignment('3', 'Georgel', '2019', '11', '29'), Assignment('4', 'George', '2020', '1', '10'),
                         Assignment('5', 'Gigel', '2019', '12', '18'), Assignment('6', 'Gicu', '2019', '12', '7'),
                         Assignment('7', 'Mercedesa', '2021', '9', '20'), Assignment('8', 'Maria', '2020', '8', '27'),
                         Assignment('9', 'Marian', '2015', '1', '24'), Assignment('10', 'Dani', '1999', '10', '24')]

    def initialize_students(self):    # pragma: no cover
        self._objects = [Student('1', 'Paricel', '3'), Student('2', 'Marcel', '1'), Student('3', 'Georgel', '2'),
                         Student('4', 'George', '1'), Student('5', 'Gigel', '4'), Student('6', 'Gicu', '7'),
                         Student('7', 'Mercedesa', '2'), Student('8', 'Maria', '7'), Student('9', 'Marian', '3'),
                         Student('10', 'Marcela', '3')]

    def add_object(self, object):
        """
        Adds a new object

        :param object: the object to be added
        :return: None if successful
        :raises Exception: from domain, handled by UI
        """
        self._objects.append(object)

    def remove_object(self, id):
        """
        Removes an object

        :param id: the id of the student
        :return None: successful
        :raises Exception: from the domain
        """
        for object in self._objects:
            if object.id == id:
                self._objects.remove(object)
                return
        raise NotExistent("Not existent!")

    def update_object(self, idx, object):
        self._objects[idx] = object

    def get_objects(self):     # pragma: no cover
        return self._objects

    def find_object(self, objectID):
        """
        Finds if an object exists

        :param objectID: the id of the object

        :return index: the index at which the student exists in the list
        :return None: Not Found
        """
        idx = 0
        for object in self._objects:
            if object.id == objectID:
                return idx
            idx += 1
        return None

    def __getitem__(self, item):
        return self._objects[item]

class GradeRepository:
    def __init__(self):
        self._grades = []

    def add(self, grade):
        for selfgrade in self._grades:
            if selfgrade == grade:
                raise NotUnique("The student already has that assignment!")
        self._grades.append(grade)

    def delete(self, studentID, assignmentID):
        for grade in self._grades:
            if grade.studentID == studentID and grade.assignmentID == assignmentID:
                self._grades.remove(grade)
                return
        raise NotExistent("ID's not found!")

    def grade(self, sid, aid, new_grade):
        for grade in self._grades:
            if grade.studentID == sid and grade.assignmentID == aid:
                grade.grade = new_grade
        raise NotExistent("Grade not found!")

    def get_student_grades(self, sid, graded):
        if graded is None:
            return [grade for grade in self._grades if grade.studentID == sid]
        if graded == 0:
            return [grade for grade in self._grades if grade.studentID == sid and grade.grade is None]
        if graded == 1:
            return [grade for grade in self._grades if grade.studentID == sid and grade.grade is not None]

    def __getitem__(self, item):
        return self._grades[item]

    def __len__(self):
        return len(self._grades)

    def extend(self, more):
        self._grades.extend(more)
