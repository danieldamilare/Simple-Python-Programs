import matplotlib.pyplot as plt

principal = 1000
interest_rate = 0.05
years = 20
values = []
for i in range(years + 1):
    values.append(principal)
    principal += principal*interest_rate
plt.plot(values, '-k', linewidth = 30)
plt.title('5% Growth, Compounded Anually', fontsize='xx-large')
plt.xlabel('Years of Compounding', fontsize='xx-small')
plt.ylabel('Values of Principal ($)')
plt.savefig('principal.png')
