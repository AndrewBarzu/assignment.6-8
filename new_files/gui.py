from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from new_files.GUI_elements.dialogue_boxes import *
import sys


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(851, 657)

        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        mainLayout = QVBoxLayout()
        mainLayout.setObjectName("mainLayout")
        mainLayout = self.init_main_menu(mainLayout)
        mainLayout.widget()
        self.mainLayout = QFrame()
        self.mainLayout.setLayout(mainLayout)

        studentMenuLayout = QVBoxLayout()
        studentMenuLayout.setObjectName("studentMenuLayout")
        studentMenuLayout = self.init_student_menu(studentMenuLayout)
        self.studentMenuLayout = QFrame()
        self.studentMenuLayout.setLayout(studentMenuLayout)

        assignmentMenuLayout = QVBoxLayout()
        assignmentMenuLayout.setObjectName("assignmentMenuLayout")
        assignmentMenuLayout = self.init_assignment_menu(assignmentMenuLayout)
        self.assignmentMenuLayout = QFrame()
        self.assignmentMenuLayout.setLayout(assignmentMenuLayout)

        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")

        self.listView = QListView(self.centralwidget)
        self.listView.setObjectName("listView")

        self.gridLayout.addWidget(self.studentMenuLayout, 0, 1)
        self.studentMenuLayout.hide()
        self.gridLayout.addWidget(self.assignmentMenuLayout, 0, 1)
        self.assignmentMenuLayout.hide()
        self.gridLayout.addWidget(self.mainLayout, 0, 1)
        self.gridLayout.addWidget(self.listView, 0, 2, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setGeometry(QRect(0, 0, 851, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QMetaObject.connectSlotsByName(MainWindow)
        self.mainWindow = MainWindow


    def on_back_click(self):
        self.assignmentMenuLayout.hide()
        self.studentMenuLayout.hide()
        self.mainLayout.show()


    def on_add_assignment_click(self):
        self.dialog = AddAssignmentDialogBox()
        self.dialog.show()


    def on_remove_assignment_click(self):
        self.dialog = RemoveDialogBox("assignment")
        self.dialog.show()


    def init_assignment_menu(self, layout):
        _translate = QCoreApplication.translate

        spacerItem = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        layout.addItem(spacerItem)

        # Add assignment
        addAssignmentButton = QPushButton(self.centralwidget)
        addAssignmentButton.setObjectName("addAssignmentButton")
        addAssignmentButton.setText(_translate("MainWindow", "Add Assignment"))
        addAssignmentButton.clicked.connect(self.on_add_assignment_click)
        layout.addWidget(addAssignmentButton)

        # Remove assignment
        removeAssignmentButton = QPushButton(self.centralwidget)
        removeAssignmentButton.setObjectName("removeAssignmentButton")
        removeAssignmentButton.setText(_translate("MainWindow", "Remove Assignment"))
        removeAssignmentButton.clicked.connect(self.on_remove_assignment_click)
        layout.addWidget(removeAssignmentButton)

        # Update assignment
        updateAssignmentButton = QPushButton(self.centralwidget)
        updateAssignmentButton.setObjectName("updateAssignmentButton")
        updateAssignmentButton.setText(_translate("MainWindow", "Update Assignment"))
        layout.addWidget(updateAssignmentButton)

        # Back
        backButton = QPushButton(self.centralwidget)
        backButton.setObjectName("backButton")
        backButton.setText(_translate("MainMenu", "Back"))
        backButton.clicked.connect(self.on_back_click)
        layout.addWidget(backButton)

        spacerItem1 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        layout.addItem(spacerItem1)
        return layout


    def on_add_student_click(self):
        self.dialog = AddStudentDialogBox()
        self.dialog.show()

    def on_remove_student_click(self):
        self.dialog = RemoveDialogBox("student")
        self.dialog.show()

    def init_student_menu(self, layout):
        _translate = QCoreApplication.translate

        spacerItem = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        layout.addItem(spacerItem)

        # Add student
        addStudentButton = QPushButton(self.centralwidget)
        addStudentButton.setObjectName("addStudentButton")
        addStudentButton.setText(_translate("MainWindow", "Add Student"))
        addStudentButton.clicked.connect(self.on_add_student_click)
        layout.addWidget(addStudentButton)

        # Remove assignment
        removeStudentButton = QPushButton(self.centralwidget)
        removeStudentButton.setObjectName("removeStudentButton")
        removeStudentButton.setText(_translate("MainWindow", "Remove Student"))
        removeStudentButton.clicked.connect(self.on_remove_student_click)
        layout.addWidget(removeStudentButton)

        # Update assignment
        updateStudentButton = QPushButton(self.centralwidget)
        updateStudentButton.setObjectName("updateStudentButton")
        updateStudentButton.setText(_translate("MainWindow", "Update Student"))
        layout.addWidget(updateStudentButton)

        # Back
        backButton = QPushButton(self.centralwidget)
        backButton.setObjectName("backButton")
        backButton.setText(_translate("MainMenu", "Back"))
        backButton.clicked.connect(self.on_back_click)
        layout.addWidget(backButton)

        spacerItem1 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        layout.addItem(spacerItem1)
        return layout


    def on_student_menu_click(self):
        self.mainLayout.hide()
        self.studentMenuLayout.show()

    def on_assignment_menu_click(self):
        self.mainLayout.hide()
        self.assignmentMenuLayout.show()

    def init_main_menu(self, layout):
        _translate = QCoreApplication.translate

        spacerItem = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        layout.addItem(spacerItem)

        studentMenuButton = QPushButton(self.centralwidget)
        studentMenuButton.setObjectName("studentMenuButton")
        studentMenuButton.setText(_translate("MainWindow", "Student Menu"))
        studentMenuButton.clicked.connect(self.on_student_menu_click)
        layout.addWidget(studentMenuButton)

        assignmentMenuButton = QPushButton(self.centralwidget)
        assignmentMenuButton.setObjectName("assignmentMenuButton")
        assignmentMenuButton.setText(_translate("MainWindow", "Assignment Menu"))
        assignmentMenuButton.clicked.connect(self.on_assignment_menu_click)
        layout.addWidget(assignmentMenuButton)

        gradeStudentButton = QPushButton(self.centralwidget)
        gradeStudentButton.setObjectName("gradeStudentButton")
        gradeStudentButton.setText(_translate("MainWindow", "Grade Student"))
        layout.addWidget(gradeStudentButton)

        assignStudentButton = QPushButton(self.centralwidget)
        assignStudentButton.setObjectName("assignStudentButton")
        assignStudentButton.setText(_translate("MainWindow", "Assign Student"))
        layout.addWidget(assignStudentButton)

        assignGroupButton = QPushButton(self.centralwidget)
        assignGroupButton.setObjectName("assignGroupButton")
        assignGroupButton.setText(_translate("MainWindow", "Assign Group"))
        layout.addWidget(assignGroupButton)

        undoButton = QPushButton(self.centralwidget)
        undoButton.setObjectName("undoButton")
        undoButton.setText(_translate("MainWindow", "Undo"))
        layout.addWidget(undoButton)

        redoButton = QPushButton(self.centralwidget)
        redoButton.setObjectName("redoButton")
        redoButton.setText(_translate("MainWindow", "Redo"))
        layout.addWidget(redoButton)

        spacerItem1 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        layout.addItem(spacerItem1)
        return layout


    def retranslateUi(self, MainWindow):
        _translate = QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))


gui = Ui_MainWindow()
app = QApplication(sys.argv)
main_window = QMainWindow()
gui.setupUi(main_window)
main_window.show()
sys.exit(app.exec_())
