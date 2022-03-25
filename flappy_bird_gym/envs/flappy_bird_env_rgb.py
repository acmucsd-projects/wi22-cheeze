from typing import Dict, Tuple, Optional, Union

import gym
import numpy as np
import pygame

from flappy_bird_gym.envs.game_logic import FlappyBirdLogic
from flappy_bird_gym.envs.renderer import FlappyBirdRenderer


class FlappyBirdEnvRGB(gym.Env):
    """  Flappy Bird Gym environment that yields images as observations.
    The observations yielded by this environment are RGB-arrays (images)
    representing the game's screen.
    The reward received by the agent in each step is equal to the score obtained
    by the agent in that step. A score point is obtained every time the bird
    passes a pipe.
    Args:
        screen_size (Tuple[int, int]): The screen's width and height.
        pipe_gap (int): Space between a lower and an upper pipe.
        bird_color (str): Color of the flappy bird. The currently available
            colors are "yellow", "blue" and "red".
        pipe_color (str): Color of the pipes. The currently available colors are
            "green" and "red".
        background (Optional[str]): Type of background image. The currently
            available types are "day" and "night". If `None`, no background will
            be drawn.
    """

    metadata = {"render.modes": ["human", "rgb_array"]}

    def __init__(self,
                 screen_size: Tuple[int, int] = (288, 512),
                 pipe_gap: int = 100,
                 bird_color: str = "yellow",
                 pipe_color: str = "green",
                 background: Optional[str] = None) -> None:
        self.action_space = gym.spaces.Discrete(2)
        self.observation_space = gym.spaces.Box(0, 255, [*screen_size, 3])

        self._screen_size = screen_size
        self._pipe_gap = pipe_gap

        self._game = None
        self._renderer = FlappyBirdRenderer(screen_size=self._screen_size,
                                            bird_color=bird_color,
                                            pipe_color=pipe_color,
                                            background=background)
        self.curr_score = 0

    def _get_observation(self):
        self._renderer.draw_surface(show_score=False)
        arr = pygame.surfarray.array3d(self._renderer.surface)
        return arr

    def reset(self):
        """ Resets the environment (starts a new game).
        """
        self._game = FlappyBirdLogic(screen_size=self._screen_size,
                                     pipe_gap_size=self._pipe_gap)

        self._renderer.game = self._game
        self.curr_score = 0
        return self._get_observation()

    def step(self,
             action: Union[FlappyBirdLogic.Actions, int],
    ) -> Tuple[np.ndarray, float, bool, Dict]:
        """ Given an action, updates the game state.
        Args:
            action (Union[FlappyBirdLogic.Actions, int]): The action taken by
                the agent. Zero (0) means "do nothing" and one (1) means "flap".
        Returns:
            A tuple containing, respectively:
                * an observation (RGB-array representing the game's screen);
                * a reward;
                * a status report (`True` if the game is over and `False`
                  otherwise);
                * an info dictionary.
        """
        alive = self._game.update_state(action)
        obs = self._get_observation()

        # reward = 1
        if self._game.score - self.curr_score == 1:
            reward = 2          # sparse + dense
            self.curr_score += 1
        else:
            reward = 1      # sparse + dense

        done = not alive
        info = {"score": self._game.score}

        return obs, reward, done, info

    def render(self, mode="human") -> Optional[np.ndarray]:
        """ Renders the environment.
        If ``mode`` is:
            - human: render to the current display. Usually for human
              consumption.
            - rgb_array: Return an numpy.ndarray with shape (x, y, 3),
              representing RGB values for an x-by-y pixel image, suitable
              for turning into a video.
        Args:
            mode (str): the mode to render with.
        Returns:
            `None` if ``mode`` is "human" and a numpy.ndarray with RGB values if
            it's "rgb_array"
        """
        if mode not in FlappyBirdEnvRGB.metadata["render.modes"]:
            raise ValueError("Invalid render mode!")

        self._renderer.draw_surface(show_score=True)
        if mode == "rgb_array":
            return pygame.surfarray.array3d(self._renderer.surface)
        else:
            if self._renderer.display is None:
                self._renderer.make_display()

            self._renderer.update_display()

    def close(self):
        """ Closes the environment. """
        if self._renderer is not None:
            pygame.display.quit()
            self._renderer = None

        super().close()