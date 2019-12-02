from PyQt5.QtCore import *
from controllers.assignment_controller import AssignmentController
from controllers.grade_controller import GradeController
from controllers.student_controller import StudentController
from controllers.undo_controller import UndoController
from new_files.GUI_elements.dialogue_boxes import *
import sys

from new_files.better_repo import Repository, GradeRepository


class Ui_MainWindow(object):
    def setupUi(self, MainWindow, controller):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(851, 657)
        self.controller = controller
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.controller.init_grades()

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

        self.listView = QListWidget(self.centralwidget)
        self.listView.setObjectName("listView")
        self.show_grades()

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
        self.show_grades()


    def on_add_assignment_click(self):
        self.dialog = AddAssignmentDialogBox(self.controller, self.show_assignments)
        self.dialog.show()


    def on_remove_assignment_click(self):
        self.dialog = RemoveDialogBox("assignment", self.controller, self.show_assignments)
        self.dialog.show()


    def on_update_assignment_click(self):
        self.dialog = UpdateAssignmentDialogBox(self.controller, self.show_assignments)
        self.dialog.show()

    def show_assignments(self):
        self.listView.clear()
        assignments = self.controller.show_assignments()
        for assignment in assignments:
            listWidget = QListWidgetItem()
            self.listView.addItem(listWidget)
            self.listView.setItemWidget(listWidget, QLabel(assignment))


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
        updateAssignmentButton.clicked.connect(self.on_update_assignment_click)
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
        self.dialog = AddStudentDialogBox(self.controller, self.show_students)
        self.dialog.show()


    def on_remove_student_click(self):
        self.dialog = RemoveDialogBox("student", self.controller, self.show_students)
        self.dialog.show()


    def on_update_student_click(self):
        self.dialog = UpdateStudentDialogBox(self.controller, self.show_students)
        self.dialog.show()


    def show_students(self):
        self.listView.clear()
        students = self.controller.show_students()
        for student in students:
            listWidget = QListWidgetItem()
            self.listView.addItem(listWidget)
            self.listView.setItemWidget(listWidget, QLabel(student))


    def assign_student_click(self):
        self.dialog = AssignStudentDialogBox(self.controller, self.show_grades)
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
        updateStudentButton.clicked.connect(self.on_update_student_click)
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
        self.show_students()


    def on_assignment_menu_click(self):
        self.mainLayout.hide()
        self.assignmentMenuLayout.show()
        self.show_assignments()


    def show_grades(self):
        self.listView.clear()
        grades = self.controller.show_grades()
        for grade in grades:
            item = QListWidgetItem()
            self.listView.addItem(item)
            self.listView.setItemWidget(item, QLabel(grade))


    def on_assign_student_click(self):
        try:
            self.assignStudentDialog = AssignStudentDialogBox(self.controller, self.show_grades)
            self.assignStudentDialog.show()
        except Exception as e:
            print(e)


    def on_grade_click(self):
        try:
            self.gradeStudentDialog = GradeDialogBox(self.controller, self.show_grades)
            self.gradeStudentDialog.show()
        except Exception as e:
            print(e)


    def on_assign_group_click(self):
        try:
            self.assignGroupDialog = AssignGroupDialogBox(self.controller, self.show_grades)
            self.assignGroupDialog.show()
        except Exception as e:
            print(e)


    def on_undo_click(self):
        try:
            self.controller.undo()
            self.show_grades()
        except Exception as e:
            self.errorDialog = ErrorDialogBox(e)
            self.errorDialog.show()


    def on_redo_click(self):
        try:
            self.controller.redo()
            self.show_grades()
        except Exception as e:
            self.errorDialog = ErrorDialogBox(e)
            self.errorDialog.show()


    def on_grade_statistics_click(self):
        try:
            self.statisticGradesDialog = GradeStatisticsDialog(self.controller)
            self.statisticGradesDialog.show()
        except Exception as e:
            self.errorDialog = ErrorDialogBox(e)
            self.errorDialog.show()


    def on_deadline_statistics_click(self):
        try:
            self.statisticDeadlineDialog = DeadlineStatisticsDialog(self.controller)
            self.statisticDeadlineDialog.show()
        except Exception as e:
            self.errorDialog = ErrorDialogBox(e)
            self.errorDialog.show()


    def on_situation_statistic_click(self):
        try:
            self.statisticSituationDialog = SituationStatisticDialog(self.controller)
            self.statisticSituationDialog.show()
        except Exception as e:
            self.errorDialog = ErrorDialogBox(e)
            self.errorDialog.show()


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
        gradeStudentButton.clicked.connect(self.on_grade_click)
        layout.addWidget(gradeStudentButton)

        assignStudentButton = QPushButton(self.centralwidget)
        assignStudentButton.setObjectName("assignStudentButton")
        assignStudentButton.setText(_translate("MainWindow", "Assign Student"))
        assignStudentButton.clicked.connect(self.on_assign_student_click)
        layout.addWidget(assignStudentButton)

        assignGroupButton = QPushButton(self.centralwidget)
        assignGroupButton.setObjectName("assignGroupButton")
        assignGroupButton.setText(_translate("MainWindow", "Assign Group"))
        assignGroupButton.clicked.connect(self.on_assign_group_click)
        layout.addWidget(assignGroupButton)

        statisticGradesButton = QPushButton(self.centralwidget)
        statisticGradesButton.setObjectName("statisticGradesButton")
        statisticGradesButton.setText(_translate("MainWindow", "Grade Statistics"))
        statisticGradesButton.clicked.connect(self.on_grade_statistics_click)
        layout.addWidget(statisticGradesButton)

        statisticDeadlineButton = QPushButton(self.centralwidget)
        statisticDeadlineButton.setObjectName("statisticDeadlineButton")
        statisticDeadlineButton.setText(_translate("MainWindow", "Deadline Statistics"))
        statisticDeadlineButton.clicked.connect(self.on_deadline_statistics_click)
        layout.addWidget(statisticDeadlineButton)

        statisticSituationButton = QPushButton(self.centralwidget)
        statisticSituationButton.setObjectName("statisticSituationButton")
        statisticSituationButton.setText(_translate("MainWindow", "Situation Statistics"))
        statisticSituationButton.clicked.connect(self.on_situation_statistic_click)
        layout.addWidget(statisticSituationButton)

        undoButton = QPushButton(self.centralwidget)
        undoButton.setObjectName("undoButton")
        undoButton.setText(_translate("MainWindow", "Undo"))
        undoButton.clicked.connect(self.on_undo_click)
        layout.addWidget(undoButton)

        redoButton = QPushButton(self.centralwidget)
        redoButton.setObjectName("redoButton")
        redoButton.setText(_translate("MainWindow", "Redo"))
        redoButton.clicked.connect(self.on_redo_click)
        layout.addWidget(redoButton)

        spacerItem1 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        layout.addItem(spacerItem1)
        return layout

    @staticmethod
    def retranslateUi(MainWindow):
        _translate = QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))

studentRepo = Repository()
studentRepo.initialize_students()
assignmentRepo = Repository()
assignmentRepo.initialize_assignments()
gradeRepo = GradeRepository()
undoController = UndoController()
gradeController = GradeController(assignmentRepo, studentRepo, gradeRepo, undoController)
studentController = StudentController(studentRepo, undoController, gradeController)
assignmentController = AssignmentController(assignmentRepo, gradeController, undoController)
main_controller = MainController(gradeController, studentController, undoController, assignmentController)

gui = Ui_MainWindow()
app = QApplication(sys.argv)
main_window = QMainWindow()
gui.setupUi(main_window, main_controller)
main_window.show()
sys.exit(app.exec_())
