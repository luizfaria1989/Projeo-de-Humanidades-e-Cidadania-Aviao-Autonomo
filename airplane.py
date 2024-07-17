import numpy as np


class Airplane:

    def __init__(self, position, velocity, angle):
        self.position = np.array(position, dtype=float)
        self.velocity = velocity
        self.angle = angle

    def update_position(self, time_step):
        self.position[0] += self.velocity * np.cos(self.angle) * time_step
        self.position[1] += self.velocity * np.sin(self.angle) * time_step

    def change_angle(self, delta_angle):
        self.angle += delta_angle

    def update_physics(self, time_step):
        self.update_position(time_step)

    def get_position(self):
        return self.position

    def get_angle(self):
        return self.angle

    def set_angle(self, angle):
        self.angle = angle
    def get_velocity(self):
        return self.velocity

    def set_velocity(self, velocity):
        self.velocity = velocity


