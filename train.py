import time
import flappy_bird_gym
# from stable_baselines3 import A2C
from stable_baselines3 import DQN
from stable_baselines3 import PPO
from stable_baselines3.common.env_checker import check_env


def main():
    # env = flappy_bird_gym.make("FlappyBird-v0")       # Original reward 1 - abs(obs[1])
    # env = flappy_bird_gym.make("FlappyBird-v1")       # New reward
    env = flappy_bird_gym.make("FlappyBird-v2")         # four observations
    # env = flappy_bird_gym.make("FlappyBird-rgb-v0")     # RGB vector output with sparse+dense reward
    env.reset()

    # Simple check on the environment
    check_env(env)

    # model = PPO('CnnPolicy', env, verbose=1)        # CNN for RGB vector input
    # # model = PPO.load("PPO_flappy", env=env)
    # # model = DQN('MlpPolicy', env, verbose=1)
    model = PPO('MlpPolicy', env, verbose=1)
    model.learn(total_timesteps=int(2e5))
    model.save("PPO_flappy_Four_Obs")
    # model.save("PPO_flappy_RGB_sparse_dense")
    # model.save("PPO_flappy")
    # model.save("DQN_flappy")

    env.close()

if __name__ == "__main__":
    main()
