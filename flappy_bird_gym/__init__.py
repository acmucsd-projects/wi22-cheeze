""" Registers the gym environments and exports the `gym.make` function.
"""

# Silencing pygame:
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

# Exporting envs:
from flappy_bird_gym.envs.flappy_bird_env_simple import FlappyBirdEnvSimple
from flappy_bird_gym.envs.flappy_bird_env_simple import FlappyBirdEnvAdvance
from flappy_bird_gym.envs.flappy_bird_env_simple import FlappyBirdEnvThreeObservations
from flappy_bird_gym.envs.flappy_bird_env_simple import FlappyBirdEnvFourObservations
from flappy_bird_gym.envs.flappy_bird_env_simple import FlappyBirdEnvFourObsSparse
from flappy_bird_gym.envs.flappy_bird_env_rgb import FlappyBirdEnvRGB

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

register(
    id="FlappyBird-v1",
    entry_point="flappy_bird_gym:FlappyBirdEnvAdvance",
)

register(
    id="FlappyBird-v2",
    entry_point="flappy_bird_gym:FlappyBirdEnvThreeObservations",
)

register(
    id="FlappyBird-v3",
    entry_point="flappy_bird_gym:FlappyBirdEnvFourObservations",
)

register(
    id="FlappyBird-v4",
    entry_point="flappy_bird_gym:FlappyBirdEnvFourObsSparse",
)


register(
    id="FlappyBird-rgb-v0",
    entry_point="flappy_bird_gym:FlappyBirdEnvRGB",
)

# Main names:
__all__ = [
    make.__name__,
    FlappyBirdEnvSimple.__name__,
    FlappyBirdEnvAdvance.__name__,
    FlappyBirdEnvThreeObservations.__name__,
    FlappyBirdEnvFourObservations.__name__,
    FlappyBirdEnvFourObsSparse.__name__,
    FlappyBirdEnvRGB.__name__,
]
