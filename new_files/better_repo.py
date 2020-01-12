from new_files.domain import *
import new_files.validation_service
import names
import random
import datetime
from new_files.my_iterable import MyIterable

class Repository:
    def __init__(self, student_list=None):
        if student_list is None:
            student_list = MyIterable()
        self._objects = student_list

    @staticmethod
    def _rand_date(start, end):
        delta = end-start
        int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
        random_second = random.randrange(int_delta)
        return start + datetime.timedelta(seconds=random_second)

    @staticmethod
    def _rand_description():
        result = ''
        result += random.choices(['Do', 'Make', 'Find', 'Create', 'Develop'])[0] + ' '
        result += random.choices(['dishes', 'database', 'online store', 'web application', 'pet shop', 'bakery', 'car rental application'], weights=[2, 11, 11, 11, 11, 11, 11])[0] + ' '
        result += 'for '
        result += names.get_full_name()
        return result

    def initialize_assignments(self):  # pragma: no cover
        self._objects = []
        for i in range(10):
            myDate = self._rand_date(datetime.datetime(2018, 12, 30), datetime.datetime(2021, 12, 30))
            self._objects.append(Assignment(str(i+1), self._rand_description(), str(myDate.year), str(myDate.month), str(myDate.day)))

    def initialize_students(self):    # pragma: no cover
        self._objects = []
        for i in range(10):
            self._objects.append(Student(str(i+1), names.get_full_name(), str(random.randint(1, 10))))

    def add_object(self, object):
        """
        Adds a new object

        :param object: the object to be added
        :return: None if successful
        :raises Exception: from domain, handled by UI
        """
        new_files.validation_service.is_unique(self._objects, object)
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
        if item is None:
            raise NotExistent("Not existent!")
        return self._objects[item]

    def __setitem__(self, key, value):
        self._objects[key] = value


    def __str__(self):
        string = "Repository: \n"
        for object in self._objects:
            string += str(object) + '\n'
        return string

class GradeRepository:
    def __init__(self):
        self._grades = MyIterable()

    def init_grades(self):
        for i in range(10):
            myGrade = Grade(str(random.randint(1, 10)), str(random.randint(1, 10)), str(random.choice([None, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10])))
            while True:
                try:
                    self.add(myGrade)
                    break
                except NotUnique:
                    myGrade = Grade(str(random.randint(1, 10)), str(random.randint(1, 10)), str(random.choice([None, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10])))

    def add(self, grade):
        for myGrade in self._grades:
            if myGrade == grade:
                raise NotUnique("The student already has that assignment!")
        self._grades.append(grade)

    def delete(self, studentID, assignmentID):
        for myGrade in self._grades:
            if myGrade.studentID == studentID and myGrade.assignmentID == assignmentID:
                self._grades.remove(myGrade)
                return

    def grade(self, sid, aid, new_grade):
        for grade in self._grades:
            if grade.studentID == sid and grade.assignmentID == aid:
                grade.grade = new_grade
                return
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

    def __setitem__(self, key, value):
        self._grades[key] = value

    def __len__(self):
        return len(self._grades)

    def __str__(self):
        string = "Repository: \n"
        for grade in self._grades:
            string += str(grade) + '\n'
        return string

    def extend(self, more):
        self._grades.extend(more)
