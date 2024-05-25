import gymnasium as gym
from enviroment.enviroment import FrozenLakeEnv

from stable_baselines3 import PPO
from stable_baselines3.common.env_util import make_vec_env
from stable_baselines3.common.vec_env.vec_monitor import VecMonitor
from stable_baselines3.common.evaluation import evaluate_policy
from stable_baselines3.common.logger import configure

import os
import statistics

def main():

    env = make_vec_env(FrozenLakeEnv, n_envs=1, monitor_dir="logs/PPO_monitor_logs", env_kwargs={'map_name': "5x5", 'is_slippery': True})
    
    # Set the logger to csv and stdout
    new_logger = configure("logs/PPO_logs", ["stdout", "csv"])


    model = PPO("MlpPolicy", env, verbose=1,learning_rate=0.01,device='cuda')
    model.set_logger(new_logger)
    model.learn(total_timesteps=20_000,progress_bar=True)

    # While training we will get two types of logs
    # PPO_monitor_logs -> writes a row (reward,length,time) for every training episode
    # PPO_logs (logger) -> writes a row with some training info, every (log_interval) training iteration (log_interval default is 1, so one row is written for every (log_interval*n_steps*n_envs) timesteps) 
    #(n_steps depends on algo used (PPO default is 2048 steps)) (example: if log_interval=1 and n_steps for the algorithm is 2048, the logger will write a row every 2048 timesteps)
    # more info about logger stats in https://stable-baselines3.readthedocs.io/en/master/common/logger.html

    # Save the model
    # model.save("ppo_frozenLake")

    # Load the model
    # model = PPO.load("ppo_frozenLake_best_slip_v2")

    
    vec_env = make_vec_env(FrozenLakeEnv, n_envs=1, env_kwargs={'desc': None, 'map_name': "5x5", 'is_slippery': True, 'render_mode': "human"})


    rewards_per_ep, timesteps_per_ep = evaluate_policy(model, vec_env, n_eval_episodes=10, return_episode_rewards=True)
    print("reward_per_ep:",rewards_per_ep)
    print("timesteps_per_ep:",timesteps_per_ep)
    print("mean_reward:",statistics.mean(rewards_per_ep))
    print("std_reward:",statistics.stdev(rewards_per_ep))
    print("mean_timesteps:",statistics.mean(timesteps_per_ep))
    print("std_timesteps:",statistics.stdev(timesteps_per_ep))

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