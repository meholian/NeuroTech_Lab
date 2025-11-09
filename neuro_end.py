import pygame
from neuro_defaults import *

def create_text_surface(text: str, font_name: str, size: int, aa = True, color = "black") -> pygame.Surface:
    font = pygame.font.Font(font_name, size)
    render = font.render(text, aa, color)
    return render, render.get_rect()

class End:
    class Button(pygame.Rect):
        def __init__(self, centerx, centery, w, h, text, color):
            super().__init__(0, 0, w, h)
            self.center = (centerx, centery)

            self.color = color
            self.textrender, self.textrect = create_text_surface(text, DEFAULT_FONT, 10)
            self.textrect.center = self.center

        def draw(self, screen):
            pygame.draw.rect(screen, self.color, self)
            screen.blit(self.textrender, self.textrect)

        def is_mouse_in_button(self):
            return self.collidepoint(pygame.mouse.get_pos())

    def __init__(self, font_name, status):
        self.status = status
        if self.status == True:
            self.titledisplay, self.titlerect = create_text_surface("You Won!", font_name, 20)
        else:
            self.titledisplay, self.titlerect = create_text_surface("You Lost!", font_name, 20)

        # Center positions based on frame size, no scaling
        frame_centerx = FRAME_SIZE[0] // 2
        frame_centery = FRAME_SIZE[1] // 2

        # Center the title slightly higher
        self.titlerect.center = (frame_centerx, frame_centery - 100)

        # Buttons evenly spaced below the title
        button_width, button_height, spacing = 180, 50, 70

        self.restart = self.Button(frame_centerx, frame_centery - spacing, button_width, button_height, "Restart","yellow")
        self.new_game = self.Button(frame_centerx, frame_centery, button_width, button_height, "New Game", "orange")
        self.exit = self.Button(frame_centerx, frame_centery + spacing, button_width, button_height, "Exit", "red")

    def draw(self, screen):
        screen.blit(self.titledisplay, self.titlerect)

        self.restart.draw(screen)
        self.new_game.draw(screen)
        self.exit.draw(screen)

    def is_mouse_in_button(self):
        return self.restart.is_mouse_in_button(), self.new_game.is_mouse_in_button(), self.exit.is_mouse_in_button()
