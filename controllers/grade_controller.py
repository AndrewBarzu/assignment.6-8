from controllers.undo_controller import *
from new_files.domain import Grade
from new_files.my_sort import CombSort
import operator

class GradeController:
    def __init__(self, gradeRepo):
        self._gradeRepo = gradeRepo

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

    def update_student_id(self, old_sid, new_sid):
        for i in range(len(self._gradeRepo)):
            if self._gradeRepo[i].studentID == old_sid:
                self._gradeRepo[i] = Grade(new_sid, self._gradeRepo[i].assignmentID, self._gradeRepo[i].grade)
        redo = FunctionCall(self.update_student_id, old_sid, new_sid)
        undo = FunctionCall(self.update_student_id, new_sid, old_sid)
        operation = Operation(undo, redo)
        return operation

    def update_assignment_id(self, old_aid, new_aid):
        for i in range(len(self._gradeRepo)):
            if self._gradeRepo[i].studentID == old_aid:
                self._gradeRepo[i] = Grade(self._gradeRepo[i].studentID, new_aid, self._gradeRepo[i].grade)
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

    # @staticmethod
    # def sort_grades(grades: list):  # Pragma: no cover
    #     return sorted(grades, key=operator.attrgetter('grade'), reverse=True)

    @staticmethod
    def sort_grades(grades):
        mySortedGrardes = CombSort(grades[:], lambda x, y: x.grade > y.grade)
        return mySortedGrardes


    def show_grades(self):
        return [str(grade) for grade in self._gradeRepo]

    def get_graded_grades(self):
        return [grade for grade in self._gradeRepo if grade.grade is not None]

    def get_grades(self):
        return [grade for grade in self._gradeRepo]
