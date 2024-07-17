import pygame

class Background:
    def __init__(self, screen, image_paths):
        self.screen = screen
        self.create_large_background(image_paths)

    def create_large_background(self, image_paths):
        images = [pygame.image.load(path) for path in image_paths]
        image_width = self.screen.get_width()
        image_height = self.screen.get_height()

        for i in range(len(images)):
            images[i] = pygame.transform.scale(images[i], (image_width, image_height))

        self.large_background = pygame.Surface((image_width * 9, image_height * 3))

        order = [
            images[18], images[19], images[20], images[21], images[22], images[23], images[24], images[25], images[26],
            images[9], images[10], images[11], images[12], images[13], images[14], images[15], images[16], images[17],
            images[0], images[1], images[2], images[3], images[4], images[5], images[6], images[7], images[8]
        ]

        for i, img in enumerate(order):
            x = (i % 9) * image_width
            y = (i // 9) * image_height
            self.large_background.blit(img, (x, y))

    def draw(self, viewport_left, viewport_top):
        self.screen.blit(self.large_background, (-viewport_left, -viewport_top))

    def get_dimensions(self):
        return self.large_background.get_width(), self.large_background.get_height()
