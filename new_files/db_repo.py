from new_files.better_repo import Repository, GradeRepository
from new_files.domain import Grade, Assignment, Student
import pymongo

class StudentMongoRepo(Repository):
    def __init__(self, client: pymongo.MongoClient):
        super(StudentMongoRepo, self).__init__()
        myDB = client["mydatabase"]
        self._myStudentCollection = myDB["students"]
        self._load_db()

    def _load_db(self):
        cursor = self._myStudentCollection.find({})
        for student in cursor:
            self._objects.append(self._deserialize(student))

    @staticmethod
    def _serialize(student):
        return {"id": student.id, "name": student.name, "group": student.group}

    @staticmethod
    def _deserialize(databaseDocument):
        return Student(databaseDocument["id"], databaseDocument["name"], databaseDocument["group"])

    def add_object(self, student: Student):
        super(StudentMongoRepo, self).add_object(student)
        self._myStudentCollection.insert_one(self._serialize(student))

    def remove_object(self, id):
        super(StudentMongoRepo, self).remove_object(id)
        self._myStudentCollection.delete_one({'id': id})

    def update_object(self, idx, object):
        old_object = self[idx]
        super(StudentMongoRepo, self).update_object(idx, object)
        self._myStudentCollection.replace_one(self._serialize(old_object), self._serialize(object))


class AssignmentMongoRepo(Repository):
    def __init__(self, client: pymongo.MongoClient):
        super(AssignmentMongoRepo, self).__init__()
        myDB = client["mydatabase"]
        self._myAssignmentCollection = myDB["assignments"]
        self._load_db()

    @staticmethod
    def _serialize(assignment: Assignment):
        return {"id": assignment.id, "description": assignment.description,
                "deadline": {"day": str(assignment.deadline.day), "month": str(assignment.deadline.month), "year": str(assignment.deadline.year)}}

    @staticmethod
    def _deserialize(databaseDocument):
        return Assignment(databaseDocument['id'], databaseDocument['description'], databaseDocument['deadline']['year'],
                          databaseDocument['deadline']['month'], databaseDocument['deadline']['day'])

    def _load_db(self):
        cursor = self._myAssignmentCollection.find({})
        for assignment in cursor:
            self._objects.append(self._deserialize(assignment))

    def add_object(self, object):
        super(AssignmentMongoRepo, self).add_object(object)
        self._myAssignmentCollection.insert_one(self._serialize(object))

    def remove_object(self, id):
        super(AssignmentMongoRepo, self).remove_object(id)
        self._myAssignmentCollection.delete_one({'id': id})

    def update_object(self, idx, object):
        old_object = self[idx]
        super(AssignmentMongoRepo, self).update_object(idx, object)
        self._myAssignmentCollection.replace_one(self._serialize(old_object), self._serialize(object))


class GradeMongoRepo(GradeRepository):
    def __init__(self, client: pymongo.MongoClient):
        super(GradeMongoRepo, self).__init__()
        myDB = client["mydatabase"]
        self._myGradeCollection = myDB["grades"]
        self._load_db()

    @staticmethod
    def _serialize(grade: Grade):
        return {"studentID": grade.studentID, "assignmentID": grade.assignmentID, "grade": grade.grade}

    @staticmethod
    def _deserialize(databaseDocument):
        return Grade(databaseDocument["studentID"], databaseDocument["assignmentID"], databaseDocument["grade"])

    def _load_db(self):
        cursor = self._myGradeCollection.find({})
        for grade in cursor:
            self._grades.append(self._deserialize(grade))

    def add(self, grade):
        super(GradeMongoRepo, self).add(grade)
        self._myGradeCollection.insert_one(self._serialize(grade))

    def delete(self, studentID, assignmentID):
        super(GradeMongoRepo, self).delete(studentID, assignmentID)
        self._myGradeCollection.delete_one({"studentID": studentID, "assignmentID": assignmentID})

    def grade(self, sid, aid, new_grade):
        super(GradeMongoRepo, self).grade(sid, aid, new_grade)
        self._myGradeCollection.update_one({"studentID": sid, "assignmentID": aid},
                                           {"$set": {"grade": (int(new_grade) if new_grade is not None else None)}})

    def extend(self, more):
        super(GradeMongoRepo, self).extend(more)
        self._myGradeCollection.insert_many([self._serialize(grade) for grade in self._grades])
