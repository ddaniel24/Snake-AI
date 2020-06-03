import pygame
from game_src.brick import Brick


class Wall(pygame.sprite.Group):
    """
        Class extends SpriteGroup in order to make use of the collision methods already implemented in Pygame
    """
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
        """
            Build the wall for the game. Bricks are added one next to the other, starting from (0 ,0) to
            (game_width, game_height).
            Remember the coordinate system in Pygame starts from the top-left corner (0, 0) and both x and y axis
            are positive to the right and down, respectively.
        """
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
