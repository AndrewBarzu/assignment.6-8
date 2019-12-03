import unittest
from new_files import exceptions, domain


class TestDomain(unittest.TestCase):

    def test_student(self):
        student = domain.Student('1', 'Didid', '5')
        self.assertEqual(student.id, '1')
        self.assertEqual(student.name, 'Didid')
        self.assertEqual(student.group, '5')
        student.group = '2'
        self.assertEqual(student.group, '2')
        student.id = '10'
        with self.assertRaises(exceptions.NotAnInt):
            student.id = 'a'

    def test_assignment(self):
        assignment = domain.Assignment('1', 'assignment', '2020', '10', '19')
        self.assertEqual(assignment.id, '1')
        self.assertEqual(assignment.description, 'assignment')
        self.assertEqual(str(assignment.deadline), '2020-10-19')
        assignment2 = domain.Assignment('1', 'assignment', '2020', '10', '19')
        with self.assertRaises(exceptions.NotAnInt):
            assignment.id = 'a'
        assert assignment2 == assignment
        assignment.description = 'arsifilud'
        self.assertEqual(assignment.description, 'arsifilud')
        #with self.assertRaises(exceptions.NotAString):
        assignment.description = 'aerse1'
        self.assertEqual(assignment.description, 'aerse1')

    def test_grade(self):
        grade = domain.Grade('1', '1', None)
        self.assertEqual(str(grade), 'Student: 1 | Assignment: 1 | Grade: None')
        grade = domain.Grade('1', '2', '8')
        self.assertEqual(str(grade), 'Student: 1 | Assignment: 2 | Grade: 8')
        with self.assertRaises(ValueError):
            grade = domain.Grade('1', '2', '11')
        with self.assertRaises(exceptions.NotAnInt):
            grade = domain.Grade('a', 'b', 'c')
        with self.assertRaises(exceptions.NotAnInt):
            grade = domain.Grade('1', 'b', 'c')
        with self.assertRaises(exceptions.NotAnInt):
            grade = domain.Grade('1', '1', 'c')
        grade = domain.Grade('1', '1', None)
        grade.grade = '10'
        self.assertEqual(str(grade), 'Student: 1 | Assignment: 1 | Grade: 10')
        with self.assertRaises(exceptions.SetError):
            grade.grade = '6'
        grade.grade = None
        with self.assertRaises(ValueError):
            grade.grade = '11'