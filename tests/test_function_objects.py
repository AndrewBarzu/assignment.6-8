import unittest
from old_files import function_objects
from new_files import domain


class TestFunctionObjects(unittest.TestCase):

    def test_assign(self):
        grades = []
        grade = domain.Grade('1', '1', '10')
        grade2 = domain.Grade('1', '1', '10')
        assign = function_objects.AssignObject(grades, grade)
        assign.execute()
        self.assertEqual(grades[0], grade2)
        assign.undo()
        self.assertEqual(len(grades), 0)
