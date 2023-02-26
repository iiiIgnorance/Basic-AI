import numpy as np
import pandas as pd
import sys

def main():
    """
    YOUR CODE GOES HERE
    Implement Linear Regression using Gradient Descent, with varying alpha values and numbers of iterations.
    Write to an output csv file the outcome betas for each (alpha, iteration #) setting.
    Please run the file as follows: python3 lr.py data2.csv, results2.csv
    """
    data = pd.read_csv(sys.argv[1], header=None)
    data[0] = (data[0] - data[0].mean()) / data[0].std()
    data[1] = (data[1] - data[1].mean()) / data[1].std()
    training_data = np.array(data)
    result = open(sys.argv[2], "w")
    alphas = [0.001, 0.005, 0.01, 0.05, 0.1, 0.5, 1, 5, 10]
    iteration = 100

    for alpha in alphas:
        b = [0, 0, 0]
        for i in range(iteration):
            sum = [0, 0, 0]
            for n in range(len(training_data)):
                sum[0] += b[0] + b[1] * training_data[n][0] + b[2] * training_data[n][1] - training_data[n][2]
                sum[1] += (b[0] + b[1] * training_data[n][0] + b[2] * training_data[n][1] - training_data[n][2]) * training_data[n][0]
                sum[2] += (b[0] + b[1] * training_data[n][0] + b[2] * training_data[n][1] - training_data[n][2]) * training_data[n][1]
            for j in range(len(b)):
                b[j] = b[j] - alpha * sum[j] / len((training_data))
        '''
        square = 0
        for n in range(len(training_data)):
            square += (b[0] + b[1] * training_data[n][0] + b[2] * training_data[n][1] - training_data[n][2]) ** 2
        R = square / (2 * len(training_data))
        print("alpha={},iteration=100: R=".format(alpha) + str(R))
        '''
        result.write("{}, {}, {}, {}, {}".format(alpha, iteration, b[0], b[1], b[2]) + "\n")

    alpha = 0.91
    b = [0, 0, 0]
    for i in range(90):
        sum = [0, 0, 0]
        for n in range(len(training_data)):
            sum[0] += b[0] + b[1] * training_data[n][0] + b[2] * training_data[n][1] - training_data[n][2]
            sum[1] += (b[0] + b[1] * training_data[n][0] + b[2] * training_data[n][1] - training_data[n][2]) * training_data[n][0]
            sum[2] += (b[0] + b[1] * training_data[n][0] + b[2] * training_data[n][1] - training_data[n][2]) * training_data[n][1]
        for j in range(len(b)):
            b[j] = b[j] - alpha * sum[j] / len((training_data))
    '''
    square = 0
    for n in range(len(training_data)):
        square += (b[0] + b[1] * training_data[n][0] + b[2] * training_data[n][1] - training_data[n][2]) ** 2
    R = square / (2 * len(training_data))
    print("alpha=0.91,iteration=90: R=" + str(R))
    '''
    result.write("{}, {}, {}, {}, {}".format(alpha, 90, b[0], b[1], b[2]) + "\n")



if __name__ == "__main__":
    main()