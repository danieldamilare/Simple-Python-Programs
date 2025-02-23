import random
import matplotlib.pyplot as plt

def flip(num_flips):
    heads = 0
    for i in range(num_flips):
        if random.choice(('H', 'T')) == 'H':
            heads +=1
    return heads/float(num_flips)

def regress_to_mean(num_flips, num_trials):
    frac_heads = []
    for t in range(num_trials):
        frac_heads.append(flip(num_flips))
    extremes, next_trials = [], []
    for i in range(len(frac_heads) -1):
        if frac_heads[i] < 0.33 or frac_heads[i] > 0.66:
            extremes.append(frac_heads[i])
            next_trials.append(frac_heads[i+1])
    plt.plot(range(len(extremes)), extremes, 'ko', label = 'Extreme')
    plt.plot(range(len(next_trials)), next_trials, 'k^', label = 'Next Trial')
    plt.axhline(0.5)
    plt.ylim(0, 1)
    plt.xlim(-1, len(extremes) + 1)
    plt.xlabel('Extreme Example and Next Trial')
    plt.ylabel('Fraction Heads')
    plt.title('Regression to the Mean')
    plt.legend(loc = 'best')
    plt.show()


def flip_sim(num_flips_per_trial, num_trials):
    frac_heads  = []
    for i in range(num_trials):
        frac_heads.append(flip(num_flips_per_trial))
    mean = sum(frac_heads)/ len(frac_heads)
    return mean

def flip_plot(min_exp, max_exp):
    ratios, diffs, xAxis = [], [], [] 
    for exp in range(min_exp, max_exp+1):
        xAxis.append(2**exp)

    for num_flip in xAxis:
        num_heads = 0
        for n in range(num_flip):
            if  random.choice(( 'H', 'T' )) == 'H':
                num_heads += 1
        num_tails = num_flip - num_heads
        try:
            # print("Appending to diff and ratio")
            ratios.append(num_heads/num_tails)
            diffs.append(abs(num_heads - num_tails))
            # print("Diff is now", diffs)

        except ZeroDivisionError:
            # print("Zero Division Error")
            continue
    plt.title('Difference Between Heads and Tails')
    plt.xlabel('Number of Flips')
    plt.ylabel("Abs(#Heads - #Tails)")
    plt.xticks(rotation = 'vertical')
    # print(xAxis)
    # print(diffs)
    plt.yscale("log")
    plt.xscale("log")
    plt.plot(xAxis, diffs, 'ko')
    plt.figure()
    plt.title('Heads/Tails Ratios')
    plt.xlabel('Number of Flips')
    plt.ylabel('#Heads/#Tails')
    plt.xticks(rotation = 'vertical')
    plt.yscale("log")
    plt.xscale("log")
    plt.plot(xAxis, ratios, 'ko')

def variance(X):
    mean = sum(X)/len(X)
    total_x = 0.0
    for x in X:
        total_x += (x - mean) ** 2
    return total_x/len(X)

def std_dev(X):
    return variance(X)**0.5

def make_plot(x_vals, y_vals, title, x_label, y_label, style, log_x = False, log_y = False):
    plt.figure()
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.plot(x_vals, y_vals, style)
    if log_x:
        plt.semilogx()
    if log_y:
        plt.semilogy()

def run_trials(num_flips):
    num_heads = 0
    for n in range(num_flips):
        if random.choice(('H', 'T')) == 'H':
            num_heads += 1
    return (num_heads, num_flips - num_heads)

def flip_plot1(min_exp, max_exp, num_trials):
    ratios_means, diffs_means, ratios_SDs, diffs_SDs = [], [], [], []
    x_axis = [2**exp for exp in range(min_exp, max_exp+1)]
    for num_flips in x_axis:
        ratios, diffs = [], []
        for t in range(num_trials):
            num_heads, num_tails = run_trials(num_flips)
            ratios.append(num_heads/num_tails)
            diffs.append(num_heads - num_tails)

        ratios_means.append(sum(ratios)/len(ratios))
        diffs_means.append(sum(diffs)/len(diffs))
        ratios_SDs.append(std_dev(ratios))
        diffs_SDs.append(std_dev(diffs))
    title = f'Mean Heads/Tails Ratio({num_trials} Trials)'
    make_plot(x_axis, ratios_means, title,  'Num of Flips', 'Mean Head/Tails', 'ko', log_x = True)
    title = f'Mean Heads/Tails Ratio({num_trials} Trials)'
    make_plot(x_axis, ratios_SDs, title,  'Num of Flips', 'Standard deviation', 'ko', log_x = True, log_y=True)
    title = f'Mean abs(#Heads - #Tails) ({num_trials} Trials)'
    make_plot(x_axis, diffs_means, title,  'Num of Flips', 'Mean abs(#Heads - #Tails)', 'ko', log_x = True, log_y=True)
    title = f'Standard Deviation abs(#Heads - #Tails) ({num_trials} Trials)'
    make_plot(x_axis, diffs_SDs, title,  'Num of Flips', 'Standard Deviation', 'ko', log_x = True, log_y=True)
    


if __name__ == '__main__':
    # while(1):
        # num_flips_per_trial = int(input("How many flips per trial: "))
        # num_trial = int(input("Ente number of trial: "))
        # print("Mean = ", flip_sim(num_flips_per_trial, num_trial))
        # play_again = input("Do you want to try again: ").lower()
        # if len(play_again) > 0 and play_again[0] == 'n':
        #     break
    # regress_to_mean(15, 50)
    random.seed(0)
    # flip_plot(2, 20)
    flip_plot1(4, 20, 20)
    plt.show()
