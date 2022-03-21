import time
import flappy_bird_gym
# from stable_baselines3 import A2C
from stable_baselines3 import DQN
from stable_baselines3 import PPO
# from stable_baselines3.common.env_checker import check_env


def main():
    # env = flappy_bird_gym.make("FlappyBird-v0")
    env = flappy_bird_gym.make("FlappyBird-v1")
    score = 0
    obs = env.reset()

    # Simple check on the environment
    # check_env(env)

    # Read Model
    # model = DQN.load("DQN_flappy", env=env)
    # model = PPO.load("PPO_flappy", env=env)
    model = PPO.load("PPO_flappy_sparse_dense", env=env)

    while True:
        env.render()
        action, _state = model.predict(obs, deterministic=True)
        obs, reward, done, info = env.step(action)

        score += reward
        print(f"Obs: {obs}\n"
              f"Reward: {score}\n"
              f"Score: {info}\n")

        time.sleep(1 / 30)
        env.render()
        if done:
            env.render()
            time.sleep(0.5)
            break

    env.close()

if __name__ == "__main__":
    main()
