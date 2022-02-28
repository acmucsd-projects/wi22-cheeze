import time
import flappy_bird_gym


def main():
    # env = gym.make("flappy_bird_gym:FlappyBird-v0")
    env = flappy_bird_gym.make("FlappyBird-v0")
    score = 0
    obs = env.reset()
    while True:
        env.render()

        # Getting random action:
        action = env.action_space.sample()

        # Processing:
        obs, reward, done, info = env.step(action)

        score += reward
        print(f"Obs: {obs}\n"
              f"Score: {score}\n")

        time.sleep(1 / 30)

        if done:
            env.render()
            time.sleep(0.5)
            break

    env.close()


if __name__ == "__main__":
    main()
