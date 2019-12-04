from new_files.better_repo import GradeRepository, Repository
from new_files.domain import Grade, Assignment, Student
import json

class StudentRepoJSON(Repository):
    def __init__(self, jsonFile):
        super(StudentRepoJSON, self).__init__()

        self._jsonFile = jsonFile
        self._load_file()

    def _encode(self):
        return [{"id": student.id, "name": student.name, "group": student.group} for student in self._objects]

    def _decode(self, json):
        return [Student(student['id'], student['name'], student['group']) for student in json]

    def _load_file(self):
        try:
            with open(self._jsonFile, 'r') as f:
                myJson = json.load(f)
                self._objects = self._decode(myJson)
        except json.decoder.JSONDecodeError as e:
            pass

    def _update_json(self):
        serialized = self._encode()
        self._pretty_format(serialized)

    def _pretty_format(self, output):
        with open(self._jsonFile, 'w') as f:
            f.write(json.dumps(output, indent=4))

    def add_object(self, student):
        super(StudentRepoJSON, self).add_object(student)
        self._update_json()

    def remove_object(self, id):
        super(StudentRepoJSON, self).remove_object(id)
        self._update_json()

    def update_object(self, idx, object):
        super(StudentRepoJSON, self).update_object(idx, object)
        self._update_json()


class AssignmentRepoJSON(Repository):
    def __init__(self, jsonFile):
        super(AssignmentRepoJSON, self).__init__()

        self._jsonFile = jsonFile
        self._load_file()

    def _encode(self):
        return [{
                    "id": assignment.id,
                    "description": assignment.description,
                    "deadline": {
                                    "day": assignment.deadline.day.__str__(),
                                    "month": assignment.deadline.month.__str__(),
                                    "year": assignment.deadline.year.__str__()
                                }
                }
                for assignment in self._objects]

    @staticmethod
    def _decode(json):
        assignments = []
        for assignment in json:
            assignment = Assignment(
                                 assignment['id'],
                                 assignment['description'],
                                 assignment['deadline']['year'],
                                 assignment['deadline']['month'],
                                 assignment['deadline']['day']
                                 )
            assignments.append(assignment)
        return assignments

    def _load_file(self):
        try:
            with open(self._jsonFile, 'r') as f:
                myJson = json.load(f)
                self._objects = self._decode(myJson)
        except json.decoder.JSONDecodeError:
            pass

    def _update_json(self):
        serialized = self._encode()
        self._pretty_format(serialized)

    def _pretty_format(self, output):
        with open(self._jsonFile, 'w') as f:
            f.write(json.dumps(output, indent=4))

    def add_object(self, student):
        super(AssignmentRepoJSON, self).add_object(student)
        self._update_json()

    def remove_object(self, id):
        super(AssignmentRepoJSON, self).remove_object(id)
        self._update_json()

    def update_object(self, idx, object):
        super(AssignmentRepoJSON, self).update_object(idx, object)
        self._update_json()


class GradeRepoJSON(GradeRepository):
    def __init__(self, fileName):
        super(GradeRepoJSON, self).__init__()

        self._fileName = fileName
        self._load_file()

    def _load_file(self):
        with open(self._fileName, 'r')  as f:
            myJson = json.load(f)
            self._grades = self._decode(myJson)

    @staticmethod
    def _decode(json):
        return [Grade(grade['studentID'], grade['assignmentID'], grade['grade']) for grade in json]

    def _encode(self):
        return [{'studentID': grade.studentID, 'assignmentID': grade.assignmentID, 'grade': grade.grade} for grade in self._grades]

    def _update_json(self):
        serialized = self._encode()
        self._pretty_format(serialized)

    def _pretty_format(self, myJson):
        with open(self._fileName, 'w') as f:
            f.write(json.dumps(myJson, indent=4))

    def add(self, grade):
        super(GradeRepoJSON, self).add(grade)
        self._update_json()

    def delete(self, studentID, assignmentID):
        super(GradeRepoJSON, self).delete(studentID, assignmentID)
        self._update_json()

    def grade(self, sid, aid, new_grade):
        super(GradeRepoJSON, self).grade(sid, aid, new_grade)
        self._update_json()



