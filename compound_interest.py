import matplotlib.pyplot as plt
import random

def compound_interest(principal: float, 
                      interest: float, 
                      year: int) -> float:
    principal_values = [principal]
    for i in range(year):
        cur = principal_values[-1]
        principal_values.append(cur + cur * interest)
    return principal_values

def plot_compound_interest(principal, interest, year):
    princip_val = compound_interest(principal, interest, year)
    print(princip_val)
    x_val = [x for x in range(year+1)]
    plt.title(f"Compound Interest growth of {principal} value at" +
              f"{interest} interest for {year} year")
    plt.ylabel("New Principal")
    plt.xlabel("Year")
    plt.plot(x_val, princip_val, 'r--')
    plt.grid(True, which='both')
    plt.show()

if __name__ == '__main__':
    plot_compound_interest(50000, 0.10, 100)
