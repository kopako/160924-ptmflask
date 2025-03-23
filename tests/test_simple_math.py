import pytest
from autoqa.simple_math import SimpleMath

@pytest.fixture
def simplemath():
    return SimpleMath()


@pytest.mark.parametrize("test_input,expected", [
    (2, 4),
    (0, 0),
    (1, 1),
    (-2, 4),
])
def test_square_po_muns(test_input, expected, simplemath):
    assert simplemath.square(test_input) == expected


@pytest.mark.parametrize("test_input,expected", [
    (2, 8),
    (0, 0),
    (1, 1),
    (-3, -27),
])
def test_cube_po_muns(test_input, expected, simplemath):
    assert simplemath.cube(test_input) == expected
