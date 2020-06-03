import pygame
from game_src.game import Brick
from game_src.game import Game
from snake_nn.neural_network import NNAgent

GAME_WIDTH = 400
GAME_HEIGHT = 400
GAME_TITLE = "Snake AI"

SLOW_DOWN_SPEED = True

MODEL_PATH = "saved_models\\snake-model-20200507-185914-15x64x64x64x3.h5"


def main():
    pygame.init()

    window = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT))
    window.fill(Brick.BLACK)

    pygame.display.set_caption(GAME_TITLE)

    agent = NNAgent()
    print(agent.model_summary())
    agent.load_weights(MODEL_PATH)

    index = 0

    run = True
    while run:

        game = Game(window, GAME_WIDTH, GAME_HEIGHT)
        agent.set_game(game)
        game.game_instance_no = index

        clock = pygame.time.Clock()

        while game.is_running():

            process_events()

            state_current = agent.get_agent_state()
            action = agent.predict_movement(state_current, -1)

            if action[0]:
                game.snake.update_direction_nn("NO_CHANGE")
            elif action[1]:
                game.snake.update_direction_nn("LEFT")
            elif action[2]:
                game.snake.update_direction_nn("RIGHT")

            game.logic()
            game.render()

            if SLOW_DOWN_SPEED:
                clock.tick(60)

        index += 1

        print("Game: {0}, score: {1}".format(index, game.score))

    pygame.quit()
    quit()


def process_events():
    global SLOW_DOWN_SPEED

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                quit()
            if event.key == pygame.K_s:
                SLOW_DOWN_SPEED = not SLOW_DOWN_SPEED


if __name__ == '__main__':
    main()
