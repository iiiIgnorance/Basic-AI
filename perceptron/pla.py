import pandas as pd
import numpy as np
import sys
from plot_db import visualize_scatter

def main():
    '''YOUR CODE GOES HERE'''
    data = pd.read_csv(sys.argv[1], header=None)
    training_data = np.array(data)
    result = open(sys.argv[2], "w")
    weights = [0, 0, 0]
    convergence = False
    result.write("{}, {}, {}".format(weights[0], weights[1], weights[2]) + "\n")

    while not convergence:
        old_weights = weights.copy()
        for row in training_data:
            function = weights[2] + weights[0] * row[0] + weights[1] * row[1]
            if row[2] * function <= 0:
                weights[0] += row[2] * row[0]
                weights[1] += row[2] * row[1]
                weights[2] += row[2]
        result.write("{}, {}, {}".format(weights[0], weights[1], weights[2]) + "\n")
        if old_weights == weights:
            convergence = True

    #visualize_scatter(df=data, weights=weights, title="Perceptron")


if __name__ == "__main__":
    """DO NOT MODIFY"""
    main()


