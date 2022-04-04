# Team-Cheeze-wi22
# :robot: RL Flappy Bird :dove:
The official ACM AI Team Cheeze repository. 

Create custom OpenAI gym environment for flappy bird and trained [stable-baselines3 PPO](https://stable-baselines3.readthedocs.io/en/master/modules/ppo.html) model to play

## Table of Contents:
- [1. Resources](https://github.com/acmucsd-projects/wi22-cheeze/blob/main/README.md#1-resources)
- [2. Getting Started](https://github.com/acmucsd-projects/wi22-cheeze/blob/main/README.md#2-getting-started)
- [3. Structure](https://github.com/acmucsd-projects/wi22-cheeze/blob/main/README.md#3-structure)
- [4. Difficulties](https://github.com/acmucsd-projects/wi22-cheeze/blob/main/README.md#4-difficulties)
- [5. Author Info](https://github.com/acmucsd-projects/wi22-cheeze/blob/main/README.md#5-author-info)

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
Alternatively, you can change the environment in test and models we trained followed with .zip files

Train you own model:
You can edit/add more environment within flappy_bird_gym, and register the environment within \__init__.py.
Then, you can edit train.py to train your own models within your custom environments.

## 3. Structure

[Insert some text on the structure of this repo and how everything is organized.]

## 4. Difficulties

[Insert some text on the difficulties you faced and how you solved them (images and GIFs are awesome).]

## 5. Author Info

[Insert your info]

- Stone (Advisor)
- Xing Hong [LinkedIn](https://www.linkedin.com/in/xing-hong-143b69214/) | [GitHub](https://github.com/TIMHX)
- Tristin
- Mohak Vaswani
- Saathvik
