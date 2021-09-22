from slitherlinking.slitherlink_internal_state import Slitherlink


if __name__ == '__main__':
    print("So far, this is just a placeholder.")
    small_example = Slitherlink(3, 4)
    small_example.change_number(2, 3, 2)
    for row in small_example.state_of_grid:
        print(row)
    print()
    print(small_example)
    print()
    for row in small_example.state_of_grid:
        print(row)
