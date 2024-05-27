import gymnasium as gym
from enviroment.enviroment import FrozenLakeEnv

from sb3_contrib import ARS
from stable_baselines3.common.env_util import make_vec_env
from stable_baselines3.common.evaluation import evaluate_policy
from stable_baselines3.common.logger import configure

import os
import statistics

def main():

    # Create enviroment for training (no render)
    env = make_vec_env(FrozenLakeEnv, n_envs=1, monitor_dir="logs/ARS_monitor_logs", env_kwargs={'map_name': "5x5", 'is_slippery': True})
    
    # Set the logger to csv and stdout
    new_logger = configure("logs/ARS_logs", ["stdout", "csv"])

    # Create model, set the logger, and train the moodel
    model = ARS("MlpPolicy", env, verbose=1, learning_rate=0.01, device='cuda')
    model.set_logger(new_logger)
    model.learn(total_timesteps=20_000, progress_bar=True)

    # Save the model
    model.save("ARS_frozenLake")

    # Load the model
    # model = ARS.load("ARS_frozenLake_final")

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