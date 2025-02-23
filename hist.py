import matplotlib.pyplot as plt
import random

random.seed(0)
vals = []
for i in range(1000):
    val1 = random.randrange(0, 101)
    val2 = random.randrange(0, 101)
    vals.append(val1 + val2)
plt.hist(vals, bins=30, ec='k')
plt.xlabel('Sum')
plt.ylabel('Frequency')
plt.title('Sum of Two Random Numbers')
plt.show()


