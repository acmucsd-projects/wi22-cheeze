""" Implementation of a Flappy Bird OpenAI Gym environment that yields simple
numerical information about the game's state as observations.
"""

from typing import Dict, Tuple, Optional, Union

import gym
import numpy as np
import pygame

from flappy_bird_gym.envs.game_logic import FlappyBirdLogic
from flappy_bird_gym.envs.game_logic import PIPE_WIDTH, PIPE_HEIGHT
from flappy_bird_gym.envs.game_logic import PLAYER_WIDTH, PLAYER_HEIGHT
# from flappy_bird_gym.envs.game_logic import 
from flappy_bird_gym.envs.renderer import FlappyBirdRenderer


class FlappyBirdEnvSimple(gym.Env):
    """ Flappy Bird Gym environment that yields simple observations.

    The observations yielded by this environment are simple numerical
    information about the game's state. Specifically, the observations are:

        * Horizontal distance to the next pipe;
        * Difference between the player's y position and the next hole's y
          position.

    The reward received by the agent in each step is equal to the score obtained
    by the agent in that step. A score point is obtained every time the bird
    passes a pipe.

    Args:
        screen_size (Tuple[int, int]): The screen's width and height.
        normalize_obs (bool): If `True`, the observations will be normalized
            before being returned.
        pipe_gap (int): Space between a lower and an upper pipe.
        bird_color (str): Color of the flappy bird. The currently available
            colors are "yellow", "blue" and "red".
        pipe_color (str): Color of the pipes. The currently available colors are
            "green" and "red".
        background (Optional[str]): Type of background image. The currently
            available types are "day" and "night". If `None`, no background will
            be drawn.
    """

    metadata = {'render.modes': ['human']}

    def __init__(self,
                 screen_size: Tuple[int, int] = (288, 512),
                 normalize_obs: bool = True,
                 pipe_gap: int = 100,
                 bird_color: str = "yellow",
                 pipe_color: str = "green",
                 background: Optional[str] = "day") -> None:
        self.action_space = gym.spaces.Discrete(2)
        self.observation_space = gym.spaces.Box(-np.inf, np.inf,
                                                shape=(2,),
                                                dtype=np.float32)
        self._screen_size = screen_size
        self._normalize_obs = normalize_obs
        self._pipe_gap = pipe_gap

        self._game = None
        self._renderer = None

        self._bird_color = bird_color
        self._pipe_color = pipe_color
        self._bg_type = background

    def _get_observation(self):
        up_pipe = low_pipe = None
        h_dist = 0
        for up_pipe, low_pipe in zip(self._game.upper_pipes,
                                     self._game.lower_pipes):
            h_dist = (low_pipe["x"] + PIPE_WIDTH / 2
                      - (self._game.player_x - PLAYER_WIDTH / 2))
            h_dist += 3  # extra distance to compensate for the buggy hit-box
            if h_dist >= 0:
                break

        upper_pipe_y = up_pipe["y"] + PIPE_HEIGHT
        lower_pipe_y = low_pipe["y"]
        player_y = self._game.player_y

        v_dist = (upper_pipe_y + lower_pipe_y) / 2 - (player_y
                                                      + PLAYER_HEIGHT/2)

        if self._normalize_obs:
            h_dist /= self._screen_size[0]
            v_dist /= self._screen_size[1]

        return np.array([
            h_dist,
            v_dist,
        ])

    def step(self,
             action: Union[FlappyBirdLogic.Actions, int],
    ) -> Tuple[np.ndarray, float, bool, Dict]:
        """ Given an action, updates the game state.

        Args:
            action (Union[FlappyBirdLogic.Actions, int]): The action taken by
                the agent. Zero (0) means "do nothing" and one (1) means "flap".

        Returns:
            A tuple containing, respectively:

                * an observation (horizontal distance to the next pipe;
                  difference between the player's y position and the next hole's
                  y position);
                * a status report (`True` if the game is over and `False`
                  otherwise);
                * an info dictionary.
        """
        alive = self._game.update_state(action)
        obs = self._get_observation()

        reward = 1 - abs(obs[1])

        done = not alive
        info = {"score": self._game.score}

        return obs, reward, done, info

    def reset(self):
        """ Resets the environment (starts a new game). """
        self._game = FlappyBirdLogic(screen_size=self._screen_size,
                                     pipe_gap_size=self._pipe_gap)
        if self._renderer is not None:
            self._renderer.game = self._game

        return self._get_observation()

    def render(self, mode='human') -> None:
        """ Renders the next frame. """
        if self._renderer is None:
            self._renderer = FlappyBirdRenderer(screen_size=self._screen_size,
                                                bird_color=self._bird_color,
                                                pipe_color=self._pipe_color,
                                                background=self._bg_type)
            self._renderer.game = self._game
            self._renderer.make_display()

        self._renderer.draw_surface(show_score=True)
        self._renderer.update_display()

    def close(self):
        """ Closes the environment. """
        if self._renderer is not None:
            pygame.display.quit()
            self._renderer = None
        super().close()

class FlappyBirdEnvAdvance(gym.Env):
    """ Flappy Bird Gym environment that yields simple observations.

    """
    metadata = {'render.modes': ['human']}

    def __init__(self,
                 screen_size: Tuple[int, int] = (288, 512),
                 normalize_obs: bool = True,
                 pipe_gap: int = 100,
                 bird_color: str = "yellow",
                 pipe_color: str = "green",
                 background: Optional[str] = "day") -> None:
        self.action_space = gym.spaces.Discrete(2)
        self.observation_space = gym.spaces.Box(-np.inf, np.inf,
                                                shape=(2,),
                                                dtype=np.float32)
        self._screen_size = screen_size
        self._normalize_obs = normalize_obs
        self._pipe_gap = pipe_gap

        self._game = None
        self._renderer = None

        self._bird_color = bird_color
        self._pipe_color = pipe_color
        self._bg_type = background
        self.curr_score = 0

    def _get_observation(self):
        up_pipe = low_pipe = None
        h_dist = 0
        for up_pipe, low_pipe in zip(self._game.upper_pipes,
                                     self._game.lower_pipes):
            h_dist = (low_pipe["x"] + PIPE_WIDTH / 2
                      - (self._game.player_x - PLAYER_WIDTH / 2))
            h_dist += 3  # extra distance to compensate for the buggy hit-box
            if h_dist >= 0:
                break

        upper_pipe_y = up_pipe["y"] + PIPE_HEIGHT
        lower_pipe_y = low_pipe["y"]
        player_y = self._game.player_y

        v_dist = (upper_pipe_y + lower_pipe_y) / 2 - (player_y
                                                      + PLAYER_HEIGHT/2)

        if self._normalize_obs:
            h_dist /= self._screen_size[0]
            v_dist /= self._screen_size[1]

        return np.array([
            h_dist,
            v_dist,
        ])

    def step(self,
             action: Union[FlappyBirdLogic.Actions, int],
    ) -> Tuple[np.ndarray, float, bool, Dict]:
        """ Given an action, updates the game state.

        Args:
            action (Union[FlappyBirdLogic.Actions, int]): The action taken by
                the agent. Zero (0) means "do nothing" and one (1) means "flap".

        Returns:
            A tuple containing, respectively:

                * an observation (horizontal distance to the next pipe;
                  difference between the player's y position and the next hole's
                  y position);
                * a status report (`True` if the game is over and `False`
                  otherwise);
                * an info dictionary.
        """
        alive = self._game.update_state(action)
        obs = self._get_observation()
        
        info = {"score": self._game.score}

        if self._game.score - self.curr_score == 1:
            reward = 2          # sparse + dense
            self.curr_score += 1
        else:
            reward = 1 - abs(obs[1])      # sparse + dense

        done = not alive

        return obs, reward, done, info

    def reset(self):
        """ Resets the environment (starts a new game). """
        self._game = FlappyBirdLogic(screen_size=self._screen_size,
                                     pipe_gap_size=self._pipe_gap)
        if self._renderer is not None:
            self._renderer.game = self._game

        self.curr_score = 0
        return self._get_observation()

    def render(self, mode='human') -> None:
        """ Renders the next frame. """
        if self._renderer is None:
            self._renderer = FlappyBirdRenderer(screen_size=self._screen_size,
                                                bird_color=self._bird_color,
                                                pipe_color=self._pipe_color,
                                                background=self._bg_type)
            self._renderer.game = self._game
            self._renderer.make_display()

        self._renderer.draw_surface(show_score=True)
        self._renderer.update_display()

    def close(self):
        """ Closes the environment. """
        if self._renderer is not None:
            pygame.display.quit()
            self._renderer = None
        super().close()

class FlappyBirdEnvFourObservations(gym.Env):
    """ Flappy Bird Gym environment that yields simple observations.

    """
    metadata = {'render.modes': ['human']}

    def __init__(self,
                 screen_size: Tuple[int, int] = (288, 512),
                 normalize_obs: bool = True,
                 pipe_gap: int = 100,
                 bird_color: str = "yellow",
                 pipe_color: str = "green",
                 background: Optional[str] = "day") -> None:
        self.action_space = gym.spaces.Discrete(2)
        self.observation_space = gym.spaces.Box(-np.inf, np.inf,
                                                shape=(4,),
                                                dtype=np.float32)
        self._screen_size = screen_size
        self._normalize_obs = normalize_obs
        self._pipe_gap = pipe_gap

        self._game = None
        self._renderer = None

        self._bird_color = bird_color
        self._pipe_color = pipe_color
        self._bg_type = background
        self.curr_score = 0

    def _get_observation(self):
        up_pipe = low_pipe = None
        h_dist = 0
        for up_pipe, low_pipe in zip(self._game.upper_pipes,
                                     self._game.lower_pipes):
            h_dist = (low_pipe["x"] + PIPE_WIDTH / 2
                      - (self._game.player_x - PLAYER_WIDTH / 2))
            h_dist += 3  # extra distance to compensate for the buggy hit-box
            if h_dist >= 0:
                break

        upper_pipe_y = up_pipe["y"] + PIPE_HEIGHT
        lower_pipe_y = low_pipe["y"]
        player_y = self._game.player_y

        v_dist = (upper_pipe_y + lower_pipe_y) / 2 - (player_y
                                                      + PLAYER_HEIGHT / 2)

        if self._normalize_obs:
            h_dist /= self._screen_size[0]
            v_dist /= self._screen_size[1]

        up_pipe_2 = low_pipe_2 = None
        h_dist_2 = 0
        up_pipe_2 = self._game.upper_pipes[1]
        low_pipe_2 = self._game.lower_pipes[1]
        h_dist_2 = (low_pipe_2["x"] + PIPE_WIDTH / 2
                      - (self._game.player_x - PLAYER_WIDTH / 2))
        h_dist_2 += 3  # extra distance to compensate for the buggy hit-box

        upper_pipe_y = up_pipe_2["y"] + PIPE_HEIGHT
        lower_pipe_y = low_pipe_2["y"]
        player_y = self._game.player_y

        v_dist_2 = (upper_pipe_y + lower_pipe_y) / 2 - (player_y
                                                      + PLAYER_HEIGHT / 2)

        if self._normalize_obs:
            h_dist_2 /= self._screen_size[0]
            v_dist_2 /= self._screen_size[1]

        return np.array([
            h_dist,
            v_dist,
            h_dist_2,
            v_dist_2])

    def step(self,
             action: Union[FlappyBirdLogic.Actions, int],
             ) -> Tuple[np.ndarray, float, bool, Dict]:

        """ Given an action, updates the game state.

        Args:
            action (Union[FlappyBirdLogic.Actions, int]): The action taken by
                the agent. Zero (0) means "do nothing" and one (1) means "flap".

        Returns:
            A tuple containing, respectively:

                * an observation (horizontal distance to the next pipe;
                  difference between the player's y position and the next hole's
                  y position);
                * a status report (`True` if the game is over and `False`
                  otherwise);
                * an info dictionary.
        """
        alive = self._game.update_state(action)
        obs = self._get_observation()
        info = {"score": self._game.score}

        if self._game.score - self.curr_score == 1:
            reward = 2  # sparse + dense
            self.curr_score += 1
        else:
            reward = 1 - abs(obs[1])  # sparse + dense

        done = not alive

        return obs, reward, done, info

    def reset(self):
        """ Resets the environment (starts a new game). """
        self._game = FlappyBirdLogic(screen_size=self._screen_size,
                                     pipe_gap_size=self._pipe_gap)
        if self._renderer is not None:
            self._renderer.game = self._game

        self.curr_score = 0
        return self._get_observation()

    def render(self, mode='human') -> None:
        """ Renders the next frame. """
        if self._renderer is None:
            self._renderer = FlappyBirdRenderer(screen_size=self._screen_size,
                                                bird_color=self._bird_color,
                                                pipe_color=self._pipe_color,
                                                background=self._bg_type)
            self._renderer.game = self._game
            self._renderer.make_display()

        self._renderer.draw_surface(show_score=True)
        self._renderer.update_display()

    def close(self):
        """ Closes the environment. """
        if self._renderer is not None:
            pygame.display.quit()
            self._renderer = None
        super().close()
