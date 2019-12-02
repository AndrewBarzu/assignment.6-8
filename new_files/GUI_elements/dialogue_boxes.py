from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from controllers.main_controller import MainController
from new_files.exceptions import *
import re

class ErrorDialogBox(QWidget):
    def __init__(self, error: Exception, parent=None):
        super(ErrorDialogBox, self).__init__(parent)

        layout = QFormLayout()

        idText = QLabel("Error! " + str(error))
        layout.addRow(idText)

        self.ok = QPushButton("Ok")
        self.ok.clicked.connect(self.ok_pressed)
        layout.addRow(self.ok)

        self.setLayout(layout)
        self.setWindowTitle("Error")
        self.resize(300, 100)


    def ok_pressed(self):
        self.close()

class AddStudentDialogBox(QWidget):
    def __init__(self, controller: MainController, show_students, parent=None):
        super(AddStudentDialogBox, self).__init__(parent)

        self.controller = controller

        self.show_students = show_students

        layout = QFormLayout()

        idText = QLabel("Student ID: ")
        self.id = QLineEdit()
        layout.addRow(idText, self.id)

        nameText = QLabel("Student name: ")
        self.name = QLineEdit()
        layout.addRow(nameText, self.name)

        groupText = QLabel("Group: ")
        self.group = QLineEdit()
        layout.addRow(groupText, self.group)

        self.ok = QPushButton("Add student")
        self.ok.clicked.connect(self.on_add_student_press)
        layout.addRow(self.ok)

        self.setLayout(layout)
        self.setWindowTitle("Add student")
        self.resize(400, 150)

    def on_add_student_press(self):
        try:
            self.controller.add_student(self.id.text(), self.name.text(), self.group.text())
            self.close()
            self.show_students()
        except Exception as e:
            self.dialog = ErrorDialogBox(e)
            self.dialog.show()


class AddAssignmentDialogBox(QWidget):
    def __init__(self, controller: MainController, show_assignments, parent=None):
        super(AddAssignmentDialogBox, self).__init__(parent)

        self.controller = controller

        self.show_assignments = show_assignments
        layout = QFormLayout()

        idText = QLabel("Assignment ID: ")
        self.id = QLineEdit()
        layout.addRow(idText, self.id)

        nameText = QLabel("Assignment description: ")
        self.desc = QLineEdit()
        layout.addRow(nameText, self.desc)

        cal = QCalendarWidget(self)
        cal.setGridVisible(True)
        cal.move(20, 20)
        cal.clicked[QDate].connect(self.showDate)
        self.transferDate = None
        self.date = QLabel("Date: ")
        layout.addRow(self.date, cal)

        self.ok = QPushButton("Add assignment")
        self.ok.clicked.connect(self.on_add_assignment_press)
        layout.addRow(self.ok)

        self.setLayout(layout)
        self.setWindowTitle("Add assignment")
        self.resize(400, 150)

    def on_add_assignment_press(self):
        try:
            self.controller.add_assignment(self.id.text(), self.desc.text(), str(self.transferDate.day()),
                                           str(self.transferDate.month()), str(self.transferDate.year()))
            self.close()
            self.show_assignments()
        except Exception as e:
            self.dialog = ErrorDialogBox(e)
            self.dialog.show()

    def showDate(self, date):
        self.transferDate = date
        self.date.setText("Date: " + date.toString())

class RemoveDialogBox(QWidget):
    def __init__(self, caller, controller: MainController, show_function, parent=None):
        super(RemoveDialogBox, self).__init__(parent)

        self.show_function = show_function

        self.caller = caller
        self.controller = controller
        layout = QFormLayout()

        idText = QLabel(str.capitalize(caller) + " ID: ")
        self.id = QLineEdit()
        layout.addRow(idText, self.id)

        self.ok = QPushButton("Remove")
        self.ok.clicked.connect(self.on_remove)
        layout.addRow(self.ok)

        self.setLayout(layout)
        self.setWindowTitle("Remove " + caller)
        self.resize(400, 60)

    def on_remove(self):
        try:
            if self.caller == "student":
                self.controller.remove_student(self.id.text())
            else:
                self.controller.remove_assignment(self.id.text())
            self.close()
            self.show_function()
        except Exception as e:
            self.dialog = ErrorDialogBox(e)
            self.dialog.show()



class UpdateStudentDialogBox(QWidget):
    def __init__(self, controller: MainController, show_students, parent=None):
        super(UpdateStudentDialogBox, self).__init__(parent)

        self.show_students = show_students

        self.controller = controller
        layout = QFormLayout()

        oldIdText = QLabel("Old ID: ")
        self.oldId = QLineEdit()
        layout.addRow(oldIdText, self.oldId)

        idText = QLabel("New ID: ")
        self.newId = QLineEdit()
        layout.addRow(idText, self.newId)

        nameText = QLabel("New name: ")
        self.newName = QLineEdit()
        layout.addRow(nameText, self.newName)

        groupText = QLabel("New group: ")
        self.newGroup = QLineEdit()
        layout.addRow(groupText, self.newGroup)

        self.ok = QPushButton("Update student")
        self.ok.clicked.connect(self.ok_pressed)
        layout.addRow(self.ok)

        self.setLayout(layout)
        self.setWindowTitle("Update student")
        self.resize(400, 150)


    def ok_pressed(self):
        try:
            self.controller.update_student(self.oldId.text(), self.newId.text(), self.newName.text(), self.newGroup.text())
            self.close()
            self.show_students()
        except Exception as e:
            self.dialog = ErrorDialogBox(e)
            self.dialog.show()


class UpdateAssignmentDialogBox(QWidget):
    def __init__(self, controller: MainController, show_assignments, parent=None):
        super(UpdateAssignmentDialogBox, self).__init__(parent)

        self.controller = controller
        self.show_assignments = show_assignments
        layout = QFormLayout()

        oldIdText = QLabel("Old ID: ")
        self.oldId = QLineEdit()
        layout.addRow(oldIdText, self.oldId)

        idText = QLabel("Assignment ID: ")
        self.newId = QLineEdit()
        layout.addRow(idText, self.newId)

        nameText = QLabel("Assignment description: ")
        self.newDesc = QLineEdit()
        layout.addRow(nameText, self.newDesc)

        cal = QCalendarWidget(self)
        cal.setGridVisible(True)
        cal.move(20, 20)
        cal.clicked[QDate].connect(self.showDate)
        self.newDate = None
        self.date = QLabel("New date: ")
        layout.addRow(self.date, cal)

        self.ok = QPushButton("Update assignment")
        self.ok.clicked.connect(self.ok_pressed)
        layout.addRow(self.ok)

        self.setLayout(layout)
        self.setWindowTitle("Update assignment")
        self.resize(400, 150)

    def ok_pressed(self):
        try:
            self.controller.update_assignment(self.oldId.text(), self.newId.text(), self.newDesc.text(), str(self.newDate.day()),
                                              str(self.newDate.month()), str(self.newDate.year()))
            self.close()
            self.show_assignments()
        except Exception as e:
            self.dialog = ErrorDialogBox(e)
            self.dialog.show()

    def showDate(self, date):
        self.newDate = date
        self.date.setText("New date: " + date.toString())


class AssignStudentDialogBox(QWidget):
    def __init__(self, controller: MainController, showGrades, parent=None):
        super(AssignStudentDialogBox, self).__init__(parent)

        self.controller = controller

        self.showGrades = showGrades

        layout = QVBoxLayout()
        box = QHBoxLayout()

        self.students = QListWidget()
        students = controller.show_students()
        for student in students:
            item = QListWidgetItem()
            item.setText(student)
            self.students.addItem(item)

        self.assignments = QListWidget()
        assignments = controller.show_assignments()
        for assignment in assignments:
            item = QListWidgetItem()
            item.setText(assignment)
            self.assignments.addItem(item)

        box.addWidget(self.students)
        box.addSpacerItem(QSpacerItem(10, 10))
        box.addWidget(self.assignments)
        layout.addItem(box)

        box = QHBoxLayout()
        box.addSpacerItem(QSpacerItem(0, 0, QSizePolicy.Maximum, QSizePolicy.Expanding))
        self.assign = QPushButton("Assign")
        self.assign.setFixedWidth(100)
        self.assign.clicked.connect(self.on_assign_click)
        box.addWidget(self.assign)
        box.addSpacerItem(QSpacerItem(0, 0, QSizePolicy.Maximum, QSizePolicy.Expanding))
        layout.addItem(box)

        self.setLayout(layout)
        self.resize(900, 300)
        self.setWindowTitle("Assign")

    def on_assign_click(self):
        try:
            assignment = self.assignments.currentItem()
            if assignment is None:
                raise NotExistent("No assignment selected!")
            assignment = assignment.text()
            assignment = re.match(r"ID: \d+", assignment)
            assignment = re.findall(r"\d+", assignment.group())[0]
            student = self.students.currentItem()
            if student is None:
                raise NotExistent("No student selected!")
            student = student.text()
            student = re.match(r"ID: \d+", student)
            student = re.findall(r"\d+", student.group())[0]
            self.controller.assign(assignment, student)
            self.showGrades()
            self.close()
        except Exception as e:
            self.errorDialog = ErrorDialogBox(e)
            self.errorDialog.show()

class AssignGroupDialogBox(QWidget):
    def __init__(self, controller: MainController, show_grades, parent=None):
        super(AssignGroupDialogBox, self).__init__(parent)
        self.controller = controller
        self.showGrades = show_grades

        layout = QVBoxLayout()

        box = QHBoxLayout()
        box.addWidget(QLabel("Group: "))

        self.group = QLineEdit()
        box.addWidget(self.group)

        layout.addItem(box)

        self.assignments = QListWidget()
        assignments = controller.show_assignments()
        for assignment in assignments:
            item = QListWidgetItem()
            item.setText(assignment)
            self.assignments.addItem(item)

        layout.addWidget(self.assignments)

        self.assign = QPushButton("Assign")
        self.assign.clicked.connect(self.on_assign_click)
        layout.addWidget(self.assign)

        self.setLayout(layout)
        self.resize(600, 300)
        self.setWindowTitle("Assign group")

    def on_assign_click(self):
        try:
            assignment = self.assignments.currentItem()
            if assignment is None:
                raise NotExistent("No assignment selected")
            assignment = assignment.text()
            assignment = re.match(r"ID: \d+", assignment)
            assignment = re.findall(r"\d+", assignment.group())[0]
            group = self.group.text()
            self.controller.assign_group(assignment, group)
            self.showGrades()
            self.close()
        except Exception as e:
            self.errorDialog = ErrorDialogBox(e)
            self.errorDialog.show()


class GradeDialogBox(QWidget):
    def __init__(self, controller: MainController, show_grades, assignments, student, parent=None):
        super(GradeDialogBox, self).__init__(parent)
        self.controller = controller
        self.show_grades = show_grades
        self.student = student

        layout = QVBoxLayout()

        self.assignments = QListWidget()
        for assignment in assignments:
            item = QListWidgetItem()
            item.setText(str(assignment))
            self.assignments.addItem(item)
        layout.addWidget(self.assignments)

        box = QHBoxLayout()
        box.addWidget(QLabel("Grade: "))
        self.grade = QLineEdit()
        box.addWidget(self.grade)

        layout.addItem(box)

        self.gradeButton = QPushButton("Grade")
        self.gradeButton.clicked.connect(self.on_grade_click)
        layout.addWidget(self.gradeButton)

        self.setLayout(layout)
        self.setWindowTitle("Grade")

    def on_grade_click(self):
        try:
            assignment = self.assignments.currentItem()
            if assignment is None:
                raise NotExistent("No assignment selected!")
            assignment = assignment.text()
            assignment = re.findall(r"\d+", assignment)[1]
            self.controller.grade(assignment, self.student, self.grade.text())
            self.show_grades()
            self.close()
        except Exception as e:
            self.errorDialog = ErrorDialogBox(e)
            self.errorDialog.show()


class StudentSelectorDialogBox(QWidget):
    def __init__(self, controller: MainController, show_grades, parent=None):
        super(StudentSelectorDialogBox, self).__init__(parent)

        students = controller.show_students()
        self.controller = controller
        self.show_grades = show_grades
        layout = QVBoxLayout()
        self.students = QListWidget()
        for student in students:
            item = QListWidgetItem()
            item.setText(student)
            self.students.addItem(item)
        layout.addWidget(self.students)

        self.select = QPushButton("Select")
        self.select.clicked.connect(self.on_select_clicked)
        layout.addWidget(self.select)

        self.setLayout(layout)
        self.setWindowTitle("Select student")

    def on_select_clicked(self):
        student = self.students.currentItem()
        if student is None:
            raise NotExistent("No student selected!")
        student = student.text()
        student = re.match(r"ID: \d+", student)
        student = re.findall(r"\d+", student.group())[0]
        assignments = self.controller.get_student_assignments(student, 0)
        if len(assignments) == 0:
            self.errorDialog = ErrorDialogBox(NotExistent("No assignments for this student!"))
            self.errorDialog.show()

        else:
            self.gradeDialog = GradeDialogBox(self.controller, self.show_grades, assignments, student)
            self.gradeDialog.show()
        self.close()

# THIS ONE I A REALLY NICE IDEA, BUT IT SHOULD BE THOUGHT MORE OVER

'''

class Communicate(QObject):
    signal = pyqtSignal()


class SelectorDialog(QWidget):
    def __init__(self, itemList: list, function, *params, nextDialog=None, parent=None, showGrades=None):
        super(SelectorDialog, self).__init__(parent)

        self.function = function

        self.params = params
        self.showGrades = showGrades
        self.communicate = Communicate()
        if nextDialog is not None:
            self.communicate.signal.connect(nextDialog.show)
            self.nexDialog = nextDialog
        else:
            self.communicate.signal = None

        layout = QFormLayout()
        self.listView = QListWidget()
        layout.addRow(self.listView)

        self.selectButton = QPushButton("Select")
        self.selectButton.clicked.connect(self.on_select_push)
        layout.addRow(self.selectButton)

        for item in itemList:
            listItem = QListWidgetItem(self.listView)
            listItem.setText(item)
            self.listView.addItem(listItem)

        self.setLayout(layout)
        self.setWindowTitle("Select")

    def on_select_push(self):
        try:
            selected = self.listView.currentItem()
            object = selected.text()
            object = re.match(r"ID: \d+", object)
            object = re.findall(r"\d+", object.group())[0]
            if self.communicate.signal is not None:
                self.nexDialog.params = object
                self.communicate.signal.emit()
            else:
                self.params = object, self.params
                self.function(*self.params)
                self.showGrades()
            self.close()
        except Exception as e:
            self.dialog = ErrorDialogBox(e)
            self.dialog.show()

class AssignStudentDialogBox:
    def __init__(self, controller: MainController, show_grades):

        students = controller.show_students()
        assignments = controller.show_assignments()
        self.controller = controller
        self.assignmentSelectorDialog = SelectorDialog(assignments, self.controller.assign, showGrades=show_grades)
        self.studentSelectorDialog = SelectorDialog(students, self.controller.assign, nextDialog=self.assignmentSelectorDialog)

    def select(self):
        try:
            self.studentSelectorDialog.show()
        except Exception as e:
            self.dialog = ErrorDialogBox(e)
            self.dialog.show()
'''