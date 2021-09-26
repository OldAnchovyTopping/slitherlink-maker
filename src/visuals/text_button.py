from pygame.freetype import SysFont
from pygame.sprite import Sprite
import pygame


def create_surface(text: str, size: int, bg_rgb: tuple, font_rgb: tuple,
                   bolds: bool = False, italics: bool = False):
    """Returns a text surface to become a button later."""
    font = SysFont("Palatino", size, bolds, italics)
    surface, _ = font.render(text, font_rgb, bg_rgb)
    return surface.convert_alpha()


class StateChangerButton(Sprite):
    def __init__(self, center_pos: tuple, text: str, size: int,
                 bg_rgb: tuple, font_rgb: tuple, action: str):
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

    def button_state_update(self, mouse_position: tuple, mouse_clicked: bool):
        if self.rect.collidepoint(mouse_position):
            self.mouse_over = True
            if mouse_clicked:
                return self.next_state
        else:
            self.mouse_over = False

    def draw_element(self, surface):
        surface.blit(self.image, self.rect)


class TextInputField:
    def __init__(self, colours: tuple, corner_x: int, corner_y: int,
                 width: int, height: int):
        self.rect = pygame.Rect(corner_x, corner_y, width, height)
        assert len(colours) == 2
        self.active_colour, self.inactive_colour = colours
        self.colour = self.inactive_colour
        self.text_size = height - 10
        self.text = "8"
        self.text_surface = create_surface(self.text, self.text_size,
                                           self.colour, (0, 0, 0))
        self.is_active = False

    def activity_update(self, mouse_position: tuple, mouse_clicked: bool):
        if mouse_clicked:
            if self.rect.collidepoint(mouse_position):
                self.is_active = True
                self.colour = self.active_colour
                self.text_surface = create_surface(self.text, self.text_size,
                                                   self.colour, (0, 0, 0))

    def text_update(self, key_press_event):
        if key_press_event.key == pygame.K_RETURN:
            self.is_active = False
            self.colour = self.inactive_colour
        elif key_press_event.key == pygame.K_BACKSPACE:
            self.text = self.text[:-1]
        else:
            self.text += key_press_event.unicode
        # Re-render the text.
        self.text_surface = create_surface(self.text, self.text_size,
                                           self.colour, (0, 0, 0))
        self.rect.w = max(200, self.text_surface.get_width() + 100)

    def draw(self, screen):
        screen.blit(self.text_surface, self.rect)
        pygame.draw.rect(screen, self.colour, self.rect, 2)
