import pygame


class Brick(pygame.sprite.Sprite):
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GREY = (200, 200, 200)
    RED = (255, 0, 0)
    BLUE = (0, 0, 255)
    GREEN = (0, 255, 0)

    size = 10
    position_x, position_y = 0, 0
    previous_position_x, previous_position_y = 0, 0

    def __init__(self, size: int):
        super().__init__()
        self.size_ = size
        self.image = pygame.Surface((size, size))
        self.image.fill(self.WHITE)
        self.rect = self.image.get_rect()

    def draw(self, window):
        window.blit(self.image, self.rect)

    def fill(self, colour):
        self.image.fill(Brick.BLACK)
        self.image.fill(colour, self.image.get_rect().inflate(-1, -1))
        # self.image.fill(colour)

    def set_position(self, position_x: int, position_y: int):
        self.position_x, self.position_y = position_x, position_y
        self.rect.x, self.rect.y = position_x, position_y

    def get_position(self):
        return self.position_x, self.position_y

    def set_previous_position(self, position_x: int, position_y: int):
        self.previous_position_x, self.previous_position_y = position_x, position_y
