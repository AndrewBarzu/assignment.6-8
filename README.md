# assignment.6-8
This is a project for my university

It is an application that manages the students of a classroom, in which someone is able to create students, assignments,
assign them to a student and grade them afterwards. It also has a statistics tab, with 3 ways in which to display students.
Undo/Redo functionalities are done using inverse function calls, rather than keeping track of all previous states and eating memory.

The GUI of the app is created with QT, but it can also be ran from a terminal window. The settings are to be placed inside /new_files/settings.properties
and a list of all the settings is found in /new_files/other_settings

Tests are done using UnitTest and before submitting the assignment, test code coverage was over 95%, but then I changed some things as to
create a random list of people and assignments each time the app was started with the 'in memory' storing settings, 
and didn't update the tests, as the system was already working.

