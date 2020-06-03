from keras.optimizers import Adam
from keras.models import Sequential
from keras.layers.core import Dense
from keras.utils import to_categorical
import collections
import numpy as np
import random
from random import randint
import os
import time

from game_src.game import Game


class NNAgent:
    model = None
    target_model = None
    game = None

    memory_length = 2500
    nn_input_layer = 15

    def __init__(self):

        self.memory = collections.deque(maxlen=self.memory_length)
        self.gamma = 0.9

        self.model = self.build_neural_network()
        self.target_model = self.build_neural_network()

    def build_neural_network(self):
        model = Sequential()
        model.add(Dense(activation='relu', input_dim=self.nn_input_layer, units=64))
        model.add(Dense(activation='relu', units=64))
        model.add(Dense(activation='relu', units=64))
        model.add(Dense(activation='softmax', units=3))
        opt = Adam(learning_rate=0.0005, beta_1=0.9, beta_2=0.999, amsgrad=False)
        model.compile(loss='mean_squared_error', optimizer=opt)

        return model

    def model_summary(self):
        return self.model.summary()

    def get_agent_state(self):
        state = []

        snake_direction = self.game.get_snake_direction()

        check_collision = self.game.check_collision_front_left_right()

        check_food_position = self.game.check_food_position()

        state += snake_direction
        state += check_collision
        state += check_food_position

        return np.array(state, dtype=bool).reshape(1, self.nn_input_layer)

    def set_game(self, game: Game):
        self.game = game

    def predict_movement(self, state: np.array, epsilon: float):
        if randint(0, 1) < epsilon:
            new_action = to_categorical(randint(0, 2), num_classes=3)
        else:
            prediction = self.model.predict(state)
            new_action = to_categorical(np.argmax(prediction[0]), num_classes=3)

        return new_action

    def compute_reward(self, moved_towards_food: bool, food_eaten: bool):
        reward = 0

        if moved_towards_food:
            reward = 0.1

        if food_eaten:
            reward = 3

        if not self.game.is_running():
            reward = -10

        return reward

    def remember_state(self, state, action, reward, next_state, done: bool):
        self.memory.append((state, action, reward, next_state, done))

    def clear_memory(self):
        self.memory.clear()
        return

    def replay_state(self, batch_size):
        if len(self.memory) < batch_size:
            samples = self.memory
        else:
            samples = random.sample(self.memory, batch_size)

        for sample in samples:
            state, action, reward, next_state, done = sample
            target = self.target_model.predict(next_state)

            if done:
                target[0][np.argmax(action)] = reward
            else:
                q_future = np.amax(self.target_model.predict(next_state)[0])
                target[0][np.argmax(action)] = reward + q_future * self.gamma
            self.model.fit(state, target, epochs=1, verbose=0)

    def train_target_model(self):
        weights = self.model.get_weights()
        target_weights = self.target_model.get_weights()
        for i in range(len(target_weights)):
            target_weights[i] = weights[i]
        self.target_model.set_weights(target_weights)

    def save_weights(self, step: int):
        local_dir = os.path.dirname(__file__)
        time_now = time.strftime("%Y%m%d-%H%M%S")
        filename = "snake-model-" + time_now + "-" + str(step) + ".h5"
        filename = os.path.join(local_dir, "model", filename)
        self.model.save_weights(filename)

    def load_weights(self, model: str):
        self.model.load_weights(model)
        print("Model weights loaded from " + model)
