import pygame
from game_src.brick import Brick


class Snake(pygame.sprite.Group):
    snake = []
    tail = None
    direction = None

    def __init__(self, brick: Brick):
        super(Snake, self).__init__()
        self.snake = []
        self.empty()
        self.snake.append(brick)
        brick.fill(Brick.WHITE)
        self.tail = pygame.sprite.Group()
        for i in range(0, 3):
            last_brick = self.snake[-1]
            new_brick = Brick(last_brick.size)
            new_brick.set_position(last_brick.position_x, last_brick.position_y + last_brick.size)
            new_brick.fill(Brick.GREEN)
            self.snake.append(new_brick)
            self.add(new_brick)
            self.tail.add(new_brick)
        self.direction = Direction.get_value("UP")
        self.moves_available = 200

    def get_first_brick(self):
        return self.snake[0]

    def add_tail(self):
        last_brick = self.snake[-1]
        new_brick = Brick(last_brick.size)
        new_brick.set_position(last_brick.position_x, last_brick.position_y)
        new_brick.fill(Brick.GREEN)
        self.snake.append(new_brick)
        self.add(new_brick)
        self.tail.add(new_brick)

    def set_moves_available(self, value: int):
        self.moves_available = value

    def get_direction(self):
        return self.direction

    def update_direction(self, direction: int):
        if direction is Direction.get_value("UP") and self.direction is Direction.get_value("DOWN"):
            return False
        if direction is Direction.get_value("DOWN") and self.direction is Direction.get_value("UP"):
            return False
        if direction is Direction.get_value("LEFT") and self.direction is Direction.get_value("RIGHT"):
            return False
        if direction is Direction.get_value("RIGHT") and self.direction is Direction.get_value("LEFT"):
            return False
        self.direction = direction
        return True

    def update_direction_nn(self, new_state: str):
        if new_state is "NO_CHANGE":
            return

        if new_state is "LEFT":
            if self.direction is Direction.get_value("UP"):
                self.direction = Direction.get_value("LEFT")
            elif self.direction is Direction.get_value("DOWN"):
                self.direction = Direction.get_value("RIGHT")
            elif self.direction is Direction.get_value("LEFT"):
                self.direction = Direction.get_value("DOWN")
            elif self.direction is Direction.get_value("RIGHT"):
                self.direction = Direction.get_value("UP")
            return

        if new_state is "RIGHT":
            if self.direction is Direction.get_value("UP"):
                self.direction = Direction.get_value("RIGHT")
            elif self.direction is Direction.get_value("DOWN"):
                self.direction = Direction.get_value("LEFT")
            elif self.direction is Direction.get_value("LEFT"):
                self.direction = Direction.get_value("UP")
            elif self.direction is Direction.get_value("RIGHT"):
                self.direction = Direction.get_value("DOWN")
            return

    def move_snake(self):
        self.moves_available -= 1

        value = self.snake[0].size

        for brick in self.snake:
            brick.set_previous_position(brick.position_x, brick.position_y)

        first_brick = self.snake[0]
        new_position_x, new_position_y = 0, 0

        if self.direction == Direction.get_value("UP"):
            new_position_x, new_position_y = first_brick.position_x, first_brick.position_y - value
        elif self.direction == Direction.get_value("DOWN"):
            new_position_x, new_position_y = first_brick.position_x, first_brick.position_y + value
        elif self.direction == Direction.get_value("LEFT"):
            new_position_x, new_position_y = first_brick.position_x - value, first_brick.position_y
        elif self.direction == Direction.get_value("RIGHT"):
            new_position_x, new_position_y = first_brick.position_x + value, first_brick.position_y

        first_brick.set_position(new_position_x, new_position_y)

        for i in range(1, len(self.snake)):
            previous_brick = self.snake[i-1]
            current_brick = self.snake[i]
            current_brick.set_position(previous_brick.previous_position_x, previous_brick.previous_position_y)

        self.empty()
        self.tail.empty()

        for brick in self.snake:
            self.add(brick)

        for brick in self.snake[1:]:
            self.tail.add(brick)


class Direction:
    direction_dictionary = {
        "UP": 0,
        "DOWN": 1,
        "LEFT": 2,
        "RIGHT": 3
    }

    @staticmethod
    def get_value(value: str):
        return Direction.direction_dictionary.get(value)
