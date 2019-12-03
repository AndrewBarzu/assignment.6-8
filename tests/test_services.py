import unittest
from new_files import exceptions
from controllers.main_controller import MainController
from controllers.assignment_controller import AssignmentController
from controllers.undo_controller import *
from controllers.student_controller import StudentController
from controllers.grade_controller import GradeController
from new_files.better_repo import *

class TestServices(unittest.TestCase):

    @staticmethod
    def initController():
        studentRepo = Repository()
        studentRepo.initialize_students()
        assignmentRepo = Repository()
        assignmentRepo.initialize_assignments()
        gradeRepo = GradeRepository()
        undoController = UndoController()
        gradeController = GradeController(assignmentRepo, studentRepo, gradeRepo, undoController)
        studentController = StudentController(studentRepo, undoController, gradeController)
        assignmentController = AssignmentController(assignmentRepo, gradeController, undoController)
        main_controller = MainController(gradeController, studentController, undoController, assignmentController)
        return main_controller

    def test_assign(self):
        main_controller = self.initController()
        main_controller.assign('1', '1')
        with self.assertRaises(exceptions.NotUnique):
            main_controller.assign('1', '1')
        with self.assertRaises(exceptions.NotExistent):
            main_controller.assign('1', 'b')
        with self.assertRaises(exceptions.NotExistent):
            main_controller.assign('20', '17')

    def test_assign_group(self):
        main_controller = self.initController()
        main_controller.assign_group('1', '3')
        self.assertEqual(main_controller.show_grades(), ["Student: 1 | Assignment: 1 | Grade: None",
                                                         "Student: 1 | Assignment: 9 | Grade: None",
                                                         "Student: 1 | Assignment: 10 | Grade: None"])
        with self.assertRaises(exceptions.NotExistent):
            main_controller.assign_group('20', '3')
        with self.assertRaises(exceptions.NotAnInt):
            main_controller.assign_group('a', '20')
        with self.assertRaises(exceptions.NotAnInt):
            main_controller.assign_group('20', 'a')
        with self.assertRaises(exceptions.NotUnique):
            main_controller.assign_group('1', '3')

    def test_grade(self):
        main_controller = self.initController()
        main_controller.assign('1', '1')
        main_controller.grade('1', '1', '10')
        self.assertEqual(main_controller.show_grades(), ["Student: 1 | Assignment: 1 | Grade: 10"])
        with self.assertRaises(exceptions.NotExistent):
            main_controller.grade('1', 'a', '10')
        with self.assertRaises(exceptions.NotExistent):
            main_controller.grade('a', '1', '10')
        main_controller.assign('1', '2')
        with self.assertRaises(exceptions.NotAnInt):
            main_controller.grade('1', '2', 'a')

    def test_add_student(self):
        main_controller = self.initController()
        result = main_controller.add_student('11', 'Borcea', '4')
        self.assertEqual(result, None)
        with self.assertRaises(exceptions.NotUnique):
            main_controller.add_student('11', 'gulugulugulu', '4')
        with self.assertRaises(exceptions.NotAnInt):
            main_controller.add_student('a', 'balabala', '7')

    def test_remove_student(self):
        main_controller = self.initController()
        main_controller.init_grades()
        main_controller.remove_student('1')
        with self.assertRaises(exceptions.NotExistent):
            main_controller.remove_student('50')


    def test_update_student(self):
        main_controller = self.initController()
        main_controller.init_grades()
        self.assertIsNone(main_controller.update_student('1', '20', 'Paricelu', '2'))
        with self.assertRaises(exceptions.NotAnInt):
            main_controller.update_student('ab', 'cd', 'aliasul', '11')
        with self.assertRaises(exceptions.NotAnInt):
            main_controller.update_student('5', 'cd', 'aliasul', '11')
        with self.assertRaises(exceptions.NotExistent):
            main_controller.update_student('21', '24', 'amin', '6')
        with self.assertRaises(exceptions.NotUnique):
            main_controller.update_student('8', '2', 'Kolind', '3')
        with self.assertRaises(exceptions.NoUpdate):
            main_controller.update_student('7', '', '', '')

    def test_add_assignment(self):
        main_controller = self.initController()
        result = main_controller.add_assignment('11', 'Borcea', '4', '5', '2019')
        self.assertEqual(result, None)
        with self.assertRaises(exceptions.NotUnique):
            main_controller.add_assignment('11', 'gulugulugulu', '4', '5', '2019')
        with self.assertRaises(exceptions.NotAnInt):
            main_controller.add_assignment('a', 'balabala', '7', '5', '2019')
        with self.assertRaises(ValueError):
            main_controller.add_assignment('13', 'balala', '7', '22', '2019')
        with self.assertRaises(exceptions.NotAnInt):
            main_controller.add_assignment('13', 'balala', '7', '1', '201a')
        with self.assertRaises(ValueError):
            main_controller.add_assignment('13', 'balala', '32', '12', '2019')

    def test_remove_assignment(self):
        main_controller = self.initController()
        main_controller.init_grades()
        main_controller.remove_assignment('1')
        with self.assertRaises(exceptions.NotExistent):
            main_controller.remove_assignment('50')
        with self.assertRaises(exceptions.NotAnInt):
            main_controller.remove_assignment('a')

    def test_update_assignment(self):
        main_controller = self.initController()
        main_controller.init_grades()
        main_controller.update_assignment('1', '20', 'Paricelu', '2', '10', '2019')
        with self.assertRaises(exceptions.NotAnInt):
            main_controller.update_assignment('ab', 'cd', 'aliasul', '11', '11', '1111')
        with self.assertRaises(exceptions.NotAnInt):
            main_controller.update_assignment('5', 'cd', 'aliasul', '11', '12', '1234')
        with self.assertRaises(exceptions.NotExistent):
            main_controller.update_assignment('21', '24', 'amin', '6', '7', '2018')
        with self.assertRaises(exceptions.NotUnique):
            main_controller.update_assignment('8', '2', 'Kolind', '3', '4', '5555')
        with self.assertRaises(exceptions.NoUpdate):
            main_controller.update_assignment('7', '', '', '', '', '')

    def test_get_show(self):
        main_controller = self.initController()
        students = main_controller.get_students()
        studentss = main_controller.show_students()
        self.assertEqual(str(students[1]), studentss[1])
        assignments = main_controller.get_assignments()
        assignmentss = main_controller.show_assignments()
        self.assertEqual(str(assignments[1]), assignmentss[1])
        grades = main_controller.show_grades()

    def test_statistics(self):
        main_controller = self.initController()
        main_controller.init_grades()
        situations = main_controller.statistic_situations()
        grades_statistic = main_controller.statistic_grades('1')
        assignment_statistic = main_controller.statistic_assignments('1')

    def test_undo_redo(self):
        main_controller = self.initController()
        main_controller.init_grades()
        main_controller.remove_student('1')
        main_controller.undo()
        main_controller.redo()

    def test_others(self):
        main_controller = self.initController()
        graded_grades = main_controller.get_student_assignments('1', 1)
        ungraded_grades = main_controller.get_student_assignments('1', 0)
        all_grades = main_controller.get_student_assignments('1', None)
