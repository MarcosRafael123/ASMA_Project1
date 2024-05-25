import gymnasium as gym
from enviroment.enviroment import FrozenLakeEnv

from stable_baselines3 import PPO
from gym.envs.registration import register
from stable_baselines3.common.env_util import make_vec_env
from stable_baselines3.common.evaluation import evaluate_policy
from stable_baselines3.common.vec_env import VecEnvWrapper
from stable_baselines3.common.vec_env import DummyVecEnv, VecMonitor

def main():

    env = make_vec_env(FrozenLakeEnv, n_envs=1)

    model = PPO("MlpPolicy", env, verbose=1,learning_rate=0.01,device='cuda')
    model.learn(total_timesteps=20_000,progress_bar=True)


    # Save the model
    # model.save("ppo_frozenLake")

    # Load the model
    # model = PPO.load("ppo_frozenLake_best_slip_v2")


    vec_env = make_vec_env(FrozenLakeEnv, n_envs=1, env_kwargs={'desc': None, 'map_name': "4x4", 'is_slippery': True, 'render_mode': "human"})


    mean_reward, std_reward = evaluate_policy(model, vec_env, n_eval_episodes=10)
    print("mean_reward:",mean_reward)
    print("std_reward:",std_reward)
    vec_env = model.get_env()

    # vec_env = model.get_env()
    obs = vec_env.reset()
    while True:
        action, _state = model.predict(obs, deterministic=True)
        obs, reward, done, info = vec_env.step(action)
        # vec_env.render("human")
        if done:
            break
    # Close the environment
    vec_env.close()

    return



if __name__ == "__main__":
    main()