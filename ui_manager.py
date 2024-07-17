import pygame
from button import Button

class UIManager:
    def __init__(self, screen):
        self.screen = screen
        self.start_button = self.create_button('Start', 'assets/Exo_2/static/Exo2-SemiBold.tff', 150, 50, 200, 200, 'white')
        self.settings_button = self.create_button('Settings', 'assets/Exo_2/static/Exo2-SemiBold.tff', 150, 50, 200, 270, 'white')
        self.exit_button = self.create_button('Exit', 'assets/Exo_2/static/Exo2-SemiBold.tff', 150, 50, 200, 340, 'white')

    def create_button(self, text, font, width, height, x, y, color):
        button_font = pygame.font.Font(font, 24)
        button = Button(image=pygame.Surface((width, height)), pos=(x, y),
                        text_input=text, font=button_font, base_color='black', hovering_color=color)
        return button

    def draw_buttons(self, mouse_pos):
        for button in [self.start_button, self.settings_button, self.exit_button]:
            button.change_color(mouse_pos)
            button.update(self.screen)
