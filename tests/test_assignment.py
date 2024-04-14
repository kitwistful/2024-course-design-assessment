import pytest
from app.assignment import Assignment

@pytest.fixture
def unpopulated_assignment():
    return Assignment('Verbs')

@pytest.fixture
def populated_assignment():
    assignment = Assignment('Vowels')
    assignment.submit_assignment(123, 98)
    assignment.submit_assignment(124, 98)
    assignment.submit_assignment(125, 0)
    return assignment

def test_assignment_init():
    assignment = Assignment('Nouns')
    assert assignment.name == 'Nouns'

def test_assignment_submit_assignment(unpopulated_assignment):
    # Check only [0, 100] is accepted
    assert unpopulated_assignment.submit_assignment(123, 98)
    assert unpopulated_assignment.submit_assignment(124, 100)
    assert unpopulated_assignment.submit_assignment(125, 0)
    assert unpopulated_assignment.submit_assignment(126, 50)
    assert not unpopulated_assignment.submit_assignment(127, -1)
    assert not unpopulated_assignment.submit_assignment(128, 101)

    # Check assignment is overwritten
    assert unpopulated_assignment.submit_assignment(125, 27)
    assert unpopulated_assignment.student_grades[125] == 27

def test_assignment_assignment_grade_avg_no_students(unpopulated_assignment):
    assert unpopulated_assignment.get_assignment_grade_avg() is None

def test_assignment_assignment_grade_avg_missing_assignments(populated_assignment):
    # Uses the 'students' param to test subsets and supersets of submitted assignments.
    populated_assignment.get_assignment_grade_avg([123, 124]) == 98
    populated_assignment.get_assignment_grade_avg([125]) == 0
    populated_assignment.get_assignment_grade_avg([124, 125]) == 49
    populated_assignment.get_assignment_grade_avg([123, 124, 125, 100, 101]) == 39

def test_assignment_assignment_grade_avg(populated_assignment):
    populated_assignment.submit_assignment(125, 98)
    assert populated_assignment.get_assignment_grade_avg() == 98
    populated_assignment.submit_assignment(125, 0)
    assert populated_assignment.get_assignment_grade_avg() == 65

def test_assignment_student_dropout_affects_grade_average(populated_assignment):
    assert populated_assignment.get_assignment_grade_avg() == 65
    populated_assignment.dropout_student(125)
    assert populated_assignment.get_assignment_grade_avg() == 98

def test_assignment_student_dropout_fail_cases(populated_assignment):
    assert populated_assignment.dropout_student(125)
    assert not populated_assignment.dropout_student(125)
    assert not populated_assignment.dropout_student(126)
