from visuals.text_button import StateChangerButton, TextInputField
import pygame
import os.path
import sys


def entire_path(file_name: str) -> str:
    return os.path.join(BASE_PATH, file_name)


class AppControl:
    """Controls the entire game."""
    def __init__(self, starting_state):
        self.game_running = True
        self.mouse_left_clicked = False
        self.pressed_key_event = None
        self.fps = 60
        self.state = STATE_DICT[starting_state]
        self.clock = pygame.time.Clock()

    def app_state_update(self):
        """Pushes states further upon choosing."""
        # self.state.cleanup() So far this doesn't seem necessary.
        try:
            self.state = STATE_DICT[self.state.next_state_to_move_to]
        except KeyError:
            assert self.state.next_state_to_move_to == "quit"
            self.game_running = False

        self.state.startup()

    def event_loop(self):
        """Basis for all application events."""
        self.mouse_left_clicked = False
        self.pressed_key_event = None
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
                self.state.next_state_to_move_to = self.state.update_menu(pygame.mouse.get_pos())
                if self.state.next_state_to_move_to is not None:
                    self.app_state_update()
                    continue
            self.state.draw_menu_buttons(SCREEN)

            # Possibly draw some other stuffs after.

            pygame.display.update()


class ButtonStateHandler:
    """Handles menu and button logic, as well as drawing."""
    def __init__(self, state_changers: list, text_input_fields: list, background, is_background_solid: bool = True):
        self.game_state_change_buttons = state_changers
        self.text_inputs = text_input_fields
        self.background = background
        self.is_background_solid = is_background_solid

    def draw_menu_buttons(self, screen):
        """Blits the buttons on the screen with appropriate highlighting based on mouse position."""
        if self.is_background_solid:  # True -> solid colour, False -> pygame.image!
            screen.fill(self.background)
        else:
            screen.blit(self.background, (0, 0))
        for button in self.game_state_change_buttons:
            button.button_state_update(pygame.mouse.get_pos(), GAME.mouse_left_clicked)
            button.draw_element(screen)

        for text_surface in self.text_inputs:
            text_surface.activity_update(pygame.mouse.get_pos(), GAME.mouse_left_clicked)
            if GAME.pressed_key_event is not None:
                text_surface.text_update(GAME.pressed_key_event)
            text_surface.draw(screen)

    def update_menu(self, mouse_position: tuple):
        """In case of a click happening, checks whether any button was clicked. If so, current state updates."""
        for button in self.game_state_change_buttons:
            maybe_new_state = button.button_state_update(mouse_position, GAME.mouse_left_clicked)
            if maybe_new_state is not None:
                return maybe_new_state

    def startup(self):
        """Does things when a state is entered. This one is just a parent function."""
        pass

    def hover_sound(self):
        """This might be better in the Button class..."""
        pass


class MainMenu(ButtonStateHandler):
    def __init__(self):
        self.next_state_to_move_to = None
        self.play_the_game = StateChangerButton((900, 200), "Play!", 36, PINK, WHITE, "player_1")
        self.read_the_instructions = StateChangerButton((900, 400), "Instructions", 36, PINK, WHITE, "instructions")
        self.edit_options = StateChangerButton((900, 600), "Options (Coming Soon)", 36, PINK, WHITE, "options")
        self.quit_the_game = StateChangerButton((900, 800), "Quit", 36, PINK, WHITE, "quit")
        self.text_buttons = [self.play_the_game, self.read_the_instructions, self.edit_options, self.quit_the_game]
        self.background = OLIVE  # It'll either be a solid colour, or a pygame.image.
        self.is_background_solid_colour = True  # Colour -> True, Image -> False!
        self.text_input_test = TextInputField((PINK, WHITE), 10, 10, 300, 200)
        super().__init__(self.text_buttons, [self.text_input_test], self.background, self.is_background_solid_colour)

    def startup(self):
        """Need to clean up both players as well as the board."""
        GAME.first_player = None
        GAME.second_player = None


class GamePlay(ButtonStateHandler):
    def __init__(self):
        self.next_state_to_move_to = None
        self.text_buttons = [back_to_main_menu_button]
        self.background = OLIVE
        self.is_background_solid_colour = False  # Colour -> True, Image -> False!
        super().__init__(self.text_buttons, [], self.background, self.is_background_solid_colour)


if __name__ == "__main__":
    PINK = (245, 202, 195)
    WHITE = (255, 255, 255)
    OLIVE = (134, 161, 96)

    # This is to have a base path to file in a variable,
    # regardless of if we freeze the project into a .exe. format.
    if getattr(sys, "frozen", False):
        BASE_PATH = sys._MEIPASS
    else:
        BASE_PATH = os.path.dirname(os.path.abspath(__file__))
    pygame.init()
    SCREEN = pygame.display.set_mode((1880, 900))
    Menu = MainMenu()
    back_to_main_menu_button = StateChangerButton((1600, 800), "<- Back to Main Menu", 36, OLIVE, WHITE, "main_menu")
    Time_To_Play = GamePlay()
    STATE_DICT = {
        "main_menu": Menu,
        "game": Time_To_Play,
        "instructions": Exception,
        "options": Exception
    }  # We don't include the quit, but instead use it as a KeyError exception.
    GAME = AppControl("main_menu")
    GAME.main_game_loop()
    pygame.quit()
    raise SystemExit
