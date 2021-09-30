from visuals.text_button import StateChangerButton, NumberInput, Position
from visuals.colours import Colour, OLIVE, PINK, WHITE
from slitherlinking.slitherlink_internal_state import Slitherlink
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
        self.grid_state = Slitherlink(1, 1)

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
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
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
                 text_input_fields: list[NumberInput], background: Colour):
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

    def update_menu(self, mouse_position: Position):
        """In case a mouse left click happens, checks whether any button
        was clicked. If so, current app state updates."""
        for button in self.game_state_change_buttons:
            new_state = button.button_state_update(mouse_position,
                                                   GAME.mouse_left_clicked)
            if new_state is not None:
                return new_state

    def draw_state_specific_objects(self):
        """Enables drawing objects specific in the current state."""

    def startup(self):
        """Placeholder for state start up."""

    def cleanup(self):
        """Cleans up a state, any necessary work to leave the current state."""


class MainMenu(ButtonStateHandler):
    def __init__(self):
        state_changers = [
            StateChangerButton((900, 200), "Play!", 36, PINK, WHITE, "game"),
            StateChangerButton((900, 400), "Instructions", 36, PINK, WHITE,
                               "instructions"),
            StateChangerButton((900, 800), "Quit", 36, PINK, WHITE, "quit")
        ]
        self.x = NumberInput((PINK, WHITE), 100, 100, "horizontal\ngrid size")
        self.y = NumberInput((PINK, WHITE), 100, 500, "vertical\ngrid size")
        super().__init__(state_changers, [self.x, self.y], OLIVE)

    def cleanup(self):
        GAME.grid_state = Slitherlink(int(self.x.text), int(self.y.text))


class GamePlay(ButtonStateHandler):
    def __init__(self):
        self.text_buttons = [back_to_menu]
        self.background = OLIVE
        super().__init__(self.text_buttons, [], self.background)


if __name__ == "__main__":
    pygame.init()
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
