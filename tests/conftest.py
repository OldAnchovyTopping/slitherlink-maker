from slitherlinking.slitherlink_internal_state import Slitherlink
import pytest


@pytest.fixture(scope="session")
def number_test_grid():
    lines = [(1, 2), (1, 8), (1, 10), (1, 12), (2, 5), (2, 7), (2, 13),
             (3, 10), (4, 1), (4, 7), (4, 13), (5, 4), (5, 8), (5, 10),
             (5, 12), (7, 4), (8, 3), (8, 5), (9, 2), (9, 6), (9, 10),
             (10, 1), (10, 7), (10, 9), (10, 11), (11, 2), (11, 6),
             (11, 10), (12, 3), (12, 5), (13, 4)]
    testing_grid = Slitherlink(6, 6)
    for x, y in lines:
        testing_grid.change_line_segment(x, y, "L")
    return testing_grid


@pytest.fixture(scope="session")
def char_grid():
    return Slitherlink(5, 6)
