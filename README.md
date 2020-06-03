# Snake-AI

The current project is an implementation of **Deep Reinforcement Learning** for the game **Snake**. The scope is to show how an AI snake learns to play the game on its own.

## Project structure

The code is grouped in the following packages:
- **game_src**: source code for the actual game
- **snake_nn**: source code for the deep learning implementation
- **saved_models**: the folder where models are saved after training. A demo model is included in this folder

For clarity, there are three distinct main files, independent one from another. Even if this duplicates the code, it serves better for the demo purposed of the project. Each file can be executed on its own.

- _main.py_ - manual play mode. It loads the game and allows a user to play it.
- _main_ai_train.py_ - executes the training algorithm for the snake and saves the output model.
- _main_ai_replay.py_ - loads a model and runs the game using the neural network from the model.

## Project execution
Clone the current git repository.

Before execution, make sure to install all dependencies from _requirements.txt_. 

`pip install -r requirements.txt`

There is no specific configuration required before running any of the three main files.
The following controls are available:
- while game is running, pressing ESC will quit the game
- during manual play, the snake is controlled with the arrow keys
- during AI execution (either train or replay), the snake speed can be toggled using key S (for "speed")

## TODO
Code comments will be included in the near future.