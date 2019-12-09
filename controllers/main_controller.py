from controllers import grade_controller, assignment_controller, student_controller
from controllers.undo_controller import *
from new_files.domain import Student, Assignment
from new_files.exceptions import *
import new_files.validation_service as ValidationServices
import datetime

class MainController:
    def __init__(self, gradeController: grade_controller.GradeController, studentController: student_controller.StudentController,
                 undoController: UndoController, assignmentController: assignment_controller.AssignmentController):
        self._gradeController = gradeController
        self._studentController = studentController
        self._assignmentController = assignmentController
        self._undoController = undoController

    def add_student(self, studentID, studentName, studentGroup):
        student = Student(studentID, studentName, studentGroup)
        self._studentController.add_student(student)
        redo = FunctionCall(self.add_student, studentID, studentName, studentGroup)
        undo = FunctionCall(self.remove_student, studentID)
        operation = Operation(undo, redo)
        self._undoController.recordOp(operation)

    def remove_student(self, studentID):
        if self._studentController.find_student(studentID) is None:
            raise NotExistent("Student does not exist!")
        oldStudent = self._studentController.get_student_object(studentID)
        self._studentController.remove_student(studentID)
        operations = []
        redo = FunctionCall(self.remove_student, studentID)
        undo = FunctionCall(self.add_student, studentID, oldStudent.name, oldStudent.group)
        operation = Operation(undo, redo)
        operations.append(operation)
        
        studentGrades = self._gradeController.get_student_grades(studentID)
        for grade in studentGrades:
            self._remove_grade(grade.studentID, grade.assignmentID)
            redo = FunctionCall(self._remove_grade, grade.studentID, grade.assignmentID)
            undo = FunctionCall(self._gradeController.assign, grade.studentID, grade.assignmentID, grade.grade)
            operation = Operation(undo, redo)
            operations.append(operation)

        cascade = CascadingOperation(operations)
        self._undoController.recordOp(cascade)

    def update_student(self, studentID, new_id, new_name, new_group):
        ValidationServices.validate_id(studentID)
        ValidationServices.validate_id(new_id)
        newStudent = Student(new_id, new_name, new_group)
        ValidationServices.validate_student(newStudent)
        oldStudent = self._studentController.get_student_object(studentID)
        self._studentController.update_student(studentID, newStudent)
        operations = []
        redo = FunctionCall(self.update_student, studentID, new_id, new_name, new_group)
        undo = FunctionCall(self.update_student, new_id, oldStudent.id, oldStudent.name, oldStudent.group)
        operation = Operation(undo, redo)
        operations.append(operation)
        operation = self._gradeController.update_student_id(studentID, new_id)
        operations.append(operation)
        cascade = CascadingOperation(operations)
        self._undoController.recordOp(cascade)

    def get_students(self):
        return self._studentController.get_students()

    def show_students(self):
        return self._studentController.show_students()

    def add_assignment(self, assignmentID, assignmentDescription, assignmentDay, assignmentMonth, assignmentYear):
        assignment = Assignment(assignmentID, assignmentDescription, assignmentYear, assignmentMonth, assignmentDay)
        self._assignmentController.add_assignment(assignment)
        redo = FunctionCall(self.add_assignment, assignmentID, assignmentDescription, assignmentDay, assignmentMonth, assignmentYear)
        undo = FunctionCall(self.remove_assignment, assignmentID)
        operation = Operation(undo, redo)
        self._undoController.recordOp(operation)

    def remove_assignment(self, assignmentID):
        if self._assignmentController.find_assignment(assignmentID) is None:
            raise NotExistent("Assignment does not exist!")
        old_assignment = self._assignmentController.get_assignment_object(assignmentID)
        self._assignmentController.remove_assignment(assignmentID)
        operations = []
        redo = FunctionCall(self.remove_assignment, assignmentID)
        undo = FunctionCall(self.add_assignment, assignmentID, old_assignment.description, str(old_assignment.deadline.day),
                            str(old_assignment.deadline.month), str(old_assignment.deadline.year))
        operation = Operation(undo, redo)
        operations.append(operation)

        assignmentGrades = self._gradeController.get_assignment_grades(assignmentID)
        for grade in assignmentGrades:
            self._remove_grade(grade.studentID, grade.assignmentID)
            redo = FunctionCall(self._remove_grade, grade.studentID, grade.assignmentID)
            undo = FunctionCall(self._gradeController.assign, grade.studentID, grade.assignmentID, grade.grade)
            operation = Operation(undo, redo)
            operations.append(operation)

        cascade = CascadingOperation(operations)
        self._undoController.recordOp(cascade)

    def update_assignment(self, assignmentID, new_id, new_description, new_day, new_month, new_year):
        ValidationServices.validate_id(assignmentID)
        ValidationServices.validate_id(new_id)
        newAssignment = Assignment(new_id, new_description, new_year, new_month, new_day)
        oldAssignment = self._assignmentController.get_assignment_object(assignmentID)
        self._assignmentController.update_assignment(assignmentID, newAssignment)
        operations = []
        redo = FunctionCall(self.update_assignment, assignmentID, new_id, new_description, new_day, new_month, new_year)
        undo = FunctionCall(self.update_assignment, new_id, oldAssignment.id, oldAssignment.description,
                            str(oldAssignment.deadline.day), str(oldAssignment.deadline.month), str(oldAssignment.deadline.year))
        operation = Operation(undo, redo)
        operations.append(operation)
        operation = self._gradeController.update_assignment_id(assignmentID, new_id)
        operations.append(operation)
        cascade = CascadingOperation(operations)
        self._undoController.recordOp(cascade)

    def show_assignments(self):
        return self._assignmentController.show_assignments()

    def get_assignments(self):
        return self._assignmentController.get_assignments()

    def get_student_assignments(self, studentID, graded):
        return self._gradeController.get_student_assignments(studentID, graded)

    def grade(self, studentID, assignmentID, grade):
        self._gradeController.grade(studentID, assignmentID, grade)
        redo = FunctionCall(self.grade, studentID, assignmentID, grade)
        undo = FunctionCall(self.grade, studentID, assignmentID, None)
        operation = Operation(undo, redo)
        self._undoController.recordOp(operation)

    def assign(self, studentID, assignmentID, grade):
        if self._assignmentController.find_assignment(assignmentID) is None:
            raise NotExistent("Assignment does not exist!")
        if self._studentController.find_student(studentID) is None:
            raise NotExistent("Student does not exist!")
        self._gradeController.assign(studentID, assignmentID)
        redo = FunctionCall(self._gradeController.assign, studentID, assignmentID)
        undo = FunctionCall(self._gradeController.remove_grade, studentID, assignmentID)
        operation = Operation(undo, redo)
        self._undoController.recordOp(operation)

    def assign_group(self, assignmentID, group):
        if not group.isnumeric():
            raise NotAnInt("Group should be an int!")
        if self._assignmentController.find_assignment(assignmentID) is None:
            raise NotExistent("Assignment does not exist!")
        studentsInGroup = self._studentController.get_students_in_group(group)
        if len(studentsInGroup) == 0:
            raise NotExistent("Group does not exist!")
        cascading = []
        for student in studentsInGroup:
            self._gradeController.assign(student.id, assignmentID)
            redo = FunctionCall(self._gradeController.assign, student.id, assignmentID)
            undo = FunctionCall(self._gradeController.remove_grade, student.id, assignmentID)
            operation = Operation(undo, redo)
            cascading.append(operation)

        cascading = CascadingOperation(cascading)
        self._undoController.recordOp(cascading)

    def _remove_grade(self, studentID, assignmentID):
        self._gradeController.remove_grade(studentID, assignmentID)

    def show_grades(self):
        return self._gradeController.show_grades()

    def statistic_grades(self, assignmentID):
        grades = self._gradeController.get_graded_grades()
        if len(grades) == 0:
            raise NotExistent("No grades found!")
        grades = self._gradeController.sort_grades(grades)
        students = []
        if self._assignmentController.find_assignment(assignmentID) is None:
            raise NotExistent("Assignment does not exist!")
        assignment = self._assignmentController.get_assignment_object(assignmentID)
        for grade in grades:
            if grade.assignmentID == assignment.id and grade.grade is not None:
                class TransferObj:
                    def __init__(self, *args):
                        self.student = args[0]
                        self.grade = args[1]

                    def __str__(self):
                        return 'Student: ' + self.student + ', Grade: ' + str(self.grade)

                transfer = TransferObj(Student.__str__(self._studentController.get_student_object(grade.studentID)), str(grade.grade))
                students.append(transfer)
        if len(students) == 0:
            raise NotExistent("No students are graded for this assignment!")
        return students

    def statistic_assignments(self, assignmentID):
        students = []
        today = datetime.datetime.now().date()
        if self._assignmentController.find_assignment(assignmentID) is None:
            raise NotExistent("Assignment does not exist!")
        assignment = self._assignmentController.get_assignment_object(assignmentID)
        grades = self._gradeController.get_grades()
        for grade in grades:
            if grade.grade is None and assignment.id == grade.assignmentID and assignment.deadline < today:
                students.append(Student.__str__(self._studentController.get_student_object(grade.studentID)))
        if len(students) == 0:
            raise NotExistent("No late students were found!")
        return students

    def statistic_situations(self):
        """
        Gives the situation of all student, sorted by average grade for all assignments

        :return list: The list of students.txt, sorted by average grade
        """

        grades = self._gradeController.get_grades()
        if len(grades) == 0:
            raise NotExistent('No students have grades yet!')
        situations = []
        count = []
        for grade in grades:
            if self._studentController.find_student(grade.studentID) is not None and grade.grade is not None:
                student = self._studentController.get_student_object(grade.studentID)
                not_added = True
                for i in range(len(situations)):
                    if situations[i].student == student:
                        situations[i].grade += grade.grade
                        count[i] += 1
                        not_added = False
                        break
                if not_added:
                    class TransferObj:
                        def __init__(self, *args):
                            self.grade = args[1]
                            self.student = args[0]

                        def __str__(self):
                            return 'Student ' + str(self.student) + ' Grade: ' + str(self.grade)

                    transfer = TransferObj(student, grade.grade)
                    situations.append(transfer)
                    count.append(1)
        for i in range(len(situations)):
            situations[i].grade /= count[i]
            situations[i].grade = round(situations[i].grade, 2)
        return self._gradeController.sort_grades(situations)

    def undo(self):
        self._undoController.undo()

    def redo(self):
        self._undoController.redo()

    def init_grades(self):
        self._gradeController._gradeRepo.init_grades()
