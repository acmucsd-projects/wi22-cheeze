# Team-Cheeze-wi22
# :robot: RL Flappy Bird :dove:
The official ACM AI Team Cheeze repository. 

Create custom OpenAI gym environment for flappy bird and trained [stable-baselines3 PPO](https://stable-baselines3.readthedocs.io/en/master/modules/ppo.html) model to play

![](Flappy.gif)

## Table of Contents:
- [1. Resources](https://github.com/acmucsd-projects/wi22-cheeze/blob/main/README.md#1-resources)
- [2. Getting Started](https://github.com/acmucsd-projects/wi22-cheeze/blob/main/README.md#2-getting-started)
- [3. Difficulties](https://github.com/acmucsd-projects/wi22-cheeze/blob/main/README.md#4-difficulties)
- [4. Author Info](https://github.com/acmucsd-projects/wi22-cheeze/blob/main/README.md#5-author-info)

## 1. Resources

For understanding the necessary tools and methodology, you can check out the following resources:

- [1. StableBaselines3](https://stable-baselines3.readthedocs.io/en/master/guide/examples.html)
- [2. OpenAI Gym](https://gym.openai.com/docs/)
- [3. Reinforcement Learning in Python with Flappy Bird](https://towardsdatascience.com/reinforcement-learning-in-python-with-flappy-bird-37eb01a4e786)

## 2. Getting Started

### Prerequisite

- python >= 3.7
- gym >= 0.18.0
- numpy >= 1.19.5
- pygame >= 2.0.1
- PyTorch >= 1.8.1
- stable-baselines3 >= 1.3.0

### Running

First `cd` into `wi22-cheeze`. Then, run

```bash
# install dependencies
pip install -r requirements.txt
```

Run human playable mode:

```bash
python3 test_simple_env_human.py
```

Run randomly action mode:

```bash
python3 test_simple_env_random.py
```

Run trained model:

```bash
python3 test.py
```
Alternatively, you can change the environment in test and models we trained followed with .zip files, the best model we have trained so far is PPO_flappy_Four_Obs.zip

Train you own model:
You can edit/add more environment within flappy_bird_gym, and register the environment within \__init__.py. 
The simple environments consists of observations with raw numbers, h_dist is the horizontal distance between the bird and the first pipe, while d_dist is the vertical distance between the bird and the first gap. Several different reward functions are build upon them. Additionally, for the last environment we also add the same obervations for the second set of pipes into the observation space, to give the model more ability of prediction. 

The RGB environment consists of using RGB output of the game by frames for training in CNNPolicy, however, it's still working in progress.

Alternatively, you can edit train.py to train your own models within your custom environments.


## Difficulties

To train a good model for playing flappy bird, the biggest factor to be considered is reward function. The naive version of our model was using +1 per step to encourage the survival of the bird, however, it has never been through the first gap but keep flying upward. Therefore, we used 1 - abs(v_dist) instead, so the bird doesn't go too far from the gap. Adding sparse reward, for example the score of the game with the dense reward is helpful. However, using sparse reward individually didn't performed well in this project. 

The second factor to be considered is the observation space. We've only considered the h_dist and v_dist of the first gap at the beginning, and achived much better result adding the same observations of the second gap. There are more observations you can try, for exa,ple the vertical speed of the bird, however it didn't boost the performance significantly in our case.


## Author Info

[Insert your info]

- Stone (Advisor)
- Xing Hong [LinkedIn](https://www.linkedin.com/in/xing-hong-143b69214/) | [GitHub](https://github.com/TIMHX)
- 
- Tristin Xie [LinkedIn](https://www.linkedin.com/in/tristinxie/) | [Website](https://www.tristinxie.com/)
- 
- Mohak Vaswani 
- 
- Saathvik Dirisala [LinkedIn](https://www.linkedin.com/in/tristinxie/) | [Github](https://github.com/saathvikpd)
