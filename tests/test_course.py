import pytest
from typing import List
from app.course import Course

# --- fixtures
@pytest.fixture
def unpopulated_course():
    return Course('French')

# "Start Of Year" course
@pytest.fixture
def soy_course(unpopulated_course):
    unpopulated_course.create_assignment('Verbs')
    unpopulated_course.create_assignment('Adjectives')
    unpopulated_course.create_assignment('Nouns')
    unpopulated_course.enroll_student(123)
    unpopulated_course.enroll_student(124)
    unpopulated_course.enroll_student(125)
    unpopulated_course.enroll_student(1000)
    unpopulated_course.enroll_student(1001)
    unpopulated_course.enroll_student(1002)
    unpopulated_course.enroll_student(1003)
    unpopulated_course.enroll_student(1004)
    unpopulated_course.enroll_student(1005)
    return unpopulated_course

# "End Of Year" course
@pytest.fixture
def eoy_course(soy_course):
    # this person is hanging around 80
    soy_course.submit_assignment(123, 0, 78)
    soy_course.submit_assignment(123, 1, 89)
    soy_course.submit_assignment(123, 2, 68)

    # this person is doing really well
    soy_course.submit_assignment(124, 0, 100)
    soy_course.submit_assignment(124, 1, 99)
    soy_course.submit_assignment(124, 2, 100)

    # this person is having a very hard time
    soy_course.submit_assignment(125, 0, 67)
    soy_course.submit_assignment(125, 1, 23)

    # these are some other people for scale
    for i in range(0,6):
        for j in range(0,3):
            soy_course.submit_assignment(1000 + i, 0, 50 + i*5 + j)
    return soy_course

# --- tests

def test_course_init():
    course = Course('Linear Algebra')
    assert course.name == 'Linear Algebra'

def test_course_create_assignment(unpopulated_course):
    assert unpopulated_course.create_assignment('Verbs') == 0
    assert unpopulated_course.create_assignment('Adjectives') == 1
    assert unpopulated_course.create_assignment('Nouns') == 2
    assert unpopulated_course.assignments[1].name == 'Adjectives'

def test_course_enroll_student(unpopulated_course):
    assert unpopulated_course.enroll_student(123)
    assert not unpopulated_course.enroll_student(123)
    assert unpopulated_course.enroll_student(124)
    assert not unpopulated_course.enroll_student(123)
    assert not unpopulated_course.enroll_student(124)

def test_course_submit_assignment(soy_course):
    # Student and/or assignment and/or grade doesn't exist
    assert not soy_course.submit_assignment(100, 0, 65)
    assert not soy_course.submit_assignment(125, 100, 65)
    assert not soy_course.submit_assignment(125, 0, -100)
    assert not soy_course.submit_assignment(125, 0, 1000)
    assert not soy_course.submit_assignment(100, 100, 65)
    assert not soy_course.submit_assignment(100, 100, 1000)
    assert not soy_course.submit_assignment(100, 100, -100)

    # This one kept trying to submit over and over
    assert soy_course.submit_assignment(123, 0, 78)
    assert soy_course.submit_assignment(123, 0, 78)
    assert soy_course.submit_assignment(123, 0, 99)
    assert soy_course.assignments[0].student_grades[123] == 99

    # Other people should be able to submit to the same assignment, right?....
    assert soy_course.submit_assignment(125, 0, 78)
    assert soy_course.submit_assignment(124, 0, 100)

    # What about other assignments?...
    assert soy_course.submit_assignment(123, 1, 90)
    assert soy_course.assignments[0].student_grades[123] == 99
    assert soy_course.assignments[1].student_grades[123] == 90


def test_course_get_assignment_grade_avg(soy_course):

    # Everyone aced the first assignment.
    for student in soy_course.students:
        soy_course.submit_assignment(student, 0, 100)
    assert soy_course.get_assignment_grade_avg(0) == 100

    # 4 students of 9 submitted the next one.
    soy_course.submit_assignment(123, 1, 78)
    soy_course.submit_assignment(124, 1, 100)
    soy_course.submit_assignment(125, 1, 67)
    soy_course.submit_assignment(1005, 1, 100)
    assert soy_course.get_assignment_grade_avg(1) == 38

    # This is still ok, right?....
    assert soy_course.get_assignment_grade_avg(0) == 100

    # Everyone got something through on the last one though.
    sum = 0
    for student in soy_course.students:
        grade = (student + 50) % 101
        assert soy_course.submit_assignment(student, 2, grade)
        sum += grade
    assert soy_course.get_assignment_grade_avg(2) == int(sum/9)
    assert soy_course.get_assignment_grade_avg(1) == 38
    assert soy_course.get_assignment_grade_avg(0) == 100

    # An assignment that does not exist should throw an exception.
    try:
        soy_course.get_assignment_grade_avg(3)
        assert False
    except KeyError:
        assert True
    
    # What about an assignment with no submissions?
    culture_id = soy_course.create_assignment('Culture')
    assert soy_course.get_assignment_grade_avg(culture_id) is None

def test_get_student_grade_avg_unpopulated(unpopulated_course):
    # Get the average of a student that doesn't exist
    try:
        unpopulated_course.get_student_grade_avg(123)
        assert False
    except KeyError:
        assert True

def test_get_student_grade_avg_soy(soy_course):
    # Get the average of a student that exists with no assignments
    assert soy_course.get_student_grade_avg(123) is None

def test_get_student_grade_avg(eoy_course):
    assert eoy_course.get_student_grade_avg(123) == 78
    assert eoy_course.get_student_grade_avg(124) == 99
    assert eoy_course.get_student_grade_avg(125) == 30
    # Test it for a student that doesn't exist in populated course
    try:
        eoy_course.get_student_grade_avg(100)
        assert False
    except KeyError:
        assert True

def test_get_top_five_students_soy(soy_course):
    # Test when no assignments are submitted.
    top_five_students = soy_course.get_top_five_students()
    assert(len(top_five_students)) == 0

    # Test when one guy has assignments submitted.
    soy_course.submit_assignment(124, 0, 100)
    top_five_students = soy_course.get_top_five_students()
    assert(len(top_five_students)) == 1

def test_get_top_five_students_eoy(eoy_course):
    # Test for > 5 students and assignments submitted.
    top_five_students = eoy_course.get_top_five_students()
    assert len(top_five_students) == 5

    # Test for == 5 students
    for i in range(1002, 1006):
        eoy_course.dropout_student(i)
    top_five_students = eoy_course.get_top_five_students()
    assert len(top_five_students) == 5
    for student in eoy_course.students:
        assert student in top_five_students
    
    # Test for < 5 students
    eoy_course.dropout_student(1000)
    eoy_course.dropout_student(1001)
    top_five_students = eoy_course.get_top_five_students()
    assert len(top_five_students) == 3
    assert 123 in top_five_students
    assert 124 in top_five_students
    assert 125 in top_five_students

    # Test for 1 student
    eoy_course.dropout_student(124)
    eoy_course.dropout_student(125)
    top_five_students = eoy_course.get_top_five_students()
    assert len(top_five_students) == 1
    assert 123 in top_five_students

    # Test for 0 students
    eoy_course.dropout_student(123)
    top_five_students = eoy_course.get_top_five_students()
    assert len(top_five_students) == 0


def test_course_dropout_student(eoy_course):
    # Remove #125, they've failed out.
    student_count = len(eoy_course.students)
    assert eoy_course.dropout_student(125)
    assert len(eoy_course.students) == student_count - 1
    assert not eoy_course.dropout_student(125)
    try:
        eoy_course.get_student_grade_avg(125)
        assert False
    except KeyError:
        assert True

    # Oh no! It was too late....
    assert not eoy_course.submit_assignment(125, 2, 100)
    
    # Remove #124, they're making the others look bad.
    assert eoy_course.dropout_student(124)
    top_five_students = eoy_course.get_top_five_students()
    assert len(eoy_course.students) == student_count - 2
    assert 124 not in top_five_students
    assert 125 not in top_five_students

    # Just prune everybody
    for student in list(eoy_course.students):
        assert eoy_course.dropout_student(student)
    assert len(eoy_course.students) == 0