import numpy as np
import matplotlib.pyplot as plt

# print(y)

y = [1, 2, 3, 4, 5]

plt.figure()
plt.plot(range(1, len(y) + 1), y)
plt.yscale("linear")  # Logarithmic scale on y-axis
plt.xlabel("Linear Scale")
plt.ylabel("Linear Scale")
plt.title("Linear Scale Example")
plt.grid(True, which='both', linestyle='--', linewidth = 3)
plt.figure()
plt.yscale("log")  # Logarithmic scale on y-axis
plt.xlabel("Log Scale")
plt.ylabel("Linear Scale")
plt.title("Log Scale Example")
plt.plot(range(1, len(y) + 1), y)
plt.grid(True, which='both', linestyle='--', linewidth = 1)
plt.show()
