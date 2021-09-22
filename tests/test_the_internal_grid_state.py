from slitherlinking.slitherlink_internal_state import *
import pytest


@pytest.mark.parametrize("x_size, y_size", [(0, 0), (1, 13), (3, 4), (20, 50)])
def test_cleared_grid_against_a_fresh_one(x_size: int, y_size: int):
    random_then_clear = Slitherlink(x_size, y_size)
    random_then_clear.populate_grid_randomly()
    random_then_clear.clear_the_numbers()
    assert Slitherlink(x_size, y_size) == random_then_clear


@pytest.mark.parametrize("lines, bad_corner", [
    ([(1, 2), (1, 4), (2, 3)], (0, 1)),
    ([(3, 6), (3, 8), (2, 7)], (1, 3)),
    ([(5, 2), (4, 1), (6, 1)], (2, 0)),
    ([(9, 10), (8, 11), (10, 11)], (4, 5)),
    ([(6, 9), (7, 8), (7, 10), (8, 9)], (3, 4))
])
def test_line_crossing_at_corner(lines: list[tuple], bad_corner: tuple[int]):
    with pytest.raises(PathCrossingException):
        new_grid = Slitherlink(5, 6)
        for x_coordinate, y_coordinate in lines:
            new_grid.change_line_segment(x_coordinate, y_coordinate, False)
        new_grid.check_a_corner(*bad_corner)
