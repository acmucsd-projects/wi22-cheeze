import time
import flappy_bird_gym
# from stable_baselines3 import A2C
from stable_baselines3 import DQN
from stable_baselines3 import PPO
# from stable_baselines3.common.env_checker import check_env


def main():
    env = flappy_bird_gym.make("FlappyBird-v0")
    score = 0
    obs = env.reset()

    # Simple check on the environment
    # check_env(env)

    # model = A2C('CnnPolicy', env).learn(total_timesteps=1000)
    model = DQN('MlpPolicy', env, verbose=1)
    # model = PPO('CnnPolicy', env, verbose=1)
    model.learn(total_timesteps=int(2e5))
    # model.save("PPO_flappy")
    model.save("DQN_flappy")
    # model.save("A2C_flappy")

    env.close()

if __name__ == "__main__":
    main()
