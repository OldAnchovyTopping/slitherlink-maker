from copy import deepcopy


class PathCrossingException(Exception):
    """Raised when a corner has >= 3 incident edges."""
    pass


class CellValueOverload(Exception):
    """Raised when a cell has more incident edges than its value."""
    pass


class Slitherlink:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.grid_width = 2 * self.width + 1
        self.grid_height = 2 * self.height + 1
        even_row = list("E" + "XE" * (self.width + 1))  # With extra padding
        odd_row = ["E" if i % 2 else 4 for i in range(self.grid_width + 2)]
        odd_row[0] = odd_row[-1] = " "  # Don't forget the padding
        self.state_of_grid = [odd_row[:] if i % 2 else even_row[:]
                              for i in range(self.grid_height)]
        vertical_padding = list(" E" * (self.width + 1) + " ")
        self.state_of_grid.insert(0, vertical_padding)  # Need to pad top...
        self.state_of_grid.append(vertical_padding)  # ... And bottom too.

    def __repr__(self):
        return f"Slitherlink(width={self.width}, height={self.height})"

    def __eq__(self, other):
        return self.state_of_grid == other.state_of_grid

    def __str__(self):
        pretty_grid = deepcopy(self.state_of_grid)
        for row in range(2, self.grid_height, 2):
            for column in range(2, self.grid_width, 2):
                pretty_grid[row][column] = str(pretty_grid[row][column])
        return "\n".join(str(row) for row in pretty_grid)

    def change_line_segment(self, line_x: int, line_y: int, to_empty: bool):
        """
        Places or erases an edge. The coordinates must point to
        an inside edge, otherwise an assertion fails.

        :param line_x: The x-coordinate of the line in self.state_of_grid.
        :param line_y: The y-coordinate of the line in self.state_of_grid.
        :param to_empty: True means erase an edge. False mean add an edge.
        """
        assert 1 <= line_x <= self.grid_height, "Row index out of bounds."
        assert 1 <= line_y <= self.grid_width, "Column index out of bounds."
        assert (line_x + line_y) % 2, "These coordinates are not an edge."
        new_addition = "E" if to_empty else "L"
        self.state_of_grid[line_x][line_y] = new_addition

    def change_number(self, cell_x: int, cell_y: int, new_number: int):
        """
        Rewrites a number at a given position.

        :param cell_x: The x-coordinate of the line in self.state_of_grid.
        :param cell_y: The y-coordinate of the line in self.state_of_grid.
        :param new_number: True means erase an edge. False mean add an edge.
        """
        assert 1 <= cell_x <= self.height, "Row index out of bounds."
        assert 1 <= cell_y <= self.width, "Column index out of bounds."
        assert 0 <= new_number <= 4, "Invalid input. 0-3 numbers, or 4 empty."
        true_x, true_y = 2 * cell_x, 2 * cell_y  # In self.state_of_grid.
        self.state_of_grid[true_x][true_y] = new_number

    def number_of_lined_edges_around(self, true_x: int, true_y: int):
        """
        Counts the number of active edges around a cell or
        the number of active edges incoming into a corner.

        :param true_x: The x-coordinate of the tile in self.state_of_grid.
        :param true_y: The y-coordinate of the tile in self.state_of_grid.
        :return: A number between 0 and 4, number of active incident edges.
        """
        assert 1 <= true_x <= self.grid_height, "Row index out of bounds."
        assert 1 <= true_y <= self.grid_width, "Column index out of bounds."
        up_edge = self.state_of_grid[true_x - 1][true_y] == "L"
        left_edge = self.state_of_grid[true_x][true_y - 1] == "L"
        right_edge = self.state_of_grid[true_x][true_y + 1] == "L"
        down_edge = self.state_of_grid[true_x + 1][true_y] == "L"
        return up_edge + left_edge + right_edge + down_edge  # Bool summing!

    def check_a_corner(self, corner_x: int, corner_y: int) -> bool:
        """Returns True iff the number of corner incident edges is <= 2."""
        assert 0 <= corner_x <= self.height, "Row index out of bounds."
        assert 0 <= corner_y <= self.width, "Column index out of bounds."
        true_x, true_y = 2 * corner_x + 1, 2 * corner_y + 1
        return self.number_of_lined_edges_around(true_x, true_y) <= 2

    def check_all_corners(self):
        """Raises a PathCrossingException if the path is crossing itself."""
        for x_coordinate in range(self.height + 1):
            for y_coordinate in range(self.width + 1):
                if not self.check_a_corner(x_coordinate, y_coordinate):
                    raise PathCrossingException(
                        f"The path crosses at {x_coordinate}, {y_coordinate}."
                    )

    def check_a_number(self, cell_x: int, cell_y: int):
        """Returns True iff
        the number of cell adjacent edges is <= cell_value."""
        assert 0 <= cell_x <= self.height, "Row index out of bounds."
        assert 0 <= cell_y <= self.width, "Column index out of bounds."
        true_x, true_y = 2 * cell_x, 2 * cell_y  # In self.state_of_grid.
        cell_value = self.state_of_grid[true_x][true_y]
        adjacent_edges = self.number_of_lined_edges_around(true_x, true_y)
        return adjacent_edges <= cell_value

    def check_all_numbers(self):
        """Raises a CellValueOverload if the path is crossing itself."""
        for x_coordinate in range(1, self.height + 1):
            for y_coordinate in range(1, self.width + 1):
                if not self.check_a_number(x_coordinate, y_coordinate):
                    raise CellValueOverload(
                        f"The cell at {x_coordinate}, {y_coordinate} has"
                        f" too many edges."
                    )