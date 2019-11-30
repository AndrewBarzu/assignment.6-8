from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import *


class AddStudentDialogBox(QWidget):
    def __init__(self, parent=None):
        super(AddStudentDialogBox, self).__init__(parent)

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
        self.ok.clicked.connect(self.ok_pressed)
        layout.addRow(self.ok)

        self.setLayout(layout)
        self.setWindowTitle("Add student")
        self.resize(400, 150)

    def ok_pressed(self):
        self.close()

class AddAssignmentDialogBox(QWidget):
    def __init__(self, parent=None):
        super(AddAssignmentDialogBox, self).__init__(parent)

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
        self.date = QLabel("Date: ")
        layout.addRow(self.date, cal)

        self.ok = QPushButton("Add assignment")
        layout.addRow(self.ok)

        self.setLayout(layout)
        self.setWindowTitle("Add assignment")
        self.resize(400, 150)

    def showDate(self, date):
        self.date.setText("Date: " + date.toString())

class RemoveDialogBox(QWidget):
    def __init__(self, caller: str, parent=None):
        super(RemoveDialogBox, self).__init__(parent)

        layout = QFormLayout()

        idText = QLabel(str.capitalize(caller) + " ID: ")
        self.id = QLineEdit()
        layout.addRow(idText, self.id)

        self.setLayout(layout)
        self.setWindowTitle("Remove " + caller)
        self.resize(400, 150)

class ErrorDialogBox(QWidget):
    def __init__(self, error: str, parent=None):
        super(ErrorDialogBox, self).__init__(parent)

        layout = QFormLayout()

        idText = QLabel("Error!" + error)
        layout.addRow(idText)

        self.ok = QPushButton("Ok")
        self.ok.clicked.connect(self.ok_pressed)
        layout.addRow(self.ok)

        self.setLayout(layout)
        self.setWindowTitle("Error")
        self.resize(300, 100)

    def ok_pressed(self):
        self.close()
