import pygame
from neuro_board2 import Board
from neuro_title import Title
from neuro_defaults import *

def main():
    pygame.init()
    pygame.mixer.init()

    pygame.display.set_caption("Neuro Grid")
    screen = pygame.display.set_mode(WINDOW_SIZE)

    title_screen = Title(pygame.font.match_font(DEFAULT_FONT))
    board = None
    state = "MENU"
    running = True

    while running:
        screen.fill("white")

        if state == "MENU":
            title_screen.draw(screen)

        elif state == "BOARD":
            board.draw()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if state == "MENU":
                    start_game = title_screen.handle_click(event.pos)
                    if start_game:
                        # Pass selected layout to Board
                        board = Board(screen, layout_name = title_screen.selected_layout)
                        state = "BOARD"

                elif state == "BOARD":
                    buttons = board.is_mouse_in_button()
                    if buttons[0]:   # Clear
                        board.clear()
                    elif buttons[1]: # Back to menu
                        state = "MENU"
                    else:
                        board.handle_click(event.pos)

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
