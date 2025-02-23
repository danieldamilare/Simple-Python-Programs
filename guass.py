import scipy.integrate
import numpy as np
import test
import random

def guassian(x, mu, sigma):
    factor1 =  (1.0 / (sigma * ((2 *np.pi) ** 0.5)))
    factor2 = np.e** -(((x-mu) ** 2)/ (2 * sigma ** 2))
    return factor1 * factor2

def check_empirical(mu_max, sigma_max, num_trials):
    for t in range(num_trials):
        mu = random.randint(-mu_max, mu_max +1)
        sigma = random.randint(1, sigma_max)
        print('For mu =', mu, 'and sigma =', sigma)
        for num_std in (1, 2, 3):
            area = scipy.integrate.quad(guassian, mu-num_std*sigma,
                                        mu+num_std * sigma,
                                        (mu, sigma))[0]
            print('  Fraction within', num_std, 'std =', round(area, 4))

def show_error_bars(min_exp, max_ep, num_trials):
    means, sds, x_vals = [], [], []
    for exp in range(min_exp, max_ep):
        x_vals.append(2**exp)
        frac_heads, mean, sd = test.flip_sim(2**exp, num_trials)
        means.append(mean)
        sds.append(sd)
    plt.errorbar(x_vals, means, yerr = 1.96 * np.array(sds))
    plt.semilogx()
    plt.title(f"Mean Fraction of Head({num_trials}) trials")
    plt.xlabel("Number of flips per trial")
    plt.ylabel("Fraction of heads & 95% confidence")

check_empirical(10, 10, 3)
