import numpy as np
import pygame

class StatisticsDisplay:
    def __init__(self, screen, airplane, end_point):
        self.screen = screen
        self.airplane = airplane
        self.end_point = end_point
        self.font = pygame.font.Font('assets/Exo_2/Exo2-VariableFont_wght.ttf', 24)
        self.font_bold_large = pygame.font.SysFont('assets/Exo_2/static/Exo2-SemiBold.tff', 36)

    def draw(self):
        altitude = self.screen.get_height() * 3 - self.airplane.get_position()[1]
        angulo_real = -(np.degrees(self.airplane.get_angle()))
        distance_to_end = np.linalg.norm(self.airplane.get_position() - self.end_point)

        text_staticts_menu_1 = self.font_bold_large.render(f'Estatísticas da', True, (0, 0, 0))
        text_staticts_menu_2 = self.font_bold_large.render(f'aeronave', True, (0, 0, 0))
        text_velocity = self.font_bold_large.render(f'Velocidade: ', True, (0, 0, 0))
        text_velocity_value = self.font.render(f'{self.airplane.get_velocity():.1f} m/s', True, (0, 0, 0))
        text_altitude = self.font_bold_large.render(f'Altitude: ', True, (0, 0, 0))
        text_altitude_value = self.font.render(f'{(altitude / 10): .1f} m', True, (0, 0, 0))
        text_angle = self.font_bold_large.render(f'Ângulo:', True, (0, 0, 0))
        text_angle_value = self.font.render(f'{angulo_real: .1f} graus', True, (0, 0, 0))
        text_distance_parte_1 = self.font_bold_large.render(f'Distância até', True, (0, 0, 0))
        text_distance_parte_2 = self.font_bold_large.render(f'o destino:', True, (0, 0, 0))
        text_distance_to_end_value = self.font.render(f'{distance_to_end:.1f} pixels', True, (0, 0, 0))

        if self.airplane.get_velocity() > 0:
            time_to_end = distance_to_end / self.airplane.get_velocity()
            text_time_to_end = self.font_bold_large.render(f'Tempo restante:', True, (0, 0, 0))
            text_time_to_end_value = self.font.render(f'{time_to_end:.1f} segundos', True, (0, 0, 0))
        else:
            text_time_to_end = self.font_bold_large.render(f'Tempo restante:', True, (255, 0, 0))
            text_time_to_end_value = self.font.render(f'Indefinido', True, (0, 0, 0))

        line_spacing_conteudo_diferente = 38
        y_start = 10
        line_spacing_mesmo_conteudo = 25
        line_spacing = line_spacing_conteudo_diferente

        self.screen.blit(text_staticts_menu_1, (10, y_start))
        self.screen.blit(text_staticts_menu_2, (10, line_spacing_mesmo_conteudo + 5))
        y_offset = y_start + line_spacing * 2
        self.screen.blit(text_velocity, (10, y_offset))
        self.screen.blit(text_velocity_value, (10, y_offset + line_spacing_mesmo_conteudo))

        y_offset += line_spacing * 2
        self.screen.blit(text_altitude, (10, y_offset))
        self.screen.blit(text_altitude_value, (10, y_offset + line_spacing_mesmo_conteudo))

        y_offset += line_spacing * 2
        self.screen.blit(text_angle, (10, y_offset))
        self.screen.blit(text_angle_value, (10, y_offset + line_spacing_mesmo_conteudo))

        y_offset += line_spacing * 2
        self.screen.blit(text_distance_parte_1, (10, y_offset))
        self.screen.blit(text_distance_parte_2, (10, y_offset + line_spacing_mesmo_conteudo))
        self.screen.blit(text_distance_to_end_value, (10, y_offset + line_spacing_mesmo_conteudo * 2))

        y_offset += line_spacing * 3
        self.screen.blit(text_time_to_end, (10, y_offset))
        self.screen.blit(text_time_to_end_value, (10, y_offset + line_spacing_mesmo_conteudo))
