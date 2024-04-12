from app.course_service import CourseService
from app.course import Course
from typing import List, Any, Dict

# TODO: fix this
# class CourseServiceImpl(CourseService):
class CourseServiceImpl:
    """
    Please implement the CourseService interface according to the requirements.
    """
    def __init__(self):
        self.courses: Dict[int, Course] = {}
        self.course_id_iteration = -1

    def get_courses(self) -> List[Any]:
        """
        Returns a list of all courses.
        """
        return list(self.courses.values())

    def get_course_by_id(self, course_id) -> Any:
        """
        Returns a course by its id. Throws a KeyError if the course does not exist.
        """
        return self.courses[course_id]

    def create_course(self, course_name) -> int:
        """
        Creates a new course.
        Returns the id of the new course.
        """
        self.course_id_iteration = self.course_id_iteration + 1
        self.courses[self.course_id_iteration] = Course(course_name)
        return self.course_id_iteration

    def delete_course(self, course_id) -> bool:
        """
        Deletes a course by its id.
        Returns True if the course was deleted successfully, otherwise False.
        """
        try:
            del self.courses[course_id]
        except KeyError:
            return False
        return True

    def create_assignment(self, course_id, assignment_name) -> int:
        """
        Creates a new assignment for a course.
        Returns the id of the new assignment.
        Throws a KeyError if the course does not exist.
        """
        return self.courses[course_id].create_assignment(assignment_name)

    def enroll_student(self, course_id, student_id) -> bool:
        """
        Enrolls a student in a course.
        Returns True if the student was enrolled successfully, otherwise False.
        Throws a KeyError if the course does not exist.
        """
        return self.courses[course_id].enroll_student(student_id)

    def dropout_student(self, course_id, student_id) -> bool:
        """
        Drops a student from a course.
        Returns True if the student was dropped successfully, otherwise False.
        """
        return self.courses[course_id].dropout_student(student_id)

    def submit_assignment(self, course_id, student_id, assignment_id, grade: int) -> bool:
        """
        Submits an assignment for a student. A grade of an assignment will be an integer between 0 and 100 inclusive.
        Returns True if the assignment was submitted successfully, otherwise False.
        """
        return self.courses[course_id].submit_assignment(student_id, assignment_id, grade)

    def get_assignment_grade_avg(self, course_id, assignment_id) -> int:
        """
        Returns the average grade for an assignment. Floors the result to the nearest integer.
        """
        print(self.courses[course_id].assignments[assignment_id].student_grades)
        return self.courses[course_id].get_assignment_grade_avg(assignment_id)

    def get_student_grade_avg(self, course_id, student_id) -> int:
        """
        Returns the average grade for a student in a course. Floors the result to the nearest integer.
        """
        return self.courses[course_id].get_student_grade_avg(student_id)

    def get_top_five_students(self, course_id) -> List[int]:
        """
        Returns the IDs of the top 5 students in a course based on their average grades of all assignments.
        """
        return self.courses[course_id].get_top_five_students()
