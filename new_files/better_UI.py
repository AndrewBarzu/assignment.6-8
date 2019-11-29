from new_files.better_repo import Repository, GradeRepository
from controllers.grade_controller import GradeController
from controllers.assignment_controller import AssignmentController
from controllers.undo_controller import UndoController
from controllers.student_controller import StudentController
from controllers.main_controller import MainController
from new_files.exceptions import *
import os

class UI:   # pragma: no cover
    def __init__(self, mainController: MainController):
        self._controller = mainController

    @staticmethod
    def print_list(given_list):
        for element in given_list:
            print(element)

    @staticmethod
    def print_student_menu():
        print("1. Add student")
        print("2. Remove student")
        print("3. Update student")
        print("4. Show students")
        print("0. Back")


    @staticmethod
    def print_assignment_menu():
        print("1. Add assignment")
        print("2. Remove assignment")
        print("3. Update assignment")
        print("4. Show assignments")
        print("0. Back")


    @staticmethod
    def print_menu():
        print("1. Student services")
        print("2. Assignment services")
        print("3. Grading services")
        print("4. Statistics WIP")
        print("5. Assign student")
        print("6. Assign group")
        print("7. Undo")
        print("8. Redo")
        print("9. Show assigned students")
        print("0. Exit")


    @staticmethod
    def print_statistics_menu():
        print("1. Grade statistics for an assignment")
        print("2. Deadline statistics for an assignment")
        print("3. Situation of all students")
        print("0. Back")


    def exit(self):
        exit()


    def stud_menu(self):
        commands = {'1': self.add_student, '2': self.remove_student, '3': self.update_student, '4': self.show_students}
        while True:
            self.print_student_menu()
            cmd = input(" > ")
            if cmd == '0':
                break
            elif cmd in commands.keys():
                commands[cmd]()
            else:
                print("Bad Command!")


    def assig_menu(self):
        commands = {'1': self.add_assignment, '2': self.remove_assignment, '3': self.update_assignment,
                    '4': self.show_assignments}
        while True:
            self.print_assignment_menu()
            cmd = input(" > ")
            if cmd == '0':
                break
            elif cmd in commands.keys():
                commands[cmd]()
            else:
                print("Bad Command!")


    def grade_menu(self):
        self.print_list(self._controller.get_students())
        studentID = input("Student ID > ")
        os.system('cls')
        self.print_list(self._controller.get_student_assignments(studentID, 0))
        assignmentID = input("Assignment ID > ")
        os.system('cls')
        grade = input("Grade > ")
        try:
            self._controller.grade(assignmentID, studentID, grade)
        except (SetError, NotAnInt, NotExistent) as e:
            print(e)


    def assign_student(self):
        self.print_list(self._controller.get_students())
        student = input("Student ID > ")
        os.system('cls')
        self.print_list(self._controller.get_assignments())
        assignment = input("Assignment ID > ")
        os.system('cls')
        try:
            self._controller.assign(assignment, student)
        except (NotUnique, NotExistent) as e:
            print(e)


    def assign_group(self):
        group = input("Group > ")
        self.print_list(self._controller.get_assignments())
        assignment = input("Assignment ID > ")
        try:
            self._controller.assign_group(assignment, group)
        except (NotAnInt, NotExistent) as e:
            print(e)


    def add_student(self):
        os.system('cls')
        id = input('ID > ')
        name = input('Name > ')
        group = input('Group > ')
        try:
            self._controller.add_student(id, name, group)
        except (NotUnique, NotAnInt, NotAString) as e:
            print(e)


    def remove_student(self):
        os.system('cls')
        id = input('ID > ')
        try:
            self._controller.remove_student(id)
        except (NotAnInt, NotExistent) as e:
            print(e)


    def update_student(self):
        os.system('cls')
        id = input('Old ID > ')
        print('------------------------------------------------------------')
        print('If you don\'t want to replace a field, leave it empty!')
        print('------------------------------------------------------------')
        new_id = input('New ID > ')
        new_name = input('New name > ')
        new_group = input('New group > ')
        try:
            self._controller.update_student(id, new_id, new_name, new_group)
        except (NotAnInt, NotAString, NotExistent, NotUnique, NoUpdate) as e:
            print(e)


    def show_students(self):
        students = self._controller.show_students()
        for student in students:
            print(student)


    def add_assignment(self):
        os.system('cls')
        id = input('ID > ')
        description = input('Description > ')
        print("===Deadline===")
        day = input('Day > ')
        month = input('Month > ')
        year = input('Year > ')
        try:
            self._controller.add_assignment(id, description, day, month, year)
        except Exception as e:
            print(e)


    def remove_assignment(self):
        os.system('cls')
        id = input('ID > ')
        try:
            self._controller.remove_assignment(id)
        except Exception as e:
            print(e)


    def update_assignment(self):
        os.system('cls')
        id = input('Old ID > ')
        print('------------------------------------------------------------')
        print('If you don\'t want to replace a field, leave it empty!')
        print('------------------------------------------------------------')
        new_id = input('New ID > ')
        new_name = input('New description > ')
        print('===New Deadline===')
        new_day = input("New day > ")
        new_month = input("New month > ")
        new_year = input("New year > ")
        try:
            self._controller.update_assignment(id, new_id, new_name, new_day, new_month, new_year)
        except Exception as e:
            print(e)


    def show_assignments(self):
        students = self._controller.show_assignments()
        for student in students:
            print(student)

    def grade_statistics(self):
        assignments = self._controller.show_assignments()
        for assignment in assignments:
            print(assignment)
        assignmentID = input("Assignment ID > ")
        try:
            students = self._controller.statistic_grades(assignmentID)
            for student in students:
                print(str(student))
        except NotExistent as e:
            print(e)


    def deadline_statistics(self):
        assignments = self._controller.show_assignments()
        for assignment in assignments:
            print(assignment)
        assignmentID = input("Assignment ID > ")
        try:
            students = self._controller.statistic_assignments(assignmentID)
            for student in students:
                print(student)
        except NotExistent as e:
            print(e)

    def situation_statistics(self):
        try:
            situations = self._controller.statistic_situations()
            for situation in situations:
                print(str(situation))
        except NotExistent as e:
            print(e)


    def statistics(self):
        commands = {'1': self.grade_statistics, '2': self.deadline_statistics, '3': self.situation_statistics}
        while True:
            self.print_statistics_menu()
            cmd = input("> ")
            os.system('cls')
            if cmd == '0':
                break
            elif cmd in commands.keys():
                commands[cmd]()
            else:
                print("Bad command!")

    def print_grades(self):
        grades = self._controller.show_grades()
        for grade in grades:
            print(grade)


    def start(self):
        commands = {'0': self.exit, '1': self.stud_menu, '2': self.assig_menu, '3': self.grade_menu,
                    '4': self.statistics, '5': self.assign_student, '6': self.assign_group, '7': self._controller.undo,
                    '8': self._controller.redo, '9': self.print_grades}
        while True:
            UI.print_menu()
            cmd = input(' > ')
            os.system('cls')
            if cmd in commands.keys():
                try:
                    commands[cmd]()
                except Exception as e:
                    print(e)
            elif cmd == 'init grades':
                self._controller.init_grades()
            else:
                print("Bad command!")


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
ui = UI(main_controller)
ui.start()
