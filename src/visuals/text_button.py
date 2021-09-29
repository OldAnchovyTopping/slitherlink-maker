from pygame.freetype import SysFont
from pygame.sprite import Sprite
import pygame
from visuals.colours import Colour, BLACK
Position = tuple[int, int]


def create_surface(text: str, size: int, bg_rgb: Colour, font_rgb: Colour,
                   bolds: bool = False, italics: bool = False):
    """Returns a text surface to become a button later."""
    font = SysFont("Palatino", size, bolds, italics)
    surface, _ = font.render(text, font_rgb, bg_rgb)
    return surface.convert_alpha()


class StateChangerButton(Sprite):
    def __init__(self, center_pos: Position, text: str, size: int,
                 bg_rgb: Colour, font_rgb: Colour, action: str):
        """
        Makes a UI text button.

        :param center_pos: An (x,y) tuple of the rectangle's center.
        :param text: Text to display.
        :param size: Size of the text.
        :param bg_rgb: Button colour.
        :param font_rgb: Font colour.
        """
        self.mouse_over = False
        self.text = text
        self.default_image = create_surface(text, size, bg_rgb, font_rgb)
        self.highlight_image = create_surface(text, round(size * 1.3),
                                              bg_rgb, font_rgb, True, True)
        self.default_rect = self.default_image.get_rect(center=center_pos)
        self.highlight_rect = self.highlight_image.get_rect(center=center_pos)
        self.next_state = action
        super().__init__()

    @property
    def image(self):
        return self.highlight_image if self.mouse_over else self.default_image

    @property
    def rect(self):
        return self.highlight_rect if self.mouse_over else self.default_rect

    def button_state_update(self, mouse_position: Position, clicked: bool):
        if self.rect.collidepoint(mouse_position):
            self.mouse_over = True
            if clicked:
                return self.next_state
        else:
            self.mouse_over = False

    def draw_element(self, surface):
        surface.blit(self.image, self.rect)


class NumberInput:
    def __init__(self, colours: tuple[Colour, Colour],
                 corner_x: int, corner_y: int, label_string: str):
        self.rect = pygame.Rect(corner_x, corner_y, 270, 270)
        assert len(colours) == 2
        self.active_colour, self.inactive_colour = colours
        self.colour = self.inactive_colour
        self.label_size = 20
        self.input_size = 200
        self.text = "8"
        self.label_list = label_string.split("\n")
        self.input_text, self.label_texts = self.recreate_surfaces()
        self.is_active = False

    def recreate_surfaces(self):
        num_in = create_surface(self.text, self.input_size, self.colour, BLACK)
        labels = [create_surface(s, self.label_size, self.colour, BLACK)
                  for s in self.label_list]
        return num_in, labels

    def activity_update(self, mouse_position: Position, clicked: bool):
        if clicked:
            if self.rect.collidepoint(mouse_position):
                self.is_active = True
                self.colour = self.active_colour
                # Re-render the text.
                self.input_text, self.label_texts = self.recreate_surfaces()

    def text_update(self, key_press_event):
        pressed_key = key_press_event.key
        if self.is_active:
            if pressed_key == pygame.K_RETURN:
                self.is_active = False
                self.colour = self.inactive_colour
            elif pressed_key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
                if not self.text:
                    self.text = "1"
            elif pygame.K_0 <= pressed_key <= pygame.K_9 or\
                    pygame.K_KP1 <= pressed_key <= pygame.K_KP0:
                self.text += key_press_event.unicode
                self.text = self.text[-2:]  # At most 2 characters allowed.
        # Re-render the text.
        self.input_text, self.label_texts = self.recreate_surfaces()

    def draw(self, screen):
        # First the box outline.
        pygame.draw.rect(screen, self.colour, self.rect, 2)

        # Then proper spacing for both the labels and input text.
        label_heights = [label.get_height() for label in self.label_texts]
        total_label_height = sum(label_heights)
        vertical_space = (self.rect.h - self.input_text.get_height() -
                          total_label_height) // 3
        horizontal_input = (self.rect.w - self.input_text.get_width()) // 2
        corner_input = (self.rect.x + horizontal_input,
                        self.rect.y + total_label_height + 2 * vertical_space)
        screen.blit(self.input_text, corner_input)

        # To finish, we work on and display the label lines.
        for index, label in enumerate(self.label_texts):
            horizontal_padding = (self.rect.w - label.get_width()) // 2
            vertical_padding = vertical_space + sum(label_heights[:index])
            corner_label = (self.rect.x + horizontal_padding,
                            self.rect.y + vertical_padding)
            screen.blit(label, corner_label)
