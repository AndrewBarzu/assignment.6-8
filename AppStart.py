from controllers.assignment_controller import AssignmentController
from controllers.grade_controller import GradeController
from controllers.main_controller import MainController
from controllers.student_controller import StudentController
from controllers.undo_controller import UndoController
from new_files.better_UI import UI
from new_files.settings import Settings
from new_files.better_repo import Repository, GradeRepository
from new_files.persistent_repos import PersistentStudentRepo, PersistentAssignmentRepo, PersistentGradeRepo
from new_files.gui import Ui_MainWindow, QApplication, QMainWindow
from new_files.json_repo import StudentRepoJSON, AssignmentRepoJSON, GradeRepoJSON
from new_files.db_repo import StudentMongoRepo, AssignmentMongoRepo, GradeMongoRepo
import pymongo
import sys


class AppStart:
    def __init__(self):
        self._settings = Settings()
        self._init()

    def _init(self):
        if self._settings.repository == 'inmemory':
            studentRepo = Repository()
            studentRepo.initialize_students()
            assignmentRepo = Repository()
            assignmentRepo.initialize_assignments()
            gradeRepo = GradeRepository()
            gradeRepo.init_grades()
        elif self._settings.repository == "JSON":
            studentRepo = StudentRepoJSON(self._settings.students)
            assignmentRepo = AssignmentRepoJSON(self._settings.assignments)
            gradeRepo = GradeRepoJSON(self._settings.grades)
        elif self._settings.repository == "DATABASE":
            myClient = pymongo.MongoClient(
                "mongodb+srv://admin:projectdb@cluster0-3x8ss.gcp.mongodb.net/test?retryWrites=true&w=majority")
            studentRepo = StudentMongoRepo(myClient)
            assignmentRepo = AssignmentMongoRepo(myClient)
            gradeRepo = GradeMongoRepo(myClient)
        else:
            studentRepo = PersistentStudentRepo(self._settings.students, self._settings.repository)
            assignmentRepo = PersistentAssignmentRepo(self._settings.assignments, self._settings.repository)
            gradeRepo = PersistentGradeRepo(self._settings.grades, self._settings.repository)
        undoController = UndoController()
        gradeController = GradeController(gradeRepo)
        studentController = StudentController(studentRepo)
        assignmentController = AssignmentController(assignmentRepo)
        main_controller = MainController(gradeController, studentController, undoController, assignmentController)
        if self._settings.ui == '':
            ui = UI(main_controller)
            ui.start()
        elif self._settings.ui == 'GUI':
            gui = Ui_MainWindow()
            app = QApplication(sys.argv)
            main_window = QMainWindow()
            gui.setupUi(main_window, main_controller)
            main_window.show()
            sys.exit(app.exec_())


app = AppStart()
