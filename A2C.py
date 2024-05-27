import gymnasium as gym
from enviroment.enviroment import FrozenLakeEnv

from stable_baselines3 import A2C
from stable_baselines3.common.env_util import make_vec_env
from stable_baselines3.common.evaluation import evaluate_policy
from stable_baselines3.common.logger import configure

import os
import statistics

def main():
    # ---------- Training ------------
    # # Create enviroment for training
    # env = make_vec_env(FrozenLakeEnv, n_envs=1, monitor_dir="logs/A2C_monitor_logs", env_kwargs={'map_name': "5x5", 'is_slippery': True})
    
    # # Set the logger to csv and stdout
    # new_logger = configure("logs/A2C_logs", ["stdout", "csv"])

    # # Create model, set the logger and train model
    # model = A2C("MlpPolicy", env, verbose=1, learning_rate=0.1, device='cuda')
    # model.set_logger(new_logger)
    # model.learn(total_timesteps=50_000, progress_bar=True)
    # --------------------------------

    # Save the model
    # model.save("A2C_frozenLake")

    # Load the model
    model = A2C.load("A2C_frozenLake_final")

    # Create enviroment for evaluation and visualization 
    vec_env = make_vec_env(FrozenLakeEnv, n_envs=1, env_kwargs={'desc': None, 'map_name': "5x5", 'is_slippery': True, 'render_mode': "human"})

    # Evaluate model's performance
    rewards_per_ep, timesteps_per_ep = evaluate_policy(model, vec_env, n_eval_episodes=10, return_episode_rewards=True)
    print("reward_per_ep:",rewards_per_ep)
    print("timesteps_per_ep:",timesteps_per_ep)
    print("mean_reward:",statistics.mean(rewards_per_ep))
    print("std_reward:",statistics.stdev(rewards_per_ep))
    print("mean_timesteps:",statistics.mean(timesteps_per_ep))
    print("std_timesteps:",statistics.stdev(timesteps_per_ep))

    # Visualize Model's actions
    obs = vec_env.reset()
    while True:
        action, _state = model.predict(obs, deterministic=True)
        obs, reward, done, info = vec_env.step(action)
        vec_env.render()
        if done:
            break
    # Close the environment
    vec_env.close()

    return

if __name__ == "__main__":
    main()