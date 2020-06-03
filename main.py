import pygame
from game_src.game import Brick
from game_src.game import Game

GAME_WIDTH = 400
GAME_HEIGHT = 400
GAME_TITLE = "Snake AI"


def main():
    """
        Main method for running the game in "play mode". In this mode, you can interact with the snake
        by using the arrow keys. There is no AI at all in this mode.
    """

    pygame.init()

    window = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT))
    pygame.display.set_caption(GAME_TITLE)
    window.fill(Brick.BLACK)

    run = True
    while run:

        game = Game(window, GAME_WIDTH, GAME_HEIGHT)
        clock = pygame.time.Clock()

        while game.is_running():
            game.process_events()

            game.logic()

            game.render()
            clock.tick(15)

        if game.break_game:
            run = False

    pygame.quit()
    quit()


if __name__ == '__main__':
    main()
