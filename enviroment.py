import gym

import gym
import numpy as np

class CustomMountainCar(gym.Wrapper):
    def __init__(self, env):
        super(CustomMountainCar, self).__init__(env)

    def reset(self,seed=None,options=None):
        # Modify the reset function if needed
        obs = self.env.reset(seed=seed,options=options)
        # Adjust observation if necessary
        return obs

    def step(self, action):
        obs, reward, terminated, truncated, info = self.env.step(action)
        
        # Custom reward calculation
        new_reward = self.calculate_reward(obs)
        
        return obs, new_reward, terminated,truncated, info
    
    def calculate_reward(self, state):
        # Custom reward calculation based on the state
        position, velocity = state
        goal_position = self.env.goal_position
        
        # Example: Sparse reward when the car reaches the goal

        # if position<-0.5:
        #     progress = 0
        # else:   
        progress = abs(velocity*2)
        # if progress < 0:
        #     progress = 0

        if position >= goal_position:
            return 5000.0
        else:
            return progress


class LunarLanderWrapper(gym.Wrapper):
    def __init__(self, env):
        super(LunarLanderWrapper, self).__init__(env)
        # Modify the environment as needed in the constructor

    def step(self, action):
        # Modify the step function if needed
        obs, reward, done, info = self.env.step(action)
        # Adjust reward or observation if necessary
        return obs, reward, done, info

    def reset(self):
        # Modify the reset function if needed
        obs = self.env.reset()
        # Adjust observation if necessary
        return obs