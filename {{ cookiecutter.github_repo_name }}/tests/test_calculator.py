import numpy as np
import pytest
from {{cookiecutter.package_dir_name}} import calculator as calc


def test_dot_product_2D_list():
    a = [1, 2]
    b = [3, 4]
    expected = 11.0
    actual = calc.dot_product(a, b)
    assert actual == expected


def test_dot_product_3D_list():
    a = [1, 2, 3]
    b = [4, 5, 6]
    expected = 32.0
    actual = calc.dot_product(a, b)
    assert actual == expected

def test_dot_product_2D_tuple():
    a = (1, 2)
    b = (3, 4)
    expected = 11.0
    actual = calc.dot_product(a, b)
    assert actual == expected


def test_dot_product_3D_tuple():
    a = (1, 2, 3)
    b = (4, 5, 6)
    expected = 32.0
    actual = calc.dot_product(a, b)
    assert actual == expected


def test_dot_product_2D_np_array():
    a = np.array([1, 2])
    b = np.array([3, 4])
    expected = 11.0
    actual = calc.dot_product(a, b)
    assert actual == expected


def test_dot_product_3D_np_array():
    a = np.array([1, 2, 3])
    b = np.array([4, 5, 6])
    expected = 32.0
    actual = calc.dot_product(a, b)
    assert actual == expected

@pytest.mark.parametrize(
    "a, b, expected",
    [
        # Test whether the dot product function works with 2D and 3D vectors
        # C1: lists given, expect no error
        ([1, 2], [3, 4], 11.0),
        ([1, 2, 3], [4, 5, 6], 32.0),
        # C2: tuples given, expect no error
        ((1, 2), (3, 4), 11.0),
        ((1, 2, 3), (4, 5, 6), 32.0),
        # C3: numpy arrays, expect no error
        (np.array([1, 2]), np.array([3, 4]), 11.0),
        (np.array([1, 2, 3]), np.array([4, 5, 6]), 32.0),
    ]

)
def test_dot_product(a, b, expected):
    actual = calc.dot_product(a, b)
    assert actual == expected
