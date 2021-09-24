from slitherlinking.slitherlink_internal_state import Slitherlink,\
    PathCrossingException, CellValueOverload, BadCellValueError,\
    BadLineCharException, NotALineTile
import pytest
from itertools import product
from typing import List, Tuple


@pytest.mark.parametrize("x_size, y_size", [(0, 0), (1, 13), (3, 4), (20, 50)])
def test_cleared_grid_against_a_fresh_one(x_size: int, y_size: int):
    random_then_clear = Slitherlink(x_size, y_size)
    random_then_clear.populate_grid_randomly()
    random_then_clear.clear_the_numbers()
    assert Slitherlink(x_size, y_size) == random_then_clear
    assert random_then_clear == eval(repr(random_then_clear))
    assert str(random_then_clear) == str(Slitherlink(x_size, y_size))


@pytest.mark.parametrize("lines, bad_corner", [
    ([(1, 2), (1, 4), (2, 3)], (0, 1)),
    ([(3, 6), (3, 8), (2, 7)], (1, 3)),
    ([(5, 2), (4, 1), (6, 1)], (2, 0)),
    ([(9, 10), (8, 11), (10, 11)], (4, 5)),
    ([(6, 9), (7, 8), (7, 10), (8, 9)], (3, 4))
])
def test_line_crossing_at_corner(lines: List[Tuple[int, int]],
                                 bad_corner: Tuple[int, int]):
    """Checks that a 3-way and 4-way corners raise PathCrossingException."""
    with pytest.raises(PathCrossingException):
        new_grid = Slitherlink(5, 6)
        for x_coordinate, y_coordinate in lines:
            new_grid.change_line_segment(x_coordinate, y_coordinate, "L")
        new_grid.check_a_corner(*bad_corner)


@pytest.mark.parametrize("lines", [
    ([]),
    ([(1, 2), (1, 4), (1, 6), (2, 7), (3, 6), (3, 4), (3, 2), (2, 1)]),
    ([(1, 2), (1, 6), (2, 7), (3, 4), (3, 2)]),
    ([(1, 4), (2, 7), (11, 2), (13, 12)])
])
def test_for_no_crossing_of_lines(lines: List[Tuple[int, int]]):
    """Checks that a grid with corners with <= 2 lines DON'T raise
    PathCrossingException. Test #2 includes a closed path."""
    new_grid = Slitherlink(6, 6)
    for x_coordinate, y_coordinate in lines:
        new_grid.change_line_segment(x_coordinate, y_coordinate, "L")
    new_grid.check_all_corners()  # No exception here.


@pytest.mark.parametrize("cell_x, cell_y, number", [
    (1, 1, 0),
    (1, 2, 0),
    (2, 1, 0),
    (2, 2, 0),
    (1, 4, 0),
    (1, 5, 0),
    (1, 6, 0),
    (2, 4, 0),
    (2, 5, 0),
    (2, 6, 0),
    (4, 2, 0),
    (5, 1, 0),
    (5, 3, 0),
    (6, 2, 0),
    (5, 5, 0),
    (1, 4, 1),
    (1, 5, 1),
    (1, 6, 1),
    (2, 4, 1),
    (2, 5, 1),
    (2, 6, 1),
    (4, 2, 1),
    (5, 1, 1),
    (5, 3, 1),
    (6, 2, 1),
    (5, 5, 1),
    (4, 2, 2),
    (5, 1, 2),
    (5, 3, 2),
    (6, 2, 2),
    (5, 5, 2),
    (5, 5, 3)
])
def test_cell_number_overloads(number_test_grid: Slitherlink,
                               cell_x: int, cell_y: int, number: int):
    """Checks that all number overloading cases raise CellValueOverload."""
    with pytest.raises(CellValueOverload):
        number_test_grid.change_number(cell_x, cell_y, number)
        number_test_grid.check_a_number(cell_x, cell_y)


@pytest.mark.parametrize("number, cells", [
    (4, [(x, y) for x, y in product((1, 2, 3, 4, 5, 6), repeat=2)]),
    (0, [(5, 2)]),
    (1, [(5, 2), (1, 1), (1, 2), (2, 1), (2, 2)]),
    (2, [(5, 2), (1, 1), (1, 2), (2, 1), (2, 2),
         (1, 4), (1, 5), (1, 6), (2, 4), (2, 5), (2, 6)]),
    (3, [(5, 2), (1, 1), (1, 2), (2, 1), (2, 2),
         (1, 4), (1, 5), (1, 6), (2, 4), (2, 5), (2, 6),
         (4, 2), (5, 1), (5, 3), (6, 2)])
])
def test_cell_number_works(number_test_grid: Slitherlink,
                           cells: List[Tuple[int, int]], number: int):
    """Checks all viable number-line configurations that work."""
    for cell_x, cell_y in cells:
        number_test_grid.change_number(cell_x, cell_y, number)
    number_test_grid.check_all_numbers()  # No exception here.


@pytest.mark.parametrize("tested_number", [-20, -3, -1, 5, 6, 8, 13, 142, 211])
def test_bad_cell_number_values(char_grid: Slitherlink, tested_number: int):
    with pytest.raises(BadCellValueError):
        char_grid.change_number(1, 2, tested_number)


@pytest.mark.parametrize("tested_number", [0, 1, 2, 3, 4])
def test_correct_cell_numbers(char_grid: Slitherlink, tested_number: int):
    char_grid.change_number(1, 2, tested_number)  # No exception here.


@pytest.mark.parametrize("tested_char", ["0", "1", "2", "3", "4", "e", "l",
                                         "x", "A", "B", "D", "K", "Y", "!"])
def test_bad_line_char_values(char_grid: Slitherlink, tested_char: str):
    with pytest.raises(BadLineCharException):
        char_grid.change_line_segment(1, 2, tested_char)


@pytest.mark.parametrize("tested_char", ["E", "L", "X"])
def test_correct_line_char_values(char_grid: Slitherlink, tested_char: str):
    char_grid.change_line_segment(1, 2, tested_char)  # No exception here.


@pytest.mark.parametrize("test_x, test_y", [
    *((x, y) for x, y in product((1, 3, 5, 7, 9, 11), repeat=2)),
    *((x, y) for x, y in product((2, 4, 6, 8, 10), repeat=2))
])
def test_bad_line_coordinates(char_grid: Slitherlink, test_x: int, test_y: int):
    with pytest.raises(NotALineTile):
        char_grid.change_line_segment(test_x, test_y, "L")


@pytest.mark.parametrize("test_x, test_y", [
    *((x, y) for x, y in product((1, 3, 5, 7, 9, 11), (2, 4, 6, 8, 10)))
])
def test_correct_line_coordinates(char_grid: Slitherlink,
                                  test_x: int, test_y: int):
    char_grid.change_line_segment(test_x, test_y, "L")  # No exception here.
