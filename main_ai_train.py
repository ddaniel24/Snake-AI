import pygame
from game_src.game import Brick
from game_src.game import Game
from snake_nn.neural_network import NNAgent

GAME_TITLE = "Snake AI"

TRAINING_STEPS = 750
TRAINING_BATCH_SIZE = 250
EPSILON_DECAY = 75

SLOW_DOWN_SPEED = False


def main():
    """
        Main method for running the game in "training mode". In this mode, games are generated and the neural
        network is trained using Deep Reinforcement Learning.
    """

    pygame.init()

    agent = NNAgent()

    game_width = 200
    game_height = 200

    pygame.display.set_caption(GAME_TITLE)

    for train_step in range(1, TRAINING_STEPS + 1):

        if 0 < train_step < 250:
            game_width = 200
            game_height = 200
        elif 250 <= train_step <= 500:
            game_width = 300
            game_height = 300
        elif 500 < train_step:
            game_width = 400
            game_height = 400

        window = pygame.display.set_mode((game_width, game_height))
        window.fill(Brick.BLACK)

        game = Game(window, game_width, game_height)
        game.game_instance_no = train_step
        clock = pygame.time.Clock()

        agent.set_game(game)

        epsilon = 1 - train_step / EPSILON_DECAY

        agent.clear_memory()

        score_new = 0

        while game.is_running():

            process_events()

            state_current = agent.get_agent_state()

            dist_to_food_init = game.compute_distance_to_food()

            action = agent.predict_movement(state_current, epsilon)

            if action[0]:
                game.snake.update_direction_nn("NO_CHANGE")
            elif action[1]:
                game.snake.update_direction_nn("LEFT")
            elif action[2]:
                game.snake.update_direction_nn("RIGHT")

            score_init = game.score

            game.logic()
            game.render()

            score_new = game.score

            dist_to_food_new = game.compute_distance_to_food()

            moved_towards_food = True if dist_to_food_new < dist_to_food_init else False
            food_eaten = True if score_new > score_init else False

            reward = agent.compute_reward(moved_towards_food, food_eaten)

            state_new = agent.get_agent_state()

            agent.remember_state(state_current, action, reward, state_new, not game.is_running())

            agent.train_target_model()

            if SLOW_DOWN_SPEED:
                clock.tick(30)

        agent.replay_state(batch_size=TRAINING_BATCH_SIZE)

        if train_step % 250 == 0:
            agent.save_weights(train_step)

        if score_new > 0:
            print("Step: {0}, score: {1}".format(train_step, score_new))

    agent.save_weights(0)

    print("Done.")

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
