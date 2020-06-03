import pygame
from game_src.brick import Brick


class Food(pygame.sprite.Group):
    food = None

    def __init__(self):
        super(Food, self).__init__()

    def set_food(self, food: Brick):
        self.food = food

    def get_food(self):
        return self.food
