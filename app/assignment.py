from statistics import fmean

class Assignment:
    def __init__(self, name):
        # This is different from the assignment id used by course/course service
        self.name = name
        # Key = student id, Value = their grade (an int)
        self.student_grades = {}

    def submit_assignment(self, student_id, grade: int):
        """
        Submits an assignment for a student. A grade of an assignment will be an integer between 0 and 100 inclusive.
        Returns True if the assignment was submitted successfully, otherwise False.
        """
        if grade >= 0 and grade <= 100:
            self.student_grades[student_id] = grade
        else:
            return False
        return True

    def dropout_student(self, student_id):
        """
        Drops a student from a course.
        Returns True if the student was dropped successfully, otherwise False.
        """
        try:
            del self.student_grades[student_id]
        except KeyError:
            return False
        return True

    def get_assignment_grade_avg(self)  -> int:
        """
        Returns the average grade for a student in a course. Floors the result to the nearest integer.
        If no assignments are submitted, returns None.
        """
        return None if len(self.student_grades) == 0 else int(fmean(self.student_grades.values()))

