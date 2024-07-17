import pygame
import numpy as np

from airplane import Airplane
from background import Background
from statistics_display import StatisticsDisplay
from waypoint_manager import WaypointManager
from ui_manager import UIManager
from button import Button

class GameV2:
    def __init__(self, screen):
        self.screen = screen
        self.paused = True
        self.clock = pygame.time.Clock()

        image_paths = [
            'assets/aeroporto_comeco.png',
            'assets/praia_comeco.png',
            'assets/oceano.png',
            'assets/oceano.png',
            'assets/oceano.png',
            'assets/oceano.png',
            'assets/oceano.png',
            'assets/praia_chegada.png',
            'assets/aeroporto_chegada.png',
            'assets/ceu_azul.png',
            'assets/ceu_azul.png',
            'assets/ceu_azul.png',
            'assets/ceu_azul.png',
            'assets/ceu_azul.png',
            'assets/ceu_azul.png',
            'assets/ceu_azul.png',
            'assets/ceu_azul.png',
            'assets/ceu_azul.png',
            'assets/ceu_azul.png',
            'assets/ceu_azul.png',
            'assets/ceu_azul.png',
            'assets/ceu_azul.png',
            'assets/ceu_azul.png',
            'assets/ceu_azul.png',
            'assets/ceu_azul.png',
            'assets/ceu_azul.png',
            'assets/ceu_azul.png',
        ]

        self.create_large_background(image_paths)

        # Definir pontos de partida e chegada
        self.start_point = np.array([300, (screen.get_height() * 3 // 2) + 1100])
        self.end_point = np.array([11000, (screen.get_height() * 3 // 2) + 1100])

        # Inicializar o avião na posição inicial sobre o aeroporto
        self.airplane = Airplane([300, (screen.get_height() * 3 // 2) + 1050], 10, 0)

        # Fonte para o texto das estatísticas
        self.font = pygame.font.Font('assets/Exo_2/Exo2-VariableFont_wght.ttf', 24)
        self.font_bold_large = pygame.font.Font('assets/Exo_2/static/Exo2-SemiBold.ttf', 36)

        # Carregar a imagem do avião (baleia) e a versão espelhada
        self.plane_img = pygame.image.load('assets/baleia.png')
        self.plane_img = pygame.transform.scale(self.plane_img, (130, 100))
        self.plane_img_flipped = pygame.transform.flip(self.plane_img, True, False)

        # Estado da direção
        self.direction = 'right'  # Inicialmente, o avião está voltado para a direita

        self.pause_button = Button(screen, 'Pausado', (10, screen.get_height() - 40), self.font)
        self.exit_button = Button(screen, 'Sair', (100, screen.get_height() - 40), self.font)

        # Definir pontos de controle
        self.pontos_de_controle = []

        # Coordenadas iniciais
        start_x = 300
        start_y = (self.screen.get_height() * 3 // 2) + 1100

        # Coordenadas finais
        end_x = 14200
        end_y = (self.screen.get_height() * 3 // 2) + 1100

        # Altura estável no céu
        altitude_estavel = (self.screen.get_height() // 2 + 500)

        # Número total de pontos por fase
        num_pontos_subida = 15
        num_pontos_nivelado = 40
        num_pontos_descida = 15

        # Gerar pontos de subida
        for i in range(num_pontos_subida):
            x = start_x + (i * ((end_x - start_x) // (num_pontos_subida + num_pontos_nivelado + num_pontos_descida)))
            y = start_y - (i * ((start_y - altitude_estavel) // num_pontos_subida))
            self.pontos_de_controle.append([x, y])

        # Gerar pontos nivelados
        for i in range(num_pontos_nivelado):
            x = start_x + (num_pontos_subida * ((end_x - start_x) // (num_pontos_subida + num_pontos_nivelado + num_pontos_descida))) + (
                i * ((end_x - start_x) // (num_pontos_subida + num_pontos_nivelado + num_pontos_descida)))
            y = altitude_estavel
            self.pontos_de_controle.append([x, y])

        # Gerar pontos de descida
        for i in range(num_pontos_descida):
            x = start_x + ((num_pontos_subida + num_pontos_nivelado) * ((end_x - start_x) // (num_pontos_subida + num_pontos_nivelado + num_pontos_descida))) + (
                i * ((end_x - start_x) // (num_pontos_subida + num_pontos_nivelado + num_pontos_descida)))
            y = altitude_estavel + (i * ((end_y - altitude_estavel) // num_pontos_descida))
            self.pontos_de_controle.append([x, y])

        # Adicionar ponto final exato (pouso)
        self.pontos_de_controle.append([end_x, end_y])

        self.current_waypoint_index = 0

        # Variável para controlar o tempo sem pressionar teclas
        self.time_without_keys = 0
        self.time_without_keys_threshold = 5  # 5 segundos
        self.base_velocity = 60  # Velocidade base (decolagem)
        self.base_velocity_no_ceu = 100
        self.cruising_velocity = 180  # Velocidade de cruzeiro (céu)
        self.landing_velocity = 60  # Velocidade de pouso

        print(f"Altura do large_background: {self.large_background.get_height()} pixels")
        print(f"Largura do large_background: {self.large_background.get_width()} pixels")

    def create_large_background(self, image_paths):
        images = [pygame.image.load(path) for path in image_paths]
        image_width = self.screen.get_width()
        image_height = self.screen.get_height()

        for i in range(len(images)):
            images[i] = pygame.transform.scale(images[i], (image_width, image_height))

        # Crie uma superfície grande para a imagem combinada
        self.large_background = pygame.Surface((image_width * 9, image_height * 3))

        # Ordem correta das imagens
        order = [
            images[18], images[19], images[20], images[21], images[22], images[23], images[24], images[25], images[26],  # Linha superior 2 (ceu de novo)
            images[9], images[10], images[11], images[12], images[13], images[14], images[15], images[16], images[17],  # Linha superior (céu)
            images[0], images[1], images[2], images[3], images[4], images[5], images[6], images[7], images[8]  # Linha inferior (terra)
        ]

        # Blit as imagens na superfície grande
        for i, img in enumerate(order):
            x = (i % 9) * image_width
            y = (i // 9) * image_height
            self.large_background.blit(img, (x, y))

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    self.paused = not self.paused
                elif event.key == pygame.K_e:
                    return False
                else:
                    self.time_without_keys = 0  # Reiniciar contagem se alguma tecla for pressionada

        keys = pygame.key.get_pressed()
        if not self.paused:
            # Contar o tempo sem pressionar teclas
            if all(not keys[key] for key in [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_SPACE]):
                self.time_without_keys += self.clock.get_time() / 1000.0

            # Verificar se passou o tempo sem pressionar teclas suficiente
            if self.time_without_keys >= self.time_without_keys_threshold:
                self.navigate_to_waypoint()
            else:
                # Controles manuais
                if keys[pygame.K_UP]:
                    self.airplane.change_angle(-0.1)
                if keys[pygame.K_DOWN]:
                    self.airplane.change_angle(0.1)
                if keys[pygame.K_LEFT]:
                    self.airplane.velocity -= 0.1
                    self.direction = 'left'
                if keys[pygame.K_RIGHT]:
                    self.airplane.velocity += 0.1
                    self.direction = 'right'
                if keys[pygame.K_SPACE]:
                    self.airplane.velocity += 1.0

        return True

    def update(self):
        if not self.paused:
            # Verificar se estamos na fase de decolagem, cruzeiro ou pouso
            if self.airplane.position[1] > (self.screen.get_height() * 3 // 2):  # Fase de decolagem
                self.airplane.velocity = self.base_velocity
            elif (self.screen.get_height() // 2) <= self.airplane.position[1] <= (self.screen.get_height() * 3 // 2):  # Fase de cruzeiro
                self.airplane.velocity = self.cruising_velocity
            elif self.airplane.position[1] < (self.screen.get_height() // 2):  # Fase de pouso
                self.airplane.velocity = self.landing_velocity

            # Atualizar posição do avião
            self.airplane.update_position()

            # Atualizar waypoint atual, se necessário
            if self.current_waypoint_index < len(self.pontos_de_controle):
                current_waypoint = self.pontos_de_controle[self.current_waypoint_index]
                distance_to_waypoint = np.linalg.norm(self.airplane.position - current_waypoint)
                if distance_to_waypoint < 100:
                    self.current_waypoint_index += 1

            # Desenhar o fundo
            self.screen.blit(self.large_background, (0, 0), area=pygame.Rect(self.airplane.position[0] - self.screen.get_width() // 2,
                                                                             self.airplane.position[1] - self.screen.get_height() // 2,
                                                                             self.screen.get_width(),
                                                                             self.screen.get_height()))

            # Desenhar o avião
            rotated_image = pygame.transform.rotate(self.plane_img_flipped if self.direction == 'left' else self.plane_img, -self.airplane.angle)
            self.screen.blit(rotated_image, self.airplane.position)

            # Exibir estatísticas na tela
            velocity_text = self.font.render(f"Velocidade: {self.airplane.velocity:.2f}", True, (255, 255, 255))
            self.screen.blit(velocity_text, (10, 10))
            altitude_text = self.font.render(f"Altitude: {self.airplane.position[1]:.2f}", True, (255, 255, 255))
            self.screen.blit(altitude_text, (10, 40))
            direction_text = self.font.render(f"Direção: {'Esquerda' if self.direction == 'left' else 'Direita'}", True, (255, 255, 255))
            self.screen.blit(direction_text, (10, 70))

            # Desenhar os botões
            self.pause_button.draw()
            self.exit_button.draw()

    def navigate_to_waypoint(self):
        if self.current_waypoint_index < len(self.pontos_de_controle):
            current_waypoint = self.pontos_de_controle[self.current_waypoint_index]
            direction_vector = current_waypoint - self.airplane.position
            distance_to_waypoint = np.linalg.norm(direction_vector)
            normalized_direction = direction_vector / distance_to_waypoint

            self.airplane.position += normalized_direction * self.airplane.velocity * self.clock.get_time() / 1000.0

    def run(self):
        while self.handle_events():
            self.update()
            pygame.display.flip()
            self.clock.tick(60)
