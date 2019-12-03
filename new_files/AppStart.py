from controllers.assignment_controller import AssignmentController
from controllers.grade_controller import GradeController
from controllers.main_controller import MainController
from controllers.student_controller import StudentController
from controllers.undo_controller import UndoController
from new_files.better_UI import UI
from new_files.persistent_repos import PersistentStudentRepo, PersistentAssignmentRepo, PersistentGradeRepo
from new_files.gui import Ui_MainWindow, QApplication, QMainWindow
import sys

from new_files.better_repo import Repository, GradeRepository


class AppStart:
    def __init__(self):
        self._settings = {}
        self._start()
        self._init()

    def _start(self):
        with open('settings.properties', 'r') as f:
            while True:
                repositoryLayout = f.readline().strip('\n').split(' = ')
                if repositoryLayout == ['']:
                    break
                self._settings[repositoryLayout[0]] = repositoryLayout[1].strip("\"")
        '''
        for key in self._settings.keys():
            print(self._settings[key])
        '''

    def _init(self):
        if self._settings['repository'] == 'inmemory':
            studentRepo = Repository()
            studentRepo.initialize_students()
            assignmentRepo = Repository()
            assignmentRepo.initialize_assignments()
            gradeRepo = GradeRepository()
        else:
            studentRepo = PersistentStudentRepo(self._settings['students'], self._settings['repository'])
            assignmentRepo = PersistentAssignmentRepo(self._settings['assignments'], self._settings['repository'])
            gradeRepo = PersistentGradeRepo(self._settings['grades'], self._settings['repository'])
        undoController = UndoController()
        gradeController = GradeController(assignmentRepo, studentRepo, gradeRepo, undoController)
        studentController = StudentController(studentRepo, undoController, gradeController)
        assignmentController = AssignmentController(assignmentRepo, gradeController, undoController)
        main_controller = MainController(gradeController, studentController, undoController, assignmentController)
        if self._settings['UI'] == '':
            ui = UI(main_controller)
            ui.start()
        elif self._settings['UI'] == 'GUI':
            gui = Ui_MainWindow()
            app = QApplication(sys.argv)
            main_window = QMainWindow()
            gui.setupUi(main_window, main_controller)
            main_window.show()
            sys.exit(app.exec_())


app = AppStart()
