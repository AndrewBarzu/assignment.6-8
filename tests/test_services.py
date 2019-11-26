import unittest
from old_files import services
from new_files import exceptions


class TestServices(unittest.TestCase):

    def test_assign(self):
        service = services.Services(services.Repository(services.Repository.initialize_students()),
                                    services.Repository(services.Repository.initialize_assignments()))
        service.assign('1', '1')
        with self.assertRaises(exceptions.NotUnique):
            service.assign('1', '1')
        with self.assertRaises(exceptions.NotExistent):
            service.assign('1', 'b')
        with self.assertRaises(exceptions.NotExistent):
            service.assign('20', '17')

    def test_assign_group(self):
        service = services.Services(services.Repository(services.Repository.initialize_students()),
                                    services.Repository(services.Repository.initialize_assignments()))
        service.assign_group('1', '3')
        self.assertEqual(service.show_grades(), ["Student: 1, Assignment: 1, Grade: None",
                                                 "Student: 9, Assignment: 1, Grade: None",
                                                 "Student: 10, Assignment: 1, Grade: None"])
        with self.assertRaises(exceptions.NotExistent):
            service.assign_group('20', '3')
        with self.assertRaises(exceptions.NotAnInt):
            service.assign_group('a', '20')
        with self.assertRaises(exceptions.NotAnInt):
            service.assign_group('20', 'a')
        with self.assertRaises(exceptions.NotExistent):
            service.assign_group('1', '3')

    def test_grade(self):
        service = services.Services(services.Repository(services.Repository.initialize_students()),
                                    services.Repository(services.Repository.initialize_assignments()))
        service.assign('1', '1')
        service.grade('1', '1', '10')
        self.assertEqual(service.show_grades(), ["Student: 1, Assignment: 1, Grade: 10"])
        with self.assertRaises(exceptions.NotExistent):
            service.grade('1', 'a', '10')
        with self.assertRaises(exceptions.NotExistent):
            service.grade('a', '1', '10')
        service.assign('1', '2')
        with self.assertRaises(exceptions.NotAnInt):
            service.grade('1', '2', 'a')

    def test_add_student(self):
        service = services.Services(services.Repository(services.Repository.initialize_students()),
                                    services.Repository(services.Repository.initialize_assignments()))
        result = service.add_student('11', 'Borcea', '4')
        self.assertEqual(result, None)
        with self.assertRaises(exceptions.NotUnique):
            service.add_student('11', 'gulugulugulu', '4')
        with self.assertRaises(exceptions.NotAString):
            service.add_student('12', "borcea2", 'a')
        with self.assertRaises(exceptions.NotAnInt):
            service.add_student('a', 'balabala', '7')
        with self.assertRaises(exceptions.NotAString):
            service.add_student('13', '7', '7')

    def test_remove_student(self):
        service = services.Services(services.Repository(services.Repository.initialize_students()),
                                    services.Repository(services.Repository.initialize_assignments()))
        service.init_grades()
        service.remove_student('1')
        self.assertEqual(service.find_student('1'), None)


    def test_update_student(self):
        service = services.Services(services.Repository(services.Repository.initialize_students()),
                                    services.Repository(services.Repository.initialize_assignments()))
        self.assertIsNone(service.update_student('1', '20', 'Paricelu', '2'))
        with self.assertRaises(exceptions.NotAnInt):
            service.update_student('ab', 'cd', 'aliasul', '11')
        with self.assertRaises(exceptions.NotAnInt):
            service.update_student('5', 'cd', 'aliasul', '11')
        with self.assertRaises(exceptions.NotAString):
            service.update_student('9', '22', '1234', '11')
        with self.assertRaises(exceptions.NotExistent):
            service.update_student('21', '24', 'amin', '6')
        with self.assertRaises(exceptions.NotUnique):
            service.update_student('8', '2', 'Kolind', '3')
        with self.assertRaises(exceptions.NoUpdate):
            service.update_student('7', '', '', '')

    def test_add_assignment(self):
        service = services.Services(services.Repository(services.Repository.initialize_students()),
                                    services.Repository(services.Repository.initialize_assignments()))
        result = service.add_assignment('11', 'Borcea', '4', '5', '2019')
        self.assertEqual(result, None)
        with self.assertRaises(exceptions.NotUnique):
            service.add_assignment('11', 'gulugulugulu', '4', '5', '2019')
        with self.assertRaises(exceptions.NotAString):
            service.add_assignment('12', "borcea2", '4', '5', '2019')
        with self.assertRaises(exceptions.NotAnInt):
            service.add_assignment('a', 'balabala', '7', '5', '2019')
        with self.assertRaises(exceptions.NotAString):
            service.add_assignment('13', '7', '7', '7', '2019')
        with self.assertRaises(ValueError):
            service.add_assignment('13', 'balala', '7', '22', '2019')
        with self.assertRaises(exceptions.NotAnInt):
            service.add_assignment('13', 'balala', '7', '1', '201a')
        with self.assertRaises(ValueError):
            service.add_assignment('13', 'balala', '32', '12', '2019')

    def test_remove_assignment(self):
        service = services.Services(services.Repository(services.Repository.initialize_students()),
                                    services.Repository(services.Repository.initialize_assignments()))
        self.assertIsNone(service.remove_assignment('1'))
        with self.assertRaises(exceptions.NotExistent):
            service.remove_assignment('50')
        with self.assertRaises(exceptions.NotAnInt):
            service.remove_assignment('a')

    def test_update_assignment(self):
        service = services.Services(services.Repository(services.Repository.initialize_students()),
                                    services.Repository(services.Repository.initialize_assignments()))
        self.assertIsNone(service.update_assignment('1', '20', 'Paricelu', '2', '10', '2019'))
        with self.assertRaises(exceptions.NotAnInt):
            service.update_assignment('ab', 'cd', 'aliasul', '11', '11', '1111')
        with self.assertRaises(exceptions.NotAnInt):
            service.update_assignment('5', 'cd', 'aliasul', '11', '12', '1234')
        with self.assertRaises(exceptions.NotAString):
            service.update_assignment('9', '22', '1234', '11', '10', '987')
        with self.assertRaises(exceptions.NotExistent):
            service.update_assignment('21', '24', 'amin', '6', '7', '2018')
        with self.assertRaises(exceptions.NotUnique):
            service.update_assignment('8', '2', 'Kolind', '3', '4', '5555')
        with self.assertRaises(exceptions.NoUpdate):
            service.update_assignment('7', '', '', '', '', '')

    def test_get_show(self):
        service = services.Services(services.Repository(services.Repository.initialize_students()),
                                    services.Repository(services.Repository.initialize_assignments()))
        students = service.get_students()
        studentss = service.show_students()
        self.assertEqual(str(students[1]), studentss[1])
        assignments = service.get_assignments()
        assignments = service.show_assignments()
        grades = service.show_grades()
