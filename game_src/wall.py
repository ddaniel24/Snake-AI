import pygame
from game_src.brick import Brick


class Wall(pygame.sprite.Group):
    bricks = []
    brick_size = 10
    (game_width, game_height) = (400, 400)

    def __init__(self, game_width: int, game_height: int, brick: Brick):
        super(Wall, self).__init__()
        self.brick_size = brick.size
        self.game_width, self.game_height = game_width, game_height
        self.bricks = []
        self.init_wall()

    def init_wall(self):
        for i in range(0, int(self.game_width / self.brick_size)):
            brick = Brick(self.brick_size)
            brick.set_position(i * self.brick_size, 0)
            self.add(brick)
            self.bricks.append(Brick)

        for i in range(0, int(self.game_height / self.brick_size)):
            brick = Brick(self.brick_size)
            brick.set_position(0, i * self.brick_size)
            self.add(brick)
            self.bricks.append(Brick)

        for i in range(0, int(self.game_width / self.brick_size)):
            brick = Brick(self.brick_size)
            brick.set_position(i * self.brick_size, self.game_height - self.brick_size)
            self.add(brick)
            self.bricks.append(Brick)

        for i in range(0, int(self.game_height / self.brick_size)):
            brick = Brick(self.brick_size)
            brick.set_position(self.game_width - self.brick_size, i * self.brick_size)
            self.add(brick)
            self.bricks.append(Brick)
