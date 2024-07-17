import pygame
import numpy as np

from airplane import Airplane
from button import Button

BRANCO = (255, 255, 255)
ROYAL_BLUE = (17, 30, 108)

def draw_rounded_rect(surface, color, rect, corner_radius):
    """
    Draw a rectangle with rounded corners.
    """
    rect = pygame.Rect(rect)
    corner_radius = min(corner_radius, rect.width // 2, rect.height // 2)

    # Create the rounded corners
    corner_rect = pygame.Surface((corner_radius * 2, corner_radius * 2), pygame.SRCALPHA)
    pygame.draw.ellipse(corner_rect, color, corner_rect.get_rect())

    # Blit the corners
    surface.blit(corner_rect, (rect.left, rect.top))
    surface.blit(corner_rect, (rect.right - corner_radius * 2, rect.top))
    surface.blit(corner_rect, (rect.left, rect.bottom - corner_radius * 2))
    surface.blit(corner_rect, (rect.right - corner_radius * 2, rect.bottom - corner_radius * 2))

    # Draw the rectangles
    pygame.draw.rect(surface, color, (rect.left + corner_radius, rect.top, rect.width - corner_radius * 2, rect.height))
    pygame.draw.rect(surface, color, (rect.left, rect.top + corner_radius, rect.width, rect.height - corner_radius * 2))


class Game:
    def __init__(self, screen):
        self.screen = screen
        self.paused = True
        self.clock = pygame.time.Clock()

        image_paths = [
            'assets/aeroporto_comeco_V2.png', # numero 1
            'assets/praia_comeco_V2.png', # numero 2
            'assets/oceano_V2.png', # numero 3
            'assets/oceano_V2.png', # numero 4
            'assets/oceano_V2.png', # numero 5
            'assets/oceano_V2.png', # numero 6
            'assets/oceano_V2.png', # numero 7
            'assets/praia_chegada_V2.png', # numero 8
            'assets/aeroporto_chegada_V2.png', # numero 9


            'assets/ceu_azul_v2.png', # numero 1
            'assets/ceu_azul_v2.png', # numero 2
            'assets/ceu_azul_v2.png', # numero 3
            'assets/ceu_azul_v2.png', # numero 4
            'assets/ceu_azul_v2.png', # numero 5
            'assets/ceu_azul_v2.png', # numero 6
            'assets/ceu_azul_v2.png', # numero 7
            'assets/ceu_azul_v2.png', # numero 8
            'assets/ceu_azul_v2.png', # numero 9


            'assets/ceu_maior_v2.png', # numero 1
            'assets/ceu_maior_v2.png', # numero 2
            'assets/ceu_maior_v2.png', # numero 3
            'assets/ceu_maior_v2.png', # numero 4
            'assets/ceu_maior_v2.png', # numero 5
            'assets/ceu_maior_v2.png', # numero 6
            'assets/ceu_maior_v2.png', # numero 7
            'assets/ceu_maior_v2.png', # numero 8
            'assets/ceu_maior_v2.png', # numero 9
        ]

        self.create_large_background(image_paths)

        # Definir pontos de partida e chegada
        self.start_point = np.array([300, (screen.get_height() * 3 // 2) + 1050])
        self.end_point = np.array([11000, (screen.get_height() * 3 // 2) + 1100])

        # Inicializar o avião na posição inicial sobre o aeroporto
        self.airplane = Airplane([300, (screen.get_height() * 3 // 2) + 1050], 10, 0)

        # Fonte para o texto das estatísticas
        self.font = pygame.font.Font('assets/Exo_2/Exo2-VariableFont_wght.ttf', 24)
        self.font_bold_large = pygame.font.SysFont('assets/Exo_2/static/Exo2-SemiBold.tff', 36)

        # Carregar a imagem do avião (baleia) e a versão espelhada
        self.plane_img = pygame.image.load('assets/aviao_bem_feito_com_cauda.png')
        self.plane_img = pygame.transform.scale(self.plane_img, (130, 100))
        self.plane_img_flipped = pygame.transform.flip(self.plane_img, True, False)

        # Estado da direção
        self.direction = 'right'  # Inicialmente, o avião está voltado para a direita

        self.pause_button = Button(screen, 'Pressione P para pausar', (15, screen.get_height() - 105),   'assets/Exo_2/Exo2-VariableFont_wght.ttf', 16, (185, 40))
        self.exit_button = Button(screen, 'Pressione S para sair', (15, screen.get_height() - 60),   'assets/Exo_2/Exo2-VariableFont_wght.ttf', 17, (185, 40))

        # Definir pontos de controle
        self.pontos_de_controle = []

        # Coordenadas iniciais
        start_x = 300
        start_y = (screen.get_height() * 3 // 2) + 1050

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
            x = start_x + (num_pontos_subida * (
                        (end_x - start_x) // (num_pontos_subida + num_pontos_nivelado + num_pontos_descida))) + (
                            i * ((end_x - start_x) // (num_pontos_subida + num_pontos_nivelado + num_pontos_descida)))
            y = altitude_estavel
            self.pontos_de_controle.append([x, y])

        # Gerar pontos de descida
        for i in range(num_pontos_descida):
            x = start_x + ((num_pontos_subida + num_pontos_nivelado) * (
                        (end_x - start_x) // (num_pontos_subida + num_pontos_nivelado + num_pontos_descida))) + (
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
            images[0], images[1], images[2], images[3], images[4], images[5], images[6], images[7], images[8]   # Linha inferior (terra)
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
                elif event.key == pygame.K_a:
                    self.time_without_keys = 10
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
                    self.airplane.change_angle(-0.05)
                if keys[pygame.K_DOWN]:
                    self.airplane.change_angle(0.05)
                if keys[pygame.K_LEFT]:
                    self.airplane.velocity -= 0.5
                    self.direction = 'left'
                if keys[pygame.K_RIGHT]:
                    self.airplane.velocity += 0.5
                    self.direction = 'right'
                if keys[pygame.K_SPACE]:
                    self.airplane.velocity += 1.0

        return True

    def navigate_to_waypoint(self):
        if self.current_waypoint_index < len(self.pontos_de_controle):
            current_position = np.array(self.airplane.get_position())

            # Encontrar o ponto mais próximo
            closest_point = min(self.pontos_de_controle[self.current_waypoint_index:],
                                key=lambda point: np.linalg.norm(np.array(point) - current_position))

            # Calcular vetor de direção para o ponto mais próximo
            direction_vector = np.array(closest_point) - current_position
            distance = np.linalg.norm(direction_vector)

            # Se estiver perto o suficiente do ponto de controle, passe para o próximo
            if distance < 10:  # Threshold de distância
                self.current_waypoint_index = self.pontos_de_controle.index(closest_point) + 1
            else:
                # Normalizar o vetor de direção
                direction_vector = direction_vector / distance

                # Calcular o ângulo desejado para o ponto mais próximo
                target_angle = np.arctan2(direction_vector[1], direction_vector[0])
                current_angle = self.airplane.get_angle()

                # Ajustar o ângulo de forma suave
                delta_angle = target_angle - current_angle
                if delta_angle > np.pi:
                    delta_angle -= 2 * np.pi
                elif delta_angle < -np.pi:
                    delta_angle += 2 * np.pi

                max_angle_change = np.pi / 30  # Máxima mudança de ângulo permitida por frame
                if delta_angle > max_angle_change:
                    delta_angle = max_angle_change
                elif delta_angle < -max_angle_change:
                    delta_angle = -max_angle_change

                new_angle = current_angle + delta_angle
                self.airplane.set_angle(new_angle)

                # Ajustar velocidade de acordo com a fase de voo
                if self.current_waypoint_index < 20:  # Decolagem
                    target_speed = self.base_velocity
                elif self.current_waypoint_index < 40:  # Voo no céu
                    target_speed = self.cruising_velocity
                else:  # Pouso
                    target_speed = self.landing_velocity

                current_speed = self.airplane.get_velocity()
                if current_speed < target_speed:
                    self.airplane.set_velocity(min(target_speed, current_speed + 0.1))
                elif current_speed > target_speed:
                    self.airplane.set_velocity(max(target_speed, current_speed - 0.1))
    def update(self, dt):
        if not self.paused:
            self.airplane.update_physics(dt)  # Tempo de atualização fixo para física do avião


    def draw(self):
        # Calcular deslocamento da câmera para manter o avião centrado
        viewport_left = max(0, self.airplane.get_position()[0] - self.screen.get_width() // 2)
        viewport_top = max(0, self.airplane.get_position()[1] - self.screen.get_height() // 2)

        # Limitar a câmera para não ultrapassar os limites da grande imagem de fundo
        max_viewport_left = self.large_background.get_width() - self.screen.get_width()
        max_viewport_top = self.large_background.get_height() - self.screen.get_height()
        viewport_left = min(viewport_left, max_viewport_left)
        viewport_top = min(viewport_top, max_viewport_top)

        # Desenhar a imagem de fundo
        self.screen.blit(self.large_background, (-viewport_left, -viewport_top))

        # Desenhar a barra lateral esquerda
        sidebar_width = 220
        draw_rounded_rect(self.screen, BRANCO,
                          [0, 0, sidebar_width, self.screen.get_height()], 20)
        draw_rounded_rect(self.screen, ROYAL_BLUE,
                          [0 + 10, 10, sidebar_width - 20, self.screen.get_height() - 20],
                          15)

        # pygame.draw.rect(self.screen, ROYAL_BLUE, pygame.Rect(0, 0, 230, self.screen.get_height()))
        # pygame.draw.rect(self.screen, BRANCO, pygame.Rect(210, 0, 20, self.screen.get_height()))

        # Calcular a altitude em relação ao ponto mais baixo da tela
        altitude = self.large_background.get_height() - self.airplane.get_position()[1]

        angulo_real = - (np.degrees(self.airplane.get_angle()))

        # Exibir estatísticas na barra lateral
        text_staticts_menu_1 = self.font_bold_large.render(f'Estatísticas da', True, BRANCO)
        text_staticts_menu_2 = self.font_bold_large.render(f'aeronave', True, BRANCO)

        text_velocity = self.font_bold_large.render(f'Velocidade: ', True, BRANCO)
        text_velocity_value = self.font.render(f'{self.airplane.get_velocity():.1f} m/s', True, BRANCO)

        text_altitude = self.font_bold_large.render(f'Altitude: ', True, BRANCO)
        text_altitude_value = self.font.render(f'{(altitude / 10): .1f} m', True, BRANCO)

        text_angle = self.font_bold_large.render(f'Ângulo:', True, BRANCO)
        text_angle_value = self.font.render(f'{angulo_real: .1f} graus', True, BRANCO)

        distance_to_end = np.linalg.norm(self.airplane.get_position() - self.end_point)
        text_distance_parte_1 = self.font_bold_large.render(f'Distância até', True, BRANCO)
        text_distance_parte_2 = self.font_bold_large.render(f'o destino:', True, BRANCO)
        text_distance_to_end_value = self.font.render(f'{distance_to_end:.1f} pixels', True, BRANCO)


        if self.airplane.get_velocity() > 0:
            time_to_end = distance_to_end / self.airplane.get_velocity()
            text_time_to_end = self.font_bold_large.render(f'Tempo restante:', True, BRANCO)
            text_time_to_end_value = self.font.render(f'{time_to_end:.1f} segundos', True, BRANCO)
        else:
            text_time_to_end = self.font_bold_large.render(f'Tempo restante:', True, (255, 0, 0))
            text_time_to_end_value = self.font.render(f'Indefinido', True, BRANCO)

        # Estabelecer um padrão de deslocamento vertical para cada linha
        line_spacing_conteudo_diferente = 38
        y_start = 20
        x_start = 20
        line_spacing_mesmo_conteudo = 25


        line_spacing = line_spacing_conteudo_diferente

        # Desenhar cada linha de texto e valor correspondente
        self.screen.blit(text_staticts_menu_1, (x_start, y_start))
        self.screen.blit(text_staticts_menu_2, (x_start, line_spacing_mesmo_conteudo + 15))
        y_offset = y_start + line_spacing * 2
        self.screen.blit(text_velocity, (x_start, y_offset))
        self.screen.blit(text_velocity_value, (x_start, y_offset + line_spacing_mesmo_conteudo))

        y_offset += line_spacing * 2
        self.screen.blit(text_altitude, (x_start, y_offset))
        self.screen.blit(text_altitude_value, (x_start, y_offset + line_spacing_mesmo_conteudo))

        y_offset += line_spacing * 2
        self.screen.blit(text_angle, (x_start, y_offset))
        self.screen.blit(text_angle_value, (x_start, y_offset + line_spacing_mesmo_conteudo))

        y_offset += line_spacing * 2
        self.screen.blit(text_distance_parte_1, (x_start, y_offset))
        self.screen.blit(text_distance_parte_2, (x_start, y_offset + line_spacing_mesmo_conteudo))
        self.screen.blit(text_distance_to_end_value, (x_start, y_offset + line_spacing_mesmo_conteudo * 2))

        y_offset += line_spacing * 3
        self.screen.blit(text_time_to_end, (x_start, y_offset))
        self.screen.blit(text_time_to_end_value, (x_start, y_offset + line_spacing_mesmo_conteudo))



        # Desenhar botão de pausa
        self.pause_button.draw()
        # Desenhar botão de saída
        self.exit_button.draw()

        # Escolher a imagem do avião com base na direção
        if self.direction == 'left':
            plane_img = self.plane_img_flipped
        else:
            plane_img = self.plane_img

        # Desenhar o avião
        rotated_plane = pygame.transform.rotate(plane_img, np.degrees(-self.airplane.get_angle()))
        plane_rect = rotated_plane.get_rect(
            center=(self.airplane.get_position()[0] - viewport_left, self.airplane.get_position()[1] - viewport_top))
        self.screen.blit(rotated_plane, plane_rect)

        # Desenhar os pontos de controle
        for ponto in self.pontos_de_controle:
            pygame.draw.circle(self.screen, (255, 0, 0), (ponto[0] - viewport_left, ponto[1] - viewport_top), 5)

        # Rotacionar e desenhar a imagem do avião de acordo com a direção e ângulo atuais
        rotated_plane_img = pygame.transform.rotate(
            self.plane_img_flipped if self.direction == 'left' else self.plane_img,
            np.degrees(self.airplane.get_angle()))
        plane_rect = rotated_plane_img.get_rect(center=self.airplane.get_position())
        self.screen.blit(rotated_plane_img, plane_rect.topleft)

    def run(self):
        running = True
        while running:
            dt = self.clock.tick(30) / 1000.0

            running = self.handle_events()
            self.update(dt)
            self.draw()

            pygame.display.flip()

        pygame.quit()
