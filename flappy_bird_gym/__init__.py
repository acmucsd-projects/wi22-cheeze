""" Registers the gym environments and exports the `gym.make` function.
"""

# Silencing pygame:
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

# Exporting envs:
from flappy_bird_gym.envs.flappy_bird_env_simple import FlappyBirdEnvSimple

# Exporting original game:
from flappy_bird_gym import original_game

# Exporting gym.make:
from gym import make

# Registering environments:
from gym.envs.registration import register

register(
    id="FlappyBird-v0",
    entry_point="flappy_bird_gym:FlappyBirdEnvSimple",
)

# Main names:
__all__ = [
    make.__name__,
    FlappyBirdEnvSimple.__name__,
]
