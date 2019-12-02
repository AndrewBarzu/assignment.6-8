from new_files.better_repo import Repository, GradeRepository
from controllers.undo_controller import *
from new_files.exceptions import *
from new_files.domain import Grade
from copy import deepcopy
import datetime
import operator

class GradeController:
    def __init__(self, assignmentRepo: Repository, studentRepo: Repository, gradeRepo: GradeRepository, undoController: UndoController):
        self._assignmentrepo = assignmentRepo
        self._studentrepo = studentRepo
        self._undoController = undoController
        self._graderepo = gradeRepo

    def init_grades(self): # Pragma: no cover
        """
        Initializes a list of grades

        :return list: the list of grades
        """
        self._graderepo.extend([Grade('1', '1', '10'), Grade('1', '9',  None), Grade('1', '10', None), Grade('2', '1', None), Grade('3', '1', '7'),
                                Grade('2', '7', '10'), Grade('2', '8', '7'), Grade('2', '6', '9'), Grade('7', '1', None), Grade('7', '7', '4'), Grade('8', '7', '3')])

    def assign(self, assignmentID, studentID, grade=None):
        """
        Function that assigns an assignment to a student

        :param grade: the grade (initialized as None if no param is given)
        :param assignmentID: the id of the assignment
        :param studentID: the id of the student
        :return: None if successful
        :raise NotUnique: if assignment is already given to that student
        :raise NotExistent: if student or assignment do not exist
        """
        ok = 0
        for ass in self._assignmentrepo:
            if ass.id == assignmentID:
                ok = 1
                break
        if ok == 0:
            raise NotExistent("Assignment does not exist!")
        ok = 0
        for student in self._studentrepo:
            if student.id == studentID:
                ok = 1
                break
        if ok == 0:
            raise NotExistent("Student does not exist!")
        grade = Grade(assignmentID, studentID, grade)
        self._graderepo.add(grade)
        redo = FunctionCall(self.assign, assignmentID, studentID)
        undo = FunctionCall(self.remove_grade, studentID, assignmentID)
        operation = Operation(undo, redo)
        self._undoController.recordOp(operation)

    def remove_grade(self, studentID, assignmentID):
        self._graderepo.delete(studentID, assignmentID)

    def remove_student_grade(self, studentID):
        operations = []
        grades = deepcopy(self._graderepo.get_student_grades(studentID, None))
        for grade in grades:
            self._graderepo.delete(grade.studentID, grade.assignmentID)
            redo = FunctionCall(self.remove_grade, grade.studentID, grade.assignmentID)
            undo = FunctionCall(self.assign, grade.assignmentID, grade.studentID, grade.grade)
            operation = Operation(undo, redo)
            operations.append(operation)
        return operations

    def remove_assignment_grade(self, assignmentID):
        operations = []
        grades = deepcopy(self._graderepo)
        for grade in grades:
            if grade.assignmentID == assignmentID:
                self._graderepo.delete(grade.studentID, grade.assignmentID)
                redo = FunctionCall(self.remove_grade, grade.assignmentID, grade.studentID)
                undo = FunctionCall(self.assign, grade.assignmentID, grade.studentID, grade.grade)
                operation = Operation(undo, redo)
                operations.append(operation)
        return operations

    def update_student_id(self, old_sid, new_sid):
        for grade in self._graderepo:
            if grade.studentID == old_sid:
                grade.studentID = new_sid
        redo = FunctionCall(self.update_student_id, old_sid, new_sid)
        undo = FunctionCall(self.update_student_id, new_sid, old_sid)
        operation = Operation(undo, redo)
        return operation

    def update_assignment_id(self, old_aid, new_aid):
        for grade in self._graderepo:
            if grade.assignmentID == old_aid:
                grade.assignmentID = new_aid
        redo = FunctionCall(self.update_assignment_id, old_aid, new_aid)
        undo = FunctionCall(self.update_assignment_id, new_aid, old_aid)
        operation = Operation(undo, redo)
        return operation

    def assign_group(self, assignmentID, group):
        """
        Gives an assignment to a group of students

        :param assignmentID: the assignment
        :param group: the group
        :return: None if successful

        :raise NotAnInt: if assignmentID or group are not ints
        :raise NotExistent: if the assignment is not existent
        """

        if not group.isnumeric():
            raise NotAnInt("Group should be an int!")
        if not assignmentID.isnumeric():
            raise NotAnInt("Assignment ID should be an int!")
        exists = False
        assignment = self._assignmentrepo.find_object(assignmentID)
        if assignment is None:
            raise NotExistent("Assignment does not exist!")
        appended = False
        cascading = []
        for student in self._studentrepo:
            if student.group == group:
                assigned = False
                for grade in self._graderepo:
                    if grade.assignmentID == assignmentID and student.id == grade.studentID:
                        assigned = True
                        break
                if not assigned:
                    studentID = student.id
                    grade = Grade(assignmentID, studentID, None)
                    self._graderepo.add(grade)
                    redo = FunctionCall(self.assign_group, assignmentID, group)
                    undo = FunctionCall(self.remove_grade, studentID, assignmentID)
                    operation = Operation(undo, redo)
                    cascading.append(operation)
                    appended = True
        if appended is False:
            raise NotExistent("No assignment given! Probably group does not exist!")
        cascading = CascadingOperation(cascading)
        self._undoController.recordOp(cascading)

    def get_student_assignments(self, studentID, graded=None):
        """
        Function that gets assignments of a student
        :param studentID: the student
        :param graded: the state of the assignment: graded = 0 => not graded
                                                    graded = 1 => graded
                                                    graded = None => all
        :return: a list of assignments for the given student
        """

        return self._graderepo.get_student_grades(studentID, graded)

    def grade(self, assignmentID, studentID, grade):
        """
        Gives a grade for an assignment of a student

        :param assignmentID: the assignment id
        :param studentID: the student id
        :param grade: the grade
        :return: None if successful
        :raises SetError: if the grade has already been set for that assignment
        :raises NotAnInt: if one of the id's or the grade is not an int
        """
        ok = 0
        for student in self._studentrepo:
            if studentID == student.id:
                ok = 1
        if ok == 0:
            raise NotExistent("Student does not exist!")
        self._graderepo.grade(studentID, assignmentID, grade)
        redo = FunctionCall(self.grade, assignmentID, studentID, grade)
        undo = FunctionCall(self.grade, assignmentID, studentID, None)
        operation = Operation(undo, redo)
        self._undoController.recordOp(operation)

    @staticmethod
    def sort_grades(grades: list):  # Pragma: no cover
        return sorted(grades, key=operator.attrgetter('grade'), reverse=True)

    def statistic_grades(self, assignmentID):
        grades = [grade for grade in self._graderepo if grade.grade is not None]
        if len(grades) == 0:
            raise NotExistent("No grades found!")
        grades = self.sort_grades(grades)
        students = []
        idx = self._assignmentrepo.find_object(assignmentID)
        if idx is None:
            raise NotExistent("Assignment does not exist!")
        assignment = self._assignmentrepo[idx]
        for grade in grades:
            if grade.assignmentID == assignment.id and grade.grade is not None:
                class TransferObj:
                    def __init__(self, *args):
                        self.student = args[0]
                        self.grade = args[1]

                    def __str__(self):
                        return 'Student: ' + self.student + ', Grade: ' + str(self.grade)

                transfer = TransferObj(str(self._studentrepo[self._studentrepo.find_object(grade.studentID)]), grade.grade)
                students.append(transfer)
        if len(students) == 0:
            raise NotExistent("No students are graded for this assignment!")
        return students

    def statistic_assignments(self, assignmentID):
        idx = self._assignmentrepo.find_object(assignmentID)
        students = []
        today = datetime.datetime.now().date()
        if idx is None:
            raise NotExistent("Assignment does not exist!")
        assignment = self._assignmentrepo[idx]
        for grade in self._graderepo:
            if grade.grade is None and assignment.id == grade.assignmentID and assignment.deadline < today:
                students.append(str(self._studentrepo[self._studentrepo.find_object(grade.studentID)]))
        if len(students) == 0:
            raise NotExistent("No late students were found!")
        return students

    def statistic_situation(self):
        """
        Gives the situation of all student, sorted by average grade for all assignments

        :return list: The list of students, sorted by average grade
        """
        if len(self._graderepo) == 0:
            raise NotExistent('No students have grades yet!')
        situations = []
        count = []
        for grade in self._graderepo:
            idx = self._studentrepo.find_object(grade.studentID)
            if idx is not None and grade.grade is not None:
                student = self._studentrepo[idx]
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
        return self.sort_grades(situations)

    def show_grades(self):
        return [str(grade) for grade in self._graderepo]
