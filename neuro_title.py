import pygame
from neuro_defaults import *

class Title:
    class Button(pygame.Rect):
        def __init__(self, centerx, centery, w, h, text, color):
            super().__init__(0, 0, w, h)
            self.center = (centerx, centery)

            self.color = color
            self.textrender, self.textrect = create_text_surface(text, DEFAULT_FONT, 24)
            self.textrect.center = self.center


        def draw(self, screen):
            pygame.draw.rect(screen, self.color, self)
            screen.blit(self.textrender, self.textrect)

        def is_mouse_in_button(self): 
            return self.collidepoint(pygame.mouse.get_pos())

    def __init__(self, font_name):
        self.font = pygame.font.Font(font_name, 24)
        self.titledisplay, self.titlerect = create_text_surface("Neuro Game", font_name, 60)

        frame_centerx = FRAME_SIZE[0] / 2
        frame_centery = FRAME_SIZE[1] / 2

        self.titlerect.center = (frame_centerx, (frame_centery-15))

        self.start_button = self.Button(frame_centerx, (frame_centery + 90), 140, 50, "Play Game", "green")

        self.layout_options = ["Layout 1", "Layout 2", "Layout 3"]  # match keys in audio_layouts
        self.selected_layout = self.layout_options[0]

    def draw(self, screen):
        screen.blit(self.titledisplay, self.titlerect)
        self.start_button.draw(screen)

        for i, layout_name in enumerate(self.layout_options):
            rect = pygame.Rect(180, 400 + i * 50, 150, 40)
            color = "green" if layout_name == self.selected_layout else "lightgray"
            pygame.draw.rect(screen, color, rect)
            text_surf = self.font.render(layout_name, True, "black")
            screen.blit(text_surf, (rect.x + 45, rect.y + 5))

    def handle_click(self, pos):
        # Check layout selection
        for i, layout_name in enumerate(self.layout_options):
            rect = pygame.Rect(180, 400 + i * 50, 150, 40)
            if rect.collidepoint(pos):
                self.selected_layout = layout_name
                print(f"Selected layout: {self.selected_layout}")

        return self.start_button.collidepoint(pos)

    def is_mouse_in_button(self):
        return self.start_button.is_mouse_in_button()

