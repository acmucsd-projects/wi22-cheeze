import gym
from stable_baselines3 import PPO
from flappyenv import FlappyEnv

env = FlappyEnv()
env.reset()

timestep_model = 430000

models_dir = "models/1645759471"
model_path = f"{models_dir}/{timestep_model}.zip"
model = PPO.load(model_path, env=env)

episodes = 10

for ep in range(episodes):
    obs = env.reset()
    done = False
    total = 0
    while not done:
        env.render()
        action, _ = model.predict(obs)
        obs, reward, done, info = env.step(action)
    print(env.score)

env.close()