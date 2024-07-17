import pygame

class BackgroundManager:
    def __init__(self, screen, image_paths):
        self.screen = screen
        self.background_images = []
        for image_path in image_paths:
            image = pygame.image.load(image_path)
            image = pygame.transform.scale(image, (screen.get_width(), screen.get_height()))
            self.background_images.append(image)

    def draw(self, viewport_left, viewport_top):
        row = int(viewport_top // self.screen.get_height()) % len(self.background_images)
        col = int(viewport_left // self.screen.get_width()) % len(self.background_images[0])
        background = self.background_images[row][col]
        self.screen.blit(background, (-viewport_left % self.screen.get_width(), -viewport_top % self.screen.get_height()))