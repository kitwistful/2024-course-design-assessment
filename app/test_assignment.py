import pytest
from assignment import Assignment

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
    # These ones should be acceptable
    result = unpopulated_assignment.submit_assignment(123, 98)
    assert result == True
    result = unpopulated_assignment.submit_assignment(124, 100)
    assert result == True
    result = unpopulated_assignment.submit_assignment(125, 0)
    assert result == True
    result = unpopulated_assignment.submit_assignment(126, 50)
    assert result == True

    # These ones shouldn't be acceptable
    result = unpopulated_assignment.submit_assignment(125, -1)
    assert result == False
    result = unpopulated_assignment.submit_assignment(126, 101)
    assert result == False

def test_assignment_assignment_grade_avg_no_students(unpopulated_assignment):
    assert unpopulated_assignment.get_assignment_grade_avg() is None

def test_assignment_assignment_grade_avg(populated_assignment):
    populated_assignment.submit_assignment(125, 98)
    assert populated_assignment.get_assignment_grade_avg() == 98
    populated_assignment.submit_assignment(125, 0)
    assert populated_assignment.get_assignment_grade_avg() == 65

def test_assignment_student_dropout(populated_assignment):
    assert populated_assignment.get_assignment_grade_avg() == 65
    populated_assignment.dropout_student(125)
    assert populated_assignment.get_assignment_grade_avg() == 98

def test_assignment_student_dropout_2(populated_assignment):
    result = populated_assignment.dropout_student(125)
    assert result == True
    result = populated_assignment.dropout_student(125)
    assert result == False
    result = populated_assignment.dropout_student(126)
    assert result == False
