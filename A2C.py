import gym
import numpy as np
from enviroment import CustomMountainCar 

from stable_baselines3 import A2C
from stable_baselines3.common.evaluation import evaluate_policy


def main():
    env = gym.make('MountainCar-v0',render_mode="human")
    env = CustomMountainCar(env)

    model = A2C("MlpPolicy", env, verbose=1,learning_rate=0.01)
    model.learn(total_timesteps=10_000,progress_bar=True)

    mean_reward, std_reward = evaluate_policy(model, model.get_env(), n_eval_episodes=10)
    print("mean_reward:",mean_reward)
    print("std_reward:",std_reward)

    vec_env = model.get_env()
    obs = vec_env.reset()


    # MountainCar 
    # mean_reward: -0.11385590000000001
    # std_reward: 0.0005874511809503813

    while True:
        action, _state = model.predict(obs, deterministic=True)
        obs, reward, done, info = vec_env.step(action)
        # vec_env.render("human")
        if done:
            break

    env.close()
    return

if __name__ == "__main__":
    main()