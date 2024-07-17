import numpy as np
import pygame

class WaypointManager:
    def __init__(self, start_point, end_point, screen_height):
        self.start_point = start_point
        self.end_point = end_point
        self.screen_height = screen_height
        self.pontos_de_controle = self.generate_waypoints()

    def generate_waypoints(self):
        waypoints = []
        start_x, start_y = self.start_point
        end_x, end_y = self.end_point
        altitude_estavel = (self.screen_height // 2 + 500)

        num_pontos_subida = 15
        num_pontos_nivelado = 40
        num_pontos_descida = 15

        for i in range(num_pontos_subida):
            x = start_x + (i * ((end_x - start_x) // (num_pontos_subida + num_pontos_nivelado + num_pontos_descida)))
            y = start_y - (i * ((start_y - altitude_estavel) // num_pontos_subida))
            waypoints.append([x, y])

        for i in range(num_pontos_nivelado):
            x = start_x + (num_pontos_subida * (
                        (end_x - start_x) // (num_pontos_subida + num_pontos_nivelado + num_pontos_descida))) + (
                            i * ((end_x - start_x) // (num_pontos_subida + num_pontos_nivelado + num_pontos_descida)))
            y = altitude_estavel
            waypoints.append([x, y])

        for i in range(num_pontos_descida):
            x = start_x + ((num_pontos_subida + num_pontos_nivelado) * (
                        (end_x - start_x) // (num_pontos_subida + num_pontos_nivelado + num_pontos_descida))) + (
                            i * ((end_x - start_x) // (num_pontos_subida + num_pontos_nivelado + num_pontos_descida)))
            y = altitude_estavel + (i * ((end_y - altitude_estavel) // num_pontos_descida))
            waypoints.append([x, y])

        waypoints.append([end_x, end_y])
        return waypoints

    def draw(self, screen, viewport_left, viewport_top):
        for ponto in self.pontos_de_controle:
            pygame.draw.circle(screen, (255, 0, 0), (ponto[0] - viewport_left, ponto[1] - viewport_top), 5)
