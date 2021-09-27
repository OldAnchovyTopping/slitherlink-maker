from pygame.freetype import SysFont
from pygame.sprite import Sprite
import pygame
Colour = tuple[int, int, int, int]  # Alpha value MUST be included!


def create_surface(text: str, size: int, bg_rgb: Colour, font_rgb: Colour,
                   bolds: bool = False, italics: bool = False):
    """Returns a text surface to become a button later."""
    font = SysFont("Palatino", size, bolds, italics)
    surface, _ = font.render(text, font_rgb, bg_rgb)
    return surface.convert_alpha()


class StateChangerButton(Sprite):
    def __init__(self, center_pos: tuple[int, int], text: str, size: int,
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

    def button_state_update(self, mouse_pos: tuple[int, int], clicked: bool):
        if self.rect.collidepoint(mouse_pos):
            self.mouse_over = True
            if clicked:
                return self.next_state
        else:
            self.mouse_over = False

    def draw_element(self, surface):
        surface.blit(self.image, self.rect)


class NumberInput:
    def __init__(self, colours: tuple[Colour, Colour],
                 corner_x: int, corner_y: int):
        self.rect = pygame.Rect(corner_x, corner_y, 250, 250)
        assert len(colours) == 2
        self.active_colour, self.inactive_colour = colours
        self.colour = self.inactive_colour
        self.text_size = 200
        self.text = "8"
        self.text_surface = create_surface(self.text, self.text_size,
                                           self.colour, (0, 0, 0, 255))
        self.is_active = False

    def activity_update(self, mouse_pos: tuple[int, int], clicked: bool):
        if clicked:
            if self.rect.collidepoint(mouse_pos):
                self.is_active = True
                self.colour = self.active_colour
                self.text_surface = create_surface(self.text, self.text_size,
                                                   self.colour, (0, 0, 0, 255))

    def text_update(self, key_press_event):
        pressed_key = key_press_event.key
        if pressed_key == pygame.K_RETURN:
            self.is_active = False
            self.colour = self.inactive_colour
        elif pressed_key == pygame.K_BACKSPACE:
            self.text = self.text[:-1]
        elif pygame.K_0 <= pressed_key <= pygame.K_9 or\
                pygame.K_KP1 <= pressed_key <= pygame.K_KP0:
            self.text += key_press_event.unicode
            self.text = self.text[-2:]  # We only allow 2 characters at most.
        # Re-render the text.
        self.text_surface = create_surface(self.text, self.text_size,
                                           self.colour, (0, 0, 0, 255))

    def draw(self, screen):
        # Here is the box outline.
        pygame.draw.rect(screen, self.colour, self.rect, 2)
        # And now we make sure the displayed text is centered.
        vertical_pad = (self.rect.h - self.text_surface.get_height()) // 2
        horizontal_pad = (self.rect.w - self.text_surface.get_width()) // 2
        corner = (self.rect.x + horizontal_pad, self.rect.y + vertical_pad)
        screen.blit(self.text_surface, corner)
