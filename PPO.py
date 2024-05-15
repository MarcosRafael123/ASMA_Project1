import gym
from enviroment import CustomMountainCar 

from stable_baselines3 import PPO
from stable_baselines3.common.evaluation import evaluate_policy


def main():
    env = gym.make('CarRacing-v2',render_mode="human")
    # env = CustomMountainCar(env)

    model = PPO("MlpPolicy", env, verbose=1,learning_rate=0.01)
    model.learn(total_timesteps=10_000,progress_bar=True)


    # model.save("ppo_lunar_lander_model.zip")


    mean_reward, std_reward = evaluate_policy(model, model.get_env(), n_eval_episodes=10)
    print("mean_reward:",mean_reward)
    print("std_reward:",std_reward)

    # model.save("ppo_cartpole")
    # del model
    # model = PPO.load("ppo_cartpole")

    # sem treino
    # mean_reward: -565.0480255
    # std_reward: 247.50064029774984


    # nao faz diferença model=

    # 10000 time steps sem model=
    # mean_reward: -2716.0203403
    # std_reward: 435.8175916772218
    # mean_reward: -1070.9660986
    # std_reward: 736.0924835693681

    # 10000 time steps com model=
    # mean_reward: -761.2811931
    # std_reward: 636.6640700309131
    # mean_reward: -2875.8595118
    # std_reward: 1074.4959584463631


    # Saved PPO model
    # mean_reward: -306.1836278
    # std_reward: 47.752289706135215


    # car montain 10000
    # mean_reward: -200.0
    # std_reward: 0.0
    # mean_reward: -200.0
    # std_reward: 0.0

    # car montain continous 10000
    # mean_reward: -0.0431926
    # std_reward: 0.00016357395880762873

    # car montain continous 10000 -> lr=0.01
    # mean_reward: -0.10652239999999999
    # std_reward: 4.959677408864378e-05


    # cartpole
    # mean_reward: 351.4
    # std_reward: 121.82052372240074
    # mean_reward: 453.9
    # std_reward: 80.647938597338


    vec_env = model.get_env()
    obs = vec_env.reset()
    while True:
        action, _states = model.predict(obs)
        obs, rewards, done, info = vec_env.step(action)
        vec_env.render("human")
        if done:
            break

    vec_env.close()
    return


if __name__ == "__main__":
    main()