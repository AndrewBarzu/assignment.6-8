from controllers import grade_controller, assignment_controller, student_controller, undo_controller

class MainController:
    def __init__(self, gradeController: grade_controller.GradeController, studentController: student_controller.StudentController,
                 undoController: undo_controller.UndoController, assignmentController: assignment_controller.AssignmentController):
        self._gradeController = gradeController
        self._studentController = studentController
        self._assignmentController = assignmentController
        self._undoController = undoController

    def add_student(self, studentID, student_name, student_group):
        self._studentController.add_student(studentID, student_name, student_group)

    def remove_student(self, studentID):
        self._studentController.remove_student(studentID)

    def update_student(self, studentID, new_id, new_name, new_group):
        self._studentController.update_student(studentID, new_id, new_name, new_group)

    def get_students(self):
        return self._studentController.get_students()

    def show_students(self):
        return self._studentController.show_students()

    def add_assignment(self, assignmentID, assignmentDescription, assignmentDay, assignmentMonth, assignmentYear):
        self._assignmentController.add_assignment(assignmentID, assignmentDescription, assignmentDay, assignmentMonth, assignmentYear)

    def remove_assignment(self, assignmentID):
        self._assignmentController.remove_assignment(assignmentID)

    def update_assignment(self, assignmentID, new_id, new_description, new_day, new_month, new_year):
        self._assignmentController.update_assignment(assignmentID, new_id, new_description, new_day, new_month, new_year)

    def show_assignments(self):
        return self._assignmentController.show_assignments()

    def get_assignments(self):
        return self._assignmentController.get_assignments()

    def get_student_assignments(self, studentID, graded):
        return self._gradeController.get_student_assignments(studentID, graded)

    def grade(self, assignmentID, studentID, grade):
        self._gradeController.grade(assignmentID, studentID, grade)

    def assign(self, assignmentID, studentID):
        self._gradeController.assign(assignmentID, studentID)

    def assign_group(self, assignmentID, group):
        self._gradeController.assign_group(assignmentID, group)

    def show_grades(self):
        return self._gradeController.show_grades()

    def Statistics(self):
        def statistic_grades(assignmentID):
            return self._gradeController.statistic_grades(assignmentID)

        def statistic_assignments(assignmentID):
            return self._gradeController.statistic_assignments(assignmentID)

        def statistic_situations():
            return self._gradeController.statistic_situation()

    def undo(self):
        self._undoController.undo()

    def redo(self):
        self._undoController.redo()

    def init_grades(self): # Pragma: no cover
        """
        Initializes a list of grades

        :return list: the list of grades
        """
        self._gradeController.init_grades()
