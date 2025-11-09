import pygame

DEFAULT_FONT = pygame.font.match_font("Arial")
FRAME_SIZE = (510, 510)
WINDOW_SIZE = (510, 660)


def create_text_surface(text: str, font_name: str, size: int, aa = True, color = "black") -> pygame.Surface:
    font = pygame.font.Font(font_name, size)
    render = font.render(text, aa, color)
    return render, render.get_rect()