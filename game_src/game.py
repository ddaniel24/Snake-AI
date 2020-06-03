import pygame
import random
import math
from game_src.brick import Brick
from game_src.wall import Wall
from game_src.food import Food
from game_src.snake import Snake, Direction


class Game:
    window = None
    running = False
    break_game = False
    (game_width, game_height) = (400, 400)
    brick_size = 10

    wall = None
    snake = None
    food = None
    score = 0
    game_instance_no = 0

    def __init__(self, window: pygame.display, game_width: int, game_height: int):
        self.window = window
        self.game_width, self.game_height = game_width, game_height

        wall_brick = Brick(self.brick_size)
        self.wall = Wall(self.game_width, self.game_height, wall_brick)

        snake_first_brick = Brick(self.brick_size)
        snake_first_brick.set_position(int(self.game_width / 2), int(self.game_height / 2))
        self.snake = Snake(snake_first_brick)
        self.snake.set_moves_available(self.game_width)

        self.food = Food()
        self.generate_food()

        self.running = True
        self.break_game = False

    def process_events(self):
        """
            Process keyboard events during "play mode". In other modes, this method is not used, as each mode
            implements its own processing method.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                self.break_game = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                    self.break_game = True
                if event.key == pygame.K_UP:
                    self.snake.update_direction(Direction.get_value("UP"))
                if event.key == pygame.K_DOWN:
                    self.snake.update_direction(Direction.get_value("DOWN"))
                if event.key == pygame.K_LEFT:
                    self.snake.update_direction(Direction.get_value("LEFT"))
                if event.key == pygame.K_RIGHT:
                    self.snake.update_direction(Direction.get_value("RIGHT"))

        return True

    def is_running(self):
        return self.running

    def logic(self):
        """
            Execute the logic of the game. This implies moving the snake and checking for collisions.
        """

        self.snake.move_snake()

        if self.snake.moves_available <= 0:
            self.running = False
            return

        snake_first_brick = self.snake.get_first_brick()

        if pygame.sprite.spritecollideany(snake_first_brick, self.wall):
            self.running = False
            return

        if pygame.sprite.spritecollideany(snake_first_brick, self.snake.tail):
            self.running = False
            return

        if pygame.sprite.spritecollideany(snake_first_brick, self.food):
            self.snake.add_tail()
            self.score += 1
            self.snake.set_moves_available(self.game_width)
            self.generate_food()

    def generate_food(self):
        """
            Method to add food to the game (after the food has just been eaten, for e.g.)
        """
        run_loop = True
        brick = None

        while run_loop:
            # Generate random position for food
            brick = Brick(self.brick_size)
            random_x = random.randint(0, self.game_width / self.brick_size - 1)
            random_y = random.randint(0, self.game_height / self.brick_size - 1)
            brick.set_position(random_x * self.brick_size, random_y * self.brick_size)

            # Make sure food is not randomly added on the wall or on the snake
            if pygame.sprite.spritecollideany(brick, self.wall) or pygame.sprite.spritecollideany(brick, self.snake):
                run_loop = True
            else:
                run_loop = False

        brick.fill(Brick.RED)

        self.food.set_food(brick)

        self.food.empty()
        self.food.add(brick)

    def check_collision_front_left_right(self):
        """
            This method is used during AI training to compute the agent state.
            The goal is to detect if a collision might happen either in front, left or right, if the snake were to
            move in that direction.
            The logic is the following: depending on the snake direction, virtual bricks are added in front, left
            and right. If these bricks collide with either the wall or the snake itself, it means that if the
            snake were to make that move, it would die.

            Returns:
            - a vector [bool, bool, bool] if collision might happen in front, left, right
        """

        # Virtual bricks used for collision check, relative to the snake head position

        snake_first_brick = self.snake.get_first_brick()
        front_brick = Brick(self.brick_size)
        left_brick = Brick(self.brick_size)
        right_brick = Brick(self.brick_size)

        # Virtual bricks position depend on the current direction of the movement

        if self.snake.direction is Direction.get_value("UP"):
            front_brick.set_position(snake_first_brick.position_x, snake_first_brick.position_y - self.brick_size)
            left_brick.set_position(snake_first_brick.position_x - self.brick_size, snake_first_brick.position_y)
            right_brick.set_position(snake_first_brick.position_x + self.brick_size, snake_first_brick.position_y)

        if self.snake.direction is Direction.get_value("DOWN"):
            front_brick.set_position(snake_first_brick.position_x, snake_first_brick.position_y + self.brick_size)
            left_brick.set_position(snake_first_brick.position_x + self.brick_size, snake_first_brick.position_y)
            right_brick.set_position(snake_first_brick.position_x - self.brick_size, snake_first_brick.position_y)

        if self.snake.direction is Direction.get_value("LEFT"):
            front_brick.set_position(snake_first_brick.position_x - self.brick_size, snake_first_brick.position_y)
            left_brick.set_position(snake_first_brick.position_x, snake_first_brick.position_y + self.brick_size)
            right_brick.set_position(snake_first_brick.position_x, snake_first_brick.position_y - self.brick_size)

        if self.snake.direction is Direction.get_value("RIGHT"):
            front_brick.set_position(snake_first_brick.position_x + self.brick_size, snake_first_brick.position_y)
            left_brick.set_position(snake_first_brick.position_x, snake_first_brick.position_y - self.brick_size)
            right_brick.set_position(snake_first_brick.position_x, snake_first_brick.position_y + self.brick_size)

        collision_front, collision_left, collision_right = False, False, False

        # Check collision of virtual bricks with either wall or snake itself

        if pygame.sprite.spritecollideany(front_brick, self.wall) or \
                pygame.sprite.spritecollideany(front_brick, self.snake.tail):
            collision_front = True

        if pygame.sprite.spritecollideany(left_brick, self.wall) or \
                pygame.sprite.spritecollideany(left_brick, self.snake.tail):
            collision_left = True

        if pygame.sprite.spritecollideany(right_brick, self.wall) or \
                pygame.sprite.spritecollideany(right_brick, self.snake.tail):
            collision_right = True

        return [collision_front, collision_left, collision_right]

    def check_food_position(self):
        """
            This method is used during AI training to compute the agent state.
            The goal is to detect in which quadrant the food is located, considering the snake head as point
            of origin. Imagine a cartesian system, with the snake head at (0, 0).
            There are four possible quadrants where the food might be located, plus an extra four possibilities
            that the food is directly on one of the axis for this system.

            Returns:
            - a vector [bool, ..., bool] (8 values), with 'true' for the specific quadrant where the food is located
        """
        delta_x = self.food.food.position_x - self.snake.get_first_brick().position_x
        delta_y = -(self.food.food.position_y - self.snake.get_first_brick().position_y)

        top, top_left, left, bottom_left = False, False, False, False
        bottom, bottom_right, right, top_right = False, False, False, False

        if not (delta_x == 0 and delta_y == 0):

            angle = int(math.atan2(delta_y, delta_x) * 180 / math.pi)
            if angle < 0:
                angle += 360

            if angle == 0:
                right = True
            if angle == 90:
                top = True
            if angle == 180:
                left = True
            if angle == 270:
                bottom = True
            if 0 < angle < 90:
                top_right = True
            if 90 < angle < 180:
                top_left = True
            if 180 < angle < 270:
                bottom_left = True
            if 270 < angle < 360:
                bottom_right = True

        return [top, top_left, left, bottom_left, bottom, bottom_right, right, top_right]

    def get_snake_direction(self):
        """
            This method is used during AI training to compute the agent state.

            Returns:
            - a vector [bool, ..., bool] (4 values), with 'true' for the current direction the snake is moving
        """
        up, down, left, right = False, False, False, False

        if self.snake.get_direction() is Direction.get_value("UP"):
            up = True
        elif self.snake.get_direction() is Direction.get_value("DOWN"):
            down = True
        elif self.snake.get_direction() is Direction.get_value("LEFT"):
            left = True
        elif self.snake.get_direction() is Direction.get_value("RIGHT"):
            right = True

        return [up, down, left, right]

    def compute_distance_to_food(self):
        """
            This method is used during AI training.
            It computes the distance to the food, with the goal of giving a small reward to the agent if it gets
            closer to the food.

            Returns:
            - distance to the food (divided by brick size, for clarity)
        """
        snake_head = self.snake.get_first_brick()
        food = self.food.get_food()

        dist = self.euclidian_distance(snake_head.position_x, snake_head.position_y,
                                       food.position_x, food.position_y)

        return dist

    def euclidian_distance(self, x1: int, y1: int, x2: int, y2: int):
        dist = float(math.sqrt((float(x1) - float(x2)) ** 2 + (float(y1) - float(y2)) ** 2))
        dist /= float(self.brick_size)
        return dist

    def render(self):
        """
            Render all game elements on screen.
        """
        self.window.fill(Brick.BLACK)
        self.wall.draw(self.window)
        self.snake.draw(self.window)
        self.food.draw(self.window)

        # Text to display on screen with game number and score
        font = pygame.font.SysFont("arial", 15)
        text = font.render("Game: " + str(self.game_instance_no) + " Score: " + str(self.score), True, Brick.WHITE)
        self.window.blit(text, [20, 20])

        # Render everything to current game display
        pygame.display.flip()
