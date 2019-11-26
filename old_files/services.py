"""
1. Manage the list of students and available assignments. The application must allow the user to add,
remove, update, and list both students and assignments.

2. Give assignments to a student or a group of students. In case an assignment is given to a group of
students, every student in the group will receive it. In case there are students who were previously
given that assignment, it will not be assigned again.

3. Grade student for a given assignment. When grading, the program must allow the user to select the
assignment that is graded, from the student’s list of ungraded assignments. A student’s grade for a
given assignment cannot be changed. Deleting a student removes their assignments. Deleting an
assignment also removes all grades at that assignment.

4. Create statistics:
- All students who received a given assignment, ordered by average grade for that assignment.
- All students who are late in handing in at least one assignment. These are all the students who
have an ungraded assignment for which the deadline has passed.
Babeș-Bolyai University
Cluj Napoca
Faculty of Mathematics and Computer Science
Fundamentals of Programming
- Students with the best school situation, sorted in descending order of the average grade
received for all assignments.

5. Unlimited undo/redo functionality. Each step will undo/redo the previous operation performed by
the user. Undo/redo operations must cascade and have a memory-efficient implementation (no
superfluous list copying).
"""
import operator
from old_files.repositories import *
from old_files.function_objects import *
from copy import deepcopy
from controllers.grade_controller import GradeController
from controllers.undo_controller import UndoController

class Services:
    def __init__(self, studrepo: Repository, assigrepo: Repository):
        self._studentrepo = studrepo
        self._assignmentrepo = assigrepo
        self._undo_stack = []
        self._redo_stack = []
        grade_controller = GradeController(assigrepo, studrepo, GradeRepository(), UndoController())
        self._grade_controller = grade_controller

    def init_grades(self): # Pragma: no cover
        """
        Initializes a list of grades

        :return list: the list of grades
        """
        self._grades = [Grade('1', '1', '10'), Grade('1', '9',  None), Grade('1', '10', None), Grade('2', '1', None), Grade('3', '1', '7'),
                        Grade('2', '7', '10'), Grade('2', '8', '7'), Grade('2', '6', '9'), Grade('7', '1', None), Grade('7', '7', '4'), Grade('8', '7', '3')]

    def assign(self, assignmentID, studentID):
        """
        Function that assigns an assignment to a student

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
        assignment = Grade(assignmentID, studentID, None)
        for grade in self._grades:
            if assignment == grade:
                raise NotUnique("The student already has that assignment!")
        assign = AssignObject(self._grades, assignment)
        assign.execute()
        self._undo_stack.append(assign)
        self._redo_stack.clear()

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
        for assignment in self._assignmentrepo:
            if assignmentID == assignment.id:
                exists = True
        if not exists:
            raise NotExistent("Assignment does not exist!")
        appended = False
        for student in self._studentrepo:
            if student.group == group:
                assigned = False
                for grade in self._grades:
                    if grade.assignmentID == assignmentID and student.id == grade.studentID:
                        assigned = True
                        break
                if not assigned:
                    assign = AssignObject(self._grades, Grade(assignmentID, student.id, None))
                    assign.execute()
                    self._undo_stack.append(assign)
                    appended = True
        if appended is False:
            raise NotExistent("No assignment given! Probably group does not exist!")
        self._redo_stack.clear()

    def get_student_assignments(self, studentID, graded=None):
        """
        Function that gets assignments of a student
        :param studentID: the student
        :param graded: the state of the assignment: graded = 0 => not graded
                                                    graded = 1 => graded
                                                    graded = None => all
        :return: a list of assignments for the given student
        """
        assignments = self.get_assignments()
        if graded == 0:
            grades = deepcopy([assignment for assignment in self._grades
                               if assignment.studentID == studentID and assignment.grade is None])
        elif graded == 1:
            grades = deepcopy([assignment for assignment in self._grades
                               if assignment.studentID == studentID and assignment.grade is not None])
        else:
            grades = deepcopy([assignment for assignment in self._grades
                               if assignment.studentID == studentID])
        studentassigs = [assig.assignmentID for assig in grades]
        return deepcopy([str(assignment) for assignment in assignments if assignment.id in studentassigs])

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
        for agrade in self._grades:
            if studentID == agrade.studentID and assignmentID == agrade.assignmentID:
                gradeobj = GradeFunctionObject(agrade, grade)
                gradeobj.execute()
                self._undo_stack.append(gradeobj)
                self._redo_stack.clear()
                return
        raise NotExistent("Assignment does not exist!")

    @staticmethod
    def sort_grades(grades: list):      # Pragma: no cover
        return sorted(grades, key=operator.attrgetter('grade'), reverse=True)

    def statistic_grades(self, assignmentID):
        grades = [grade for grade in self._grades if grade.grade is not None]
        if len(grades) == 0:
            raise NotExistent("No grades found!")
        grades = self.sort_grades(grades)
        students = []
        assignment = self.find_assignment(assignmentID)
        if assignment is None:
            raise NotExistent("Assignment does not exist!")
        for grade in grades:
            if grade.assignmentID == assignment.id and grade.grade is not None:
                class TransferObj:
                    def __init__(self, *args):
                        self.student = args[0]
                        self.grade = args[1]

                    def __str__(self):
                        return 'Student: ' + self.student + ', Grade: ' + str(self.grade)

                transfer = TransferObj(str(self.find_student(grade.studentID)), grade.grade)
                students.append(transfer)
        if len(students) == 0:
            raise NotExistent("No students are graded for this assignment!")
        return students

    def statistic_assignments(self, assignmentID):
        assignment = self.find_assignment(assignmentID)
        students = []
        today = datetime.datetime.now().date()
        if assignment is None:
            raise NotExistent("Assignment does not exist!")
        for grade in self._grades:
            if grade.grade is None and assignment.id == grade.assignmentID and assignment.deadline < today:
                students.append(str(self.find_student(grade.studentID)))
        if len(students) == 0:
            raise NotExistent("No late students were found!")
        return students

    @property
    def statistic_situation(self):
        """
        Gives the situation of all student, sorted by average grade for all assignments

        :return list: The list of students, sorted by average grade
        """
        if len(self._grades) == 0:
            raise NotExistent('No students have grades yet!')
        students = []
        count = []
        for grade in self._grades:
            student = self.find_student(grade.studentID)
            if student is not None and grade.grade is not None:
                not_added = True
                for i in range(len(students)):
                    if students[i].student == student:
                        students[i].grade += grade.grade
                        count[i] += 1
                        not_added = False
                if not_added:
                    class TransferObj:
                        def __init__(self, *args):
                            self.grade = args[1]
                            self.student = args[0]

                        def __str__(self):
                            return 'Student ' + str(self.student) + ' Grade: ' + str(self.grade)

                    transfer = TransferObj(student, grade.grade)
                    students.append(transfer)
                    count.append(1)
        for i in range(len(students)):
            students[i].grade /= count[i]
            students[i].grade = round(students[i].grade, 2)
        return self.sort_grades(students)       # sorted(students, key=operator.attrgetter('grade'), reverse=True)


    def add_student(self, sid, name, group):
        """
        Adds a new student

        :param sid: the id of the student
        :param name: the name of the student
        :param group: the group fom which the student takes part of
        :return None: success
        :raises NotUnique: id is not unique
        :raises NotAnInt: id is not an int or the group is not an int
        :raises NotAString: name is not a string
        """
        student = Student(sid, name, group)
        self._studentrepo.add_object(student, self._undo_stack)
        self._redo_stack.clear()

    def remove_student(self, sid):
        """
        Removes a student by it's id

        :param sid: the id of the student
        :return None: success
        :raises NotAnInt: the id is not an int
        :raises NotExistent: the student does not exist
        """
        deleted_grades = [grade for grade in self._grades if grade.studentID == sid]
        self._studentrepo.remove_object(sid, deleted_grades, self._grades, self._undo_stack)
        self._redo_stack.clear()

    def update_student(self, sid, new_id, new_name, new_group):
        """
        Updates the id, name and/or group of a student

        :param sid: the id of the student
        :param new_id: the new id (remains the same if left empty)
        :param new_name: the new name (remains the same if left empty)
        :param new_group: the new group (remains the same if left empty)
        :return None: success
        :raises NotAnInt: id, new_id or group are not ints
        :raises NotAString: the name is not a string
        :raises NotExistent: student does not exist
        :raises NotUnique: new id is not unique
        :raises NoUpdate: student was not changed
        """
        if not sid.isnumeric():
            raise NotAnInt("ID should be an int!")
        old_student = self.find_student(sid)
        if old_student is None:
            raise NotExistent("Student does not exist")
        if new_id.isnumeric() and new_id != '':
            for s in self._studentrepo:
                if s.id == new_id:
                    raise NotUnique("ID should be unique!")
        elif new_id != '':
            raise NotAnInt("ID should be an int!")

        updated = 0
        student = []
        if new_id != '':
            student.append(new_id)
            updated = 1
        else:
            student.append(old_student.id)
        if new_name != '':
            student.append(new_name)
            updated = 1
        else:
            student.append(old_student.name)
        if new_group != '':
            student.append(new_group)
            updated = 1
        else:
            student.append(old_student.group)
        if updated == 0:
            raise NoUpdate("No changes made!")
        student = Student(student[0], student[1], student[2])

        self._studentrepo.update_object(self._studentrepo.find_object(sid), student, self._undo_stack)
        self._redo_stack.clear()

    def get_students(self):
        return deepcopy(self._studentrepo.get_objects())

    def show_students(self):
        return [str(student) for student in self.get_students()]

    def add_assignment(self, aid, desc, day, month, year):
        assignment = Assignment(aid, desc, year, month, day)
        self._assignmentrepo.add_object(assignment, self._undo_stack)
        self._redo_stack.clear()

    def remove_assignment(self, aid):
        grades = [grade for grade in self._grades if grade.assignmentID == aid]
        self._assignmentrepo.remove_object(aid, grades, self._grades, self._undo_stack)
        self._redo_stack.clear()

    def update_assignment(self, aid, new_aid, new_desc, new_day, new_month, new_year):
        if not aid.isnumeric():
            raise NotAnInt("ID should be an int!")
        idx = self._assignmentrepo.find_object(aid)
        if idx is None:
            raise NotExistent("Assignment does not exist!")

        if new_aid.isnumeric() and new_aid != '':
            for assig in self._assignmentrepo:
                if assig.id == new_aid:
                    raise NotUnique("ID should be unique!")
        elif new_aid != '':
            raise NotAnInt("ID should be an int!")
        updated = 0
        assignment = []
        old_assignment = self._assignmentrepo[idx]
        if new_aid != '':
            assignment.append(new_aid)
            updated = 1
        else:
            assignment.append(old_assignment.id)
        if new_desc != '':
            assignment.append(new_desc)
            updated = 1
        else:
            assignment.append(old_assignment.description)
        if new_year != '':
            assignment.append(new_year)
            updated = 1
        else:
            assignment.append(old_assignment.deadline.year)
        if new_month != '':
            assignment.append(new_month)
            updated = 1
        else:
            assignment.append(old_assignment.deadline.month)
        if new_day != '':
            assignment.append(new_day)
            updated = 1
        else:
            assignment.append(old_assignment.deadline.day)
        if updated == 0:
            raise NoUpdate("No changes made!")
        assignment = Assignment(assignment[0], assignment[1], assignment[2], assignment[3], assignment[4])
        self._assignmentrepo.update_object(idx, assignment, self._undo_stack)
        self._redo_stack.clear()

    def get_assignments(self):
        return deepcopy(self._assignmentrepo.get_objects())

    def show_grades(self):
        return [str(grade) for grade in self._grades]

    def show_assignments(self):
        return [str(assignment) for assignment in self.get_assignments()]

    def find_student(self, studentID):
        idx = self._studentrepo.find_object(studentID)
        if idx is None:
            return None
        return self._studentrepo[idx]

    def find_assignment(self, assignmentID):
        idx = self._assignmentrepo.find_object(assignmentID)
        if idx is None:
            return None
        return self._assignmentrepo[idx]

    def undo(self):
        if len(self._undo_stack) <= 0:
            raise ValueError("No more undo's!")
        undoable = self._undo_stack.pop()
        undoable.undo()
        self._redo_stack.append(undoable)

    def redo(self):
        if len(self._redo_stack) <= 0:
            raise ValueError("No more redo's!")
        redoable = self._redo_stack.pop()
        redoable.execute()
        self._undo_stack.append(redoable)
