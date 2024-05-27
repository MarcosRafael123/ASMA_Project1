# ASMA_Project1

## Compilation and execution

- Activate virtual enviroment (python 3.9.5)
- Install requirements if needed: pip install -r requirements.txt
- Run the program: python 


Install venv python3.9.5
Install Depencies -> Had to install swig, because of error during installation.
pip install gymnasium
pip install gymnasium[box2d] -> For 'LunarLander-v2' Enviroment
pip install stable-baselines3
pip install stable-baselines3[extra]
pip install sb3-contrib -> Adds experimental algos: TRPO


Changes to enviroment
Added a new map
changed probability of slipping 30% (15% in each opposite dir) 
Added penalty for each step -> Had to reinforce reward for reaching goal, makes agent more prone to explore.
    timestep: -0.01
    hole: -10.0
    goal: 500.0


Training:
trained with lr=0.01
around 20000 timesteps

running every algo:
python .\A2C.py
python .\ARS.py
python .\DQN.py
python .\PPO.py
python .\TRPO.py



A2C:
reward_per_ep: [-10.42, -10.42, -10.03, -10.09, -11.05, -10.39, -10.59, -10.09, -10.61, -10.26]
timesteps_per_ep: [43, 43, 4, 10, 106, 40, 60, 10, 62, 27]
mean_reward: -10.395
std_reward: 0.30768851493388955
mean_timesteps: 40.5
std_timesteps: 30.76885149338893

ARS: -> Tenta dar o minimo numero de passos possível
reward_per_ep: [-10.02, -10.04, -10.03, -10.03, -10.02, -10.02, -10.02, -10.02, -10.02, -10.02]
timesteps_per_ep: [3, 5, 4, 4, 3, 3, 3, 3, 3, 3]
mean_reward: -10.024
std_reward: 0.006992058987800862
mean_timesteps: 3.4
std_timesteps: 0.6992058987801011

DQN:
reward_per_ep: [-10.59, -10.49, -11.23, -10.37, -11.17, -10.08, -10.1, -10.27, -10.24, -10.15]
timesteps_per_ep: [60, 50, 124, 38, 118, 9, 11, 28, 25, 16]
mean_reward: -10.469
std_reward: 0.41855439046529885
mean_timesteps: 47.9
std_timesteps: 41.855439046529874

PPO:
reward_per_ep: [499.88, -10.05, 499.91, 499.93, 499.9, 499.91, -10.07, 499.86, 499.88, 499.88]
timesteps_per_ep: [13, 6, 10, 8, 11, 10, 8, 15, 13, 13]
mean_reward: 397.903
std_reward: 215.01538115782427
mean_timesteps: 10.7
std_timesteps: 2.8303906287138374

TRPO:
reward_per_ep: [-10.04, 499.9, 499.93, -10.06, 499.9, 499.88, 499.9, -10.16, 499.88, -10.06]
timesteps_per_ep: [5, 11, 8, 7, 11, 13, 11, 17, 13, 7]
mean_reward: 295.907
std_reward: 263.35168113506825
mean_timesteps: 10.3
std_timesteps: 3.591656999213594




