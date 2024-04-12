from app.assignment import Assignment
from typing import List
from statistics import fmean

class Course:
    def __init__(self, name):
        self.name = name
        # Student ids must be ints.
        self.students = []
        # list of Assignments. 
        self.assignments = {}
        self.assignment_id_iteration = 0
    
    def create_assignment(self, assignment_name) -> int:
        """
        Creates a new assignment.
        Returns the id of the new assignment.
        """
        id = self.assignment_id_iteration
        self.assignments[id] = Assignment(assignment_name)
        self.assignment_id_iteration = self.assignment_id_iteration + 1
        return id

    def enroll_student(self, student_id: int) -> bool:
        """
        Enrolls a student .
        Returns True if the student was enrolled successfully, otherwise False.
        """
        if student_id not in self.students:
            self.students.append(student_id)
        else:
            return False
        return True


    def dropout_student(self, student_id: int) -> bool:
        """
        Drops a student.
        Returns True if the student was dropped successfully, otherwise False.
        """
        if student_id in self.students:
            del self.students[self.students.index(student_id)]
            for assignment in self.assignments.values():
                assignment.dropout_student(student_id)
        else:
            return False
        return True


    def submit_assignment(self, student_id: int, assignment_id: int, grade: int) -> bool:
        """
        Submits an assignment for a student. A grade of an assignment will be an integer between 0 and 100 inclusive.
        Returns True if the assignment was submitted successfully, otherwise False.
        """
        if student_id in self.students and assignment_id in self.assignments:
            return self.assignments[assignment_id].submit_assignment(student_id, grade)
        return False

    def get_assignment_grade_avg(self, assignment_id: int) -> int:
        """
        Returns the average grade for an assignment. Floors the result to the nearest integer.
        """
        return self.assignments[assignment_id].get_assignment_grade_avg(self.students)

    def get_student_grade_avg(self, student_id) -> int:
        """
        Returns the average grade for a student in a course. Floors the result to the nearest integer.
        Returns None if the student has no assignments submitted.
        Throws a KeyError if the student is not enrolled in the course.
        """
        if student_id not in self.students:
            raise KeyError()
        grades = [assignment.student_grades.get(student_id) for assignment in self.assignments.values()]
        return None if grades.count(None) == len(grades) else int(fmean([grade or 0 for grade in grades]))

    def get_top_five_students(self) -> List[int]:
        """
        Returns the IDs of the top 5 students based on their average grades of all assignments.
        """
        grade_averages = {s: self.get_student_grade_avg(s) for s in self.students if self.get_student_grade_avg(s) is not None}.items()
        return list([x[0] for x in sorted(grade_averages, key=lambda y: y[1], reverse=True)])[0:5]



    
