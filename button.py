import pygame

class Button:
    def __init__(self, screen, text, position, font_path, font_size, size=(80, 30)):
        self.screen = screen
        self.text = text
        self.position = position
        self.font_path = font_path
        self.font_size = font_size
        self.size = size
        self.font = pygame.font.Font(font_path, font_size)

    def draw(self):
        pygame.draw.rect(self.screen, (255, 255, 255), pygame.Rect(self.position, self.size))
        pygame.draw.rect(self.screen, (0, 0, 0), pygame.Rect(self.position, self.size), 2)

        text_surface = self.font.render(self.text, True, (0, 0, 0))

        # Calcular a posição do texto para centralizá-lo no botão
        text_rect = text_surface.get_rect(
            center=(self.position[0] + self.size[0] // 2, self.position[1] + self.size[1] // 2))

        self.screen.blit(text_surface, (self.position[0] + 5, self.position[1] + 5))

    def set_font_size(self, new_size):
        self.font_size = new_size
        self.font = pygame.font.Font(self.font_path, new_size)

    def set_text(self, new_text):
        self.text = new_text

