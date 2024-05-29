import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import linregress
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF, ConstantKernel as C
import seaborn as sns

def plot_train_data():

    logs_dir = "logs"
    logs_monitor_algo_file = "0.monitor.csv"
    logs_algos_dir = ["A2C", "ARS", "DQN", "PPO", "TRPO"]


    filename = logs_dir + "/" + logs_algos_dir[0]+"_monitor_logs/" + logs_monitor_algo_file
    # Load the data from CSV files
    df = pd.read_csv(filename,skiprows=2, names=['r', 'l', 't'])

    # Display the first few rows of the DataFrame to ensure it loaded correctly
    print(df.head())
    print(df.shape)

    # Plotting
    plt.figure(figsize=(14, 10))


    # ------------ Reward vs. Episode with Gaussian Process Regression ----------------
    # Extract the data for plotting
    x = df.index.values.reshape(-1, 1)  # Assuming index represents episodes
    y = df['r'].values.reshape(-1, 1)    # Assuming 'r' is the column for rewards

    # Define the kernel for the Gaussian Process Regression
    kernel = C(1.0, (1e-3, 1e3)) * RBF(10, (1e-2, 1e2))

    # Fit the Gaussian Process Regression model
    gpr = GaussianProcessRegressor(kernel=kernel, n_restarts_optimizer=10)
    gpr.fit(x, y)

    # Generate y values for the fitted curve
    x_pred = np.linspace(min(x), max(x), 100).reshape(-1, 1)
    y_pred, sigma = gpr.predict(x_pred, return_std=True)

    # Plot the data and the fitted curve
    plt.subplot(4, 1, 3)
    # plt.plot(x, y, 'bo', label='Data
    plt.plot(x_pred, y_pred, 'r-', label='Fitted Curve')
    plt.fill_between(x_pred.flatten(), (y_pred - sigma).flatten(), (y_pred + sigma).flatten(), alpha=0.3, color='red')
    plt.xlabel('Episode')
    plt.ylabel('Reward')
    plt.title('Reward vs. Episode with Gaussian Process Regression')
    # ----------------------------------------------------------------------------------


    # --------- Episode Length vs. Episode with Gaussian Process Regression ---------------
    # Extract the data for plotting
    x = df.index.values.reshape(-1, 1)  # Assuming index represents episodes
    y = df['l'].values.reshape(-1, 1)    # Assuming 'r' is the column for rewards

    # Define the kernel for the Gaussian Process Regression
    kernel = C(1.0, (1e-3, 1e3)) * RBF(10, (1e-2, 1e2))

    # Fit the Gaussian Process Regression model
    gpr = GaussianProcessRegressor(kernel=kernel, n_restarts_optimizer=10)
    gpr.fit(x, y)

    # Generate y values for the fitted curve
    x_pred = np.linspace(min(x), max(x), 100).reshape(-1, 1)
    y_pred, sigma = gpr.predict(x_pred, return_std=True)

    # Plot the data and the fitted curve
    plt.subplot(4, 1, 4)
    # plt.plot(x, y, 'bo', label='Data')
    plt.plot(x_pred, y_pred, 'r-', label='Fitted Curve')
    plt.fill_between(x_pred.flatten(), (y_pred - sigma).flatten(), (y_pred + sigma).flatten(), alpha=0.3, color='red')
    plt.xlabel('Episode')
    plt.ylabel('Episode Length')
    plt.title('Episode Length vs. Episode with Gaussian Process Regression')
    # ------------------------------------------------------------------------------------


    # ------------ Reward vs. Episode ----------------
    # Extract the data for plotting
    x = df.index  # Assuming index represents episodes
    y = df['r']   # Assuming 'r' is the column for rewards

    # Fit a linear regression line
    slope, intercept, r_value, p_value, std_err = linregress(x, y)
    line = slope * x + intercept

    # Plot the data and the regression line
    plt.subplot(4, 1, 1)
    # plt.plot(x, y, 'bo', label='Data')
    plt.plot(x, line, 'r-', label='Regression Line')
    plt.xlabel('Episode')
    plt.ylabel('Reward')
    plt.title('Reward vs. Episode with Linear Regression Line')
    # ---------------------------------------------


    # ------------ Length vs. Episode ----------------
    x = df.index  # Assuming index represents episodes
    y = df['l']   # Assuming 'r' is the column for rewards

    # Fit a linear regression line
    slope, intercept, r_value, p_value, std_err = linregress(x, y)
    line = slope * x + intercept

    # Episode Length vs. Episode
    plt.subplot(4, 1, 2)
    # plt.plot(x, y, 'bo', label='Data')
    plt.plot(x, line, 'r-', label='Regression Line')
    plt.xlabel('Episode')
    plt.ylabel('Episode Length')
    plt.title('Episode Length vs. Episode with Linear Regression Line')
    plt.tight_layout()
    plt.show()
    # ---------------------------------------------
    
    return




def plot_test():

    A2C = {
    "reward_per_ep": [-10.42, -10.42, -10.03, -10.09, -11.05, -10.39, -10.59, -10.09, -10.61, -10.26],
    "timesteps_per_ep": [43, 43, 4, 10, 106, 40, 60, 10, 62, 27],
    "mean_reward": -10.395,
    "std_reward": 0.30768851493388955,
    "mean_timesteps": 40.5,
    "std_timesteps": 30.76885149338893
    }

    ARS = { #Tenta dar o minimo numero de passos possível
    "reward_per_ep": [-10.02, -10.04, -10.03, -10.03, -10.02, -10.02, -10.02, -10.02, -10.02, -10.02],
    "timesteps_per_ep": [3, 5, 4, 4, 3, 3, 3, 3, 3, 3],
    "mean_reward": -10.024,
    "std_reward": 0.006992058987800862,
    "mean_timesteps": 3.4,
    "std_timesteps": 0.6992058987801011
    }

    DQN = {
    "reward_per_ep": [-10.59, -10.49, -11.23, -10.37, -11.17, -10.08, -10.1, -10.27, -10.24, -10.15],
    "timesteps_per_ep": [60, 50, 124, 38, 118, 9, 11, 28, 25, 16],
    "mean_reward": -10.469,
    "std_reward": 0.41855439046529885,
    "mean_timesteps": 47.9,
    "std_timesteps": 41.855439046529874
    }

    PPO = {
    "reward_per_ep": [499.88, -10.05, 499.91, 499.93, 499.9, 499.91, -10.07, 499.86, 499.88, 499.88],
    "timesteps_per_ep": [13, 6, 10, 8, 11, 10, 8, 15, 13, 13],
    "mean_reward": 397.903,
    "std_reward": 215.01538115782427,
    "mean_timesteps": 10.7,
    "std_timesteps": 2.8303906287138374
    }

    TRPO = {
    "reward_per_ep": [-10.04, 499.9, 499.93, -10.06, 499.9, 499.88, 499.9, -10.16, 499.88, -10.06],
    "timesteps_per_ep": [5, 11, 8, 7, 11, 13, 11, 17, 13, 7],
    "mean_reward": 295.907,
    "std_reward": 263.35168113506825,
    "mean_timesteps": 10.3,
    "std_timesteps": 3.591656999213594
    }


    algos = [A2C, ARS, DQN, PPO, TRPO]

    # Extracting mean rewards and standard deviations
    algorithms = ['A2C', 'ARS', 'DQN', 'PPO', 'TRPO']
    mean_rewards = [A2C["mean_reward"], ARS["mean_reward"], DQN["mean_reward"], PPO["mean_reward"], TRPO["mean_reward"]]
    std_rewards = [A2C["std_reward"], ARS["std_reward"], DQN["std_reward"], PPO["std_reward"], TRPO["std_reward"]]
    mean_timesteps = [A2C["mean_timesteps"], ARS["mean_timesteps"], DQN["mean_timesteps"], PPO["mean_timesteps"], TRPO["mean_timesteps"]]
    std_timesteps = [A2C["std_timesteps"], ARS["std_timesteps"], DQN["std_timesteps"], PPO["std_timesteps"], TRPO["std_timesteps"]]

    # Define colors for each bar
    colors = ['red', 'orange', 'purple', 'green', 'blue']

    # Create subplots
    fig, ax1 = plt.subplots(2, 1, figsize=(12, 16))

    # Plotting the mean rewards with standard deviation error bars
    ax1[0].bar(algorithms, mean_rewards, yerr=std_rewards, capsize=5, color=colors, alpha=0.7)
    ax1[0].set_xlabel('Algorithms')
    ax1[0].set_ylabel('Mean Reward')
    ax1[0].set_title('Mean Reward for Each Algorithm')
    ax1[0].set_ylim(-15, 500)

    # Plotting the mean timesteps with standard deviation error bars
    ax1[1].bar(algorithms, mean_timesteps, yerr=std_timesteps, capsize=5, color=colors, alpha=0.7)
    ax1[1].set_xlabel('Algorithms')
    ax1[1].set_ylabel('Mean Timesteps')
    ax1[1].set_title('Mean Timesteps for Each Algorithm')
    ax1[1].set_ylim(0, max(mean_timesteps) + max(std_timesteps) + 10)

    # Adjust layout for better fit
    plt.tight_layout()

    # Display the plot
    plt.show()

    return


def main():
    plot_train_data()
    plot_test()
    return




if __name__ == "__main__":
    main()