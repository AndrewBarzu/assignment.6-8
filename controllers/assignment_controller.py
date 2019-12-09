from new_files.better_repo import Repository
from copy import deepcopy
from new_files.domain import Assignment
from new_files.exceptions import *
import new_files.validation_service as ValidationServices

class AssignmentController:
    def __init__(self, assignmentRepo: Repository):
        self._assignmentRepo = assignmentRepo


    def add_assignment(self, assignment: Assignment):
        ValidationServices.validate_id(assignment.id)
        ValidationServices.is_unique(self.get_assignments(), assignment)
        self._assignmentRepo.add_object(assignment)

    def remove_assignment(self, aid):
        ValidationServices.validate_id(aid)
        self._assignmentRepo.remove_object(aid)

    def update_assignment(self, assignmentID, newAssignment: Assignment):
        ValidationServices.validate_id(assignmentID)
        idx = self._assignmentRepo.find_object(assignmentID)
        if idx is None:
            raise NotExistent("Student does not exist")
        if newAssignment.id.isnumeric() or newAssignment.id == '':
            for assignment in self._assignmentRepo:
                if assignment.id == newAssignment.id and assignment.id != assignmentID:
                    raise NotUnique("ID should be unique!")
        else:
            raise NotAnInt("ID should be an int!")
        self._assignmentRepo.update_object(idx, newAssignment)


    def get_assignments(self):
        return deepcopy(self._assignmentRepo.get_objects())

    def show_assignments(self):
        return [str(assignment) for assignment in self.get_assignments()]

    def find_assignment(self, assignmentID):
        return self._assignmentRepo.find_object(assignmentID)

    def get_assignment_object(self, assignmentID):
        return deepcopy(self._assignmentRepo[self.find_assignment(assignmentID)])