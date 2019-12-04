from new_files.better_repo import Repository, GradeRepository
from new_files.domain import Student, Assignment, Grade
import _pickle as pickle

class PersistentStudentRepo(Repository):
    def __init__(self, fileName, storageType):
        super(PersistentStudentRepo, self).__init__()

        if storageType == 'textfile':
            self._update_file = self._update_file_text
            self._load_file = self._load_file_text
        elif storageType == 'binaryfile':
            self._update_file = self._update_file_binary
            self._load_file = self._load_file_binary
        self._fileName = fileName
        self._load_file()

    def _load_file_text(self):
        with open(self._fileName, 'r') as f:
            while True:
                student = f.readline().strip('\n').split(',')
                if student == ['']:
                    break
                Repository.add_object(self, Student(*student))

    def _load_file_binary(self):
        with open(self._fileName, 'rb') as f:
            while True:
                try:
                    Repository.add_object(self, pickle.load(f))
                except EOFError:
                    break

    def add_object(self, object):
        super(PersistentStudentRepo, self).add_object(object)
        self._update_file()

    def remove_object(self, id):
        super(PersistentStudentRepo, self).remove_object(id)
        self._update_file()

    def update_object(self, idx, object):
        super(PersistentStudentRepo, self).update_object(idx, object)
        self._update_file()

    def _update_file_text(self):
        with open(self._fileName, 'w') as f:
            for student in self._objects:
                f.write(student.id + ',' + student.name + ',' + student.group + '\n')

    def _update_file_binary(self):
        with open(self._fileName, 'wb') as f:
            for student in self._objects:
                pickle.dump(student, f)


class PersistentAssignmentRepo(Repository):
    def __init__(self, fileName, storageType):
        super(PersistentAssignmentRepo, self).__init__()

        if storageType == 'textfile':
            self._update_file = self._update_file_text
            self._load_file = self._load_file_text
        elif storageType == 'binaryfile':
            self._update_file = self._update_file_binary
            self._load_file = self._load_file_binary
        self._fileName = fileName
        self._load_file()

    def _load_file_text(self):
        with open(self._fileName, 'r') as f:
            while True:
                assignment = f.readline().strip('\n').split(',')
                if assignment == ['']:
                    break
                Repository.add_object(self, Assignment(*assignment))

    def _load_file_binary(self):
        with open(self._fileName, 'rb') as f:
            while True:
                try:
                    Repository.add_object(self, pickle.load(f))
                except EOFError:
                    break

    def add_object(self, object):
        super(PersistentAssignmentRepo, self).add_object(object)
        self._update_file()

    def remove_object(self, id):
        super(PersistentAssignmentRepo, self).remove_object(id)
        self._update_file()

    def update_object(self, idx, object):
        super(PersistentAssignmentRepo, self).update_object(idx, object)
        self._update_file()

    def _update_file_text(self):
        with open(self._fileName, 'w') as f:
            for assignment in self._objects:
                f.write(assignment.id + ',' + assignment.description + ',' + str(assignment.deadline).replace('-', ',') + '\n')

    def _update_file_binary(self):
        with open(self._fileName, 'wb') as f:
            for assignment in self._objects:
                pickle.dump(assignment, f)


class PersistentGradeRepo(GradeRepository):
    def __init__(self, fileName, storageType):
        super(PersistentGradeRepo, self).__init__()

        if storageType == 'textfile':
            self._update_file = self._update_file_text
            self._load_file = self._load_file_text
        elif storageType == 'binaryfile':
            self._update_file = self._update_file_binary
            self._load_file = self._load_file_binary
        self._fileName = fileName
        self._load_file()

    def _load_file_text(self):
        with open(self._fileName, 'r') as f:
            while True:
                grade = f.readline().strip('\n').split(',')
                if grade == ['']:
                    break
                GradeRepository.add(self, Grade(*grade))

    def _load_file_binary(self):
        with open(self._fileName, 'rb') as f:
            while True:
                try:
                    GradeRepository.add(self, pickle.load(f))
                except EOFError:
                    break

    def _update_file_text(self):
        with open(self._fileName, 'w') as f:
            for grade in self._grades:
                f.write(grade.studentID + ',' + grade.assignmentID + ',' + str(grade.grade) + '\n')

    def _update_file_binary(self):
        with open(self._fileName, 'wb') as f:
            for grade in self._grades:
                pickle.dump(grade, f)

    def add(self, grade):
        super(PersistentGradeRepo, self).add(grade)
        self._update_file()

    def delete(self, studentID, assignmentID):
        super(PersistentGradeRepo, self).delete(studentID, assignmentID)
        self._update_file()

    def grade(self, sid, aid, new_grade):
        super(PersistentGradeRepo, self).grade(sid, aid, new_grade)
        self._update_file()

    def extend(self, more):
        super(PersistentGradeRepo, self).extend(more)
        self._update_file()

