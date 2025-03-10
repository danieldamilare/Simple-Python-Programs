
# generate the distribution of sum of the number generated by rolling a pair of dice
import random
import matplotlib.pylab as plt

def flip(num_flips):
    heads = 0
    for i in range(num_flips):
        if random.choice(('H', 'T')) == 'H':
            heads +=1
    return heads/float(num_flips)

def variance(X):
    mean = sum(X)/len(X)
    total_x = 0.0
    for x in X:
        total_x += (x - mean) ** 2
    return total_x/len(X)

def std_dev(X):
    return variance(X)**0.5

def flip_sim(num_flips_per_trial, num_trials):
    frac_heads  = []
    for i in range(num_trials):
        frac_heads.append(flip(num_flips_per_trial))
    mean = sum(frac_heads)/ len(frac_heads)
    sd = std_dev(frac_heads)
    return (frac_heads, mean, sd)


import matplotlib.pyplot as plt

def label_plot(num_flips, num_trials, mean, sd):
    plt.title(str(num_trials) + ' trials of ' + str(num_flips) + ' flips each')
    plt.xlabel('Fraction of Heads')
    plt.ylabel('Number of Trials')
    plt.annotate('Mean = ' + str(round(mean, 4)) +
                 '\nSD = ' + str(round(sd, 4)),
                 size='x-large', xycoords='axes fraction', xy=(0.67, 0.5))

def make_plots(num_flips1, num_flips2, num_trials):
    val1, mean1, sd1 = flip_sim(num_flips1, num_trials)
    plt.hist(val1, bins=20)
    x_min, x_max = plt.xlim()
    label_plot(num_flips1, num_trials, mean1, sd1)

    plt.figure()
    val2, mean2, sd2 = flip_sim(num_flips2, num_trials)
    plt.hist(val2, bins=20, ec='k')
    plt.xlim(x_min, x_max)
    label_plot(num_flips2, num_trials, mean2, sd2)

# make_plots(100, 1000, 100000)
plt.show()
