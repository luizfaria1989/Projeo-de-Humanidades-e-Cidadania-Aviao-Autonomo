import pygame
from start_screen import StartScreen
from game import Game

pygame.init()

screen_width, screen_height = 1600, 900
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Simulação de Avião Autônomo")

WHITE = (255, 255, 255)

# Criar tela de início
start_screen = StartScreen(screen)

# Loop da tela de início
running = True
while running:
    running = start_screen.handle_events()  # Lidar com eventos da tela de início

    start_screen.draw()  # Desenhar elementos na tela de início

    pygame.display.flip()  # Atualizar tela

# Inicializar e executar o jogo
game = Game(screen)
game.run()

pygame.quit()
