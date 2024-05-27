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



Added a new map
changed probability of slipping 30% (15% in each opposite dir) 
Added penalty for each step -> Had to reinforce reward for reaching goal, makes agent more prone to explore.




A2C:
reward_per_ep: [-10.64, -10.48, -10.34, -10.11, -10.08, -10.59, -11.05, -10.31, -10.44, -10.62]
timesteps_per_ep: [65, 49, 35, 12, 9, 60, 106, 32, 45, 63]
mean_reward: -10.466
std_reward: 0.2842612257140332
mean_timesteps: 47.6
std_timesteps: 28.426122571403305

ARS: -> Tenta dar o minimo numero de passos possível
reward_per_ep: [-10.02, -10.05, -10.03, -10.03, -10.02, -10.03, -10.02, -10.04, -10.03, -10.02]
timesteps_per_ep: [3, 6, 4, 4, 3, 4, 3, 5, 4, 3]
mean_reward: -10.029
std_reward: 0.009944289260117737
mean_timesteps: 3.9
std_timesteps: 0.9944289260117531

DQN:
reward_per_ep: [-10.24, -10.71, -10.52, -10.56, -11.82, -10.23, -10.13, -10.26, -10.08, -10.28]
timesteps_per_ep: [25, 72, 53, 57, 183, 24, 14, 27, 9, 29]
mean_reward: -10.483
std_reward: 0.5107086579776511
mean_timesteps: 49.3
std_timesteps: 51.0708657977651

PPO:
reward_per_ep: [499.91, 499.92, -10.17, -10.09, 499.91, -10.04, 499.89, 499.91, 499.91, 499.93]
timesteps_per_ep: [10, 9, 18, 10, 10, 5, 12, 10, 10, 8]
mean_reward: 346.908
std_reward: 246.35892734878607
mean_timesteps: 10.2
std_timesteps: 3.2930904093942583

TRPO:
reward_per_ep: [-10.04, -10.03, -10.09, 499.93, 499.91, 499.93, -10.06, 499.92, -10.04, 499.91]
timesteps_per_ep: [5, 4, 10, 8, 10, 8, 7, 9, 5, 10]
mean_reward: 244.934
std_reward: 268.7788443725105
mean_timesteps: 7.6
std_timesteps: 2.270584848790187




