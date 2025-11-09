import pygame
from neuro_defaults import *

class Board:
    CELL_SIZE = 60
    GRID_SIZE = 8

    # -----------------------------
    # Inner Button class
    # -----------------------------
    class Button(pygame.Rect):
        def __init__(self, centerx, centery, w, h, text, color):
            super().__init__(0, 0, w, h)
            self.center = (centerx, centery)
            self.color = color
            self.text, self.text_rect = create_text_surface(text, DEFAULT_FONT, 20)
            self.text_rect.center = self.center

        def draw(self, screen):
            # keep text centered if button moves
            self.text_rect.center = self.center
            pygame.draw.rect(screen, self.color, self)
            pygame.draw.rect(screen, "black", self, 2)
            screen.blit(self.text, self.text_rect)

        def is_mouse_in_button(self):
            return self.collidepoint(pygame.mouse.get_pos())

    # -----------------------------
    # Main Board class
    # -----------------------------
    def __init__(self, screen, layout_name):
        self.screen = screen
        self.width = self.height = self.GRID_SIZE
        self.layout_name = layout_name

        # Grid state: False = empty, True = X
        self.grid = [[False for _ in range(self.width)] for _ in range(self.height)]

        # Fonts
        self.font = pygame.font.Font(pygame.font.match_font(DEFAULT_FONT), 36)
        self.timer_font = pygame.font.Font(pygame.font.match_font(DEFAULT_FONT), 28)

        #  Load sounds for each cell
        self.sound_map = self.load_sounds()


        # Buttons (positions adjusted later in draw)
        self.clear_button = self.Button(WINDOW_SIZE[0] // 3, WINDOW_SIZE[1] - 60, 140, 45, "Clear Board", "yellow")
        self.menu_button = self.Button(WINDOW_SIZE[0] * 2 // 3, WINDOW_SIZE[1] - 60, 140, 45, "Back to Menu", "orange")

        # Timer
        self.start_time = pygame.time.get_ticks()

    def load_sounds(self):
        """Define a sound file for each cell (8x8)."""
        sounds = []

        # Define file names for each row — make this however you like!
        # Example: alternating tones for variety
        audio_layouts = {
            "Layout 1": [
                ["Hz400.wav", "click2.wav", "click3.wav", "click4.wav", "click1.wav", "click2.wav",
                 "click3.wav", "click4.wav"],
                ["click2.wav", "click3.wav", "click4.wav", "click1.wav", "click2.wav", "click3.wav", "click4.wav",
                 "click1.wav"],
            ],

            "Layout 2": [
                ["click3.wav", "click4.wav", "click1.wav", "click2.wav", "click3.wav", "click4.wav", "click1.wav",
                 "click2.wav"],
                ["click4.wav", "click1.wav", "click2.wav", "click3.wav", "click4.wav", "click1.wav", "click2.wav",
                 "click3.wav"],
            ],

            "Layout 3": [
                ["click3.wav", "click4.wav", "click1.wav", "click2.wav", "click3.wav", "click4.wav", "click1.wav",
                 "click2.wav"],
                ["click4.wav", "click1.wav", "click2.wav", "click3.wav", "click4.wav", "click1.wav", "click2.wav",
                 "click3.wav"],
            ],
            # add as many layouts as you want
        }
        sound_files = audio_layouts[self.layout_name]
        # Load each file (handle missing files gracefully)
        for row_files in sound_files:
            row = []
            for filename in row_files:
                try:
                    row.append(pygame.mixer.Sound(filename))
                except Exception:
                    row.append(None)  # fallback if missing
            sounds.append(row)

        return sounds

    # -----------------------------
    # Draw board, buttons, timer
    # -----------------------------
    def draw(self):
        board_size = self.CELL_SIZE * self.GRID_SIZE
        board_x = (WINDOW_SIZE[0] - board_size) // 2
        board_y = 60  # space for timer

        # Draw grid and X's
        for y in range(self.height):
            for x in range(self.width):
                rect = pygame.Rect(
                    board_x + x * self.CELL_SIZE,
                    board_y + y * self.CELL_SIZE,
                    self.CELL_SIZE,
                    self.CELL_SIZE
                )
                pygame.draw.rect(self.screen, "black", rect, 1)

                if self.grid[y][x]:
                    text_surface = self.font.render("X", True, "red")
                    text_rect = text_surface.get_rect(center=rect.center)
                    self.screen.blit(text_surface, text_rect)

        # Draw buttons (centered below board)
        button_y = board_y + board_size + 40
        self.clear_button.center = (WINDOW_SIZE[0] // 3, button_y)
        self.menu_button.center = (WINDOW_SIZE[0] * 2 // 3, button_y)
        self.clear_button.draw(self.screen)
        self.menu_button.draw(self.screen)

        # Draw timer (centered above board)
        elapsed_time = (pygame.time.get_ticks() - self.start_time) // 1000
        minutes = elapsed_time // 60
        seconds = elapsed_time % 60
        timer_text = f"{minutes:02}:{seconds:02}"
        timer_surface = self.timer_font.render(timer_text, True, "black")
        timer_rect = timer_surface.get_rect(center=(WINDOW_SIZE[0] // 2, 20))
        self.screen.blit(timer_surface, timer_rect)

    # -----------------------------
    # Handle clicks
    # -----------------------------
    def handle_click(self, pos):
        x, y = pos
        board_size = self.CELL_SIZE * self.GRID_SIZE
        board_x = (WINDOW_SIZE[0] - board_size) // 2
        board_y = 50  # same offset as in draw()

        # Click inside board
        if board_x <= x < board_x + board_size and board_y <= y < board_y + board_size:
            col = (x - board_x) // self.CELL_SIZE
            row = (y - board_y) // self.CELL_SIZE
            self.grid[row][col] = not self.grid[row][col]

            #  Play per-cell sound if available
            sound = self.sound_map[row][col]
            if sound:
                try:
                    sound.play()
                except Exception:
                    pass

    # -----------------------------
    # Button state checks
    # -----------------------------
    def is_mouse_in_button(self):
        return (
            self.clear_button.is_mouse_in_button(),
            self.menu_button.is_mouse_in_button()
        )

    # -----------------------------
    # Clear grid
    # -----------------------------
    def clear(self):
        # Reset all cells
        for r in range(self.height):
            for c in range(self.width):
                self.grid[r][c] = False

        #  Reset timer
        self.start_time = pygame.time.get_ticks()


