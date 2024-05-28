import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import linregress
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF, ConstantKernel as C

def main():

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
    # plt.plot(x, y, 'bo', label='Data')
    plt.plot(x_pred, y_pred, 'r-', label='Fitted Curve')
    plt.fill_between(x_pred.flatten(), (y_pred - sigma).flatten(), (y_pred + sigma).flatten(), alpha=0.3, color='red')
    plt.xlabel('Episode')
    plt.ylabel('Reward')
    plt.title('Reward vs. Episode with Gaussian Process Regression')




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


    # Reward vs. Episode


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
    # plt.subplot(3, 1, 1)
    # plt.plot(df.index, df['r'], marker='o', linestyle='-', color='b')
    # plt.xlabel('Episode')
    # plt.ylabel('Reward')
    # plt.title('Reward vs. Episode')
    # plt.grid(True)

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
    # plt.subplot(3, 1, 2)
    # plt.plot(df.index, df['l'], marker='o', linestyle='-', color='g')
    # plt.xlabel('Episode')
    # plt.ylabel('Episode Length')
    # plt.title('Episode Length vs. Episode')
    # plt.grid(True)

    plt.tight_layout()
    plt.show()
    

    return

if __name__ == "__main__":
    main()