import math
import matplotlib.pyplot as plt
import random

def binomial_probability(k, n, prob_success, prob_failure):
    return (math.comb(n, k) * 
            prob_success ** k *
            prob_failure ** (n - k)
           )
def flip_probability(k, n):
    prob_success = 1/6
    prob_failure = 1 - prob_success
    return binomial_probability(k, n, prob_success, prob_failure)

def plot_flip(start: int, end: int):
    x_vals = []
    y_vals = []
    for i in range(start, end+1):
        y_vals.append(flip_probability(2, i))
        x_vals.append(i)
    plt.title("Probability of two 3's occuring in a fair die throw")
    plt.xlabel("No. of Throws")
    plt.ylabel("Probability")
    plt.grid(True, which='both')
    plt.plot(x_vals, y_vals, 'r-')
    plt.show()

if __name__ == '__main__':
    plot_flip(2, 100)
