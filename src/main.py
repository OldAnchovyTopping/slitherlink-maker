from visuals.text_button import StateChangerButton,\
    NumberInput, Position, TextTile
from visuals.colours import Colour, OLIVE, PINK, WHITE, BLACK, GRAY
from slitherlinking.slitherlink_internal_state import Slitherlink
from pygame.font import SysFont
from typing import Sequence, Union
import pygame


class AppControl:
    """Controls the entire game."""
    def __init__(self, starting_state: str):
        self.game_running = True
        self.mouse_left_clicked = False
        self.pressed_key_event = pygame.NOEVENT
        self.fps = 60
        self.state: ButtonStateHandler = STATE_DICT[starting_state]
        self.clock = pygame.time.Clock()
        self.grid_width, self.grid_height = 8, 8

    def app_state_update(self):
        """Pushes states further upon choosing."""
        self.state.cleanup()  # Any necessary work to close the state.

        try:
            self.state = STATE_DICT[self.state.next_state_to_move_to]
        except KeyError:
            assert self.state.next_state_to_move_to == "quit"
            self.game_running = False

        self.state.startup()  # Any necessary work to open up the state.

    def event_loop(self):
        """Basis for all application events."""
        self.mouse_left_clicked = False
        self.pressed_key_event = pygame.NOEVENT
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.state.process_specific_events(event)
                if event.button == 1:
                    self.mouse_left_clicked = True
            if event.type == pygame.KEYDOWN:
                self.pressed_key_event = event

    def main_game_loop(self):
        """Handles the main game loop. Duh."""
        while self.game_running:
            self.clock.tick(self.fps)
            self.event_loop()
            if self.mouse_left_clicked:
                new_state = self.state.update_menu(pygame.mouse.get_pos())
                self.state.next_state_to_move_to = new_state
                if self.state.next_state_to_move_to:
                    self.app_state_update()
                    continue
            self.state.draw_visible_objects(SCREEN)

            # Possibly draw some other stuffs after.

            pygame.display.update()


class ButtonStateHandler:
    """Handles menu and button logic, as well as drawing."""
    def __init__(self, state_changers: list[StateChangerButton],
                 text_input_fields: Sequence[Union[TextTile, NumberInput]],
                 background: Colour):
        self.next_state_to_move_to = ""
        self.game_state_change_buttons = state_changers
        self.text_inputs = text_input_fields
        self.background = background

    def draw_visible_objects(self, screen):
        """Blits all objects on the screen with
        appropriate highlighting based on mouse position."""
        screen.fill(self.background)
        for button in self.game_state_change_buttons:
            button.button_state_update(pygame.mouse.get_pos(),
                                       GAME.mouse_left_clicked)
            button.draw_element(screen)

        for text_surface in self.text_inputs:
            text_surface.activity_update(pygame.mouse.get_pos(),
                                         GAME.mouse_left_clicked)
            if GAME.pressed_key_event:
                text_surface.text_update(GAME.pressed_key_event)
            text_surface.draw(screen)
        self.draw_state_specific_objects(screen)

    def update_menu(self, mouse_position: Position):
        """In case a mouse left click happens, checks whether any button
        was clicked. If so, current app state updates."""
        for button in self.game_state_change_buttons:
            new_state = button.button_state_update(mouse_position,
                                                   GAME.mouse_left_clicked)
            if new_state is not None:
                return new_state

    def draw_state_specific_objects(self, screen):
        """Enables drawing objects specific in the current state."""

    def process_specific_events(self, event):
        """Takes care of the more specific events."""

    def startup(self):
        """Placeholder for state start up."""

    def cleanup(self):
        """Cleans up a state, any necessary work to leave the current state."""


class MainMenu(ButtonStateHandler):
    def __init__(self):
        state_changers = [
            StateChangerButton((900, 200), "Play!", 70, PINK, WHITE, "game"),
            StateChangerButton((900, 400), "Instructions", 65, PINK, WHITE,
                               "instructions"),
            StateChangerButton((900, 800), "Quit", 60, PINK, WHITE, "quit")
        ]
        self.x = NumberInput((PINK, WHITE), 100, 100, "horizontal\ngrid size")
        self.y = NumberInput((PINK, WHITE), 100, 500, "vertical\ngrid size")
        super().__init__(state_changers, [self.x, self.y], OLIVE)

    def cleanup(self):
        GAME.grid_width = int(self.x.text)
        GAME.grid_height = int(self.y.text)


class GamePlay(ButtonStateHandler):
    def __init__(self):
        # Just placeholders for now, to not declare outside of __init__.
        self.grid_state = Slitherlink(1, 1)
        self.outline_rect = pygame.Rect(25, 25, 0, 0)
        self.corner_rectangles: list[pygame.Rect] = []
        self.edges: list[tuple[int, int, pygame.Rect]] = []
        self.cell_rectangles: list[tuple[int, int, pygame.Rect]] = []
        self.x_rectangles: dict[tuple[int, int], pygame.Rect] = {}
        self.number_font = SysFont("palatinolinotype", 1)
        self.edge_x = self.number_font.render("x", True, BLACK, WHITE)
        self.editor_mode = True
        self.editor_switcher = pygame.Rect(1600, 100, 60, 60)

        filename = TextTile((PINK, WHITE), 1400, 300, "Name of puzzle/file:")
        self.state_buttons = [back_to_menu]
        self.input_tiles = [filename]
        self.background = OLIVE
        super().__init__(self.state_buttons, self.input_tiles, self.background)

    def startup(self):
        self.grid_state = Slitherlink(GAME.grid_width, GAME.grid_height)
        self.grid_state.change_line_segment(1, 2, 12)
        self.grid_state.change_line_segment(1, 4, 24)
        self.grid_state.change_line_segment(1, 6, 24)
        self.grid_state.change_line_segment(1, 8, 24)
        self.grid_state.change_line_segment(7, 10, 12)
        self.grid_state.change_line_segment(2, 3, 12)
        self.grid_state.change_line_segment(9, 4, 24)
        self.grid_state.change_line_segment(12, 5, 12)
        self.grid_state.change_line_segment(14, 5, 12)
        self.grid_state.change_line_segment(14, 11, 12)
        self.grid_state.change_line_segment(11, 14, 12)
        self.grid_state.change_line_segment(13, 16, 12)
        self.grid_state.change_number(1, 4, 0)
        self.grid_state.change_number(4, 2, 1)
        self.grid_state.change_number(3, 1, 2)
        self.grid_state.change_number(5, 6, 3)
        self.grid_state.change_number(8, 8, 0)
        # We need to calculate some grid and cell sizes.
        number_of_tiny_columns = 3 + 7 * GAME.grid_width
        maximum_column_size = SLITHERLINK_MAX_WIDTH // number_of_tiny_columns
        number_of_tiny_rows = 3 + 7 * GAME.grid_height
        maximum_row_size = SLITHERLINK_MAX_HEIGHT // number_of_tiny_rows
        thin_size = min(10, maximum_row_size, maximum_column_size)
        cell_size = 6 * thin_size  # This is why the 7* was present.
        size_together = thin_size + cell_size
        total_width = number_of_tiny_columns * thin_size
        total_height = number_of_tiny_rows * thin_size
        self.number_font = SysFont("palatinolinotype", cell_size)
        x_font = SysFont("palatinolinotype", cell_size // 2)
        self.edge_x = x_font.render("x", True, BLACK, WHITE)
        cross_h, cross_w = self.edge_x.get_height(), self.edge_x.get_width()
        horizontal_thin_offset_x: int = (cross_h - thin_size) // 2
        horizontal_thick_offset_x: int = (cell_size - cross_w) // 2
        vertical_thick_offset_x: int = (cell_size - cross_h) // 2
        vertical_thin_offset_x: int = (cross_w - thin_size) // 2

        # First we reset the rectangle memory:
        the_x, the_y = THE_CORNER
        self.outline_rect = pygame.Rect(the_x, the_y, total_width, total_height)
        self.corner_rectangles = []
        self.edges = []
        self.cell_rectangles = []
        self.x_rectangles = {}
        # Having done that, let's precompute the relevant rectangles.
        # First go the corners:
        for index_y in range(GAME.grid_height + 1):
            new_corner = [the_x + thin_size,
                          the_y + thin_size + index_y * size_together]
            for _ in range(GAME.grid_width + 1):
                x_cor, y_cor = new_corner
                new_rect = pygame.Rect(x_cor, y_cor, thin_size, thin_size)
                self.corner_rectangles.append(new_rect)
                new_corner[0] += size_together
        # Secondly, the horizontal edge segments:
        horizontal_edges: list[tuple[int, int, pygame.Rect]] = []
        for index_y in range(GAME.grid_height + 1):
            y_base = the_y + thin_size + index_y * size_together
            new_corner = [the_x + 2 * thin_size, y_base]
            cross_corner = [the_x + 2 * thin_size + horizontal_thick_offset_x,
                            y_base - horizontal_thin_offset_x]
            state_y = 2 * index_y + 1
            state_x = 2
            for _ in range(GAME.grid_width):
                x_cor, y_cor = new_corner
                new_rect = pygame.Rect(x_cor, y_cor, cell_size, thin_size)
                horizontal_edges.append((state_y, state_x, new_rect))
                # We also have to stash the rectangles for X's.
                x_cor, y_cor = cross_corner
                x_rect = pygame.Rect(x_cor, y_cor, cross_w, cross_h)
                self.x_rectangles[(state_y, state_x)] = x_rect
                new_corner[0] += size_together
                cross_corner[0] += size_together
                state_x += 2
        # Next go the vertical edge segments:
        vertical_edges: list[tuple[int, int, pygame.Rect]] = []
        for index_x in range(GAME.grid_height + 1):
            x_base = the_x + thin_size + index_x * size_together
            new_corner = [the_x + thin_size + index_x * size_together,
                          the_y + 2 * thin_size]
            cross_corner = [x_base - vertical_thin_offset_x,
                            the_y + 2 * thin_size + vertical_thick_offset_x]
            state_x = 2 * index_x + 1
            state_y = 2
            for _ in range(GAME.grid_width):
                x_cor, y_cor = new_corner
                new_rect = pygame.Rect(x_cor, y_cor, thin_size, cell_size)
                vertical_edges.append((state_y, state_x, new_rect))
                # We also have to stash the rectangles for X's.
                x_cor, y_cor = cross_corner
                x_rect = pygame.Rect(x_cor, y_cor, cross_w, cross_h)
                self.x_rectangles[(state_y, state_x)] = x_rect
                new_corner[1] += size_together
                cross_corner[1] += size_together
                state_y += 2
        self.edges = vertical_edges + horizontal_edges
        # Finally, we make the number cell rectangles:
        for index_y in range(GAME.grid_height):
            new_corner = [the_x + 2 * thin_size,
                          the_y + 2 * thin_size + index_y * size_together]
            state_y = 2 * index_y + 2
            state_x = 2
            for index_x in range(1, GAME.grid_width + 1):
                x_cor, y_cor = new_corner
                new_rect = pygame.Rect(x_cor, y_cor, cell_size, cell_size)
                self.cell_rectangles.append((state_y, state_x, new_rect))
                new_corner[0] += size_together
                state_x += 2

    def draw_state_specific_objects(self, screen):
        """Draws the slitherlink grid. That's why we're here!"""
        if self.editor_mode:
            pygame.draw.rect(screen, BLACK, self.editor_switcher)
        else:
            pygame.draw.rect(screen, WHITE, self.editor_switcher)
        pygame.draw.rect(screen, WHITE, self.outline_rect)
        for rect in self.corner_rectangles:
            pygame.draw.rect(screen, BLACK, rect)
        for y, x, orthogonal_edge_rect in self.edges:
            if self.grid_state.state_of_grid[y][x] == 24:
                x_rect = self.x_rectangles[(y, x)]
                screen.blit(self.edge_x, x_rect)
                continue
            edge_is_lined = self.grid_state.state_of_grid[y][x] == 12
            colour = GRAY if edge_is_lined else WHITE
            pygame.draw.rect(screen, colour, orthogonal_edge_rect)
        for y, x, grid_cell in self.cell_rectangles:
            if (number := self.grid_state.state_of_grid[y][x]) in {0, 1, 2, 3}:
                text = str(number)
                surface = self.number_font.render(text, True, BLACK, PINK)
                surface = surface.convert_alpha()
                vertical_pad = (grid_cell.h - surface.get_height()) // 2
                horizontal_pad = (grid_cell.w - surface.get_width()) // 2
                number_corner = (grid_cell.x + horizontal_pad,
                                 grid_cell.y + vertical_pad)
                screen.blit(surface, number_corner)

    def process_specific_events(self, event):
        """More specifically, processes the clicks."""
        click_x, click_y = pygame.mouse.get_pos()
        if self.editor_switcher.collidepoint(click_x, click_y):
            self.editor_mode = not self.editor_mode
        if self.outline_rect.collidepoint(click_x, click_y):
            # This means that the click needs further processing.
            if event.button == 3:
                number_shift = -1
                number_to_put = 24
            else:  # We shall regard *only* the right click as decrement.
                number_shift = 1
                number_to_put = 12
            for y, x, rectangle in self.edges:
                if rectangle.collidepoint(click_x, click_y):
                    current_tile = self.grid_state.state_of_grid[y][x]
                    new_tile = number_to_put if current_tile == 5 else 5
                    self.grid_state.state_of_grid[y][x] = new_tile
            if self.editor_mode:  # Otherwise numbers can't change.
                for y, x, cell in self.cell_rectangles:
                    if cell.collidepoint(click_x, click_y):
                        current_number = self.grid_state.state_of_grid[y][x]
                        new_number = (current_number + number_shift) % 5
                        self.grid_state.state_of_grid[y][x] = new_number


if __name__ == "__main__":
    pygame.init()
    pygame.display.set_caption("Slitherlink Maker")
    # pygame.display.set_icon(pygame.image.load("hearts.png"))  To be added!
    SLITHERLINK_MAX_WIDTH, SLITHERLINK_MAX_HEIGHT = 1500, 880
    THE_CORNER = (25, 25)
    SCREEN = pygame.display.set_mode((1880, 900))
    Menu = MainMenu()
    back_to_menu = StateChangerButton((1600, 800), "<- Back to Main Menu", 36,
                                      OLIVE, WHITE, "main_menu")
    Time_To_Play = GamePlay()
    STATE_DICT: dict[str, ButtonStateHandler] = {
        "main_menu": Menu,
        "game": Time_To_Play,
        # "instructions": Exception
    }  # We don't include the quit, but instead use it as a KeyError exception.
    GAME = AppControl("main_menu")
    GAME.main_game_loop()
    pygame.quit()
    raise SystemExit
