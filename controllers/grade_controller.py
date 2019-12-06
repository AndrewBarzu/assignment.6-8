from new_files.better_repo import GradeRepository
from controllers.undo_controller import *
from new_files.domain import Grade
import new_files.exceptions as exceptions
import operator

class GradeController:
    def __init__(self, gradeRepo: GradeRepository):
        self._gradeRepo = gradeRepo

    def init_grades(self): # Pragma: no cover
        """
        Initializes a list of grades

        :return list: the list of grades
        """
        self._gradeRepo.extend([Grade('1', '1', '10'), Grade('1', '9', None), Grade('1', '10', None), Grade('2', '1', None), Grade('3', '1', '7'),
                                Grade('2', '7', '10'), Grade('2', '8', '7'), Grade('2', '6', '9'), Grade('7', '1', None), Grade('7', '7', '4'), Grade('8', '7', '3')])

    def assign(self, studentID, assignmentID, grade="None"):
        """
        Function that assigns an assignment to a student

        :param grade: the grade (initialized as None if no param is given)
        :param assignmentID: the id of the assignment
        :param studentID: the id of the student
        :return: None if successful
        :raise NotUnique: if assignment is already given to that student
        :raise NotExistent: if student or assignment do not exist
        """
        grade = Grade(studentID, assignmentID, grade)
        for myGrade in self._gradeRepo:
            if myGrade.studentID == grade.studentID and myGrade.assignmentID == grade.assignmentID:
                return
        self._gradeRepo.add(grade)

    def remove_grade(self, studentID, assignmentID):
        self._gradeRepo.delete(studentID, assignmentID)

    def get_student_grades(self, studentID):
        return [grade for grade in self._gradeRepo if grade.studentID == studentID]

    def get_assignment_grades(self, assignmentID):
        return [grade for grade in self._gradeRepo if grade.assignmentID == assignmentID]

    def remove_assignment_grade(self, assignmentID):
        operations = []
        grades = self._gradeRepo
        for grade in grades:
            if grade.assignmentID == assignmentID:
                self._gradeRepo.delete(grade.studentID, grade.assignmentID)
                redo = FunctionCall(self.remove_grade, grade.assignmentID, grade.studentID)
                undo = FunctionCall(self.assign, grade.studentID, grade.assignmentID, grade.grade)
                operation = Operation(undo, redo)
                operations.append(operation)
        return operations

    def update_student_id(self, old_sid, new_sid):
        for grade in self._gradeRepo:
            if grade.studentID == old_sid:
                grade.studentID = new_sid
                print(new_sid)
                print(grade)
        redo = FunctionCall(self.update_student_id, old_sid, new_sid)
        undo = FunctionCall(self.update_student_id, new_sid, old_sid)
        operation = Operation(undo, redo)
        return operation

    def update_assignment_id(self, old_aid, new_aid):
        for grade in self._gradeRepo:
            if grade.assignmentID == old_aid:
                grade.assignmentID = new_aid
        redo = FunctionCall(self.update_assignment_id, old_aid, new_aid)
        undo = FunctionCall(self.update_assignment_id, new_aid, old_aid)
        operation = Operation(undo, redo)
        return operation

    def get_student_assignments(self, studentID, graded=None):
        """
        Function that gets assignments of a student
        :param studentID: the student
        :param graded: the state of the assignment: graded = 0 => not graded
                                                    graded = 1 => graded
                                                    graded = None => all
        :return: a list of assignments for the given student
        """

        return self._gradeRepo.get_student_grades(studentID, graded)

    def grade(self, studentID, assignmentID, grade):
        """
        Gives a grade for an assignment of a student

        :param assignmentID: the assignment id
        :param studentID: the student id
        :param grade: the grade
        :return: None if successful
        :raises SetError: if the grade has already been set for that assignment
        :raises NotAnInt: if one of the id's or the grade is not an int
        """
        self._gradeRepo.grade(studentID, assignmentID, grade)

    @staticmethod
    def sort_grades(grades: list):  # Pragma: no cover
        return sorted(grades, key=operator.attrgetter('grade'), reverse=True)


    def show_grades(self):
        return [str(grade) for grade in self._gradeRepo]

    def get_graded_grades(self):
        return [grade for grade in self._gradeRepo if grade.grade is not None]

    def get_grades(self):
        return [grade for grade in self._gradeRepo]
