import pytest
# TODO: test it with CourseService interface
from app.course_service_impl import CourseServiceImpl

# --- fixtures
@pytest.fixture
def unpopulated_course_service():
    return CourseServiceImpl()
    
@pytest.fixture
def fresh_course_service(unpopulated_course_service):
    unpopulated_course_service.create_course('French')
    unpopulated_course_service.create_course('English')
    unpopulated_course_service.create_course('Sociology')
    return unpopulated_course_service

# "Start Of Year"
@pytest.fixture
def soy_course_service(fresh_course_service):
    # Assignments
    fresh_course_service.create_assignment
    fresh_course_service.create_assignment(0, 'Aller')
    fresh_course_service.create_assignment(0, 'Les Animaux')
    fresh_course_service.create_assignment(0, 'Vocabulary I')
    fresh_course_service.create_assignment(1, 'Verbs')
    fresh_course_service.create_assignment(1, 'Conjugation')
    fresh_course_service.create_assignment(1, 'Tenses')
    fresh_course_service.create_assignment(1, 'Romeo and Juliet')
    fresh_course_service.create_assignment(1, 'Hamlet')
    fresh_course_service.create_assignment(2, 'Social Justice')
    fresh_course_service.create_assignment(2, 'Case Study I')

    # Students
    assert fresh_course_service.enroll_student(0, 123)
    assert fresh_course_service.enroll_student(0, 124)
    assert fresh_course_service.enroll_student(0, 125)
    assert fresh_course_service.enroll_student(0, 1000)
    assert fresh_course_service.enroll_student(0, 1001)
    assert fresh_course_service.enroll_student(0, 1003)
    assert fresh_course_service.enroll_student(0, 1005)
    assert fresh_course_service.enroll_student(1, 123)
    assert fresh_course_service.enroll_student(1, 124)
    assert fresh_course_service.enroll_student(1, 1000)
    assert fresh_course_service.enroll_student(1, 1003)
    assert fresh_course_service.enroll_student(1, 1004)
    assert fresh_course_service.enroll_student(2, 123)
    assert fresh_course_service.enroll_student(2, 125)
    assert fresh_course_service.enroll_student(2, 1000)
    assert fresh_course_service.enroll_student(2, 1001)
    assert fresh_course_service.enroll_student(2, 1002)

    return fresh_course_service

# "End Of Year"
@pytest.fixture
def eoy_course_service(soy_course_service):
    for course_id, course in soy_course_service.courses.items():
        for student_id in course.students:
            for assignment_id in course.assignments:
                soy_course_service.submit_assignment(course_id, student_id, assignment_id, (50 + student_id + int((course_id+0.5)*assignment_id)) % 101)
    return soy_course_service

# --- tests

def test_course_service_impl_create_course(unpopulated_course_service):
    r1 = unpopulated_course_service.create_course('French')
    r2 = unpopulated_course_service.create_course('English')
    r3 = unpopulated_course_service.create_course('Sociology')
    assert r1 == 0
    assert r2 == 1
    assert r3 == 2

def test_course_service_impl_get_courses(unpopulated_course_service):
    # Should return empty list (it's unpopulated)
    empty_courses = unpopulated_course_service.get_courses()
    assert len(empty_courses) == 0

    # Add courses
    unpopulated_course_service.create_course('French')
    unpopulated_course_service.create_course('English')
    unpopulated_course_service.create_course('Sociology')

    # Confirm that we didn't just get the internal courses reference
    assert len(empty_courses) == 0

    # Confirm that we can get the three we just added
    assert len(unpopulated_course_service.get_courses()) == 3
    populated_courses = [course.name for course in unpopulated_course_service.get_courses()]
    assert 'French' in populated_courses
    assert 'English' in populated_courses
    assert 'Sociology' in populated_courses


def test_course_service_impl_delete_course(fresh_course_service):
    # Let's delete everything, even things that aren't in there.
    courses = fresh_course_service.get_courses()
    assert not fresh_course_service.delete_course(3)
    assert fresh_course_service.delete_course(2)
    assert fresh_course_service.delete_course(0)
    assert fresh_course_service.delete_course(1)

    # Check it's empty now
    assert not fresh_course_service.delete_course(2)
    assert not fresh_course_service.delete_course(0)
    assert not fresh_course_service.delete_course(1)
    assert len(fresh_course_service.get_courses()) == 0

    # Check previous references are valid
    assert 'French' in [course.name for course in courses]

    # Add and remove an item
    assert fresh_course_service.create_course('Biology') == 3
    assert fresh_course_service.delete_course(3)
    assert not fresh_course_service.delete_course(3)
    assert len(fresh_course_service.get_courses()) == 0

def test_course_service_impl_get_course_by_id(fresh_course_service):
    assert fresh_course_service.get_course_by_id(0).name == 'French'
    assert fresh_course_service.get_course_by_id(1).name == 'English'
    assert fresh_course_service.get_course_by_id(2).name == 'Sociology'

def test_course_service_create_assignment(fresh_course_service):
    assert fresh_course_service.create_assignment(0, 'Aller') == 0
    assert fresh_course_service.create_assignment(0, 'Les Animaux') == 1
    assert fresh_course_service.create_assignment(0, 'Vocabulary I') == 2
    assert fresh_course_service.create_assignment(2, 'Social Justice') == 0
    
    # Check assignment is correct
    french_assignments = [c.name for c in fresh_course_service.courses[0].assignments.values()]
    english_assignments = [c.name for c in fresh_course_service.courses[1].assignments.values()]
    sociology_assignments = [c.name for c in fresh_course_service.courses[2].assignments.values()]
    assert len(french_assignments) == 3
    assert len(english_assignments) == 0
    assert len(sociology_assignments) == 1
    assert 'Aller' in french_assignments
    assert 'Les Animaux' in french_assignments
    assert 'Vocabulary I' in french_assignments
    assert 'Social Justice' in sociology_assignments

def test_course_service_enroll_student(fresh_course_service):
    # This person really wants to take french
    assert fresh_course_service.enroll_student(0, 123)
    assert not fresh_course_service.enroll_student(0, 123)
    assert not fresh_course_service.enroll_student(0, 123)

    # Continue populating
    assert fresh_course_service.enroll_student(0, 124)
    assert fresh_course_service.enroll_student(0, 125)
    assert fresh_course_service.enroll_student(1, 123)
    assert fresh_course_service.enroll_student(1, 124)
    assert fresh_course_service.enroll_student(1, 1000)
    assert fresh_course_service.enroll_student(1, 1003)
    assert fresh_course_service.enroll_student(2, 125)
    assert fresh_course_service.enroll_student(2, 1000)

    # Check how many students are now in each course
    student_count_per_course = [len(c.students) for c in fresh_course_service.courses.values()]
    assert student_count_per_course[0] == 3
    assert student_count_per_course[1] == 4
    assert student_count_per_course[2] == 2

def test_course_service_submit_assignment(soy_course_service):
    assert soy_course_service.submit_assignment(0, 123, 0, 78)
    assert soy_course_service.submit_assignment(0, 123, 0, 100)
    assert soy_course_service.submit_assignment(0, 123, 1, 90)
    assert soy_course_service.submit_assignment(0, 123, 2, 67)
    assert not soy_course_service.submit_assignment(0, 123, 3, 100)
    assert soy_course_service.submit_assignment(1, 123, 0, 88)

    assert soy_course_service.courses[0].assignments[0].student_grades[123] == 100
    assert soy_course_service.courses[0].assignments[0].student_grades[123] == 100
    assert soy_course_service.courses[0].assignments[1].student_grades[123] == 90
    assert soy_course_service.courses[0].assignments[2].student_grades[123] == 67
    assert soy_course_service.courses[1].assignments[0].student_grades[123] == 88
    assert soy_course_service.courses[2].get_student_grade_avg(123) is None

def test_course_service_get_assignment_grade_avg(eoy_course_service):
    assert eoy_course_service.get_assignment_grade_avg(0, 0) == 55
    assert eoy_course_service.get_assignment_grade_avg(1, 0) == 54
    assert eoy_course_service.get_assignment_grade_avg(1, 4) == 60
    assert eoy_course_service.get_assignment_grade_avg(2, 0) == 53

def test_course_service_get_student_grade_avg(eoy_course_service):
    assert eoy_course_service.get_student_grade_avg(0, 125) == 74
    assert eoy_course_service.get_student_grade_avg(2, 125) == 75
    assert eoy_course_service.get_student_grade_avg(2, 123) == 73
    assert eoy_course_service.get_student_grade_avg(0, 1000) == 40
    assert eoy_course_service.get_student_grade_avg(0, 1003) == 43
    assert eoy_course_service.get_student_grade_avg(2, 1001) == 42

def test_course_service_get_top_five_students(eoy_course_service):
    assert set(eoy_course_service.get_top_five_students(0)) == {125, 124, 123, 1005, 1003}

def test_course_service_dropout_student(eoy_course_service):
    assert eoy_course_service.dropout_student(0, 125)
    assert not eoy_course_service.dropout_student(0, 125)
    assert 125 not in eoy_course_service.courses[0].students
    assert 125 not in eoy_course_service.courses[1].students
    assert 125 in eoy_course_service.courses[2].students