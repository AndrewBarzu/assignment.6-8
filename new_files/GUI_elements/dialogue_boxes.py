from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import *
from controllers.main_controller import MainController

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
    def __init__(self, controller: MainController, show_grades, parent=None):
        super(AssignStudentDialogBox, self).__init__(parent)

