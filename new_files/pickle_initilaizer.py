# THIS FILE IS MEANT FOR ONE TIME USE ONLY, OR AFTER DELETING THE CONTENTS OF ALL .pickle FILES

from new_files.domain import Assignment, Student, Grade
import pickle

assignments = [Assignment('1', 'Paricel', '1999', '10', '15'), Assignment('2', 'Marcel', '2010', '12', '19'),
               Assignment('3', 'Georgel', '2019', '11', '29'), Assignment('4', 'George', '2020', '1', '10'),
               Assignment('5', 'Gigel', '2019', '12', '18'), Assignment('6', 'Gicu', '2019', '12', '7'),
               Assignment('7', 'Mercedesa', '2021', '9', '20'), Assignment('8', 'Maria', '2020', '8', '27'),
               Assignment('9', 'Marian', '2015', '1', '24'), Assignment('10', 'Dani', '1999', '10', '24')]


students = [Student('1', 'Paricel', '3'), Student('2', 'Marcel', '1'), Student('3', 'Georgel', '2'),
            Student('4', 'George', '1'), Student('5', 'Gigel', '4'), Student('6', 'Gicu', '7'),
            Student('7', 'Mercedesa', '2'), Student('8', 'Maria', '7'), Student('9', 'Marian', '3'),
            Student('10', 'Marcela', '3')]

grades = [Grade('1', '1', '10'), Grade('1', '9',  None), Grade('1', '10', None), Grade('2', '1', None), Grade('3', '1', '7'),
          Grade('2', '7', '10'), Grade('2', '8', '7'), Grade('2', '6', '9'), Grade('7', '1', None), Grade('7', '7', '4'), Grade('8', '7', '3')]

with open("assignments.pickle", 'wb') as f:
    for assignment in assignments:
        pickle.dump(assignment, f)

with open("students.pickle", 'wb') as f:
    for student in students:
        pickle.dump(student, f)

with open("grades.pickle", 'wb') as f:
    for grade in grades:
        pickle.dump(grade, f)

