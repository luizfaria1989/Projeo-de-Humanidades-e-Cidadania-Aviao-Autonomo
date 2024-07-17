# start_screen.py
import pygame
pygame.font.init()

button_font = pygame.font.Font('assets/Orbitron/Orbitron-VariableFont_wght.ttf', 12)

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_GRAY = (200, 200, 200)
DARK_GRAY = (100, 100, 100)

class StartButton:
    def __init__(self, screen, rect, text, font, text_color, bg_color, hover_color=None, border_radius=0):
        self.screen = screen
        self.base_rect = rect
        self.rect = rect
        self.text = text
        self.font = font
        self.text_color = text_color
        self.bg_color = bg_color
        self.hover_color = hover_color if hover_color else bg_color
        self.border_radius = border_radius
        self.hovered = False

    def draw(self):
        # Desenhar botão com bordas arredondadas
        pygame.draw.rect(self.screen, self.hover_color if self.hovered else self.bg_color, self.rect, border_radius=self.border_radius)

        # Desenhar texto centralizado no botão
        text_surf = self.font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        self.screen.blit(text_surf, text_rect)

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            # Aumentar o tamanho do botão quando hover
            self.rect = self.base_rect.inflate(18, 18)  # Aumenta em 10 pixels em todas as direções
            self.hovered = True
            self.text_color = WHITE
        else:
            # Retorna ao tamanho original quando não hover
            self.rect = self.base_rect
            self.hovered = False
            self.text_color = BLACK