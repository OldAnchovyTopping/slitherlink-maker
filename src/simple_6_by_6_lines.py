from slitherlinking.slitherlink_internal_state import Slitherlink


if __name__ == '__main__':
    lines = [(1, 2), (1, 8), (1, 10), (1, 12), (2, 5), (2, 7), (2, 13),
             (3, 10), (4, 1), (4, 7), (4, 13), (5, 4), (5, 8), (5, 10),
             (5, 12), (7, 4), (8, 3), (8, 5), (9, 2), (9, 6), (9, 10),
             (10, 1), (10, 7), (10, 9), (10, 11), (11, 2), (11, 6),
             (11, 10), (12, 3), (12, 5), (13, 4)]
    number_test_grid = Slitherlink(6, 6)
    for x, y in lines:
        number_test_grid.change_line_segment(x, y, "L")

    number_test_grid.change_number(1, 4, 0)
    number_test_grid.change_number(4, 2, 1)
    number_test_grid.change_number(3, 1, 2)
    number_test_grid.change_number(5, 6, 3)
    print(number_test_grid)
