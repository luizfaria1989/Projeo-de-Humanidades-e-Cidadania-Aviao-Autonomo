# start_screen.py
import pygame
from PIL import Image, ImageFilter
from start_button import StartButton

pygame.font.init()

button_font = pygame.font.Font('assets/Orbitron/Orbitron-VariableFont_wght.ttf', 30)
title_font = pygame.font.Font('assets/Orbitron/Orbitron-VariableFont_wght.ttf', 50)
author_font = pygame.font.Font('assets/Orbitron/Orbitron-VariableFont_wght.ttf', 15)

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (255, 255, 0)

button_color = (235, 81, 0)
button_hover_color = (50, 54, 75)

class StartScreen:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont(None, 48)
        self.button_rect = pygame.Rect(screen.get_width() // 2 - 100, screen.get_height() // 2 - 25, 200, 50)
        # Carregar e aplicar efeito de vidro na imagem de fundo
        self.background = self.load_blurred_background('assets/start_background.png', (screen.get_width(), screen.get_height()))
        self.button_width = 285  # Largura do botão
        self.button_height = 50  # Altura do botão
        self.button_rect = pygame.Rect(screen.get_width() // 2 - self.button_width // 2,
                                       screen.get_height() // 2 - self.button_height // 2,
                                       self.button_width, self.button_height)
        self.start_button = StartButton(
            screen, self.button_rect, "Iniciar Simulador", button_font, BLACK, button_color, hover_color=button_hover_color, border_radius=10)

    def load_blurred_background(self, image_path, size):
        # Carregar imagem com Pillow
        image = Image.open(image_path)
        # Redimensionar para o tamanho desejado
        image = image.resize(size)
        # Aplicar filtro de desfoque
        blurred_image = image.filter(ImageFilter.GaussianBlur(radius=3))
        # Converter para formato Pygame
        pygame_image = self.pil_image_to_pygame(blurred_image)
        return pygame_image

    def pil_image_to_pygame(self, image):
        # Converter imagem do PIL para formato Pygame
        image_bytes = image.tobytes()
        image_size = image.size
        mode = image.mode
        return pygame.image.fromstring(image_bytes, image_size, mode)

    def draw(self):
        # Desenhar imagem de fundo
        self.screen.blit(self.background, (0, 0))

        # Desenhar título
        title_text = title_font.render("Simulador de Avião Autônomo", True, WHITE)
        title_rect = title_text.get_rect(center=(self.screen.get_width() // 2, 100))
        self.screen.blit(title_text, title_rect)

        author_text = author_font.render("Feito por Luiz Guilherme Faria", True, WHITE)
        author_rect = author_text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() - 30))
        self.screen.blit(author_text, author_rect)

        # Desenhar botão de início
        self.start_button.draw()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Verifica se foi clicado com o botão esquerdo do mouse
                    if self.button_rect.collidepoint(event.pos):  # Verifica se o clique foi dentro do botão
                        return False  # Sai da tela de início

        # Atualizar estado do botão
        self.start_button.update()

        return True
